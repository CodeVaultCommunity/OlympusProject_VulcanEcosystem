"""UC-BOOKING-LOOKUP: independently authorized, including composed lookup."""
from apps.BookingDesk.entities.Entity_ActorContext import Entity_ActorContext
from apps.BookingDesk.entities.Entity_Booking import Entity_Booking
from apps.BookingDesk.support.OperationFailure import OperationFailure

class UseCase_LookupBooking:
    def __init__(self, store) -> None:
        self.store = store

    def lookupBooking(self, actor_context: Entity_ActorContext | None, booking_code: str) -> Entity_Booking:
        if not isinstance(actor_context, Entity_ActorContext) or not actor_context.permits("booking.lookup", "ACT-BOOKING-CLERK"):
            raise OperationFailure("DENIED")
        Entity_Booking.validateIdentity(booking_code)
        return self.store.loadBooking(booking_code)
