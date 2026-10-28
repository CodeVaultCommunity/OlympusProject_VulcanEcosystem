"""OP-REQUEST-STORE consumes validated scalars; uniqueness is an atomic storage condition."""
from apps.RequestRegister.entities.Entity_Request import Entity_Request
from apps.RequestRegister.support.SqliteResource import SqliteResource
from apps.RequestRegister.support.OperationFailure import OperationFailure

class Tool_SqliteRequestStore:
    def __init__(self, db_path: str) -> None:
        self.resource = SqliteResource(db_path)
        self.resource.initialize("CREATE TABLE IF NOT EXISTS requests (code TEXT PRIMARY KEY COLLATE BINARY, quantity TEXT NOT NULL)")

    def storeRequest(self, request_code: str, quantity: int) -> Entity_Request:
        with self.resource.open(write=True) as connection:
            result = connection.execute("INSERT INTO requests(code, quantity) VALUES (?, ?) ON CONFLICT(code) DO NOTHING", (request_code, str(quantity)))
            if result.rowcount != 1:
                raise OperationFailure("DUPLICATE_CODE")
            # This is hydration of a raw retained record, not validation of an input entity.
            row = connection.execute("SELECT code, quantity FROM requests WHERE code = ?", (request_code,)).fetchone()
            retained = Entity_Request(row[0], int(row[1]))
        return retained

    def readRequest(self, request_code: str) -> Entity_Request | None:
        """Technical observation for persistence verification, not an extra UCS case."""
        with self.resource.open() as connection:
            row = connection.execute("SELECT code, quantity FROM requests WHERE code = ?", (request_code,)).fetchone()
        return Entity_Request(row[0], int(row[1])) if row else None
