from __future__ import annotations

import json
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from .checkpoint import load_checkpoint, write_checkpoint
from .comparison import build_branch_comparison_payload, write_branch_comparison
from .observer import build_ant_checkpoint_observer_payload, write_ant_observer_html
from .open_endedness import build_open_endedness_payload, write_open_endedness_report
from .showcase import build_showcase_config
from .simulation import run_world_until
from .world import initialize_world


def _campaign_id() -> str:
    return datetime.now().strftime("campaign_%Y%m%d_%H%M%S")


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _render_campaign_markdown(manifest: dict[str, object]) -> str:
    lines = [
        f"# Multi-Niche Open Evolution {manifest['campaign_id']}",
        "",
        f"Generated: {manifest['generated_at']}",
        "",
        f"Root branch: `{manifest['root_branch']['branch_id']}`  ",
        f"Fork branches: `{len(manifest['fork_branches'])}`",
        "",
        "## Branches",
        "",
        "| Branch | Seed | Start | Final | Alive | Decomp | Residue | Observer |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    all_branches = [manifest["root_branch"], *manifest["fork_branches"]]
    for branch in all_branches:
        summary = branch["summary"]
        lines.append(
            "| "
            f"{branch['branch_id']} | "
            f"{branch['seed']} | "
            f"{branch['start_tick']} | "
            f"{branch['final_tick']} | "
            f"{summary['alive']} | "
            f"{summary['decomposer_patch_count']} | "
            f"{summary['residue_cell_count']} | "
            f"`{branch['observer_html']}` |"
        )
    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            f"- comparison: `{manifest['comparison_json']}`",
            f"- open-endedness: `{manifest['open_endedness_json']}`",
            f"- comparison markdown: `{manifest['comparison_markdown']}`",
            f"- open-endedness markdown: `{manifest['open_endedness_markdown']}`",
            "",
            "## Caution",
            "",
            "This campaign reports branch divergence and early ecological dependency. It does not claim a finished open-ended ecosystem.",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def _export_branch(
    output_dir: Path,
    branch_id: str,
    run_id: str,
    *,
    config,
    world,
    parent_branch_id: str | None = None,
    parent_run_id: str | None = None,
    parent_checkpoint: Path | None = None,
    forked_from_tick: int | None = None,
    observer_title: str = "Ant Sandbox Branch",
) -> dict[str, object]:
    branch_dir = output_dir / "branches" / branch_id
    metadata = {
        "run_id": run_id,
        "branch_id": branch_id,
        "parent_run_id": parent_run_id,
        "parent_branch_id": parent_branch_id,
        "parent_checkpoint": None if parent_checkpoint is None else str(parent_checkpoint.resolve()),
        "forked_from_tick": forked_from_tick,
        "note": "multi_niche_open_evolution_campaign",
    }
    checkpoint_path = write_checkpoint(branch_dir / "checkpoint_final.json", config, world, metadata)
    summary = world.summary()
    status = {
        "run_id": run_id,
        "branch_id": branch_id,
        "start_tick": 0 if forked_from_tick is None else forked_from_tick,
        "final_tick": world.tick,
        "summary": summary,
        "checkpoint_final": str(checkpoint_path),
    }
    _write_json(branch_dir / "status.json", status)
    _write_json(branch_dir / "config.json", config.to_dict())
    _write_json(branch_dir / "world.json", world.to_dict())
    (branch_dir / "events.json").write_text(
        json.dumps([event.to_dict() for event in world.events], indent=2),
        encoding="utf-8",
    )

    observer_dir = output_dir / "observers" / branch_id
    observer_dir.mkdir(parents=True, exist_ok=True)
    observer_payload = build_ant_checkpoint_observer_payload(checkpoint_path, title=observer_title)
    write_ant_observer_html(observer_dir / "observer.html", observer_payload)
    _write_json(observer_dir / "observer_data.json", observer_payload)

    return {
        "branch_id": branch_id,
        "seed": config.seed,
        "start_tick": status["start_tick"],
        "final_tick": world.tick,
        "summary": summary,
        "checkpoint_final": str(checkpoint_path),
        "observer_html": str(observer_dir / "observer.html"),
        "observer_data": str(observer_dir / "observer_data.json"),
    }


def run_multi_niche_open_evolution_campaign(
    output_dir: str | Path,
    *,
    campaign_id: str | None = None,
    root_seed: int = 7,
    root_tick: int = 900,
    fork_additional_ticks: int = 900,
    fork_seeds: tuple[int, ...] = (11, 29, 47),
    inheritance_mode: str | None = None,
    mutation_rate: float | None = None,
    mutation_step: float | None = None,
) -> dict[str, object]:
    root_output = Path(output_dir)
    root_output.mkdir(parents=True, exist_ok=True)
    resolved_campaign_id = campaign_id or _campaign_id()
    run_id = resolved_campaign_id

    base_config = build_showcase_config(seed=root_seed, ticks=root_tick)
    ants_config = base_config.ants
    if inheritance_mode is not None:
        ants_config = replace(ants_config, inheritance_mode=inheritance_mode)
    if mutation_rate is not None:
        ants_config = replace(ants_config, mutation_rate=mutation_rate)
    if mutation_step is not None:
        ants_config = replace(ants_config, mutation_step=mutation_step)
    root_config = replace(base_config, ants=ants_config)

    root_world = initialize_world(root_config)
    run_world_until(root_world, root_config, root_tick)
    root_branch_id = f"{resolved_campaign_id}_root"
    root_branch = _export_branch(
        root_output,
        root_branch_id,
        run_id,
        config=root_config,
        world=root_world,
        observer_title="Ant Sandbox Branch - Root",
    )

    fork_branches: list[dict[str, object]] = []
    root_checkpoint = Path(root_branch["checkpoint_final"])
    for seed in fork_seeds:
        loaded = load_checkpoint(root_checkpoint)
        fork_config = replace(loaded.config, seed=seed, ticks=loaded.world.tick + fork_additional_ticks)
        run_world_until(loaded.world, fork_config, fork_config.ticks)
        branch_id = f"{resolved_campaign_id}_seed_{seed}"
        fork_branch = _export_branch(
            root_output,
            branch_id,
            run_id,
            config=fork_config,
            world=loaded.world,
            parent_branch_id=root_branch_id,
            parent_run_id=run_id,
            parent_checkpoint=root_checkpoint,
            forked_from_tick=loaded.metadata["tick"],
            observer_title=f"Ant Sandbox Branch - Seed {seed}",
        )
        fork_branches.append(fork_branch)

    checkpoints = [Path(root_branch["checkpoint_final"]), *(Path(branch["checkpoint_final"]) for branch in fork_branches)]
    comparison_payload = build_branch_comparison_payload(checkpoints)
    comparison_dir = root_output / "comparison"
    comparison_json, comparison_markdown = write_branch_comparison(comparison_dir, comparison_payload)

    open_payload = build_open_endedness_payload(comparison_payload)
    open_dir = root_output / "open_endedness"
    open_json, open_markdown = write_open_endedness_report(open_dir, open_payload)

    manifest = {
        "campaign_id": resolved_campaign_id,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "root_branch": root_branch,
        "fork_branches": fork_branches,
        "comparison_json": str(comparison_json),
        "comparison_markdown": str(comparison_markdown),
        "open_endedness_json": str(open_json),
        "open_endedness_markdown": str(open_markdown),
    }
    _write_json(root_output / "campaign_manifest.json", manifest)
    (root_output / "campaign_summary.md").write_text(_render_campaign_markdown(manifest), encoding="utf-8")
    return manifest
