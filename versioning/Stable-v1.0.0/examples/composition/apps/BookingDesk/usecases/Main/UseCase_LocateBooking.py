"""Generated from Minerva module UC-BOOKING-LOOKUP.

Source refs: UC-BOOKING-LOOKUP
Do not edit generated files by hand; update Minerva and regenerate."""

MINERVA_MODULE_ID = "UC-BOOKING-LOOKUP"
SOURCE_REFS = ('UC-BOOKING-LOOKUP',)

from apps.BookingDesk.usecases.Main.UseCase_LookupBooking import UseCase_LookupBooking

class UseCase_LocateBooking(UseCase_LookupBooking):
    """Terminology-aligned realization of the lookup use case."""

    def execute(self, actor_context, booking_code):
        return self.lookupBooking(actor_context, booking_code)
