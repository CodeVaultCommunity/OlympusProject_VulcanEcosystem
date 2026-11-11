from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ValueObject_TaskIdentity:
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or not self.value.strip():
            raise ValueError("invalid_identifier")
