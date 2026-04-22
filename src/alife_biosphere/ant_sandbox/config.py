from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class NestConfig:
    x: int = 16
    y: int = 24
    radius: int = 3
    initial_stored_food: int = 18
    colony_upkeep_per_ant_tick: float = 0.002

    def __post_init__(self) -> None:
        if self.radius <= 0:
            raise ValueError("radius must be positive")
        if self.initial_stored_food < 0:
            raise ValueError("initial_stored_food must be non-negative")
        if self.colony_upkeep_per_ant_tick < 0:
            raise ValueError("colony_upkeep_per_ant_tick must be non-negative")


@dataclass(frozen=True)
class FoodPatchConfig:
    patch_id: str
    x: int
    y: int
    radius: int
    amount: int
    max_amount: int | None = None
    regrowth_rate: int = 0
    relocate_on_depletion: bool = True
    respawn_delay_ticks: int = 28

    def __post_init__(self) -> None:
        if self.radius <= 0:
            raise ValueError("radius must be positive")
        if self.amount <= 0:
            raise ValueError("amount must be positive")
        if self.max_amount is not None and self.max_amount <= 0:
            raise ValueError("max_amount must be positive when provided")
        if self.max_amount is not None and self.max_amount < self.amount:
            raise ValueError("max_amount must not be less than amount")
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
    food_sense_radius: int = 16
    nest_sense_radius: int = 8
    food_pickup_radius: int = 1
    nest_drop_radius: int = 3
    max_age: int = 1000
    spawn_food_cost: int = 8
    spawn_interval: int = 10
    pheromone_enabled: bool = True
    pheromone_sense_radius: int = 6
    pheromone_weight: float = 4.5
    trail_deposit: float = 1.4
    home_trail_deposit: float = 0.8
    trail_decay: float = 0.03
    initial_energy: float = 18.0
    max_energy: float = 20.0
    metabolism_cost: float = 0.03
    hunger_return_threshold: float = 6.0
    nest_feed_amount: float = 4.0

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
        if self.spawn_food_cost < 0:
            raise ValueError("spawn_food_cost must be non-negative")
        if self.spawn_interval <= 0:
            raise ValueError("spawn_interval must be positive")
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


@dataclass(frozen=True)
class AntSandboxConfig:
    seed: int = 7
    ticks: int = 180
    width: int = 64
    height: int = 48
    nest: NestConfig = field(default_factory=NestConfig)
    food_patches: tuple[FoodPatchConfig, ...] = field(
        default_factory=lambda: (
            FoodPatchConfig("food_a", x=38, y=14, radius=3, amount=48, max_amount=48, regrowth_rate=0, respawn_delay_ticks=16),
            FoodPatchConfig("food_b", x=48, y=35, radius=4, amount=72, max_amount=72, regrowth_rate=0, respawn_delay_ticks=18),
        )
    )
    ants: AntAgentConfig = field(default_factory=AntAgentConfig)
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
        if self.disturbance_tick < 0:
            raise ValueError("disturbance_tick must be non-negative")
        if self.disturbance_kill_radius < 0:
            raise ValueError("disturbance_kill_radius must be non-negative")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
