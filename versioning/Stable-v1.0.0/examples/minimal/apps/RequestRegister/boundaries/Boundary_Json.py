"""L4 projection shared by the local CLI and HTTP channel; the core owns authorization."""
from dataclasses import asdict
from apps.RequestRegister.support.OperationFailure import OperationFailure

class Boundary_Json:
    def __init__(self, composition) -> None:
        self.composition = composition

    def invoke(self, operation: str, payload: dict, token: str | None) -> tuple[int, dict]:
        if not isinstance(payload, dict):
            return 400, {"error": "INVALID_JSON_OBJECT"}
        context = self.composition.resolveActor(token)
        try:
            if operation == "submit":
                result = self.composition.submit.submitRequest(context, payload.get("request_code"), payload.get("quantity"))
            else:
                return 404, {"error": "UNKNOWN_OPERATION"}
            body = [asdict(item) for item in result] if isinstance(result, list) else asdict(result)
            return 200, {"result": body}
        except OperationFailure as error:
            status = 403 if error.code == "DENIED" else 503 if error.code == "STORE_UNAVAILABLE" else 500 if error.code == "STORE_INVALID_STATE" else 409
            body = {"error": error.code}
            if error.code == "STORE_UNAVAILABLE":
                body["write_outcome"] = error.write_outcome
            return status, body
        except ValueError as error:
            return 400, {"error": "INVALID_INPUT", "detail": str(error)}
