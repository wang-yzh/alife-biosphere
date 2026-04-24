import json
from pathlib import Path

from alife_biosphere.ant_sandbox import AntSandboxConfig, initialize_world
from alife_biosphere.ant_sandbox.checkpoint import load_checkpoint, write_checkpoint
from alife_biosphere.ant_sandbox.observer import build_ant_checkpoint_observer_payload, write_ant_observer_html
from alife_biosphere.ant_sandbox.simulation import run_world_until


def _write_checkpoint_fixture(tmp_path: Path, tick: int = 8) -> Path:
    config = AntSandboxConfig(ticks=max(20, tick))
    world = initialize_world(config)
    run_world_until(world, config, tick)
    checkpoint_path = tmp_path / "checkpoint.json"
    write_checkpoint(
        checkpoint_path,
        config,
        world,
        {"run_id": "fixture-run", "branch_id": "fixture-root", "parent_branch_id": "origin", "forked_from_tick": 3},
    )
    return checkpoint_path


def test_checkpoint_observer_payload_contains_provenance(tmp_path: Path) -> None:
    checkpoint_path = _write_checkpoint_fixture(tmp_path, tick=8)
    payload = build_ant_checkpoint_observer_payload(checkpoint_path, title="Checkpoint Observer")
    assert payload["source_checkpoint"] == str(checkpoint_path.resolve())
    assert payload["checkpoint_metadata"]["branch_id"] == "fixture-root"
    assert payload["loaded_tick"] == 8
    assert payload["target_tick"] == 8
    assert payload["replayed_from_checkpoint"] is False
    assert len(payload["frames"]) == 1
    assert payload["frames"][0]["tick"] == 8
    assert payload["config_inheritance_mode"] == "clone"


def test_checkpoint_observer_continuation_reaches_target_tick(tmp_path: Path) -> None:
    checkpoint_path = _write_checkpoint_fixture(tmp_path, tick=8)
    payload = build_ant_checkpoint_observer_payload(
        checkpoint_path,
        title="Checkpoint Observer",
        target_tick=12,
    )
    assert payload["replayed_from_checkpoint"] is True
    assert payload["loaded_tick"] == 8
    assert payload["target_tick"] == 12
    assert payload["frames"][0]["tick"] == 8
    assert payload["frames"][-1]["tick"] == 12
    assert payload["total_ticks"] == 12


def test_checkpoint_observer_does_not_mutate_source_checkpoint(tmp_path: Path) -> None:
    checkpoint_path = _write_checkpoint_fixture(tmp_path, tick=8)
    before = checkpoint_path.read_text(encoding="utf-8")
    payload = build_ant_checkpoint_observer_payload(checkpoint_path, target_tick=10)
    output_path = tmp_path / "observer.html"
    write_ant_observer_html(output_path, payload)
    after = checkpoint_path.read_text(encoding="utf-8")
    reloaded = load_checkpoint(checkpoint_path)
    assert "fixture-root" in output_path.read_text(encoding="utf-8")
    assert json.loads(before) == json.loads(after)
    assert reloaded.world.tick == 8
