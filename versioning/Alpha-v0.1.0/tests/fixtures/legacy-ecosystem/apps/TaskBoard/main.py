"""Technical process entry point; core operations live in their own class files."""

import argparse
import functools
import json
import os
from pathlib import Path
import sqlite3
import socket
import sys
from http.server import ThreadingHTTPServer

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from apps.TaskBoard.boundaries.Boundary_Cli import Boundary_Cli
from apps.TaskBoard.boundaries.Boundary_Http import Boundary_Http
from apps.TaskBoard.composition.AppComposition import AppComposition


def main(argv: list[str] | None = None) -> int:
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description="TaskBoard: the same core through CLI or HTTP")
    parser.add_argument("--db", default=".runtime/tasks.sqlite3")
    parser.add_argument("--token", default=os.environ.get("TASKBOARD_TOKEN"))
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list")
    create = commands.add_parser("create")
    create.add_argument("--title", required=True)
    complete = commands.add_parser("complete")
    complete.add_argument("task_id")
    serve = commands.add_parser("serve")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8765)
    serve.add_argument("--instance-id", default="standalone")
    args = parser.parse_args(argv)
    db_path = Path(args.db)
    if not db_path.is_absolute():
        db_path = root / db_path
    try:
        app = AppComposition(str(db_path), os.environ.get("TASKBOARD_EDITOR_TOKEN", "demo-editor"),
                             os.environ.get("TASKBOARD_READER_TOKEN", "demo-reader"))
    except ValueError as error:
        parser.exit(2, f"configuration_error: {error}\n")
    except (sqlite3.Error, OSError):
        print(json.dumps({"error": "storage_unavailable"}), file=sys.stderr)
        return 5
    if args.command == "serve":
        handler = functools.partial(Boundary_Http, create_task=app.create_task,
            list_tasks=app.list_tasks, complete_task=app.complete_task,
            resolve_actor=app.resolveActor, instance_id=args.instance_id)
        with ThreadingHTTPServer((args.host, args.port), handler, bind_and_activate=False) as server:
            if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
                server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
                server.allow_reuse_address = False
            server.server_bind()
            server.server_activate()
            print(f"TaskBoard: http://{args.host}:{server.server_port}", flush=True)
            try:
                server.serve_forever(poll_interval=0.2)
            except KeyboardInterrupt:
                pass
        return 0
    boundary = Boundary_Cli(app.create_task, app.list_tasks, app.complete_task, app.resolveActor)
    return boundary.run(args.command, args.token, getattr(args, "title", None), getattr(args, "task_id", None))


if __name__ == "__main__":
    raise SystemExit(main())
