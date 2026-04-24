from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from alife_biosphere.ant_sandbox.observer import build_ant_checkpoint_observer_payload, write_ant_observer_html


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render an observer for a saved ant sandbox checkpoint branch.")
    parser.add_argument("--checkpoint", type=Path, required=True, help="Checkpoint JSON file to inspect.")
    parser.add_argument("--target-tick", type=int, default=None, help="Optional continuation replay target tick.")
    parser.add_argument("--output-dir", type=Path, default=None, help="Optional observer output directory.")
    parser.add_argument("--title", default="Ant Sandbox Branch", help="Observer window title.")
    return parser.parse_args()


def _branch_dir_name(payload: dict[str, object]) -> str:
    metadata = dict(payload.get("checkpoint_metadata", {}))
    branch_id = metadata.get("branch_id")
    if branch_id:
        return str(branch_id)
    return f"checkpoint_tick_{payload['loaded_tick']}"


def main() -> None:
    args = _parse_args()
    payload = build_ant_checkpoint_observer_payload(
        args.checkpoint,
        title=args.title,
        target_tick=args.target_tick,
    )
    output_dir = args.output_dir or ROOT / "outputs" / "ant_sandbox_checkpoint_observer" / _branch_dir_name(payload)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_ant_observer_html(output_dir / "observer.html", payload)
    (output_dir / "observer_data.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (output_dir / "checkpoint_metadata.json").write_text(
        json.dumps(payload.get("checkpoint_metadata", {}), indent=2),
        encoding="utf-8",
    )
    print(
        {
            "loaded_tick": payload["loaded_tick"],
            "target_tick": payload["target_tick"],
            "replayed_from_checkpoint": payload["replayed_from_checkpoint"],
            "html": str(output_dir / "observer.html"),
        }
    )


if __name__ == "__main__":
    main()
