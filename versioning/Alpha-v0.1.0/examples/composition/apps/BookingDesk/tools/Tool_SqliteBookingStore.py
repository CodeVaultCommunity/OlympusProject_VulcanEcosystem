"""Atomic insert/compare-and-save; ready Booking inputs are not revalidated."""
from apps.BookingDesk.entities.Entity_Booking import Entity_Booking
from apps.BookingDesk.support.OperationFailure import OperationFailure
from apps.BookingDesk.support.SqliteResource import SqliteResource

class Tool_SqliteBookingStore:
    def __init__(self, db_path: str) -> None:
        self.resource = SqliteResource(db_path)
        self.resource.initialize("CREATE TABLE IF NOT EXISTS bookings (code TEXT PRIMARY KEY COLLATE BINARY, title TEXT NOT NULL, status TEXT NOT NULL, version INTEGER NOT NULL)")

    def loadBooking(self, booking_code: str) -> Entity_Booking:
        with self.resource.open() as connection:
            row = connection.execute("SELECT code, title, status, version FROM bookings WHERE code = ?", (booking_code,)).fetchone()
        if row is None:
            raise OperationFailure("NOT_FOUND")
        try:
            return Entity_Booking(*row)
        except ValueError as error:
            raise OperationFailure("STORE_INVALID_STATE") from error

    def saveBooking(self, booking: Entity_Booking, expected_version: int) -> Entity_Booking:
        with self.resource.open(write=True) as connection:
            if expected_version == 0:
                result = connection.execute("INSERT INTO bookings VALUES (?, ?, ?, 1) ON CONFLICT(code) DO NOTHING", (booking.booking_code, booking.title, booking.status))
            else:
                result = connection.execute("UPDATE bookings SET title = ?, status = ?, version = version + 1 WHERE code = ? AND version = ?", (booking.title, booking.status, booking.booking_code, expected_version))
            if result.rowcount != 1:
                raise OperationFailure("VERSION_CONFLICT")
            row = connection.execute("SELECT code, title, status, version FROM bookings WHERE code = ?", (booking.booking_code,)).fetchone()
            retained = Entity_Booking(*row)
        return retained
