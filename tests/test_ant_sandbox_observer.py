import json
from pathlib import Path

from alife_biosphere.ant_sandbox import AntSandboxConfig
from alife_biosphere.ant_sandbox.observer import build_ant_observer_payload, write_ant_observer_html


def test_ant_sandbox_observer_payload_contains_world_frames() -> None:
    payload = build_ant_observer_payload(AntSandboxConfig(ticks=40), title="Ant Observer")
    assert payload["width"] == 64
    assert payload["height"] == 48
    assert payload["total_ticks"] == 40
    assert payload["frames"]
    first = payload["frames"][0]
    assert "ants" in first
    assert "food_patches" in first
    assert "food_trail" in first
    assert "home_trail" in first


def test_ant_sandbox_observer_html_writes_canvas_window(tmp_path: Path) -> None:
    payload = build_ant_observer_payload(AntSandboxConfig(ticks=20), title="Ant Observer")
    output = tmp_path / "observer.html"
    write_ant_observer_html(output, payload)
    html = output.read_text(encoding="utf-8")
    assert "<canvas id=\"world\"" in html
    assert "observer-data" in html
    assert "Ant Observer" in html
