"""UC-TASK-LIST: authorization precedes entity validation and persistence."""
from apps.TaskBoard.entities.Entity_ActorContext import Entity_ActorContext
from apps.TaskBoard.entities.Entity_Task import Entity_Task
from apps.TaskBoard.support.OperationFailure import OperationFailure

class UseCase_ListTasks:
    def __init__(self, store, board_id: str) -> None:
        self.store = store
        self.board_id = board_id

    def listTasks(self, actor_context: Entity_ActorContext | None) -> list[Entity_Task]:
        if not isinstance(actor_context, Entity_ActorContext) or not actor_context.permits("task.list", "ACT-BOARD-MEMBER", self.board_id):
            raise OperationFailure("DENIED")
        return self.store.listTasks()

    def execute(self, actor_context: Entity_ActorContext | None) -> list[Entity_Task]:
        return self.listTasks(actor_context)
