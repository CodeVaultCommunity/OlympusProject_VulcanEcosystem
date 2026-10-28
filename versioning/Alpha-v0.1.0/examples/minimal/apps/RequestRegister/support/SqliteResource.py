"""Per-operation connection ownership. A commit error is conservatively unknown; no retry."""
from contextlib import contextmanager
from pathlib import Path
import sqlite3
from apps.RequestRegister.support.OperationFailure import OperationFailure

class SqliteResource:
    def __init__(self, db_path: str) -> None:
        self.db_path = str(Path(db_path).resolve())
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def open(self, write: bool = False):
        connection = None
        commit_started = False
        try:
            connection = sqlite3.connect(self.db_path, timeout=5, isolation_level=None)
            connection.execute("BEGIN IMMEDIATE" if write else "BEGIN")
            yield connection
            commit_started = True
            connection.commit()
        except (sqlite3.Error, OSError, OverflowError) as error:
            outcome = "unknown" if write and commit_started else "not_applied"
            if connection is not None:
                try:
                    connection.rollback()
                except sqlite3.Error:
                    if write:
                        outcome = "unknown"
            raise OperationFailure("STORE_UNAVAILABLE", outcome) from error
        except BaseException:
            if connection is not None:
                connection.rollback()
            raise
        finally:
            if connection is not None:
                connection.close()

    def initialize(self, statement: str) -> None:
        with self.open(write=True) as connection:
            connection.execute(statement)
