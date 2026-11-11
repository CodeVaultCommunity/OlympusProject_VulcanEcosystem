"""Generated from Minerva module CTL-REQUEST-STORE.

Source refs: TOL-REQUEST-STORE
Do not edit generated files by hand; update Minerva and regenerate."""

MINERVA_MODULE_ID = "CTL-REQUEST-STORE"
SOURCE_REFS = ('TOL-REQUEST-STORE',)

from apps.RequestRegister.tools.Tool_SqliteRequestStore import Tool_SqliteRequestStore as _ReferenceImplementation

class Tool_SqliteRequestStore(_ReferenceImplementation):
    """Concrete realization of TOL-REQUEST-STORE."""

    minerva_design = {
        "technology": 'SQLite',
        "configuration": ['database_path'],
        "lifecycle": 'application_scope_factory_with_operation_scoped_connections',
    }

    def store_request(self, request_code, quantity) -> object:
        """Realize OP-REQUEST-STORE through the verified SQLite implementation."""
        return super().storeRequest(request_code, quantity)
