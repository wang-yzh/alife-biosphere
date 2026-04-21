# Negative Results Ledger v1

## Purpose

This file records negative, null, or limiting results for `alife_biosphere`.

At the current stage, the project still has only a small run set.
So the most important negative records are still the current limits of what the
existing runs can show.

This is still worth recording, because otherwise the library risks drifting
into positive-story bias.

## Ledger

| ID | Kind | Source | Negative or limiting result | Why it matters |
| --- | --- | --- | --- | --- |
| `NEG-000` | smoke limitation | `outputs/smoke/summary.json` | The default smoke run now shows movement and births, but it still ends with `alive=13`, `dead=0`; it is too gentle to support claims about loss, rescue, or disturbance-driven recovery. | Prevents the default smoke run from being misread as evidence for resilience under stress. |
| `NEG-001` | probe limitation | `outputs/ecology_probe/derived_summary.json` | The current ecology probe still ends with many habitats empty and only `alive=5`; it shows partial persistence, not a robust sustained ecosystem. | Prevents the harsher probe from being overread as proof of stable long-run ecology. |
| `NEG-002` | evidence limitation | `tests/` and `outputs/` | Current evidence is still based on deterministic small-world smoke and probe runs. It does not yet establish multi-seed robustness, stable coexistence, or strong rescue dynamics. | Keeps the evidence layer honest and marks the gap between early signs and stronger ecological claims. |
| `NEG-003` | mechanism limitation | current code state | The project still does not implement compact inheritance, signaling, archive systems, antagonists, or higher-level group mechanisms. | Prevents later readers from confusing current ecological progress with completion of the larger mechanism library. |

## Current Interpretation

At this stage, the negative-results ledger is still mostly a limitation ledger.

That is appropriate.

The project should prefer explicit absence-of-evidence records over silent
inflation of what a smoke run supposedly proves.
