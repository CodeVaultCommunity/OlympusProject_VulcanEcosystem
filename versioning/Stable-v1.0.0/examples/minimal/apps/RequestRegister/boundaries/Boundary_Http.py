"""Loopback-only demonstration transport; no production identity provider is supplied."""
from http.server import BaseHTTPRequestHandler
import json

class Boundary_Http(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/health":
            self.respond(200, {"status": "ready", "instance": self.server.instance_id})
        else:
            self.respond(404, {"error": "NOT_FOUND"})

    def do_POST(self) -> None:
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 65536:
                raise ValueError("invalid_body_length")
            self.connection.settimeout(5)
            payload = json.loads(self.rfile.read(length))
        except (ValueError, UnicodeError, OSError):
            self.respond(400, {"error": "INVALID_JSON"})
            return
        authorization = self.headers.get("Authorization", "")
        token = authorization[7:] if authorization.startswith("Bearer ") else None
        status, body = self.server.boundary.invoke(self.path.removeprefix("/"), payload, token)
        self.respond(status, body)

    def respond(self, status: int, body: dict) -> None:
        data = json.dumps(body, ensure_ascii=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args) -> None:
        pass
