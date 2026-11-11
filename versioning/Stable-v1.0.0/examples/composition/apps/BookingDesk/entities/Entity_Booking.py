"""ENT-BOOKING: exact data and canonical state; immutable public objects."""
from dataclasses import dataclass
from apps.BookingDesk.value_objects.ValueObject_BookingIdentity import ValueObject_BookingIdentity

@dataclass(frozen=True, slots=True)
class Entity_Booking:
    booking_code: str
    title: str
    status: str = "active"
    version: int = 0

    def __post_init__(self) -> None:
        self.validateIdentity(self.booking_code)
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("invalid_title")
        if self.status not in ("active", "cancelled") or type(self.version) is not int or self.version < 0:
            raise ValueError("invalid_stored_state")

    @staticmethod
    def validateIdentity(value) -> None:
        ValueObject_BookingIdentity(value)

    def cancel(self):
        if self.status != "active":
            raise ValueError("already_cancelled")
        return Entity_Booking(self.booking_code, self.title, "cancelled", self.version)

    @classmethod
    def create(cls, booking_code: str, title: str, status: str = "active", version: int = 0):
        return cls(booking_code, title, status, version)

    @staticmethod
    def validate_booking_code_format(booking_code: str) -> None:
        Entity_Booking.validateIdentity(booking_code)

    @staticmethod
    def validate_cancellation_is_allowed_only_from_active(current_status: str) -> None:
        if current_status != "active":
            raise ValueError("already_cancelled")

    @staticmethod
    def validate_booking_title_validity(title: str) -> None:
        if not isinstance(title, str) or not title.strip():
            raise ValueError("invalid_title")
