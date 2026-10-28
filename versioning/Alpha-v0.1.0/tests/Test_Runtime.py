"""Observe canonical launchers through actual CLI/HTTP boundaries and process cleanup."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import importlib.util
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

EDITION = Path(__file__).resolve().parents[1]
EXAMPLES = {"minimal": ("RequestRegister", "submit", {"request_code": "REQ001", "quantity": 2}),
            "composition": ("BookingDesk", "create", {"booking_code": "BOOK001", "title": "Annual review"}),
            "task-board": ("TaskBoard", "create", {"task_id": "TASK001", "title": "Review Atlas"})}


class Test_Runtime(unittest.TestCase):
    def testCanonicalHttpAndResourceClosure(self):
        for name, (app, operation, payload) in EXAMPLES.items():
            with self.subTest(example=name), tempfile.TemporaryDirectory() as temporary:
                process = subprocess.Popen([sys.executable, str(EDITION / "examples" / name / "launch.py"),
                    "start", "--apps", app, "--port", "0", "--duration", "1.5", "--db", str(Path(temporary) / "state.sqlite3")],
                    cwd=temporary, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                    env=dict(os.environ, VULCAN_DEMO_TOKEN="demo-editor"))
                try:
                    # Queue avoids an unbounded readline if startup fails before readiness.
                    import queue
                    ready = queue.Queue()
                    reader = threading.Thread(target=lambda: ready.put(process.stdout.readline()), daemon=True)
                    reader.start()
                    metadata = json.loads(ready.get(timeout=8))
                    base = f"http://127.0.0.1:{metadata['port']}"
                    with urlopen(base + "/health", timeout=2) as response:
                        self.assertEqual(json.load(response)["instance"], metadata["instance"])
                    request = Request(base + "/" + operation, json.dumps(payload).encode(), {"Content-Type": "application/json"})
                    with self.assertRaises(HTTPError) as failure:
                        urlopen(request, timeout=2)
                    self.assertEqual(failure.exception.code, 403)
                    self.assertEqual(json.load(failure.exception), {"error": "DENIED"})
                    failure.exception.close()
                    request.add_header("Authorization", "Bearer demo-editor")
                    with urlopen(request, timeout=2) as response:
                        self.assertIn("result", json.load(response))
                    process.wait(timeout=8)
                    self.assertEqual(process.returncode, 0, process.stderr.read())
                    with socket.socket() as probe:
                        probe.settimeout(0.3)
                        self.assertNotEqual(probe.connect_ex(("127.0.0.1", metadata["port"])), 0)
                finally:
                    if process.poll() is None:
                        process.terminate()
                        process.wait(timeout=5)
                    process.stdout.close()
                    process.stderr.close()

    def testOccupiedPortIsRejectedWithoutTouchingForeignService(self):
        with HTTPServer(("127.0.0.1", 0), BaseHTTPRequestHandler) as server, tempfile.TemporaryDirectory() as temporary:
            for name in EXAMPLES:
                with self.subTest(example=name):
                    result = subprocess.run([sys.executable, str(EDITION / "examples" / name / "launch.py"), "start",
                        "--port", str(server.server_port), "--duration", "0.1", "--db", str(Path(temporary) / (name + ".sqlite3"))],
                        capture_output=True, text=True, timeout=8)
                    self.assertEqual(result.returncode, 1)
                    self.assertNotIn('"ready"', result.stdout)
                    self.assertGreaterEqual(server.fileno(), 0)

    def testExplicitRegistryAndUnknownSelection(self):
        for name, (app, _, _) in EXAMPLES.items():
            with self.subTest(example=name):
                entry = str(EDITION / "examples" / name / "launch.py")
                result = subprocess.run([sys.executable, entry, "list"], capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(list(json.loads(result.stdout)), [app])
                result = subprocess.run([sys.executable, entry, "start", "--apps", "unknown"], capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 2)

    def testCoverageDoesNotInventUnexecutedScenarios(self):
        spec = importlib.util.spec_from_file_location("record_tests", EDITION / "scripts/record_tests.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        records = [{"status": "passed", "parameters": {"scenario_id": "SC-PASS"}},
                   {"status": "failed", "parameters": {"scenario_ids": ["SC-PASS", "SC-FAIL"]}},
                   {"status": "passed", "test": "successful-method-without-scenario"}]
        self.assertEqual(module.coverage(records, ["SC-PASS", "SC-FAIL", "SC-MISSING"]),
                         {"SC-PASS": "failed", "SC-FAIL": "failed", "SC-MISSING": "not_run"})

    def testMissingMinervaIsInconclusive(self):
        spec = importlib.util.spec_from_file_location("run_examples", EDITION / "run_examples.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temporary:
            self.assertFalse(module.validateMinerva("minimal", Path(temporary), None))
            self.assertEqual(json.loads((Path(temporary) / "minimal/minerva.json").read_text())["status"], "inconclusive")

    def testRecorderHandlesNativeValuesAndRejectsStaleBinding(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            tests = root / "tests"
            tests.mkdir()
            (tests / "Test_Demo.py").write_text("import unittest\nfrom pathlib import Path\nclass Test_Demo(unittest.TestCase):\n    def testNative(self):\n        with self.subTest(native=Path('example')):\n            self.assertTrue(True)\n", encoding="utf-8")
            blueprint = root / "docs/L2_MinervaBlueprints/blueprint.yaml"
            blueprint.parent.mkdir(parents=True)
            blueprint.write_text("changed binding", encoding="utf-8")
            expected = root / "expected.json"
            expected.write_text(json.dumps({"model_baseline": {"binding_sha256": "0" * 64}}), encoding="utf-8")
            report_path = root / "verification/report.json"
            process = subprocess.run([sys.executable, str(EDITION / "scripts/record_tests.py"), "--root", str(root),
                "--tests", str(tests), "--report", str(report_path), "--expectations", str(expected)],
                capture_output=True, text=True, timeout=10)
            self.assertEqual(process.returncode, 1, process.stderr)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertFalse(report["binding_baseline_matches"])
            self.assertEqual(report["errors"], 0)
            self.assertEqual(report["records"][0]["status"], "passed")
