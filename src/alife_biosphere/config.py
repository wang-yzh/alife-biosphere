from __future__ import annotations

from dataclasses import asdict, dataclass, field


HABITAT_FAMILIES = {"nursery", "refuge", "frontier", "wild"}


@dataclass(frozen=True)
class HabitatConfig:
    habitat_id: str
    habitat_family: str = "wild"
    capacity: int = 8
    initial_resource_level: float = 20.0
    max_resource_level: float = 24.0
    hazard_level: float = 0.1
    climate_state: float = 0.0
    regeneration_rate: float = 1.0
    climate_drift: float = 0.02
    climate_push: float = 0.0
    refuge_score: float = 0.0

    def __post_init__(self) -> None:
        if self.habitat_family not in HABITAT_FAMILIES:
            raise ValueError("habitat_family must be one of nursery/refuge/frontier/wild")
        if self.capacity <= 0:
            raise ValueError("capacity must be positive")
        if self.initial_resource_level < 0:
            raise ValueError("initial_resource_level must be non-negative")
        if self.max_resource_level <= 0:
            raise ValueError("max_resource_level must be positive")
        if self.initial_resource_level > self.max_resource_level:
            raise ValueError("initial_resource_level must not exceed max_resource_level")
        if not 0.0 <= self.hazard_level <= 1.0:
            raise ValueError("hazard_level must be within [0, 1]")
        if self.regeneration_rate < 0:
            raise ValueError("regeneration_rate must be non-negative")
        if self.climate_drift < 0:
            raise ValueError("climate_drift must be non-negative")
        if not 0.0 <= self.refuge_score <= 1.0:
            raise ValueError("refuge_score must be within [0, 1]")


@dataclass(frozen=True)
class OrganismConfig:
    initial_energy: float = 12.0
    initial_matter: float = 8.0
    initial_integrity: float = 1.0
    initial_information: float = 0.0
    metabolism_cost: float = 0.6
    harvest_gain: float = 1.2
    repair_gain_scale: float = 0.03
    hazard_damage_scale: float = 0.25
    crowding_integrity_penalty: float = 0.2
    movement_cooldown_ticks: int = 2

    def __post_init__(self) -> None:
        if self.initial_energy <= 0:
            raise ValueError("initial_energy must be positive")
        if self.initial_matter < 0:
            raise ValueError("initial_matter must be non-negative")
        if not 0.0 < self.initial_integrity <= 1.0:
            raise ValueError("initial_integrity must be within (0, 1]")
        if self.initial_information < 0:
            raise ValueError("initial_information must be non-negative")
        if self.metabolism_cost <= 0:
            raise ValueError("metabolism_cost must be positive")
        if self.harvest_gain <= 0:
            raise ValueError("harvest_gain must be positive")
        if self.repair_gain_scale < 0:
            raise ValueError("repair_gain_scale must be non-negative")
        if self.hazard_damage_scale < 0:
            raise ValueError("hazard_damage_scale must be non-negative")
        if self.crowding_integrity_penalty < 0:
            raise ValueError("crowding_integrity_penalty must be non-negative")
        if self.movement_cooldown_ticks < 0:
            raise ValueError("movement_cooldown_ticks must be non-negative")


@dataclass(frozen=True)
class WorldConfig:
    seed: int = 7
    ticks: int = 20
    founder_count: int = 8
    habitats: tuple[HabitatConfig, ...] = field(
        default_factory=lambda: (
            HabitatConfig(
                habitat_id="nursery_a",
                habitat_family="nursery",
                capacity=2,
                initial_resource_level=14.0,
                max_resource_level=16.0,
                hazard_level=0.03,
                regeneration_rate=1.0,
                refuge_score=0.2,
            ),
            HabitatConfig(
                habitat_id="nursery_b",
                habitat_family="nursery",
                capacity=2,
                initial_resource_level=14.0,
                max_resource_level=16.0,
                hazard_level=0.03,
                regeneration_rate=1.0,
                refuge_score=0.2,
            ),
            HabitatConfig(
                habitat_id="refuge",
                habitat_family="refuge",
                capacity=4,
                initial_resource_level=12.0,
                max_resource_level=14.0,
                hazard_level=0.02,
                regeneration_rate=0.7,
                refuge_score=1.0,
            ),
            HabitatConfig(
                habitat_id="frontier_a",
                habitat_family="frontier",
                capacity=3,
                initial_resource_level=16.0,
                max_resource_level=18.0,
                hazard_level=0.08,
                regeneration_rate=0.9,
                climate_drift=0.03,
            ),
            HabitatConfig(
                habitat_id="frontier_b",
                habitat_family="frontier",
                capacity=3,
                initial_resource_level=16.0,
                max_resource_level=18.0,
                hazard_level=0.08,
                regeneration_rate=0.9,
                climate_drift=0.03,
            ),
            HabitatConfig(
                habitat_id="wild_a",
                habitat_family="wild",
                capacity=2,
                initial_resource_level=20.0,
                max_resource_level=22.0,
                hazard_level=0.16,
                regeneration_rate=1.1,
                climate_drift=0.04,
            ),
            HabitatConfig(
                habitat_id="wild_b",
                habitat_family="wild",
                capacity=2,
                initial_resource_level=20.0,
                max_resource_level=22.0,
                hazard_level=0.16,
                regeneration_rate=1.1,
                climate_drift=0.04,
            ),
        )
    )
    habitat_edges: tuple[tuple[str, str], ...] = field(
        default_factory=lambda: (
            ("nursery_a", "refuge"),
            ("nursery_b", "refuge"),
            ("refuge", "frontier_a"),
            ("refuge", "frontier_b"),
            ("frontier_a", "wild_a"),
            ("frontier_b", "wild_b"),
            ("frontier_a", "frontier_b"),
        )
    )
    movement_cost: float = 0.8
    migration_integrity_risk: float = 0.04
    occupancy_stress_scale: float = 1.0
    crowding_energy_penalty: float = 0.35
    maturity_age: int = 3
    senescence_age: int = 24
    max_age: int = 50
    reproduction_chance: float = 0.35
    reproduction_energy_threshold: float = 13.5
    reproduction_matter_threshold: float = 8.5
    reproduction_integrity_threshold: float = 0.7
    reproduction_energy_cost: float = 4.0
    reproduction_matter_cost: float = 2.0
    reproduction_integrity_cost: float = 0.05
    offspring_energy_scale: float = 0.55
    offspring_matter_scale: float = 0.5
    disturbance_interval: int = 0
    disturbance_resource_shock: float = 0.0
    disturbance_hazard_pulse: float = 0.0
    disturbance_seed_offset: int = 1_000
    organism: OrganismConfig = field(default_factory=OrganismConfig)

    def __post_init__(self) -> None:
        if self.ticks <= 0:
            raise ValueError("ticks must be positive")
        if self.founder_count <= 0:
            raise ValueError("founder_count must be positive")
        if not self.habitats:
            raise ValueError("at least one habitat is required")
        if self.movement_cost < 0:
            raise ValueError("movement_cost must be non-negative")
        if self.migration_integrity_risk < 0:
            raise ValueError("migration_integrity_risk must be non-negative")
        if self.occupancy_stress_scale < 0:
            raise ValueError("occupancy_stress_scale must be non-negative")
        if self.crowding_energy_penalty < 0:
            raise ValueError("crowding_energy_penalty must be non-negative")
        if self.maturity_age < 0:
            raise ValueError("maturity_age must be non-negative")
        if self.senescence_age < self.maturity_age:
            raise ValueError("senescence_age must not precede maturity_age")
        if self.max_age < self.senescence_age:
            raise ValueError("max_age must not precede senescence_age")
        if not 0.0 <= self.reproduction_chance <= 1.0:
            raise ValueError("reproduction_chance must be within [0, 1]")
        if self.reproduction_energy_threshold <= 0:
            raise ValueError("reproduction_energy_threshold must be positive")
        if self.reproduction_matter_threshold < 0:
            raise ValueError("reproduction_matter_threshold must be non-negative")
        if not 0.0 < self.reproduction_integrity_threshold <= 1.0:
            raise ValueError("reproduction_integrity_threshold must be within (0, 1]")
        if self.reproduction_energy_cost < 0:
            raise ValueError("reproduction_energy_cost must be non-negative")
        if self.reproduction_matter_cost < 0:
            raise ValueError("reproduction_matter_cost must be non-negative")
        if self.reproduction_integrity_cost < 0:
            raise ValueError("reproduction_integrity_cost must be non-negative")
        if not 0.0 < self.offspring_energy_scale <= 1.0:
            raise ValueError("offspring_energy_scale must be within (0, 1]")
        if not 0.0 < self.offspring_matter_scale <= 1.0:
            raise ValueError("offspring_matter_scale must be within (0, 1]")
        if self.disturbance_interval < 0:
            raise ValueError("disturbance_interval must be non-negative")
        if self.disturbance_resource_shock < 0:
            raise ValueError("disturbance_resource_shock must be non-negative")
        if self.disturbance_hazard_pulse < 0:
            raise ValueError("disturbance_hazard_pulse must be non-negative")
        habitat_ids = {habitat.habitat_id for habitat in self.habitats}
        if len(habitat_ids) != len(self.habitats):
            raise ValueError("habitat_id values must be unique")
        for left, right in self.habitat_edges:
            if left not in habitat_ids or right not in habitat_ids:
                raise ValueError("habitat_edges must reference known habitat ids")
            if left == right:
                raise ValueError("habitat_edges must connect distinct habitats")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class SimulationConfig:
    world: WorldConfig = field(default_factory=WorldConfig)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
