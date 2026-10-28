"""A value is immutable; only Entity_Task uses it in production code."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValueObject_TaskTitle:
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise ValueError("title_must_be_text")
        normalized = self.value.strip()
        if not 1 <= len(normalized) <= 120:
            raise ValueError("title_length_must_be_between_1_and_120")
        object.__setattr__(self, "value", normalized)

    def getValue(self) -> str:
        return self.value
