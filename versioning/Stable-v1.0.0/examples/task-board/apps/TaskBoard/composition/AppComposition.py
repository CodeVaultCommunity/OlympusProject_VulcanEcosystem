"""Select concrete collaborators. Local demo tokens are not production authentication."""
import hmac
from apps.TaskBoard.entities.Entity_ActorContext import Entity_ActorContext
from apps.TaskBoard.tools.Tool_SqliteTaskStore import Tool_SqliteTaskStore
from apps.TaskBoard.usecases.Main.UseCase_CreateTask import UseCase_CreateTask
from apps.TaskBoard.usecases.Main.UseCase_CompleteTask import UseCase_CompleteTask
from apps.TaskBoard.usecases.Main.UseCase_ListTasks import UseCase_ListTasks

class AppComposition:
    def __init__(self, db_path: str, board_id: str = "board-A", token: str = "demo-editor") -> None:
        if not isinstance(token, str) or not token or not isinstance(board_id, str) or not board_id.strip():
            raise ValueError("invalid_composition_configuration")
        self.token = token
        self.board_id = board_id
        self.store = Tool_SqliteTaskStore(db_path, board_id)
        self.create = UseCase_CreateTask(self.store, board_id)
        self.complete = UseCase_CompleteTask(self.store, board_id)
        self.list = UseCase_ListTasks(self.store, board_id)

    def resolveActor(self, token: str | None) -> Entity_ActorContext | None:
        if not isinstance(token, str) or not hmac.compare_digest(token.encode(), self.token.encode()):
            return None
        return Entity_ActorContext("local-operator", "ACT-BOARD-MEMBER", ('task.create', 'task.complete', 'task.list'), self.board_id)
