"""Select concrete collaborators. Local demo tokens are not production authentication."""
import hmac
from apps.RequestRegister.entities.Entity_ActorContext import Entity_ActorContext
from apps.RequestRegister.tools.Tool_SqliteRequestStore import Tool_SqliteRequestStore
from apps.RequestRegister.usecases.Main.UseCase_SubmitRequest import UseCase_SubmitRequest

class AppComposition:
    def __init__(self, db_path: str, board_id: str = "board-A", token: str = "demo-editor") -> None:
        if not isinstance(token, str) or not token or not isinstance(board_id, str) or not board_id.strip():
            raise ValueError("invalid_composition_configuration")
        self.token = token
        self.board_id = None
        self.store = Tool_SqliteRequestStore(db_path)
        self.submit = UseCase_SubmitRequest(self.store)

    def resolveActor(self, token: str | None) -> Entity_ActorContext | None:
        if not isinstance(token, str) or not hmac.compare_digest(token.encode(), self.token.encode()):
            return None
        return Entity_ActorContext("local-operator", "ACT-REQUESTER", ('request.submit',), self.board_id)
