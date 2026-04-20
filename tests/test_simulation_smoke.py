from alife_biosphere.config import SimulationConfig
from alife_biosphere.simulation import run_simulation


def test_smoke_run_is_deterministic() -> None:
    first = run_simulation(SimulationConfig())
    second = run_simulation(SimulationConfig())
    assert first.summary() == second.summary()
    assert [event.to_dict() for event in first.events] == [
        event.to_dict() for event in second.events
    ]


def test_smoke_run_emits_events() -> None:
    result = run_simulation(SimulationConfig())
    assert result.events
    assert result.summary()["ticks"] == 20
    event_types = {event.event_type for event in result.events}
    assert "move" in event_types
    assert "crowding_damage" in event_types
    assert "reproduction_ready" in event_types
    assert "tick_summary" in event_types


def test_tick_summary_contains_ecology_probe_fields() -> None:
    result = run_simulation(SimulationConfig())
    summary_events = [event for event in result.events if event.event_type == "tick_summary"]
    assert summary_events
    final_payload = summary_events[-1].payload
    assert "occupancy_by_habitat" in final_payload
    assert "occupancy_pressure_by_habitat" in final_payload
    assert "movement_count" in final_payload
    assert "birth_count" in final_payload
    assert "reproduction_ready_count" in final_payload
    assert "lineage_count" in final_payload
    assert len(final_payload["occupancy_by_habitat"]) == 7


def test_reproduction_produces_births_and_lineage_links() -> None:
    result = run_simulation(SimulationConfig())
    birth_events = [event for event in result.events if event.event_type == "birth"]
    assert birth_events
    born_ids = {event.organism_id for event in birth_events}
    for organism_id in born_ids:
        organism = result.world.organisms[organism_id]
        assert organism.parent_id is not None
        assert organism.generation >= 1
        assert organism.lineage_id == result.world.organisms[organism.parent_id].lineage_id


def test_disturbance_hook_emits_events_when_enabled() -> None:
    result = run_simulation(
        SimulationConfig(
            world=SimulationConfig().world.__class__(
                ticks=12,
                disturbance_interval=4,
                disturbance_resource_shock=3.0,
                disturbance_hazard_pulse=0.2,
            )
        )
    )
    disturbance_events = [event for event in result.events if event.event_type == "disturbance"]
    assert disturbance_events
