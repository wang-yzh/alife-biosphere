from dataclasses import replace

from alife_biosphere.ant_sandbox import AntSandboxConfig
from alife_biosphere.ant_sandbox.checkpoint import load_checkpoint, write_checkpoint
from alife_biosphere.ant_sandbox.simulation import run_simulation, run_world_until
from alife_biosphere.ant_sandbox.world import initialize_world


def test_ant_sandbox_config_from_dict_round_trips() -> None:
    config = AntSandboxConfig(ticks=42)
    loaded = AntSandboxConfig.from_dict(config.to_dict())
    assert loaded == config


def test_ant_sandbox_world_from_dict_round_trips_after_running() -> None:
    config = AntSandboxConfig(ticks=25)
    result = run_simulation(config)
    loaded_world = result.world.__class__.from_dict(result.world.to_dict())
    assert loaded_world.summary() == result.world.summary()
    assert [event.to_dict() for event in loaded_world.events] == [event.to_dict() for event in result.world.events]
    assert [ant.to_dict() for ant in loaded_world.ants] == [ant.to_dict() for ant in result.world.ants]
    assert loaded_world.food_trail == result.world.food_trail
    assert loaded_world.home_trail == result.world.home_trail


def test_checkpoint_resume_matches_uninterrupted_run(tmp_path) -> None:
    full_config = AntSandboxConfig(ticks=60)
    full = run_simulation(full_config)

    partial_config = replace(full_config, ticks=30)
    partial = run_simulation(partial_config)
    checkpoint_path = tmp_path / "tick_000030.json"
    write_checkpoint(checkpoint_path, partial_config, partial.world, {"run_id": "resume-test", "branch_id": "main"})

    loaded = load_checkpoint(checkpoint_path)
    resumed_config = replace(loaded.config, ticks=60)
    resumed = run_world_until(loaded.world, resumed_config, 60)

    assert resumed.summary() == full.summary()
    assert [event.to_dict() for event in resumed.events] == [event.to_dict() for event in full.events]
    assert resumed.world.to_dict() == full.world.to_dict()


def test_checkpoint_fork_metadata_and_future_seed_override(tmp_path) -> None:
    config = AntSandboxConfig(ticks=20)
    world = initialize_world(config)
    run_world_until(world, config, 10)
    source_path = tmp_path / "source.json"
    write_checkpoint(source_path, config, world, {"run_id": "source", "branch_id": "root"})

    loaded = load_checkpoint(source_path)
    fork_config = replace(loaded.config, seed=99, ticks=25)
    fork_result = run_world_until(loaded.world, fork_config, 25)
    fork_path = tmp_path / "fork.json"
    write_checkpoint(
        fork_path,
        fork_config,
        fork_result.world,
        {"run_id": "source", "branch_id": "seed-99", "parent_run_id": "source", "forked_from_tick": 10},
    )

    forked = load_checkpoint(fork_path)
    assert forked.metadata["branch_id"] == "seed-99"
    assert forked.metadata["parent_run_id"] == "source"
    assert forked.metadata["forked_from_tick"] == 10
    assert forked.world.tick == 25
