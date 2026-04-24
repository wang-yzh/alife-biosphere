"""Ant sandbox substrate branch."""

from .config import AntAgentConfig, AntSandboxConfig, ColonyConfig, FoodPatchConfig, NestConfig, TerrainConfig
from .checkpoint import AntSandboxCheckpoint, load_checkpoint, write_checkpoint
from .comparison import build_branch_comparison_payload, render_branch_comparison_markdown, write_branch_comparison
from .open_endedness import (
    build_open_endedness_payload,
    build_open_endedness_payload_from_checkpoints,
    render_open_endedness_markdown,
    write_open_endedness_report,
)
from .observer import (
    build_ant_checkpoint_observer_payload,
    build_ant_observer_payload,
    write_ant_live_observer_html,
    write_ant_observer_html,
)
from .reporting import summarize_behavior_roles, summarize_food_source_competition, summarize_inheritance_dynamics
from .showcase import build_showcase_config
from .simulation import AntSandboxResult, run_simulation, run_world_until, step_world
from .validation import DEFAULT_VALIDATION_SEEDS, run_validation_cases, summarize_validation_status
from .world import AntSandboxWorld, Corpse, FoodPatch, InstinctGenome, Nest, SandboxAnt, initialize_world

__all__ = [
    "AntAgentConfig",
    "AntSandboxConfig",
    "AntSandboxCheckpoint",
    "AntSandboxResult",
    "ColonyConfig",
    "Corpse",
    "FoodPatch",
    "FoodPatchConfig",
    "InstinctGenome",
    "Nest",
    "NestConfig",
    "TerrainConfig",
    "SandboxAnt",
    "AntSandboxWorld",
    "DEFAULT_VALIDATION_SEEDS",
    "build_ant_checkpoint_observer_payload",
    "build_branch_comparison_payload",
    "build_ant_observer_payload",
    "build_open_endedness_payload",
    "build_open_endedness_payload_from_checkpoints",
    "build_showcase_config",
    "initialize_world",
    "load_checkpoint",
    "render_branch_comparison_markdown",
    "render_open_endedness_markdown",
    "run_simulation",
    "run_world_until",
    "run_validation_cases",
    "summarize_behavior_roles",
    "summarize_food_source_competition",
    "summarize_inheritance_dynamics",
    "summarize_validation_status",
    "step_world",
    "write_branch_comparison",
    "write_checkpoint",
    "write_open_endedness_report",
    "write_ant_live_observer_html",
    "write_ant_observer_html",
]
