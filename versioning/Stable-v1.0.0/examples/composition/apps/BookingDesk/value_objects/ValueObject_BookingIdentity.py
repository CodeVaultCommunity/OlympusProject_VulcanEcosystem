import re

from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ValueObject_BookingIdentity:
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or re.fullmatch(r"[A-Z0-9]{1,12}", self.value) is None:
            raise ValueError("invalid_identifier")
