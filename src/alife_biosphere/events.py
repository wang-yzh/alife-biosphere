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

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "Event":
        return cls(
            tick=int(payload["tick"]),
            event_type=str(payload["event_type"]),
            organism_id=None if payload.get("organism_id") is None else str(payload["organism_id"]),
            habitat_id=None if payload.get("habitat_id") is None else str(payload["habitat_id"]),
            payload=dict(payload.get("payload", {})),
        )
