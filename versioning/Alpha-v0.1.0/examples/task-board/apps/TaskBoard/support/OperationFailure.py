"""Documented refusal/failure; certainty concerns this invocation's write only."""
class OperationFailure(Exception):
    def __init__(self, code: str, write_outcome: str = "not_applied") -> None:
        self.code = code
        self.write_outcome = write_outcome
        super().__init__(code)
