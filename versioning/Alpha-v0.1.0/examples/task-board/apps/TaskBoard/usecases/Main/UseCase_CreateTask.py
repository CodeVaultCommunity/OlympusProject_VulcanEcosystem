"""UC-TASK-CREATE: authorization precedes entity validation and persistence."""
from apps.TaskBoard.entities.Entity_ActorContext import Entity_ActorContext
from apps.TaskBoard.entities.Entity_Task import Entity_Task
from apps.TaskBoard.support.OperationFailure import OperationFailure

class UseCase_CreateTask:
    def __init__(self, store, board_id: str) -> None:
        self.store = store
        self.board_id = board_id

    def createTask(self, actor_context: Entity_ActorContext | None, task_id: str, title: str) -> Entity_Task:
        if not isinstance(actor_context, Entity_ActorContext) or not actor_context.permits("task.create", "ACT-BOARD-MEMBER", self.board_id):
            raise OperationFailure("DENIED")
        task = Entity_Task(task_id, title)
        return self.store.createTask(task)
