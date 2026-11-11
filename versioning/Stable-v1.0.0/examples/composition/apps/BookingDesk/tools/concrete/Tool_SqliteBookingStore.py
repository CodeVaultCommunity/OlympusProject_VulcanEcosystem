"""Generated from Minerva module CTL-BOOKING-STORE.

Source refs: TOL-BOOKING-STORE
Do not edit generated files by hand; update Minerva and regenerate."""

MINERVA_MODULE_ID = "CTL-BOOKING-STORE"
SOURCE_REFS = ('TOL-BOOKING-STORE',)

from apps.BookingDesk.tools.Tool_SqliteBookingStore import Tool_SqliteBookingStore as _ReferenceImplementation

class Tool_SqliteBookingStore(_ReferenceImplementation):
    """Concrete realization of TOL-BOOKING-STORE."""

    minerva_design = {
        "technology": 'SQLite',
        "configuration": ['database_path', 'busy_timeout_ms'],
        "lifecycle": 'application_scope_factory_with_operation_scoped_connections',
    }

    def load_booking(self, booking_code) -> object:
        """Realize OP-BOOKING-LOAD through the verified SQLite implementation."""
        return super().loadBooking(booking_code)

    def save_booking(self, booking, expected_version) -> object:
        """Realize OP-BOOKING-SAVE through the verified SQLite implementation."""
        return super().saveBooking(booking, expected_version)
