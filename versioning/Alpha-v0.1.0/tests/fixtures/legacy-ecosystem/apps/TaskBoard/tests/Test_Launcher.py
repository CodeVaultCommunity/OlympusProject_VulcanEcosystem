"""Supporting lifecycle checks: selective startup, readiness and owned-process cleanup."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

import launch


class Test_Launcher(unittest.TestCase):
    def availablePort(self) -> int:
        with socket.socket() as reservation:
            reservation.bind(("127.0.0.1", 0))
            return reservation.getsockname()[1]

    def testAllAndSelectedApps(self) -> None:
        root = Path(__file__).resolve().parents[3]
        for selection, expected in [(["--all"], ["TaskBoard", "LegacyReports"]),
                                     (["--apps", "TaskBoard"], ["TaskBoard"]),
                                     (["--apps", "LegacyReports"], ["TaskBoard", "LegacyReports"])]:
            with self.subTest(selection=selection), tempfile.TemporaryDirectory() as temporary:
                task_port = self.availablePort()
                report_port = self.availablePort()
                while report_port == task_port:
                    report_port = self.availablePort()
                process = subprocess.run([sys.executable, str(root / "launch.py"), "start", *selection,
                    "--task-port", str(task_port), "--report-port", str(report_port),
                    "--db", str(Path(temporary) / "tasks.sqlite3"), "--duration", "0.2"],
                    cwd=root, capture_output=True, text=True, timeout=15)
                self.assertEqual(process.returncode, 0, process.stderr)
                for app_id in expected:
                    self.assertIn("Ready: " + app_id, process.stdout)
                if expected == ["TaskBoard"]:
                    self.assertNotIn("Ready: LegacyReports", process.stdout)
                for port in (task_port, report_port):
                    with self.assertRaises(URLError):
                        urlopen(f"http://127.0.0.1:{port}/health", timeout=0.3)

    def testOccupiedPortDoesNotStopForeignService(self) -> None:
        root = Path(__file__).resolve().parents[3]
        server = ThreadingHTTPServer(("127.0.0.1", 0), BaseHTTPRequestHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as temporary:
                process = subprocess.run([sys.executable, str(root / "launch.py"), "start", "--apps", "TaskBoard",
                    "--task-port", str(server.server_port), "--db", str(Path(temporary) / "tasks.sqlite3"),
                    "--duration", "0.1"], cwd=root, capture_output=True, text=True, timeout=15)
            self.assertEqual(process.returncode, 1)
            self.assertRegex(process.stderr, r"exited before readiness|did not become ready")
            # This server belongs to the test, not the launcher: it still responds.
            with self.assertRaises(HTTPError) as response:
                urlopen(f"http://127.0.0.1:{server.server_port}/health", timeout=1)
            self.assertEqual(response.exception.code, 501)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)

    def testDependencyCyclesAndSelectionDiagnostics(self) -> None:
        self.assertEqual(launch.planApps({"LegacyReports"}), ["TaskBoard", "LegacyReports"])
        with self.assertRaisesRegex(ValueError, "startup_dependency_cycle"):
            launch.planApps({"A"}, {"A": ["B"], "B": ["A"]})
        with self.assertRaisesRegex(ValueError, "unknown_app"):
            launch.planApps({"missing"})
        root = Path(__file__).resolve().parents[3]
        for arguments in [["--apps", "missing"], ["--all", "--duration", "nan"],
                          ["--all", "--task-port", "0"], ["--all", "--task-port", "9000", "--report-port", "9000"]]:
            process = subprocess.run([sys.executable, str(root / "launch.py"), "start", *arguments],
                capture_output=True, text=True, timeout=5)
            self.assertEqual(process.returncode, 2)

    def testReadinessRejectsForeignInstance(self) -> None:
        child = Mock()
        child.poll.return_value = None
        response = json.dumps({"app": "TaskBoard", "ready": True, "instance_id": "foreign"}).encode()
        with patch.object(launch, "urlopen", side_effect=lambda *args, **kwargs: io.BytesIO(response)):
            with self.assertRaisesRegex(RuntimeError, "did not become ready"):
                launch.waitReady(child, "http://example.invalid/health", "TaskBoard", "owned", timeout=0.08)

    def testPartialStartupCleansEarlierChild(self) -> None:
        root = Path(__file__).resolve().parents[3]
        foreign = ThreadingHTTPServer(("127.0.0.1", 0), BaseHTTPRequestHandler)
        thread = threading.Thread(target=foreign.serve_forever, daemon=True)
        thread.start()
        task_port = self.availablePort()
        try:
            with tempfile.TemporaryDirectory() as temporary:
                process = subprocess.run([sys.executable, str(root / "launch.py"), "start", "--all",
                    "--task-port", str(task_port), "--report-port", str(foreign.server_port),
                    "--db", str(Path(temporary) / "tasks.sqlite3"), "--duration", "0.1"],
                    cwd=temporary, capture_output=True, text=True, timeout=15)
            self.assertEqual(process.returncode, 1)
            self.assertIn("Ready: TaskBoard", process.stdout)
            with self.assertRaises(URLError):
                urlopen(f"http://127.0.0.1:{task_port}/health", timeout=0.3)
            with self.assertRaises(HTTPError) as error:
                urlopen(f"http://127.0.0.1:{foreign.server_port}/health", timeout=1)
            self.assertEqual(error.exception.code, 501)
        finally:
            foreign.shutdown()
            foreign.server_close()
            thread.join(timeout=2)

    @unittest.skipUnless(os.name == "posix", "SIGTERM lifecycle assertion requires POSIX")
    def testSignalStopsOwnedChildren(self) -> None:
        root = Path(__file__).resolve().parents[3]
        task_port = self.availablePort()
        with tempfile.TemporaryDirectory() as temporary:
            process = subprocess.Popen([sys.executable, str(root / "launch.py"), "start", "--apps", "TaskBoard",
                "--task-port", str(task_port), "--db", str(Path(temporary) / "tasks.sqlite3")],
                cwd=temporary, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                deadline = time.monotonic() + 10
                ready = False
                while time.monotonic() < deadline:
                    if process.poll() is not None:
                        break
                    try:
                        with urlopen(f"http://127.0.0.1:{task_port}/health", timeout=0.3) as response:
                            ready = json.load(response).get("ready") is True
                        if ready:
                            break
                    except URLError:
                        time.sleep(0.05)
                self.assertTrue(ready)
                process.send_signal(signal.SIGTERM)
                output, errors = process.communicate(timeout=8)
                self.assertEqual(process.returncode, 0, errors)
                with self.assertRaises(URLError):
                    urlopen(f"http://127.0.0.1:{task_port}/health", timeout=0.3)
            finally:
                if process.poll() is None:
                    process.terminate()
                    process.communicate(timeout=8)

    def testCleanupEscalatesOnlyOwnedProcess(self) -> None:
        child = Mock()
        child.poll.return_value = None
        child.wait.side_effect = [subprocess.TimeoutExpired("example-child", 3), 0]
        launch.stopOwned([child])
        child.terminate.assert_called_once()
        child.kill.assert_called_once()
        self.assertEqual(child.wait.call_count, 2)


if __name__ == "__main__":
    unittest.main()
