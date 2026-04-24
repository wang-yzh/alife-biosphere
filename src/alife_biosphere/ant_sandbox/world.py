from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import atan2, cos, dist, sin, tau

from .config import AntSandboxConfig, ColonyConfig
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

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "Nest":
        return cls(
            x=int(payload["x"]),
            y=int(payload["y"]),
            radius=int(payload["radius"]),
            stored_food=int(payload.get("stored_food", 0)),
            upkeep_reserve=float(payload.get("upkeep_reserve", 0.0)),
        )


@dataclass
class Colony:
    colony_id: str
    display_name: str
    color: str
    nest: Nest

    @classmethod
    def from_dict(cls, colony_id: str, payload: dict[str, object]) -> "Colony":
        return cls(
            colony_id=str(payload.get("colony_id", colony_id)),
            display_name=str(payload["display_name"]),
            color=str(payload["color"]),
            nest=Nest.from_dict(dict(payload["nest"])),
        )


@dataclass
class FoodPatch:
    patch_id: str
    x: int
    y: int
    radius: int
    amount: int
    max_amount: int
    value_score: float = 1.0
    regrowth_rate: int = 0
    relocate_on_depletion: bool = True
    respawn_delay_ticks: int = 28
    regrow_only_when_empty: bool = False
    empty_ticks: int = 0
    respawn_count: int = 0
    nearby_ants: int = 0
    carrying_nearby: int = 0
    recent_pickups: int = 0
    competition_pressure: float = 0.0
    contested_ticks: int = 0
    depletion_count: int = 0

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "FoodPatch":
        return cls(
            patch_id=str(payload["patch_id"]),
            x=int(payload["x"]),
            y=int(payload["y"]),
            radius=int(payload["radius"]),
            amount=int(payload["amount"]),
            max_amount=int(payload["max_amount"]),
            value_score=float(payload.get("value_score", 1.0)),
            regrowth_rate=int(payload.get("regrowth_rate", 0)),
            relocate_on_depletion=bool(payload.get("relocate_on_depletion", True)),
            respawn_delay_ticks=int(payload.get("respawn_delay_ticks", 28)),
            regrow_only_when_empty=bool(payload.get("regrow_only_when_empty", False)),
            empty_ticks=int(payload.get("empty_ticks", 0)),
            respawn_count=int(payload.get("respawn_count", 0)),
            nearby_ants=int(payload.get("nearby_ants", 0)),
            carrying_nearby=int(payload.get("carrying_nearby", 0)),
            recent_pickups=int(payload.get("recent_pickups", 0)),
            competition_pressure=float(payload.get("competition_pressure", 0.0)),
            contested_ticks=int(payload.get("contested_ticks", 0)),
            depletion_count=int(payload.get("depletion_count", 0)),
        )


@dataclass
class Corpse:
    corpse_id: str
    source_ant_id: str
    x: int
    y: int
    colony_id: str
    death_tick: int
    energy_value: float
    decay_ticks_remaining: int
    death_reason: str

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "Corpse":
        return cls(
            corpse_id=str(payload["corpse_id"]),
            source_ant_id=str(payload["source_ant_id"]),
            x=int(payload["x"]),
            y=int(payload["y"]),
            colony_id=str(payload["colony_id"]),
            death_tick=int(payload["death_tick"]),
            energy_value=float(payload["energy_value"]),
            decay_ticks_remaining=int(payload["decay_ticks_remaining"]),
            death_reason=str(payload["death_reason"]),
        )


@dataclass
class InstinctGenome:
    genome_id: str
    parent_genome_id: str | None = None
    generation: int = 0
    range_bias: float = 0.5
    trail_affinity: float = 0.5
    harvest_drive: float = 0.5
    mutation_count: int = 0
    mutation_log: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "InstinctGenome":
        return cls(
            genome_id=str(payload["genome_id"]),
            parent_genome_id=None if payload.get("parent_genome_id") is None else str(payload["parent_genome_id"]),
            generation=int(payload.get("generation", 0)),
            range_bias=float(payload.get("range_bias", 0.5)),
            trail_affinity=float(payload.get("trail_affinity", 0.5)),
            harvest_drive=float(payload.get("harvest_drive", 0.5)),
            mutation_count=int(payload.get("mutation_count", 0)),
            mutation_log=[str(item) for item in payload.get("mutation_log", [])],
        )


@dataclass
class SandboxAnt:
    ant_id: str
    colony_id: str
    x: int
    y: int
    heading: float
    energy: float
    genome: InstinctGenome
    carrying_food: bool = False
    target_patch_id: str | None = None
    outbound_commit_ticks: int = 0
    combat_with_id: str | None = None
    combat_ticks_remaining: int = 0
    combat_cooldown_ticks: int = 0
    behavior_state: str = "forage"
    contest_patch_id: str | None = None
    starvation_ticks: int = 0
    recent_positions: list[tuple[int, int]] = field(default_factory=list)
    age: int = 0
    birth_tick: int = 0
    alive: bool = True
    parent_id: str | None = None
    lineage_id: str | None = None
    delivered_food: int = 0

    @property
    def genome_id(self) -> str:
        return self.genome.genome_id

    @property
    def parent_genome_id(self) -> str | None:
        return self.genome.parent_genome_id

    @property
    def generation(self) -> int:
        return self.genome.generation

    @property
    def mutation_count(self) -> int:
        return self.genome.mutation_count

    @property
    def mutation_log(self) -> list[str]:
        return self.genome.mutation_log

    @property
    def range_bias(self) -> float:
        return self.genome.range_bias

    @range_bias.setter
    def range_bias(self, value: float) -> None:
        self.genome.range_bias = value

    @property
    def trail_affinity(self) -> float:
        return self.genome.trail_affinity

    @trail_affinity.setter
    def trail_affinity(self, value: float) -> None:
        self.genome.trail_affinity = value

    @property
    def harvest_drive(self) -> float:
        return self.genome.harvest_drive

    @harvest_drive.setter
    def harvest_drive(self, value: float) -> None:
        self.genome.harvest_drive = value

    def to_dict(self) -> dict[str, object]:
        return {
            "ant_id": self.ant_id,
            "colony_id": self.colony_id,
            "x": self.x,
            "y": self.y,
            "heading": self.heading,
            "energy": self.energy,
            "genome": self.genome.to_dict(),
            "genome_id": self.genome_id,
            "parent_genome_id": self.parent_genome_id,
            "generation": self.generation,
            "mutation_count": self.mutation_count,
            "mutation_log": list(self.mutation_log),
            "range_bias": self.range_bias,
            "trail_affinity": self.trail_affinity,
            "harvest_drive": self.harvest_drive,
            "carrying_food": self.carrying_food,
            "target_patch_id": self.target_patch_id,
            "outbound_commit_ticks": self.outbound_commit_ticks,
            "combat_with_id": self.combat_with_id,
            "combat_ticks_remaining": self.combat_ticks_remaining,
            "combat_cooldown_ticks": self.combat_cooldown_ticks,
            "behavior_state": self.behavior_state,
            "contest_patch_id": self.contest_patch_id,
            "starvation_ticks": self.starvation_ticks,
            "recent_positions": list(self.recent_positions),
            "age": self.age,
            "birth_tick": self.birth_tick,
            "alive": self.alive,
            "parent_id": self.parent_id,
            "lineage_id": self.lineage_id,
            "delivered_food": self.delivered_food,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "SandboxAnt":
        genome_payload = dict(payload.get("genome", payload))
        return cls(
            ant_id=str(payload["ant_id"]),
            colony_id=str(payload["colony_id"]),
            x=int(payload["x"]),
            y=int(payload["y"]),
            heading=float(payload["heading"]),
            energy=float(payload["energy"]),
            genome=InstinctGenome.from_dict(genome_payload),
            carrying_food=bool(payload.get("carrying_food", False)),
            target_patch_id=None if payload.get("target_patch_id") is None else str(payload["target_patch_id"]),
            outbound_commit_ticks=int(payload.get("outbound_commit_ticks", 0)),
            combat_with_id=None if payload.get("combat_with_id") is None else str(payload["combat_with_id"]),
            combat_ticks_remaining=int(payload.get("combat_ticks_remaining", 0)),
            combat_cooldown_ticks=int(payload.get("combat_cooldown_ticks", 0)),
            behavior_state=str(payload.get("behavior_state", "forage")),
            contest_patch_id=None if payload.get("contest_patch_id") is None else str(payload["contest_patch_id"]),
            starvation_ticks=int(payload.get("starvation_ticks", 0)),
            recent_positions=[_cell_from_sequence(cell) for cell in payload.get("recent_positions", [])],
            age=int(payload.get("age", 0)),
            birth_tick=int(payload.get("birth_tick", 0)),
            alive=bool(payload.get("alive", True)),
            parent_id=None if payload.get("parent_id") is None else str(payload["parent_id"]),
            lineage_id=None if payload.get("lineage_id") is None else str(payload["lineage_id"]),
            delivered_food=int(payload.get("delivered_food", 0)),
        )


@dataclass
class AntSandboxWorld:
    width: int
    height: int
    nest: Nest
    colonies: dict[str, Colony]
    food_patches: list[FoodPatch]
    ants: list[SandboxAnt]
    corpses: list[Corpse] = field(default_factory=list)
    tick: int = 0
    next_ant_index: int = 0
    next_genome_index: int = 0
    occupied_cells: set[tuple[int, int]] = field(default_factory=set)
    events: list[Event] = field(default_factory=list)
    food_trail: dict[str, dict[tuple[int, int], float]] = field(default_factory=dict)
    home_trail: dict[str, dict[tuple[int, int], float]] = field(default_factory=dict)
    stale_field: dict[tuple[int, int], float] = field(default_factory=dict)
    residue_field: dict[tuple[int, int], dict[str, object]] = field(default_factory=dict)
    terrain: dict[tuple[int, int], str] = field(default_factory=dict)
    navigation_cache: dict[str, dict[tuple[int, int], float]] = field(default_factory=dict)

    def emit(self, event: Event) -> None:
        self.events.append(event)

    def alive_count(self) -> int:
        return sum(1 for ant in self.ants if ant.alive)

    def carrying_count(self) -> int:
        return sum(1 for ant in self.ants if ant.alive and ant.carrying_food)

    def food_remaining(self) -> int:
        return sum(patch.amount for patch in self.food_patches)

    def delivered_food_total(self) -> int:
        return sum(colony.nest.stored_food for colony in self.colonies.values())

    def corpse_count(self) -> int:
        return len(self.corpses)

    def residue_cell_count(self) -> int:
        return len(self.residue_field)

    def residue_total_value(self) -> float:
        return round(sum(float(entry["value"]) for entry in self.residue_field.values()), 4)

    def colony_nest(self, colony_id: str) -> Nest:
        return self.colonies[colony_id].nest

    def alive_count_for_colony(self, colony_id: str) -> int:
        return sum(1 for ant in self.ants if ant.alive and ant.colony_id == colony_id)

    def allocate_ant_id(self, colony_id: str | None = None) -> str:
        prefix = colony_id or "ant"
        ant_id = f"{prefix}_{self.next_ant_index:03d}"
        self.next_ant_index += 1
        return ant_id

    def allocate_genome_id(self, colony_id: str | None = None) -> str:
        prefix = colony_id or "genome"
        genome_id = f"{prefix}_g{self.next_genome_index:03d}"
        self.next_genome_index += 1
        return genome_id

    def summary(self) -> dict[str, int]:
        return {
            "ticks": self.tick,
            "alive": self.alive_count(),
            "carrying": self.carrying_count(),
            "nest_food": self.delivered_food_total(),
            "food_remaining": self.food_remaining(),
            "corpse_count": self.corpse_count(),
            "residue_cell_count": self.residue_cell_count(),
            "residue_total_value": self.residue_total_value(),
            "events": len(self.events),
        }

    def to_dict(self) -> dict[str, object]:
        return {
            "width": self.width,
            "height": self.height,
            "tick": self.tick,
            "next_ant_index": self.next_ant_index,
            "next_genome_index": self.next_genome_index,
            "nest": asdict(self.nest),
            "colonies": {colony_id: {"display_name": colony.display_name, "color": colony.color, "nest": asdict(colony.nest)} for colony_id, colony in self.colonies.items()},
            "food_patches": [asdict(patch) for patch in self.food_patches],
            "ants": [ant.to_dict() for ant in self.ants],
            "corpses": [asdict(corpse) for corpse in self.corpses],
            "occupied_cells": [[x, y] for x, y in sorted(self.occupied_cells)],
            "events": [event.to_dict() for event in self.events],
            "food_trail": {
                colony_id: {f"{x},{y}": value for (x, y), value in field.items()}
                for colony_id, field in self.food_trail.items()
            },
            "home_trail": {
                colony_id: {f"{x},{y}": value for (x, y), value in field.items()}
                for colony_id, field in self.home_trail.items()
            },
            "stale_field": {f"{x},{y}": value for (x, y), value in self.stale_field.items()},
            "residue_field": {
                f"{x},{y}": {
                    "value": round(float(entry["value"]), 6),
                    "source_type": str(entry.get("source_type", "unknown")),
                }
                for (x, y), entry in self.residue_field.items()
            },
            "terrain": {f"{x},{y}": kind for (x, y), kind in self.terrain.items()},
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "AntSandboxWorld":
        colonies_payload = dict(payload["colonies"])
        colonies = {
            str(colony_id): Colony.from_dict(str(colony_id), dict(colony_payload))
            for colony_id, colony_payload in colonies_payload.items()
        }
        nest = Nest.from_dict(dict(payload["nest"]))
        if colonies:
            first_colony = next(iter(colonies.values()))
            if (nest.x, nest.y, nest.radius) == (first_colony.nest.x, first_colony.nest.y, first_colony.nest.radius):
                nest = first_colony.nest
        ants = [SandboxAnt.from_dict(dict(ant_payload)) for ant_payload in payload.get("ants", [])]
        occupied_payload = payload.get("occupied_cells")
        occupied_cells = (
            {_cell_from_sequence(cell) for cell in occupied_payload}
            if occupied_payload is not None
            else {(ant.x, ant.y) for ant in ants if ant.alive}
        )
        return cls(
            width=int(payload["width"]),
            height=int(payload["height"]),
            nest=nest,
            colonies=colonies,
            food_patches=[FoodPatch.from_dict(dict(patch)) for patch in payload.get("food_patches", [])],
            ants=ants,
            corpses=[Corpse.from_dict(dict(corpse)) for corpse in payload.get("corpses", [])],
            tick=int(payload.get("tick", 0)),
            next_ant_index=int(payload.get("next_ant_index", len(ants))),
            next_genome_index=int(payload.get("next_genome_index", len(ants))),
            occupied_cells=occupied_cells,
            events=[Event.from_dict(dict(event)) for event in payload.get("events", [])],
            food_trail={
                str(colony_id): _cell_float_map(dict(field))
                for colony_id, field in dict(payload.get("food_trail", {})).items()
            },
            home_trail={
                str(colony_id): _cell_float_map(dict(field))
                for colony_id, field in dict(payload.get("home_trail", {})).items()
            },
            stale_field=_cell_float_map(dict(payload.get("stale_field", {}))),
            residue_field=_residue_cell_map(dict(payload.get("residue_field", {}))),
            terrain={_cell_from_key(key): str(kind) for key, kind in dict(payload.get("terrain", {})).items()},
            navigation_cache={},
        )


def _cell_from_key(key: str) -> tuple[int, int]:
    x_text, y_text = key.split(",", 1)
    return int(x_text), int(y_text)


def _cell_from_sequence(cell: object) -> tuple[int, int]:
    x, y = cell
    return int(x), int(y)


def _cell_float_map(payload: dict[str, object]) -> dict[tuple[int, int], float]:
    return {_cell_from_key(key): float(value) for key, value in payload.items()}


def _residue_cell_map(payload: dict[str, object]) -> dict[tuple[int, int], dict[str, object]]:
    return {
        _cell_from_key(key): {
            "value": float(dict(value).get("value", 0.0)),
            "source_type": str(dict(value).get("source_type", "unknown")),
        }
        for key, value in payload.items()
    }


def _clamp_cell(value: int, lower: int, upper: int) -> int:
    return min(upper, max(lower, value))


def _distance(a_x: int, a_y: int, b_x: int, b_y: int) -> float:
    return dist((a_x, a_y), (b_x, b_y))


def _clamp_unit(value: float) -> float:
    return min(1.0, max(0.0, value))


def sample_instinct_genome(
    config: AntSandboxConfig,
    colony_cfg: ColonyConfig,
    local_index: int,
    genome_id: str,
    rng_tag: str,
    *,
    parent_genome_id: str | None = None,
    generation: int = 0,
    mutation_count: int = 0,
    mutation_log: list[str] | None = None,
) -> InstinctGenome:
    trait_rng = make_rng(config.seed, rng_tag)
    count_scale = local_index / max(1, colony_cfg.ant_count - 1)
    range_bias = _clamp_unit(0.12 + 0.76 * count_scale + trait_rng.uniform(-0.12, 0.12))
    trail_phase = ((local_index * 7) % max(1, colony_cfg.ant_count)) / max(1, colony_cfg.ant_count - 1)
    trail_affinity = _clamp_unit(0.15 + 0.7 * trail_phase + trait_rng.uniform(-0.15, 0.15))
    harvest_phase = ((local_index * 13) % max(1, colony_cfg.ant_count)) / max(1, colony_cfg.ant_count - 1)
    harvest_drive = _clamp_unit(0.18 + 0.66 * harvest_phase + trait_rng.uniform(-0.16, 0.16))
    return InstinctGenome(
        genome_id=genome_id,
        parent_genome_id=parent_genome_id,
        generation=generation,
        range_bias=round(range_bias, 4),
        trail_affinity=round(trail_affinity, 4),
        harvest_drive=round(harvest_drive, 4),
        mutation_count=mutation_count,
        mutation_log=list(mutation_log or []),
    )


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

    if config.terrain.layout == "surface_showcase_walls":
        wall_sets = [
            # northwest choke
            ((width * 3) // 10, (height * 3) // 10, (height * 9) // 20, "vertical", {height // 3}),
            # central maze wall
            ((width * 7) // 12, (height * 5) // 24, (height * 19) // 24, "vertical", {height // 2, (height * 2) // 3}),
            # southeast stagger
            ((width * 4) // 5, (height * 9) // 16, (height * 7) // 8, "vertical", {(height * 11) // 16}),
            # lower middle shelf
            ((width * 9) // 20, (height * 7) // 10, (width * 11) // 16, "horizontal", {(width * 11) // 20}),
        ]
        for anchor, start, end, orientation, gaps in wall_sets:
            if orientation == "vertical":
                x = anchor
                for y in range(start, end):
                    if any(abs(y - gap) <= 2 for gap in gaps):
                        continue
                    terrain[(x, y)] = "rock"
                    if y % 3 != 0:
                        terrain[(x + 1, y)] = "rock"
            else:
                y = start
                for x in range(anchor, end):
                    if any(abs(x - gap) <= 2 for gap in gaps):
                        continue
                    terrain[(x, y)] = "rock"
                    if x % 3 != 0:
                        terrain[(x, y + 1)] = "rock"

    for colony in config.resolved_colonies():
        _clear_safe_zone(terrain, colony.nest.x, colony.nest.y, colony.nest.radius + 6)
    for patch in config.food_patches:
        _clear_safe_zone(terrain, patch.x, patch.y, patch.radius + 5)
    return terrain


def initialize_world(config: AntSandboxConfig) -> AntSandboxWorld:
    resolved_colonies = config.resolved_colonies()
    colonies = {
        colony.colony_id: Colony(
            colony_id=colony.colony_id,
            display_name=colony.display_name,
            color=colony.color,
            nest=Nest(
                x=_clamp_cell(colony.nest.x, 0, config.width - 1),
                y=_clamp_cell(colony.nest.y, 0, config.height - 1),
                radius=colony.nest.radius,
                stored_food=colony.nest.initial_stored_food,
            ),
        )
        for colony in resolved_colonies
    }
    nest = colonies[resolved_colonies[0].colony_id].nest
    food_patches = [
        FoodPatch(
            patch_id=patch.patch_id,
            x=_clamp_cell(patch.x, 0, config.width - 1),
            y=_clamp_cell(patch.y, 0, config.height - 1),
            radius=patch.radius,
            amount=patch.amount,
            max_amount=patch.amount if patch.max_amount is None else patch.max_amount,
            value_score=patch.value_score,
            regrowth_rate=patch.regrowth_rate,
            relocate_on_depletion=patch.relocate_on_depletion,
            respawn_delay_ticks=patch.respawn_delay_ticks,
            regrow_only_when_empty=patch.regrow_only_when_empty,
        )
        for patch in config.food_patches
    ]
    terrain = _generate_terrain(config)
    ants: list[SandboxAnt] = []
    occupied_cells: set[tuple[int, int]] = set()
    for colony_index, colony_cfg in enumerate(resolved_colonies):
        colony = colonies[colony_cfg.colony_id]
        colony_nest = colony.nest
        candidate_cells = sorted(
            [
                (
                    _clamp_cell(colony_nest.x + dx, 0, config.width - 1),
                    _clamp_cell(colony_nest.y + dy, 0, config.height - 1),
                )
                for radius in range(max(2, colony_nest.radius) + 4)
                for dy in range(-radius, radius + 1)
                for dx in range(-radius, radius + 1)
                if _distance(0, 0, dx, dy) <= max(2, colony_nest.radius) + 2
                and terrain.get(
                    (
                        _clamp_cell(colony_nest.x + dx, 0, config.width - 1),
                        _clamp_cell(colony_nest.y + dy, 0, config.height - 1),
                    ),
                    "open_ground",
                )
                != "rock"
            ],
            key=lambda cell: (
                _distance(cell[0], cell[1], colony_nest.x, colony_nest.y),
                round(atan2(cell[1] - colony_nest.y, cell[0] - colony_nest.x), 6),
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
        for local_index in range(colony_cfg.ant_count):
            global_index = len(ants)
            angle = tau * (local_index / max(colony_cfg.ant_count, 1))
            spawn_x, spawn_y = unique_cells[local_index % len(unique_cells)]
            while (spawn_x, spawn_y) in occupied_cells:
                local_index += 1
                spawn_x, spawn_y = unique_cells[local_index % len(unique_cells)]
            genome = sample_instinct_genome(
                config,
                colony_cfg,
                local_index,
                genome_id=f"{colony_cfg.colony_id}_g{local_index:03d}",
                rng_tag=f"ant-sandbox:{colony_cfg.colony_id}:traits:{global_index}",
            )
            ant = SandboxAnt(
                ant_id=f"{colony_cfg.colony_id}_{local_index:03d}",
                colony_id=colony_cfg.colony_id,
                x=spawn_x,
                y=spawn_y,
                heading=round(angle, 6),
                energy=config.ants.initial_energy,
                genome=genome,
                lineage_id=f"{colony_cfg.colony_id}_{local_index:03d}",
            )
            ants.append(ant)
            occupied_cells.add((ant.x, ant.y))
    return AntSandboxWorld(
        width=config.width,
        height=config.height,
        nest=nest,
        colonies=colonies,
        food_patches=food_patches,
        ants=ants,
        next_ant_index=len(ants),
        next_genome_index=len(ants),
        occupied_cells=occupied_cells,
        terrain=terrain,
        food_trail={colony_id: {} for colony_id in colonies},
        home_trail={colony_id: {} for colony_id in colonies},
    )
