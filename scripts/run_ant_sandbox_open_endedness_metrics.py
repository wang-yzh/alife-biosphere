from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from alife_biosphere.ant_sandbox.comparison import build_branch_comparison_payload
from alife_biosphere.ant_sandbox.open_endedness import (
    build_open_endedness_payload,
    write_open_endedness_report,
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate open-endedness metrics from ant sandbox branch comparisons.")
    parser.add_argument("--comparison", type=Path, default=None, help="Existing comparison.json file.")
    parser.add_argument("--checkpoints", nargs="*", type=Path, default=None, help="Checkpoint files to compare directly.")
    parser.add_argument("--input-dir", type=Path, default=None, help="Directory to scan for checkpoint_final.json files.")
    parser.add_argument("--output-dir", type=Path, default=None, help="Directory for metrics.json and metrics.md.")
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
    if args.comparison is not None:
        comparison_payload = json.loads(args.comparison.read_text(encoding="utf-8"))
    else:
        comparison_payload = build_branch_comparison_payload(_collect_checkpoints(args))
    payload = build_open_endedness_payload(comparison_payload)
    output_dir = args.output_dir or ROOT / "outputs" / "ant_sandbox_open_endedness" / payload["comparison_id"]
    json_path, markdown_path = write_open_endedness_report(output_dir, payload)
    print(
        {
            "comparison_id": payload["comparison_id"],
            "json": str(json_path),
            "markdown": str(markdown_path),
        }
    )


if __name__ == "__main__":
    main()
