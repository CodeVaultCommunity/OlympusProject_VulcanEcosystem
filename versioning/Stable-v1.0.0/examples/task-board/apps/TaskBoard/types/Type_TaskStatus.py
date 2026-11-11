"""Generated from Minerva module TYP-TASK-STATUS.

Source refs: TYP-TASK-STATUS
Do not edit generated files by hand; update Minerva and regenerate."""

MINERVA_MODULE_ID = "TYP-TASK-STATUS"
SOURCE_REFS = ('TYP-TASK-STATUS',)

from enum import StrEnum

class Type_TaskStatus(StrEnum):
    OPEN = 'open'
    COMPLETED = 'completed'
