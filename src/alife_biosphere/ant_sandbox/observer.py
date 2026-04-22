from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .config import AntSandboxConfig
from .simulation import step_world
from .world import AntSandboxWorld, initialize_world, terrain_kind


def _trail_points(field: dict[tuple[int, int], float], minimum: float = 0.04) -> list[dict[str, float]]:
    return [
        {"x": float(x), "y": float(y), "value": round(value, 4)}
        for (x, y), value in sorted(field.items())
        if value >= minimum
    ]


def _terrain_points(world: AntSandboxWorld) -> list[dict[str, object]]:
    return [
        {"x": x, "y": y, "kind": kind}
        for (x, y), kind in sorted(world.terrain.items(), key=lambda item: (item[0][1], item[0][0]))
    ]


def _event_dicts(world: AntSandboxWorld, tick: int, event_type: str) -> list[dict[str, object]]:
    return [
        event.to_dict()
        for event in world.events
        if event.tick == tick and event.event_type == event_type
    ]


def _frame_payload(world: AntSandboxWorld, summary: dict[str, int], tick: int) -> dict[str, object]:
    ants = [
        {
            "ant_id": ant.ant_id,
            "x": ant.x,
            "y": ant.y,
            "heading": ant.heading,
            "terrain_kind": terrain_kind(world, ant.x, ant.y),
            "carrying_food": ant.carrying_food,
            "target_patch_id": ant.target_patch_id,
            "outbound_commit_ticks": ant.outbound_commit_ticks,
            "delivered_food": ant.delivered_food,
            "age": ant.age,
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
            "nearby_ants": patch.nearby_ants,
            "carrying_nearby": patch.carrying_nearby,
            "competition_pressure": patch.competition_pressure,
            "contested_ticks": patch.contested_ticks,
            "depletion_count": patch.depletion_count,
        }
        for patch in world.food_patches
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
        "ants": ants,
        "food_patches": food_patches,
        "food_trail": _trail_points(world.food_trail),
        "home_trail": _trail_points(world.home_trail),
        "birth_events": _event_dicts(world, tick, "ant_birth"),
        "death_events": _event_dicts(world, tick, "ant_death"),
        "pickup_events": _event_dicts(world, tick, "food_pickup"),
        "unload_events": _event_dicts(world, tick, "food_unload"),
        "reseed_events": _event_dicts(world, tick, "food_patch_reseed"),
        "upkeep_events": _event_dicts(world, tick, "nest_upkeep"),
        "contested_source_events": _event_dicts(world, tick, "food_source_contested"),
        "depleted_source_events": _event_dicts(world, tick, "food_source_depleted"),
    }


def build_ant_observer_payload(
    config: AntSandboxConfig,
    title: str = "Ant Sandbox World",
) -> dict[str, object]:
    world = initialize_world(config)
    frames = []
    for tick in range(1, config.ticks + 1):
        summary = step_world(world, config, tick)
        frames.append(_frame_payload(world, summary, tick))
    return {
        "title": title,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "width": config.width,
        "height": config.height,
        "total_ticks": config.ticks,
        "terrain": _terrain_points(world),
        "nest": {
            "x": world.nest.x,
            "y": world.nest.y,
            "radius": world.nest.radius,
        },
        "frames": frames,
    }


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
      --dense-grass: rgba(106, 141, 84, 0.42);
      --sand: rgba(214, 184, 129, 0.44);
      --rock: rgba(92, 86, 81, 0.78);
      --birth: rgba(51, 165, 116, 0.9);
      --death: rgba(156, 52, 43, 0.86);
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
        <span><i class="dot" style="background: var(--food-trail)"></i>food trail</span>
        <span><i class="dot" style="background: var(--home-trail)"></i>home trail</span>
      </div>
      <canvas id="world" width="960" height="720"></canvas>
    </section>
    <aside class="panel">
      <div class="cards">
        <div class="card"><h3>Alive</h3><strong id="alive"></strong></div>
        <div class="card"><h3>Nest Food</h3><strong id="nest-food"></strong></div>
        <div class="card"><h3>Carrying</h3><strong id="carrying"></strong></div>
        <div class="card"><h3>Food Left</h3><strong id="food-left"></strong></div>
      </div>
      <section class="section">
        <h2>Moment</h2>
        <div id="moment-log" class="log"></div>
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
    const generatedAtEl = document.getElementById('generated-at');
    const momentLog = document.getElementById('moment-log');
    const selectedAntEl = document.getElementById('selected-ant');

    const widthScale = canvas.width / data.width;
    const heightScale = canvas.height / data.height;
    const terrainPalette = {{
      dense_grass: 'rgba(106, 141, 84, 0.42)',
      sand: 'rgba(214, 184, 129, 0.44)',
      rock: 'rgba(92, 86, 81, 0.78)',
    }};

    let index = 0;
    let playing = false;
    let timer = null;
    const frames = data.frames;
    let hoverAntId = null;
    let pinnedAntId = null;

    generatedAtEl.textContent = `Generated ${{data.generated_at}}${{data.live ? ' · live export' : ''}}`;

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

    function drawTrails(frame) {{
      for (const point of frame.home_trail) {{
        ctx.fillStyle = `rgba(217, 153, 72, ${{Math.min(0.30, point.value / 8)}})`;
        ctx.beginPath();
        ctx.arc(toCanvasX(point.x), toCanvasY(point.y), 4 + point.value * 1.2, 0, Math.PI * 2);
        ctx.fill();
      }}
      for (const point of frame.food_trail) {{
        ctx.fillStyle = `rgba(64, 163, 120, ${{Math.min(0.34, point.value / 8)}})`;
        ctx.beginPath();
        ctx.arc(toCanvasX(point.x), toCanvasY(point.y), 4 + point.value * 1.2, 0, Math.PI * 2);
        ctx.fill();
      }}
    }}

    function drawNest() {{
      const x = toCanvasX(data.nest.x);
      const y = toCanvasY(data.nest.y);
      ctx.fillStyle = 'rgba(126, 94, 66, 0.14)';
      ctx.beginPath();
      ctx.arc(x, y, (data.nest.radius + 4.5) * widthScale, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = 'rgba(126, 94, 66, 0.96)';
      ctx.beginPath();
      ctx.arc(x, y, (data.nest.radius + 1.8) * widthScale, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = 'rgba(255, 246, 235, 0.92)';
      ctx.beginPath();
      ctx.arc(x, y, (data.nest.radius + 0.7) * widthScale, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#4d3726';
      ctx.beginPath();
      ctx.arc(x, y, data.nest.radius * widthScale, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = 'rgba(255, 248, 239, 0.84)';
      ctx.lineWidth = 2.2;
      ctx.beginPath();
      ctx.moveTo(x + (data.nest.radius + 0.8) * widthScale, y);
      ctx.lineTo(x + (data.nest.radius + 3.1) * widthScale, y);
      ctx.stroke();
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
        ctx.fillText(`${{patch.amount}} · ${{patch.nearby_ants}}`, toCanvasX(patch.x) - 18, toCanvasY(patch.y) + 4);
      }}
    }}

    function antColor(ant) {{
      if (ant.carrying_food) return '#d8893c';
      let hash = 0;
      for (let i = 0; i < ant.ant_id.length; i += 1) {{
        hash = ((hash << 5) - hash + ant.ant_id.charCodeAt(i)) | 0;
      }}
      const hue = Math.abs(hash) % 360;
      return `hsl(${{hue}} 30% 22%)`;
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
      drawTrails(frame);
      drawFood(frame);
      drawNest();
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
      drawFrame(frame);
      momentLog.innerHTML = '';
      const logItems = [];
      if (frame.pickups) logItems.push(`food pickups +${{frame.pickups}}`);
      if (frame.unloads) logItems.push(`nest unloads +${{frame.unloads}}`);
      if (frame.upkeep_events.length) logItems.push(`nest upkeep -${{frame.upkeep_events.reduce((sum, event) => sum + event.payload.consumed, 0)}}`);
      if (frame.reseed_events.length) logItems.push(`food reseeds +${{frame.reseed_events.length}}`);
      if (frame.contested_source_events.length) logItems.push(`source contests +${{frame.contested_source_events.length}}`);
      if (frame.depleted_source_events.length) logItems.push(`sources depleted +${{frame.depleted_source_events.length}}`);
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

      const selectedId = pinnedAntId || hoverAntId;
      const selected = selectedId ? frame.ants.find(ant => ant.ant_id === selectedId) : null;
      if (selected) {{
        selectedAntEl.innerHTML = `
          <strong>${{selected.ant_id}}</strong>
          <div class="tiny">pos = (${{selected.x}}, ${{selected.y}})</div>
          <div class="tiny">carrying = ${{selected.carrying_food ? 'yes' : 'no'}}</div>
          <div class="tiny">terrain = ${{selected.terrain_kind}}</div>
          <div class="tiny">target = ${{selected.target_patch_id || 'none'}}</div>
          <div class="tiny">outbound = ${{selected.outbound_commit_ticks}}</div>
          <div class="tiny">delivered = ${{selected.delivered_food}}</div>
          <div class="tiny">age = ${{selected.age}}</div>
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
    if (data.live) {{
      playButton.disabled = true;
      backButton.disabled = true;
      forwardButton.disabled = true;
      timeline.disabled = true;
      playButton.textContent = data.complete ? 'Done' : 'Live';
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
