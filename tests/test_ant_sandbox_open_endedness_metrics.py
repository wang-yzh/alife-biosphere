from dataclasses import replace
import json
from pathlib import Path

from alife_biosphere.ant_sandbox import AntSandboxConfig, initialize_world
from alife_biosphere.ant_sandbox.checkpoint import load_checkpoint, write_checkpoint
from alife_biosphere.ant_sandbox.comparison import build_branch_comparison_payload
from alife_biosphere.ant_sandbox.open_endedness import (
    STATUS_VALUES,
    build_open_endedness_payload,
    render_open_endedness_markdown,
    write_open_endedness_report,
)
from alife_biosphere.ant_sandbox.simulation import run_world_until


def _make_root_checkpoint(tmp_path: Path, branch_id: str, seed: int = 7, tick: int = 8) -> Path:
    config = AntSandboxConfig(seed=seed, ticks=max(tick, 20))
    world = initialize_world(config)
    run_world_until(world, config, tick)
    checkpoint_path = tmp_path / f"{branch_id}.json"
    write_checkpoint(checkpoint_path, config, world, {"run_id": f"{branch_id}-run", "branch_id": branch_id})
    return checkpoint_path


def _make_child_checkpoint(tmp_path: Path, branch_id: str, parent_checkpoint: Path, seed: int, target_tick: int = 12) -> Path:
    loaded = load_checkpoint(parent_checkpoint)
    fork_tick = loaded.world.tick
    config = replace(loaded.config, seed=seed, ticks=target_tick)
    run_world_until(loaded.world, config, target_tick)
    checkpoint_path = tmp_path / f"{branch_id}.json"
    write_checkpoint(
        checkpoint_path,
        config,
        loaded.world,
        {
            "run_id": str(loaded.metadata["run_id"]),
            "branch_id": branch_id,
            "parent_run_id": loaded.metadata["run_id"],
            "parent_branch_id": loaded.metadata["branch_id"],
            "parent_checkpoint": str(parent_checkpoint.resolve()),
            "forked_from_tick": fork_tick,
        },
    )
    return checkpoint_path


def _comparison_payload(tmp_path: Path) -> dict[str, object]:
    root = _make_root_checkpoint(tmp_path, "metrics_root", seed=7, tick=8)
    child_a = _make_child_checkpoint(tmp_path, "metrics_seed11", root, seed=11, target_tick=12)
    child_b = _make_child_checkpoint(tmp_path, "metrics_seed99", root, seed=99, target_tick=12)
    return build_branch_comparison_payload([root, child_a, child_b])


def test_open_endedness_metrics_load_from_branch_comparison(tmp_path: Path) -> None:
    comparison_payload = _comparison_payload(tmp_path)
    payload = build_open_endedness_payload(comparison_payload)
    assert payload["comparison_id"] == comparison_payload["comparison_id"]
    assert "metric_families" in payload
    assert "branch_divergence" in payload["metric_families"]
    assert "niche_occupancy" in payload["metric_families"]
    assert "stepping_stone_persistence" in payload["metric_families"]
    assert "ecological_dependency" in payload["metric_families"]
    assert "novelty_without_collapse" in payload["metric_families"]


def test_open_endedness_metric_status_labels_are_present(tmp_path: Path) -> None:
    payload = build_open_endedness_payload(_comparison_payload(tmp_path))
    for family_payload in payload["metric_families"].values():
        for metrics in family_payload["metrics"].values():
            for metric in metrics.values():
                assert metric["status"] in STATUS_VALUES


def test_ecological_dependency_metrics_remain_requires_m16(tmp_path: Path) -> None:
    payload = build_open_endedness_payload(_comparison_payload(tmp_path))
    dependency_family = payload["metric_families"]["ecological_dependency"]["metrics"]
    for metrics in dependency_family.values():
        for metric in metrics.values():
            assert metric["status"] == "requires_m16"


def test_open_endedness_output_does_not_emit_single_scalar_score(tmp_path: Path) -> None:
    payload = build_open_endedness_payload(_comparison_payload(tmp_path))
    output_dir = tmp_path / "open_endedness"
    json_path, markdown_path = write_open_endedness_report(output_dir, payload)
    written = json.loads(json_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    serialized = json.dumps(written)
    assert "open_endedness_score" not in serialized
    assert "\"score\"" not in serialized
    assert "universal fitness" in markdown or "fitness score" in markdown


def test_open_endedness_markdown_mentions_metric_families(tmp_path: Path) -> None:
    payload = build_open_endedness_payload(_comparison_payload(tmp_path))
    markdown = render_open_endedness_markdown(payload)
    assert "Branch Divergence" in markdown
    assert "Niche Occupancy" in markdown
    assert "Stepping Stone Persistence" in markdown
    assert "Ecological Dependency" in markdown
    assert "Novelty Without Collapse" in markdown
