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
    base_hazard_level: float
    hazard_level: float
    climate_state: float
    base_regeneration_rate: float
    regeneration_rate: float
    climate_drift: float
    climate_push: float
    refuge_score: float
    neighbors: tuple[str, ...] = ()
    occupancy_pressure: float = 0.0
    recent_occupancy: float = 0.0
    depletion_trace: float = 0.0
    disturbance_trace: float = 0.0
    memory_field: float = 0.0
    recovery_lag: int = 0
    empty_ticks: int = 0
    occupants: set[str] = field(default_factory=set)

    @classmethod
    def from_config(cls, config: HabitatConfig) -> "Habitat":
        return cls(
            habitat_id=config.habitat_id,
            habitat_family=config.habitat_family,
            capacity=config.capacity,
            resource_level=config.initial_resource_level,
            max_resource_level=config.max_resource_level,
            base_hazard_level=config.hazard_level,
            hazard_level=config.hazard_level,
            climate_state=config.climate_state,
            base_regeneration_rate=config.regeneration_rate,
            regeneration_rate=config.regeneration_rate,
            climate_drift=config.climate_drift,
            climate_push=config.climate_push,
            refuge_score=config.refuge_score,
        )

    def set_neighbors(self, neighbors: tuple[str, ...]) -> None:
        self.neighbors = neighbors

    def colonization_pressure(self) -> float:
        return _clamp(
            0.65 * self.memory_field + 0.35 * min(self.recovery_lag / 12.0, 1.0),
            0.0,
            1.0,
        )

    def recompute_pressure(self, occupancy_stress_scale: float) -> None:
        occupant_count = len(self.occupants)
        occupancy_ratio = occupant_count / self.capacity
        self.occupancy_pressure = max(0.0, occupancy_ratio - 1.0) * occupancy_stress_scale
        self.recent_occupancy = 0.8 * self.recent_occupancy + 0.2 * occupant_count
        if occupant_count == 0:
            self.empty_ticks += 1
        else:
            self.empty_ticks = 0

    def update_memory(self) -> None:
        occupancy_load = min(1.5, self.recent_occupancy / self.capacity)
        depletion_load = min(1.0, self.depletion_trace / max(self.max_resource_level, 1e-6))
        disturbance_load = min(1.0, self.disturbance_trace / max(self.max_resource_level, 1e-6))
        empty_relief = min(1.0, self.empty_ticks / 5.0)
        self.memory_field = _clamp(
            0.62 * self.memory_field
            + 0.09 * depletion_load
            + 0.06 * disturbance_load
            + 0.05 * occupancy_load
            - 0.07 * empty_relief
            - 0.02 * self.refuge_score,
            0.0,
            1.0,
        )
        if self.empty_ticks > 0 and (disturbance_load > 0.08 or depletion_load > 0.2 or self.memory_field > 0.22):
            self.recovery_lag = min(self.recovery_lag + 1, 999)
        elif self.empty_ticks > 0 or occupancy_load > 0:
            self.recovery_lag = max(0, self.recovery_lag - 1)
        regen_scale = _clamp(
            1.0
            - 0.20 * self.memory_field
            - 0.10 * depletion_load
            + 0.08 * empty_relief
            + 0.04 * self.refuge_score,
            0.55,
            1.15,
        )
        hazard_shift = (
            0.08 * self.memory_field
            + 0.06 * disturbance_load
            - 0.03 * empty_relief
            - 0.03 * self.refuge_score
        )
        self.regeneration_rate = self.base_regeneration_rate * regen_scale
        self.hazard_level = _clamp(self.base_hazard_level + hazard_shift, 0.0, 1.0)

    def regenerate(self, climate_noise: float) -> None:
        self.update_memory()
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
