"""UC-BOOKING-CANCEL: independently authorized, including composed lookup."""
from apps.BookingDesk.entities.Entity_ActorContext import Entity_ActorContext
from apps.BookingDesk.entities.Entity_Booking import Entity_Booking
from apps.BookingDesk.support.OperationFailure import OperationFailure

class UseCase_CancelBooking:
    def __init__(self, store, lookup_case) -> None:
        self.store = store
        self.lookup_case = lookup_case

    def cancelBooking(self, actor_context: Entity_ActorContext | None, booking_code: str) -> Entity_Booking:
        if not isinstance(actor_context, Entity_ActorContext) or not actor_context.permits("booking.cancel", "ACT-BOOKING-CLERK"):
            raise OperationFailure("DENIED")
        booking = self.lookup_case.lookupBooking(actor_context, booking_code)
        if booking.status == "cancelled":
            raise OperationFailure("ALREADY_CANCELLED")
        return self.store.saveBooking(booking.cancel(), booking.version)

    def execute(self, actor_context: Entity_ActorContext | None, booking_code: str) -> Entity_Booking:
        return self.cancelBooking(actor_context, booking_code)
