from __future__ import annotations

from dataclasses import dataclass
import heapq
from math import atan2, cos, dist, sin, tau

from ..events import Event
from ..rng import make_rng
from .config import AntSandboxConfig
from .world import AntSandboxWorld, Colony, FoodPatch, Nest, SandboxAnt, initialize_world, terrain_effect, terrain_kind


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


def _terrain_move_cost(world: AntSandboxWorld, x: int, y: int) -> float:
    return float(terrain_effect(world, x, y)["move_cost"])


def _terrain_trail_factor(world: AntSandboxWorld, x: int, y: int) -> float:
    return float(terrain_effect(world, x, y)["trail_factor"])


def _terrain_sense_factor(world: AntSandboxWorld, x: int, y: int) -> float:
    return float(terrain_effect(world, x, y)["sense_factor"])


def _terrain_blocked(world: AntSandboxWorld, x: int, y: int) -> bool:
    return bool(terrain_effect(world, x, y)["blocked"])


def _nearest_open_cell(world: AntSandboxWorld, x: int, y: int) -> tuple[int, int]:
    if not _terrain_blocked(world, x, y):
        return x, y
    for radius in range(1, max(world.width, world.height)):
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if abs(dx) != radius and abs(dy) != radius:
                    continue
                nx = _clamp(x + dx, 0, world.width - 1)
                ny = _clamp(y + dy, 0, world.height - 1)
                if not _terrain_blocked(world, nx, ny):
                    return nx, ny
    return x, y


def _neighbor_cells(world: AntSandboxWorld, cell: tuple[int, int]) -> list[tuple[int, int]]:
    x, y = cell
    neighbors: list[tuple[int, int]] = []
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx = _clamp(x + dx, 0, world.width - 1)
            ny = _clamp(y + dy, 0, world.height - 1)
            if _terrain_blocked(world, nx, ny):
                continue
            neighbors.append((nx, ny))
    return neighbors


def _distance_field(world: AntSandboxWorld, key: str, goal: tuple[int, int]) -> dict[tuple[int, int], float]:
    cached = world.navigation_cache.get(key)
    if cached is not None:
        return cached
    distances: dict[tuple[int, int], float] = {goal: 0.0}
    heap: list[tuple[float, tuple[int, int]]] = [(0.0, goal)]
    while heap:
        current_cost, cell = heapq.heappop(heap)
        if current_cost > distances.get(cell, float("inf")):
            continue
        for neighbor in _neighbor_cells(world, cell):
            step_cost = _terrain_move_cost(world, neighbor[0], neighbor[1])
            next_cost = current_cost + step_cost
            if next_cost < distances.get(neighbor, float("inf")):
                distances[neighbor] = next_cost
                heapq.heappush(heap, (next_cost, neighbor))
    world.navigation_cache[key] = distances
    return distances


def _home_colony(world: AntSandboxWorld, ant: SandboxAnt) -> Colony:
    return world.colonies[ant.colony_id]


def _home_nest(world: AntSandboxWorld, ant: SandboxAnt) -> Nest:
    return _home_colony(world, ant).nest


def _food_trail_field(world: AntSandboxWorld, colony_id: str) -> dict[tuple[int, int], float]:
    return world.food_trail[colony_id]


def _home_trail_field(world: AntSandboxWorld, colony_id: str) -> dict[tuple[int, int], float]:
    return world.home_trail[colony_id]


def _patch_by_id(world: AntSandboxWorld, patch_id: str | None) -> FoodPatch | None:
    if patch_id is None:
        return None
    for patch in world.food_patches:
        if patch.patch_id == patch_id:
            return patch
    return None


def _nearest_food_patch(world: AntSandboxWorld, x: int, y: int) -> FoodPatch | None:
    active = [patch for patch in world.food_patches if patch.amount > 0]
    if not active:
        return None
    return min(active, key=lambda patch: (_distance(x, y, patch.x, patch.y), patch.patch_id))


def _food_within_range(
    world: AntSandboxWorld,
    ant: SandboxAnt,
    patches: list[FoodPatch],
    radius: int,
) -> FoodPatch | None:
    effective_radius = max(
        4,
        int(round(radius * (0.8 + ant.harvest_drive * 0.65) * _terrain_sense_factor(world, ant.x, ant.y))),
    )
    visible = [
        patch
        for patch in patches
        if patch.amount > 0 and _distance(ant.x, ant.y, patch.x, patch.y) <= effective_radius
    ]
    if not visible:
        return None
    return min(
        visible,
        key=lambda patch: (
            _food_patch_selection_cost(world, ant, patch),
            _distance(ant.x, ant.y, patch.x, patch.y),
            patch.patch_id,
        ),
    )


def _food_patch_selection_cost(world: AntSandboxWorld, ant: SandboxAnt, patch: FoodPatch) -> float:
    distance = _distance(ant.x, ant.y, patch.x, patch.y)
    richness_ratio = 0.0 if patch.max_amount <= 0 else patch.amount / patch.max_amount
    value_bonus = (
        richness_ratio * (3.8 + ant.harvest_drive * 3.2)
        + patch.radius * 0.18
        + patch.value_score * (4.5 + ant.harvest_drive * 2.2)
    )
    pressure_penalty = patch.competition_pressure * (0.18 + ant.harvest_drive * 0.08)
    crowd_penalty = patch.nearby_ants * (0.34 - ant.trail_affinity * 0.08)
    return distance + pressure_penalty + crowd_penalty - value_bonus


def _local_density(world: AntSandboxWorld, ant: SandboxAnt, cell: tuple[int, int], radius: int = 2) -> int:
    density = 0
    for other in world.ants:
        if not other.alive or other.ant_id == ant.ant_id:
            continue
        if max(abs(other.x - cell[0]), abs(other.y - cell[1])) <= radius:
            density += 1
    return density


def _enemy_density(world: AntSandboxWorld, ant: SandboxAnt, cell: tuple[int, int], radius: int) -> int:
    density = 0
    for other in world.ants:
        if not other.alive or other.ant_id == ant.ant_id or other.colony_id == ant.colony_id:
            continue
        if max(abs(other.x - cell[0]), abs(other.y - cell[1])) <= radius:
            density += 1
    return density


def _foreign_trail_pressure(world: AntSandboxWorld, ant: SandboxAnt, cell: tuple[int, int]) -> float:
    pressure = 0.0
    for colony_id, field in world.food_trail.items():
        if colony_id == ant.colony_id:
            continue
        pressure += field.get(cell, 0.0)
    for colony_id, field in world.home_trail.items():
        if colony_id == ant.colony_id:
            continue
        pressure += field.get(cell, 0.0) * 0.7
    return pressure


def _blocked_neighbor_count(world: AntSandboxWorld, cell: tuple[int, int]) -> int:
    x, y = cell
    blocked = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx = _clamp(x + dx, 0, world.width - 1)
            ny = _clamp(y + dy, 0, world.height - 1)
            if _terrain_blocked(world, nx, ny):
                blocked += 1
    return blocked


def _remember_position(ant: SandboxAnt) -> None:
    ant.recent_positions.append((ant.x, ant.y))
    if len(ant.recent_positions) > 12:
        ant.recent_positions.pop(0)


def _revisit_penalty(ant: SandboxAnt, cell: tuple[int, int]) -> float:
    penalty = 0.0
    for index, recent in enumerate(reversed(ant.recent_positions[-8:]), start=1):
        if recent == cell:
            penalty += 1.4 / index
        elif max(abs(recent[0] - cell[0]), abs(recent[1] - cell[1])) <= 1:
            penalty += 0.35 / index
    return penalty


def _edge_stuck(world: AntSandboxWorld, ant: SandboxAnt) -> bool:
    if _wall_margin(world, (ant.x, ant.y)) > 2:
        return False
    recent = ant.recent_positions[-8:]
    if len(recent) < 6:
        return False
    return len(set(recent)) <= 4


def _obstacle_stuck(world: AntSandboxWorld, ant: SandboxAnt) -> bool:
    recent = ant.recent_positions[-8:]
    if len(recent) < 6:
        return False
    if len(set(recent)) > 5:
        return False
    return any(_blocked_neighbor_count(world, cell) >= 2 for cell in recent)


def _egress_spread_heading(ant: SandboxAnt, base_heading: float) -> float:
    # Spread outbound ants into a fan so they do not all re-form the same nest-side clump.
    spread = (ant.range_bias - 0.5) * 0.9 + (ant.trail_affinity - 0.5) * 0.55
    return (base_heading + spread) % tau


def _task_oriented_patch(world: AntSandboxWorld, ant: SandboxAnt) -> FoodPatch | None:
    patch = _patch_by_id(world, ant.target_patch_id)
    if patch is None or patch.amount <= 0:
        ant.target_patch_id = None
        return None
    return patch


def _should_switch_to_visible_food(
    world: AntSandboxWorld,
    ant: SandboxAnt,
    config: AntSandboxConfig,
    current_patch: FoodPatch | None,
    visible_patch: FoodPatch | None,
) -> bool:
    if current_patch is None or visible_patch is None:
        return False
    if current_patch.patch_id == visible_patch.patch_id:
        return False
    if ant.carrying_food:
        return False
    current_cost = _food_patch_selection_cost(world, ant, current_patch)
    visible_cost = _food_patch_selection_cost(world, ant, visible_patch)
    current_ratio = 0.0 if current_patch.max_amount <= 0 else current_patch.amount / current_patch.max_amount
    visible_ratio = 0.0 if visible_patch.max_amount <= 0 else visible_patch.amount / visible_patch.max_amount
    visible_edge_distance = max(0.0, _distance(ant.x, ant.y, visible_patch.x, visible_patch.y) - visible_patch.radius)

    # Keep task-stage stability, but do not let stale targets override obvious nearby food.
    switch_margin = 3.5 + ant.trail_affinity * 1.5
    if current_ratio < 0.35:
        switch_margin -= 1.0
    if visible_ratio > current_ratio + 0.25:
        switch_margin -= 0.8
    if visible_edge_distance <= max(3, visible_patch.radius + config.ants.food_pickup_radius + 1):
        switch_margin = min(switch_margin, 1.4)
    if _local_density(world, ant, (ant.x, ant.y), radius=3) >= 4:
        switch_margin -= 1.0
    if config.ants.hostility_radius > 0 and _enemy_density(world, ant, (ant.x, ant.y), config.ants.hostility_radius) > 0:
        switch_margin -= 1.0
    switch_margin = max(1.0, switch_margin)
    return visible_cost + switch_margin < current_cost


def _patch_respawn_cell(
    world: AntSandboxWorld,
    patch: FoodPatch,
    config: AntSandboxConfig,
    tick: int,
) -> tuple[int, int]:
    rng = make_rng(config.seed, f"ant-sandbox:{tick}:{patch.patch_id}:respawn:{patch.respawn_count}")
    wall_margin = max(5, patch.radius + 2)
    spacing = patch.radius + 10
    candidates: list[tuple[int, int]] = []
    for y in range(wall_margin, world.height - wall_margin):
        for x in range(wall_margin, world.width - wall_margin):
            if any(_distance(x, y, colony.nest.x, colony.nest.y) < colony.nest.radius + patch.radius + 10 for colony in world.colonies.values()):
                continue
            if _terrain_blocked(world, x, y):
                continue
            if any(
                other.patch_id != patch.patch_id and _distance(x, y, other.x, other.y) < other.radius + spacing
                for other in world.food_patches
            ):
                continue
            candidates.append((x, y))
    if not candidates:
        return patch.x, patch.y
    return candidates[rng.randrange(len(candidates))]


def _dampen_food_trails(world: AntSandboxWorld, center_x: int, center_y: int, radius: int) -> None:
    cutoff = radius + 8
    world.food_trail = {
        colony_id: {
            cell: value * (0.15 if _distance(cell[0], cell[1], center_x, center_y) <= cutoff else 1.0)
            for cell, value in field.items()
            if value > 0.02
        }
        for colony_id, field in world.food_trail.items()
    }
    world.home_trail = {
        colony_id: {
            cell: value * (0.35 if _distance(cell[0], cell[1], center_x, center_y) <= cutoff else 1.0)
            for cell, value in field.items()
            if value > 0.02
        }
        for colony_id, field in world.home_trail.items()
    }


def _regrow_food(world: AntSandboxWorld, config: AntSandboxConfig, tick: int) -> int:
    reseeds = 0
    for patch in world.food_patches:
        if patch.amount <= 0:
            patch.empty_ticks += 1
            if patch.relocate_on_depletion and patch.empty_ticks >= patch.respawn_delay_ticks:
                old_x = patch.x
                old_y = patch.y
                patch.x, patch.y = _patch_respawn_cell(world, patch, config, tick)
                patch.amount = patch.max_amount
                patch.empty_ticks = 0
                patch.respawn_count += 1
                patch.nearby_ants = 0
                patch.carrying_nearby = 0
                patch.recent_pickups = 0
                patch.competition_pressure = 0.0
                _dampen_food_trails(world, old_x, old_y, patch.radius)
                world.emit(
                    Event(
                        tick=tick,
                        event_type="food_patch_reseed",
                        organism_id=None,
                        habitat_id=patch.patch_id,
                        payload={
                            "from_x": old_x,
                            "from_y": old_y,
                            "to_x": patch.x,
                            "to_y": patch.y,
                            "amount": patch.amount,
                            "respawn_count": patch.respawn_count,
                        },
                    )
                )
                reseeds += 1
            elif not patch.relocate_on_depletion and patch.regrowth_rate > 0 and patch.empty_ticks >= patch.respawn_delay_ticks:
                before = patch.amount
                patch.amount = min(patch.max_amount, patch.amount + patch.regrowth_rate)
                if before == 0 and patch.amount > 0:
                    world.emit(
                        Event(
                            tick=tick,
                            event_type="food_patch_regrow",
                            organism_id=None,
                            habitat_id=patch.patch_id,
                            payload={"x": patch.x, "y": patch.y, "amount": patch.amount},
                        )
                    )
            continue
        patch.empty_ticks = 0
        if patch.regrowth_rate <= 0:
            continue
        if patch.regrow_only_when_empty:
            continue
        if patch.amount >= patch.max_amount:
            continue
        patch.amount = min(patch.max_amount, patch.amount + patch.regrowth_rate)
    return reseeds


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
            if _terrain_blocked(world, nx, ny):
                continue
            cells.append((nx, ny))
    return cells


def _wall_margin(world: AntSandboxWorld, cell: tuple[int, int]) -> int:
    x, y = cell
    return min(x, y, world.width - 1 - x, world.height - 1 - y)


def _best_pheromone_cell(
    ant: SandboxAnt,
    world: AntSandboxWorld,
    config: AntSandboxConfig,
    target: str,
) -> tuple[int, int] | None:
    if not config.ants.pheromone_enabled or config.ants.pheromone_sense_radius <= 0:
        return None
    field = _food_trail_field(world, ant.colony_id) if target == "food" else _home_trail_field(world, ant.colony_id)
    candidates = []
    task_boost = 0.35 if (ant.target_patch_id is not None or ant.outbound_commit_ticks > 0) else 0.0
    radius = max(2, int(round(config.ants.pheromone_sense_radius * (0.75 + ant.trail_affinity * 1.05 + task_boost))))
    for (x, y), strength in field.items():
        if strength <= 0:
            continue
        distance = _distance(ant.x, ant.y, x, y)
        if distance == 0 or distance > radius:
            continue
        desirability = (strength / distance) * (0.55 + ant.trail_affinity * 1.2) * _terrain_sense_factor(world, x, y)
        candidates.append(((x, y), desirability))
    if not candidates:
        return None
    return max(candidates, key=lambda item: (item[1], item[0][1], item[0][0]))[0]


def _task_trail_bonus(world: AntSandboxWorld, ant: SandboxAnt, cell: tuple[int, int], target_x: int | None, target_y: int | None) -> float:
    food_field = _food_trail_field(world, ant.colony_id)
    home_field = _home_trail_field(world, ant.colony_id)
    if ant.carrying_food:
        return home_field.get(cell, 0.0) * 0.55
    if target_x is not None and target_y is not None:
        return food_field.get(cell, 0.0) * 0.6
    return food_field.get(cell, 0.0) * 0.28 - home_field.get(cell, 0.0) * 0.16


def _hostility_penalty(
    world: AntSandboxWorld,
    ant: SandboxAnt,
    config: AntSandboxConfig,
    cell: tuple[int, int],
    exploration_phase: bool,
) -> float:
    if config.ants.hostility_radius <= 0:
        return 0.0
    enemy_density = _enemy_density(world, ant, cell, config.ants.hostility_radius)
    foreign_trail = _foreign_trail_pressure(world, ant, cell)
    phase_weight = 1.0 if exploration_phase else 0.45
    return (
        enemy_density * config.ants.hostility_weight * phase_weight
        + foreign_trail * config.ants.foreign_trail_weight * phase_weight
    )


def _ant_by_id(world: AntSandboxWorld, ant_id: str | None) -> SandboxAnt | None:
    if ant_id is None:
        return None
    for ant in world.ants:
        if ant.ant_id == ant_id:
            return ant
    return None


def _combat_balance(world: AntSandboxWorld, ant: SandboxAnt, radius: int) -> tuple[int, int]:
    allies = 0
    enemies = 0
    for other in world.ants:
        if not other.alive or other.ant_id == ant.ant_id:
            continue
        if max(abs(other.x - ant.x), abs(other.y - ant.y)) > radius:
            continue
        if other.colony_id == ant.colony_id:
            allies += 1
        else:
            enemies += 1
    return allies, enemies


def _engage_score(world: AntSandboxWorld, ant: SandboxAnt, enemy: SandboxAnt, config: AntSandboxConfig) -> float:
    if not config.ants.combat_enabled:
        return -1.0
    if not ant.alive or ant.combat_ticks_remaining > 0 or ant.combat_cooldown_ticks > 0:
        return -1.0
    score = 0.0
    home_nest = _home_nest(world, ant)
    if _distance(ant.x, ant.y, home_nest.x, home_nest.y) <= home_nest.radius + 10:
        score += 0.9
    if ant.carrying_food:
        score -= 1.15
    if ant.energy <= config.ants.hunger_return_threshold + 1.5:
        score -= 0.75
    if enemy.carrying_food:
        score += 0.35
    allies, enemies = _combat_balance(world, ant, config.ants.combat_radius + 1)
    score += max(-0.8, min(0.9, (allies - enemies) * 0.45))
    if ant.target_patch_id is not None and ant.target_patch_id == enemy.target_patch_id:
        score += 0.25
    for patch in world.food_patches:
        if patch.amount <= 0:
            continue
        if _distance(ant.x, ant.y, patch.x, patch.y) <= patch.radius + 5:
            score += 0.45 + patch.value_score * 0.22
            break
    score += ant.harvest_drive * 0.35 + ant.trail_affinity * 0.15
    score += min(0.45, _foreign_trail_pressure(world, ant, (ant.x, ant.y)) * 0.08)
    return score


def _start_combats(world: AntSandboxWorld, config: AntSandboxConfig, tick: int) -> int:
    if not config.ants.combat_enabled or config.ants.combat_duration <= 0 or config.ants.combat_radius <= 0:
        return 0
    candidates: list[tuple[float, str, str]] = []
    ants = [ant for ant in world.ants if ant.alive and ant.combat_ticks_remaining <= 0 and ant.combat_cooldown_ticks <= 0]
    for index, ant in enumerate(ants):
        for enemy in ants[index + 1:]:
            if enemy.colony_id == ant.colony_id:
                continue
            if max(abs(enemy.x - ant.x), abs(enemy.y - ant.y)) > config.ants.combat_radius:
                continue
            ant_score = _engage_score(world, ant, enemy, config)
            enemy_score = _engage_score(world, enemy, ant, config)
            if (
                ant_score >= config.ants.combat_decision_threshold
                and enemy_score >= config.ants.combat_decision_threshold
            ):
                candidates.append((ant_score + enemy_score, ant.ant_id, enemy.ant_id))
    engaged: set[str] = set()
    started = 0
    for _, ant_id, enemy_id in sorted(candidates, reverse=True):
        if ant_id in engaged or enemy_id in engaged:
            continue
        ant = _ant_by_id(world, ant_id)
        enemy = _ant_by_id(world, enemy_id)
        if ant is None or enemy is None or not ant.alive or not enemy.alive:
            continue
        ant.combat_with_id = enemy.ant_id
        enemy.combat_with_id = ant.ant_id
        ant.combat_ticks_remaining = config.ants.combat_duration
        enemy.combat_ticks_remaining = config.ants.combat_duration
        ant.target_patch_id = None
        enemy.target_patch_id = None
        ant.outbound_commit_ticks = 0
        enemy.outbound_commit_ticks = 0
        engaged.add(ant.ant_id)
        engaged.add(enemy.ant_id)
        started += 1
        world.emit(
            Event(
                tick=tick,
                event_type="combat_start",
                organism_id=None,
                habitat_id="world",
                payload={
                    "ant_a": ant.ant_id,
                    "ant_b": enemy.ant_id,
                    "colony_a": ant.colony_id,
                    "colony_b": enemy.colony_id,
                    "x": round((ant.x + enemy.x) / 2, 2),
                    "y": round((ant.y + enemy.y) / 2, 2),
                    "duration": config.ants.combat_duration,
                },
            )
        )
    return started


def _current_combat_pairs(world: AntSandboxWorld) -> int:
    seen: set[tuple[str, str]] = set()
    for ant in world.ants:
        if not ant.alive or ant.combat_ticks_remaining <= 0 or ant.combat_with_id is None:
            continue
        pair = tuple(sorted((ant.ant_id, ant.combat_with_id)))
        seen.add(pair)
    return len(seen)


def _advance_combat_state(world: AntSandboxWorld, config: AntSandboxConfig, tick: int) -> int:
    active_pairs = 0
    handled: set[str] = set()
    for ant in world.ants:
        if not ant.alive or ant.ant_id in handled:
            continue
        if ant.combat_ticks_remaining <= 0 or ant.combat_with_id is None:
            if ant.combat_cooldown_ticks > 0:
                ant.combat_cooldown_ticks -= 1
            continue
        enemy = _ant_by_id(world, ant.combat_with_id)
        if enemy is None or not enemy.alive:
            ant.combat_with_id = None
            ant.combat_ticks_remaining = 0
            if ant.combat_cooldown_ticks > 0:
                ant.combat_cooldown_ticks -= 1
            continue
        handled.add(ant.ant_id)
        handled.add(enemy.ant_id)
        active_pairs += 1
        ant.combat_ticks_remaining = max(0, ant.combat_ticks_remaining - 1)
        enemy.combat_ticks_remaining = max(0, enemy.combat_ticks_remaining - 1)
        if ant.combat_ticks_remaining == 0 or enemy.combat_ticks_remaining == 0:
            ant.combat_with_id = None
            enemy.combat_with_id = None
            ant.combat_ticks_remaining = 0
            enemy.combat_ticks_remaining = 0
            ant.combat_cooldown_ticks = max(ant.combat_cooldown_ticks, config.ants.combat_cooldown)
            enemy.combat_cooldown_ticks = max(enemy.combat_cooldown_ticks, config.ants.combat_cooldown)
            world.emit(
                Event(
                    tick=tick,
                    event_type="combat_end",
                    organism_id=None,
                    habitat_id="world",
                    payload={
                        "ant_a": ant.ant_id,
                        "ant_b": enemy.ant_id,
                        "colony_a": ant.colony_id,
                        "colony_b": enemy.colony_id,
                        "x": round((ant.x + enemy.x) / 2, 2),
                        "y": round((ant.y + enemy.y) / 2, 2),
                    },
                )
            )
    for ant in world.ants:
        if not ant.alive or ant.ant_id in handled:
            continue
        if ant.combat_ticks_remaining <= 0 and ant.combat_cooldown_ticks > 0:
            ant.combat_cooldown_ticks -= 1
    return active_pairs


def _decay_stale_field(world: AntSandboxWorld) -> None:
    world.stale_field = {
        cell: value * 0.92
        for cell, value in world.stale_field.items()
        if value * 0.92 > 0.02
    }


def _choose_step(
    world: AntSandboxWorld,
    ant: SandboxAnt,
    config: AntSandboxConfig,
    tick: int,
) -> tuple[int, int, float]:
    rng = make_rng(config.seed, f"ant-sandbox:{tick}:{ant.ant_id}:move")
    home_nest = _home_nest(world, ant)
    target_x: int | None = None
    target_y: int | None = None
    target_key: str | None = None
    hungry = ant.energy <= config.ants.hunger_return_threshold
    distance_from_nest = _distance(ant.x, ant.y, home_nest.x, home_nest.y)
    launch_exploration = ant.outbound_commit_ticks > 6 and distance_from_nest <= home_nest.radius + 7
    task_patch = _task_oriented_patch(world, ant)

    if ant.carrying_food or (hungry and home_nest.stored_food > 0):
        target_x = home_nest.x
        target_y = home_nest.y
        target_key = f"nest:{ant.colony_id}:{home_nest.x}:{home_nest.y}"
    else:
        patch = None if launch_exploration else task_patch
        if patch is not None:
            visible_patch = _food_within_range(world, ant, world.food_patches, config.ants.food_sense_radius)
            if _should_switch_to_visible_food(world, ant, config, patch, visible_patch):
                patch = visible_patch
        if patch is None:
            patch = _food_within_range(world, ant, world.food_patches, config.ants.food_sense_radius)
        if patch is not None:
            target_x = patch.x
            target_y = patch.y
            target_key = f"patch:{patch.patch_id}:{patch.x}:{patch.y}"
            ant.target_patch_id = patch.patch_id
        elif ant.outbound_commit_ticks <= 6 or distance_from_nest > home_nest.radius + 5:
            pheromone_target = _best_pheromone_cell(
                ant,
                world,
                config,
                target="food",
            )
            if pheromone_target is not None:
                target_x, target_y = pheromone_target
                nearest_patch = _nearest_food_patch(world, target_x, target_y)
                if nearest_patch is not None:
                    ant.target_patch_id = nearest_patch.patch_id
                    target_key = f"pheromone:{ant.colony_id}:food:{target_x}:{target_y}"
    if target_x is not None and target_y is not None:
        target_heading = _target_heading(ant.x, ant.y, target_x, target_y)
    else:
        target_heading = None
        desired_distance = home_nest.radius + 6 + int(
            round(ant.range_bias * max(18, min(world.width, world.height) * 0.45))
        )
        if ant.carrying_food or (hungry and home_nest.stored_food > 0):
            base_heading = _target_heading(ant.x, ant.y, home_nest.x, home_nest.y)
        else:
            outward_heading = _target_heading(home_nest.x, home_nest.y, ant.x, ant.y)
            if hungry and home_nest.stored_food <= 0:
                base_heading = ant.heading
            elif launch_exploration:
                base_heading = _egress_spread_heading(ant, outward_heading)
            elif distance_from_nest < desired_distance - 2:
                base_heading = outward_heading
            elif distance_from_nest > desired_distance + 4:
                base_heading = _target_heading(ant.x, ant.y, home_nest.x, home_nest.y)
            else:
                base_heading = ant.heading
        if ant.x <= 1 or ant.x >= world.width - 2 or ant.y <= 1 or ant.y >= world.height - 2:
            center_x = world.width // 2
            center_y = world.height // 2
            base_heading = _target_heading(ant.x, ant.y, center_x, center_y)
        jitter_scale = config.ants.wander_turn_jitter * (0.65 if ant.carrying_food else 0.75 + ant.range_bias * 0.45)
        if target_heading is not None:
            base_heading = (base_heading * 0.35 + target_heading * 0.65)
            jitter_scale *= 0.6
        jitter = rng.uniform(-jitter_scale, jitter_scale)
        target_heading = (base_heading + jitter) % tau
    candidates = _candidate_cells(world, ant, config)
    free_candidates = [
        cell for cell in candidates if cell not in world.occupied_cells or cell == (ant.x, ant.y)
    ]
    if not free_candidates:
        return ant.x, ant.y, target_heading
    near_wall = _wall_margin(world, (ant.x, ant.y)) <= 2
    edge_stuck = _edge_stuck(world, ant)
    obstacle_stuck = _obstacle_stuck(world, ant)
    current_stale = world.stale_field.get((ant.x, ant.y), 0.0)
    near_nest = _distance(ant.x, ant.y, home_nest.x, home_nest.y) <= home_nest.radius + 8
    exploration_phase = (not ant.carrying_food) and (not hungry) and (target_x is None or launch_exploration)
    force_egress = launch_exploration and not ant.carrying_food and not hungry
    home_field = _home_trail_field(world, ant.colony_id)
    path_field = _distance_field(world, target_key, (target_x, target_y)) if target_key is not None and target_x is not None and target_y is not None else None
    if target_x is None or target_y is None:
        return min(
            free_candidates,
            key=lambda cell: (
                (_local_density(world, ant, cell, radius=2) * 1.45 + _revisit_penalty(ant, cell) + home_field.get(cell, 0.0) * 0.18) if exploration_phase else (_local_density(world, ant, cell, radius=2) if near_nest else 0),
                _hostility_penalty(world, ant, config, cell, exploration_phase),
                -_wall_margin(world, cell) * 4 if edge_stuck else 0,
                _blocked_neighbor_count(world, cell) * 3 if obstacle_stuck else 0,
                -_distance(cell[0], cell[1], home_nest.x, home_nest.y) if force_egress else 0,
                -_task_trail_bonus(world, ant, cell, target_x, target_y),
                _terrain_move_cost(world, cell[0], cell[1]),
                -_wall_margin(world, cell) if near_wall else 0,
                world.stale_field.get(cell, 0.0),
                abs(_target_heading(ant.x, ant.y, cell[0], cell[1]) - target_heading),
                _distance(cell[0], cell[1], home_nest.x, home_nest.y) if near_wall else 0,
                cell[1],
                cell[0],
            ),
        ) + (target_heading,)
    return min(
        free_candidates,
        key=lambda cell: (
            (_local_density(world, ant, cell, radius=2) * 0.8 + _revisit_penalty(ant, cell) * 0.2) if launch_exploration else (_local_density(world, ant, cell, radius=2) if near_nest else 0),
            _hostility_penalty(world, ant, config, cell, exploration_phase),
            -_wall_margin(world, cell) * 4 if edge_stuck else 0,
            _blocked_neighbor_count(world, cell) * 3 if obstacle_stuck else 0,
            -_distance(cell[0], cell[1], home_nest.x, home_nest.y) if force_egress else 0,
            path_field.get(cell, float("inf")) if path_field is not None else float("inf"),
            _distance(cell[0], cell[1], target_x, target_y),
            -_task_trail_bonus(world, ant, cell, target_x, target_y),
            _terrain_move_cost(world, cell[0], cell[1]),
            abs(_target_heading(ant.x, ant.y, cell[0], cell[1]) - target_heading),
            world.stale_field.get(cell, 0.0) - current_stale * 0.4,
            -_wall_margin(world, cell) if near_wall else 0,
            cell[1],
            cell[0],
        ),
    ) + (target_heading,)


def _pickup_food(world: AntSandboxWorld, ant: SandboxAnt, config: AntSandboxConfig, tick: int) -> str | None:
    if ant.carrying_food:
        return None
    for patch in world.food_patches:
        if patch.amount <= 0:
            continue
        if _distance(ant.x, ant.y, patch.x, patch.y) <= max(patch.radius, config.ants.food_pickup_radius):
            patch.amount -= 1
            ant.carrying_food = True
            ant.target_patch_id = patch.patch_id
            ant.outbound_commit_ticks = 0
            patch.recent_pickups += 1
            world.emit(
                Event(
                    tick=tick,
                    event_type="food_pickup",
                    organism_id=ant.ant_id,
                    habitat_id=patch.patch_id,
                    payload={"x": ant.x, "y": ant.y, "remaining_amount": patch.amount},
                )
            )
            if patch.amount == 0:
                patch.depletion_count += 1
                world.emit(
                    Event(
                        tick=tick,
                        event_type="food_source_depleted",
                        organism_id=ant.ant_id,
                        habitat_id=patch.patch_id,
                        payload={"x": patch.x, "y": patch.y, "depletion_count": patch.depletion_count},
                    )
                )
            return patch.patch_id
    return None


def _unload_food(world: AntSandboxWorld, ant: SandboxAnt, config: AntSandboxConfig, tick: int) -> bool:
    home_colony = _home_colony(world, ant)
    home_nest = home_colony.nest
    if not ant.carrying_food:
        return False
    if _distance(ant.x, ant.y, home_nest.x, home_nest.y) > max(home_nest.radius, config.ants.nest_drop_radius):
        return False
    ant.carrying_food = False
    ant.delivered_food += 1
    ant.outbound_commit_ticks = 14
    home_nest.stored_food += 1
    world.emit(
        Event(
            tick=tick,
            event_type="food_unload",
            organism_id=ant.ant_id,
            habitat_id=home_colony.colony_id,
            payload={"x": ant.x, "y": ant.y, "nest_food": home_nest.stored_food, "colony_id": home_colony.colony_id},
        )
    )
    return True


def _feed_at_nest(world: AntSandboxWorld, ant: SandboxAnt, config: AntSandboxConfig, tick: int) -> bool:
    home_colony = _home_colony(world, ant)
    home_nest = home_colony.nest
    if _distance(ant.x, ant.y, home_nest.x, home_nest.y) > max(home_nest.radius, config.ants.nest_drop_radius):
        return False
    if ant.energy >= config.ants.max_energy:
        return False
    if home_nest.stored_food <= 0:
        return False
    home_nest.stored_food -= 1
    ant.energy = min(config.ants.max_energy, ant.energy + config.ants.nest_feed_amount)
    world.emit(
        Event(
            tick=tick,
            event_type="nest_feed",
            organism_id=ant.ant_id,
            habitat_id=home_colony.colony_id,
            payload={"x": ant.x, "y": ant.y, "energy": round(ant.energy, 3), "nest_food": home_nest.stored_food, "colony_id": home_colony.colony_id},
        )
    )
    return True


def _apply_colony_upkeep(world: AntSandboxWorld, config: AntSandboxConfig, tick: int) -> int:
    consumed_total = 0
    for colony in world.colonies.values():
        if colony.nest.upkeep_reserve is None:
            colony.nest.upkeep_reserve = 0.0
        upkeep_rate = config.nest.colony_upkeep_per_ant_tick
        if upkeep_rate <= 0:
            continue
        colony.nest.upkeep_reserve += world.alive_count_for_colony(colony.colony_id) * upkeep_rate
        consumed = min(int(colony.nest.upkeep_reserve), colony.nest.stored_food)
        if consumed <= 0:
            colony.nest.upkeep_reserve = min(colony.nest.upkeep_reserve, 0.999)
            continue
        colony.nest.stored_food -= consumed
        colony.nest.upkeep_reserve -= consumed
        colony.nest.upkeep_reserve = min(colony.nest.upkeep_reserve, 0.999)
        consumed_total += consumed
        world.emit(
            Event(
                tick=tick,
                event_type="nest_upkeep",
                organism_id=None,
                habitat_id=colony.colony_id,
                payload={"consumed": consumed, "nest_food": colony.nest.stored_food, "colony_id": colony.colony_id},
            )
        )
    return consumed_total


def _apply_disturbance(world: AntSandboxWorld, config: AntSandboxConfig, tick: int) -> None:
    if config.disturbance_tick <= 0 or tick != config.disturbance_tick:
        return
    if config.disturbance_food_shift:
        for patch in world.food_patches:
            shifted_x = _clamp(patch.x + config.disturbance_food_shift_dx, 0, world.width - 1)
            shifted_y = _clamp(patch.y + config.disturbance_food_shift_dy, 0, world.height - 1)
            patch.x, patch.y = _nearest_open_cell(world, shifted_x, shifted_y)
        world.emit(
            Event(
                tick=tick,
                event_type="food_shift",
                organism_id=None,
                habitat_id=None,
                payload={
                    "dx": config.disturbance_food_shift_dx,
                    "dy": config.disturbance_food_shift_dy,
                },
            )
        )
    if config.disturbance_kill_radius > 0:
        killed = 0
        for ant in world.ants:
            if not ant.alive:
                continue
            if any(
                _distance(ant.x, ant.y, colony.nest.x, colony.nest.y) <= config.disturbance_kill_radius
                for colony in world.colonies.values()
            ):
                ant.alive = False
                world.emit(
                    Event(
                        tick=tick,
                        event_type="ant_death",
                        organism_id=ant.ant_id,
                        habitat_id="world",
                        payload={"x": ant.x, "y": ant.y, "age": ant.age, "reason": "disturbance"},
                    )
                )
                killed += 1
        world.emit(
            Event(
                tick=tick,
                event_type="disturbance",
                organism_id=None,
                habitat_id=None,
                payload={"killed": killed, "kill_radius": config.disturbance_kill_radius},
            )
        )


def _decay_trails(world: AntSandboxWorld, config: AntSandboxConfig) -> None:
    decay = max(0.0, 1.0 - config.ants.trail_decay)
    world.food_trail = {
        colony_id: {cell: value * decay for cell, value in field.items() if value * decay > 0.02}
        for colony_id, field in world.food_trail.items()
    }
    world.home_trail = {
        colony_id: {cell: value * decay for cell, value in field.items() if value * decay > 0.02}
        for colony_id, field in world.home_trail.items()
    }


def _deposit_trail(world: AntSandboxWorld, ant: SandboxAnt, config: AntSandboxConfig, tick: int) -> None:
    if not config.ants.pheromone_enabled:
        return
    key = (ant.x, ant.y)
    food_field = _food_trail_field(world, ant.colony_id)
    home_field = _home_trail_field(world, ant.colony_id)
    if ant.carrying_food:
        food_field[key] = food_field.get(key, 0.0) + config.ants.trail_deposit * _terrain_trail_factor(world, ant.x, ant.y)
        world.emit(
            Event(
                tick=tick,
                event_type="trail_deposit",
                organism_id=ant.ant_id,
                habitat_id=ant.colony_id,
                payload={"trail_kind": "food", "x": ant.x, "y": ant.y, "strength": round(food_field[key], 4), "colony_id": ant.colony_id},
            )
        )
    else:
        home_field[key] = home_field.get(key, 0.0) + config.ants.home_trail_deposit * _terrain_trail_factor(world, ant.x, ant.y)
        world.emit(
            Event(
                tick=tick,
                event_type="trail_deposit",
                organism_id=ant.ant_id,
                habitat_id=ant.colony_id,
                payload={"trail_kind": "home", "x": ant.x, "y": ant.y, "strength": round(home_field[key], 4), "colony_id": ant.colony_id},
            )
        )


def _update_stale_signal(world: AntSandboxWorld, ant: SandboxAnt) -> None:
    key = (ant.x, ant.y)
    wall_penalty = 0.45 if _wall_margin(world, key) <= 1 else 0.0
    carrying_relief = -0.35 if ant.carrying_food else 0.0
    world.stale_field[key] = max(
        0.0,
        world.stale_field.get(key, 0.0) + 0.18 + wall_penalty + carrying_relief,
    )


def _update_food_source_competition(world: AntSandboxWorld, tick: int) -> int:
    contested_sources = 0
    for patch in world.food_patches:
        nearby_colonies = {
            ant.colony_id
            for ant in world.ants
            if ant.alive and _distance(ant.x, ant.y, patch.x, patch.y) <= patch.radius + 6
        }
        nearby_ants = sum(
            1
            for ant in world.ants
            if ant.alive and _distance(ant.x, ant.y, patch.x, patch.y) <= patch.radius + 4
        )
        carrying_nearby = sum(
            1
            for ant in world.ants
            if ant.alive and ant.carrying_food and _distance(ant.x, ant.y, patch.x, patch.y) <= patch.radius + 6
        )
        patch.nearby_ants = nearby_ants
        patch.carrying_nearby = carrying_nearby
        depletion_ratio = 0.0 if patch.max_amount <= 0 else 1.0 - (patch.amount / patch.max_amount)
        patch.competition_pressure = round(
            patch.competition_pressure * 0.78
            + nearby_ants * 0.65
            + carrying_nearby * 0.45
            + patch.recent_pickups * 1.6
            + depletion_ratio * 1.2,
            4,
        )
        is_contested = (
            len(nearby_colonies) >= 2
            or nearby_ants >= 4
            or patch.recent_pickups >= 2
            or (depletion_ratio >= 0.4 and nearby_ants >= 2)
        )
        if is_contested:
            patch.contested_ticks += 1
            contested_sources += 1
            world.emit(
                Event(
                    tick=tick,
                    event_type="food_source_contested",
                    organism_id=None,
                    habitat_id=patch.patch_id,
                    payload={
                        "x": patch.x,
                        "y": patch.y,
                        "nearby_ants": nearby_ants,
                        "nearby_colonies": len(nearby_colonies),
                        "carrying_nearby": carrying_nearby,
                        "recent_pickups": patch.recent_pickups,
                        "remaining_amount": patch.amount,
                        "competition_pressure": patch.competition_pressure,
                    },
                )
            )
        patch.recent_pickups = 0
    return contested_sources


def _count_hostility_contacts(world: AntSandboxWorld, config: AntSandboxConfig) -> int:
    if config.ants.hostility_radius <= 0:
        return 0
    contacts = 0
    for ant in world.ants:
        if not ant.alive:
            continue
        if _enemy_density(world, ant, (ant.x, ant.y), config.ants.hostility_radius) > 0:
            contacts += 1
    return contacts


def _spawn_ant(world: AntSandboxWorld, config: AntSandboxConfig, tick: int) -> bool:
    if not config.ants.allow_spawning:
        return False
    if tick % config.ants.spawn_interval != 0:
        return False
    if world.alive_count() >= config.ants.max_population * max(1, len(world.colonies)):
        return False
    for colony in world.colonies.values():
        if colony.nest.stored_food < config.ants.spawn_food_cost:
            continue
        spawn_cells = [
            (colony.nest.x, colony.nest.y),
            (colony.nest.x + 1, colony.nest.y),
            (colony.nest.x - 1, colony.nest.y),
            (colony.nest.x, colony.nest.y + 1),
            (colony.nest.x, colony.nest.y - 1),
        ]
        for x, y in spawn_cells:
            if (x, y) in world.occupied_cells:
                continue
            ant_id = world.allocate_ant_id()
            trait_rng = make_rng(config.seed, f"ant-sandbox:{colony.colony_id}:birth-traits:{tick}:{ant_id}")
            parentless_center = (len(world.ants) % 9) / 8 if world.ants else 0.5
            ant = SandboxAnt(
                ant_id=ant_id,
                colony_id=colony.colony_id,
                x=max(0, min(world.width - 1, x)),
                y=max(0, min(world.height - 1, y)),
                heading=0.0,
                energy=config.ants.initial_energy,
                range_bias=max(0.0, min(1.0, 0.2 + 0.6 * parentless_center + trait_rng.uniform(-0.18, 0.18))),
                trail_affinity=max(0.0, min(1.0, 0.2 + 0.6 * ((len(world.ants) * 3) % 9) / 8 + trait_rng.uniform(-0.18, 0.18))),
                harvest_drive=max(0.0, min(1.0, 0.2 + 0.6 * ((len(world.ants) * 5) % 9) / 8 + trait_rng.uniform(-0.18, 0.18))),
                lineage_id=f"{colony.colony_id}:{ant_id}",
            )
            world.ants.append(ant)
            colony.nest.stored_food -= config.ants.spawn_food_cost
            world.occupied_cells.add((ant.x, ant.y))
            world.emit(
                Event(
                    tick=tick,
                    event_type="ant_birth",
                    organism_id=ant.ant_id,
                    habitat_id=colony.colony_id,
                    payload={"x": ant.x, "y": ant.y, "nest_food": colony.nest.stored_food, "colony_id": colony.colony_id},
                )
            )
            return True
    return False


def step_world(world: AntSandboxWorld, config: AntSandboxConfig, tick: int) -> dict[str, int]:
    world.tick = tick
    moves = 0
    pickups = 0
    unloads = 0
    deaths = 0
    births = 0
    feeds = 0
    upkeep = 0
    reseeds = 0
    contested_sources = 0
    hostility_contacts = 0
    combat_starts = 0
    _apply_disturbance(world, config, tick)
    _decay_trails(world, config)
    _decay_stale_field(world)
    upkeep += _apply_colony_upkeep(world, config, tick)
    reseeds += _regrow_food(world, config, tick)
    world.occupied_cells = {(ant.x, ant.y) for ant in world.ants if ant.alive}
    combat_starts += _start_combats(world, config, tick)
    for ant in world.ants:
        if not ant.alive:
            continue
        if ant.outbound_commit_ticks > 0:
            ant.outbound_commit_ticks -= 1
        ant.age += 1
        ant.energy = max(0.0, ant.energy - config.ants.metabolism_cost)
        if ant.age > config.ants.max_age:
            ant.alive = False
            world.occupied_cells.discard((ant.x, ant.y))
            world.emit(
                Event(
                    tick=tick,
                    event_type="ant_death",
                    organism_id=ant.ant_id,
                    habitat_id="world",
                    payload={"x": ant.x, "y": ant.y, "age": ant.age},
                )
            )
            deaths += 1
            continue
        if ant.combat_ticks_remaining > 0:
            world.occupied_cells.add((ant.x, ant.y))
            continue
        if _feed_at_nest(world, ant, config, tick):
            feeds += 1
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
        if _pickup_food(world, ant, config, tick):
            pickups += 1
        if _unload_food(world, ant, config, tick):
            unloads += 1
        _deposit_trail(world, ant, config, tick)
        _update_stale_signal(world, ant)
        _remember_position(ant)
        world.occupied_cells.add((ant.x, ant.y))
    if _spawn_ant(world, config, tick):
        births += 1
    contested_sources += _update_food_source_competition(world, tick)
    hostility_contacts += _count_hostility_contacts(world, config)
    combat_pairs = _current_combat_pairs(world)
    frozen_ants = combat_pairs * 2
    _advance_combat_state(world, config, tick)
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
        "births": births,
        "deaths": deaths,
        "feeds": feeds,
        "upkeep": upkeep,
        "food_reseeds": reseeds,
        "contested_sources": contested_sources,
        "hostility_contacts": hostility_contacts,
        "combat_starts": combat_starts,
        "combat_pairs": combat_pairs,
        "frozen_ants": frozen_ants,
        "max_source_pressure": round(max((patch.competition_pressure for patch in world.food_patches), default=0.0), 4),
        "food_trail_cells": sum(len(field) for field in world.food_trail.values()),
        "home_trail_cells": sum(len(field) for field in world.home_trail.values()),
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
