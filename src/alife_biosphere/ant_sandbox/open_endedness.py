from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Iterable

from .comparison import build_branch_comparison_payload


STATUS_VALUES = {"available", "proxy", "requires_m14", "requires_m16", "not_implemented"}


def _metric(status: str, **payload: object) -> dict[str, object]:
    if status not in STATUS_VALUES:
        raise ValueError(f"unsupported metric status: {status}")
    return {"status": status, **payload}


def _sum_metric(mapping: dict[str, int]) -> int:
    return sum(int(value) for value in mapping.values())


def _outcome_value(branch: dict[str, object], key: str, default: int | float = 0) -> int | float:
    return dict(branch["outcomes"]).get(key, default)


def _spatial_value(branch: dict[str, object], key: str, default: int | float = 0) -> int | float:
    return dict(branch["spatial"]).get(key, default)


def _normalized_delta(left: float, right: float) -> float:
    scale = max(abs(left), abs(right), 1.0)
    return round(abs(left - right) / scale, 4)


def _population_vector(branch: dict[str, object]) -> list[int]:
    alive_by_colony = dict(branch["outcomes"]["alive_by_colony"])
    return [int(alive_by_colony[colony_id]) for colony_id in sorted(alive_by_colony)]


def _signature_distance(first: dict[str, object], second: dict[str, object]) -> dict[str, object]:
    first_outcomes = dict(first["outcomes"])
    second_outcomes = dict(second["outcomes"])
    first_spatial = dict(first["spatial"])
    second_spatial = dict(second["spatial"])
    first_population = _population_vector(first)
    second_population = _population_vector(second)
    population_distance = (
        round(
            sum(_normalized_delta(a, b) for a, b in zip(first_population, second_population))
            / max(1, len(first_population)),
            4,
        )
        if first_population and second_population
        else 0.0
    )
    top_food_shift = 0.0 if first_spatial["top_food_source"]["patch_id"] == second_spatial["top_food_source"]["patch_id"] else 1.0
    components = {
        "population_vector": population_distance,
        "unloads": _normalized_delta(
            _sum_metric(first_outcomes["unloads_by_colony"]),
            _sum_metric(second_outcomes["unloads_by_colony"]),
        ),
        "nest_food": _normalized_delta(
            _sum_metric(first_outcomes["nest_food_by_colony"]),
            _sum_metric(second_outcomes["nest_food_by_colony"]),
        ),
        "generation": _normalized_delta(first_outcomes["max_generation"], second_outcomes["max_generation"]),
        "trail_corridor": _normalized_delta(
            _spatial_value(first, "total_trail_cell_count"),
            _spatial_value(second, "total_trail_cell_count"),
        ),
        "lineages": _normalized_delta(first_outcomes["unique_lineage_count"], second_outcomes["unique_lineage_count"]),
        "residue": _normalized_delta(
            _spatial_value(first, "residue_total_value"),
            _spatial_value(second, "residue_total_value"),
        ),
        "corpse_events": _normalized_delta(
            _outcome_value(first, "corpse_create_count"),
            _outcome_value(second, "corpse_create_count"),
        ),
        "top_food_source_shift": top_food_shift,
    }
    distance_total = round(sum(components.values()) / max(1, len(components)), 4)
    return {
        "branch_a": first["provenance"]["branch_id"],
        "branch_b": second["provenance"]["branch_id"],
        "distance_total": distance_total,
        "components": components,
    }


def _family_branch_divergence(family: dict[str, object]) -> dict[str, object]:
    branches = list(family["branches"])
    distances = [
        _signature_distance(branches[idx], branches[jdx])
        for idx in range(len(branches))
        for jdx in range(idx + 1, len(branches))
    ]
    mean_distance = round(sum(item["distance_total"] for item in distances) / max(1, len(distances)), 4) if distances else 0.0
    max_distance = round(max((item["distance_total"] for item in distances), default=0.0), 4)
    population_vectors = {branch["provenance"]["branch_id"]: _population_vector(branch) for branch in branches}
    top_food_sources = {
        branch["provenance"]["branch_id"]: branch["spatial"]["top_food_source"]["patch_id"] or "none"
        for branch in branches
    }
    return {
        "pairwise_signature_distance": _metric(
            "available",
            family_id=family["family_id"],
            mean_distance=mean_distance,
            max_distance=max_distance,
            pairwise=distances,
        ),
        "final_population_vectors": _metric(
            "available",
            family_id=family["family_id"],
            values=population_vectors,
        ),
        "top_food_source_diversity": _metric(
            "proxy",
            family_id=family["family_id"],
            distinct_source_count=len(set(top_food_sources.values())),
            values=top_food_sources,
            reason="Only the top food source per branch is tracked in the current comparison layer.",
        ),
    }


def _family_niche_occupancy(family: dict[str, object]) -> dict[str, object]:
    branches = list(family["branches"])
    return {
        "occupied_resource_patches_proxy": _metric(
            "proxy",
            family_id=family["family_id"],
            distinct_top_sources=len({branch["spatial"]["top_food_source"]["patch_id"] or "none" for branch in branches}),
            values={
                branch["provenance"]["branch_id"]: branch["spatial"]["top_food_source"]["patch_id"] or "none"
                for branch in branches
            },
            reason="The current branch comparison tracks only dominant source identity, not full patch occupancy histories.",
        ),
        "used_corridors_proxy": _metric(
            "proxy",
            family_id=family["family_id"],
            values={
                branch["provenance"]["branch_id"]: branch["spatial"]["total_trail_cell_count"]
                for branch in branches
            },
            reason="Total trail cells are a corridor proxy rather than a true corridor count.",
        ),
        "substrate_bearing_cells": _metric(
            "available",
            family_id=family["family_id"],
            values={
                branch["provenance"]["branch_id"]: {
                    "residue_cell_count": _spatial_value(branch, "residue_cell_count"),
                    "corpse_count": _outcome_value(branch, "corpse_count"),
                }
                for branch in branches
            },
        ),
        "active_food_classes": _metric(
            "not_implemented",
            reason="Food classes are not implemented yet.",
        ),
        "corpse_use_events": _metric(
            "requires_m16",
            reason="No successor organism exists yet to consume corpse substrate.",
        ),
        "residue_use_events": _metric(
            "requires_m16",
            reason="No successor organism exists yet to exploit residue substrate directly.",
        ),
        "successor_occupied_zones": _metric(
            "requires_m16",
            reason="Successor life layers are not implemented yet.",
        ),
    }


def _family_stepping_stone_persistence(family: dict[str, object]) -> dict[str, object]:
    branches = list(family["branches"])
    return {
        "trail_corridor_persistence_proxy": _metric(
            "proxy",
            family_id=family["family_id"],
            values={
                branch["provenance"]["branch_id"]: {
                    "trail_cells": _spatial_value(branch, "total_trail_cell_count"),
                    "unloads": _sum_metric(branch["outcomes"]["unloads_by_colony"]),
                }
                for branch in branches
            },
            reason="Current persistence is inferred from final trail structure and completed unload loops, not full corridor lifetimes.",
        ),
        "residue_zone_persistence_proxy": _metric(
            "proxy",
            family_id=family["family_id"],
            values={
                branch["provenance"]["branch_id"]: {
                    "residue_cell_count": _spatial_value(branch, "residue_cell_count"),
                    "residue_total_value": _spatial_value(branch, "residue_total_value"),
                }
                for branch in branches
            },
            reason="Residue persistence is inferred from final residue maps rather than cell-by-cell time series.",
        ),
        "recurring_corpse_field_proxy": _metric(
            "proxy",
            family_id=family["family_id"],
            values={
                branch["provenance"]["branch_id"]: {
                    "corpse_create_count": _outcome_value(branch, "corpse_create_count"),
                    "corpse_expire_count": _outcome_value(branch, "corpse_expire_count"),
                    "corpse_count": _outcome_value(branch, "corpse_count"),
                }
                for branch in branches
            },
            reason="Corpse recurrence is inferred from create/expire counts rather than explicit spatial corpse clusters over time.",
        ),
        "stable_territory_partitions": _metric(
            "not_implemented",
            reason="Stable territory partitions are not tracked yet.",
        ),
        "successor_patch_persistence": _metric(
            "requires_m16",
            reason="Successor organism patches do not exist yet.",
        ),
    }


def _family_ecological_dependency(family: dict[str, object]) -> dict[str, object]:
    return {
        "dependency_edge_count": _metric(
            "requires_m16",
            reason="Dependency edges beyond substrate creation require successor life.",
        ),
        "maximum_dependency_depth": _metric(
            "requires_m16",
            reason="Dependency depth cannot be measured before successor life exists.",
        ),
        "dependency_events_by_type": _metric(
            "requires_m16",
            reason="No successor organism dependency events are emitted yet.",
        ),
        "future_dependency_graph": _metric(
            "requires_m16",
            family_id=family["family_id"],
            values=[
                {"from": "corpse", "to": "decomposer", "status": "requires_m16"},
                {"from": "residue", "to": "fungus", "status": "requires_m16"},
                {"from": "ant_transport", "to": "seed_patch", "status": "requires_m16"},
            ],
            reason="These edges are defined as the next dependency targets, not current implemented observations.",
        ),
    }


def _family_novelty_without_collapse(family: dict[str, object]) -> dict[str, object]:
    branches = list(family["branches"])
    return {
        "surviving_colony_counts": _metric(
            "available",
            family_id=family["family_id"],
            values={
                branch["provenance"]["branch_id"]: sum(
                    1 for value in branch["outcomes"]["alive_by_colony"].values() if int(value) > 0
                )
                for branch in branches
            },
        ),
        "noncollapse_branches": _metric(
            "available",
            family_id=family["family_id"],
            values={
                branch["provenance"]["branch_id"]: branch["outcomes"]["alive_total"] > 0
                and any(int(value) > 0 for value in branch["outcomes"]["alive_by_colony"].values())
                for branch in branches
            },
        ),
        "resource_loop_proxy": _metric(
            "proxy",
            family_id=family["family_id"],
            values={
                branch["provenance"]["branch_id"]: _sum_metric(branch["outcomes"]["unloads_by_colony"]) > 0
                and _spatial_value(branch, "total_trail_cell_count") > 0
                for branch in branches
            },
            reason="Resource loops are inferred from unload counts plus trail presence rather than explicit cycle detection.",
        ),
        "substrate_signal_proxy": _metric(
            "proxy",
            family_id=family["family_id"],
            values={
                branch["provenance"]["branch_id"]: (
                    _spatial_value(branch, "residue_cell_count") > 0
                    or _outcome_value(branch, "corpse_create_count") > 0
                )
                for branch in branches
            },
            reason="Substrate novelty is inferred from corpse/residue signals rather than explicit novelty search.",
        ),
        "branch_observability": _metric(
            "available",
            family_id=family["family_id"],
            values={
                branch["provenance"]["branch_id"]: bool(branch["provenance"]["checkpoint_path"])
                for branch in branches
            },
        ),
    }


def build_open_endedness_payload(comparison_payload: dict[str, object]) -> dict[str, object]:
    families = list(comparison_payload["families"])
    return {
        "comparison_id": comparison_payload["comparison_id"],
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_comparison": comparison_payload["comparison_id"],
        "caution": "These metrics organize divergence, occupancy, persistence, dependency, and collapse signals. They do not produce one universal fitness score.",
        "metric_families": {
            "branch_divergence": {
                "question": "Do forks from the same checkpoint develop different ecological histories?",
                "metrics": {
                    family["family_id"]: _family_branch_divergence(family)
                    for family in families
                },
            },
            "niche_occupancy": {
                "question": "Which ecological opportunities are being used?",
                "metrics": {
                    family["family_id"]: _family_niche_occupancy(family)
                    for family in families
                },
            },
            "stepping_stone_persistence": {
                "question": "Does a new structure last long enough to support later structures?",
                "metrics": {
                    family["family_id"]: _family_stepping_stone_persistence(family)
                    for family in families
                },
            },
            "ecological_dependency": {
                "question": "Does one process depend on another process created earlier?",
                "metrics": {
                    family["family_id"]: _family_ecological_dependency(family)
                    for family in families
                },
            },
            "novelty_without_collapse": {
                "question": "Does novelty coexist with sustained ecology?",
                "metrics": {
                    family["family_id"]: _family_novelty_without_collapse(family)
                    for family in families
                },
            },
        },
    }


def build_open_endedness_payload_from_checkpoints(checkpoint_paths: Iterable[str | Path]) -> dict[str, object]:
    comparison_payload = build_branch_comparison_payload(checkpoint_paths)
    return build_open_endedness_payload(comparison_payload)


def render_open_endedness_markdown(payload: dict[str, object]) -> str:
    lines = [
        f"# Open-Endedness Metrics {payload['comparison_id']}",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        f"Source comparison: `{payload['source_comparison']}`",
        "",
    ]
    for family_name, family_payload in payload["metric_families"].items():
        lines.extend([f"## {family_name.replace('_', ' ').title()}", "", family_payload["question"], ""])
        for family_id, metrics in family_payload["metrics"].items():
            lines.extend([f"### {family_id}", ""])
            for metric_name, metric in metrics.items():
                status = metric["status"]
                line = f"- `{metric_name}`: `{status}`"
                if "reason" in metric:
                    line += f" - {metric['reason']}"
                elif "mean_distance" in metric:
                    line += f" - mean distance `{metric['mean_distance']}`, max distance `{metric['max_distance']}`"
                elif "values" in metric:
                    if isinstance(metric["values"], dict):
                        line += f" - branches `{len(metric['values'])}`"
                    elif isinstance(metric["values"], list):
                        line += f" - entries `{len(metric['values'])}`"
                lines.append(line)
            lines.append("")
    lines.extend(["## Caution", "", payload["caution"], ""])
    return "\n".join(lines).rstrip() + "\n"


def write_open_endedness_report(output_dir: str | Path, payload: dict[str, object]) -> tuple[Path, Path]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    json_path = output_path / "metrics.json"
    markdown_path = output_path / "metrics.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    markdown_path.write_text(render_open_endedness_markdown(payload), encoding="utf-8")
    return json_path, markdown_path
