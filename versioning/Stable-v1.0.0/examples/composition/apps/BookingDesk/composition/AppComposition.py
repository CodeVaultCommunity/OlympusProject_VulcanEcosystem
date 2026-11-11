"""Select concrete collaborators. Local demo tokens are not production authentication."""
import hmac
from apps.BookingDesk.entities.Entity_ActorContext import Entity_ActorContext
from apps.BookingDesk.tools.Tool_SqliteBookingStore import Tool_SqliteBookingStore
from apps.BookingDesk.usecases.Main.UseCase_LookupBooking import UseCase_LookupBooking
from apps.BookingDesk.usecases.Main.UseCase_CreateBooking import UseCase_CreateBooking
from apps.BookingDesk.usecases.Main.UseCase_CancelBooking import UseCase_CancelBooking

class AppComposition:
    def __init__(self, db_path: str, board_id: str = "board-A", token: str = "demo-editor") -> None:
        if not isinstance(token, str) or not token or not isinstance(board_id, str) or not board_id.strip():
            raise ValueError("invalid_composition_configuration")
        self.token = token
        self.board_id = None
        self.store = Tool_SqliteBookingStore(db_path)
        self.lookup = UseCase_LookupBooking(self.store)
        self.create = UseCase_CreateBooking(self.store)
        self.cancel = UseCase_CancelBooking(self.store, self.lookup)

    def resolveActor(self, token: str | None) -> Entity_ActorContext | None:
        if not isinstance(token, str) or not hmac.compare_digest(token.encode(), self.token.encode()):
            return None
        return Entity_ActorContext("local-operator", "ACT-BOOKING-CLERK", ('booking.lookup', 'booking.create', 'booking.cancel'), self.board_id)
