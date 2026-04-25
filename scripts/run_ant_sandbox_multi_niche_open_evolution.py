from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from alife_biosphere.ant_sandbox.campaign import run_multi_niche_open_evolution_campaign


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a forked multi-niche open evolution campaign.")
    parser.add_argument("--output-dir", type=Path, default=None, help="Directory for campaign outputs.")
    parser.add_argument("--campaign-id", default=None, help="Optional campaign identifier.")
    parser.add_argument("--root-seed", type=int, default=7, help="Seed for the root branch.")
    parser.add_argument("--root-tick", type=int, default=900, help="Tick horizon for the root branch.")
    parser.add_argument("--fork-additional-ticks", type=int, default=900, help="Ticks added to each fork after the root checkpoint.")
    parser.add_argument("--fork-seeds", nargs="*", type=int, default=[11, 29, 47], help="Seeds for fork branches.")
    parser.add_argument("--inheritance-mode", choices=("clone", "mutate", "resample"), default=None)
    parser.add_argument("--mutation-rate", type=float, default=None)
    parser.add_argument("--mutation-step", type=float, default=None)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output_dir = args.output_dir or ROOT / "outputs" / "ant_sandbox_multi_niche_open_evolution" / (
        args.campaign_id or "latest_campaign"
    )
    manifest = run_multi_niche_open_evolution_campaign(
        output_dir,
        campaign_id=args.campaign_id,
        root_seed=args.root_seed,
        root_tick=args.root_tick,
        fork_additional_ticks=args.fork_additional_ticks,
        fork_seeds=tuple(args.fork_seeds),
        inheritance_mode=args.inheritance_mode,
        mutation_rate=args.mutation_rate,
        mutation_step=args.mutation_step,
    )
    print(
        {
            "campaign_id": manifest["campaign_id"],
            "root_branch": manifest["root_branch"]["branch_id"],
            "forks": len(manifest["fork_branches"]),
            "comparison": manifest["comparison_json"],
            "open_endedness": manifest["open_endedness_json"],
        }
    )


if __name__ == "__main__":
    main()
