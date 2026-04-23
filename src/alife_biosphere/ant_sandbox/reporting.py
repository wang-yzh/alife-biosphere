from __future__ import annotations

from dataclasses import dataclass
from math import dist

from ..events import Event
from .config import AntSandboxConfig
from .simulation import AntSandboxResult
from .world import SandboxAnt, initialize_world


@dataclass
class _AntState:
    ant_id: str
    colony_id: str
    x: int
    y: int
    carrying_food: bool
    alive: bool
    age: int


def _tick_summaries(events: list[Event]) -> list[Event]:
    return [event for event in events if event.event_type == "tick_summary"]


def _replay_ant_states(config: AntSandboxConfig, result: AntSandboxResult) -> dict[int, dict[str, _AntState]]:
    seed_world = initialize_world(config)
    states: dict[str, _AntState] = {
        ant.ant_id: _AntState(
            ant_id=ant.ant_id,
            colony_id=ant.colony_id,
            x=ant.x,
            y=ant.y,
            carrying_food=ant.carrying_food,
            alive=ant.alive,
            age=ant.age,
        )
        for ant in seed_world.ants
    }
    snapshots: dict[int, dict[str, _AntState]] = {}
    tick_events: dict[int, list[Event]] = {}
    for event in result.events:
        if event.event_type == "tick_summary":
            continue
        tick_events.setdefault(event.tick, []).append(event)

    final_tick = result.summary()["ticks"]
    for tick in range(1, final_tick + 1):
        for event in tick_events.get(tick, []):
            if event.event_type == "move" and event.organism_id is not None and event.organism_id in states:
                states[event.organism_id].x = int(event.payload["to_x"])
                states[event.organism_id].y = int(event.payload["to_y"])
            elif event.event_type == "food_pickup" and event.organism_id is not None and event.organism_id in states:
                states[event.organism_id].carrying_food = True
            elif event.event_type == "food_unload" and event.organism_id is not None and event.organism_id in states:
                states[event.organism_id].carrying_food = False
            elif event.event_type == "ant_birth" and event.organism_id is not None:
                states[event.organism_id] = _AntState(
                    ant_id=event.organism_id,
                    colony_id=str(event.payload.get("colony_id", "solo")),
                    x=int(event.payload["x"]),
                    y=int(event.payload["y"]),
                    carrying_food=False,
                    alive=True,
                    age=0,
                )
            elif event.event_type == "ant_death" and event.organism_id is not None and event.organism_id in states:
                states[event.organism_id].alive = False
            if event.organism_id is not None and event.organism_id in states:
                states[event.organism_id].age += 1
        snapshots[tick] = {
            ant_id: _AntState(
                ant_id=state.ant_id,
                colony_id=state.colony_id,
                x=state.x,
                y=state.y,
                carrying_food=state.carrying_food,
                alive=state.alive,
                age=state.age,
            )
            for ant_id, state in states.items()
        }
    return snapshots


def _kmeans(
    feature_map: dict[str, list[float]],
    k: int = 3,
    iterations: int = 8,
) -> tuple[dict[str, int], list[list[float]]]:
    ant_ids = sorted(feature_map)
    vectors = [feature_map[ant_id] for ant_id in ant_ids]
    if not vectors:
        return {}, []
    dims = len(vectors[0])
    initial_ids = [ant_ids[min(i * len(ant_ids) // max(1, k), len(ant_ids) - 1)] for i in range(k)]
    centroids = [feature_map[ant_id][:] for ant_id in initial_ids]
    assignments = {ant_id: 0 for ant_id in ant_ids}
    for _ in range(iterations):
        for ant_id in ant_ids:
            vector = feature_map[ant_id]
            assignments[ant_id] = min(
                range(k),
                key=lambda idx: sum((vector[d] - centroids[idx][d]) ** 2 for d in range(dims)),
            )
        for idx in range(k):
            members = [feature_map[ant_id] for ant_id in ant_ids if assignments[ant_id] == idx]
            if not members:
                continue
            centroids[idx] = [
                sum(member[d] for member in members) / len(members)
                for d in range(dims)
            ]
    return assignments, centroids


def summarize_behavior_roles(
    config: AntSandboxConfig,
    result: AntSandboxResult,
    cluster_count: int = 3,
) -> dict[str, object]:
    snapshots = _replay_ant_states(config, result)
    events = result.events
    trait_map = {
        ant.ant_id: {
            "range_bias": ant.range_bias,
            "trail_affinity": ant.trail_affinity,
            "harvest_drive": ant.harvest_drive,
        }
        for ant in result.world.ants
    }
    moves_by_ant: dict[str, int] = {}
    pickups_by_ant: dict[str, int] = {}
    unloads_by_ant: dict[str, int] = {}
    for event in events:
        if event.organism_id is None:
            continue
        if event.event_type == "move":
            moves_by_ant[event.organism_id] = moves_by_ant.get(event.organism_id, 0) + 1
        elif event.event_type == "food_pickup":
            pickups_by_ant[event.organism_id] = pickups_by_ant.get(event.organism_id, 0) + 1
        elif event.event_type == "food_unload":
            unloads_by_ant[event.organism_id] = unloads_by_ant.get(event.organism_id, 0) + 1

    final_tick = result.summary()["ticks"]
    per_ant: dict[str, dict[str, object]] = {}
    for ant_id, final_state in snapshots[final_tick].items():
        alive_ticks = 0
        carrying_ticks = 0
        near_nest_ticks = 0
        far_field_ticks = 0
        total_distance = 0.0
        prev: _AntState | None = None
        for tick in range(1, final_tick + 1):
            state = snapshots[tick].get(ant_id)
            if state is None:
                continue
            if state.alive:
                alive_ticks += 1
            if state.carrying_food:
                carrying_ticks += 1
            colony = result.world.colonies.get(state.colony_id)
            nest_x = result.world.nest.x if colony is None else colony.nest.x
            nest_y = result.world.nest.y if colony is None else colony.nest.y
            nest_radius = result.world.nest.radius if colony is None else colony.nest.radius
            distance_from_nest = dist((state.x, state.y), (nest_x, nest_y))
            if distance_from_nest <= nest_radius + 3:
                near_nest_ticks += 1
            if distance_from_nest >= 12:
                far_field_ticks += 1
            if prev is not None:
                total_distance += dist((prev.x, prev.y), (state.x, state.y))
            prev = state
        per_ant[ant_id] = {
            "alive": final_state.alive,
            "colony_id": final_state.colony_id,
            "final_x": final_state.x,
            "final_y": final_state.y,
            "range_bias": round(trait_map.get(ant_id, {}).get("range_bias", 0.0), 4),
            "trail_affinity": round(trait_map.get(ant_id, {}).get("trail_affinity", 0.0), 4),
            "harvest_drive": round(trait_map.get(ant_id, {}).get("harvest_drive", 0.0), 4),
            "moves": moves_by_ant.get(ant_id, 0),
            "pickups": pickups_by_ant.get(ant_id, 0),
            "unloads": unloads_by_ant.get(ant_id, 0),
            "alive_ticks": alive_ticks,
            "carrying_ticks": carrying_ticks,
            "near_nest_ticks": near_nest_ticks,
            "far_field_ticks": far_field_ticks,
            "travel_distance": round(total_distance, 3),
        }

    feature_map = {
        ant_id: [
            values["moves"] / max(1, final_tick),
            values["pickups"],
            values["unloads"],
            values["far_field_ticks"] / max(1, final_tick),
            values["near_nest_ticks"] / max(1, final_tick),
        ]
        for ant_id, values in per_ant.items()
    }
    assignments, centroids = _kmeans(feature_map, k=cluster_count)

    cluster_members: dict[int, list[str]] = {idx: [] for idx in range(cluster_count)}
    for ant_id, cluster_idx in assignments.items():
        cluster_members[cluster_idx].append(ant_id)

    role_labels: dict[int, str] = {}
    for idx, centroid in enumerate(centroids):
        move_rate, pickups, unloads, far_ratio, near_ratio = centroid
        if far_ratio >= 0.36 and near_ratio <= 0.18 and unloads <= max(1.8, pickups * 0.9):
            label = "scout_like"
        elif near_ratio >= 0.42 and far_ratio <= 0.24 and pickups <= 2.0 and unloads <= 1.5:
            label = "nest_like"
        elif unloads >= max(2.0, pickups * 0.65):
            label = "forager_like"
        elif far_ratio > near_ratio and move_rate > 0.54:
            label = "scout_like"
        else:
            label = "forager_like"
        role_labels[idx] = label

    cluster_summaries = []
    for idx in range(cluster_count):
        members = sorted(cluster_members[idx])
        centroid = centroids[idx] if idx < len(centroids) else [0.0] * 5
        cluster_summaries.append(
            {
                "cluster_id": idx,
                "role_label": role_labels.get(idx, f"cluster_{idx}"),
                "member_count": len(members),
                "members": members,
                "centroid": {
                    "move_rate": round(centroid[0], 4),
                    "pickups": round(centroid[1], 4),
                    "unloads": round(centroid[2], 4),
                    "far_ratio": round(centroid[3], 4),
                    "near_ratio": round(centroid[4], 4),
                },
            }
        )

    return {
        "tick_count": final_tick,
        "per_ant": per_ant,
        "cluster_summaries": cluster_summaries,
        "role_distribution": {
            label: sum(1 for idx in assignments.values() if role_labels[idx] == label)
            for label in sorted(set(role_labels.values()))
        },
    }


def summarize_food_source_competition(result: AntSandboxResult) -> dict[str, object]:
    pickups_by_source: dict[str, int] = {}
    contested_by_source: dict[str, int] = {}
    for event in result.events:
        if event.habitat_id is None:
            continue
        if event.event_type == "food_pickup":
            pickups_by_source[event.habitat_id] = pickups_by_source.get(event.habitat_id, 0) + 1
        elif event.event_type == "food_source_contested":
            contested_by_source[event.habitat_id] = contested_by_source.get(event.habitat_id, 0) + 1

    per_source = []
    for patch in result.world.food_patches:
        per_source.append(
            {
                "patch_id": patch.patch_id,
                "amount": patch.amount,
                "max_amount": patch.max_amount,
                "value_score": patch.value_score,
                "nearby_ants": patch.nearby_ants,
                "carrying_nearby": patch.carrying_nearby,
                "competition_pressure": round(patch.competition_pressure, 4),
                "contested_ticks": patch.contested_ticks,
                "depletion_count": patch.depletion_count,
                "pickup_count": pickups_by_source.get(patch.patch_id, 0),
                "contested_event_count": contested_by_source.get(patch.patch_id, 0),
            }
        )
    top_sources = sorted(
        per_source,
        key=lambda item: (
            item["contested_ticks"],
            item["pickup_count"],
            item["competition_pressure"],
        ),
        reverse=True,
    )
    return {
        "per_source": per_source,
        "top_competition_sources": top_sources[:3],
    }
