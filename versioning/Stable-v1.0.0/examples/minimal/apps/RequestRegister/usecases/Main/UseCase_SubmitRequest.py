"""UC-REQUEST-SUBMIT; authorization precedes canonical construction and tool access."""
from apps.RequestRegister.entities.Entity_ActorContext import Entity_ActorContext
from apps.RequestRegister.entities.Entity_Request import Entity_Request
from apps.RequestRegister.support.OperationFailure import OperationFailure

class UseCase_SubmitRequest:
    def __init__(self, store) -> None:
        self.store = store

    def submitRequest(self, actor_context: Entity_ActorContext | None, request_code: str, quantity: int) -> Entity_Request:
        if not isinstance(actor_context, Entity_ActorContext) or not actor_context.permits("request.submit", "ACT-REQUESTER"):
            raise OperationFailure("DENIED")
        request = Entity_Request(request_code, quantity)
        return self.store.storeRequest(request.request_code, request.quantity)

    def execute(self, actor_context: Entity_ActorContext | None, request_code: str, quantity: int) -> Entity_Request:
        return self.submitRequest(actor_context, request_code, quantity)
