from __future__ import annotations

from dataclasses import dataclass, field
from math import cos, sin, tau

from .config import AntSandboxConfig


@dataclass(frozen=True)
class Nest:
    x: int
    y: int
    radius: int
    stored_food: int = 0


@dataclass(frozen=True)
class FoodPatch:
    patch_id: str
    x: int
    y: int
    radius: int
    amount: int


@dataclass(frozen=True)
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


@dataclass
class AntSandboxWorld:
    width: int
    height: int
    nest: Nest
    food_patches: list[FoodPatch]
    ants: list[SandboxAnt]
    tick: int = 0
    occupied_cells: set[tuple[int, int]] = field(default_factory=set)


def _clamp_cell(value: int, lower: int, upper: int) -> int:
    return min(upper, max(lower, value))


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
    for index in range(config.ants.ant_count):
        angle = tau * (index / max(config.ants.ant_count, 1))
        ant = SandboxAnt(
            ant_id=f"ant_{index:03d}",
            x=_clamp_cell(nest.x + round(cos(angle) * min(2, nest.radius)), 0, config.width - 1),
            y=_clamp_cell(nest.y + round(sin(angle) * min(2, nest.radius)), 0, config.height - 1),
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
