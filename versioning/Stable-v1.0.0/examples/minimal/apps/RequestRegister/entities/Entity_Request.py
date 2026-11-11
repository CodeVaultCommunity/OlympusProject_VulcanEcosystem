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

    @classmethod
    def create(cls, request_code: str, quantity: int):
        return cls(request_code, quantity)

    @staticmethod
    def validate_quantity_is_a_positive_integer(quantity: int) -> None:
        Entity_Request.validateQuantity(quantity)

    @staticmethod
    def validate_request_code_is_non_empty_text(code: str) -> None:
        Entity_Request.validateCode(code)
