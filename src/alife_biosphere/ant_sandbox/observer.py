from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .checkpoint import load_checkpoint
from .config import AntSandboxConfig
from .simulation import step_world
from .world import AntSandboxWorld, initialize_world, terrain_kind


def _trail_points(field: dict[tuple[int, int], float], minimum: float = 0.04) -> list[dict[str, float]]:
    return [
        {"x": float(x), "y": float(y), "value": round(value, 4)}
        for (x, y), value in sorted(field.items())
        if value >= minimum
    ]


def _trail_layers(
    fields: dict[str, dict[tuple[int, int], float]],
    colonies: dict[str, object],
    minimum: float = 0.04,
) -> list[dict[str, object]]:
    layers: list[dict[str, object]] = []
    for colony_id, field in fields.items():
        colony = colonies[colony_id]
        layers.append(
            {
                "colony_id": colony_id,
                "color": colony.color,
                "points": _trail_points(field, minimum=minimum),
            }
        )
    return layers


def _terrain_points(world: AntSandboxWorld) -> list[dict[str, object]]:
    return [
        {"x": x, "y": y, "kind": kind}
        for (x, y), kind in sorted(world.terrain.items(), key=lambda item: (item[0][1], item[0][0]))
    ]


def _corpse_points(world: AntSandboxWorld) -> list[dict[str, object]]:
    return [
        {
            "corpse_id": corpse.corpse_id,
            "x": corpse.x,
            "y": corpse.y,
            "colony_id": corpse.colony_id,
            "death_tick": corpse.death_tick,
            "energy_value": round(corpse.energy_value, 4),
            "decay_ticks_remaining": corpse.decay_ticks_remaining,
            "death_reason": corpse.death_reason,
        }
        for corpse in world.corpses
    ]


def _decomposer_points(world: AntSandboxWorld) -> list[dict[str, object]]:
    return [
        {
            "patch_id": patch.patch_id,
            "x": patch.x,
            "y": patch.y,
            "biomass": round(patch.biomass, 4),
            "age": patch.age,
            "source_corpse_id": patch.source_corpse_id,
            "source_type": patch.source_type,
            "spread_count": patch.spread_count,
        }
        for patch in world.decomposer_patches
    ]


def _residue_points(world: AntSandboxWorld, minimum: float = 0.03) -> list[dict[str, object]]:
    return [
        {
            "x": x,
            "y": y,
            "value": round(float(entry["value"]), 4),
            "source_type": str(entry.get("source_type", "unknown")),
            "enriched": bool(entry.get("enriched", False)),
        }
        for (x, y), entry in sorted(world.residue_field.items(), key=lambda item: (item[0][1], item[0][0]))
        if float(entry["value"]) >= minimum
    ]


def _event_dicts(world: AntSandboxWorld, tick: int, event_type: str) -> list[dict[str, object]]:
    return [
        event.to_dict()
        for event in world.events
        if event.tick == tick and event.event_type == event_type
    ]


def _quiet_summary(world: AntSandboxWorld, tick: int) -> dict[str, int]:
    return {
        "ticks": tick,
        "alive": world.alive_count(),
        "carrying": world.carrying_count(),
        "nest_food": world.delivered_food_total(),
        "food_remaining": world.food_remaining(),
        "events": len(world.events),
        "moves": 0,
        "pickups": 0,
        "unloads": 0,
        "births": 0,
        "deaths": 0,
        "feeds": 0,
        "upkeep": 0,
        "food_reseeds": 0,
        "contested_sources": 0,
        "hostility_contacts": 0,
        "combat_starts": 0,
        "combat_pairs": 0,
        "frozen_ants": 0,
        "contest_entries": 0,
        "contesting_ants": sum(1 for ant in world.ants if ant.alive and ant.behavior_state == "contest"),
        "avoidance_turns": sum(1 for ant in world.ants if ant.alive and ant.behavior_state == "avoid"),
        "hungry_ants": sum(1 for ant in world.ants if ant.alive and ant.behavior_state == "hungry"),
        "corpse_count": world.corpse_count(),
        "decomposer_patch_count": world.decomposer_patch_count(),
        "residue_cell_count": world.residue_cell_count(),
        "residue_total_value": world.residue_total_value(),
        "enriched_residue_cell_count": world.enriched_residue_cell_count(),
        "max_source_pressure": round(max((patch.competition_pressure for patch in world.food_patches), default=0.0), 4),
        "food_trail_cells": sum(len(field) for field in world.food_trail.values()),
        "home_trail_cells": sum(len(field) for field in world.home_trail.values()),
    }


def _summary_for_tick(world: AntSandboxWorld, tick: int) -> dict[str, int]:
    for event in reversed(world.events):
        if event.tick == tick and event.event_type == "tick_summary":
            return dict(event.payload)
        if event.tick < tick:
            break
    return _quiet_summary(world, tick)


def _frame_payload(world: AntSandboxWorld, summary: dict[str, int], tick: int) -> dict[str, object]:
    ants = [
        {
            "ant_id": ant.ant_id,
            "colony_id": ant.colony_id,
            "x": ant.x,
            "y": ant.y,
            "heading": ant.heading,
            "terrain_kind": terrain_kind(world, ant.x, ant.y),
            "carrying_food": ant.carrying_food,
            "target_patch_id": ant.target_patch_id,
            "behavior_state": ant.behavior_state,
            "contest_patch_id": ant.contest_patch_id,
            "outbound_commit_ticks": ant.outbound_commit_ticks,
            "in_combat": ant.combat_ticks_remaining > 0,
            "combat_ticks_remaining": ant.combat_ticks_remaining,
            "combat_with_id": ant.combat_with_id,
            "combat_cooldown_ticks": ant.combat_cooldown_ticks,
            "energy": round(ant.energy, 3),
            "starvation_ticks": ant.starvation_ticks,
            "delivered_food": ant.delivered_food,
            "age": ant.age,
            "birth_tick": ant.birth_tick,
            "parent_id": ant.parent_id,
            "lineage_id": ant.lineage_id,
            "genome_id": ant.genome_id,
            "parent_genome_id": ant.parent_genome_id,
            "generation": ant.generation,
            "mutation_count": ant.mutation_count,
            "mutation_log": list(ant.mutation_log),
            "range_bias": ant.range_bias,
            "trail_affinity": ant.trail_affinity,
            "harvest_drive": ant.harvest_drive,
        }
        for ant in world.ants
        if ant.alive
    ]
    food_patches = [
        {
            "patch_id": patch.patch_id,
            "x": patch.x,
            "y": patch.y,
            "radius": patch.radius,
            "amount": patch.amount,
            "max_amount": patch.max_amount,
            "value_score": patch.value_score,
            "nearby_ants": patch.nearby_ants,
            "carrying_nearby": patch.carrying_nearby,
            "competition_pressure": patch.competition_pressure,
            "contested_ticks": patch.contested_ticks,
            "depletion_count": patch.depletion_count,
        }
        for patch in world.food_patches
    ]
    birth_events = _event_dicts(world, tick, "ant_birth")
    death_events = _event_dicts(world, tick, "ant_death")
    colony_stats = [
        {
            "colony_id": colony.colony_id,
            "display_name": colony.display_name,
            "color": colony.color,
            "alive": world.alive_count_for_colony(colony.colony_id),
            "carrying": sum(1 for ant in world.ants if ant.alive and ant.colony_id == colony.colony_id and ant.carrying_food),
            "births": sum(1 for event in birth_events if event["payload"].get("colony_id") == colony.colony_id),
            "deaths": sum(1 for event in death_events if event["payload"].get("colony_id") == colony.colony_id),
            "nest_food": colony.nest.stored_food,
        }
        for colony in world.colonies.values()
    ]
    return {
        "tick": tick,
        "alive": summary["alive"],
        "carrying": summary["carrying"],
        "nest_food": summary["nest_food"],
        "food_remaining": summary["food_remaining"],
        "moves": summary["moves"],
        "pickups": summary["pickups"],
        "unloads": summary["unloads"],
        "births": summary["births"],
        "deaths": summary["deaths"],
        "combat_starts": summary["combat_starts"],
        "combat_pairs": summary["combat_pairs"],
        "frozen_ants": summary["frozen_ants"],
        "contest_entries": summary["contest_entries"],
        "contesting_ants": summary["contesting_ants"],
        "avoidance_turns": summary["avoidance_turns"],
        "hungry_ants": summary["hungry_ants"],
        "corpse_count": summary.get("corpse_count", world.corpse_count()),
        "decomposer_patch_count": summary.get("decomposer_patch_count", world.decomposer_patch_count()),
        "residue_cell_count": summary.get("residue_cell_count", world.residue_cell_count()),
        "residue_total_value": summary.get("residue_total_value", world.residue_total_value()),
        "enriched_residue_cell_count": summary.get("enriched_residue_cell_count", world.enriched_residue_cell_count()),
        "ants": ants,
        "corpses": _corpse_points(world),
        "decomposer_patches": _decomposer_points(world),
        "residue_points": _residue_points(world),
        "food_patches": food_patches,
        "colony_stats": colony_stats,
        "food_trail_layers": _trail_layers(world.food_trail, world.colonies),
        "home_trail_layers": _trail_layers(world.home_trail, world.colonies),
        "birth_events": birth_events,
        "death_events": death_events,
        "pickup_events": _event_dicts(world, tick, "food_pickup"),
        "unload_events": _event_dicts(world, tick, "food_unload"),
        "reseed_events": _event_dicts(world, tick, "food_patch_reseed"),
        "upkeep_events": _event_dicts(world, tick, "nest_upkeep"),
        "contested_source_events": _event_dicts(world, tick, "food_source_contested"),
        "depleted_source_events": _event_dicts(world, tick, "food_source_depleted"),
        "combat_start_events": _event_dicts(world, tick, "combat_start"),
        "combat_end_events": _event_dicts(world, tick, "combat_end"),
        "contest_entry_events": _event_dicts(world, tick, "contest_entry"),
    }


def _observer_payload(
    config: AntSandboxConfig,
    world: AntSandboxWorld,
    frames: list[dict[str, object]],
    *,
    title: str,
    total_ticks: int,
    generated_at: str,
    extra: dict[str, object] | None = None,
) -> dict[str, object]:
    payload = {
        "title": title,
        "generated_at": generated_at,
        "width": config.width,
        "height": config.height,
        "total_ticks": total_ticks,
        "terrain": _terrain_points(world),
        "nest": {
            "x": world.nest.x,
            "y": world.nest.y,
            "radius": world.nest.radius,
        },
        "colonies": [
            {
                "colony_id": colony.colony_id,
                "display_name": colony.display_name,
                "color": colony.color,
                "nest": {
                    "x": colony.nest.x,
                    "y": colony.nest.y,
                    "radius": colony.nest.radius,
                    "stored_food": colony.nest.stored_food,
                },
            }
            for colony in world.colonies.values()
        ],
        "frames": frames,
    }
    if extra:
        payload.update(extra)
    return payload


def build_ant_replay_observer_payload(
    config: AntSandboxConfig,
    world: AntSandboxWorld,
    *,
    title: str = "Ant Sandbox World",
    target_tick: int | None = None,
    include_loaded_frame: bool = True,
    extra: dict[str, object] | None = None,
) -> dict[str, object]:
    loaded_tick = world.tick
    final_tick = loaded_tick if target_tick is None else target_tick
    if final_tick < loaded_tick:
        raise ValueError("target_tick must be greater than or equal to the current world tick")

    frames: list[dict[str, object]] = []
    if include_loaded_frame:
        frames.append(_frame_payload(world, _summary_for_tick(world, loaded_tick), loaded_tick))
    for tick in range(loaded_tick + 1, final_tick + 1):
        summary = step_world(world, config, tick)
        frames.append(_frame_payload(world, summary, tick))

    merged_extra = {
        "loaded_tick": loaded_tick,
        "target_tick": final_tick,
        "config_seed": config.seed,
        "config_inheritance_mode": config.ants.inheritance_mode,
        "config_mutation_rate": config.ants.mutation_rate,
    }
    if extra:
        merged_extra.update(extra)
    return _observer_payload(
        config,
        world,
        frames,
        title=title,
        total_ticks=final_tick,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        extra=merged_extra,
    )


def build_ant_observer_payload(
    config: AntSandboxConfig,
    title: str = "Ant Sandbox World",
    extra: dict[str, object] | None = None,
) -> dict[str, object]:
    return build_ant_replay_observer_payload(
        config,
        initialize_world(config),
        title=title,
        target_tick=config.ticks,
        include_loaded_frame=False,
        extra=extra,
    )


def build_ant_checkpoint_observer_payload(
    checkpoint_path: str | Path,
    *,
    title: str = "Ant Sandbox Branch",
    target_tick: int | None = None,
) -> dict[str, object]:
    checkpoint_file = Path(checkpoint_path).resolve()
    checkpoint = load_checkpoint(checkpoint_file)
    config = checkpoint.config
    world = checkpoint.world
    loaded_tick = world.tick
    final_tick = loaded_tick if target_tick is None else target_tick
    return build_ant_replay_observer_payload(
        config,
        world,
        title=title,
        target_tick=final_tick,
        include_loaded_frame=True,
        extra={
            "source_checkpoint": str(checkpoint_file),
            "checkpoint_metadata": dict(checkpoint.metadata),
            "replayed_from_checkpoint": final_tick > loaded_tick,
        },
    )


def _html_shell(data_json: str, title: str, auto_reload_ms: int | None = None) -> str:
    live_reload_script = (
        f"if (data.live && !data.complete) {{ setTimeout(() => location.reload(), {auto_reload_ms}); }}"
        if auto_reload_ms is not None
        else ""
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{
      --bg: #f7f0e8;
      --panel: rgba(255, 250, 244, 0.84);
      --ink: #1f1a15;
      --muted: #6f665c;
      --soil: #e7d7c0;
      --nest: #7e5e42;
      --food: #98b85f;
      --food-glow: rgba(152, 184, 95, 0.28);
      --food-trail: rgba(64, 163, 120, 0.28);
      --home-trail: rgba(217, 153, 72, 0.22);
      --ant: #2c241d;
      --ant-carry: #d8893c;
      --contest: rgba(181, 72, 43, 0.9);
      --avoid: rgba(55, 90, 127, 0.78);
      --hungry: rgba(189, 142, 49, 0.85);
      --dense-grass: rgba(106, 141, 84, 0.42);
      --sand: rgba(214, 184, 129, 0.44);
      --rock: rgba(92, 86, 81, 0.78);
      --birth: rgba(51, 165, 116, 0.9);
      --death: rgba(156, 52, 43, 0.86);
      --corpse: rgba(101, 55, 44, 0.94);
      --decomposer: rgba(88, 129, 74, 0.94);
      --residue-trail: rgba(74, 132, 115, 0.18);
      --residue-nest: rgba(182, 126, 58, 0.22);
      --residue-corpse: rgba(132, 66, 56, 0.24);
      --residue-decomposer: rgba(79, 141, 91, 0.26);
      --shadow: 0 18px 48px rgba(35, 26, 17, 0.12);
      --accent: #26493b;
    }}

    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background:
        radial-gradient(circle at top left, rgba(152,184,95,0.12), transparent 26%),
        radial-gradient(circle at top right, rgba(216,137,60,0.10), transparent 22%),
        linear-gradient(180deg, #f9f3eb 0%, #efe2d2 100%);
      color: var(--ink);
      font-family: "Avenir Next", "Segoe UI", "Helvetica Neue", sans-serif;
    }}

    .shell {{
      min-height: 100vh;
      display: flex;
      gap: 18px;
      padding: 18px;
    }}

    .world, .panel {{
      border-radius: 26px;
      box-shadow: var(--shadow);
      background: var(--panel);
      border: 1px solid rgba(52, 39, 26, 0.08);
      backdrop-filter: blur(10px);
    }}

    .world {{
      flex: 1;
      padding: 18px;
      background:
        radial-gradient(circle at top, rgba(255,255,255,0.62), transparent 44%),
        linear-gradient(180deg, rgba(252, 246, 239, 0.95), rgba(245, 235, 224, 0.96));
    }}

    .panel {{
      width: 320px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}

    h1 {{
      margin: 0 0 6px;
      font-size: 34px;
      line-height: 1;
      letter-spacing: 0.01em;
      font-family: "Avenir Next Condensed", "Helvetica Neue", sans-serif;
    }}

    .sub {{
      margin: 0 0 14px;
      font-size: 14px;
      color: var(--muted);
    }}

    .meta {{
      margin: 0 0 12px;
      font-size: 12px;
      color: var(--muted);
      font-family: "SF Mono", "Menlo", "Consolas", monospace;
    }}

    .controls {{
      display: flex;
      gap: 10px;
      align-items: center;
      flex-wrap: wrap;
      margin-bottom: 12px;
    }}

    button {{
      appearance: none;
      border: 0;
      border-radius: 999px;
      background: var(--accent);
      color: #f7f4ee;
      padding: 10px 16px;
      font-size: 13px;
      font-family: "SF Mono", "Menlo", "Consolas", monospace;
      cursor: pointer;
    }}

    button.secondary {{
      background: rgba(38, 73, 59, 0.1);
      color: var(--accent);
    }}

    input[type="range"] {{
      flex: 1;
      min-width: 200px;
      accent-color: var(--accent);
    }}

    .tick {{
      font-family: "SF Mono", "Menlo", "Consolas", monospace;
      color: var(--muted);
      font-size: 13px;
    }}

    .legend {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-bottom: 10px;
      font-size: 12px;
      color: var(--muted);
      font-family: "SF Mono", "Menlo", "Consolas", monospace;
    }}

    .legend span {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}

    .dot {{
      width: 10px;
      height: 10px;
      border-radius: 999px;
      display: inline-block;
    }}

    canvas {{
      width: 100%;
      max-height: calc(100vh - 170px);
      aspect-ratio: 4 / 3;
      border-radius: 22px;
      background:
        radial-gradient(circle at top, rgba(255,255,255,0.42), transparent 44%),
        linear-gradient(180deg, rgba(255,252,247,0.92), rgba(241, 228, 211, 0.96));
    }}

    .cards {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }}

    .card {{
      border-radius: 18px;
      padding: 12px;
      background: rgba(250, 245, 238, 0.9);
      border: 1px solid rgba(48, 36, 25, 0.08);
    }}

    .card h3 {{
      margin: 0 0 8px;
      font-size: 13px;
      color: var(--muted);
      font-family: "SF Mono", "Menlo", "Consolas", monospace;
      font-weight: 600;
    }}

    .card strong {{
      display: block;
      font-size: 26px;
      line-height: 1;
    }}

    .section {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .section h2 {{
      margin: 0;
      font-size: 14px;
      font-family: "SF Mono", "Menlo", "Consolas", monospace;
      color: var(--muted);
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}

    .log {{
      display: flex;
      flex-direction: column;
      gap: 8px;
      max-height: 230px;
      overflow: auto;
      padding-right: 4px;
    }}

    .log-row {{
      border-radius: 14px;
      padding: 10px 12px;
      background: rgba(250, 245, 238, 0.9);
      border: 1px solid rgba(48, 36, 25, 0.08);
      font-size: 13px;
      line-height: 1.35;
    }}

    .selected-ant {{
      border-radius: 16px;
      padding: 12px;
      background: rgba(250, 245, 238, 0.9);
      border: 1px solid rgba(48, 36, 25, 0.08);
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    .tiny {{
      font-size: 11px;
      color: var(--muted);
      font-family: "SF Mono", "Menlo", "Consolas", monospace;
    }}

    @media (max-width: 980px) {{
      .shell {{
        flex-direction: column;
      }}
      .panel {{
        width: 100%;
      }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <section class="world">
      <h1>{title}</h1>
      <p class="sub">A colony window that prioritizes nest, food, ants, and trace flow over dashboard metrics.</p>
      <p class="meta" id="generated-at"></p>
      <div class="controls">
        <button id="play">Play</button>
        <button id="back" class="secondary">Back</button>
        <button id="forward" class="secondary">Forward</button>
        <input id="timeline" type="range" min="1" max="1" value="1">
        <span class="tick" id="tick-label"></span>
      </div>
      <div class="legend">
        <span><i class="dot" style="background: var(--dense-grass)"></i>dense grass</span>
        <span><i class="dot" style="background: var(--sand)"></i>sand</span>
        <span><i class="dot" style="background: var(--rock)"></i>rock</span>
        <span><i class="dot" style="background: var(--nest)"></i>nest</span>
        <span><i class="dot" style="background: var(--food)"></i>food</span>
        <span><i class="dot" style="background: var(--ant)"></i>ant</span>
        <span><i class="dot" style="background: var(--ant-carry)"></i>carrying food</span>
        <span><i class="dot" style="background: var(--contest)"></i>contest</span>
        <span><i class="dot" style="background: var(--avoid)"></i>avoid</span>
        <span><i class="dot" style="background: var(--hungry)"></i>hungry</span>
        <span><i class="dot" style="background: rgba(173, 48, 48, 0.9)"></i>combat</span>
        <span><i class="dot" style="background: var(--food-trail)"></i>food trail</span>
        <span><i class="dot" style="background: var(--home-trail)"></i>home trail</span>
        <span><i class="dot" style="background: var(--corpse)"></i>corpse</span>
        <span><i class="dot" style="background: var(--decomposer)"></i>decomposer</span>
        <span><i class="dot" style="background: var(--residue-corpse)"></i>residue</span>
      </div>
      <canvas id="world" width="960" height="720"></canvas>
    </section>
    <aside class="panel">
      <div class="cards">
        <div class="card"><h3>Alive</h3><strong id="alive"></strong></div>
        <div class="card"><h3>Nest Food</h3><strong id="nest-food"></strong></div>
        <div class="card"><h3>Carrying</h3><strong id="carrying"></strong></div>
        <div class="card"><h3>Food Left</h3><strong id="food-left"></strong></div>
        <div class="card"><h3>Contest</h3><strong id="contest"></strong></div>
        <div class="card"><h3>Avoid</h3><strong id="avoid"></strong></div>
        <div class="card"><h3>Corpses</h3><strong id="corpse-count"></strong></div>
        <div class="card"><h3>Residue</h3><strong id="residue-cells"></strong></div>
        <div class="card"><h3>Decomp</h3><strong id="decomposer-count"></strong></div>
        <div class="card"><h3>Enriched</h3><strong id="enriched-residue"></strong></div>
      </div>
      <section class="section">
        <h2>Moment</h2>
        <div id="moment-log" class="log"></div>
      </section>
      <section class="section" id="branch-section">
        <h2>Branch</h2>
        <div id="branch-meta" class="selected-ant"></div>
      </section>
      <section class="section">
        <h2>Colonies</h2>
        <div id="colony-log" class="log"></div>
      </section>
      <section class="section">
        <h2>Selected Ant</h2>
        <div id="selected-ant" class="selected-ant">
          <strong>No selection</strong>
          <div class="tiny">Hover or click an ant to inspect its position.</div>
        </div>
      </section>
    </aside>
  </div>
  <script id="observer-data" type="application/json">{data_json}</script>
  <script>
    const data = JSON.parse(document.getElementById('observer-data').textContent);
    const canvas = document.getElementById('world');
    const ctx = canvas.getContext('2d');
    const timeline = document.getElementById('timeline');
    const tickLabel = document.getElementById('tick-label');
    const playButton = document.getElementById('play');
    const backButton = document.getElementById('back');
    const forwardButton = document.getElementById('forward');
    const aliveEl = document.getElementById('alive');
    const nestFoodEl = document.getElementById('nest-food');
    const carryingEl = document.getElementById('carrying');
    const foodLeftEl = document.getElementById('food-left');
    const contestEl = document.getElementById('contest');
    const avoidEl = document.getElementById('avoid');
    const corpseCountEl = document.getElementById('corpse-count');
    const residueCellsEl = document.getElementById('residue-cells');
    const decomposerCountEl = document.getElementById('decomposer-count');
    const enrichedResidueEl = document.getElementById('enriched-residue');
    const generatedAtEl = document.getElementById('generated-at');
    const momentLog = document.getElementById('moment-log');
    const branchSection = document.getElementById('branch-section');
    const branchMetaEl = document.getElementById('branch-meta');
    const colonyLog = document.getElementById('colony-log');
    const selectedAntEl = document.getElementById('selected-ant');

    const widthScale = canvas.width / data.width;
    const heightScale = canvas.height / data.height;
    const colonyMeta = Object.fromEntries(data.colonies.map(colony => [colony.colony_id, colony]));
    const terrainPalette = {{
      dense_grass: 'rgba(106, 141, 84, 0.42)',
      sand: 'rgba(214, 184, 129, 0.44)',
      rock: 'rgba(92, 86, 81, 0.78)',
    }};
    const residuePalette = {{
      trail: 'rgba(74, 132, 115, 0.16)',
      nest: 'rgba(182, 126, 58, 0.22)',
      corpse: 'rgba(132, 66, 56, 0.24)',
      decomposer: 'rgba(79, 141, 91, 0.26)',
      unknown: 'rgba(99, 87, 73, 0.16)',
    }};

    let index = 0;
    let playing = false;
    let timer = null;
    const frames = data.frames;
    let hoverAntId = null;
    let pinnedAntId = null;

    const checkpointMode = data.replayed_from_checkpoint ? ' · checkpoint continuation' : (data.source_checkpoint ? ' · checkpoint snapshot' : '');
    generatedAtEl.textContent = `Generated ${{data.generated_at}}${{data.live ? ' · live export' : ''}}${{checkpointMode}}`;

    if (data.source_checkpoint || data.checkpoint_metadata) {{
      const metadata = data.checkpoint_metadata || {{}};
      const branchRows = [
        ['mode', data.replayed_from_checkpoint ? 'continuation replay' : 'checkpoint snapshot'],
        ['branch', metadata.branch_id || 'none'],
        ['run', metadata.run_id || 'none'],
        ['parent branch', metadata.parent_branch_id || 'none'],
        ['parent run', metadata.parent_run_id || 'none'],
        ['forked from tick', metadata.forked_from_tick ?? 'none'],
        ['loaded tick', data.loaded_tick ?? 'none'],
        ['target tick', data.target_tick ?? data.total_ticks],
        ['seed', data.config_seed ?? 'config'],
        ['inheritance', data.config_inheritance_mode || 'config'],
        ['mutation rate', data.config_mutation_rate ?? 'config'],
        ['checkpoint', data.source_checkpoint || 'none'],
      ];
      branchMetaEl.innerHTML = `
        <strong>${{metadata.branch_id || 'Checkpoint Branch'}}</strong>
        ${{branchRows.map(([label, value]) => `<div class="tiny">${{label}} = ${{value}}</div>`).join('')}}
      `;
    }} else {{
      branchSection.style.display = 'none';
    }}

    function toCanvasX(x) {{
      return (x + 0.5) * widthScale;
    }}

    function toCanvasY(y) {{
      return (y + 0.5) * heightScale;
    }}

    function drawBackground() {{
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
      gradient.addColorStop(0, '#fbf6ef');
      gradient.addColorStop(1, '#eedfcb');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.strokeStyle = 'rgba(65, 49, 31, 0.045)';
      ctx.lineWidth = 1;
      for (let x = 0; x <= data.width; x += 4) {{
        ctx.beginPath();
        ctx.moveTo(x * widthScale, 0);
        ctx.lineTo(x * widthScale, canvas.height);
        ctx.stroke();
      }}
      for (let y = 0; y <= data.height; y += 4) {{
        ctx.beginPath();
        ctx.moveTo(0, y * heightScale);
        ctx.lineTo(canvas.width, y * heightScale);
        ctx.stroke();
      }}
    }}

    function drawTerrain() {{
      for (const cell of data.terrain) {{
        const fill = terrainPalette[cell.kind];
        if (!fill) continue;
        ctx.fillStyle = fill;
        ctx.fillRect(
          cell.x * widthScale,
          cell.y * heightScale,
          Math.max(1.2, widthScale),
          Math.max(1.2, heightScale),
        );
      }}
    }}

    function drawResidue(frame) {{
      for (const point of frame.residue_points) {{
        const fill = residuePalette[point.source_type] || residuePalette.unknown;
        if (point.enriched) {{
          ctx.fillStyle = residuePalette.decomposer;
        }} else {{
          ctx.fillStyle = fill;
        }}
        ctx.beginPath();
        ctx.arc(toCanvasX(point.x), toCanvasY(point.y), 2.8 + point.value * 1.35, 0, Math.PI * 2);
        ctx.fill();
      }}
    }}

    function drawTrails(frame) {{
      for (const layer of frame.home_trail_layers) {{
        for (const point of layer.points) {{
          ctx.fillStyle = `${{layer.color}}33`;
          ctx.beginPath();
          ctx.arc(toCanvasX(point.x), toCanvasY(point.y), 3.5 + point.value * 1.1, 0, Math.PI * 2);
          ctx.fill();
        }}
      }}
      for (const layer of frame.food_trail_layers) {{
        for (const point of layer.points) {{
          ctx.fillStyle = `${{layer.color}}55`;
          ctx.beginPath();
          ctx.arc(toCanvasX(point.x), toCanvasY(point.y), 4 + point.value * 1.2, 0, Math.PI * 2);
          ctx.fill();
        }}
      }}
    }}

    function drawNests() {{
      for (const colony of data.colonies) {{
        const x = toCanvasX(colony.nest.x);
        const y = toCanvasY(colony.nest.y);
        ctx.fillStyle = `${{colony.color}}22`;
        ctx.beginPath();
        ctx.arc(x, y, (colony.nest.radius + 4.5) * widthScale, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = colony.color;
        ctx.beginPath();
        ctx.arc(x, y, (colony.nest.radius + 1.8) * widthScale, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = 'rgba(255, 246, 235, 0.92)';
        ctx.beginPath();
        ctx.arc(x, y, (colony.nest.radius + 0.7) * widthScale, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#4d3726';
        ctx.beginPath();
        ctx.arc(x, y, colony.nest.radius * widthScale, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = 'rgba(255, 248, 239, 0.84)';
        ctx.lineWidth = 2.2;
        ctx.beginPath();
        ctx.moveTo(x + (colony.nest.radius + 0.8) * widthScale, y);
        ctx.lineTo(x + (colony.nest.radius + 3.1) * widthScale, y);
        ctx.stroke();
        ctx.fillStyle = colony.color;
        ctx.font = '12px Menlo, monospace';
        ctx.fillText(colony.display_name, x - 18, y - 14);
      }}
    }}

    function drawFood(frame) {{
      for (const patch of frame.food_patches) {{
        if (patch.amount <= 0) continue;
        const pressureAlpha = Math.min(0.36, patch.competition_pressure / 18);
        if (pressureAlpha > 0.02) {{
          ctx.fillStyle = `rgba(214, 116, 59, ${{pressureAlpha}})`;
          ctx.beginPath();
          ctx.arc(
            toCanvasX(patch.x),
            toCanvasY(patch.y),
            (patch.radius + 2.6 + patch.nearby_ants * 0.18) * widthScale,
            0,
            Math.PI * 2,
          );
          ctx.fill();
        }}
        const alpha = patch.max_amount === 0 ? 0 : Math.max(0.08, patch.amount / patch.max_amount);
        ctx.fillStyle = `rgba(152, 184, 95, ${{alpha}})`;
        ctx.strokeStyle = patch.competition_pressure >= 3.2 ? 'rgba(168, 84, 34, 0.72)' : 'rgba(93, 120, 44, 0.28)';
        ctx.lineWidth = patch.competition_pressure >= 3.2 ? 3.2 : 2;
        ctx.beginPath();
        ctx.arc(toCanvasX(patch.x), toCanvasY(patch.y), (patch.radius + 1.3) * widthScale, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        ctx.fillStyle = 'rgba(58, 82, 28, 0.58)';
        ctx.font = '11px Menlo, monospace';
        ctx.fillText(`${{patch.amount}} · ${{patch.nearby_ants}} · v${{patch.value_score.toFixed(1)}}`, toCanvasX(patch.x) - 34, toCanvasY(patch.y) + 4);
      }}
    }}

    function drawCorpses(frame) {{
      for (const corpse of frame.corpses) {{
        const x = toCanvasX(corpse.x);
        const y = toCanvasY(corpse.y);
        ctx.strokeStyle = 'rgba(101, 55, 44, 0.92)';
        ctx.lineWidth = 2.2;
        ctx.beginPath();
        ctx.moveTo(x - 4.5, y - 4.5);
        ctx.lineTo(x + 4.5, y + 4.5);
        ctx.moveTo(x + 4.5, y - 4.5);
        ctx.lineTo(x - 4.5, y + 4.5);
        ctx.stroke();
        ctx.fillStyle = 'rgba(255, 248, 239, 0.6)';
        ctx.beginPath();
        ctx.arc(x, y, 1.6, 0, Math.PI * 2);
        ctx.fill();
      }}
    }}

    function drawDecomposers(frame) {{
      for (const patch of frame.decomposer_patches) {{
        const x = toCanvasX(patch.x);
        const y = toCanvasY(patch.y);
        ctx.fillStyle = 'rgba(88, 129, 74, 0.92)';
        ctx.beginPath();
        ctx.arc(x, y, 3.2 + patch.biomass * 2.4, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = 'rgba(241, 247, 231, 0.78)';
        ctx.lineWidth = 1.3;
        ctx.beginPath();
        ctx.arc(x, y, 4.6 + patch.biomass * 1.8, 0, Math.PI * 2);
        ctx.stroke();
      }}
    }}

    function antColor(ant) {{
      const colony = colonyMeta[ant.colony_id];
      if (!colony) return ant.carrying_food ? '#d8893c' : '#2c241d';
      return ant.carrying_food ? '#d8893c' : colony.color;
    }}

    function drawAnts(frame) {{
      for (const ant of frame.ants) {{
        const x = toCanvasX(ant.x);
        const y = toCanvasY(ant.y);
        ctx.fillStyle = antColor(ant);
        const heading = ant.heading || 0;
        const dx = Math.cos(heading);
        const dy = Math.sin(heading);
        const abdomenX = x - dx * 5;
        const abdomenY = y - dy * 5;
        const headX = x + dx * 4;
        const headY = y + dy * 4;
        ctx.beginPath();
        ctx.arc(abdomenX, abdomenY, 3.6, 0, Math.PI * 2);
        ctx.arc(x, y, 2.9, 0, Math.PI * 2);
        ctx.arc(headX, headY, 2.4, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = 'rgba(255,255,255,0.26)';
        ctx.lineWidth = 0.9;
        ctx.beginPath();
        ctx.moveTo(abdomenX, abdomenY);
        ctx.lineTo(headX, headY);
        ctx.stroke();
        if (ant.carrying_food) {{
          ctx.fillStyle = 'rgba(216, 137, 60, 0.96)';
          ctx.beginPath();
          ctx.arc(headX + dx * 3, headY + dy * 3, 2.3, 0, Math.PI * 2);
          ctx.fill();
        }}
        if (ant.behavior_state === 'contest') {{
          ctx.strokeStyle = 'rgba(181, 72, 43, 0.92)';
          ctx.lineWidth = 2.1;
          ctx.beginPath();
          ctx.arc(x, y, 8.4, 0, Math.PI * 2);
          ctx.stroke();
        }} else if (ant.behavior_state === 'avoid') {{
          ctx.strokeStyle = 'rgba(55, 90, 127, 0.76)';
          ctx.lineWidth = 1.8;
          ctx.setLineDash([3, 3]);
          ctx.beginPath();
          ctx.arc(x, y, 8.0, 0, Math.PI * 2);
          ctx.stroke();
          ctx.setLineDash([]);
        }} else if (ant.behavior_state === 'hungry') {{
          ctx.strokeStyle = 'rgba(189, 142, 49, 0.86)';
          ctx.lineWidth = 1.8;
          ctx.beginPath();
          ctx.arc(x, y, 7.6, 0, Math.PI * 2);
          ctx.stroke();
        }}
        if (ant.in_combat) {{
          ctx.strokeStyle = 'rgba(173, 48, 48, 0.92)';
          ctx.lineWidth = 2.4;
          ctx.beginPath();
          ctx.arc(x, y, 9.5, 0, Math.PI * 2);
          ctx.stroke();
        }}
        const highlighted = ant.ant_id === (pinnedAntId || hoverAntId);
        if (highlighted) {{
          ctx.strokeStyle = 'rgba(38, 73, 59, 0.95)';
          ctx.lineWidth = 2.5;
          ctx.beginPath();
          ctx.arc(x, y, 10, 0, Math.PI * 2);
          ctx.stroke();
          ctx.fillStyle = 'rgba(255, 252, 247, 0.92)';
          ctx.fillRect(x + 10, y - 20, 104, 24);
          ctx.strokeStyle = 'rgba(38, 73, 59, 0.22)';
          ctx.strokeRect(x + 10, y - 20, 104, 24);
          ctx.fillStyle = '#26493b';
          ctx.font = '11px Menlo, monospace';
          ctx.fillText(`${{ant.ant_id}} @ (${{ant.x}},${{ant.y}})`, x + 14, y - 5);
        }}
      }}
      for (const death of frame.death_events) {{
        const x = toCanvasX(death.payload.x);
        const y = toCanvasY(death.payload.y);
        ctx.strokeStyle = 'rgba(156, 52, 43, 0.86)';
        ctx.lineWidth = 2.4;
        ctx.beginPath();
        ctx.moveTo(x - 6, y - 6);
        ctx.lineTo(x + 6, y + 6);
        ctx.moveTo(x + 6, y - 6);
        ctx.lineTo(x - 6, y + 6);
        ctx.stroke();
      }}
    }}

    function drawFrame(frame) {{
      drawBackground();
      drawTerrain();
      drawResidue(frame);
      drawTrails(frame);
      drawFood(frame);
      drawNests();
      drawCorpses(frame);
      drawDecomposers(frame);
      drawAnts(frame);
    }}

    function render(indexToRender) {{
      const frame = frames[indexToRender];
      index = indexToRender;
      timeline.value = String(indexToRender + 1);
      tickLabel.textContent = `Tick ${{frame.tick}} / ${{data.total_ticks}}${{data.live ? ' · live' : ''}}`;
      aliveEl.textContent = frame.alive;
      nestFoodEl.textContent = frame.nest_food;
      carryingEl.textContent = frame.carrying;
      foodLeftEl.textContent = frame.food_remaining;
      contestEl.textContent = frame.contesting_ants;
      avoidEl.textContent = frame.avoidance_turns;
      corpseCountEl.textContent = frame.corpse_count;
      residueCellsEl.textContent = frame.residue_cell_count;
      decomposerCountEl.textContent = frame.decomposer_patch_count;
      enrichedResidueEl.textContent = frame.enriched_residue_cell_count;
      drawFrame(frame);
      momentLog.innerHTML = '';
      colonyLog.innerHTML = '';
      const logItems = [];
      if (frame.contest_entries) logItems.push(`contest entries +${{frame.contest_entries}}`);
      if (frame.contesting_ants) logItems.push(`contesting ants ${{frame.contesting_ants}}`);
      if (frame.avoidance_turns) logItems.push(`avoid turns ${{frame.avoidance_turns}}`);
      if (frame.pickups) logItems.push(`food pickups +${{frame.pickups}}`);
      if (frame.unloads) logItems.push(`nest unloads +${{frame.unloads}}`);
      if (frame.upkeep_events.length) logItems.push(`nest upkeep -${{frame.upkeep_events.reduce((sum, event) => sum + event.payload.consumed, 0)}}`);
      if (frame.reseed_events.length) logItems.push(`food reseeds +${{frame.reseed_events.length}}`);
      if (frame.contested_source_events.length) logItems.push(`source contests +${{frame.contested_source_events.length}}`);
      if (frame.combat_start_events.length) logItems.push(`combat starts +${{frame.combat_start_events.length}}`);
      if (frame.combat_pairs) logItems.push(`combat pairs ${{frame.combat_pairs}}`);
      if (frame.depleted_source_events.length) logItems.push(`sources depleted +${{frame.depleted_source_events.length}}`);
      if (frame.corpse_count) logItems.push(`corpses ${{frame.corpse_count}} · residue ${{frame.residue_cell_count}}`);
      if (frame.decomposer_patch_count) logItems.push(`decomposer ${{frame.decomposer_patch_count}} · enriched ${{frame.enriched_residue_cell_count}}`);
      if (frame.births) logItems.push(`ant births +${{frame.births}}`);
      if (frame.death_events.length) logItems.push(`ant deaths +${{frame.death_events.length}}`);
      if (frame.moves) logItems.push(`moves +${{frame.moves}}`);
      if (!logItems.length) logItems.push('quiet tick');
      logItems.forEach(item => {{
        const row = document.createElement('div');
        row.className = 'log-row';
        row.innerHTML = `<strong>${{item}}</strong>`;
        momentLog.appendChild(row);
      }});
      frame.colony_stats.forEach(colony => {{
        const row = document.createElement('div');
        row.className = 'log-row';
        row.innerHTML = `
          <strong style="color: ${{colony.color}}">${{colony.display_name}}</strong>
          <div class="tiny">alive = ${{colony.alive}} · carrying = ${{colony.carrying}} · nest = ${{colony.nest_food}}</div>
          <div class="tiny">births +${{colony.births}} · deaths +${{colony.deaths}}</div>
        `;
        colonyLog.appendChild(row);
      }});

      const selectedId = pinnedAntId || hoverAntId;
      const selected = selectedId ? frame.ants.find(ant => ant.ant_id === selectedId) : null;
      if (selected) {{
        selectedAntEl.innerHTML = `
          <strong>${{selected.ant_id}}</strong>
          <div class="tiny">colony = ${{selected.colony_id}}</div>
          <div class="tiny">pos = (${{selected.x}}, ${{selected.y}})</div>
          <div class="tiny">carrying = ${{selected.carrying_food ? 'yes' : 'no'}}</div>
          <div class="tiny">terrain = ${{selected.terrain_kind}}</div>
          <div class="tiny">state = ${{selected.behavior_state}}</div>
          <div class="tiny">target = ${{selected.target_patch_id || 'none'}}</div>
          <div class="tiny">contest patch = ${{selected.contest_patch_id || 'none'}}</div>
          <div class="tiny">energy = ${{selected.energy.toFixed(2)}} · starvation = ${{selected.starvation_ticks}}</div>
          <div class="tiny">outbound = ${{selected.outbound_commit_ticks}}</div>
          <div class="tiny">combat = ${{selected.in_combat ? 'yes' : 'no'}}</div>
          <div class="tiny">combat with = ${{selected.combat_with_id || 'none'}}</div>
          <div class="tiny">combat ticks = ${{selected.combat_ticks_remaining}}</div>
          <div class="tiny">combat cooldown = ${{selected.combat_cooldown_ticks}}</div>
          <div class="tiny">delivered = ${{selected.delivered_food}}</div>
          <div class="tiny">age = ${{selected.age}}</div>
          <div class="tiny">born = ${{selected.birth_tick}} · parent = ${{selected.parent_id || 'founder'}}</div>
          <div class="tiny">lineage = ${{selected.lineage_id || selected.ant_id}}</div>
          <div class="tiny">genome = ${{selected.genome_id}} · parent genome = ${{selected.parent_genome_id || 'founder'}}</div>
          <div class="tiny">generation = ${{selected.generation}} · mutations = ${{selected.mutation_count}}</div>
          <div class="tiny">mutation log = ${{selected.mutation_log.length ? selected.mutation_log.join(' | ') : 'none'}}</div>
          <div class="tiny">range = ${{selected.range_bias.toFixed(2)}}</div>
          <div class="tiny">trail = ${{selected.trail_affinity.toFixed(2)}}</div>
          <div class="tiny">harvest = ${{selected.harvest_drive.toFixed(2)}}</div>
        `;
      }} else {{
        selectedAntEl.innerHTML = `
          <strong>No selection</strong>
          <div class="tiny">Hover or click an ant to inspect its position.</div>
        `;
      }}
    }}

    function setPlaying(next) {{
      if (data.live) return;
      playing = next;
      playButton.textContent = playing ? 'Pause' : 'Play';
      if (timer) {{
        clearInterval(timer);
        timer = null;
      }}
      if (playing) {{
        timer = setInterval(() => {{
          const nextIndex = index + 1 >= data.frames.length ? 0 : index + 1;
          render(nextIndex);
        }}, 420);
      }}
    }}

    timeline.max = String(frames.length);
    if (data.live || frames.length <= 1) {{
      playButton.disabled = true;
      backButton.disabled = true;
      forwardButton.disabled = true;
      timeline.disabled = true;
      playButton.textContent = data.live ? (data.complete ? 'Done' : 'Live') : 'Snapshot';
    }} else {{
      timeline.addEventListener('input', () => render(Number(timeline.value) - 1));
      playButton.addEventListener('click', () => setPlaying(!playing));
      backButton.addEventListener('click', () => {{
        setPlaying(false);
        render((index - 1 + frames.length) % frames.length);
      }});
      forwardButton.addEventListener('click', () => {{
        setPlaying(false);
        render((index + 1) % frames.length);
      }});
    }}

    function antAtPointer(event) {{
      const rect = canvas.getBoundingClientRect();
      const scaleX = canvas.width / rect.width;
      const scaleY = canvas.height / rect.height;
      const px = (event.clientX - rect.left) * scaleX;
      const py = (event.clientY - rect.top) * scaleY;
      let best = null;
      let bestDistance = 14;
      for (const ant of frames[index].ants) {{
        const dx = toCanvasX(ant.x) - px;
        const dy = toCanvasY(ant.y) - py;
        const distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < bestDistance) {{
          bestDistance = distance;
          best = ant.ant_id;
        }}
      }}
      return best;
    }}

    canvas.addEventListener('mousemove', event => {{
      if (pinnedAntId) return;
      hoverAntId = antAtPointer(event);
      render(index);
    }});

    canvas.addEventListener('mouseleave', () => {{
      if (pinnedAntId) return;
      hoverAntId = null;
      render(index);
    }});

    canvas.addEventListener('click', event => {{
      const selected = antAtPointer(event);
      if (pinnedAntId && pinnedAntId === selected) {{
        pinnedAntId = null;
        hoverAntId = null;
      }} else {{
        pinnedAntId = selected;
      }}
      render(index);
    }});
    render(0);
    {live_reload_script}
  </script>
</body>
</html>"""


def write_ant_observer_html(path: str | Path, payload: dict[str, object]) -> None:
    Path(path).write_text(_html_shell(json.dumps(payload), payload["title"]), encoding="utf-8")


def write_ant_live_observer_html(path: str | Path, payload: dict[str, object], auto_reload_ms: int = 450) -> None:
    Path(path).write_text(
        _html_shell(json.dumps(payload), payload["title"], auto_reload_ms=auto_reload_ms),
        encoding="utf-8",
    )
