from __future__ import annotations

from dataclasses import asdict, dataclass, field


def _payload_value(payload: dict[str, object], key: str, fallback: object) -> object:
    return payload[key] if key in payload else fallback


@dataclass(frozen=True)
class TerrainConfig:
    enabled: bool = True
    layout: str = "surface_showcase_walls"

    def __post_init__(self) -> None:
        if not self.layout:
            raise ValueError("layout must be non-empty")

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "TerrainConfig":
        default = cls()
        return cls(
            enabled=bool(_payload_value(payload, "enabled", default.enabled)),
            layout=str(_payload_value(payload, "layout", default.layout)),
        )


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

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "NestConfig":
        default = cls()
        return cls(
            x=int(_payload_value(payload, "x", default.x)),
            y=int(_payload_value(payload, "y", default.y)),
            radius=int(_payload_value(payload, "radius", default.radius)),
            initial_stored_food=int(_payload_value(payload, "initial_stored_food", default.initial_stored_food)),
            colony_upkeep_per_ant_tick=float(
                _payload_value(payload, "colony_upkeep_per_ant_tick", default.colony_upkeep_per_ant_tick)
            ),
        )


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

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "ColonyConfig":
        return cls(
            colony_id=str(payload["colony_id"]),
            display_name=str(payload["display_name"]),
            color=str(payload["color"]),
            ant_count=int(payload["ant_count"]),
            nest=NestConfig.from_dict(dict(payload["nest"])),
        )


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

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "FoodPatchConfig":
        return cls(
            patch_id=str(payload["patch_id"]),
            x=int(payload["x"]),
            y=int(payload["y"]),
            radius=int(payload["radius"]),
            amount=int(payload["amount"]),
            max_amount=None if payload.get("max_amount") is None else int(payload["max_amount"]),
            value_score=float(_payload_value(payload, "value_score", 1.0)),
            regrowth_rate=int(_payload_value(payload, "regrowth_rate", 0)),
            relocate_on_depletion=bool(_payload_value(payload, "relocate_on_depletion", True)),
            respawn_delay_ticks=int(_payload_value(payload, "respawn_delay_ticks", 28)),
            regrow_only_when_empty=bool(_payload_value(payload, "regrow_only_when_empty", False)),
        )


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
    corpse_enabled: bool = True
    corpse_decay_ticks: int = 64
    residue_enabled: bool = True
    residue_decay: float = 0.03
    trail_residue_deposit: float = 0.008
    nest_residue_deposit: float = 0.16
    corpse_residue_release: float = 0.14
    decomposer_enabled: bool = True
    decomposer_emerge_delay_ticks: int = 4
    decomposer_feed_rate: float = 0.14
    decomposer_decay: float = 0.05
    decomposer_spread_interval: int = 12
    decomposer_residue_threshold: float = 0.28
    decomposer_enrich_residue: float = 0.09

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
        if self.corpse_decay_ticks <= 0:
            raise ValueError("corpse_decay_ticks must be positive")
        if self.residue_decay < 0:
            raise ValueError("residue_decay must be non-negative")
        if self.trail_residue_deposit < 0:
            raise ValueError("trail_residue_deposit must be non-negative")
        if self.nest_residue_deposit < 0:
            raise ValueError("nest_residue_deposit must be non-negative")
        if self.corpse_residue_release < 0:
            raise ValueError("corpse_residue_release must be non-negative")
        if self.decomposer_emerge_delay_ticks < 0:
            raise ValueError("decomposer_emerge_delay_ticks must be non-negative")
        if self.decomposer_feed_rate < 0:
            raise ValueError("decomposer_feed_rate must be non-negative")
        if self.decomposer_decay < 0:
            raise ValueError("decomposer_decay must be non-negative")
        if self.decomposer_spread_interval <= 0:
            raise ValueError("decomposer_spread_interval must be positive")
        if self.decomposer_residue_threshold < 0:
            raise ValueError("decomposer_residue_threshold must be non-negative")
        if self.decomposer_enrich_residue < 0:
            raise ValueError("decomposer_enrich_residue must be non-negative")

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "AntAgentConfig":
        default = cls()
        return cls(
            ant_count=int(_payload_value(payload, "ant_count", default.ant_count)),
            max_population=int(_payload_value(payload, "max_population", default.max_population)),
            step_size=int(_payload_value(payload, "step_size", default.step_size)),
            wander_turn_jitter=float(_payload_value(payload, "wander_turn_jitter", default.wander_turn_jitter)),
            food_sense_radius=int(_payload_value(payload, "food_sense_radius", default.food_sense_radius)),
            nest_sense_radius=int(_payload_value(payload, "nest_sense_radius", default.nest_sense_radius)),
            food_pickup_radius=int(_payload_value(payload, "food_pickup_radius", default.food_pickup_radius)),
            nest_drop_radius=int(_payload_value(payload, "nest_drop_radius", default.nest_drop_radius)),
            max_age=int(_payload_value(payload, "max_age", default.max_age)),
            allow_spawning=bool(_payload_value(payload, "allow_spawning", default.allow_spawning)),
            spawn_food_cost=int(_payload_value(payload, "spawn_food_cost", default.spawn_food_cost)),
            spawn_interval=int(_payload_value(payload, "spawn_interval", default.spawn_interval)),
            inheritance_mode=str(_payload_value(payload, "inheritance_mode", default.inheritance_mode)),
            mutation_rate=float(_payload_value(payload, "mutation_rate", default.mutation_rate)),
            mutation_step=float(_payload_value(payload, "mutation_step", default.mutation_step)),
            pheromone_enabled=bool(_payload_value(payload, "pheromone_enabled", default.pheromone_enabled)),
            pheromone_sense_radius=int(_payload_value(payload, "pheromone_sense_radius", default.pheromone_sense_radius)),
            pheromone_weight=float(_payload_value(payload, "pheromone_weight", default.pheromone_weight)),
            trail_deposit=float(_payload_value(payload, "trail_deposit", default.trail_deposit)),
            home_trail_deposit=float(_payload_value(payload, "home_trail_deposit", default.home_trail_deposit)),
            trail_decay=float(_payload_value(payload, "trail_decay", default.trail_decay)),
            initial_energy=float(_payload_value(payload, "initial_energy", default.initial_energy)),
            max_energy=float(_payload_value(payload, "max_energy", default.max_energy)),
            metabolism_cost=float(_payload_value(payload, "metabolism_cost", default.metabolism_cost)),
            hunger_return_threshold=float(
                _payload_value(payload, "hunger_return_threshold", default.hunger_return_threshold)
            ),
            nest_feed_amount=float(_payload_value(payload, "nest_feed_amount", default.nest_feed_amount)),
            starvation_grace_ticks=int(_payload_value(payload, "starvation_grace_ticks", default.starvation_grace_ticks)),
            hostility_radius=int(_payload_value(payload, "hostility_radius", default.hostility_radius)),
            hostility_weight=float(_payload_value(payload, "hostility_weight", default.hostility_weight)),
            foreign_trail_weight=float(_payload_value(payload, "foreign_trail_weight", default.foreign_trail_weight)),
            combat_enabled=bool(_payload_value(payload, "combat_enabled", default.combat_enabled)),
            combat_radius=int(_payload_value(payload, "combat_radius", default.combat_radius)),
            combat_duration=int(_payload_value(payload, "combat_duration", default.combat_duration)),
            combat_cooldown=int(_payload_value(payload, "combat_cooldown", default.combat_cooldown)),
            combat_decision_threshold=float(
                _payload_value(payload, "combat_decision_threshold", default.combat_decision_threshold)
            ),
            corpse_enabled=bool(_payload_value(payload, "corpse_enabled", default.corpse_enabled)),
            corpse_decay_ticks=int(_payload_value(payload, "corpse_decay_ticks", default.corpse_decay_ticks)),
            residue_enabled=bool(_payload_value(payload, "residue_enabled", default.residue_enabled)),
            residue_decay=float(_payload_value(payload, "residue_decay", default.residue_decay)),
            trail_residue_deposit=float(
                _payload_value(payload, "trail_residue_deposit", default.trail_residue_deposit)
            ),
            nest_residue_deposit=float(
                _payload_value(payload, "nest_residue_deposit", default.nest_residue_deposit)
            ),
            corpse_residue_release=float(
                _payload_value(payload, "corpse_residue_release", default.corpse_residue_release)
            ),
            decomposer_enabled=bool(_payload_value(payload, "decomposer_enabled", default.decomposer_enabled)),
            decomposer_emerge_delay_ticks=int(
                _payload_value(payload, "decomposer_emerge_delay_ticks", default.decomposer_emerge_delay_ticks)
            ),
            decomposer_feed_rate=float(
                _payload_value(payload, "decomposer_feed_rate", default.decomposer_feed_rate)
            ),
            decomposer_decay=float(_payload_value(payload, "decomposer_decay", default.decomposer_decay)),
            decomposer_spread_interval=int(
                _payload_value(payload, "decomposer_spread_interval", default.decomposer_spread_interval)
            ),
            decomposer_residue_threshold=float(
                _payload_value(payload, "decomposer_residue_threshold", default.decomposer_residue_threshold)
            ),
            decomposer_enrich_residue=float(
                _payload_value(payload, "decomposer_enrich_residue", default.decomposer_enrich_residue)
            ),
        )


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

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "AntSandboxConfig":
        default = cls()
        colonies_payload = payload.get("colonies", default.to_dict()["colonies"])
        food_patches_payload = payload.get("food_patches", default.to_dict()["food_patches"])
        return cls(
            seed=int(_payload_value(payload, "seed", default.seed)),
            ticks=int(_payload_value(payload, "ticks", default.ticks)),
            width=int(_payload_value(payload, "width", default.width)),
            height=int(_payload_value(payload, "height", default.height)),
            nest=NestConfig.from_dict(dict(_payload_value(payload, "nest", default.to_dict()["nest"]))),
            colonies=tuple(ColonyConfig.from_dict(dict(colony)) for colony in colonies_payload),
            food_patches=tuple(FoodPatchConfig.from_dict(dict(patch)) for patch in food_patches_payload),
            ants=AntAgentConfig.from_dict(dict(_payload_value(payload, "ants", default.to_dict()["ants"]))),
            terrain=TerrainConfig.from_dict(dict(_payload_value(payload, "terrain", default.to_dict()["terrain"]))),
            disturbance_tick=int(_payload_value(payload, "disturbance_tick", default.disturbance_tick)),
            disturbance_food_shift=bool(
                _payload_value(payload, "disturbance_food_shift", default.disturbance_food_shift)
            ),
            disturbance_food_shift_dx=int(
                _payload_value(payload, "disturbance_food_shift_dx", default.disturbance_food_shift_dx)
            ),
            disturbance_food_shift_dy=int(
                _payload_value(payload, "disturbance_food_shift_dy", default.disturbance_food_shift_dy)
            ),
            disturbance_kill_radius=int(
                _payload_value(payload, "disturbance_kill_radius", default.disturbance_kill_radius)
            ),
        )
