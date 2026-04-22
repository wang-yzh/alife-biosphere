from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import atan2, cos, dist, sin, tau

from .config import AntSandboxConfig
from ..events import Event
from ..rng import make_rng


TERRAIN_EFFECTS: dict[str, dict[str, float | bool]] = {
    "open_ground": {"move_cost": 1.0, "trail_factor": 1.0, "sense_factor": 1.0, "blocked": False},
    "dense_grass": {"move_cost": 1.28, "trail_factor": 0.78, "sense_factor": 0.82, "blocked": False},
    "sand": {"move_cost": 1.18, "trail_factor": 1.24, "sense_factor": 0.94, "blocked": False},
    "rock": {"move_cost": 9.0, "trail_factor": 0.0, "sense_factor": 0.0, "blocked": True},
}


@dataclass
class Nest:
    x: int
    y: int
    radius: int
    stored_food: int = 0
    upkeep_reserve: float = 0.0


@dataclass
class FoodPatch:
    patch_id: str
    x: int
    y: int
    radius: int
    amount: int
    max_amount: int
    regrowth_rate: int = 0
    relocate_on_depletion: bool = True
    respawn_delay_ticks: int = 28
    empty_ticks: int = 0
    respawn_count: int = 0
    nearby_ants: int = 0
    carrying_nearby: int = 0
    recent_pickups: int = 0
    competition_pressure: float = 0.0
    contested_ticks: int = 0
    depletion_count: int = 0


@dataclass
class SandboxAnt:
    ant_id: str
    x: int
    y: int
    heading: float
    energy: float
    range_bias: float
    trail_affinity: float
    harvest_drive: float
    carrying_food: bool = False
    target_patch_id: str | None = None
    outbound_commit_ticks: int = 0
    age: int = 0
    alive: bool = True
    parent_id: str | None = None
    lineage_id: str | None = None
    delivered_food: int = 0


@dataclass
class AntSandboxWorld:
    width: int
    height: int
    nest: Nest
    food_patches: list[FoodPatch]
    ants: list[SandboxAnt]
    tick: int = 0
    next_ant_index: int = 0
    occupied_cells: set[tuple[int, int]] = field(default_factory=set)
    events: list[Event] = field(default_factory=list)
    food_trail: dict[tuple[int, int], float] = field(default_factory=dict)
    home_trail: dict[tuple[int, int], float] = field(default_factory=dict)
    stale_field: dict[tuple[int, int], float] = field(default_factory=dict)
    terrain: dict[tuple[int, int], str] = field(default_factory=dict)

    def emit(self, event: Event) -> None:
        self.events.append(event)

    def alive_count(self) -> int:
        return sum(1 for ant in self.ants if ant.alive)

    def carrying_count(self) -> int:
        return sum(1 for ant in self.ants if ant.alive and ant.carrying_food)

    def food_remaining(self) -> int:
        return sum(patch.amount for patch in self.food_patches)

    def delivered_food_total(self) -> int:
        return self.nest.stored_food

    def allocate_ant_id(self) -> str:
        ant_id = f"ant_{self.next_ant_index:03d}"
        self.next_ant_index += 1
        return ant_id

    def summary(self) -> dict[str, int]:
        return {
            "ticks": self.tick,
            "alive": self.alive_count(),
            "carrying": self.carrying_count(),
            "nest_food": self.delivered_food_total(),
            "food_remaining": self.food_remaining(),
            "events": len(self.events),
        }

    def to_dict(self) -> dict[str, object]:
        return {
            "width": self.width,
            "height": self.height,
            "tick": self.tick,
            "nest": asdict(self.nest),
            "food_patches": [asdict(patch) for patch in self.food_patches],
            "ants": [asdict(ant) for ant in self.ants],
            "food_trail": {f"{x},{y}": value for (x, y), value in self.food_trail.items()},
            "home_trail": {f"{x},{y}": value for (x, y), value in self.home_trail.items()},
            "stale_field": {f"{x},{y}": value for (x, y), value in self.stale_field.items()},
            "terrain": {f"{x},{y}": kind for (x, y), kind in self.terrain.items()},
        }


def _clamp_cell(value: int, lower: int, upper: int) -> int:
    return min(upper, max(lower, value))


def _distance(a_x: int, a_y: int, b_x: int, b_y: int) -> float:
    return dist((a_x, a_y), (b_x, b_y))


def _clamp_unit(value: float) -> float:
    return min(1.0, max(0.0, value))


def terrain_kind(world: AntSandboxWorld, x: int, y: int) -> str:
    return world.terrain.get((x, y), "open_ground")


def terrain_effect(world: AntSandboxWorld, x: int, y: int) -> dict[str, float | bool]:
    return TERRAIN_EFFECTS[terrain_kind(world, x, y)]


def _apply_ellipse_terrain(
    terrain: dict[tuple[int, int], str],
    width: int,
    height: int,
    center_x: float,
    center_y: float,
    radius_x: float,
    radius_y: float,
    kind: str,
) -> None:
    min_x = max(0, int(center_x - radius_x) - 1)
    max_x = min(width - 1, int(center_x + radius_x) + 1)
    min_y = max(0, int(center_y - radius_y) - 1)
    max_y = min(height - 1, int(center_y + radius_y) + 1)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            dx = (x - center_x) / max(radius_x, 1.0)
            dy = (y - center_y) / max(radius_y, 1.0)
            if dx * dx + dy * dy <= 1.0:
                terrain[(x, y)] = kind


def _clear_safe_zone(terrain: dict[tuple[int, int], str], center_x: int, center_y: int, radius: int) -> None:
    for y in range(center_y - radius, center_y + radius + 1):
        for x in range(center_x - radius, center_x + radius + 1):
            if (x, y) in terrain and _distance(x, y, center_x, center_y) <= radius:
                terrain.pop((x, y), None)


def _generate_terrain(config: AntSandboxConfig) -> dict[tuple[int, int], str]:
    if not config.terrain.enabled:
        return {}
    terrain: dict[tuple[int, int], str] = {}
    width = config.width
    height = config.height

    _apply_ellipse_terrain(
        terrain,
        width,
        height,
        center_x=width * 0.34,
        center_y=height * 0.25,
        radius_x=max(8.0, width * 0.15),
        radius_y=max(6.0, height * 0.12),
        kind="dense_grass",
    )
    _apply_ellipse_terrain(
        terrain,
        width,
        height,
        center_x=width * 0.68,
        center_y=height * 0.74,
        radius_x=max(10.0, width * 0.18),
        radius_y=max(8.0, height * 0.14),
        kind="sand",
    )

    ridge_x = width // 2
    gap_a = height // 3
    gap_b = (height * 2) // 3
    for y in range(max(4, height // 8), min(height - 4, (height * 7) // 8)):
        if abs(y - gap_a) <= 4 or abs(y - gap_b) <= 5:
            continue
        terrain[(ridge_x, y)] = "rock"
        if y % 3 != 0:
            terrain[(ridge_x + 1, y)] = "rock"

    shelf_y = (height * 5) // 8
    for x in range((width * 3) // 5, min(width - 6, (width * 4) // 5)):
        if abs(x - (width * 7) // 10) <= 3:
            continue
        terrain[(x, shelf_y)] = "rock"

    _clear_safe_zone(terrain, config.nest.x, config.nest.y, config.nest.radius + 6)
    for patch in config.food_patches:
        _clear_safe_zone(terrain, patch.x, patch.y, patch.radius + 5)
    return terrain


def initialize_world(config: AntSandboxConfig) -> AntSandboxWorld:
    nest = Nest(
        x=_clamp_cell(config.nest.x, 0, config.width - 1),
        y=_clamp_cell(config.nest.y, 0, config.height - 1),
        radius=config.nest.radius,
        stored_food=config.nest.initial_stored_food,
    )
    food_patches = [
        FoodPatch(
            patch_id=patch.patch_id,
            x=_clamp_cell(patch.x, 0, config.width - 1),
            y=_clamp_cell(patch.y, 0, config.height - 1),
            radius=patch.radius,
            amount=patch.amount,
            max_amount=patch.amount if patch.max_amount is None else patch.max_amount,
            regrowth_rate=patch.regrowth_rate,
            relocate_on_depletion=patch.relocate_on_depletion,
            respawn_delay_ticks=patch.respawn_delay_ticks,
        )
        for patch in config.food_patches
    ]
    terrain = _generate_terrain(config)
    ants: list[SandboxAnt] = []
    occupied_cells: set[tuple[int, int]] = set()
    candidate_cells = sorted(
        [
            (_clamp_cell(nest.x + dx, 0, config.width - 1), _clamp_cell(nest.y + dy, 0, config.height - 1))
            for radius in range(max(2, nest.radius) + 3)
            for dy in range(-radius, radius + 1)
            for dx in range(-radius, radius + 1)
            if _distance(0, 0, dx, dy) <= max(2, nest.radius) + 1
            and terrain.get((_clamp_cell(nest.x + dx, 0, config.width - 1), _clamp_cell(nest.y + dy, 0, config.height - 1)), "open_ground") != "rock"
        ],
        key=lambda cell: (
            _distance(cell[0], cell[1], nest.x, nest.y),
            round(atan2(cell[1] - nest.y, cell[0] - nest.x), 6),
            cell[1],
            cell[0],
        ),
    )
    unique_cells: list[tuple[int, int]] = []
    seen_cells: set[tuple[int, int]] = set()
    for cell in candidate_cells:
        if cell in seen_cells:
            continue
        seen_cells.add(cell)
        unique_cells.append(cell)
    for index in range(config.ants.ant_count):
        angle = tau * (index / max(config.ants.ant_count, 1))
        spawn_x, spawn_y = unique_cells[index % len(unique_cells)]
        trait_rng = make_rng(config.seed, f"ant-sandbox:traits:{index}")
        count_scale = index / max(1, config.ants.ant_count - 1)
        range_bias = _clamp_unit(0.12 + 0.76 * count_scale + trait_rng.uniform(-0.12, 0.12))
        trail_phase = ((index * 7) % max(1, config.ants.ant_count)) / max(1, config.ants.ant_count - 1)
        trail_affinity = _clamp_unit(0.15 + 0.7 * trail_phase + trait_rng.uniform(-0.15, 0.15))
        harvest_phase = ((index * 13) % max(1, config.ants.ant_count)) / max(1, config.ants.ant_count - 1)
        harvest_drive = _clamp_unit(0.18 + 0.66 * harvest_phase + trait_rng.uniform(-0.16, 0.16))
        ant = SandboxAnt(
            ant_id=f"ant_{index:03d}",
            x=spawn_x,
            y=spawn_y,
            heading=round(angle, 6),
            energy=config.ants.initial_energy,
            range_bias=round(range_bias, 4),
            trail_affinity=round(trail_affinity, 4),
            harvest_drive=round(harvest_drive, 4),
            lineage_id=f"ant_{index:03d}",
        )
        ants.append(ant)
        occupied_cells.add((ant.x, ant.y))
    return AntSandboxWorld(
        width=config.width,
        height=config.height,
        nest=nest,
        food_patches=food_patches,
        ants=ants,
        next_ant_index=config.ants.ant_count,
        occupied_cells=occupied_cells,
        terrain=terrain,
    )
