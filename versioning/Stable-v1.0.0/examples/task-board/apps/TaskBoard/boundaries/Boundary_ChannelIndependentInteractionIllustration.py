"""Generated from Minerva module BND-TASK-ILLUSTRATION.

Source refs: BND-TASK-ILLUSTRATION
Do not edit generated files by hand; update Minerva and regenerate."""

MINERVA_MODULE_ID = "BND-TASK-ILLUSTRATION"
SOURCE_REFS = ('BND-TASK-ILLUSTRATION',)

from apps.TaskBoard.boundaries.Boundary_Json import Boundary_Json

class Boundary_ChannelIndependentInteractionIllustration:
    """Interaction adapter; this is not a test scenario or observation point."""

    def __init__(self, application) -> None:
        self._delegate = Boundary_Json(application)

    def create_task(self, payload: dict, caller_token: str | None = None):
        """Expose UC-TASK-CREATE."""
        return self._delegate.invoke('create', payload, caller_token)

    def complete_task(self, payload: dict, caller_token: str | None = None):
        """Expose UC-TASK-COMPLETE."""
        return self._delegate.invoke('complete', payload, caller_token)

    def list_tasks(self, payload: dict, caller_token: str | None = None):
        """Expose UC-TASK-LIST."""
        return self._delegate.invoke('list', payload, caller_token)
