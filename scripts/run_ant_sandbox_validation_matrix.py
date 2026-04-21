from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from alife_biosphere.ant_sandbox.validation import DEFAULT_VALIDATION_SEEDS
from alife_biosphere.ant_sandbox.validation import run_validation_cases
from alife_biosphere.ant_sandbox.validation import summarize_validation_status


def main() -> None:
    cases = run_validation_cases(DEFAULT_VALIDATION_SEEDS)
    summary = summarize_validation_status(cases)
    output_dir = ROOT / "outputs" / "ant_sandbox_validation_matrix"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "cases.json").write_text(
        json.dumps([case.to_dict() for case in cases], indent=2),
        encoding="utf-8",
    )
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    print(summary)


if __name__ == "__main__":
    main()
