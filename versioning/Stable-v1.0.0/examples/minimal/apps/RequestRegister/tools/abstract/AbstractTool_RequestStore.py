"""Generated from Minerva module TOL-REQUEST-STORE.

Source refs: TOL-REQUEST-STORE
Do not edit generated files by hand; update Minerva and regenerate."""

MINERVA_MODULE_ID = "TOL-REQUEST-STORE"
SOURCE_REFS = ('TOL-REQUEST-STORE',)

from typing import Protocol, runtime_checkable

@runtime_checkable
class AbstractTool_RequestStore(Protocol):
    def store_request(self, request_code: str, quantity: int) -> object:
        """Implements OP-REQUEST-STORE."""
        ...
