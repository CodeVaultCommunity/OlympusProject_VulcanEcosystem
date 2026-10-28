"""Task data and the intrinsic pending -> completed state transition."""

from apps.TaskBoard.value_objects.ValueObject_TaskTitle import ValueObject_TaskTitle


class Entity_Task:
    __slots__ = ("_task_id", "_task_title", "_completed")

    def __init__(self, task_id: str, title: str, completed: bool = False) -> None:
        if not isinstance(task_id, str) or not task_id.strip():
            raise ValueError("task_id_required")
        if not isinstance(completed, bool):
            raise ValueError("completed_must_be_boolean")
        self._task_id = task_id
        self._task_title = ValueObject_TaskTitle(title)
        self._completed = completed

    def getId(self) -> str:
        return self._task_id

    def getTitle(self) -> str:
        return self._task_title.getValue()

    def isCompleted(self) -> bool:
        return self._completed

    def complete(self) -> None:
        self._completed = True
