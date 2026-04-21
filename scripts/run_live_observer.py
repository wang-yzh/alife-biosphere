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
from alife_biosphere.observer import DEFAULT_LAYOUT
from alife_biosphere.simulation import step_world
from alife_biosphere.world import World


def _build_tick_zero_payload(world: World) -> dict[str, object]:
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
        "occupancy_pressure_by_habitat": {
            habitat_id: 0.0 for habitat_id in world.habitats
        },
        "lineage_count": len(
            {
                organism.lineage_id
                for organism in world.organisms.values()
                if organism.alive
            }
        ),
    }


def _frame_payload(world: World, tick_summary_payload: dict[str, object], tick: int) -> dict[str, object]:
    def event_dicts(event_type: str) -> list[dict[str, object]]:
        return [
            event.to_dict()
            for event in world.events
            if event.tick == tick and event.event_type == event_type
        ]

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
        "habitats": habitats_payload,
    }


def _state_payload(
    config: SimulationConfig,
    world: World,
    tick_summary_payload: dict[str, object],
    running: bool,
    complete: bool,
) -> dict[str, object]:
    habitats = []
    for habitat in config.world.habitats:
        layout = DEFAULT_LAYOUT.get(habitat.habitat_id, {"x": 100, "y": 100})
        habitats.append(
            {
                "habitat_id": habitat.habitat_id,
                "habitat_family": habitat.habitat_family,
                "x": layout["x"],
                "y": layout["y"],
            }
        )
    return {
        "title": "Alife Biosphere Live Sandbox",
        "running": running,
        "complete": complete,
        "total_ticks": config.world.ticks,
        "habitats": habitats,
        "edges": [{"from": left, "to": right} for left, right in config.world.habitat_edges],
        "frame": _frame_payload(world, tick_summary_payload, world.tick),
    }


def _render_live_html(state: dict[str, object]) -> str:
    state_json = json.dumps(state)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{state["title"]}</title>
  <style>
    :root {{
      --bg: #f4efe6;
      --panel: rgba(255, 250, 242, 0.92);
      --ink: #1e1b17;
      --muted: #665f57;
      --line: rgba(42, 33, 24, 0.18);
      --nursery: #9bcf8b;
      --refuge: #7db7a4;
      --frontier: #caa35e;
      --wild: #b66a4d;
      --disturb: #c53a2f;
      --accent: #1b4d3e;
      --shadow: 0 16px 40px rgba(36, 27, 17, 0.12);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background:
        radial-gradient(circle at top left, rgba(155, 207, 139, 0.16), transparent 28%),
        radial-gradient(circle at top right, rgba(182, 106, 77, 0.14), transparent 24%),
        linear-gradient(180deg, #f7f1e8 0%, #f0e7db 100%);
      color: var(--ink);
      font-family: "Iowan Old Style", "Palatino Linotype", "Book Antiqua", Georgia, serif;
    }}
    .shell {{
      min-height: 100vh;
      display: grid;
      grid-template-columns: minmax(560px, 1.3fr) minmax(340px, 0.7fr);
      gap: 20px;
      padding: 24px;
    }}
    .stage, .panel {{
      background: var(--panel);
      border: 1px solid rgba(59, 45, 32, 0.08);
      border-radius: 24px;
      box-shadow: var(--shadow);
      backdrop-filter: blur(10px);
    }}
    .stage {{ padding: 18px; }}
    .panel {{ padding: 22px; display: flex; flex-direction: column; gap: 18px; }}
    .title {{ margin: 0 0 6px; font-size: 30px; line-height: 1.05; letter-spacing: 0.02em; }}
    .subtitle {{ margin: 0; font-size: 14px; color: var(--muted); }}
    .statusbar {{
      display: flex; gap: 12px; align-items: center; flex-wrap: wrap;
      margin: 18px 0 12px;
      font-family: "SF Mono", "Menlo", "Consolas", monospace;
      font-size: 13px;
      color: var(--muted);
    }}
    .pill {{
      border-radius: 999px; padding: 8px 12px;
      background: rgba(27, 77, 62, 0.1); color: var(--accent);
    }}
    .legend {{
      display: flex; gap: 12px; flex-wrap: wrap; font-size: 12px; color: var(--muted);
      margin-bottom: 12px; font-family: "SF Mono", "Menlo", "Consolas", monospace;
    }}
    .legend span {{ display: inline-flex; align-items: center; gap: 6px; }}
    .legend-dot {{ width: 10px; height: 10px; border-radius: 999px; display: inline-block; }}
    svg {{
      width: 100%; height: auto; border-radius: 18px;
      background:
        linear-gradient(180deg, rgba(255,255,255,0.65), rgba(247, 240, 229, 0.9)),
        repeating-linear-gradient(0deg, transparent, transparent 28px, rgba(42, 33, 24, 0.035) 28px, rgba(42, 33, 24, 0.035) 29px),
        repeating-linear-gradient(90deg, transparent, transparent 28px, rgba(42, 33, 24, 0.035) 28px, rgba(42, 33, 24, 0.035) 29px);
    }}
    .edge {{ stroke: rgba(60, 47, 35, 0.22); stroke-width: 6; stroke-linecap: round; }}
    .node-core {{ stroke: rgba(40, 29, 20, 0.22); stroke-width: 2; }}
    .node-ring {{ fill: none; stroke: transparent; stroke-width: 6; }}
    .node-label {{ font-size: 13px; text-anchor: middle; font-family: "SF Mono", "Menlo", "Consolas", monospace; fill: rgba(31, 24, 18, 0.9); }}
    .node-meta {{ font-size: 11px; text-anchor: middle; font-family: "SF Mono", "Menlo", "Consolas", monospace; fill: rgba(90, 74, 60, 0.88); }}
    .cards {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }}
    .card {{ border-radius: 18px; padding: 14px; background: rgba(250, 245, 238, 0.92); border: 1px solid rgba(48, 36, 25, 0.08); }}
    .card h3 {{ margin: 0 0 8px; font-size: 13px; color: var(--muted); font-family: "SF Mono", "Menlo", "Consolas", monospace; font-weight: 600; }}
    .card strong {{ display: block; font-size: 28px; line-height: 1; }}
    .section-title {{ margin: 0 0 8px; font-size: 14px; font-family: "SF Mono", "Menlo", "Consolas", monospace; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; }}
    .scroll-list {{ display: flex; flex-direction: column; gap: 8px; max-height: 260px; overflow: auto; padding-right: 4px; }}
    .log-row {{ border-radius: 14px; padding: 10px 12px; background: rgba(250, 245, 238, 0.92); border: 1px solid rgba(48, 36, 25, 0.08); font-size: 13px; line-height: 1.4; }}
    .habitat-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    .habitat-table th, .habitat-table td {{ padding: 8px 0; border-bottom: 1px solid rgba(48, 36, 25, 0.08); text-align: left; vertical-align: top; }}
    .habitat-table th {{ color: var(--muted); font-family: "SF Mono", "Menlo", "Consolas", monospace; font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; }}
    .tiny {{ font-size: 11px; color: var(--muted); font-family: "SF Mono", "Menlo", "Consolas", monospace; }}
    @media (max-width: 980px) {{ .shell {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <div class="shell">
    <section class="stage">
      <h1 class="title">{state["title"]}</h1>
      <p class="subtitle">Open this file once in your browser and it will refresh itself as the simulation advances.</p>
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
        <span><i class="legend-dot" style="background: var(--disturb)"></i>disturbance pulse</span>
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
        <h2 class="section-title">Recent Disturbance</h2>
        <div id="disturbance-log" class="scroll-list"></div>
      </section>
      <section>
        <h2 class="section-title">Habitat State</h2>
        <table class="habitat-table">
          <thead>
            <tr><th>Habitat</th><th>Occ</th><th>Pressure</th><th>Lineages</th></tr>
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

    const habitatMap = Object.fromEntries(state.habitats.map(item => [item.habitat_id, item]));
    state.edges.forEach(edge => {{
      const from = habitatMap[edge.from];
      const to = habitatMap[edge.to];
      const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      line.setAttribute('x1', from.x);
      line.setAttribute('y1', from.y);
      line.setAttribute('x2', to.x);
      line.setAttribute('y2', to.y);
      line.setAttribute('class', 'edge');
      svg.appendChild(line);
    }});

    const nodeEls = Object.fromEntries(state.habitats.map(item => {{
      const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      const ring = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      ring.setAttribute('cx', item.x);
      ring.setAttribute('cy', item.y);
      ring.setAttribute('r', 38);
      ring.setAttribute('class', 'node-ring');
      const core = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      core.setAttribute('cx', item.x);
      core.setAttribute('cy', item.y);
      core.setAttribute('r', 30);
      core.setAttribute('class', 'node-core');
      core.setAttribute('fill', familyColor[item.habitat_family]);
      const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      label.setAttribute('x', item.x);
      label.setAttribute('y', item.y - 2);
      label.setAttribute('class', 'node-label');
      const meta = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      meta.setAttribute('x', item.x);
      meta.setAttribute('y', item.y + 16);
      meta.setAttribute('class', 'node-meta');
      group.appendChild(ring);
      group.appendChild(core);
      group.appendChild(label);
      group.appendChild(meta);
      svg.appendChild(group);
      return [item.habitat_id, {{ ring, core, label, meta }}];
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
      const node = nodeEls[habitat.habitat_id];
      const occupancy = entry.occupancy;
      node.core.setAttribute('r', String(24 + occupancy * 7));
      node.core.setAttribute('opacity', occupancy === 0 ? '0.38' : '0.95');
      node.ring.setAttribute('stroke', disturbed.has(habitat.habitat_id) ? 'var(--disturb)' : 'transparent');
      node.ring.setAttribute('opacity', disturbed.has(habitat.habitat_id) ? '0.85' : '0');
      node.label.textContent = `${{habitat.habitat_id}} · ${{occupancy}}`;
      const lineageLabel = entry.lineages.length ? entry.lineages.join(', ') : 'empty';
      node.meta.textContent = lineageLabel.length > 22 ? lineageLabel.slice(0, 22) + '…' : lineageLabel;
    }});

    disturbanceLog.innerHTML = '';
    const logs = frame.disturbances.length ? frame.disturbances : [{{
      habitat_id: 'none',
      payload: {{ resource_loss: 0, hazard_pulse: 0 }},
    }}];
    logs.forEach(item => {{
      const row = document.createElement('div');
      row.className = 'log-row';
      if (item.habitat_id === 'none') {{
        row.innerHTML = `<strong>No disturbance</strong><div class="tiny">Quiet tick</div>`;
      }} else {{
        row.innerHTML = `<strong>${{item.habitat_id}}</strong><div class="tiny">resource_loss=${{item.payload.resource_loss}} · hazard_pulse=${{item.payload.hazard_pulse}}</div>`;
      }}
      disturbanceLog.appendChild(row);
    }});

    habitatTable.innerHTML = '';
    state.habitats.forEach(habitat => {{
      const entry = frame.habitats[habitat.habitat_id];
      const row = document.createElement('tr');
      row.innerHTML = `
        <td><strong>${{habitat.habitat_id}}</strong><div class="tiny">${{habitat.habitat_family}}</div></td>
        <td>${{entry.occupancy}}</td>
        <td>${{entry.pressure.toFixed(2)}}</td>
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
    _write_atomic(output_dir / "live_observer.html", _render_live_html(state))
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
    output_dir = ROOT / "outputs" / "live_observer"
    output_dir.mkdir(parents=True, exist_ok=True)

    world = World.from_config(config.world)
    initial_state = _state_payload(
        config,
        world,
        _build_tick_zero_payload(world),
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
            world,
            final_summary,
            running=False,
            complete=True,
        ),
    )
    print("Live observer export complete.")


if __name__ == "__main__":
    main()
