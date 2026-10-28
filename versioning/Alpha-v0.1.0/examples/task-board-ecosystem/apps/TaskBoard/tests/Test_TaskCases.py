"""Three directly linked behavioral tests, with their positive and negative scenarios."""

from pathlib import Path
from dataclasses import FrozenInstanceError
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
import uuid

from apps.TaskBoard.composition.AppComposition import AppComposition
from apps.TaskBoard.entities.Entity_ActorContext import Entity_ActorContext
from apps.TaskBoard.entities.Entity_Task import Entity_Task
from apps.TaskBoard.value_objects.ValueObject_TaskTitle import ValueObject_TaskTitle


class Test_TaskCases(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.temp_directory.name) / "tasks.sqlite3")
        self.app = AppComposition(self.db_path)
        self.editor = self.app.resolveActor("demo-editor")
        self.reader = self.app.resolveActor("demo-reader")
        self.denied_contexts = [
            None,
            Entity_ActorContext("unresolved", ("tasks:create", "tasks:read", "tasks:complete"), "unresolved"),
            Entity_ActorContext("unknown", ("tasks:create", "tasks:read", "tasks:complete"), known_actor=False),
            Entity_ActorContext("limited", ()),
        ]

    def tearDown(self) -> None:
        self.temp_directory.cleanup()

    def testCreateTask(self) -> None:
        """UC-TASK-001: denied callers and invalid titles have no task-write effects."""
        for context in self.denied_contexts + [self.reader]:
            with self.subTest(context=context), self.assertRaises(PermissionError):
                self.app.create_task.createTask(context, "Denied task")
        self.assertEqual(self.app.list_tasks.listTasks(self.editor), [])
        for title in ["", "   ", "x" * 121, None]:
            with self.subTest(title=title), self.assertRaises(ValueError):
                self.app.create_task.createTask(self.editor, title)
        self.assertEqual(self.app.list_tasks.listTasks(self.editor), [])
        task = self.app.create_task.createTask(self.editor, "  Document a boundary  ")
        self.assertEqual(uuid.UUID(hex=task.getId()).version, 4)
        self.assertEqual(task.getTitle(), "Document a boundary")
        self.assertFalse(task.isCompleted())
        reloaded = AppComposition(self.db_path).list_tasks.listTasks(self.reader)
        self.assertEqual([item.getId() for item in reloaded], [task.getId()])

    def testListTasks(self) -> None:
        """UC-TASK-002: the direct core and a read-only actor enforce the same policy."""
        self.assertEqual(self.app.list_tasks.listTasks(self.reader), [])
        # Reverse lexical UUID order makes insertion ordering distinguishable from ID sorting.
        identities = [uuid.UUID("ffffffff-ffff-4fff-bfff-ffffffffffff"),
                      uuid.UUID("00000000-0000-4000-8000-000000000001")]
        with patch("apps.TaskBoard.tools.Tool_SqliteTaskStore.uuid.uuid4", side_effect=identities):
            task = self.app.create_task.createTask(self.editor, "Review the model")
            second_task = self.app.create_task.createTask(self.editor, "Review the implementation")
        for context in self.denied_contexts:
            with self.subTest(context=context), self.assertRaises(PermissionError):
                self.app.list_tasks.listTasks(context)
        tasks = self.app.list_tasks.listTasks(self.reader)
        self.assertEqual([item.getId() for item in tasks], [task.getId(), second_task.getId()])
        self.assertEqual([item.getTitle() for item in tasks], ["Review the model", "Review the implementation"])
        self.assertTrue(all(not item.isCompleted() for item in tasks))

    def testCompleteTask(self) -> None:
        """UC-TASK-003: refusal precedes mutation; completion is durable and idempotent."""
        task = self.app.create_task.createTask(self.editor, "Run the example")
        for context in self.denied_contexts + [self.reader]:
            with self.subTest(context=context), self.assertRaises(PermissionError):
                self.app.complete_task.completeTask(context, task.getId())
        self.assertFalse(self.app.task_store.getTask(task.getId()).isCompleted())
        with self.assertRaises(LookupError):
            self.app.complete_task.completeTask(self.editor, "missing")
        with self.assertRaises(ValueError):
            self.app.complete_task.completeTask(self.editor, "")
        first = self.app.complete_task.completeTask(self.editor, task.getId())
        second = self.app.complete_task.completeTask(self.editor, task.getId())
        self.assertTrue(first.isCompleted())
        self.assertEqual(first.getId(), second.getId())
        self.assertEqual(len(self.app.list_tasks.listTasks(self.editor)), 1)
        self.assertTrue(AppComposition(self.db_path).list_tasks.listTasks(self.reader)[0].isCompleted())

    def testAuthorizationPrecedesDependencyAccess(self) -> None:
        """Supporting proof: denied direct invocations never call an injected tool."""
        with patch.object(self.app.create_task, "task_store") as store:
            with self.assertRaises(PermissionError):
                self.app.create_task.createTask(None, "Denied")
            store.assert_not_called()
            self.assertEqual(store.mock_calls, [])
        with patch.object(self.app.list_tasks, "task_store") as store:
            with self.assertRaises(PermissionError):
                self.app.list_tasks.listTasks(None)
            self.assertEqual(store.mock_calls, [])
        with patch.object(self.app.complete_task, "task_store") as store:
            with self.assertRaises(PermissionError):
                self.app.complete_task.completeTask(self.reader, "unknown")
            self.assertEqual(store.mock_calls, [])

    def testCanonicalValuesAndContext(self) -> None:
        value = ValueObject_TaskTitle("  title  ")
        self.assertEqual(value, ValueObject_TaskTitle("title"))
        with self.assertRaises(FrozenInstanceError):
            value.value = ""
        for invalid in ["", "   ", None, "x" * 121]:
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                Entity_Task("id", invalid)
        with self.assertRaises(ValueError):
            Entity_Task("id", "title", completed=1)
        with self.assertRaises(ValueError):
            Entity_ActorContext("actor", ["tasks:create"])
        self.assertFalse(Entity_ActorContext(" ", ("tasks:create",)).canPerform("tasks:create"))

    def testStorageFailureAndCanonicalConstruction(self) -> None:
        """PERSISTENCE includes durable success and explicit connection failure."""
        module = "apps.TaskBoard.tools.Tool_SqliteTaskStore.sqlite3.connect"
        with patch(module, side_effect=sqlite3.OperationalError("unavailable")):
            with self.assertRaises(sqlite3.OperationalError):
                self.app.create_task.createTask(self.editor, "Valid title")
            with self.assertRaises(sqlite3.OperationalError):
                self.app.list_tasks.listTasks(self.reader)
            with self.assertRaises(ValueError):
                self.app.create_task.createTask(self.editor, " ")
        self.assertEqual(self.app.list_tasks.listTasks(self.reader), [])
        task = self.app.create_task.createTask(self.editor, "Valid title")
        with patch(module, side_effect=sqlite3.OperationalError("unavailable")):
            with self.assertRaises(sqlite3.OperationalError):
                self.app.complete_task.completeTask(self.editor, task.getId())
        self.assertFalse(self.app.task_store.getTask(task.getId()).isCompleted())


if __name__ == "__main__":
    unittest.main()
