"""Generated from Minerva module BND-BOOKING-CLI.

Source refs: BND-BOOKING-CLI
Do not edit generated files by hand; update Minerva and regenerate."""

MINERVA_MODULE_ID = "BND-BOOKING-CLI"
SOURCE_REFS = ('BND-BOOKING-CLI',)

from apps.BookingDesk.boundaries.Boundary_Json import Boundary_Json

class Boundary_BookingDeskCommandLine:
    """Interaction adapter; this is not a test scenario or observation point."""

    def __init__(self, application) -> None:
        self._delegate = Boundary_Json(application)

    def create_command(self, payload: dict, caller_token: str | None = None):
        """Expose UC-BOOKING-CREATE."""
        return self._delegate.invoke('create', payload, caller_token)

    def cancel_command(self, payload: dict, caller_token: str | None = None):
        """Expose UC-BOOKING-CANCEL."""
        return self._delegate.invoke('cancel', payload, caller_token)

    def lookup_command(self, payload: dict, caller_token: str | None = None):
        """Expose UC-BOOKING-LOOKUP."""
        return self._delegate.invoke('lookup', payload, caller_token)
