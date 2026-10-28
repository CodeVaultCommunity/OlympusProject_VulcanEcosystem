"""Select collaborators once and resolve demonstration identities at the trusted edge."""

import hmac

from apps.TaskBoard.entities.Entity_ActorContext import Entity_ActorContext
from apps.TaskBoard.tools.Tool_SqliteTaskStore import Tool_SqliteTaskStore
from apps.TaskBoard.usecases.TaskManagement.UseCase_CreateTask import UseCase_CreateTask
from apps.TaskBoard.usecases.TaskManagement.UseCase_ListTasks import UseCase_ListTasks
from apps.TaskBoard.usecases.TaskManagement.UseCase_CompleteTask import UseCase_CompleteTask


class AppComposition:
    def __init__(self, db_path: str, editor_token: str = "demo-editor", reader_token: str = "demo-reader") -> None:
        if not editor_token or not reader_token or editor_token == reader_token:
            raise ValueError("tokens_must_be_nonempty_and_distinct")
        self.editor_token = editor_token
        self.reader_token = reader_token
        self.task_store = Tool_SqliteTaskStore(db_path)
        self.create_task = UseCase_CreateTask(self.task_store)
        self.list_tasks = UseCase_ListTasks(self.task_store)
        self.complete_task = UseCase_CompleteTask(self.task_store)

    def resolveActor(self, token: str | None) -> Entity_ActorContext | None:
        if not isinstance(token, str):
            return None
        candidate = token.encode("utf-8")
        if hmac.compare_digest(candidate, self.editor_token.encode("utf-8")):
            return Entity_ActorContext("demo-editor", ("tasks:create", "tasks:read", "tasks:complete"))
        if hmac.compare_digest(candidate, self.reader_token.encode("utf-8")):
            return Entity_ActorContext("demo-reader", ("tasks:read",))
        return None
