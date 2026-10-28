"""ENT-TASK: exact data and canonical state; immutable public objects."""
from dataclasses import dataclass
from apps.TaskBoard.value_objects.ValueObject_TaskIdentity import ValueObject_TaskIdentity

@dataclass(frozen=True, slots=True)
class Entity_Task:
    task_id: str
    title: str
    status: str = "open"
    revision: int = 0

    def __post_init__(self) -> None:
        self.validateIdentity(self.task_id)
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("invalid_title")
        if self.status not in ("open", "completed") or type(self.revision) is not int or self.revision < 0:
            raise ValueError("invalid_stored_state")

    @staticmethod
    def validateIdentity(value) -> None:
        ValueObject_TaskIdentity(value)

    def complete(self):
        if self.status != "open":
            raise ValueError("already_completed")
        return Entity_Task(self.task_id, self.title, "completed", self.revision + 1)
