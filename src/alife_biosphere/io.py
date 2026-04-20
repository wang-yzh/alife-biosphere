from __future__ import annotations

import json
from pathlib import Path

from .config import SimulationConfig
from .simulation import SimulationResult


def write_config(path: str | Path, config: SimulationConfig) -> None:
    Path(path).write_text(json.dumps(config.to_dict(), indent=2), encoding="utf-8")


def write_summary(path: str | Path, result: SimulationResult) -> None:
    Path(path).write_text(json.dumps(result.summary(), indent=2), encoding="utf-8")


def write_events(path: str | Path, result: SimulationResult) -> None:
    payload = [event.to_dict() for event in result.events]
    Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
