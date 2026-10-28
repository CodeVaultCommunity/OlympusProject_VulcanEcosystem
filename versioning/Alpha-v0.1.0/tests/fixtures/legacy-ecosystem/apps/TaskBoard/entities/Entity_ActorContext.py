"""A trusted caller supplies this local context; it is not a JSON request field."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Entity_ActorContext:
    actor_id: str | None
    permissions: tuple[str, ...]
    resolution: str = "resolved"
    known_actor: bool = True

    def __post_init__(self) -> None:
        if self.actor_id is not None and not isinstance(self.actor_id, str):
            raise ValueError("actor_id_must_be_text_or_none")
        if not isinstance(self.permissions, tuple) or any(not isinstance(item, str) for item in self.permissions):
            raise ValueError("permissions_must_be_tuple_of_text")
        if not isinstance(self.resolution, str) or not isinstance(self.known_actor, bool):
            raise ValueError("invalid_context_resolution")

    def canPerform(self, permission: str) -> bool:
        return (
            self.resolution == "resolved"
            and self.known_actor
            and isinstance(self.actor_id, str)
            and bool(self.actor_id.strip())
            and permission in self.permissions
        )
