"""UC-TASK-001: authorize the caller, then create a task through a capability."""

from apps.TaskBoard.entities.Entity_ActorContext import Entity_ActorContext
from apps.TaskBoard.entities.Entity_Task import Entity_Task
from apps.TaskBoard.tools.Tool_SqliteTaskStore import Tool_SqliteTaskStore


class UseCase_CreateTask:
    def __init__(self, task_store: Tool_SqliteTaskStore) -> None:
        self.task_store = task_store

    def createTask(self, actor_context: Entity_ActorContext | None, title: str) -> Entity_Task:
        if not isinstance(actor_context, Entity_ActorContext) or not actor_context.canPerform("tasks:create"):
            raise PermissionError("forbidden")
        return self.task_store.createTask(title)
