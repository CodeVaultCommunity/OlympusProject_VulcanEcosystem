"""Executable ADVS observations: scenario IDs refer to the pinned designed blueprint."""
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
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
from apps.TaskBoard.composition.AppComposition import AppComposition
from apps.TaskBoard.entities.Entity_ActorContext import Entity_ActorContext
from apps.TaskBoard.support.OperationFailure import OperationFailure
from apps.TaskBoard.boundaries.Boundary_Json import Boundary_Json
from apps.TaskBoard.entities.Entity_Task import Entity_Task

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
        with patch("apps.TaskBoard.support.SqliteResource.sqlite3.connect", side_effect=sqlite3.OperationalError("offline")):
            error = self.assertFailure("STORE_UNAVAILABLE", self.app.store.resource.initialize, "SELECT 1")
        self.assertEqual(error.write_outcome, "not_applied")

    def testCommitUncertaintyIsPreserved(self):
        connection = Mock()
        connection.commit.side_effect = sqlite3.OperationalError("lost commit confirmation")
        with patch("apps.TaskBoard.support.SqliteResource.sqlite3.connect", return_value=connection):
            error = self.assertFailure("STORE_UNAVAILABLE", self.app.store.resource.initialize, "SELECT 1")
        self.assertEqual(error.write_outcome, "unknown")
        connection.commit.assert_called_once()
        connection.close.assert_called_once()

    def testCreateAuthorization(self):
        self.assertDeniedContexts("SC-TASK-CREATE", self.app.create.createTask, "", "")

    def testCompleteAuthorization(self):
        self.assertDeniedContexts("SC-TASK-COMPLETE", self.app.complete.completeTask, "")

    def testListAuthorization(self):
        self.assertDeniedContexts("SC-TASK-LIST", self.app.list.listTasks)
        self.assertFailure("DENIED", self.app.list.listTasks, replace(self.context, board_id="board-B"))

    def testCreateSurvivesRestart(self):
        with self.subTest(scenario_id="SC-TASK-CREATE-SUCCESS", check_id="CHK-RNF-TASK-CREATE-RETENTION"):
            task = self.app.create.createTask(self.context, "TASK001", "Review Atlas")
            self.assertEqual((task.task_id, task.title, task.status, task.revision), ("TASK001", "Review Atlas", "open", 0))
            restarted = AppComposition(self.db)
            self.assertEqual(restarted.list.listTasks(self.context), [task])

    def testCreateInvalid(self):
        with self.subTest(scenario_id="SC-TASK-CREATE-INVALID"):
            with patch.object(self.app.store, "createTask") as store:
                for identity, title in [("TASK001", ""), ("  ", "Title")]:
                    with self.assertRaises(ValueError):
                        self.app.create.createTask(self.context, identity, title)
                store.assert_not_called()

    def testCreateDuplicate(self):
        with self.subTest(scenario_id="SC-TASK-CREATE-DUPLICATE", check_id="CHK-OP-TASK-CREATE"):
            first = self.app.create.createTask(self.context, "TASK001", "First")
            self.assertFailure("DUPLICATE_ID", self.app.create.createTask, self.context, "TASK001", "Second")
            self.assertEqual(self.app.store.loadTask("TASK001"), first)

    def testCreateUnknown(self):
        with self.subTest(scenario_id="SC-TASK-CREATE-UNKNOWN"):
            original = self.app.store.createTask
            def loseConfirmation(task):
                original(task)
                raise OperationFailure("STORE_UNAVAILABLE", "unknown")
            with patch.object(self.app.store, "createTask", side_effect=loseConfirmation) as store:
                error = self.assertFailure("STORE_UNAVAILABLE", self.app.create.createTask, self.context, "TASK001", "Review Atlas")
                self.assertEqual(error.write_outcome, "unknown")
                store.assert_called_once()
            self.assertEqual(len(self.app.store.listTasks()), 1)

    def testCompleteSuccess(self):
        with self.subTest(scenario_id="SC-TASK-COMPLETE-SUCCESS", check_id="CHK-OP-TASK-COMPLETE"):
            self.app.create.createTask(self.context, "TASK001", "Review Atlas")
            task = self.app.complete.completeTask(self.context, "TASK001")
            self.assertEqual((task.task_id, task.title, task.status, task.revision), ("TASK001", "Review Atlas", "completed", 1))
            self.assertEqual(self.app.list.listTasks(self.context), [task])

    def testCompleteMissing(self):
        with self.subTest(scenario_id="SC-TASK-COMPLETE-MISSING", check_id="CHK-OP-TASK-LOAD"):
            with patch.object(self.app.store, "completeTask") as store:
                self.assertFailure("NOT_FOUND", self.app.complete.completeTask, self.context, "MISSING")
                store.assert_not_called()

    def testCompleteInvalid(self):
        with self.subTest(scenario_id="SC-TASK-COMPLETE-INVALID"):
            with patch.object(self.app.store, "loadTask") as load, patch.object(self.app.store, "completeTask") as complete:
                for identity in ("", "  "):
                    with self.assertRaises(ValueError):
                        self.app.complete.completeTask(self.context, identity)
                load.assert_not_called()
                complete.assert_not_called()

    def testCompleteAlready(self):
        with self.subTest(scenario_id="SC-TASK-COMPLETE-ALREADY"):
            self.app.create.createTask(self.context, "TASK001", "Review Atlas")
            retained = self.app.complete.completeTask(self.context, "TASK001")
            with patch.object(self.app.store, "completeTask") as store:
                self.assertFailure("ALREADY_COMPLETED", self.app.complete.completeTask, self.context, "TASK001")
                store.assert_not_called()
            self.assertEqual(self.app.store.loadTask("TASK001"), retained)

    def testCompleteConflict(self):
        with self.subTest(scenario_id="SC-TASK-COMPLETE-CONFLICT"):
            self.app.create.createTask(self.context, "TASK001", "Review Atlas")
            original = self.app.store.completeTask
            def compete(task, revision):
                with closing(sqlite3.connect(self.db)) as connection, connection:
                    connection.execute("UPDATE tasks SET title='Competing state', revision=1 WHERE task_id='TASK001'")
                return original(task, revision)
            with patch.object(self.app.store, "completeTask", side_effect=compete):
                self.assertFailure("VERSION_CONFLICT", self.app.complete.completeTask, self.context, "TASK001")
            retained = self.app.store.loadTask("TASK001")
            self.assertEqual((retained.title, retained.status, retained.revision), ("Competing state", "open", 1))

    def testCompleteUnknown(self):
        with self.subTest(scenario_id="SC-TASK-COMPLETE-UNKNOWN"):
            self.app.create.createTask(self.context, "TASK001", "Review Atlas")
            original = self.app.store.completeTask
            def loseConfirmation(task, revision):
                original(task, revision)
                raise OperationFailure("STORE_UNAVAILABLE", "unknown")
            with patch.object(self.app.store, "completeTask", side_effect=loseConfirmation) as store:
                error = self.assertFailure("STORE_UNAVAILABLE", self.app.complete.completeTask, self.context, "TASK001")
                self.assertEqual(error.write_outcome, "unknown")
                store.assert_called_once()
            self.assertEqual(self.app.store.loadTask("TASK001").revision, 1)

    def testListContentsAndIsolation(self):
        with self.subTest(scenario_id="SC-TASK-LIST-CONTENT", check_id="CHK-OP-TASK-LIST"):
            second = self.app.create.createTask(self.context, "TASK002", "  Keep exact title  ")
            self.app.create.createTask(self.context, "TASK001", "Review Atlas")
            first = self.app.complete.completeTask(self.context, "TASK001")
            other = AppComposition(self.db, board_id="board-B")
            other.create.createTask(other.resolveActor("demo-editor"), "SECRET", "Other board")
            before = Path(self.db).read_bytes()
            self.assertEqual(self.app.list.listTasks(self.context), [first, second])
            self.assertEqual(Path(self.db).read_bytes(), before)

    def testListEmptyVersusUnavailable(self):
        with self.subTest(scenario_id="SC-TASK-LIST-EMPTY"):
            before = Path(self.db).read_bytes()
            self.assertEqual(self.app.list.listTasks(self.context), [])
            self.assertEqual(Path(self.db).read_bytes(), before)
            with patch.object(self.app.store, "listTasks", side_effect=OperationFailure("STORE_UNAVAILABLE")):
                self.assertFailure("STORE_UNAVAILABLE", self.app.list.listTasks, self.context)

    def testListInvalidHydration(self):
        with self.subTest(scenario_id="SC-TASK-LIST-INTEGRITY"):
            self.app.create.createTask(self.context, "TASK001", "Valid")
            with closing(sqlite3.connect(self.db)) as connection, connection:
                connection.execute("INSERT INTO tasks VALUES ('board-A','TASK002','','open',0)")
            before = Path(self.db).read_bytes()
            self.assertFailure("STORE_INVALID_STATE", self.app.list.listTasks, self.context)
            self.assertEqual(Path(self.db).read_bytes(), before)

    def testRealConcurrentCompletion(self):
        with self.subTest(check_id="CHK-RNF-TASK-COMPLETE-ATOMICITY"):
            task = self.app.create.createTask(self.context, "TASK001", "Review Atlas")
            barrier = threading.Barrier(2)
            def complete(index):
                barrier.wait(timeout=5)
                try:
                    return self.app.store.completeTask(task.complete(), 0)
                except OperationFailure as error:
                    return error.code
            with ThreadPoolExecutor(max_workers=2) as pool:
                results = list(pool.map(complete, range(2)))
            self.assertEqual(results.count("VERSION_CONFLICT"), 1)
            self.assertEqual(self.app.store.loadTask("TASK001").revision, 1)

    def testConsistentReadDuringWrite(self):
        with self.subTest(check_id="CHK-RNF-TASK-LIST-CONSISTENCY"):
            self.app.create.createTask(self.context, "TASK001", "Before")
            self.app.create.createTask(self.context, "TASK002", "Before")
            with closing(sqlite3.connect(self.db)) as connection, connection:
                connection.execute("PRAGMA journal_mode=WAL")
            original = Entity_Task
            hydrated = []
            def hydrate(*row):
                hydrated.append(row[0])
                if len(hydrated) == 1:
                    with closing(sqlite3.connect(self.db)) as connection, connection:
                        connection.execute("UPDATE tasks SET title='After', revision=1")
                return original(*row)
            with patch("apps.TaskBoard.tools.Tool_SqliteTaskStore.Entity_Task", side_effect=hydrate):
                snapshot = self.app.list.listTasks(self.context)
            self.assertEqual([task.title for task in snapshot], ["Before", "Before"])
            self.assertEqual([task.revision for task in snapshot], [0, 0])
            self.assertEqual([task.title for task in self.app.list.listTasks(self.context)], ["After", "After"])
