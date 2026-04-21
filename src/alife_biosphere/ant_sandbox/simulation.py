from __future__ import annotations

from dataclasses import dataclass
from math import atan2, cos, dist, sin, tau

from ..events import Event
from ..rng import make_rng
from .config import AntSandboxConfig
from .world import AntSandboxWorld, FoodPatch, SandboxAnt, initialize_world


@dataclass(frozen=True)
class AntSandboxResult:
    world: AntSandboxWorld

    @property
    def events(self) -> list[Event]:
        return self.world.events

    def summary(self) -> dict[str, int]:
        return self.world.summary()


def _clamp(value: int, lower: int, upper: int) -> int:
    return min(upper, max(lower, value))


def _distance(a_x: int, a_y: int, b_x: int, b_y: int) -> float:
    return dist((a_x, a_y), (b_x, b_y))


def _food_within_range(ant: SandboxAnt, patches: list[FoodPatch], radius: int) -> FoodPatch | None:
    visible = [
        patch
        for patch in patches
        if patch.amount > 0 and _distance(ant.x, ant.y, patch.x, patch.y) <= radius
    ]
    if not visible:
        return None
    return min(visible, key=lambda patch: (_distance(ant.x, ant.y, patch.x, patch.y), patch.patch_id))


def _target_heading(from_x: int, from_y: int, to_x: int, to_y: int) -> float:
    return atan2(to_y - from_y, to_x - from_x)


def _candidate_cells(world: AntSandboxWorld, ant: SandboxAnt, config: AntSandboxConfig) -> list[tuple[int, int]]:
    step = config.ants.step_size
    cells = []
    for dy in (-step, 0, step):
        for dx in (-step, 0, step):
            if dx == 0 and dy == 0:
                continue
            nx = _clamp(ant.x + dx, 0, world.width - 1)
            ny = _clamp(ant.y + dy, 0, world.height - 1)
            cells.append((nx, ny))
    return cells


def _choose_step(
    world: AntSandboxWorld,
    ant: SandboxAnt,
    config: AntSandboxConfig,
    tick: int,
) -> tuple[int, int, float]:
    rng = make_rng(config.seed, f"ant-sandbox:{tick}:{ant.ant_id}:move")
    target_x: int | None = None
    target_y: int | None = None
    if ant.carrying_food:
        target_x = world.nest.x
        target_y = world.nest.y
    else:
        patch = _food_within_range(ant, world.food_patches, config.ants.food_sense_radius)
        if patch is not None:
            target_x = patch.x
            target_y = patch.y
    if target_x is not None and target_y is not None:
        target_heading = _target_heading(ant.x, ant.y, target_x, target_y)
    else:
        distance_from_nest = _distance(ant.x, ant.y, world.nest.x, world.nest.y)
        outward_heading = _target_heading(world.nest.x, world.nest.y, ant.x, ant.y)
        if distance_from_nest <= world.nest.radius + 5:
            base_heading = outward_heading
        else:
            base_heading = ant.heading
        if ant.x <= 1 or ant.x >= world.width - 2 or ant.y <= 1 or ant.y >= world.height - 2:
            center_x = world.width // 2
            center_y = world.height // 2
            base_heading = _target_heading(ant.x, ant.y, center_x, center_y)
        jitter = rng.uniform(-config.ants.wander_turn_jitter, config.ants.wander_turn_jitter)
        target_heading = (base_heading + jitter) % tau
    candidates = _candidate_cells(world, ant, config)
    free_candidates = [
        cell for cell in candidates if cell not in world.occupied_cells or cell == (ant.x, ant.y)
    ]
    if not free_candidates:
        return ant.x, ant.y, target_heading
    if target_x is None or target_y is None:
        return min(
            free_candidates,
            key=lambda cell: (
                abs(_target_heading(ant.x, ant.y, cell[0], cell[1]) - target_heading),
                cell[1],
                cell[0],
            ),
        ) + (target_heading,)
    return min(
        free_candidates,
        key=lambda cell: (
            _distance(cell[0], cell[1], target_x, target_y),
            abs(_target_heading(ant.x, ant.y, cell[0], cell[1]) - target_heading),
            cell[1],
            cell[0],
        ),
    ) + (target_heading,)


def _pickup_food(world: AntSandboxWorld, ant: SandboxAnt, config: AntSandboxConfig, tick: int) -> bool:
    if ant.carrying_food:
        return False
    for patch in world.food_patches:
        if patch.amount <= 0:
            continue
        if _distance(ant.x, ant.y, patch.x, patch.y) <= max(patch.radius, config.ants.food_pickup_radius):
            patch.amount -= 1
            ant.carrying_food = True
            world.emit(
                Event(
                    tick=tick,
                    event_type="food_pickup",
                    organism_id=ant.ant_id,
                    habitat_id=patch.patch_id,
                    payload={"x": ant.x, "y": ant.y, "remaining_amount": patch.amount},
                )
            )
            return True
    return False


def _unload_food(world: AntSandboxWorld, ant: SandboxAnt, config: AntSandboxConfig, tick: int) -> bool:
    if not ant.carrying_food:
        return False
    if _distance(ant.x, ant.y, world.nest.x, world.nest.y) > max(world.nest.radius, config.ants.nest_drop_radius):
        return False
    ant.carrying_food = False
    ant.delivered_food += 1
    world.nest.stored_food += 1
    world.emit(
        Event(
            tick=tick,
            event_type="food_unload",
            organism_id=ant.ant_id,
            habitat_id="nest",
            payload={"x": ant.x, "y": ant.y, "nest_food": world.nest.stored_food},
        )
    )
    return True


def step_world(world: AntSandboxWorld, config: AntSandboxConfig, tick: int) -> dict[str, int]:
    world.tick = tick
    moves = 0
    pickups = 0
    unloads = 0
    world.occupied_cells = {(ant.x, ant.y) for ant in world.ants if ant.alive}
    for ant in world.ants:
        if not ant.alive:
            continue
        world.occupied_cells.discard((ant.x, ant.y))
        next_x, next_y, next_heading = _choose_step(world, ant, config, tick)
        if (next_x, next_y) != (ant.x, ant.y):
            world.emit(
                Event(
                    tick=tick,
                    event_type="move",
                    organism_id=ant.ant_id,
                    habitat_id=None,
                    payload={
                        "from_x": ant.x,
                        "from_y": ant.y,
                        "to_x": next_x,
                        "to_y": next_y,
                        "carrying_food": ant.carrying_food,
                    },
                )
            )
            ant.x = next_x
            ant.y = next_y
            moves += 1
        ant.heading = next_heading
        ant.age += 1
        if _pickup_food(world, ant, config, tick):
            pickups += 1
        if _unload_food(world, ant, config, tick):
            unloads += 1
        world.occupied_cells.add((ant.x, ant.y))
    summary = {
        "ticks": world.tick,
        "alive": world.alive_count(),
        "carrying": world.carrying_count(),
        "nest_food": world.delivered_food_total(),
        "food_remaining": world.food_remaining(),
        "events": len(world.events),
        "moves": moves,
        "pickups": pickups,
        "unloads": unloads,
    }
    world.emit(
        Event(
            tick=tick,
            event_type="tick_summary",
            organism_id=None,
            habitat_id=None,
            payload=summary,
        )
    )
    return summary


def run_simulation(config: AntSandboxConfig) -> AntSandboxResult:
    world = initialize_world(config)
    for tick in range(1, config.ticks + 1):
        step_world(world, config, tick)
    return AntSandboxResult(world=world)
