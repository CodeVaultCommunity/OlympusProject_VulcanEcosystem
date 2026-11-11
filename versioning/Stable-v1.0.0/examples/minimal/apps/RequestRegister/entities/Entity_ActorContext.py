"""Trusted invocation data. Only the configured authority or a trusted direct caller creates it."""
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Entity_ActorContext:
    principal: str
    role: str
    permissions: tuple[str, ...]
    board_id: str | None = None
    issuer: str = "local-demo"
    authenticated: bool = True
    valid: bool = True
    known: bool = True
    resolved: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.principal, str) or not isinstance(self.role, str):
            raise ValueError("invalid_context_data")
        if not isinstance(self.permissions, tuple) or any(not isinstance(p, str) for p in self.permissions):
            raise ValueError("invalid_permissions")
        if not isinstance(self.issuer, str) or self.board_id is not None and not isinstance(self.board_id, str):
            raise ValueError("invalid_context_origin")
        if any(type(v) is not bool for v in (self.authenticated, self.valid, self.known, self.resolved)):
            raise ValueError("invalid_context_flags")

    def permits(self, permission: str, role: str, board_id: str | None = None) -> bool:
        return bool(self.principal.strip()) and self.issuer == "local-demo" and self.authenticated and self.valid and self.known and self.resolved and self.role == role and permission in self.permissions and self.board_id == board_id
