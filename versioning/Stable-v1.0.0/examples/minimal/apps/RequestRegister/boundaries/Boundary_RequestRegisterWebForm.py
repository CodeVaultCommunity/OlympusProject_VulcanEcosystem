"""Generated from Minerva module BND-REQUEST-WEB.

Source refs: BND-REQUEST-WEB
Do not edit generated files by hand; update Minerva and regenerate."""

MINERVA_MODULE_ID = "BND-REQUEST-WEB"
SOURCE_REFS = ('BND-REQUEST-WEB',)

from apps.RequestRegister.boundaries.Boundary_Json import Boundary_Json

class Boundary_RequestRegisterWebForm:
    """Interaction adapter; this is not a test scenario or observation point."""

    def __init__(self, application) -> None:
        self._delegate = Boundary_Json(application)

    def submit_request_form(self, payload: dict, caller_token: str | None = None):
        """Expose UC-REQUEST-SUBMIT."""
        return self._delegate.invoke('submit', payload, caller_token)
