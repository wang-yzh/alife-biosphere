from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class NestConfig:
    x: int = 16
    y: int = 24
    radius: int = 3

    def __post_init__(self) -> None:
        if self.radius <= 0:
            raise ValueError("radius must be positive")


@dataclass(frozen=True)
class FoodPatchConfig:
    patch_id: str
    x: int
    y: int
    radius: int
    amount: int

    def __post_init__(self) -> None:
        if self.radius <= 0:
            raise ValueError("radius must be positive")
        if self.amount <= 0:
            raise ValueError("amount must be positive")


@dataclass(frozen=True)
class AntAgentConfig:
    ant_count: int = 32
    step_size: int = 1
    wander_turn_jitter: float = 0.55
    food_sense_radius: int = 24
    food_pickup_radius: int = 1
    nest_drop_radius: int = 3

    def __post_init__(self) -> None:
        if self.ant_count <= 0:
            raise ValueError("ant_count must be positive")
        if self.step_size <= 0:
            raise ValueError("step_size must be positive")
        if self.wander_turn_jitter < 0:
            raise ValueError("wander_turn_jitter must be non-negative")
        if self.food_sense_radius <= 0:
            raise ValueError("food_sense_radius must be positive")
        if self.food_pickup_radius < 0:
            raise ValueError("food_pickup_radius must be non-negative")
        if self.nest_drop_radius < 0:
            raise ValueError("nest_drop_radius must be non-negative")


@dataclass(frozen=True)
class AntSandboxConfig:
    seed: int = 7
    ticks: int = 180
    width: int = 64
    height: int = 48
    nest: NestConfig = field(default_factory=NestConfig)
    food_patches: tuple[FoodPatchConfig, ...] = field(
        default_factory=lambda: (
            FoodPatchConfig("food_a", x=38, y=14, radius=3, amount=120),
            FoodPatchConfig("food_b", x=48, y=35, radius=4, amount=180),
        )
    )
    ants: AntAgentConfig = field(default_factory=AntAgentConfig)

    def __post_init__(self) -> None:
        if self.ticks <= 0:
            raise ValueError("ticks must be positive")
        if self.width <= 0 or self.height <= 0:
            raise ValueError("width and height must be positive")
        if not self.food_patches:
            raise ValueError("at least one food patch is required")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
