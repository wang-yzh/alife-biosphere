from pathlib import Path

from alife_biosphere.config import SimulationConfig
from alife_biosphere.observer import build_observer_payload, render_observer_html
from alife_biosphere.simulation import run_simulation


def test_observer_payload_contains_graph_and_frames() -> None:
    config = SimulationConfig()
    result = run_simulation(config)
    payload = build_observer_payload(config, result, title="Observer")
    assert payload["ticks"] == config.world.ticks
    assert len(payload["habitats"]) == 7
    assert len(payload["edges"]) == len(config.world.habitat_edges)
    assert len(payload["frames"]) == config.world.ticks
    assert "lineages_by_habitat" not in payload["frames"][0]
    assert "habitats" in payload["frames"][0]
    assert "organisms" in payload["frames"][0]
    assert payload["frames"][0]["organisms"]
    assert payload["frames"][0]["tick"] == 1


def test_observer_html_embeds_payload() -> None:
    config = SimulationConfig()
    result = run_simulation(config)
    payload = build_observer_payload(config, result, title="Observer")
    html = render_observer_html(payload)
    assert "<svg id=\"map\"" in html
    assert "observer-data" in html
    assert "nursery_a" in html
    assert "organism" in html
    assert "birth-ring" in html
    assert "Alife Biosphere Observer" not in html
    assert "Observer" in html
