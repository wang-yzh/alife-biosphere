from dataclasses import replace
from pathlib import Path

from alife_biosphere.ant_sandbox import AntSandboxConfig, initialize_world
from alife_biosphere.ant_sandbox.checkpoint import load_checkpoint, write_checkpoint
from alife_biosphere.ant_sandbox.comparison import (
    build_branch_comparison_payload,
    render_branch_comparison_markdown,
    write_branch_comparison,
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


def _make_family(tmp_path: Path, prefix: str) -> list[Path]:
    root = _make_root_checkpoint(tmp_path, f"{prefix}_root", seed=7, tick=8)
    child_a = _make_child_checkpoint(tmp_path, f"{prefix}_seed11", root, seed=11, target_tick=12)
    child_b = _make_child_checkpoint(tmp_path, f"{prefix}_seed99", root, seed=99, target_tick=12)
    return [root, child_a, child_b]


def test_branch_comparison_groups_root_and_forks_into_one_family(tmp_path: Path) -> None:
    checkpoints = _make_family(tmp_path, "family")
    payload = build_branch_comparison_payload(checkpoints)
    assert payload["checkpoint_count"] == 3
    assert payload["family_count"] == 1
    family = payload["families"][0]
    assert family["branch_count"] == 3
    assert {branch["provenance"]["branch_id"] for branch in family["branches"]} == {
        "family_root",
        "family_seed11",
        "family_seed99",
    }
    assert len(family["pairwise_deltas"]) == 3
    assert family["pairwise_deltas"][0]["branch_a"]
    assert "alive_delta" in family["pairwise_deltas"][0]


def test_branch_comparison_preserves_provenance_and_metrics(tmp_path: Path) -> None:
    checkpoints = _make_family(tmp_path, "provenance")
    payload = build_branch_comparison_payload(checkpoints)
    branch = payload["families"][0]["branches"][0]
    provenance = branch["provenance"]
    outcomes = branch["outcomes"]
    spatial = branch["spatial"]
    assert provenance["branch_id"] == "provenance_root"
    assert provenance["final_tick"] == 8
    assert provenance["seed"] == 7
    assert "alive_by_colony" in outcomes
    assert "unloads_by_colony" in outcomes
    assert "max_generation" in outcomes
    assert "occupied_cell_count" in spatial
    assert "trail_cell_count_by_colony" in spatial
    assert "corpse_count" in outcomes
    assert "residue_cell_count" in spatial
    assert "top_food_source" in spatial


def test_branch_comparison_writes_json_and_markdown(tmp_path: Path) -> None:
    checkpoints = _make_family(tmp_path, "write")
    payload = build_branch_comparison_payload(checkpoints)
    output_dir = tmp_path / "comparison"
    json_path, markdown_path = write_branch_comparison(output_dir, payload)
    markdown = markdown_path.read_text(encoding="utf-8")
    assert json_path.exists()
    assert markdown_path.exists()
    assert payload["comparison_id"] in markdown
    assert "These metrics show branch differences. They do not prove open-ended evolution." in markdown


def test_branch_comparison_groups_unrelated_families_separately(tmp_path: Path) -> None:
    family_a = _make_family(tmp_path, "group_a")
    family_b_root = _make_root_checkpoint(tmp_path, "group_b_root", seed=17, tick=9)
    payload = build_branch_comparison_payload([*family_a, family_b_root])
    assert payload["family_count"] == 2
    family_sizes = sorted(family["branch_count"] for family in payload["families"])
    assert family_sizes == [1, 3]


def test_branch_comparison_markdown_mentions_pairwise_divergence(tmp_path: Path) -> None:
    checkpoints = _make_family(tmp_path, "markdown")
    payload = build_branch_comparison_payload(checkpoints)
    markdown = render_branch_comparison_markdown(payload)
    assert "Pairwise Divergence Notes" in markdown
    assert "markdown_seed11" in markdown
    assert "markdown_seed99" in markdown
