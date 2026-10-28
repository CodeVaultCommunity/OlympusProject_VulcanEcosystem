"""UC-TASK-002: authorization also applies to direct and read-only invocations."""

from apps.TaskBoard.entities.Entity_ActorContext import Entity_ActorContext
from apps.TaskBoard.entities.Entity_Task import Entity_Task
from apps.TaskBoard.tools.Tool_SqliteTaskStore import Tool_SqliteTaskStore


class UseCase_ListTasks:
    def __init__(self, task_store: Tool_SqliteTaskStore) -> None:
        self.task_store = task_store

    def listTasks(self, actor_context: Entity_ActorContext | None) -> list[Entity_Task]:
        if not isinstance(actor_context, Entity_ActorContext) or not actor_context.canPerform("tasks:read"):
            raise PermissionError("forbidden")
        return self.task_store.listTasks()
