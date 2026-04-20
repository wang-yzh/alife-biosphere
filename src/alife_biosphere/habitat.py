from __future__ import annotations

from dataclasses import dataclass, field

from .config import HabitatConfig


def _clamp(value: float, lower: float, upper: float) -> float:
    return min(upper, max(lower, value))


@dataclass
class Habitat:
    habitat_id: str
    habitat_family: str
    capacity: int
    resource_level: float
    max_resource_level: float
    hazard_level: float
    climate_state: float
    regeneration_rate: float
    climate_drift: float
    climate_push: float
    refuge_score: float
    neighbors: tuple[str, ...] = ()
    occupancy_pressure: float = 0.0
    recent_occupancy: float = 0.0
    depletion_trace: float = 0.0
    disturbance_trace: float = 0.0
    occupants: set[str] = field(default_factory=set)

    @classmethod
    def from_config(cls, config: HabitatConfig) -> "Habitat":
        return cls(
            habitat_id=config.habitat_id,
            habitat_family=config.habitat_family,
            capacity=config.capacity,
            resource_level=config.initial_resource_level,
            max_resource_level=config.max_resource_level,
            hazard_level=config.hazard_level,
            climate_state=config.climate_state,
            regeneration_rate=config.regeneration_rate,
            climate_drift=config.climate_drift,
            climate_push=config.climate_push,
            refuge_score=config.refuge_score,
        )

    def set_neighbors(self, neighbors: tuple[str, ...]) -> None:
        self.neighbors = neighbors

    def recompute_pressure(self, occupancy_stress_scale: float) -> None:
        occupant_count = len(self.occupants)
        occupancy_ratio = occupant_count / self.capacity
        self.occupancy_pressure = max(0.0, occupancy_ratio - 1.0) * occupancy_stress_scale
        self.recent_occupancy = 0.8 * self.recent_occupancy + 0.2 * occupant_count

    def regenerate(self, climate_noise: float) -> None:
        self.resource_level = _clamp(
            self.resource_level + self.regeneration_rate - self.occupancy_pressure * 0.25,
            0.0,
            self.max_resource_level,
        )
        self.climate_state = _clamp(
            self.climate_state + self.climate_push + climate_noise,
            -1.0,
            1.0,
        )
        depletion_gap = self.max_resource_level - self.resource_level
        self.depletion_trace = 0.7 * self.depletion_trace + 0.3 * depletion_gap
        self.disturbance_trace *= 0.85
