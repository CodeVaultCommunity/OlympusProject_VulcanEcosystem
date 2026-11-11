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

    @classmethod
    def create(cls, task_identifier: str, title: str, status: str = "open", revision: int = 0):
        return cls(task_identifier, title, status, revision)

    @staticmethod
    def validate_task_identifier(candidate: str) -> None:
        Entity_Task.validateIdentity(candidate)

    @staticmethod
    def validate_new_task_validity(candidate) -> None:
        if isinstance(candidate, Entity_Task):
            if candidate.status != "open" or candidate.revision != 0:
                raise ValueError("invalid_new_task")
            return
        if not isinstance(candidate, str) or not candidate.strip():
            raise ValueError("invalid_title")

    @staticmethod
    def validate_completion_transition(candidate) -> None:
        status = candidate.status if isinstance(candidate, Entity_Task) else candidate
        if status != "open":
            raise ValueError("already_completed")
