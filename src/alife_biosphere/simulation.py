from __future__ import annotations

from dataclasses import dataclass

from .config import SimulationConfig
from .config import WorldConfig
from .events import Event
from .rng import make_rng
from .world import World


@dataclass(frozen=True)
class SimulationResult:
    world: World

    @property
    def events(self) -> list[Event]:
        return self.world.events

    def summary(self) -> dict[str, int]:
        return {
            "ticks": self.world.tick,
            "alive": self.world.alive_count(),
            "dead": len(self.world.organisms) - self.world.alive_count(),
            "events": len(self.world.events),
        }


def _clamp(value: float, lower: float, upper: float) -> float:
    return min(upper, max(lower, value))


def _recompute_habitat_pressure(world: World, config: WorldConfig) -> None:
    for habitat in world.habitats.values():
        habitat.recompute_pressure(config.occupancy_stress_scale)


def _update_habitats(world: World, config: WorldConfig, tick: int) -> None:
    for habitat_id in sorted(world.habitats):
        habitat = world.habitats[habitat_id]
        rng = make_rng(config.seed, f"tick:{tick}:habitat:{habitat_id}:climate")
        noise = rng.uniform(-habitat.climate_drift, habitat.climate_drift)
        habitat.regenerate(noise)


def _apply_disturbance_hook(world: World, config: WorldConfig, tick: int) -> None:
    if config.disturbance_interval <= 0 or tick % config.disturbance_interval != 0:
        return
    candidate_ids = sorted(
        habitat_id
        for habitat_id, habitat in world.habitats.items()
        if habitat.habitat_family != "refuge"
    )
    if not candidate_ids:
        candidate_ids = sorted(world.habitats)
    rng = make_rng(config.seed + config.disturbance_seed_offset, f"disturbance:{tick}")
    target_id = candidate_ids[rng.randrange(len(candidate_ids))]
    habitat = world.habitats[target_id]
    resource_loss = min(habitat.resource_level, config.disturbance_resource_shock)
    habitat.resource_level -= resource_loss
    habitat.climate_state = _clamp(
        habitat.climate_state + config.disturbance_hazard_pulse,
        -1.0,
        1.0,
    )
    habitat.disturbance_trace += resource_loss + config.disturbance_hazard_pulse
    world.emit(
        Event(
            tick=tick,
            event_type="disturbance",
            organism_id=None,
            habitat_id=target_id,
            payload={
                "resource_loss": round(resource_loss, 4),
                "hazard_pulse": round(config.disturbance_hazard_pulse, 4),
            },
        )
    )


def _habitat_score(
    habitat,
    organism,
    current_habitat_id: str,
) -> float:
    resource_score = habitat.resource_level / habitat.max_resource_level
    hazard_cost = habitat.hazard_level + max(0.0, habitat.climate_state) * 0.1
    pressure_cost = habitat.occupancy_pressure
    score = resource_score * 1.4 - hazard_cost * 1.8 - pressure_cost * 1.3
    if organism.life_stage == "juvenile" and habitat.habitat_family == "nursery":
        score += 0.35
    if organism.integrity < 0.55 or organism.life_stage == "senescent":
        score += habitat.refuge_score * 0.55
    else:
        score += habitat.refuge_score * 0.1
    if habitat.habitat_family == "wild" and organism.life_stage == "mature":
        score += 0.15
    if habitat.habitat_id == current_habitat_id:
        score += 0.05
    return score


def _attempt_movement(
    world: World,
    organism_id: str,
    config: WorldConfig,
    tick: int,
) -> bool:
    organism = world.organisms[organism_id]
    if not organism.alive:
        return False
    current = world.habitats[organism.habitat_id]
    if organism.life_stage == "juvenile" and current.habitat_family == "nursery":
        return False
    if not current.neighbors:
        return False
    current_score = _habitat_score(current, organism, current.habitat_id)
    best_neighbor_id = max(
        current.neighbors,
        key=lambda neighbor_id: (
            _habitat_score(world.habitats[neighbor_id], organism, current.habitat_id),
            neighbor_id,
        ),
    )
    best_neighbor = world.habitats[best_neighbor_id]
    best_score = _habitat_score(best_neighbor, organism, current.habitat_id)
    wants_move = (
        best_score > current_score + 0.25
        or current.occupancy_pressure > 0.0
        or current.hazard_level >= 0.15
    )
    if not wants_move:
        return False
    if organism.movement_cooldown > 0:
        world.emit(
            Event(
                tick=tick,
                event_type="move_blocked",
                organism_id=organism.organism_id,
                habitat_id=organism.habitat_id,
                payload={"reason": "cooldown", "target_habitat_id": best_neighbor_id},
            )
        )
        return False
    if organism.integrity <= 0.25:
        world.emit(
            Event(
                tick=tick,
                event_type="move_blocked",
                organism_id=organism.organism_id,
                habitat_id=organism.habitat_id,
                payload={"reason": "low_integrity", "target_habitat_id": best_neighbor_id},
            )
        )
        return False
    origin_id = organism.habitat_id
    world.move_organism(organism.organism_id, best_neighbor_id)
    organism.energy = max(0.0, organism.energy - config.movement_cost)
    organism.integrity = max(0.0, organism.integrity - config.migration_integrity_risk)
    organism.movement_cooldown = config.organism.movement_cooldown_ticks
    if organism.integrity <= 0.0:
        organism.die("migration_failure")
    world.emit(
        Event(
            tick=tick,
            event_type="move",
            organism_id=organism.organism_id,
            habitat_id=best_neighbor_id,
            payload={"from_habitat_id": origin_id, "to_habitat_id": best_neighbor_id},
        )
    )
    return True


def _emit_damage_event(
    world: World,
    tick: int,
    organism_id: str,
    habitat_id: str,
    event_type: str,
    amount: float,
) -> None:
    world.emit(
        Event(
            tick=tick,
            event_type=event_type,
            organism_id=organism_id,
            habitat_id=habitat_id,
            payload={"amount": round(amount, 4)},
        )
    )


def _emit_repair_event(
    world: World,
    tick: int,
    organism_id: str,
    habitat_id: str,
    amount: float,
) -> None:
    world.emit(
        Event(
            tick=tick,
            event_type="repair",
            organism_id=organism_id,
            habitat_id=habitat_id,
            payload={"amount": round(amount, 4)},
        )
    )


def _apply_ecological_damage(world: World, organism_id: str, config: WorldConfig, tick: int) -> None:
    organism = world.organisms[organism_id]
    if not organism.alive:
        return
    habitat = world.habitats[organism.habitat_id]
    hazard_amount = _clamp(
        (habitat.hazard_level + max(0.0, habitat.climate_state) * 0.05)
        * config.organism.hazard_damage_scale,
        0.0,
        1.0,
    )
    if hazard_amount > 0.0:
        applied = organism.apply_damage(hazard_amount, "hazard_damage")
        if applied > 0.0:
            _emit_damage_event(
                world,
                tick,
                organism.organism_id,
                organism.habitat_id,
                "hazard_damage",
                applied,
            )
    if not organism.alive:
        return
    crowding_amount = habitat.occupancy_pressure * config.organism.crowding_integrity_penalty
    if crowding_amount > 0.0:
        applied = organism.apply_damage(crowding_amount, "crowding_damage")
        organism.energy = max(0.0, organism.energy - habitat.occupancy_pressure * config.crowding_energy_penalty)
        if applied > 0.0:
            _emit_damage_event(
                world,
                tick,
                organism.organism_id,
                organism.habitat_id,
                "crowding_damage",
                applied,
            )


def _update_reproduction_readiness(world: World, organism_id: str, config: WorldConfig, tick: int) -> None:
    organism = world.organisms[organism_id]
    if not organism.alive:
        return
    ready = (
        organism.life_stage in {"mature", "senescent"}
        and organism.energy >= config.reproduction_energy_threshold
        and organism.matter >= config.reproduction_matter_threshold
        and organism.integrity >= config.reproduction_integrity_threshold
    )
    if ready == organism.reproduction_ready:
        return
    organism.reproduction_ready = ready
    world.emit(
        Event(
            tick=tick,
            event_type="reproduction_ready" if ready else "reproduction_unready",
            organism_id=organism.organism_id,
            habitat_id=organism.habitat_id,
            payload={
                "energy": round(organism.energy, 4),
                "matter": round(organism.matter, 4),
                "integrity": round(organism.integrity, 4),
            },
        )
    )


def _base_reproduction_score(organism, habitat, config: WorldConfig) -> float:
    family_bonus = {
        "nursery": 0.12,
        "refuge": 0.04,
        "frontier": 0.0,
        "wild": -0.05,
    }[habitat.habitat_family]
    score = config.reproduction_chance
    score += family_bonus
    score -= habitat.hazard_level * 0.35
    score -= habitat.occupancy_pressure * 0.45
    if organism.life_stage == "senescent":
        score -= 0.08
    return _clamp(score, 0.0, 1.0)


def _attempt_reproduction(
    world: World,
    organism_id: str,
    config: WorldConfig,
    tick: int,
) -> Organism | None:
    organism = world.organisms[organism_id]
    if not organism.alive or not organism.reproduction_ready:
        return None
    habitat = world.habitats[organism.habitat_id]
    if len(habitat.occupants) >= habitat.capacity:
        return None
    if organism.energy < config.reproduction_energy_cost or organism.matter < config.reproduction_matter_cost:
        return None
    rng = make_rng(config.seed, f"tick:{tick}:reproduction:{organism_id}")
    if rng.random() > _base_reproduction_score(organism, habitat, config):
        return None
    child_id = world.allocate_organism_id()
    child = type(organism)(
        organism_id=child_id,
        lineage_id=organism.lineage_id,
        parent_id=organism.organism_id,
        habitat_id=organism.habitat_id,
        energy=max(1.0, config.organism.initial_energy * config.offspring_energy_scale),
        matter=config.organism.initial_matter * config.offspring_matter_scale,
        integrity=min(organism.integrity, config.organism.initial_integrity),
        information=0.0,
        age=0,
        generation=organism.generation + 1,
        birth_tick=tick,
    )
    organism.energy = max(0.0, organism.energy - config.reproduction_energy_cost)
    organism.matter = max(0.0, organism.matter - config.reproduction_matter_cost)
    organism.apply_damage(config.reproduction_integrity_cost, "reproduction_cost")
    organism.reproduction_ready = False
    world.emit(
        Event(
            tick=tick,
            event_type="birth",
            organism_id=child.organism_id,
            habitat_id=child.habitat_id,
            payload={
                "parent_id": organism.organism_id,
                "lineage_id": child.lineage_id,
                "generation": child.generation,
            },
        )
    )
    world.emit(
        Event(
            tick=tick,
            event_type="reproduction_unready",
            organism_id=organism.organism_id,
            habitat_id=organism.habitat_id,
            payload={
                "energy": round(organism.energy, 4),
                "matter": round(organism.matter, 4),
                "integrity": round(organism.integrity, 4),
                "reason": "post_birth_cost",
            },
        )
    )
    return child


def _resolve_death(world: World, organism_id: str, config: WorldConfig, tick: int) -> None:
    organism = world.organisms[organism_id]
    if not organism.alive:
        world.remove_from_habitat(organism_id)
        world.emit(
            Event(
                tick=tick,
                event_type="death",
                organism_id=organism.organism_id,
                habitat_id=organism.habitat_id,
                payload={"reason": organism.death_reason or "unknown"},
            )
        )
        return
    if organism.age >= config.max_age and organism.die("old_age"):
        world.remove_from_habitat(organism_id)
        world.emit(
            Event(
                tick=tick,
                event_type="death",
                organism_id=organism.organism_id,
                habitat_id=organism.habitat_id,
                payload={"reason": organism.death_reason},
            )
        )


def run_simulation(config: SimulationConfig) -> SimulationResult:
    world = World.from_config(config.world)
    _recompute_habitat_pressure(world, config.world)
    for tick in range(1, config.world.ticks + 1):
        world.tick = tick
        _update_habitats(world, config.world, tick)
        _apply_disturbance_hook(world, config.world, tick)
        _recompute_habitat_pressure(world, config.world)
        moves_this_tick = 0
        births_this_tick: list[Organism] = []
        for organism_id in sorted(world.organisms):
            organism = world.organisms[organism_id]
            if not organism.alive:
                continue
            organism.begin_tick(
                metabolism_cost=config.world.organism.metabolism_cost,
                maturity_age=config.world.maturity_age,
                senescence_age=config.world.senescence_age,
            )
            if organism.age >= config.world.max_age:
                organism.die("old_age")
            if not organism.alive:
                _resolve_death(world, organism_id, config.world, tick)
                continue
            moved = _attempt_movement(world, organism_id, config.world, tick)
            moves_this_tick += int(moved)
            habitat = world.habitats[organism.habitat_id]
            if habitat.resource_level > 0:
                harvest = min(config.world.organism.harvest_gain, habitat.resource_level)
                habitat.resource_level -= harvest
                habitat.depletion_trace = 0.7 * habitat.depletion_trace + 0.3 * (
                    habitat.max_resource_level - habitat.resource_level
                )
                repair = organism.harvest(harvest, config.world.organism.repair_gain_scale)
                world.emit(
                    Event(
                        tick=tick,
                        event_type="harvest",
                        organism_id=organism.organism_id,
                        habitat_id=organism.habitat_id,
                        payload={"amount": round(harvest, 4)},
                    )
                )
                if repair > 0.0:
                    _emit_repair_event(
                        world,
                        tick,
                        organism.organism_id,
                        organism.habitat_id,
                        repair,
                    )
            _apply_ecological_damage(world, organism_id, config.world, tick)
            _update_reproduction_readiness(world, organism_id, config.world, tick)
            child = _attempt_reproduction(world, organism_id, config.world, tick)
            if child is not None:
                births_this_tick.append(child)
            _resolve_death(world, organism_id, config.world, tick)
        for child in births_this_tick:
            world.add_organism(child)
        _recompute_habitat_pressure(world, config.world)
        world.emit(
            Event(
                tick=tick,
                event_type="tick_summary",
                organism_id=None,
                habitat_id=None,
                payload={
                    "alive": world.alive_count(),
                    "movement_count": moves_this_tick,
                    "birth_count": len(births_this_tick),
                    "reproduction_ready_count": world.reproduction_ready_count(),
                    "refuge_occupancy": len(
                        [
                            organism_id
                            for organism_id in world.habitats["refuge"].occupants
                            if world.organisms[organism_id].alive
                        ]
                    )
                    if "refuge" in world.habitats
                    else 0,
                    "occupancy_by_habitat": world.occupancy_by_habitat(),
                    "occupancy_pressure_by_habitat": {
                        habitat_id: round(habitat.occupancy_pressure, 4)
                        for habitat_id, habitat in world.habitats.items()
                    },
                    "lineage_count": len(
                        {
                            organism.lineage_id
                            for organism in world.organisms.values()
                            if organism.alive
                        }
                    ),
                },
            )
        )
    return SimulationResult(world=world)
