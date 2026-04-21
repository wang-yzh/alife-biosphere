from __future__ import annotations

import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from alife_biosphere.config import SimulationConfig, WorldConfig
from alife_biosphere.observer import DEFAULT_LAYOUT, build_positioned_organisms
from alife_biosphere.simulation import step_world
from alife_biosphere.world import World


def _habitat_entries(config: SimulationConfig) -> list[dict[str, object]]:
    habitats = []
    for habitat in sorted(config.world.habitats, key=lambda item: item.habitat_id):
        layout = DEFAULT_LAYOUT.get(habitat.habitat_id, {"x": 100, "y": 100, "w": 160, "h": 100})
        habitats.append(
            {
                "habitat_id": habitat.habitat_id,
                "habitat_family": habitat.habitat_family,
                "x": layout["x"],
                "y": layout["y"],
                "w": layout["w"],
                "h": layout["h"],
            }
        )
    return habitats


def _base_summary(world: World) -> dict[str, object]:
    return {
        "alive": world.alive_count(),
        "movement_count": 0,
        "birth_count": 0,
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
        "lineages_by_habitat": world.living_lineages_by_habitat(),
        "occupancy_pressure_by_habitat": {habitat_id: 0.0 for habitat_id in world.habitats},
        "lineage_count": len({organism.lineage_id for organism in world.organisms.values() if organism.alive}),
    }


def _frame_payload(
    habitats: list[dict[str, object]],
    world: World,
    tick_summary_payload: dict[str, object],
    tick: int,
) -> dict[str, object]:
    def event_dicts(event_type: str) -> list[dict[str, object]]:
        return [
            event.to_dict()
            for event in world.events
            if event.tick == tick and event.event_type == event_type
        ]

    birth_ids = {event["organism_id"] for event in event_dicts("birth") if event["organism_id"] is not None}
    move_ids = {event["organism_id"] for event in event_dicts("move") if event["organism_id"] is not None}
    organisms_by_habitat: dict[str, list[dict[str, object]]] = {habitat["habitat_id"]: [] for habitat in habitats}
    for organism in world.organisms.values():
        if not organism.alive:
            continue
        organisms_by_habitat[organism.habitat_id].append(
            {
                "organism_id": organism.organism_id,
                "lineage_id": organism.lineage_id,
                "generation": organism.generation,
                "age": organism.age,
                "just_born": organism.organism_id in birth_ids,
                "just_moved": organism.organism_id in move_ids,
            }
        )

    habitats_payload: dict[str, dict[str, object]] = {}
    for habitat_id, occupancy in tick_summary_payload["occupancy_by_habitat"].items():
        habitats_payload[habitat_id] = {
            "occupancy": occupancy,
            "pressure": tick_summary_payload["occupancy_pressure_by_habitat"][habitat_id],
            "lineages": tick_summary_payload["lineages_by_habitat"][habitat_id],
        }

    return {
        "tick": tick,
        "alive": tick_summary_payload["alive"],
        "movement_count": tick_summary_payload["movement_count"],
        "birth_count": tick_summary_payload["birth_count"],
        "reproduction_ready_count": tick_summary_payload["reproduction_ready_count"],
        "refuge_occupancy": tick_summary_payload["refuge_occupancy"],
        "lineage_count": tick_summary_payload["lineage_count"],
        "disturbances": event_dicts("disturbance"),
        "births": event_dicts("birth"),
        "deaths": event_dicts("death"),
        "moves": event_dicts("move"),
        "organisms": build_positioned_organisms(habitats, organisms_by_habitat),
        "habitats": habitats_payload,
    }


def _state_payload(
    config: SimulationConfig,
    habitats: list[dict[str, object]],
    world: World,
    tick_summary_payload: dict[str, object],
    running: bool,
    complete: bool,
) -> dict[str, object]:
    return {
        "title": "Alife Biosphere Live World",
        "running": running,
        "complete": complete,
        "total_ticks": config.world.ticks,
        "habitats": habitats,
        "edges": [{"from": left, "to": right} for left, right in config.world.habitat_edges],
        "frame": _frame_payload(habitats, world, tick_summary_payload, world.tick),
    }


def _render_html(state: dict[str, object]) -> str:
    state_json = json.dumps(state)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{state["title"]}</title>
  <style>
    :root {{
      --bg: #f5eee1;
      --panel: rgba(255, 249, 241, 0.76);
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
    .statusbar {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin: 16px 0 10px;
      font-family: "SF Mono", "Menlo", "Consolas", monospace;
      font-size: 13px;
      color: var(--muted);
    }}
    .pill {{
      border-radius: 999px;
      padding: 8px 12px;
      background: rgba(27, 77, 62, 0.1);
      color: var(--accent);
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
    .legend span {{ display: inline-flex; align-items: center; gap: 6px; }}
    .legend-dot {{ width: 10px; height: 10px; border-radius: 999px; display: inline-block; }}
    svg {{
      width: 100%;
      height: auto;
      border-radius: 22px;
      background:
        linear-gradient(180deg, rgba(255,255,255,0.52), rgba(246, 237, 224, 0.9)),
        repeating-linear-gradient(0deg, transparent, transparent 34px, rgba(42, 33, 24, 0.03) 34px, rgba(42, 33, 24, 0.03) 35px),
        repeating-linear-gradient(90deg, transparent, transparent 34px, rgba(42, 33, 24, 0.03) 34px, rgba(42, 33, 24, 0.03) 35px);
    }}
    .edge {{ stroke: rgba(64, 49, 34, 0.18); stroke-width: 10; stroke-linecap: round; fill: none; }}
    .region {{ stroke: rgba(42, 30, 20, 0.16); stroke-width: 3; }}
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
    .organism {{ fill: #231c16; opacity: 0.92; }}
    .organism.moved {{ stroke: rgba(255,255,255,0.92); stroke-width: 1.8; }}
    .organism.born {{ stroke: var(--birth); stroke-width: 2.2; }}
    .birth-ring {{ fill: none; stroke: rgba(42, 143, 98, 0.82); stroke-width: 2; }}
    .death-marker {{ stroke: rgba(92, 43, 39, 0.92); stroke-width: 2.4; stroke-linecap: round; }}
    .disturbance-pulse {{ fill: rgba(197, 58, 47, 0.12); stroke: rgba(197, 58, 47, 0.78); stroke-width: 3; }}
    .cards {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }}
    .card {{ border-radius: 18px; padding: 12px; background: rgba(250, 245, 238, 0.92); border: 1px solid rgba(48, 36, 25, 0.08); }}
    .card h3 {{ margin: 0 0 8px; font-size: 13px; color: var(--muted); font-family: "SF Mono", "Menlo", "Consolas", monospace; font-weight: 600; }}
    .card strong {{ display: block; font-size: 26px; line-height: 1; }}
    .section-title {{ margin: 0 0 8px; font-size: 14px; font-family: "SF Mono", "Menlo", "Consolas", monospace; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; }}
    .scroll-list {{ display: flex; flex-direction: column; gap: 8px; max-height: 260px; overflow: auto; padding-right: 4px; }}
    .log-row {{ border-radius: 14px; padding: 10px 12px; background: rgba(250, 245, 238, 0.92); border: 1px solid rgba(48, 36, 25, 0.08); font-size: 13px; line-height: 1.4; }}
    .habitat-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    .habitat-table th, .habitat-table td {{ padding: 8px 0; border-bottom: 1px solid rgba(48, 36, 25, 0.08); text-align: left; vertical-align: top; }}
    .habitat-table th {{ color: var(--muted); font-family: "SF Mono", "Menlo", "Consolas", monospace; font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; }}
    .tiny {{ font-size: 11px; color: var(--muted); font-family: "SF Mono", "Menlo", "Consolas", monospace; }}
    @media (max-width: 980px) {{
      .shell {{ flex-direction: column; }}
      .panel {{ width: 100%; }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <section class="stage">
      <h1 class="title">{state["title"]}</h1>
      <p class="subtitle">A living-world window for watching organisms move through regions while the experiment advances.</p>
      <div class="statusbar">
        <span class="pill" id="tick-label"></span>
        <span class="pill" id="run-state"></span>
        <span class="pill" id="reload-note"></span>
      </div>
      <div class="legend">
        <span><i class="legend-dot" style="background: var(--nursery)"></i>nursery</span>
        <span><i class="legend-dot" style="background: var(--refuge)"></i>refuge</span>
        <span><i class="legend-dot" style="background: var(--frontier)"></i>frontier</span>
        <span><i class="legend-dot" style="background: var(--wild)"></i>wild</span>
        <span><i class="legend-dot" style="background: var(--birth)"></i>birth</span>
        <span><i class="legend-dot" style="background: var(--disturb)"></i>disturbance</span>
      </div>
      <svg id="map" viewBox="0 0 920 460" role="img" aria-label="Live ecology observer map"></svg>
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
  <script id="live-state" type="application/json">{state_json}</script>
  <script>
    const state = JSON.parse(document.getElementById('live-state').textContent);
    const familyColor = {{
      nursery: 'var(--nursery)',
      refuge: 'var(--refuge)',
      frontier: 'var(--frontier)',
      wild: 'var(--wild)',
    }};
    const svg = document.getElementById('map');
    const tickLabel = document.getElementById('tick-label');
    const runState = document.getElementById('run-state');
    const reloadNote = document.getElementById('reload-note');
    const aliveEl = document.getElementById('alive');
    const birthsEl = document.getElementById('births');
    const movesEl = document.getElementById('moves');
    const lineagesEl = document.getElementById('lineages');
    const disturbanceLog = document.getElementById('disturbance-log');
    const habitatTable = document.getElementById('habitat-table');

    function lineageColor(lineageId) {{
      let hash = 0;
      for (let i = 0; i < lineageId.length; i += 1) {{
        hash = ((hash << 5) - hash + lineageId.charCodeAt(i)) | 0;
      }}
      const hue = Math.abs(hash) % 360;
      return `hsl(${{hue}} 64% 42%)`;
    }}

    const habitatMap = Object.fromEntries(state.habitats.map(item => [item.habitat_id, item]));
    state.edges.forEach(edge => {{
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

    const regionEls = Object.fromEntries(state.habitats.map(item => {{
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
      return [item.habitat_id, {{ region, label, meta }}];
    }}));

    const frame = state.frame;
    tickLabel.textContent = `Tick ${{frame.tick}} / ${{state.total_ticks}}`;
    runState.textContent = state.complete ? 'Complete' : (state.running ? 'Running' : 'Preparing');
    reloadNote.textContent = state.complete ? 'Live run finished' : 'Auto-refresh every 450ms';
    aliveEl.textContent = frame.alive;
    birthsEl.textContent = frame.birth_count;
    movesEl.textContent = frame.movement_count;
    lineagesEl.textContent = frame.lineage_count;

    const disturbed = new Set(frame.disturbances.map(item => item.habitat_id));
    state.habitats.forEach(habitat => {{
      const entry = frame.habitats[habitat.habitat_id];
      const region = regionEls[habitat.habitat_id];
      const occupancy = entry.occupancy;
      region.region.setAttribute('fill-opacity', occupancy === 0 ? '0.12' : String(Math.min(0.18 + occupancy * 0.06, 0.44)));
      region.region.setAttribute('stroke', disturbed.has(habitat.habitat_id) ? 'rgba(197, 58, 47, 0.88)' : 'rgba(42, 30, 20, 0.16)');
      region.region.setAttribute('stroke-width', disturbed.has(habitat.habitat_id) ? '4' : '3');
      region.label.textContent = habitat.habitat_id.replace('_', ' ').toUpperCase();
      region.meta.textContent = `${{occupancy}} alive · ${{entry.lineages.length}} lineages`;
    }});

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
    Object.entries(deathByHabitat).forEach(([habitatId, count]) => {{
      const habitat = habitatMap[habitatId];
      if (!habitat) return;
      for (let i = 0; i < count; i += 1) {{
        const dx = (i - (count - 1) / 2) * 12;
        const x = habitat.x + dx;
        const y = habitat.y - habitat.h / 2 - 10;
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
    logs.forEach(item => {{
      const row = document.createElement('div');
      row.className = 'log-row';
      row.innerHTML = `<strong>${{item}}</strong>`;
      disturbanceLog.appendChild(row);
    }});

    habitatTable.innerHTML = '';
    state.habitats.forEach(habitat => {{
      const entry = frame.habitats[habitat.habitat_id];
      const row = document.createElement('tr');
      row.innerHTML = `
        <td><strong>${{habitat.habitat_id}}</strong><div class="tiny">${{habitat.habitat_family}}</div></td>
        <td>${{entry.occupancy}} · ${{entry.pressure.toFixed(2)}}</td>
        <td>${{entry.lineages.length ? entry.lineages.join(', ') : '—'}}</td>
      `;
      habitatTable.appendChild(row);
    }});

    if (!state.complete) {{
      setTimeout(() => location.reload(), 450);
    }}
  </script>
</body>
</html>"""


def _write_atomic(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def _write_live_files(output_dir: Path, state: dict[str, object]) -> None:
    _write_atomic(output_dir / "live_observer.html", _render_html(state))
    _write_atomic(output_dir / "state.json", json.dumps(state, indent=2))


def main() -> None:
    config = SimulationConfig(
        world=WorldConfig(
            ticks=40,
            founder_count=10,
            disturbance_interval=8,
            disturbance_resource_shock=2.0,
            disturbance_hazard_pulse=0.12,
            senescence_age=24,
            max_age=50,
        )
    )
    habitats = _habitat_entries(config)
    output_dir = ROOT / "outputs" / "live_observer"
    output_dir.mkdir(parents=True, exist_ok=True)

    world = World.from_config(config.world)
    initial_state = _state_payload(
        config,
        habitats,
        world,
        _base_summary(world),
        running=False,
        complete=False,
    )
    _write_live_files(output_dir, initial_state)
    html_path = output_dir / "live_observer.html"
    print({"html": str(html_path), "ticks": config.world.ticks})

    time.sleep(0.6)
    for tick in range(1, config.world.ticks + 1):
        summary_payload = step_world(world, config.world, tick)
        _write_live_files(
            output_dir,
            _state_payload(
                config,
                habitats,
                world,
                summary_payload,
                running=True,
                complete=False,
            ),
        )
        time.sleep(0.45)

    final_summary = next(
        event.payload
        for event in reversed(world.events)
        if event.event_type == "tick_summary"
    )
    _write_live_files(
        output_dir,
        _state_payload(
            config,
            habitats,
            world,
            final_summary,
            running=False,
            complete=True,
        ),
    )
    print("Live observer export complete.")


if __name__ == "__main__":
    main()
