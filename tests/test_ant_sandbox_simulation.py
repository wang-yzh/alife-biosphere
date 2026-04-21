from alife_biosphere.ant_sandbox import AntSandboxConfig
from alife_biosphere.ant_sandbox.simulation import run_simulation


def test_ant_sandbox_run_is_deterministic() -> None:
    first = run_simulation(AntSandboxConfig())
    second = run_simulation(AntSandboxConfig())
    assert first.summary() == second.summary()
    assert [event.to_dict() for event in first.events] == [event.to_dict() for event in second.events]


def test_ant_sandbox_produces_foraging_loop_events() -> None:
    result = run_simulation(AntSandboxConfig())
    event_types = {event.event_type for event in result.events}
    assert "food_pickup" in event_types
    assert "food_unload" in event_types
    assert result.world.nest.stored_food > 0


def test_ant_sandbox_keeps_ants_in_bounds() -> None:
    result = run_simulation(AntSandboxConfig())
    assert all(0 <= ant.x < result.world.width and 0 <= ant.y < result.world.height for ant in result.world.ants)
