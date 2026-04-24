from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from alife_biosphere.ant_sandbox import build_showcase_config
from alife_biosphere.ant_sandbox.observer import build_ant_observer_payload, write_ant_observer_html


def main() -> None:
    base = build_showcase_config(seed=7, ticks=1200)
    config = replace(base, ants=replace(base.ants, inheritance_mode="mutate", mutation_rate=0.35, mutation_step=0.06))
    payload = build_ant_observer_payload(config, title="Ant Sandbox World - Mutation Probe")
    output_dir = ROOT / "outputs" / "ant_sandbox_inheritance_observer"
    output_dir.mkdir(parents=True, exist_ok=True)
    write_ant_observer_html(output_dir / "observer.html", payload)
    (output_dir / "observer_data.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print({"ticks": payload["total_ticks"], "html": str(output_dir / "observer.html")})


if __name__ == "__main__":
    main()
