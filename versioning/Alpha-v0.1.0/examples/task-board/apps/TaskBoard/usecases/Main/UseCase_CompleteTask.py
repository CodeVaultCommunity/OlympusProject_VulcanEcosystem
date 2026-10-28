"""UC-TASK-COMPLETE: authorization precedes entity validation and persistence."""
from apps.TaskBoard.entities.Entity_ActorContext import Entity_ActorContext
from apps.TaskBoard.entities.Entity_Task import Entity_Task
from apps.TaskBoard.support.OperationFailure import OperationFailure

class UseCase_CompleteTask:
    def __init__(self, store, board_id: str) -> None:
        self.store = store
        self.board_id = board_id

    def completeTask(self, actor_context: Entity_ActorContext | None, task_id: str) -> Entity_Task:
        if not isinstance(actor_context, Entity_ActorContext) or not actor_context.permits("task.complete", "ACT-BOARD-MEMBER", self.board_id):
            raise OperationFailure("DENIED")
        Entity_Task.validateIdentity(task_id)
        task = self.store.loadTask(task_id)
        if task.status == "completed":
            raise OperationFailure("ALREADY_COMPLETED")
        return self.store.completeTask(task.complete(), task.revision)
