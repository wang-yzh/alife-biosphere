from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from alife_biosphere.ant_sandbox.comparison import build_branch_comparison_payload, write_branch_comparison


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare saved ant sandbox branches from checkpoint files.")
    parser.add_argument("--checkpoints", nargs="*", type=Path, default=None, help="Checkpoint files to compare.")
    parser.add_argument("--input-dir", type=Path, default=None, help="Directory to scan for checkpoint_final.json files.")
    parser.add_argument("--output-dir", type=Path, default=None, help="Directory for comparison.json and comparison.md.")
    return parser.parse_args()


def _collect_checkpoints(args: argparse.Namespace) -> list[Path]:
    paths: list[Path] = []
    if args.checkpoints:
        paths.extend(args.checkpoints)
    if args.input_dir is not None:
        paths.extend(sorted(args.input_dir.rglob("checkpoint_final.json")))
    unique = sorted({path.resolve() for path in paths if path.exists()})
    if not unique:
        raise ValueError("no checkpoint files found")
    return unique


def main() -> None:
    args = _parse_args()
    checkpoints = _collect_checkpoints(args)
    payload = build_branch_comparison_payload(checkpoints)
    output_dir = args.output_dir or ROOT / "outputs" / "ant_sandbox_branch_comparison" / payload["comparison_id"]
    json_path, markdown_path = write_branch_comparison(output_dir, payload)
    print(
        {
            "comparison_id": payload["comparison_id"],
            "families": payload["family_count"],
            "checkpoints": payload["checkpoint_count"],
            "json": str(json_path),
            "markdown": str(markdown_path),
        }
    )


if __name__ == "__main__":
    main()
