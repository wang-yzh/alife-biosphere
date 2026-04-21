from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import atan2, cos, dist, sin, tau

from .config import AntSandboxConfig
from ..events import Event


@dataclass
class Nest:
    x: int
    y: int
    radius: int
    stored_food: int = 0


@dataclass
class FoodPatch:
    patch_id: str
    x: int
    y: int
    radius: int
    amount: int


@dataclass
class SandboxAnt:
    ant_id: str
    x: int
    y: int
    heading: float
    carrying_food: bool = False
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
    occupied_cells: set[tuple[int, int]] = field(default_factory=set)
    events: list[Event] = field(default_factory=list)

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
        }


def _clamp_cell(value: int, lower: int, upper: int) -> int:
    return min(upper, max(lower, value))


def _distance(a_x: int, a_y: int, b_x: int, b_y: int) -> float:
    return dist((a_x, a_y), (b_x, b_y))


def initialize_world(config: AntSandboxConfig) -> AntSandboxWorld:
    nest = Nest(
        x=_clamp_cell(config.nest.x, 0, config.width - 1),
        y=_clamp_cell(config.nest.y, 0, config.height - 1),
        radius=config.nest.radius,
    )
    food_patches = [
        FoodPatch(
            patch_id=patch.patch_id,
            x=_clamp_cell(patch.x, 0, config.width - 1),
            y=_clamp_cell(patch.y, 0, config.height - 1),
            radius=patch.radius,
            amount=patch.amount,
        )
        for patch in config.food_patches
    ]
    ants: list[SandboxAnt] = []
    occupied_cells: set[tuple[int, int]] = set()
    candidate_cells = sorted(
        [
            (_clamp_cell(nest.x + dx, 0, config.width - 1), _clamp_cell(nest.y + dy, 0, config.height - 1))
            for radius in range(max(2, nest.radius) + 3)
            for dy in range(-radius, radius + 1)
            for dx in range(-radius, radius + 1)
            if _distance(0, 0, dx, dy) <= max(2, nest.radius) + 1
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
        ant = SandboxAnt(
            ant_id=f"ant_{index:03d}",
            x=spawn_x,
            y=spawn_y,
            heading=round(angle, 6),
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
        occupied_cells=occupied_cells,
    )
