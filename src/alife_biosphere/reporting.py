from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from .events import Event
from .simulation import SimulationResult


@dataclass(frozen=True)
class OccupancyTransition:
    habitat_id: str
    tick: int
    occupancy: int
    previous_occupancy: int
    empty_duration_ticks: int | None = None

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "habitat_id": self.habitat_id,
            "tick": self.tick,
            "occupancy": self.occupancy,
            "previous_occupancy": self.previous_occupancy,
        }
        if self.empty_duration_ticks is not None:
            payload["empty_duration_ticks"] = self.empty_duration_ticks
        return payload


def _tick_summaries(events: list[Event]) -> list[Event]:
    return [event for event in events if event.event_type == "tick_summary"]


def _disturbances(events: list[Event]) -> list[Event]:
    return [event for event in events if event.event_type == "disturbance"]


def _moves(events: list[Event]) -> list[Event]:
    return [event for event in events if event.event_type == "move"]


def summarize_disturbance_recovery(
    result: SimulationResult,
    recolonization_window: int = 8,
) -> dict[str, object]:
    events = result.events
    tick_summaries = _tick_summaries(events)
    disturbances = _disturbances(events)
    move_events = _moves(events)
    if not tick_summaries:
        return {
            "disturbance_count": 0,
            "collapse_count": 0,
            "recolonization_count": 0,
            "disturbance_by_habitat": {},
            "disturbance_status_counts": {},
            "recovery_source_habitat_counts": {},
            "recovery_source_family_counts": {},
            "recovery_source_mode_counts": {},
            "collapse_events": [],
            "recolonization_events": [],
            "disturbance_summaries": [],
            "final_empty_habitats": [],
        }

    summary_by_tick = {event.tick: event.payload for event in tick_summaries}
    sorted_ticks = sorted(summary_by_tick)
    habitat_ids = sorted(next(iter(summary_by_tick.values()))["occupancy_by_habitat"])
    family_by_habitat = {
        habitat_id: habitat.habitat_family for habitat_id, habitat in result.world.habitats.items()
    }

    collapse_events: list[OccupancyTransition] = []
    recolonization_events: list[OccupancyTransition] = []
    collapse_lookup: dict[str, list[OccupancyTransition]] = {habitat_id: [] for habitat_id in habitat_ids}
    recol_lookup: dict[str, list[OccupancyTransition]] = {habitat_id: [] for habitat_id in habitat_ids}

    for habitat_id in habitat_ids:
        previous_tick = sorted_ticks[0]
        previous_occupancy = summary_by_tick[previous_tick]["occupancy_by_habitat"][habitat_id]
        empty_since_tick = None
        for tick in sorted_ticks[1:]:
            occupancy = summary_by_tick[tick]["occupancy_by_habitat"][habitat_id]
            if previous_occupancy > 0 and occupancy == 0:
                event = OccupancyTransition(
                    habitat_id=habitat_id,
                    tick=tick,
                    occupancy=occupancy,
                    previous_occupancy=previous_occupancy,
                )
                collapse_events.append(event)
                collapse_lookup[habitat_id].append(event)
                empty_since_tick = tick
            elif previous_occupancy == 0 and occupancy > 0:
                if empty_since_tick is not None:
                    event = OccupancyTransition(
                        habitat_id=habitat_id,
                        tick=tick,
                        occupancy=occupancy,
                        previous_occupancy=previous_occupancy,
                        empty_duration_ticks=tick - empty_since_tick,
                    )
                    recolonization_events.append(event)
                    recol_lookup[habitat_id].append(event)
                empty_since_tick = None
            previous_occupancy = occupancy

    status_counts: Counter[str] = Counter()
    lineage_recovery_mode_counts: Counter[str] = Counter()
    recovery_source_mode_counts: Counter[str] = Counter()
    recovery_source_habitat_counts: Counter[str] = Counter()
    recovery_source_family_counts: Counter[str] = Counter()
    disturbance_summaries: list[dict[str, object]] = []
    final_tick = sorted_ticks[-1]

    for disturbance in disturbances:
        habitat_id = disturbance.habitat_id
        assert habitat_id is not None
        pre_tick = max((tick for tick in sorted_ticks if tick < disturbance.tick), default=sorted_ticks[0])
        pre_occupancy = summary_by_tick[pre_tick]["occupancy_by_habitat"][habitat_id]
        post_occupancy = summary_by_tick[disturbance.tick]["occupancy_by_habitat"][habitat_id]
        pre_lineages = set(summary_by_tick[pre_tick]["lineages_by_habitat"][habitat_id])
        collapse = next(
            (
                event
                for event in collapse_lookup[habitat_id]
                if disturbance.tick <= event.tick <= min(final_tick, disturbance.tick + recolonization_window)
            ),
            None,
        )
        delayed_recovery = None
        recovery = None
        if collapse is not None:
            recovery = next(
                (
                    event
                    for event in recol_lookup[habitat_id]
                    if event.tick > collapse.tick and event.tick <= min(final_tick, disturbance.tick + recolonization_window)
                ),
                None,
            )
            delayed_recovery = next(
                (
                    event
                    for event in recol_lookup[habitat_id]
                    if event.tick > collapse.tick and event.tick > min(final_tick, disturbance.tick + recolonization_window)
                ),
                None,
            )
        if collapse is None and pre_occupancy == 0 and post_occupancy == 0:
            status = "already_empty"
        elif collapse is None:
            status = "occupied_after_disturbance"
        elif recovery is not None:
            status = "collapsed_and_recovered"
        elif delayed_recovery is not None:
            status = "collapsed_delayed_recovery"
        else:
            status = "collapsed_unrecovered"
        status_counts[status] += 1
        effective_recovery = recovery or delayed_recovery
        recovery_lineages = (
            set(summary_by_tick[effective_recovery.tick]["lineages_by_habitat"][habitat_id])
            if effective_recovery is not None
            else set()
        )
        shared_lineages = sorted(pre_lineages & recovery_lineages)
        replacement_lineages = sorted(recovery_lineages - pre_lineages)
        if effective_recovery is None:
            lineage_recovery_mode = None
        elif shared_lineages and replacement_lineages:
            lineage_recovery_mode = "mixed_recovery"
        elif shared_lineages:
            lineage_recovery_mode = "same_lineage_return"
        elif recovery_lineages:
            lineage_recovery_mode = "replacement_recovery"
        else:
            lineage_recovery_mode = "empty_recovery"
        if lineage_recovery_mode is not None:
            lineage_recovery_mode_counts[lineage_recovery_mode] += 1
        source_move_events = []
        if effective_recovery is not None:
            source_move_events = [
                event
                for event in move_events
                if event.tick == effective_recovery.tick and event.habitat_id == habitat_id
            ]
        source_habitats = sorted(
            {
                str(event.payload["from_habitat_id"])
                for event in source_move_events
                if "from_habitat_id" in event.payload
            }
        )
        source_families = sorted({family_by_habitat[source_habitat] for source_habitat in source_habitats})
        source_lineages = sorted(
            {
                result.world.organisms[event.organism_id].lineage_id
                for event in source_move_events
                if event.organism_id is not None and event.organism_id in result.world.organisms
            }
        )
        if effective_recovery is None:
            recovery_source_mode = None
        elif not source_habitats:
            recovery_source_mode = "unknown_source"
        elif len(source_habitats) == 1:
            recovery_source_mode = "single_habitat_source"
        else:
            recovery_source_mode = "multi_habitat_source"
        if recovery_source_mode is not None:
            recovery_source_mode_counts[recovery_source_mode] += 1
        for source_habitat in source_habitats:
            recovery_source_habitat_counts[source_habitat] += 1
            recovery_source_family_counts[family_by_habitat[source_habitat]] += 1
        disturbance_summaries.append(
            {
                "tick": disturbance.tick,
                "habitat_id": habitat_id,
                "habitat_family": family_by_habitat[habitat_id],
                "resource_loss": disturbance.payload.get("resource_loss"),
                "hazard_pulse": disturbance.payload.get("hazard_pulse"),
                "pre_occupancy": pre_occupancy,
                "post_occupancy": post_occupancy,
                "pre_lineages": sorted(pre_lineages),
                "status": status,
                "collapse_tick": collapse.tick if collapse else None,
                "recovery_tick": recovery.tick if recovery else None,
                "delayed_recovery_tick": delayed_recovery.tick if delayed_recovery else None,
                "lineage_recovery_mode": lineage_recovery_mode,
                "recovery_lineages": sorted(recovery_lineages),
                "shared_lineages": shared_lineages,
                "replacement_lineages": replacement_lineages,
                "recovery_source_mode": recovery_source_mode,
                "source_habitats": source_habitats,
                "source_families": source_families,
                "source_lineages": source_lineages,
            }
        )

    disturbance_by_habitat = Counter(event.habitat_id for event in disturbances if event.habitat_id is not None)
    final_empty_habitats = [
        habitat_id
        for habitat_id, occupancy in summary_by_tick[final_tick]["occupancy_by_habitat"].items()
        if occupancy == 0
    ]
    longest_empty_span_by_habitat: dict[str, int] = {}
    for habitat_id in habitat_ids:
        longest = 0
        current = 0
        for tick in sorted_ticks:
            occupancy = summary_by_tick[tick]["occupancy_by_habitat"][habitat_id]
            if occupancy == 0:
                current += 1
                longest = max(longest, current)
            else:
                current = 0
        longest_empty_span_by_habitat[habitat_id] = longest

    return {
        "disturbance_count": len(disturbances),
        "collapse_count": len(collapse_events),
        "recolonization_count": len(recolonization_events),
        "successful_recovery_count": status_counts["collapsed_and_recovered"],
        "failed_recovery_count": status_counts["collapsed_unrecovered"],
        "delayed_recovery_count": status_counts["collapsed_delayed_recovery"],
        "disturbance_by_habitat": dict(disturbance_by_habitat),
        "disturbance_status_counts": dict(status_counts),
        "lineage_recovery_mode_counts": dict(lineage_recovery_mode_counts),
        "recovery_source_habitat_counts": dict(recovery_source_habitat_counts),
        "recovery_source_family_counts": dict(recovery_source_family_counts),
        "recovery_source_mode_counts": dict(recovery_source_mode_counts),
        "collapse_events": [event.to_dict() for event in collapse_events],
        "recolonization_events": [event.to_dict() for event in recolonization_events],
        "disturbance_summaries": disturbance_summaries,
        "final_empty_habitats": final_empty_habitats,
        "longest_empty_span_by_habitat": longest_empty_span_by_habitat,
    }


def summarize_source_sink_roles(
    results: list[SimulationResult],
    recolonization_window: int = 8,
) -> dict[str, object]:
    if not results:
        return {
            "run_count": 0,
            "per_habitat": {},
            "per_family": {},
            "top_source_habitats": [],
            "top_sink_habitats": [],
        }

    family_by_habitat = {
        habitat_id: habitat.habitat_family
        for habitat_id, habitat in results[0].world.habitats.items()
    }
    habitat_ids = sorted(family_by_habitat)
    source_counts: Counter[str] = Counter()
    disturbance_target_counts: Counter[str] = Counter()
    sink_collapse_counts: Counter[str] = Counter()
    sink_recovery_counts: Counter[str] = Counter()
    sink_failure_counts: Counter[str] = Counter()
    already_empty_target_counts: Counter[str] = Counter()

    for result in results:
        recovery_summary = summarize_disturbance_recovery(
            result,
            recolonization_window=recolonization_window,
        )
        for habitat_id, count in recovery_summary["disturbance_by_habitat"].items():
            disturbance_target_counts[habitat_id] += int(count)
        for item in recovery_summary["disturbance_summaries"]:
            habitat_id = str(item["habitat_id"])
            status = str(item["status"])
            if status in {"collapsed_and_recovered", "collapsed_delayed_recovery", "collapsed_unrecovered"}:
                sink_collapse_counts[habitat_id] += 1
            if status in {"collapsed_and_recovered", "collapsed_delayed_recovery"}:
                sink_recovery_counts[habitat_id] += 1
            if status == "collapsed_unrecovered":
                sink_failure_counts[habitat_id] += 1
            if status == "already_empty":
                already_empty_target_counts[habitat_id] += 1
            for source_habitat in item["source_habitats"]:
                source_counts[str(source_habitat)] += 1

    per_habitat: dict[str, dict[str, object]] = {}
    family_source_counts: Counter[str] = Counter()
    family_sink_counts: Counter[str] = Counter()
    family_recovery_counts: Counter[str] = Counter()

    for habitat_id in habitat_ids:
        family = family_by_habitat[habitat_id]
        source_recovery_count = source_counts[habitat_id]
        sink_collapse_count = sink_collapse_counts[habitat_id]
        sink_recovery_count = sink_recovery_counts[habitat_id]
        sink_failure_count = sink_failure_counts[habitat_id]
        disturbance_target_count = disturbance_target_counts[habitat_id]
        already_empty_target_count = already_empty_target_counts[habitat_id]
        balance = source_recovery_count - sink_collapse_count
        if source_recovery_count > sink_collapse_count:
            dominant_role = "source_leaning"
        elif sink_collapse_count > source_recovery_count:
            dominant_role = "sink_leaning"
        elif source_recovery_count == 0 and sink_collapse_count == 0:
            dominant_role = "inactive"
        else:
            dominant_role = "balanced"
        recovery_ratio = (
            0.0
            if sink_collapse_count == 0
            else round(sink_recovery_count / sink_collapse_count, 4)
        )
        per_habitat[habitat_id] = {
            "habitat_family": family,
            "source_recovery_count": source_recovery_count,
            "disturbance_target_count": disturbance_target_count,
            "sink_collapse_count": sink_collapse_count,
            "sink_recovery_count": sink_recovery_count,
            "sink_failure_count": sink_failure_count,
            "already_empty_target_count": already_empty_target_count,
            "source_sink_balance": balance,
            "sink_recovery_ratio": recovery_ratio,
            "dominant_role": dominant_role,
        }
        family_source_counts[family] += source_recovery_count
        family_sink_counts[family] += sink_collapse_count
        family_recovery_counts[family] += sink_recovery_count

    per_family: dict[str, dict[str, object]] = {}
    for family in sorted(set(family_by_habitat.values())):
        source_recovery_count = family_source_counts[family]
        sink_collapse_count = family_sink_counts[family]
        sink_recovery_count = family_recovery_counts[family]
        if source_recovery_count > sink_collapse_count:
            dominant_role = "source_leaning"
        elif sink_collapse_count > source_recovery_count:
            dominant_role = "sink_leaning"
        elif source_recovery_count == 0 and sink_collapse_count == 0:
            dominant_role = "inactive"
        else:
            dominant_role = "balanced"
        per_family[family] = {
            "source_recovery_count": source_recovery_count,
            "sink_collapse_count": sink_collapse_count,
            "sink_recovery_count": sink_recovery_count,
            "source_sink_balance": source_recovery_count - sink_collapse_count,
            "dominant_role": dominant_role,
        }

    top_source_habitats = sorted(
        (
            {
                "habitat_id": habitat_id,
                "count": values["source_recovery_count"],
                "habitat_family": values["habitat_family"],
            }
            for habitat_id, values in per_habitat.items()
            if values["source_recovery_count"] > 0
        ),
        key=lambda item: (-int(item["count"]), str(item["habitat_id"])),
    )
    top_sink_habitats = sorted(
        (
            {
                "habitat_id": habitat_id,
                "count": values["sink_collapse_count"],
                "habitat_family": values["habitat_family"],
            }
            for habitat_id, values in per_habitat.items()
            if values["sink_collapse_count"] > 0
        ),
        key=lambda item: (-int(item["count"]), str(item["habitat_id"])),
    )

    return {
        "run_count": len(results),
        "per_habitat": per_habitat,
        "per_family": per_family,
        "top_source_habitats": top_source_habitats,
        "top_sink_habitats": top_sink_habitats,
    }


def summarize_habitat_memory(result: SimulationResult) -> dict[str, object]:
    tick_summaries = _tick_summaries(result.events)
    if not tick_summaries:
        return {
            "per_habitat": {},
            "top_memory_habitats": [],
            "top_recovery_lag_habitats": [],
        }

    habitat_ids = sorted(tick_summaries[0].payload["memory_field_by_habitat"])
    per_habitat: dict[str, dict[str, object]] = {}
    for habitat_id in habitat_ids:
        memory_series = [event.payload["memory_field_by_habitat"][habitat_id] for event in tick_summaries]
        recovery_series = [event.payload["recovery_lag_by_habitat"][habitat_id] for event in tick_summaries]
        hazard_series = [event.payload["hazard_by_habitat"][habitat_id] for event in tick_summaries]
        regen_series = [event.payload["regeneration_by_habitat"][habitat_id] for event in tick_summaries]
        occupancy_series = [event.payload["occupancy_by_habitat"][habitat_id] for event in tick_summaries]
        per_habitat[habitat_id] = {
            "final_memory_field": round(memory_series[-1], 4),
            "peak_memory_field": round(max(memory_series), 4),
            "max_recovery_lag": max(recovery_series),
            "final_hazard": round(hazard_series[-1], 4),
            "peak_hazard": round(max(hazard_series), 4),
            "final_regeneration": round(regen_series[-1], 4),
            "min_regeneration": round(min(regen_series), 4),
            "occupied_ticks": sum(1 for value in occupancy_series if value > 0),
            "empty_ticks": sum(1 for value in occupancy_series if value == 0),
        }

    top_memory_habitats = sorted(
        (
            {
                "habitat_id": habitat_id,
                "peak_memory_field": values["peak_memory_field"],
            }
            for habitat_id, values in per_habitat.items()
        ),
        key=lambda item: (-float(item["peak_memory_field"]), str(item["habitat_id"])),
    )
    top_recovery_lag_habitats = sorted(
        (
            {
                "habitat_id": habitat_id,
                "max_recovery_lag": values["max_recovery_lag"],
            }
            for habitat_id, values in per_habitat.items()
        ),
        key=lambda item: (-int(item["max_recovery_lag"]), str(item["habitat_id"])),
    )
    return {
        "per_habitat": per_habitat,
        "top_memory_habitats": top_memory_habitats,
        "top_recovery_lag_habitats": top_recovery_lag_habitats,
    }
