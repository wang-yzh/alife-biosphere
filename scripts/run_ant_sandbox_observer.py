from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from alife_biosphere.ant_sandbox import AntSandboxConfig
from alife_biosphere.ant_sandbox.observer import build_ant_observer_payload, write_ant_observer_html


def main() -> None:
    config = AntSandboxConfig(ticks=360)
    payload = build_ant_observer_payload(config, title="Ant Sandbox World")
    output_dir = ROOT / "outputs" / "ant_sandbox_observer"
    output_dir.mkdir(parents=True, exist_ok=True)
    write_ant_observer_html(output_dir / "observer.html", payload)
    (output_dir / "observer_data.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print({"ticks": payload["total_ticks"], "html": str(output_dir / "observer.html")})


if __name__ == "__main__":
    main()
