from alife_biosphere.ant_sandbox import AntAgentConfig, AntSandboxConfig
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


def test_ant_sandbox_with_pheromones_beats_no_pheromones() -> None:
    with_pheromones = run_simulation(AntSandboxConfig(ants=AntAgentConfig(pheromone_enabled=True)))
    without_pheromones = run_simulation(AntSandboxConfig(ants=AntAgentConfig(pheromone_enabled=False)))
    assert with_pheromones.world.nest.stored_food >= without_pheromones.world.nest.stored_food
    assert sum(1 for event in with_pheromones.events if event.event_type == "trail_deposit") > 0
    assert sum(1 for event in without_pheromones.events if event.event_type == "trail_deposit") == 0


def test_ant_sandbox_can_show_births_and_deaths_in_longer_run() -> None:
    result = run_simulation(
        AntSandboxConfig(
            ticks=420,
            ants=AntAgentConfig(
                max_age=200,
                max_population=44,
                spawn_food_cost=3,
                spawn_interval=6,
                pheromone_enabled=True,
            ),
        )
    )
    event_types = {event.event_type for event in result.events}
    assert "ant_birth" in event_types
    assert "ant_death" in event_types
    summaries = [event.payload for event in result.events if event.event_type == "tick_summary"]
    alive_counts = [summary["alive"] for summary in summaries]
    assert min(alive_counts) > 0
    assert max(alive_counts) <= 44
