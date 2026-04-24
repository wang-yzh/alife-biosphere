from dataclasses import replace
from pathlib import Path

from alife_biosphere.ant_sandbox import AntAgentConfig, AntSandboxConfig, initialize_world
from alife_biosphere.ant_sandbox.checkpoint import load_checkpoint, write_checkpoint
from alife_biosphere.ant_sandbox.comparison import build_branch_comparison_payload
from alife_biosphere.ant_sandbox.observer import build_ant_observer_payload
from alife_biosphere.ant_sandbox.open_endedness import build_open_endedness_payload
from alife_biosphere.ant_sandbox.simulation import run_simulation, run_world_until


def _successor_config(ticks: int) -> AntSandboxConfig:
    ants = replace(
        AntAgentConfig(),
        max_age=1,
        allow_spawning=False,
        pheromone_enabled=False,
        metabolism_cost=0.0001,
        corpse_decay_ticks=10,
        residue_decay=0.0,
        trail_residue_deposit=0.0,
        nest_residue_deposit=0.0,
        corpse_residue_release=0.04,
        decomposer_emerge_delay_ticks=1,
        decomposer_feed_rate=0.18,
        decomposer_decay=0.03,
        decomposer_spread_interval=2,
        decomposer_residue_threshold=0.04,
        decomposer_enrich_residue=0.08,
    )
    return AntSandboxConfig(ticks=ticks, ants=ants)


def test_decomposer_emerges_only_when_substrate_exists() -> None:
    result = run_simulation(_successor_config(ticks=4))
    assert result.world.decomposer_patch_count() > 0
    assert sum(1 for event in result.events if event.event_type == "decomposer_emerge") > 0
    assert result.world.corpse_count() > 0


def test_decomposer_state_survives_checkpoint_round_trip(tmp_path: Path) -> None:
    config = _successor_config(ticks=4)
    result = run_simulation(config)
    checkpoint_path = tmp_path / "successor_checkpoint.json"
    write_checkpoint(checkpoint_path, config, result.world, {"run_id": "successor", "branch_id": "successor-root"})
    loaded = load_checkpoint(checkpoint_path)
    assert loaded.world.decomposer_patch_count() == result.world.decomposer_patch_count()
    assert [patch.to_dict() for patch in loaded.world.decomposer_patches] == [
        patch.to_dict() for patch in result.world.decomposer_patches
    ]


def test_decomposer_decays_without_substrate() -> None:
    ants = replace(
        _successor_config(ticks=4).ants,
        residue_enabled=False,
        decomposer_decay=0.18,
        corpse_decay_ticks=1,
        decomposer_spread_interval=99,
    )
    result = run_simulation(AntSandboxConfig(ticks=8, ants=ants))
    assert result.world.decomposer_patch_count() == 0
    assert sum(1 for event in result.events if event.event_type == "decomposer_decay") > 0


def test_observer_payload_includes_decomposer_layer() -> None:
    payload = build_ant_observer_payload(_successor_config(ticks=4), title="Successor Observer")
    frame = payload["frames"][-1]
    assert "decomposer_patches" in frame
    assert frame["decomposer_patches"]
    assert frame["decomposer_patch_count"] > 0
    assert frame["enriched_residue_cell_count"] >= 0


def test_dependency_metrics_count_corpse_to_decomposer_links(tmp_path: Path) -> None:
    config = _successor_config(ticks=4)
    world = initialize_world(config)
    run_world_until(world, config, 4)
    root_path = tmp_path / "successor_root.json"
    write_checkpoint(root_path, config, world, {"run_id": "successor-run", "branch_id": "successor-root"})

    loaded = load_checkpoint(root_path)
    fork_config = replace(loaded.config, ticks=6)
    run_world_until(loaded.world, fork_config, 6)
    fork_path = tmp_path / "successor_child.json"
    write_checkpoint(
        fork_path,
        fork_config,
        loaded.world,
        {
            "run_id": "successor-run",
            "branch_id": "successor-child",
            "parent_run_id": "successor-run",
            "parent_branch_id": "successor-root",
            "parent_checkpoint": str(root_path.resolve()),
            "forked_from_tick": 4,
        },
    )

    payload = build_open_endedness_payload(build_branch_comparison_payload([root_path, fork_path]))
    dependency_family = payload["metric_families"]["ecological_dependency"]["metrics"]
    dependency_metrics = dependency_family[next(iter(dependency_family))]
    assert dependency_metrics["corpse_to_decomposer_edges"]["status"] == "available"
    values = dependency_metrics["corpse_to_decomposer_edges"]["values"]
    assert values["successor-root"] > 0 or values["successor-child"] > 0
