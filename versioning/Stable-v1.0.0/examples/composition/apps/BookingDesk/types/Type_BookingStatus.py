"""Generated from Minerva module TYP-BOOKING-STATUS.

Source refs: TYP-BOOKING-STATUS
Do not edit generated files by hand; update Minerva and regenerate."""

MINERVA_MODULE_ID = "TYP-BOOKING-STATUS"
SOURCE_REFS = ('TYP-BOOKING-STATUS',)

from enum import StrEnum

class Type_BookingStatus(StrEnum):
    ACTIVE = 'active'
    CANCELLED = 'cancelled'
