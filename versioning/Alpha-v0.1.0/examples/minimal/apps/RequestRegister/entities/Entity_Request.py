"""ENT-REQUEST: exact nonempty code, then positive integer quantity."""
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Entity_Request:
    request_code: str
    quantity: int

    def __post_init__(self) -> None:
        self.validateCode(self.request_code)
        self.validateQuantity(self.quantity)

    @staticmethod
    def validateCode(value) -> None:
        if not isinstance(value, str) or not value:
            raise ValueError("invalid_code")

    @staticmethod
    def validateQuantity(value) -> None:
        if type(value) is not int or value < 1:
            raise ValueError("invalid_quantity")
