from __future__ import annotations

import json
from pathlib import Path

from .config import SimulationConfig
from .events import Event
from .simulation import SimulationResult


DEFAULT_LAYOUT = {
    "nursery_a": {"x": 140, "y": 120},
    "nursery_b": {"x": 140, "y": 340},
    "refuge": {"x": 340, "y": 230},
    "frontier_a": {"x": 560, "y": 150},
    "frontier_b": {"x": 560, "y": 310},
    "wild_a": {"x": 780, "y": 110},
    "wild_b": {"x": 780, "y": 350},
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

    habitat_config = {habitat.habitat_id: habitat for habitat in config.world.habitats}
    habitats = []
    for habitat_id in sorted(habitat_config):
        layout = DEFAULT_LAYOUT.get(habitat_id, {"x": 100, "y": 100})
        habitats.append(
            {
                "habitat_id": habitat_id,
                "habitat_family": habitat_config[habitat_id].habitat_family,
                "x": layout["x"],
                "y": layout["y"],
            }
        )

    disturbances_by_tick = _event_dicts_by_tick(result.events, "disturbance")
    births_by_tick = _event_dicts_by_tick(result.events, "birth")
    deaths_by_tick = _event_dicts_by_tick(result.events, "death")
    moves_by_tick = _event_dicts_by_tick(result.events, "move")

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
        frames.append(
            {
                "tick": summary.tick,
                "alive": payload["alive"],
                "movement_count": payload["movement_count"],
                "birth_count": payload["birth_count"],
                "reproduction_ready_count": payload["reproduction_ready_count"],
                "refuge_occupancy": payload["refuge_occupancy"],
                "lineage_count": payload["lineage_count"],
                "disturbances": disturbances_by_tick.get(summary.tick, []),
                "births": births_by_tick.get(summary.tick, []),
                "deaths": deaths_by_tick.get(summary.tick, []),
                "moves": moves_by_tick.get(summary.tick, []),
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
      --bg: #f4efe6;
      --panel: rgba(255, 250, 242, 0.88);
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

    .stage {{
      padding: 18px;
    }}

    .panel {{
      padding: 22px;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }}

    .title {{
      margin: 0 0 6px;
      font-size: 30px;
      line-height: 1.05;
      letter-spacing: 0.02em;
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
      margin: 18px 0 12px;
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
      margin-bottom: 12px;
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
      border-radius: 18px;
      background:
        linear-gradient(180deg, rgba(255,255,255,0.65), rgba(247, 240, 229, 0.9)),
        repeating-linear-gradient(
          0deg,
          transparent,
          transparent 28px,
          rgba(42, 33, 24, 0.035) 28px,
          rgba(42, 33, 24, 0.035) 29px
        ),
        repeating-linear-gradient(
          90deg,
          transparent,
          transparent 28px,
          rgba(42, 33, 24, 0.035) 28px,
          rgba(42, 33, 24, 0.035) 29px
        );
    }}

    .edge {{
      stroke: rgba(60, 47, 35, 0.22);
      stroke-width: 6;
      stroke-linecap: round;
    }}

    .node-core {{
      stroke: rgba(40, 29, 20, 0.22);
      stroke-width: 2;
      transition: r 180ms ease, fill 180ms ease, opacity 180ms ease;
    }}

    .node-ring {{
      fill: none;
      stroke: transparent;
      stroke-width: 6;
      transition: stroke 180ms ease, opacity 180ms ease;
    }}

    .node-label {{
      font-size: 13px;
      text-anchor: middle;
      font-family: "SF Mono", "Menlo", "Consolas", monospace;
      fill: rgba(31, 24, 18, 0.9);
    }}

    .node-meta {{
      font-size: 11px;
      text-anchor: middle;
      font-family: "SF Mono", "Menlo", "Consolas", monospace;
      fill: rgba(90, 74, 60, 0.88);
    }}

    .cards {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }}

    .card {{
      border-radius: 18px;
      padding: 14px;
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
      font-size: 28px;
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
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <section class="stage">
      <h1 class="title">{payload["title"]}</h1>
      <p class="subtitle">A small, self-contained observer for occupancy, lineage presence, and disturbance across time.</p>
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
        <h2 class="section-title">Disturbance Log</h2>
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
    const edges = data.edges.map(edge => {{
      const from = habitatMap[edge.from];
      const to = habitatMap[edge.to];
      const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      line.setAttribute('x1', from.x);
      line.setAttribute('y1', from.y);
      line.setAttribute('x2', to.x);
      line.setAttribute('y2', to.y);
      line.setAttribute('class', 'edge');
      svg.appendChild(line);
      return line;
    }});

    const nodeEls = Object.fromEntries(data.habitats.map(item => {{
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
      return [item.habitat_id, {{ group, ring, core, label, meta }}];
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
        const node = nodeEls[habitat.habitat_id];
        const occupancy = state.occupancy;
        const radius = 24 + occupancy * 7;
        node.core.setAttribute('r', String(radius));
        node.core.setAttribute('fill', familyColor[habitat.habitat_family]);
        node.core.setAttribute('opacity', occupancy === 0 ? '0.38' : '0.95');
        node.ring.setAttribute('stroke', disturbedHabitats.has(habitat.habitat_id) ? 'var(--disturb)' : 'transparent');
        node.ring.setAttribute('opacity', disturbedHabitats.has(habitat.habitat_id) ? '0.85' : '0');
        node.label.textContent = `${{habitat.habitat_id}} · ${{occupancy}}`;
        const lineageLabel = state.lineages.length ? state.lineages.join(', ') : 'empty';
        node.meta.textContent = lineageLabel.length > 22 ? lineageLabel.slice(0, 22) + '…' : lineageLabel;
      }}

      disturbanceLog.innerHTML = '';
      const logs = frame.disturbances.length ? frame.disturbances : [{{
        habitat_id: 'none',
        payload: {{ resource_loss: 0, hazard_pulse: 0 }},
      }}];
      for (const item of logs) {{
        const row = document.createElement('div');
        row.className = 'log-row';
        if (item.habitat_id === 'none') {{
          row.innerHTML = `<strong>No disturbance</strong><div class="tiny">Quiet tick</div>`;
        }} else {{
          row.innerHTML = `<strong>${{item.habitat_id}}</strong><div class="tiny">resource_loss=${{item.payload.resource_loss}} · hazard_pulse=${{item.payload.hazard_pulse}}</div>`;
        }}
        disturbanceLog.appendChild(row);
      }}

      habitatTable.innerHTML = '';
      for (const habitat of data.habitats) {{
        const state = frame.habitats[habitat.habitat_id];
        const row = document.createElement('tr');
        const lineageText = state.lineages.length ? state.lineages.join(', ') : '—';
        row.innerHTML = `
          <td><strong>${{habitat.habitat_id}}</strong><div class="tiny">${{habitat.habitat_family}}</div></td>
          <td>${{state.occupancy}}</td>
          <td>${{state.pressure.toFixed(2)}}</td>
          <td>${{lineageText}}</td>
        `;
        habitatTable.appendChild(row);
      }}
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
