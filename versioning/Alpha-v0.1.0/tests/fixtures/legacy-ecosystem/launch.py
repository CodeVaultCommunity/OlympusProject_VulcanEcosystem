"""Example-specific process composition; not a required Vulcan runtime.

The selected HTTP processes are direct children owned by this launcher. No
container daemon or unrelated process is stopped. Application contracts are
referenced in Minerva; these declarations only select concrete runtime modes.
"""

import argparse
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen
import uuid


APP_DEPENDENCIES = {"TaskBoard": [], "LegacyReports": ["TaskBoard"]}


def planApps(selected, dependencies=None):
    """Expand required dependencies in a stable order, rejecting cycles."""
    dependencies = APP_DEPENDENCIES if dependencies is None else dependencies
    result, active, visited = [], set(), set()

    def visit(app_id):
        if app_id not in dependencies:
            raise ValueError("unknown_app: " + app_id)
        if app_id in active:
            raise ValueError("startup_dependency_cycle: " + app_id)
        if app_id in visited:
            return
        active.add(app_id)
        for dependency in dependencies[app_id]:
            visit(dependency)
        active.remove(app_id)
        visited.add(app_id)
        result.append(app_id)

    for app_id in sorted(selected):
        visit(app_id)
    return result


def waitReady(process, url, app_id, instance_id, peers=(), timeout=10.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"{app_id} exited before readiness (code {process.returncode})")
        if any(peer.poll() is not None for peer in peers):
            raise RuntimeError("An owned dependency exited during startup")
        try:
            with urlopen(url, timeout=min(0.4, timeout)) as response:
                data = json.load(response)
            if (isinstance(data, dict) and data.get("app") == app_id
                    and data.get("ready") is True and data.get("instance_id") == instance_id
                    and process.poll() is None):
                return
        except (URLError, OSError, ValueError):
            pass
        time.sleep(0.05)
    raise RuntimeError(f"{app_id} did not become ready within {timeout:g}s")


def stopOwned(processes):
    for process in reversed(processes):
        if process.poll() is None:
            try:
                process.terminate()
            except ProcessLookupError:
                pass
    for process in reversed(processes):
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=3)


def handleStop(signum, frame):
    raise KeyboardInterrupt


def main(argv=None):
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Launch the example's default modes with explicit ownership")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list")
    start = commands.add_parser("start")
    selection = start.add_mutually_exclusive_group(required=True)
    selection.add_argument("--all", action="store_true")
    selection.add_argument("--apps", nargs="+", metavar="APP")
    start.add_argument("--task-port", type=int, default=8765)
    start.add_argument("--report-port", type=int, default=8766)
    start.add_argument("--db", default=".runtime/tasks.sqlite3")
    start.add_argument("--duration", type=float, help="Stop after this many seconds of readiness")
    start.add_argument("--startup-timeout", type=float, default=10.0)
    args = parser.parse_args(argv)
    if args.command == "list":
        print(json.dumps({"apps": [
            {"id": name, "default_mode": "http", "other_mode": "cli", "startup_dependencies": required}
            for name, required in APP_DEPENDENCIES.items()
        ], "dependency_policy": "expand_required", "host": "127.0.0.1"}, indent=2))
        return 0
    selected = set(APP_DEPENDENCIES) if args.all else {part for value in args.apps for part in value.split(",")}
    try:
        plan = planApps(selected)
    except ValueError as error:
        parser.error(str(error))
    if args.duration is not None and (not math.isfinite(args.duration) or args.duration < 0):
        parser.error("--duration must be finite and nonnegative")
    if not math.isfinite(args.startup_timeout) or args.startup_timeout <= 0:
        parser.error("--startup-timeout must be finite and positive")
    if not 1 <= args.task_port <= 65535 or not 1 <= args.report_port <= 65535:
        parser.error("ports must be between 1 and 65535")
    if args.task_port == args.report_port and "LegacyReports" in plan:
        parser.error("TaskBoard and LegacyReports require different ports")
    if "TaskBoard" in plan and "TaskBoard" not in selected:
        print("Including TaskBoard:http, required by LegacyReports:http.", flush=True)
    db_path = Path(args.db)
    if not db_path.is_absolute():
        db_path = root / db_path
    instance_id = uuid.uuid4().hex
    task_url, report_url = f"http://127.0.0.1:{args.task_port}", f"http://127.0.0.1:{args.report_port}"
    runtime = {
        "TaskBoard": ([sys.executable, str(root / "apps/TaskBoard/main.py"), "--db", str(db_path),
                       "serve", "--port", str(args.task_port), "--instance-id", instance_id], task_url),
        "LegacyReports": ([sys.executable, str(root / "apps/LegacyReports/reports.py"), "--upstream", task_url,
                           "serve", "--port", str(args.report_port), "--instance-id", instance_id], report_url),
    }
    processes = []
    previous_handler = signal.signal(signal.SIGTERM, handleStop)
    try:
        for app_id in plan:
            command, url = runtime[app_id]
            process = subprocess.Popen(command, cwd=root, stdin=subprocess.DEVNULL, env=os.environ.copy())
            previous_processes = tuple(processes)
            processes.append(process)
            waitReady(process, url + "/health", app_id, instance_id, previous_processes, args.startup_timeout)
            print(f"Ready: {app_id} ({url})", flush=True)
        deadline = time.monotonic() + args.duration if args.duration is not None else None
        print("Selected apps are ready. Ctrl+C stops only this launcher's direct children.", flush=True)
        while deadline is None or time.monotonic() < deadline:
            if any(process.poll() is not None for process in processes):
                raise RuntimeError("An owned app exited; stopping the remaining owned apps")
            time.sleep(0.05)
        return 0
    except KeyboardInterrupt:
        return 0
    except (OSError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        return 1
    finally:
        stopOwned(processes)
        signal.signal(signal.SIGTERM, previous_handler)


if __name__ == "__main__":
    raise SystemExit(main())
