"""Concrete single-app ecosystem entry; registration is explicit, not folder discovery."""
import argparse
from http.server import HTTPServer
import json
import math
import os
from pathlib import Path
import socket
import sys
import time
import uuid
from apps.RequestRegister.composition.AppComposition import AppComposition
from apps.RequestRegister.boundaries.Boundary_Json import Boundary_Json
from apps.RequestRegister.boundaries.Boundary_Http import Boundary_Http

ROOT = Path(__file__).resolve().parent
REGISTRY = {"RequestRegister": {"default_mode": "http", "modes": ["http", "cli"], "dependencies": []}}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["list", "start"])
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--all", action="store_true")
    selection.add_argument("--apps", nargs="+", choices=list(REGISTRY))
    parser.add_argument("--mode", choices=["http", "cli"], default="http")
    parser.add_argument("--db", type=Path, default=ROOT / "work/demo.sqlite3")
    parser.add_argument("--board", default="board-A")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--duration", type=float)
    parser.add_argument("--operation")
    parser.add_argument("--payload", default="{}")
    args = parser.parse_args(argv)
    if args.command == "list":
        print(json.dumps(REGISTRY, indent=2))
        return 0
    if not 0 <= args.port <= 65535 or args.duration is not None and (not math.isfinite(args.duration) or args.duration <= 0):
        parser.error("invalid port or duration")
    # Paths are explicit; default storage is local to this ecosystem, independent of cwd.
    args.db.parent.mkdir(parents=True, exist_ok=True)
    try:
        app = AppComposition(str(args.db), board_id=args.board, token=os.environ.get("VULCAN_DEMO_TOKEN", "demo-editor"))
        boundary = Boundary_Json(app)
        if args.mode == "cli":
            if not args.operation:
                parser.error("--operation is required for CLI mode")
            status, body = boundary.invoke(args.operation, json.loads(args.payload), os.environ.get("VULCAN_CALLER_TOKEN"))
            print(json.dumps(body, ensure_ascii=True))
            return 0 if status == 200 else 1
        server = HTTPServer(("127.0.0.1", args.port), Boundary_Http, bind_and_activate=False)
        try:
            # Windows must refuse sharing a foreign listening port.
            if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
                server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
                server.allow_reuse_address = False
            server.server_bind()
            server.server_activate()
            server.boundary = boundary
            server.instance_id = str(uuid.uuid4())
            server.timeout = 0.1
            print(json.dumps({"ready": "RequestRegister", "port": server.server_port, "instance": server.instance_id}), flush=True)
            deadline = time.monotonic() + args.duration if args.duration else None
            while deadline is None or time.monotonic() < deadline:
                server.handle_request()
        finally:
            server.server_close()
        return 0
    except KeyboardInterrupt:
        return 130
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
