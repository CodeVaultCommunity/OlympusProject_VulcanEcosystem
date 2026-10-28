"""Executable ADVS observations: scenario IDs refer to the pinned designed blueprint."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import Mock, patch
from apps.RequestRegister.composition.AppComposition import AppComposition
from apps.RequestRegister.entities.Entity_ActorContext import Entity_ActorContext
from apps.RequestRegister.support.OperationFailure import OperationFailure
from apps.RequestRegister.boundaries.Boundary_Json import Boundary_Json
from apps.RequestRegister.entities.Entity_Request import Entity_Request

class Test_Contracts(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.db = str(Path(self.temporary.name) / "test.sqlite3")
        self.app = AppComposition(self.db)
        self.context = self.app.resolveActor("demo-editor")

    def assertFailure(self, code, function, *args):
        with self.assertRaises(OperationFailure) as caught:
            function(*args)
        self.assertEqual(caught.exception.code, code)
        return caught.exception

    def assertDeniedContexts(self, prefix, function, *args):
        contexts = {"ABSENT": None, "UNRESOLVED": replace(self.context, resolved=False),
                    "UNKNOWN": replace(self.context, known=False), "INSUFFICIENT": replace(self.context, permissions=()),
                    "EXPIRED": replace(self.context, valid=False), "ANONYMOUS": replace(self.context, authenticated=False)}
        for label, context in contexts.items():
            with self.subTest(scenario_id=prefix + "-AUTH-" + label):
                with patch.object(self.app.store.resource, "open", side_effect=AssertionError("store invoked before denial")):
                    self.assertFailure("DENIED", function, context, *args)

    def measureCli(self, operation, payloads):
        root = Path(__file__).resolve().parents[3]
        env = dict(os.environ, VULCAN_CALLER_TOKEN="demo-editor", VULCAN_DEMO_TOKEN="demo-editor")
        elapsed = []
        for payload, success in payloads:
            started = time.monotonic()
            result = subprocess.run([sys.executable, str(root / "launch.py"), "start", "--mode", "cli",
                "--operation", operation, "--payload", json.dumps(payload), "--db", self.db],
                capture_output=True, text=True, env=env, timeout=5)
            elapsed.append(time.monotonic() - started)
            self.assertEqual(result.returncode, 0 if success else 1, result.stderr)
            self.assertIn("result" if success else "error", json.loads(result.stdout))
        self.assertEqual(len(elapsed), 30)
        self.assertLessEqual(max(elapsed), 2.0, elapsed)
        self.observations = {"boundary": "CLI subprocess start through captured complete JSON stdout", "samples": len(elapsed), "elapsed_seconds": elapsed, "production_sla": False}

    def testChannelCannotForgeTrustedContext(self):
        status, body = Boundary_Json(self.app).invoke("submit", {"actor_context": {"permissions": ["*"]}}, "invalid")
        self.assertEqual(status, 403)
        self.assertEqual(body, {"error": "DENIED"})

    def testRealStoreFailureIsNotApplied(self):
        with patch("apps.RequestRegister.support.SqliteResource.sqlite3.connect", side_effect=sqlite3.OperationalError("offline")):
            error = self.assertFailure("STORE_UNAVAILABLE", self.app.store.resource.initialize, "SELECT 1")
        self.assertEqual(error.write_outcome, "not_applied")

    def testCommitUncertaintyIsPreserved(self):
        connection = Mock()
        connection.commit.side_effect = sqlite3.OperationalError("lost commit confirmation")
        with patch("apps.RequestRegister.support.SqliteResource.sqlite3.connect", return_value=connection):
            error = self.assertFailure("STORE_UNAVAILABLE", self.app.store.resource.initialize, "SELECT 1")
        self.assertEqual(error.write_outcome, "unknown")
        connection.commit.assert_called_once()
        connection.close.assert_called_once()

    def testSubmitAuthorization(self):
        self.assertDeniedContexts("SC-REQUEST-SUBMIT", self.app.submit.submitRequest, "", 0)

    def testSubmitSuccess(self):
        with self.subTest(scenario_id="SC-REQUEST-01", check_id="CHK-OP-REQUEST-STORE"):
            result = self.app.submit.submitRequest(self.context, "REQ001", 2)
            self.assertEqual((result.request_code, result.quantity), ("REQ001", 2))
            self.assertEqual(self.app.store.readRequest("REQ001"), result)
            self.assertEqual(self.app.submit.submitRequest(self.context, "req001", 10**30).quantity, 10**30)

    def testSubmitQuantityRefusal(self):
        with self.subTest(scenario_id="SC-REQUEST-02"):
            with patch.object(self.app.store, "storeRequest") as store:
                for quantity in (0, -1, True, 1.5):
                    with self.assertRaises(ValueError):
                        self.app.submit.submitRequest(self.context, "REQ001", quantity)
                store.assert_not_called()

    def testSubmitDuplicate(self):
        with self.subTest(scenario_id="SC-REQUEST-04"):
            first = self.app.submit.submitRequest(self.context, "REQ001", 2)
            self.assertFailure("DUPLICATE_CODE", self.app.submit.submitRequest, self.context, "REQ001", 3)
            self.assertEqual(self.app.store.readRequest("REQ001"), first)

    def testSubmitUnknown(self):
        with self.subTest(scenario_id="SC-REQUEST-05"):
            original = self.app.store.storeRequest
            def loseConfirmation(code, quantity):
                original(code, quantity)
                raise OperationFailure("STORE_UNAVAILABLE", "unknown")
            with patch.object(self.app.store, "storeRequest", side_effect=loseConfirmation) as store:
                error = self.assertFailure("STORE_UNAVAILABLE", self.app.submit.submitRequest, self.context, "REQ001", 2)
                self.assertEqual(error.write_outcome, "unknown")
                store.assert_called_once()
            self.assertIsNotNone(self.app.store.readRequest("REQ001"))

    def testSubmitCodeBeforeQuantity(self):
        with self.subTest(scenario_id="SC-REQUEST-06"):
            with patch.object(Entity_Request, "validateQuantity", side_effect=AssertionError("quantity reached")), patch.object(self.app.store, "storeRequest") as store:
                with self.assertRaises(ValueError):
                    self.app.submit.submitRequest(self.context, "", 0)
                store.assert_not_called()

    def testSubmitQuality(self):
        with self.subTest(scenario_id="SC-REQUEST-SUBMIT-QUALITY", check_id="CHK-RNF-REQUEST-01"):
            self.measureCli("submit", [({"request_code": f"REQ{i}", "quantity": 1 if i % 2 == 0 else 0}, i % 2 == 0) for i in range(30)])
