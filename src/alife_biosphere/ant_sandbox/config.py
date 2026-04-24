from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class TerrainConfig:
    enabled: bool = True
    layout: str = "surface_showcase_walls"

    def __post_init__(self) -> None:
        if not self.layout:
            raise ValueError("layout must be non-empty")


@dataclass(frozen=True)
class NestConfig:
    x: int = 28
    y: int = 48
    radius: int = 4
    initial_stored_food: int = 24
    colony_upkeep_per_ant_tick: float = 0.002

    def __post_init__(self) -> None:
        if self.radius <= 0:
            raise ValueError("radius must be positive")
        if self.initial_stored_food < 0:
            raise ValueError("initial_stored_food must be non-negative")
        if self.colony_upkeep_per_ant_tick < 0:
            raise ValueError("colony_upkeep_per_ant_tick must be non-negative")


@dataclass(frozen=True)
class ColonyConfig:
    colony_id: str
    display_name: str
    color: str
    ant_count: int
    nest: NestConfig

    def __post_init__(self) -> None:
        if not self.colony_id:
            raise ValueError("colony_id must be non-empty")
        if not self.display_name:
            raise ValueError("display_name must be non-empty")
        if not self.color:
            raise ValueError("color must be non-empty")
        if self.ant_count <= 0:
            raise ValueError("ant_count must be positive")


@dataclass(frozen=True)
class FoodPatchConfig:
    patch_id: str
    x: int
    y: int
    radius: int
    amount: int
    max_amount: int | None = None
    value_score: float = 1.0
    regrowth_rate: int = 0
    relocate_on_depletion: bool = True
    respawn_delay_ticks: int = 28
    regrow_only_when_empty: bool = False

    def __post_init__(self) -> None:
        if self.radius <= 0:
            raise ValueError("radius must be positive")
        if self.amount <= 0:
            raise ValueError("amount must be positive")
        if self.max_amount is not None and self.max_amount <= 0:
            raise ValueError("max_amount must be positive when provided")
        if self.max_amount is not None and self.max_amount < self.amount:
            raise ValueError("max_amount must not be less than amount")
        if self.value_score <= 0:
            raise ValueError("value_score must be positive")
        if self.regrowth_rate < 0:
            raise ValueError("regrowth_rate must be non-negative")
        if self.respawn_delay_ticks <= 0:
            raise ValueError("respawn_delay_ticks must be positive")


@dataclass(frozen=True)
class AntAgentConfig:
    ant_count: int = 32
    max_population: int = 32
    step_size: int = 1
    wander_turn_jitter: float = 0.55
    food_sense_radius: int = 24
    nest_sense_radius: int = 10
    food_pickup_radius: int = 1
    nest_drop_radius: int = 3
    max_age: int = 1000
    allow_spawning: bool = True
    spawn_food_cost: int = 8
    spawn_interval: int = 10
    inheritance_mode: str = "clone"
    mutation_rate: float = 0.0
    mutation_step: float = 0.05
    pheromone_enabled: bool = True
    pheromone_sense_radius: int = 10
    pheromone_weight: float = 4.5
    trail_deposit: float = 1.4
    home_trail_deposit: float = 0.8
    trail_decay: float = 0.03
    initial_energy: float = 18.0
    max_energy: float = 20.0
    metabolism_cost: float = 0.04
    hunger_return_threshold: float = 6.0
    nest_feed_amount: float = 4.0
    starvation_grace_ticks: int = 60
    hostility_radius: int = 3
    hostility_weight: float = 1.0
    foreign_trail_weight: float = 0.25
    combat_enabled: bool = False
    combat_radius: int = 1
    combat_duration: int = 6
    combat_cooldown: int = 4
    combat_decision_threshold: float = 1.2

    def __post_init__(self) -> None:
        if self.ant_count <= 0:
            raise ValueError("ant_count must be positive")
        if self.max_population < self.ant_count:
            raise ValueError("max_population must not be smaller than ant_count")
        if self.step_size <= 0:
            raise ValueError("step_size must be positive")
        if self.wander_turn_jitter < 0:
            raise ValueError("wander_turn_jitter must be non-negative")
        if self.food_sense_radius <= 0:
            raise ValueError("food_sense_radius must be positive")
        if self.nest_sense_radius <= 0:
            raise ValueError("nest_sense_radius must be positive")
        if self.food_pickup_radius < 0:
            raise ValueError("food_pickup_radius must be non-negative")
        if self.nest_drop_radius < 0:
            raise ValueError("nest_drop_radius must be non-negative")
        if self.max_age <= 0:
            raise ValueError("max_age must be positive")
        if self.hostility_radius < 0:
            raise ValueError("hostility_radius must be non-negative")
        if self.hostility_weight < 0:
            raise ValueError("hostility_weight must be non-negative")
        if self.foreign_trail_weight < 0:
            raise ValueError("foreign_trail_weight must be non-negative")
        if self.spawn_food_cost < 0:
            raise ValueError("spawn_food_cost must be non-negative")
        if self.spawn_interval <= 0:
            raise ValueError("spawn_interval must be positive")
        if self.inheritance_mode not in {"clone", "mutate", "resample"}:
            raise ValueError("inheritance_mode must be clone, mutate, or resample")
        if not 0.0 <= self.mutation_rate <= 1.0:
            raise ValueError("mutation_rate must be between 0 and 1")
        if self.mutation_step < 0:
            raise ValueError("mutation_step must be non-negative")
        if self.pheromone_sense_radius < 0:
            raise ValueError("pheromone_sense_radius must be non-negative")
        if self.pheromone_weight < 0:
            raise ValueError("pheromone_weight must be non-negative")
        if self.trail_deposit < 0:
            raise ValueError("trail_deposit must be non-negative")
        if self.home_trail_deposit < 0:
            raise ValueError("home_trail_deposit must be non-negative")
        if self.trail_decay < 0:
            raise ValueError("trail_decay must be non-negative")
        if self.initial_energy <= 0:
            raise ValueError("initial_energy must be positive")
        if self.max_energy < self.initial_energy:
            raise ValueError("max_energy must not be less than initial_energy")
        if self.metabolism_cost <= 0:
            raise ValueError("metabolism_cost must be positive")
        if self.hunger_return_threshold < 0:
            raise ValueError("hunger_return_threshold must be non-negative")
        if self.nest_feed_amount <= 0:
            raise ValueError("nest_feed_amount must be positive")
        if self.starvation_grace_ticks < 0:
            raise ValueError("starvation_grace_ticks must be non-negative")
        if self.combat_radius < 0:
            raise ValueError("combat_radius must be non-negative")
        if self.combat_duration < 0:
            raise ValueError("combat_duration must be non-negative")
        if self.combat_cooldown < 0:
            raise ValueError("combat_cooldown must be non-negative")
        if self.combat_decision_threshold < 0:
            raise ValueError("combat_decision_threshold must be non-negative")


@dataclass(frozen=True)
class AntSandboxConfig:
    seed: int = 7
    ticks: int = 320
    width: int = 128
    height: int = 96
    nest: NestConfig = field(default_factory=NestConfig)
    colonies: tuple[ColonyConfig, ...] = field(
        default_factory=lambda: (
            ColonyConfig(
                colony_id="wei",
                display_name="Wei",
                color="#375a7f",
                ant_count=11,
                nest=NestConfig(x=18, y=48, radius=4, initial_stored_food=14, colony_upkeep_per_ant_tick=0.0025),
            ),
            ColonyConfig(
                colony_id="shu",
                display_name="Shu",
                color="#b24a3a",
                ant_count=11,
                nest=NestConfig(x=92, y=20, radius=4, initial_stored_food=14, colony_upkeep_per_ant_tick=0.0025),
            ),
            ColonyConfig(
                colony_id="wu",
                display_name="Wu",
                color="#2f8f5b",
                ant_count=10,
                nest=NestConfig(x=80, y=66, radius=4, initial_stored_food=14, colony_upkeep_per_ant_tick=0.0025),
            ),
        )
    )
    food_patches: tuple[FoodPatchConfig, ...] = field(
        default_factory=lambda: (
            FoodPatchConfig("food_near", x=58, y=30, radius=4, amount=36, max_amount=36, value_score=0.85, regrowth_rate=0, respawn_delay_ticks=18),
            FoodPatchConfig("food_gap", x=66, y=50, radius=5, amount=80, max_amount=80, value_score=1.08, regrowth_rate=0, respawn_delay_ticks=22),
            FoodPatchConfig("food_far", x=92, y=58, radius=7, amount=160, max_amount=160, value_score=1.5, regrowth_rate=0, respawn_delay_ticks=26),
        )
    )
    ants: AntAgentConfig = field(default_factory=AntAgentConfig)
    terrain: TerrainConfig = field(default_factory=TerrainConfig)
    disturbance_tick: int = 0
    disturbance_food_shift: bool = False
    disturbance_food_shift_dx: int = 0
    disturbance_food_shift_dy: int = 0
    disturbance_kill_radius: int = 0

    def __post_init__(self) -> None:
        if self.ticks <= 0:
            raise ValueError("ticks must be positive")
        if self.width <= 0 or self.height <= 0:
            raise ValueError("width and height must be positive")
        if not self.food_patches:
            raise ValueError("at least one food patch is required")
        if len({colony.colony_id for colony in self.colonies}) != len(self.colonies):
            raise ValueError("colony_id values must be unique")
        if self.disturbance_tick < 0:
            raise ValueError("disturbance_tick must be non-negative")
        if self.disturbance_kill_radius < 0:
            raise ValueError("disturbance_kill_radius must be non-negative")

    def resolved_colonies(self) -> tuple[ColonyConfig, ...]:
        if self.colonies:
            return self.colonies
        return (
            ColonyConfig(
                colony_id="solo",
                display_name="Solo",
                color="#7e5e42",
                ant_count=self.ants.ant_count,
                nest=self.nest,
            ),
        )

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
