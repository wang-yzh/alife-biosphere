import json
import math
from pathlib import Path

from alife_biosphere.ant_sandbox import AntSandboxConfig
from alife_biosphere.ant_sandbox.observer import build_ant_observer_payload, write_ant_observer_html


def test_ant_sandbox_observer_payload_contains_world_frames() -> None:
    payload = build_ant_observer_payload(AntSandboxConfig(ticks=40), title="Ant Observer")
    assert payload["width"] == 128
    assert payload["height"] == 96
    assert payload["total_ticks"] == 40
    assert payload["generated_at"]
    assert payload["terrain"]
    assert payload["frames"]
    first = payload["frames"][0]
    assert "ants" in first
    assert "food_patches" in first
    assert "food_trail" in first
    assert "home_trail" in first
    assert "terrain_kind" in first["ants"][0]
    assert "competition_pressure" in first["food_patches"][0]
    assert "nearby_ants" in first["food_patches"][0]


def test_ant_sandbox_observer_html_writes_canvas_window(tmp_path: Path) -> None:
    payload = build_ant_observer_payload(AntSandboxConfig(ticks=20), title="Ant Observer")
    output = tmp_path / "observer.html"
    write_ant_observer_html(output, payload)
    html = output.read_text(encoding="utf-8")
    assert "<canvas id=\"world\"" in html
    assert "observer-data" in html
    assert "Ant Observer" in html


def test_ant_sandbox_showcase_world_keeps_all_ants_alive_to_tick_239() -> None:
    payload = build_ant_observer_payload(AntSandboxConfig(ticks=240), title="Ant Observer")
    frame_239 = payload["frames"][238]
    assert frame_239["alive"] == 32


def test_ant_sandbox_showcase_avoids_right_side_nest_pileup() -> None:
    payload = build_ant_observer_payload(AntSandboxConfig(ticks=240), title="Ant Observer")
    frame_211 = payload["frames"][210]
    nest_x = payload["nest"]["x"]
    nest_y = payload["nest"]["y"]
    near = [
        ant
        for ant in frame_211["ants"]
        if math.dist((ant["x"], ant["y"]), (nest_x, nest_y)) <= 10
    ]
    east_sector = [
        ant
        for ant in near
        if -math.pi / 4 <= math.atan2(ant["y"] - nest_y, ant["x"] - nest_x) < math.pi / 4
    ]
    assert len(near) <= 10
    assert len(east_sector) <= 6
