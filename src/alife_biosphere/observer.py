from __future__ import annotations

import json
import math
from pathlib import Path

from .config import SimulationConfig
from .events import Event
from .simulation import SimulationResult
from .world import World


DEFAULT_LAYOUT = {
    "nursery_a": {"x": 165, "y": 120, "w": 200, "h": 112},
    "nursery_b": {"x": 165, "y": 344, "w": 200, "h": 112},
    "refuge": {"x": 372, "y": 232, "w": 214, "h": 146},
    "frontier_a": {"x": 590, "y": 152, "w": 236, "h": 126},
    "frontier_b": {"x": 590, "y": 320, "w": 236, "h": 126},
    "wild_a": {"x": 800, "y": 112, "w": 210, "h": 132},
    "wild_b": {"x": 800, "y": 360, "w": 210, "h": 132},
}


def _tick_summaries(events: list[Event]) -> list[Event]:
    return [event for event in events if event.event_type == "tick_summary"]


def _event_dicts_by_tick(events: list[Event], event_type: str) -> dict[int, list[dict[str, object]]]:
    payload: dict[int, list[dict[str, object]]] = {}
    for event in events:
        if event.event_type != event_type:
            continue
        payload.setdefault(event.tick, []).append(event.to_dict())
    return payload


def _habitat_entries(config: SimulationConfig) -> list[dict[str, object]]:
    entries = []
    for habitat in sorted(config.world.habitats, key=lambda item: item.habitat_id):
        layout = DEFAULT_LAYOUT.get(habitat.habitat_id, {"x": 100, "y": 100, "w": 160, "h": 100})
        entries.append(
            {
                "habitat_id": habitat.habitat_id,
                "habitat_family": habitat.habitat_family,
                "x": layout["x"],
                "y": layout["y"],
                "w": layout["w"],
                "h": layout["h"],
            }
        )
    return entries


def _initial_organism_states(config: SimulationConfig) -> dict[str, dict[str, object]]:
    seed_world = World.from_config(config.world)
    payload: dict[str, dict[str, object]] = {}
    for organism in seed_world.organisms.values():
        payload[organism.organism_id] = {
            "organism_id": organism.organism_id,
            "lineage_id": organism.lineage_id,
            "parent_id": organism.parent_id,
            "generation": organism.generation,
            "birth_tick": 0,
            "habitat_id": organism.habitat_id,
            "alive": True,
        }
    return payload


def _organism_snapshot_by_tick(
    config: SimulationConfig,
    result: SimulationResult,
) -> dict[int, dict[str, object]]:
    tick_summaries = _tick_summaries(result.events)
    timeline_events: dict[int, list[Event]] = {}
    for event in result.events:
        if event.event_type == "tick_summary":
            continue
        timeline_events.setdefault(event.tick, []).append(event)

    organism_states = _initial_organism_states(config)
    snapshots: dict[int, dict[str, object]] = {}
    for summary in tick_summaries:
        tick = summary.tick
        birth_ids: set[str] = set()
        moved_ids: set[str] = set()
        death_events: list[dict[str, object]] = []
        disturbance_events: list[dict[str, object]] = []
        move_events: list[dict[str, object]] = []
        birth_events: list[dict[str, object]] = []
        for event in timeline_events.get(tick, []):
            if event.event_type == "birth" and event.organism_id is not None:
                organism_states[event.organism_id] = {
                    "organism_id": event.organism_id,
                    "lineage_id": event.payload["lineage_id"],
                    "parent_id": event.payload["parent_id"],
                    "generation": int(event.payload["generation"]),
                    "birth_tick": tick,
                    "habitat_id": event.habitat_id,
                    "alive": True,
                }
                birth_ids.add(event.organism_id)
                birth_events.append(event.to_dict())
            elif event.event_type == "move" and event.organism_id is not None:
                if event.organism_id in organism_states:
                    organism_states[event.organism_id]["habitat_id"] = event.habitat_id
                    moved_ids.add(event.organism_id)
                    move_events.append(event.to_dict())
            elif event.event_type == "death" and event.organism_id is not None:
                if event.organism_id in organism_states:
                    organism_states[event.organism_id]["alive"] = False
                    death_events.append(event.to_dict())
            elif event.event_type == "disturbance":
                disturbance_events.append(event.to_dict())

        organisms_by_habitat: dict[str, list[dict[str, object]]] = {
            habitat.habitat_id: [] for habitat in config.world.habitats
        }
        for organism in organism_states.values():
            if not organism["alive"]:
                continue
            habitat_id = str(organism["habitat_id"])
            organisms_by_habitat.setdefault(habitat_id, []).append(
                {
                    "organism_id": organism["organism_id"],
                    "lineage_id": organism["lineage_id"],
                    "generation": organism["generation"],
                    "age": tick - int(organism["birth_tick"]),
                    "just_born": organism["organism_id"] in birth_ids,
                    "just_moved": organism["organism_id"] in moved_ids,
                }
            )
        snapshots[tick] = {
            "organisms_by_habitat": organisms_by_habitat,
            "births": birth_events,
            "moves": move_events,
            "deaths": death_events,
            "disturbances": disturbance_events,
        }
    return snapshots


def build_positioned_organisms(
    habitats: list[dict[str, object]],
    organisms_by_habitat: dict[str, list[dict[str, object]]],
) -> list[dict[str, object]]:
    habitat_lookup = {item["habitat_id"]: item for item in habitats}
    positioned: list[dict[str, object]] = []
    golden_angle = 2.399963229728653
    for habitat_id, organisms in organisms_by_habitat.items():
        layout = habitat_lookup[habitat_id]
        rx = float(layout["w"]) * 0.38
        ry = float(layout["h"]) * 0.32
        for index, organism in enumerate(sorted(organisms, key=lambda item: (item["generation"], item["organism_id"]))):
            radius_factor = min(0.82, 0.18 + 0.12 * math.sqrt(index))
            angle = index * golden_angle + (0.17 if organism["generation"] % 2 else 0.0)
            x = float(layout["x"]) + math.cos(angle) * rx * radius_factor
            y = float(layout["y"]) + math.sin(angle) * ry * radius_factor
            positioned.append(
                {
                    **organism,
                    "habitat_id": habitat_id,
                    "x": round(x, 2),
                    "y": round(y, 2),
                }
            )
    return positioned


def build_observer_payload(
    config: SimulationConfig,
    result: SimulationResult,
    title: str = "Alife Biosphere Observer",
) -> dict[str, object]:
    tick_summaries = _tick_summaries(result.events)
    if not tick_summaries:
        return {
            "title": title,
            "ticks": 0,
            "habitats": [],
            "edges": [],
            "frames": [],
        }

    habitats = _habitat_entries(config)
    organism_snapshots = _organism_snapshot_by_tick(config, result)

    frames = []
    for summary in tick_summaries:
        payload = summary.payload
        habitats_payload: dict[str, dict[str, object]] = {}
        for habitat_id, occupancy in payload["occupancy_by_habitat"].items():
            habitats_payload[habitat_id] = {
                "occupancy": occupancy,
                "pressure": payload["occupancy_pressure_by_habitat"][habitat_id],
                "lineages": payload["lineages_by_habitat"][habitat_id],
            }
        organism_frame = organism_snapshots[summary.tick]
        frames.append(
            {
                "tick": summary.tick,
                "alive": payload["alive"],
                "movement_count": payload["movement_count"],
                "birth_count": payload["birth_count"],
                "reproduction_ready_count": payload["reproduction_ready_count"],
                "refuge_occupancy": payload["refuge_occupancy"],
                "lineage_count": payload["lineage_count"],
                "disturbances": organism_frame["disturbances"],
                "births": organism_frame["births"],
                "deaths": organism_frame["deaths"],
                "moves": organism_frame["moves"],
                "organisms": build_positioned_organisms(habitats, organism_frame["organisms_by_habitat"]),
                "habitats": habitats_payload,
            }
        )

    return {
        "title": title,
        "ticks": len(frames),
        "habitats": habitats,
        "edges": [
            {"from": left, "to": right}
            for left, right in config.world.habitat_edges
        ],
        "frames": frames,
    }


def render_observer_html(payload: dict[str, object]) -> str:
    data_json = json.dumps(payload)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{payload["title"]}</title>
  <style>
    :root {{
      --bg: #f5eee1;
      --panel: rgba(255, 249, 241, 0.76);
      --stage: rgba(252, 246, 238, 0.78);
      --ink: #1f1a15;
      --muted: #6d665d;
      --line: rgba(48, 36, 24, 0.16);
      --nursery: #9bcf8b;
      --refuge: #7fae8f;
      --frontier: #c89f5d;
      --wild: #a55b43;
      --disturb: #c53a2f;
      --birth: #2a8f62;
      --death: #5c2b27;
      --organism: #231c16;
      --accent: #214e41;
      --shadow: 0 18px 48px rgba(36, 27, 17, 0.14);
    }}

    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background:
        radial-gradient(circle at top left, rgba(155, 207, 139, 0.16), transparent 24%),
        radial-gradient(circle at top right, rgba(182, 106, 77, 0.14), transparent 22%),
        linear-gradient(180deg, #f8f2ea 0%, #eee3d5 100%);
      color: var(--ink);
      font-family: "Avenir Next", "Segoe UI", "Helvetica Neue", sans-serif;
    }}

    .shell {{
      min-height: 100vh;
      display: flex;
      gap: 18px;
      padding: 18px;
    }}

    .stage, .panel {{
      background: var(--panel);
      border: 1px solid rgba(59, 45, 32, 0.08);
      border-radius: 26px;
      box-shadow: var(--shadow);
      backdrop-filter: blur(10px);
    }}

    .stage {{
      flex: 1;
      padding: 18px;
      background:
        radial-gradient(circle at top, rgba(255,255,255,0.65), transparent 46%),
        linear-gradient(180deg, rgba(252, 246, 238, 0.94), rgba(246, 238, 227, 0.94));
    }}

    .panel {{
      width: 320px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}

    .title {{
      margin: 0 0 6px;
      font-size: 32px;
      line-height: 1;
      letter-spacing: 0.01em;
      font-family: "Avenir Next Condensed", "Helvetica Neue", sans-serif;
      font-weight: 700;
    }}

    .subtitle {{
      margin: 0;
      font-size: 14px;
      color: var(--muted);
    }}

    .toolbar {{
      display: flex;
      gap: 10px;
      align-items: center;
      margin: 16px 0 10px;
      flex-wrap: wrap;
    }}

    button {{
      appearance: none;
      border: 0;
      border-radius: 999px;
      background: var(--accent);
      color: #f8f5ef;
      padding: 10px 16px;
      font-size: 13px;
      font-family: "SF Mono", "Menlo", "Consolas", monospace;
      cursor: pointer;
      transition: transform 120ms ease, opacity 120ms ease;
    }}

    button:hover {{ transform: translateY(-1px); }}
    button.secondary {{
      background: rgba(27, 77, 62, 0.12);
      color: var(--accent);
    }}

    input[type="range"] {{
      flex: 1;
      min-width: 220px;
      accent-color: var(--accent);
    }}

    .tick-label {{
      font-family: "SF Mono", "Menlo", "Consolas", monospace;
      font-size: 13px;
      color: var(--muted);
    }}

    .legend {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      font-size: 12px;
      color: var(--muted);
      margin-bottom: 10px;
      font-family: "SF Mono", "Menlo", "Consolas", monospace;
    }}

    .legend span {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}

    .legend-dot {{
      width: 10px;
      height: 10px;
      border-radius: 999px;
      display: inline-block;
    }}

    svg {{
      width: 100%;
      height: auto;
      border-radius: 22px;
      background:
        linear-gradient(180deg, rgba(255,255,255,0.52), rgba(246, 237, 224, 0.9)),
        repeating-linear-gradient(
          0deg,
          transparent,
          transparent 34px,
          rgba(42, 33, 24, 0.03) 34px,
          rgba(42, 33, 24, 0.03) 35px
        ),
        repeating-linear-gradient(
          90deg,
          transparent,
          transparent 34px,
          rgba(42, 33, 24, 0.03) 34px,
          rgba(42, 33, 24, 0.03) 35px
        );
    }}

    .edge {{
      stroke: rgba(64, 49, 34, 0.18);
      stroke-width: 10;
      stroke-linecap: round;
      fill: none;
    }}

    .region {{
      stroke: rgba(42, 30, 20, 0.16);
      stroke-width: 3;
      transition: opacity 160ms ease, transform 160ms ease;
    }}

    .region-label {{
      font-size: 14px;
      font-weight: 700;
      fill: rgba(27, 21, 16, 0.92);
      text-anchor: middle;
      letter-spacing: 0.04em;
      font-family: "Avenir Next Condensed", "Helvetica Neue", sans-serif;
    }}

    .region-meta {{
      font-size: 11px;
      text-anchor: middle;
      font-family: "SF Mono", "Menlo", "Consolas", monospace;
      fill: rgba(88, 72, 57, 0.84);
    }}

    .organism {{
      fill: var(--organism);
      opacity: 0.92;
      transition: transform 140ms ease, opacity 140ms ease;
    }}

    .organism.moved {{
      stroke: rgba(255,255,255,0.92);
      stroke-width: 1.8;
    }}

    .organism.born {{
      stroke: var(--birth);
      stroke-width: 2.2;
    }}

    .birth-ring {{
      fill: none;
      stroke: rgba(42, 143, 98, 0.82);
      stroke-width: 2;
    }}

    .death-marker {{
      stroke: rgba(92, 43, 39, 0.92);
      stroke-width: 2.4;
      stroke-linecap: round;
    }}

    .disturbance-pulse {{
      fill: rgba(197, 58, 47, 0.12);
      stroke: rgba(197, 58, 47, 0.78);
      stroke-width: 3;
    }}

    .cards {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }}

    .card {{
      border-radius: 18px;
      padding: 12px;
      background: rgba(250, 245, 238, 0.92);
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

    .section-title {{
      margin: 0 0 8px;
      font-size: 14px;
      font-family: "SF Mono", "Menlo", "Consolas", monospace;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}

    .scroll-list {{
      display: flex;
      flex-direction: column;
      gap: 8px;
      max-height: 240px;
      overflow: auto;
      padding-right: 4px;
    }}

    .log-row {{
      border-radius: 14px;
      padding: 10px 12px;
      background: rgba(250, 245, 238, 0.92);
      border: 1px solid rgba(48, 36, 25, 0.08);
      font-size: 13px;
      line-height: 1.4;
    }}

    .habitat-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}

    .habitat-table th,
    .habitat-table td {{
      padding: 8px 0;
      border-bottom: 1px solid rgba(48, 36, 25, 0.08);
      text-align: left;
      vertical-align: top;
    }}

    .habitat-table th {{
      color: var(--muted);
      font-family: "SF Mono", "Menlo", "Consolas", monospace;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
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
    <section class="stage">
      <h1 class="title">{payload["title"]}</h1>
      <p class="subtitle">A world-first observation window where the map comes first and the metrics stay secondary.</p>
      <div class="toolbar">
        <button id="play">Play</button>
        <button id="step-back" class="secondary">Back</button>
        <button id="step-forward" class="secondary">Forward</button>
        <input id="timeline" type="range" min="1" max="{payload["ticks"]}" value="1">
        <span class="tick-label" id="tick-label">Tick 1 / {payload["ticks"]}</span>
      </div>
      <div class="legend">
        <span><i class="legend-dot" style="background: var(--nursery)"></i>nursery</span>
        <span><i class="legend-dot" style="background: var(--refuge)"></i>refuge</span>
        <span><i class="legend-dot" style="background: var(--frontier)"></i>frontier</span>
        <span><i class="legend-dot" style="background: var(--wild)"></i>wild</span>
        <span><i class="legend-dot" style="background: var(--birth)"></i>birth</span>
        <span><i class="legend-dot" style="background: var(--disturb)"></i>disturbance pulse</span>
      </div>
      <svg id="map" viewBox="0 0 920 460" role="img" aria-label="Ecology observer map"></svg>
    </section>
    <aside class="panel">
      <div class="cards">
        <div class="card"><h3>Alive</h3><strong id="alive"></strong></div>
        <div class="card"><h3>Births</h3><strong id="births"></strong></div>
        <div class="card"><h3>Moves</h3><strong id="moves"></strong></div>
        <div class="card"><h3>Lineages</h3><strong id="lineages"></strong></div>
      </div>
      <section>
        <h2 class="section-title">Pulse Log</h2>
        <div id="disturbance-log" class="scroll-list"></div>
      </section>
      <section>
        <h2 class="section-title">Habitat Whisper</h2>
        <table class="habitat-table">
          <thead>
            <tr><th>Habitat</th><th>Life</th><th>Lineages</th></tr>
          </thead>
          <tbody id="habitat-table"></tbody>
        </table>
      </section>
    </aside>
  </div>
  <script id="observer-data" type="application/json">{data_json}</script>
  <script>
    const data = JSON.parse(document.getElementById('observer-data').textContent);
    const svg = document.getElementById('map');
    const timeline = document.getElementById('timeline');
    const tickLabel = document.getElementById('tick-label');
    const playButton = document.getElementById('play');
    const stepBack = document.getElementById('step-back');
    const stepForward = document.getElementById('step-forward');
    const aliveEl = document.getElementById('alive');
    const birthsEl = document.getElementById('births');
    const movesEl = document.getElementById('moves');
    const lineagesEl = document.getElementById('lineages');
    const disturbanceLog = document.getElementById('disturbance-log');
    const habitatTable = document.getElementById('habitat-table');

    const familyColor = {{
      nursery: 'var(--nursery)',
      refuge: 'var(--refuge)',
      frontier: 'var(--frontier)',
      wild: 'var(--wild)',
    }};

    const habitatMap = Object.fromEntries(data.habitats.map(item => [item.habitat_id, item]));
    data.edges.forEach(edge => {{
      const from = habitatMap[edge.from];
      const to = habitatMap[edge.to];
      const line = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      const midX = (from.x + to.x) / 2;
      const midY = (from.y + to.y) / 2 + (from.y < to.y ? 18 : -18);
      line.setAttribute('d', `M ${{from.x}} ${{from.y}} Q ${{midX}} ${{midY}} ${{to.x}} ${{to.y}}`);
      line.setAttribute('class', 'edge');
      svg.appendChild(line);
    }});

    const regionLayer = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    svg.appendChild(regionLayer);
    const organismLayer = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    svg.appendChild(organismLayer);
    const effectLayer = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    svg.appendChild(effectLayer);

    const regionEls = Object.fromEntries(data.habitats.map(item => {{
      const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      const region = document.createElementNS('http://www.w3.org/2000/svg', 'ellipse');
      region.setAttribute('cx', item.x);
      region.setAttribute('cy', item.y);
      region.setAttribute('rx', item.w / 2);
      region.setAttribute('ry', item.h / 2);
      region.setAttribute('class', 'region');
      region.setAttribute('fill', familyColor[item.habitat_family]);
      region.setAttribute('fill-opacity', '0.24');
      const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      label.setAttribute('x', item.x);
      label.setAttribute('y', item.y - 6);
      label.setAttribute('class', 'region-label');
      const meta = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      meta.setAttribute('x', item.x);
      meta.setAttribute('y', item.y + 14);
      meta.setAttribute('class', 'region-meta');
      group.appendChild(region);
      group.appendChild(label);
      group.appendChild(meta);
      regionLayer.appendChild(group);
      return [item.habitat_id, {{ group, region, label, meta }}];
    }}));

    let currentIndex = 0;
    let playing = false;
    let timer = null;

    function renderFrame(index) {{
      const frame = data.frames[index];
      currentIndex = index;
      timeline.value = String(frame.tick);
      tickLabel.textContent = `Tick ${{frame.tick}} / ${{data.ticks}}`;
      aliveEl.textContent = frame.alive;
      birthsEl.textContent = frame.birth_count;
      movesEl.textContent = frame.movement_count;
      lineagesEl.textContent = frame.lineage_count;

      const disturbedHabitats = new Set(frame.disturbances.map(item => item.habitat_id));
      for (const habitat of data.habitats) {{
        const state = frame.habitats[habitat.habitat_id];
        const region = regionEls[habitat.habitat_id];
        const occupancy = state.occupancy;
        region.region.setAttribute('fill-opacity', occupancy === 0 ? '0.12' : String(Math.min(0.18 + occupancy * 0.06, 0.44)));
        region.region.setAttribute('stroke', disturbedHabitats.has(habitat.habitat_id) ? 'rgba(197, 58, 47, 0.88)' : 'rgba(42, 30, 20, 0.16)');
        region.region.setAttribute('stroke-width', disturbedHabitats.has(habitat.habitat_id) ? '4' : '3');
        region.label.textContent = habitat.habitat_id.replace('_', ' ').toUpperCase();
        region.meta.textContent = `${{occupancy}} alive · ${{state.lineages.length}} lineages`;
      }}

      organismLayer.innerHTML = '';
      effectLayer.innerHTML = '';
      frame.organisms.forEach(organism => {{
        const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        dot.setAttribute('cx', organism.x);
        dot.setAttribute('cy', organism.y);
        dot.setAttribute('r', organism.generation > 0 ? 5.2 : 4.2);
        dot.setAttribute('class', `organism${{organism.just_moved ? ' moved' : ''}}${{organism.just_born ? ' born' : ''}}`);
        dot.setAttribute('fill', lineageColor(organism.lineage_id));
        organismLayer.appendChild(dot);

        if (organism.just_born) {{
          const ring = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
          ring.setAttribute('cx', organism.x);
          ring.setAttribute('cy', organism.y);
          ring.setAttribute('r', 9.5);
          ring.setAttribute('class', 'birth-ring');
          effectLayer.appendChild(ring);
        }}
      }});
      frame.disturbances.forEach(item => {{
        const habitat = habitatMap[item.habitat_id];
        const pulse = document.createElementNS('http://www.w3.org/2000/svg', 'ellipse');
        pulse.setAttribute('cx', habitat.x);
        pulse.setAttribute('cy', habitat.y);
        pulse.setAttribute('rx', habitat.w / 2 + 10);
        pulse.setAttribute('ry', habitat.h / 2 + 6);
        pulse.setAttribute('class', 'disturbance-pulse');
        effectLayer.appendChild(pulse);
      }});

      const deathByHabitat = frame.deaths.reduce((acc, item) => {{
        const key = item.habitat_id || 'unknown';
        acc[key] = (acc[key] || 0) + 1;
        return acc;
      }}, {{}});
      Object.entries(deathByHabitat).forEach(([habitatId, count], idx) => {{
        const habitat = habitatMap[habitatId];
        if (!habitat) return;
        for (let i = 0; i < count; i += 1) {{
          const dx = (i - (count - 1) / 2) * 12;
          const x = habitat.x + dx;
          const y = habitat.y - habitat.h / 2 - 10 - idx * 2;
          const lineA = document.createElementNS('http://www.w3.org/2000/svg', 'line');
          lineA.setAttribute('x1', x - 5);
          lineA.setAttribute('y1', y - 5);
          lineA.setAttribute('x2', x + 5);
          lineA.setAttribute('y2', y + 5);
          lineA.setAttribute('class', 'death-marker');
          const lineB = document.createElementNS('http://www.w3.org/2000/svg', 'line');
          lineB.setAttribute('x1', x + 5);
          lineB.setAttribute('y1', y - 5);
          lineB.setAttribute('x2', x - 5);
          lineB.setAttribute('y2', y + 5);
          lineB.setAttribute('class', 'death-marker');
          effectLayer.appendChild(lineA);
          effectLayer.appendChild(lineB);
        }}
      }});

      disturbanceLog.innerHTML = '';
      const logs = [];
      if (frame.births.length) logs.push(`births +${{frame.births.length}}`);
      if (frame.moves.length) logs.push(`moves +${{frame.moves.length}}`);
      if (frame.deaths.length) logs.push(`deaths +${{frame.deaths.length}}`);
      frame.disturbances.forEach(item => logs.push(`${{item.habitat_id}} disturbed`));
      if (!logs.length) logs.push('quiet tick');
      for (const item of logs) {{
        const row = document.createElement('div');
        row.className = 'log-row';
        row.innerHTML = `<strong>${{item}}</strong>`;
        disturbanceLog.appendChild(row);
      }}

      habitatTable.innerHTML = '';
      for (const habitat of data.habitats) {{
        const state = frame.habitats[habitat.habitat_id];
        const row = document.createElement('tr');
        const lineageText = state.lineages.length ? state.lineages.join(', ') : '—';
        row.innerHTML = `
          <td><strong>${{habitat.habitat_id}}</strong><div class="tiny">${{habitat.habitat_family}}</div></td>
          <td>${{state.occupancy}} · ${{state.pressure.toFixed(2)}}</td>
          <td>${{lineageText}}</td>
        `;
        habitatTable.appendChild(row);
      }}
    }}

    function lineageColor(lineageId) {{
      let hash = 0;
      for (let i = 0; i < lineageId.length; i += 1) {{
        hash = ((hash << 5) - hash + lineageId.charCodeAt(i)) | 0;
      }}
      const hue = Math.abs(hash) % 360;
      return `hsl(${{hue}} 64% 42%)`;
    }}

    function setPlaying(next) {{
      playing = next;
      playButton.textContent = playing ? 'Pause' : 'Play';
      if (timer) {{
        clearInterval(timer);
        timer = null;
      }}
      if (playing) {{
        timer = setInterval(() => {{
          const nextIndex = currentIndex + 1 >= data.frames.length ? 0 : currentIndex + 1;
          renderFrame(nextIndex);
        }}, 520);
      }}
    }}

    timeline.addEventListener('input', () => renderFrame(Number(timeline.value) - 1));
    playButton.addEventListener('click', () => setPlaying(!playing));
    stepBack.addEventListener('click', () => {{
      setPlaying(false);
      renderFrame((currentIndex - 1 + data.frames.length) % data.frames.length);
    }});
    stepForward.addEventListener('click', () => {{
      setPlaying(false);
      renderFrame((currentIndex + 1) % data.frames.length);
    }});

    renderFrame(0);
  </script>
</body>
</html>"""


def write_observer_html(
    path: str | Path,
    config: SimulationConfig,
    result: SimulationResult,
    title: str = "Alife Biosphere Observer",
) -> None:
    payload = build_observer_payload(config, result, title=title)
    Path(path).write_text(render_observer_html(payload), encoding="utf-8")
