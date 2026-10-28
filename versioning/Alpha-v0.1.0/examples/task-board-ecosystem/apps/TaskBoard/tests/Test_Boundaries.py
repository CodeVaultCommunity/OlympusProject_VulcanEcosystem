"""Supporting checks for channel projection and interoperability, beyond the three ADVS identities."""

from contextlib import redirect_stderr, redirect_stdout
import functools
from http.server import ThreadingHTTPServer
import io
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from apps.TaskBoard.boundaries.Boundary_Http import Boundary_Http
from apps.TaskBoard.boundaries.Boundary_Cli import Boundary_Cli
from apps.TaskBoard.composition.AppComposition import AppComposition


class Test_Boundaries(unittest.TestCase):
    def setUp(self) -> None:
        environment = patch.dict(os.environ, {"TASKBOARD_EDITOR_TOKEN": "demo-editor", "TASKBOARD_READER_TOKEN": "demo-reader"})
        environment.start()
        self.addCleanup(environment.stop)
        self.temp_directory = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.temp_directory.name) / "tasks.sqlite3")
        self.app = AppComposition(self.db_path)
        handler = functools.partial(Boundary_Http, create_task=self.app.create_task,
            list_tasks=self.app.list_tasks, complete_task=self.app.complete_task,
            resolve_actor=self.app.resolveActor, instance_id="test")
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.server.server_port}"
        self.root = Path(__file__).resolve().parents[3]

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.temp_directory.cleanup()

    def requestData(self, path, token="demo-editor", data=None):
        encoded = json.dumps(data).encode() if data is not None else None
        request = Request(self.url + path, data=encoded, headers={"Authorization": "Bearer " + token,
            "Content-Type": "application/json"})
        with urlopen(request, timeout=3) as response:
            return response.status, json.load(response)

    def testHttpCliAndLegacySharePublicContracts(self) -> None:
        status, task = self.requestData("/tasks", data={"title": "Created through HTTP"})
        self.assertEqual(status, 201)
        process = subprocess.run([sys.executable, str(self.root / "apps/TaskBoard/main.py"),
            "--db", self.db_path, "--token", "demo-reader", "list"], cwd=self.root,
            capture_output=True, text=True, timeout=5)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(json.loads(process.stdout)["tasks"][0]["task_id"], task["task_id"])
        boundary = Boundary_Cli(self.app.create_task, self.app.list_tasks, self.app.complete_task, self.app.resolveActor)
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(boundary.run("complete", "demo-editor", task_id=task["task_id"]), 0)
        self.assertTrue(self.requestData("/tasks", token="demo-reader")[1]["tasks"][0]["completed"])
        report = subprocess.run([sys.executable, str(self.root / "apps/LegacyReports/reports.py"),
            "--upstream", self.url, "report"], cwd=self.root, capture_output=True, text=True, timeout=5)
        self.assertEqual(report.returncode, 0, report.stderr)
        self.assertEqual(json.loads(report.stdout), {"total": 1, "completed": 1, "pending": 0})

    def testChannelRejectsUntrustedOrInsufficientContext(self) -> None:
        for token in ["unknown", "unknown-ç", "demo-reader", ""]:
            with self.subTest(token=token), self.assertRaises(HTTPError) as error:
                self.requestData("/tasks", token=token, data={"title": "Must not be stored"})
            self.assertEqual(error.exception.code, 403)
        with self.assertRaises(HTTPError) as error:
            self.requestData("/tasks", token="unknown", data={"title": "Attempt", "permissions": ["tasks:create"]})
        self.assertEqual(error.exception.code, 422)
        self.assertEqual(self.requestData("/tasks")[1], {"tasks": []})
        boundary = Boundary_Cli(self.app.create_task, self.app.list_tasks, self.app.complete_task, self.app.resolveActor)
        output = io.StringIO()
        with redirect_stderr(output):
            self.assertEqual(boundary.run("create", "demo-reader", title="Denied"), 3)
        self.assertEqual(json.loads(output.getvalue()), {"error": "forbidden"})
        task = self.requestData("/tasks", data={"title": "Must remain pending"})[1]
        before = self.requestData("/tasks", token="demo-reader")[1]
        process = subprocess.run([sys.executable, str(self.root / "apps/TaskBoard/main.py"),
            "--db", self.db_path, "--token", "demo-reader", "complete", task["task_id"]],
            cwd=self.temp_directory.name, capture_output=True, text=True, timeout=5)
        self.assertEqual(process.returncode, 3)
        self.assertEqual(json.loads(process.stderr), {"error": "forbidden"})
        self.assertEqual(process.stdout, "")
        self.assertFalse(task["completed"])
        self.assertEqual(self.requestData("/tasks", token="demo-reader")[1], before)

    def testBrowserPageAndHttpFailureProjection(self) -> None:
        with urlopen(self.url, timeout=3) as response:
            self.assertIn("Vulcan", response.read().decode())
        for data in [{"title": ""}, {"title": "x" * 121}, {"title": "ok", "role": "admin"}]:
            with self.subTest(data=data), self.assertRaises(HTTPError) as error:
                self.requestData("/tasks", data=data)
            self.assertEqual(error.exception.code, 422)
        with self.assertRaises(HTTPError) as error:
            self.requestData("/tasks/missing/complete", data={})
        self.assertEqual(error.exception.code, 404)

    def testMalformedBodiesAndStorageProjection(self) -> None:
        for body in [b"not-json", b"[]", b"x" * 8193]:
            request = Request(self.url + "/tasks", data=body, headers={"Authorization": "Bearer demo-editor"})
            with self.subTest(body_size=len(body)), self.assertRaises(HTTPError) as error:
                urlopen(request, timeout=3)
            self.assertEqual(error.exception.code, 422)
        with patch.object(self.app.create_task, "createTask", side_effect=sqlite3.OperationalError("private storage detail")):
            with self.assertRaises(HTTPError) as error:
                self.requestData("/tasks", data={"title": "task"})
            self.assertEqual(error.exception.code, 503)
            self.assertEqual(json.load(error.exception), {"error": "storage_unavailable"})

    def testCliExitCodesAndArbitraryWorkingDirectory(self) -> None:
        entry = self.root / "apps/TaskBoard/main.py"
        for arguments, expected in [(["--token", "bad", "list"], 3),
                                    (["--token", "demo-editor", "create", "--title", " "], 2),
                                    (["--token", "demo-editor", "complete", "missing"], 4)]:
            process = subprocess.run([sys.executable, str(entry), "--db", self.db_path, *arguments],
                cwd=self.temp_directory.name, capture_output=True, text=True, timeout=5)
            self.assertEqual(process.returncode, expected, process.stderr)
            self.assertIn("error", json.loads(process.stderr))
        boundary = Boundary_Cli(self.app.create_task, self.app.list_tasks, self.app.complete_task, self.app.resolveActor)
        output = io.StringIO()
        with patch.object(self.app.list_tasks, "listTasks", side_effect=sqlite3.OperationalError("failure")), redirect_stderr(output):
            self.assertEqual(boundary.run("list", "demo-reader"), 5)
        self.assertEqual(json.loads(output.getvalue()), {"error": "storage_unavailable"})

    def testLegacyReportsUsesDocumentedUpstreamFailure(self) -> None:
        process = subprocess.run([sys.executable, str(self.root / "apps/LegacyReports/reports.py"),
            "--upstream", self.url, "--token", "unknown", "report"], cwd=self.temp_directory.name,
            capture_output=True, text=True, timeout=8)
        self.assertEqual(process.returncode, 5)
        self.assertEqual(json.loads(process.stdout), {"error": "upstream_unavailable_or_invalid"})


if __name__ == "__main__":
    unittest.main()
