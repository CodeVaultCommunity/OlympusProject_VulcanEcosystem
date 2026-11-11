"""UC-BOOKING-CREATE: independently authorized, including composed lookup."""
from apps.BookingDesk.entities.Entity_ActorContext import Entity_ActorContext
from apps.BookingDesk.entities.Entity_Booking import Entity_Booking
from apps.BookingDesk.support.OperationFailure import OperationFailure

class UseCase_CreateBooking:
    def __init__(self, store) -> None:
        self.store = store

    def createBooking(self, actor_context: Entity_ActorContext | None, booking_code: str, title: str) -> Entity_Booking:
        if not isinstance(actor_context, Entity_ActorContext) or not actor_context.permits("booking.create", "ACT-BOOKING-CLERK"):
            raise OperationFailure("DENIED")
        booking = Entity_Booking(booking_code, title)
        return self.store.saveBooking(booking, 0)

    def execute(self, actor_context: Entity_ActorContext | None, booking_code: str, title: str) -> Entity_Booking:
        return self.createBooking(actor_context, booking_code, title)
