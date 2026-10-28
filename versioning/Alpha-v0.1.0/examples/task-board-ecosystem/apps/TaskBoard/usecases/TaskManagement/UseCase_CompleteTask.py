"""UC-TASK-003: completing an existing task twice has the same observable result."""

from apps.TaskBoard.entities.Entity_ActorContext import Entity_ActorContext
from apps.TaskBoard.entities.Entity_Task import Entity_Task
from apps.TaskBoard.tools.Tool_SqliteTaskStore import Tool_SqliteTaskStore


class UseCase_CompleteTask:
    def __init__(self, task_store: Tool_SqliteTaskStore) -> None:
        self.task_store = task_store

    def completeTask(self, actor_context: Entity_ActorContext | None, task_id: str) -> Entity_Task:
        if not isinstance(actor_context, Entity_ActorContext) or not actor_context.canPerform("tasks:complete"):
            raise PermissionError("forbidden")
        if not isinstance(task_id, str) or not task_id:
            raise ValueError("task_id_required")
        task = self.task_store.getTask(task_id)
        if task is None:
            raise LookupError("task_not_found")
        if not task.isCompleted():
            task.complete()
            self.task_store.saveTask(task)
        return task
