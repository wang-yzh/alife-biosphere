from dataclasses import replace

from alife_biosphere.ant_sandbox import AntAgentConfig, AntSandboxConfig
from alife_biosphere.ant_sandbox.checkpoint import load_checkpoint, write_checkpoint
from alife_biosphere.ant_sandbox.observer import build_ant_observer_payload
from alife_biosphere.ant_sandbox.simulation import run_simulation


def _substrate_config(ticks: int, corpse_decay_ticks: int = 5) -> AntSandboxConfig:
    ants = replace(
        AntAgentConfig(),
        max_age=1,
        allow_spawning=False,
        pheromone_enabled=False,
        metabolism_cost=0.0001,
        corpse_decay_ticks=corpse_decay_ticks,
        residue_decay=0.0,
        trail_residue_deposit=0.0,
        nest_residue_deposit=0.0,
        corpse_residue_release=0.12,
    )
    return AntSandboxConfig(ticks=ticks, ants=ants)


def test_corpse_appears_when_ants_die() -> None:
    result = run_simulation(_substrate_config(ticks=2, corpse_decay_ticks=5))
    assert result.world.corpse_count() == 32
    assert sum(1 for event in result.events if event.event_type == "corpse_create") == 32


def test_corpse_decay_is_deterministic() -> None:
    config = _substrate_config(ticks=5, corpse_decay_ticks=2)
    first = run_simulation(config)
    second = run_simulation(config)
    assert first.summary() == second.summary()
    assert [event.to_dict() for event in first.events] == [event.to_dict() for event in second.events]
    assert first.world.corpse_count() == 0
    assert first.world.residue_cell_count() > 0


def test_substrate_survives_checkpoint_round_trip(tmp_path) -> None:
    config = _substrate_config(ticks=3, corpse_decay_ticks=5)
    result = run_simulation(config)
    checkpoint_path = tmp_path / "substrate_checkpoint.json"
    write_checkpoint(checkpoint_path, config, result.world, {"run_id": "substrate", "branch_id": "substrate-root"})
    loaded = load_checkpoint(checkpoint_path)
    assert loaded.world.corpse_count() == result.world.corpse_count()
    assert loaded.world.residue_cell_count() == result.world.residue_cell_count()
    assert loaded.world.residue_field == result.world.residue_field


def test_observer_payload_includes_substrate_layers() -> None:
    payload = build_ant_observer_payload(_substrate_config(ticks=3, corpse_decay_ticks=5), title="Substrate Observer")
    frame = payload["frames"][-1]
    assert "corpses" in frame
    assert "residue_points" in frame
    assert frame["corpses"]
    assert frame["residue_points"]


def test_summary_reports_substrate_counts() -> None:
    result = run_simulation(_substrate_config(ticks=3, corpse_decay_ticks=5))
    summary = result.summary()
    assert "corpse_count" in summary
    assert "residue_cell_count" in summary
    assert "residue_total_value" in summary
    assert summary["corpse_count"] > 0
