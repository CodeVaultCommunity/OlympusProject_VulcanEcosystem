"""An intentionally non-Vulcan application: functions and a class share one source.

Its only integration with TaskBoard is the published HTTP contract. There are
no imports of TaskBoard components and no access to its SQLite file.
"""

import argparse
import functools
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


def fetch_tasks(upstream_url, token):
    request = Request(upstream_url.rstrip("/") + "/tasks", headers={"Authorization": "Bearer " + token})
    with urlopen(request, timeout=5) as response:
        payload = json.load(response)
    if not isinstance(payload, dict) or not isinstance(payload.get("tasks"), list):
        raise ValueError("invalid_upstream_contract")
    for task in payload["tasks"]:
        if not isinstance(task, dict) or not isinstance(task.get("task_id"), str) or not isinstance(task.get("title"), str) or not isinstance(task.get("completed"), bool):
            raise ValueError("invalid_upstream_task")
    return payload["tasks"]


def summarize_tasks(tasks):
    completed = sum(task["completed"] for task in tasks)
    return {"total": len(tasks), "completed": completed, "pending": len(tasks) - completed}


def create_report(upstream_url, token):
    return summarize_tasks(fetch_tasks(upstream_url, token))


class ReportsHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, upstream_url, token, instance_id="standalone", **kwargs):
        self.upstream_url = upstream_url
        self.token = token
        self.instance_id = instance_id
        super().__init__(*args, **kwargs)

    def send_json(self, status, payload):
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/health":
            self.send_json(200, {"app": "LegacyReports", "ready": True, "instance_id": self.instance_id})
        elif path in ("/", "/report"):
            try:
                self.send_json(200, create_report(self.upstream_url, self.token))
            except (HTTPError, URLError, ValueError, OSError):
                self.send_json(502, {"error": "upstream_unavailable_or_invalid"})
        else:
            self.send_json(404, {"error": "route_not_found"})

    def log_message(self, format, *args):
        return


def main(argv=None):
    parser = argparse.ArgumentParser(description="Existing reporting code integrated through a public HTTP boundary")
    parser.add_argument("--upstream", default="http://127.0.0.1:8765")
    parser.add_argument("--token", default=os.environ.get("TASKBOARD_READER_TOKEN", "demo-reader"))
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("report")
    serve = commands.add_parser("serve")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8766)
    serve.add_argument("--instance-id", default="standalone")
    args = parser.parse_args(argv)
    if args.command == "report":
        try:
            print(json.dumps(create_report(args.upstream, args.token)))
        except (HTTPError, URLError, ValueError, OSError):
            print(json.dumps({"error": "upstream_unavailable_or_invalid"}))
            return 5
        return 0
    handler = functools.partial(ReportsHandler, upstream_url=args.upstream, token=args.token, instance_id=args.instance_id)
    with ThreadingHTTPServer((args.host, args.port), handler) as server:
        print(f"LegacyReports: http://{args.host}:{server.server_port}/report", flush=True)
        try:
            server.serve_forever(poll_interval=0.2)
        except KeyboardInterrupt:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
