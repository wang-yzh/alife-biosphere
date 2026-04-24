from __future__ import annotations

import json
from datetime import datetime
from itertools import combinations
from pathlib import Path
from typing import Iterable

from .checkpoint import load_checkpoint
from .reporting import summarize_food_source_competition, summarize_inheritance_dynamics
from .simulation import AntSandboxResult


def _normalize_path(path: str | Path) -> str:
    return str(Path(path).resolve())


def _normalize_parent_path(parent_path: str | None) -> str | None:
    if not parent_path:
        return None
    return _normalize_path(parent_path)


def _event_counts_by_colony(events, event_type: str, colony_ids: list[str]) -> dict[str, int]:
    counts = {colony_id: 0 for colony_id in colony_ids}
    for event in events:
        if event.event_type != event_type:
            continue
        colony_id = event.payload.get("colony_id")
        if colony_id in counts:
            counts[str(colony_id)] += 1
            continue
        if event.organism_id is None:
            continue
        prefix = str(event.organism_id).split("_", 1)[0]
        if prefix in counts:
            counts[prefix] += 1
    return counts


def _top_food_source(events, competition_summary: dict[str, object]) -> dict[str, object]:
    per_source = list(competition_summary["per_source"])
    if not per_source:
        return {"patch_id": None, "pickup_count": 0, "contested_event_count": 0}
    top = max(
        per_source,
        key=lambda item: (
            item["pickup_count"],
            item["contested_event_count"],
            item["contested_ticks"],
            item["competition_pressure"],
        ),
    )
    return {
        "patch_id": top["patch_id"],
        "pickup_count": top["pickup_count"],
        "contested_event_count": top["contested_event_count"],
    }


def _branch_summary(checkpoint_path: str | Path) -> dict[str, object]:
    resolved_path = Path(checkpoint_path).resolve()
    checkpoint = load_checkpoint(resolved_path)
    config = checkpoint.config
    world = checkpoint.world
    metadata = dict(checkpoint.metadata)
    result = AntSandboxResult(world=world)
    colony_ids = sorted(world.colonies)
    inheritance = summarize_inheritance_dynamics(result)
    competition = summarize_food_source_competition(result)
    alive_ants = [ant for ant in world.ants if ant.alive]
    unique_lineages = {ant.lineage_id for ant in world.ants if ant.lineage_id}
    provenance = {
        "checkpoint_path": str(resolved_path),
        "branch_id": str(metadata.get("branch_id", resolved_path.parent.name)),
        "run_id": str(metadata.get("run_id", "unknown")),
        "parent_branch_id": None if metadata.get("parent_branch_id") is None else str(metadata["parent_branch_id"]),
        "parent_run_id": None if metadata.get("parent_run_id") is None else str(metadata["parent_run_id"]),
        "parent_checkpoint": _normalize_parent_path(
            None if metadata.get("parent_checkpoint") is None else str(metadata["parent_checkpoint"])
        ),
        "forked_from_tick": None if metadata.get("forked_from_tick") is None else int(metadata["forked_from_tick"]),
        "start_tick": 0 if metadata.get("forked_from_tick") is None else int(metadata["forked_from_tick"]),
        "final_tick": world.tick,
        "seed": config.seed,
        "inheritance_mode": config.ants.inheritance_mode,
        "mutation_rate": config.ants.mutation_rate,
        "mutation_step": config.ants.mutation_step,
    }
    outcomes = {
        "alive_total": world.alive_count(),
        "alive_by_colony": {colony_id: world.alive_count_for_colony(colony_id) for colony_id in colony_ids},
        "births_by_colony": _event_counts_by_colony(world.events, "ant_birth", colony_ids),
        "deaths_by_colony": _event_counts_by_colony(world.events, "ant_death", colony_ids),
        "unloads_by_colony": _event_counts_by_colony(world.events, "food_unload", colony_ids),
        "pickups_by_colony": _event_counts_by_colony(world.events, "food_pickup", colony_ids),
        "nest_food_by_colony": {colony_id: world.colonies[colony_id].nest.stored_food for colony_id in colony_ids},
        "total_food_remaining": world.food_remaining(),
        "depleted_source_count": sum(1 for event in world.events if event.event_type == "food_source_depleted"),
        "contested_source_count": sum(1 for event in world.events if event.event_type == "food_source_contested"),
        "combat_start_count": sum(1 for event in world.events if event.event_type == "combat_start"),
        "max_generation": int(inheritance["max_generation"]),
        "genome_count": len({ant.genome_id for ant in world.ants}),
        "mutated_birth_count": int(inheritance["mutated_births"]),
        "unique_lineage_count": len(unique_lineages),
        "total_event_count": len(world.events),
    }
    spatial = {
        "occupied_cell_count": len({(ant.x, ant.y) for ant in alive_ants}),
        "food_trail_cell_count_by_colony": {
            colony_id: len(world.food_trail.get(colony_id, {}))
            for colony_id in colony_ids
        },
        "home_trail_cell_count_by_colony": {
            colony_id: len(world.home_trail.get(colony_id, {}))
            for colony_id in colony_ids
        },
        "trail_cell_count_by_colony": {
            colony_id: len(world.food_trail.get(colony_id, {})) + len(world.home_trail.get(colony_id, {}))
            for colony_id in colony_ids
        },
        "total_trail_cell_count": sum(len(field) for field in world.food_trail.values())
        + sum(len(field) for field in world.home_trail.values()),
        "top_food_source": _top_food_source(world.events, competition),
    }
    return {
        "provenance": provenance,
        "outcomes": outcomes,
        "spatial": spatial,
    }


def _family_anchor(checkpoint_path: str, parent_by_path: dict[str, str | None]) -> str:
    current = checkpoint_path
    visited: set[str] = set()
    while current not in visited:
        visited.add(current)
        parent = parent_by_path.get(current)
        if parent is None:
            return current
        if parent not in parent_by_path:
            return parent
        current = parent
    return checkpoint_path


def _family_id(anchor_path: str, branch_by_path: dict[str, dict[str, object]]) -> str:
    if anchor_path in branch_by_path:
        return f"{branch_by_path[anchor_path]['provenance']['branch_id']}_family"
    anchor = Path(anchor_path)
    candidate = anchor.parent.name or anchor.stem or "checkpoint_family"
    return f"{candidate}_family"


def _family_summary(anchor_path: str, branches: list[dict[str, object]], branch_by_path: dict[str, dict[str, object]]) -> dict[str, object]:
    ordered = sorted(
        branches,
        key=lambda branch: (
            1 if branch["provenance"]["parent_checkpoint"] else 0,
            branch["provenance"]["start_tick"],
            branch["provenance"]["branch_id"],
        ),
    )
    pairwise = []
    for first, second in combinations(ordered, 2):
        pairwise.append(
            {
                "branch_a": first["provenance"]["branch_id"],
                "branch_b": second["provenance"]["branch_id"],
                "alive_delta": second["outcomes"]["alive_total"] - first["outcomes"]["alive_total"],
                "unload_delta": sum(second["outcomes"]["unloads_by_colony"].values())
                - sum(first["outcomes"]["unloads_by_colony"].values()),
                "nest_food_delta": sum(second["outcomes"]["nest_food_by_colony"].values())
                - sum(first["outcomes"]["nest_food_by_colony"].values()),
                "generation_delta": second["outcomes"]["max_generation"] - first["outcomes"]["max_generation"],
                "trail_cell_delta": second["spatial"]["total_trail_cell_count"] - first["spatial"]["total_trail_cell_count"],
                "lineage_count_delta": second["outcomes"]["unique_lineage_count"] - first["outcomes"]["unique_lineage_count"],
            }
        )
    return {
        "family_id": _family_id(anchor_path, branch_by_path),
        "anchor_checkpoint": anchor_path,
        "anchor_branch_id": None
        if anchor_path not in branch_by_path
        else branch_by_path[anchor_path]["provenance"]["branch_id"],
        "branch_count": len(ordered),
        "branches": ordered,
        "pairwise_deltas": pairwise,
    }


def build_branch_comparison_payload(checkpoint_paths: Iterable[str | Path]) -> dict[str, object]:
    normalized = sorted({_normalize_path(path) for path in checkpoint_paths})
    if not normalized:
        raise ValueError("at least one checkpoint path is required")
    branches = [_branch_summary(path) for path in normalized]
    branch_by_path = {branch["provenance"]["checkpoint_path"]: branch for branch in branches}
    parent_by_path = {
        branch["provenance"]["checkpoint_path"]: branch["provenance"]["parent_checkpoint"]
        for branch in branches
    }
    families_by_anchor: dict[str, list[dict[str, object]]] = {}
    for branch in branches:
        checkpoint_path = branch["provenance"]["checkpoint_path"]
        anchor = _family_anchor(checkpoint_path, parent_by_path)
        families_by_anchor.setdefault(anchor, []).append(branch)
    families = [
        _family_summary(anchor_path, family_branches, branch_by_path)
        for anchor_path, family_branches in sorted(families_by_anchor.items())
    ]
    comparison_id = (
        families[0]["family_id"]
        if len(families) == 1
        else f"multi_family_{len(families)}_{len(branches)}branches"
    )
    return {
        "comparison_id": comparison_id,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "checkpoint_count": len(branches),
        "family_count": len(families),
        "families": families,
        "caution": "These metrics show branch differences. They do not prove open-ended evolution.",
    }


def render_branch_comparison_markdown(payload: dict[str, object]) -> str:
    lines = [
        f"# Branch Comparison {payload['comparison_id']}",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        f"Families: {payload['family_count']}  ",
        f"Checkpoints: {payload['checkpoint_count']}",
        "",
    ]
    for family in payload["families"]:
        lines.extend(
            [
                f"## {family['family_id']}",
                "",
                f"Anchor checkpoint: `{family['anchor_checkpoint']}`",
                "",
                "### Branch Table",
                "",
                "| Branch | Parent | Start | Final | Seed | Inheritance | Mutation |",
                "| --- | --- | ---: | ---: | ---: | --- | ---: |",
            ]
        )
        for branch in family["branches"]:
            provenance = branch["provenance"]
            lines.append(
                "| "
                f"{provenance['branch_id']} | "
                f"{provenance['parent_branch_id'] or 'root'} | "
                f"{provenance['start_tick']} | "
                f"{provenance['final_tick']} | "
                f"{provenance['seed']} | "
                f"{provenance['inheritance_mode']} | "
                f"{provenance['mutation_rate']} |"
            )
        lines.extend(
            [
                "",
                "### Outcome Table",
                "",
                "| Branch | Alive | Unloads | Nest Food | Max Gen | Lineages | Events |",
                "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        for branch in family["branches"]:
            outcomes = branch["outcomes"]
            lines.append(
                "| "
                f"{branch['provenance']['branch_id']} | "
                f"{outcomes['alive_total']} | "
                f"{sum(outcomes['unloads_by_colony'].values())} | "
                f"{sum(outcomes['nest_food_by_colony'].values())} | "
                f"{outcomes['max_generation']} | "
                f"{outcomes['unique_lineage_count']} | "
                f"{outcomes['total_event_count']} |"
            )
        lines.extend(
            [
                "",
                "### Spatial Signature Table",
                "",
                "| Branch | Occupied Cells | Total Trail Cells | Top Food Source |",
                "| --- | ---: | ---: | --- |",
            ]
        )
        for branch in family["branches"]:
            spatial = branch["spatial"]
            top_source = spatial["top_food_source"]["patch_id"] or "none"
            lines.append(
                "| "
                f"{branch['provenance']['branch_id']} | "
                f"{spatial['occupied_cell_count']} | "
                f"{spatial['total_trail_cell_count']} | "
                f"{top_source} |"
            )
        lines.extend(["", "### Pairwise Divergence Notes", ""])
        if family["pairwise_deltas"]:
            for delta in family["pairwise_deltas"]:
                lines.append(
                    "- "
                    f"{delta['branch_b']} vs {delta['branch_a']}: "
                    f"alive {delta['alive_delta']:+d}, "
                    f"unloads {delta['unload_delta']:+d}, "
                    f"nest food {delta['nest_food_delta']:+d}, "
                    f"max generation {delta['generation_delta']:+d}, "
                    f"trail cells {delta['trail_cell_delta']:+d}, "
                    f"lineages {delta['lineage_count_delta']:+d}"
                )
        else:
            lines.append("- only one branch in this family")
        lines.extend(["", "### Caution", "", payload["caution"], ""])
    return "\n".join(lines).rstrip() + "\n"


def write_branch_comparison(output_dir: str | Path, payload: dict[str, object]) -> tuple[Path, Path]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    json_path = output_path / "comparison.json"
    markdown_path = output_path / "comparison.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    markdown_path.write_text(render_branch_comparison_markdown(payload), encoding="utf-8")
    return json_path, markdown_path
