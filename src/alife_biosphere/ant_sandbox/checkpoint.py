from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .config import AntSandboxConfig
from .world import AntSandboxWorld


CHECKPOINT_KIND = "ant_sandbox_checkpoint"
CHECKPOINT_VERSION = 1


@dataclass(frozen=True)
class AntSandboxCheckpoint:
    config: AntSandboxConfig
    world: AntSandboxWorld
    metadata: dict[str, object]


def build_checkpoint_payload(
    config: AntSandboxConfig,
    world: AntSandboxWorld,
    metadata: dict[str, object] | None = None,
) -> dict[str, object]:
    merged_metadata = dict(metadata or {})
    merged_metadata.update(
        {
            "checkpoint_kind": CHECKPOINT_KIND,
            "checkpoint_version": CHECKPOINT_VERSION,
            "saved_at": datetime.now(timezone.utc).isoformat(),
            "tick": world.tick,
        }
    )
    return {
        "metadata": merged_metadata,
        "config": config.to_dict(),
        "world": world.to_dict(),
    }


def write_checkpoint(
    path: str | Path,
    config: AntSandboxConfig,
    world: AntSandboxWorld,
    metadata: dict[str, object] | None = None,
) -> Path:
    checkpoint_path = Path(path)
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_checkpoint_payload(config, world, metadata)
    temp_path = checkpoint_path.with_suffix(checkpoint_path.suffix + ".tmp")
    temp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    temp_path.replace(checkpoint_path)
    return checkpoint_path


def load_checkpoint(path: str | Path) -> AntSandboxCheckpoint:
    checkpoint_path = Path(path)
    payload = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    metadata = dict(payload.get("metadata", {}))
    if metadata.get("checkpoint_kind") not in {None, CHECKPOINT_KIND}:
        raise ValueError(f"unsupported checkpoint kind: {metadata.get('checkpoint_kind')}")
    version = int(metadata.get("checkpoint_version", CHECKPOINT_VERSION))
    if version != CHECKPOINT_VERSION:
        raise ValueError(f"unsupported checkpoint version: {version}")
    return AntSandboxCheckpoint(
        config=AntSandboxConfig.from_dict(dict(payload["config"])),
        world=AntSandboxWorld.from_dict(dict(payload["world"])),
        metadata=metadata,
    )
