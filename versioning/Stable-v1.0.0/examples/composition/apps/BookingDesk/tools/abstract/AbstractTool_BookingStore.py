"""Generated from Minerva module TOL-BOOKING-STORE.

Source refs: TOL-BOOKING-STORE
Do not edit generated files by hand; update Minerva and regenerate."""

MINERVA_MODULE_ID = "TOL-BOOKING-STORE"
SOURCE_REFS = ('TOL-BOOKING-STORE',)

from typing import Protocol, runtime_checkable

@runtime_checkable
class AbstractTool_BookingStore(Protocol):
    def load_booking(self, booking_code: str) -> object:
        """Implements OP-BOOKING-LOAD."""
        ...

    def save_booking(self, booking: object, expected_version: int) -> object:
        """Implements OP-BOOKING-SAVE."""
        ...
