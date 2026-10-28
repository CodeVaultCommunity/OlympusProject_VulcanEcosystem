"""Board-scoped atomic persistence; data validity belongs to the canonical entity."""
from apps.TaskBoard.entities.Entity_Task import Entity_Task
from apps.TaskBoard.support.OperationFailure import OperationFailure
from apps.TaskBoard.support.SqliteResource import SqliteResource

class Tool_SqliteTaskStore:
    def __init__(self, db_path: str, board_id: str) -> None:
        self.board_id = board_id
        self.resource = SqliteResource(db_path)
        self.resource.initialize("CREATE TABLE IF NOT EXISTS tasks (board TEXT NOT NULL, task_id TEXT NOT NULL COLLATE BINARY, title TEXT NOT NULL, status TEXT NOT NULL, revision INTEGER NOT NULL, PRIMARY KEY(board, task_id))")

    def createTask(self, task: Entity_Task) -> Entity_Task:
        with self.resource.open(write=True) as connection:
            result = connection.execute("INSERT INTO tasks VALUES (?, ?, ?, ?, ?) ON CONFLICT(board, task_id) DO NOTHING", (self.board_id, task.task_id, task.title, task.status, task.revision))
            if result.rowcount != 1:
                raise OperationFailure("DUPLICATE_ID")
        return task

    def loadTask(self, task_id: str) -> Entity_Task:
        with self.resource.open() as connection:
            row = connection.execute("SELECT task_id, title, status, revision FROM tasks WHERE board = ? AND task_id = ?", (self.board_id, task_id)).fetchone()
        if row is None:
            raise OperationFailure("NOT_FOUND")
        try:
            return Entity_Task(*row)
        except ValueError as error:
            raise OperationFailure("STORE_INVALID_STATE") from error

    def completeTask(self, task: Entity_Task, expected_revision: int) -> Entity_Task:
        with self.resource.open(write=True) as connection:
            row = connection.execute("SELECT revision FROM tasks WHERE board = ? AND task_id = ?", (self.board_id, task.task_id)).fetchone()
            if row is None:
                raise OperationFailure("NOT_FOUND")
            if row[0] != expected_revision:
                raise OperationFailure("VERSION_CONFLICT")
            # BEGIN IMMEDIATE owns the write lock across this comparison and update.
            connection.execute("UPDATE tasks SET status = ?, revision = ? WHERE board = ? AND task_id = ? AND revision = ?", (task.status, expected_revision + 1, self.board_id, task.task_id, expected_revision))
        return task

    def listTasks(self) -> list[Entity_Task]:
        with self.resource.open() as connection:
            rows = connection.execute("SELECT task_id, title, status, revision FROM tasks WHERE board = ? ORDER BY task_id COLLATE BINARY", (self.board_id,)).fetchall()
            try:
                tasks = [Entity_Task(*row) for row in rows]
            except ValueError as error:
                raise OperationFailure("STORE_INVALID_STATE") from error
        return tasks
