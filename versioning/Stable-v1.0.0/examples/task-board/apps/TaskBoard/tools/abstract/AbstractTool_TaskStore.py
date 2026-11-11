"""Generated from Minerva module TOL-TASK-STORE.

Source refs: TOL-TASK-STORE
Do not edit generated files by hand; update Minerva and regenerate."""

MINERVA_MODULE_ID = "TOL-TASK-STORE"
SOURCE_REFS = ('TOL-TASK-STORE',)

from typing import Protocol, runtime_checkable

@runtime_checkable
class AbstractTool_TaskStore(Protocol):
    def retain_a_new_task(self, task: object, board: object) -> object:
        """Implements OP-TASK-CREATE."""
        ...

    def read_one_task(self, task_identifier: str, board: object) -> object:
        """Implements OP-TASK-LOAD."""
        ...

    def retain_a_completion(self, task: object, expected_revision: int, board: object) -> object:
        """Implements OP-TASK-COMPLETE."""
        ...

    def read_the_board(self, board: object) -> object:
        """Implements OP-TASK-LIST."""
        ...
