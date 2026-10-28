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
from apps.BookingDesk.composition.AppComposition import AppComposition
from apps.BookingDesk.entities.Entity_ActorContext import Entity_ActorContext
from apps.BookingDesk.support.OperationFailure import OperationFailure
from apps.BookingDesk.boundaries.Boundary_Json import Boundary_Json


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
        status, body = Boundary_Json(self.app).invoke("create", {"actor_context": {"permissions": ["*"]}}, "invalid")
        self.assertEqual(status, 403)
        self.assertEqual(body, {"error": "DENIED"})

    def testRealStoreFailureIsNotApplied(self):
        with patch("apps.BookingDesk.support.SqliteResource.sqlite3.connect", side_effect=sqlite3.OperationalError("offline")):
            error = self.assertFailure("STORE_UNAVAILABLE", self.app.store.resource.initialize, "SELECT 1")
        self.assertEqual(error.write_outcome, "not_applied")

    def testCommitUncertaintyIsPreserved(self):
        connection = Mock()
        connection.commit.side_effect = sqlite3.OperationalError("lost commit confirmation")
        with patch("apps.BookingDesk.support.SqliteResource.sqlite3.connect", return_value=connection):
            error = self.assertFailure("STORE_UNAVAILABLE", self.app.store.resource.initialize, "SELECT 1")
        self.assertEqual(error.write_outcome, "unknown")
        connection.commit.assert_called_once()
        connection.close.assert_called_once()

    def testLookupAuthorization(self):
        self.assertDeniedContexts("SC-BOOKING-LOOKUP", self.app.lookup.lookupBooking, "invalid-")

    def testCreateAuthorization(self):
        self.assertDeniedContexts("SC-BOOKING-CREATE", self.app.create.createBooking, "invalid-", "")

    def testCancelAuthorization(self):
        self.assertDeniedContexts("SC-BOOKING-CANCEL", self.app.cancel.cancelBooking, "invalid-")

    def testLookupSuccess(self):
        with self.subTest(scenario_id="SC-BOOKING-LOOKUP-01", check_id="CHK-OP-BOOKING-LOAD"):
            created = self.app.create.createBooking(self.context, "BOOK001", "Annual review")
            with patch.object(self.app.store, "saveBooking", side_effect=AssertionError("lookup wrote")):
                self.assertEqual(self.app.lookup.lookupBooking(self.context, "BOOK001"), created)

    def testLookupMissing(self):
        with self.subTest(scenario_id="SC-BOOKING-LOOKUP-02"):
            self.assertFailure("NOT_FOUND", self.app.lookup.lookupBooking, self.context, "BOOK999")

    def testLookupFailure(self):
        with self.subTest(scenario_id="SC-BOOKING-LOOKUP-03"):
            with patch.object(self.app.store, "loadBooking", side_effect=OperationFailure("STORE_UNAVAILABLE")):
                self.assertFailure("STORE_UNAVAILABLE", self.app.lookup.lookupBooking, self.context, "BOOK001")

    def testLookupInvalid(self):
        with self.subTest(scenario_id="SC-BOOKING-LOOKUP-INVALID"):
            with patch.object(self.app.store, "loadBooking") as store:
                for code in ("book001", "BOOK-001", "", "A" * 13):
                    with self.assertRaises(ValueError):
                        self.app.lookup.lookupBooking(self.context, code)
                store.assert_not_called()

    def testCreateSuccess(self):
        with self.subTest(scenario_id="SC-BOOKING-CREATE-01", check_id="CHK-OP-BOOKING-SAVE"):
            with patch.object(self.app.store, "saveBooking", wraps=self.app.store.saveBooking) as store:
                result = self.app.create.createBooking(self.context, "BOOK001", "Annual review")
                self.assertEqual(store.call_args.args[1], 0)
            self.assertEqual((result.booking_code, result.title, result.status, result.version), ("BOOK001", "Annual review", "active", 1))
            self.assertEqual(self.app.lookup.lookupBooking(self.context, "BOOK001"), result)

    def testCreateInvalid(self):
        with self.subTest(scenario_id="SC-BOOKING-CREATE-02"):
            with patch.object(self.app.store, "saveBooking") as store:
                for code in ("book001", "BOOK-001"):
                    with self.assertRaises(ValueError):
                        self.app.create.createBooking(self.context, code, "Title")
                store.assert_not_called()
        with self.subTest(scenario_id="SC-BOOKING-CREATE-TITLE"):
            with patch.object(self.app.store, "saveBooking") as store:
                with self.assertRaises(ValueError):
                    self.app.create.createBooking(self.context, "BOOK001", "  ")
                store.assert_not_called()

    def testCreateConflict(self):
        with self.subTest(scenario_id="SC-BOOKING-CREATE-03"):
            first = self.app.create.createBooking(self.context, "BOOK001", "First")
            self.assertFailure("VERSION_CONFLICT", self.app.create.createBooking, self.context, "BOOK001", "Second")
            self.assertEqual(self.app.lookup.lookupBooking(self.context, "BOOK001"), first)

    def testCancelSuccess(self):
        with self.subTest(scenario_id="SC-BOOKING-CANCEL-01"):
            self.app.create.createBooking(self.context, "BOOK001", "Annual review")
            result = self.app.cancel.cancelBooking(self.context, "BOOK001")
            self.assertEqual((result.booking_code, result.title, result.status, result.version), ("BOOK001", "Annual review", "cancelled", 2))
            self.assertEqual(self.app.lookup.lookupBooking(self.context, "BOOK001"), result)

    def testCancelRefusals(self):
        self.app.create.createBooking(self.context, "BOOK001", "Annual review")
        retained = self.app.cancel.cancelBooking(self.context, "BOOK001")
        with self.subTest(scenario_id="SC-BOOKING-CANCEL-02"):
            with patch.object(self.app.store, "saveBooking") as store:
                self.assertFailure("ALREADY_CANCELLED", self.app.cancel.cancelBooking, self.context, "BOOK001")
                store.assert_not_called()
            self.assertEqual(self.app.lookup.lookupBooking(self.context, "BOOK001"), retained)
        with self.subTest(scenario_id="SC-BOOKING-CANCEL-03"):
            with patch.object(self.app.store, "saveBooking") as store:
                self.assertFailure("NOT_FOUND", self.app.cancel.cancelBooking, self.context, "BOOK999")
                self.assertFailure("ALREADY_CANCELLED", self.app.cancel.cancelBooking, self.context, "BOOK001")
                store.assert_not_called()

    def testCancelFailures(self):
        self.app.create.createBooking(self.context, "BOOK001", "Annual review")
        with self.subTest(scenario_id="SC-BOOKING-CANCEL-FAILURE"):
            with patch.object(self.app.store, "loadBooking", side_effect=OperationFailure("STORE_UNAVAILABLE")), patch.object(self.app.store, "saveBooking") as save:
                self.assertFailure("STORE_UNAVAILABLE", self.app.cancel.cancelBooking, self.context, "BOOK001")
                save.assert_not_called()
            with patch.object(self.app.store, "saveBooking", side_effect=OperationFailure("STORE_UNAVAILABLE", "not_applied")) as save:
                error = self.assertFailure("STORE_UNAVAILABLE", self.app.cancel.cancelBooking, self.context, "BOOK001")
                self.assertEqual(error.write_outcome, "not_applied")
                save.assert_called_once()
            original = self.app.store.saveBooking
            def loseConfirmation(booking, version):
                original(booking, version)
                raise OperationFailure("STORE_UNAVAILABLE", "unknown")
            with patch.object(self.app.store, "saveBooking", side_effect=loseConfirmation) as save:
                error = self.assertFailure("STORE_UNAVAILABLE", self.app.cancel.cancelBooking, self.context, "BOOK001")
                self.assertEqual(error.write_outcome, "unknown")
                save.assert_called_once()
            self.assertEqual(self.app.lookup.lookupBooking(self.context, "BOOK001").version, 2)

    def testCancelPreservesContext(self):
        with self.subTest(scenario_id="SC-BOOKING-CANCEL-CONTEXT"):
            context = replace(self.context, permissions=("booking.cancel",))
            with patch.object(self.app.lookup, "lookupBooking", wraps=self.app.lookup.lookupBooking) as lookup, patch.object(self.app.store, "saveBooking") as save:
                self.assertFailure("DENIED", self.app.cancel.cancelBooking, context, "BOOK001")
                self.assertIs(lookup.call_args.args[0], context)
                save.assert_not_called()

    def testSharedCreationQuality(self):
        # Atlas cancellation explicitly references the creation RNF; preserve that source wording.
        with self.subTest(scenario_ids=["SC-BOOKING-CREATE-QUALITY", "SC-BOOKING-CANCEL-QUALITY"], check_id="CHK-RNF-BOOKING-CREATE-RESPONSE"):
            self.measureCli("create", [({"booking_code": f"BOOK{i}", "title": "Annual review" if i % 2 == 0 else " "}, i % 2 == 0) for i in range(30)])

    def testConcurrentSaveIsConditional(self):
        booking = self.app.create.createBooking(self.context, "BOOK001", "Original")
        barrier = threading.Barrier(2)
        def save(title):
            barrier.wait(timeout=5)
            try:
                return self.app.store.saveBooking(replace(booking, title=title), 1)
            except OperationFailure as error:
                return error.code
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(save, ["First", "Second"]))
        self.assertEqual(results.count("VERSION_CONFLICT"), 1)
        winner = next(item for item in results if item != "VERSION_CONFLICT")
        self.assertEqual(winner.version, 2)
        self.assertEqual(self.app.lookup.lookupBooking(self.context, "BOOK001"), winner)
