from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Event:
    tick: int
    event_type: str
    organism_id: str | None
    habitat_id: str | None
    payload: dict[str, object]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
