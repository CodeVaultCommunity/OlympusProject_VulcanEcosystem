"""Concrete SQLite capability. No architectural base class or interface is needed."""

from contextlib import closing
import sqlite3
import uuid
from pathlib import Path

from apps.TaskBoard.entities.Entity_Task import Entity_Task


class Tool_SqliteTaskStore:
    def __init__(self, db_path: str) -> None:
        self.db_path = str(Path(db_path).resolve())
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.db_path, timeout=5)) as connection, connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS tasks "
                "(task_id TEXT PRIMARY KEY, title TEXT NOT NULL, completed INTEGER NOT NULL CHECK(completed IN (0, 1)))"
            )

    def createTask(self, title: str) -> Entity_Task:
        task = Entity_Task(uuid.uuid4().hex, title)
        with closing(sqlite3.connect(self.db_path, timeout=5)) as connection, connection:
            connection.execute(
                "INSERT INTO tasks(task_id, title, completed) VALUES (?, ?, ?)",
                (task.getId(), task.getTitle(), int(task.isCompleted())),
            )
        return task

    def listTasks(self) -> list[Entity_Task]:
        with closing(sqlite3.connect(self.db_path, timeout=5)) as connection, connection:
            rows = connection.execute(
                "SELECT task_id, title, completed FROM tasks ORDER BY rowid"
            ).fetchall()
        return [Entity_Task(task_id, title, bool(completed)) for task_id, title, completed in rows]

    def getTask(self, task_id: str) -> Entity_Task | None:
        with closing(sqlite3.connect(self.db_path, timeout=5)) as connection, connection:
            row = connection.execute(
                "SELECT task_id, title, completed FROM tasks WHERE task_id = ?", (task_id,)
            ).fetchone()
        return Entity_Task(row[0], row[1], bool(row[2])) if row else None

    def saveTask(self, task: Entity_Task) -> Entity_Task:
        with closing(sqlite3.connect(self.db_path, timeout=5)) as connection, connection:
            result = connection.execute(
                "UPDATE tasks SET title = ?, completed = ? WHERE task_id = ?",
                (task.getTitle(), int(task.isCompleted()), task.getId()),
            )
            if result.rowcount != 1:
                raise LookupError("task_not_found")
        return task
