# Negative Results Ledger v1

## Purpose

This file records negative, null, or limiting results for `alife_biosphere`.

At the current stage, the project has not yet run a formal experimental suite.
So the most important negative records are not failed headline experiments.
They are the current limits of what existing runs can show.

This is still worth recording, because otherwise the library risks drifting
into positive-story bias.

## Ledger

| ID | Kind | Source | Negative or limiting result | Why it matters |
| --- | --- | --- | --- | --- |
| `NEG-000` | scope limitation | `outputs/smoke/summary.json` | The only recorded run is a short smoke run with `alive=8` and `dead=0`; it does not exercise collapse, rescue, founder turnover, or reproductive dynamics. | Prevents the smoke run from being misread as evidence for ecological resilience or selective pressure. |
| `NEG-001` | unsupported-claim warning | `current_build_status_and_next_steps.md` | M0 explicitly does not yet implement migration, reproduction, lineage graph, mutation, life stages, protocol discovery, somatic learning, inheritance packets, cultural archive, species inference, or coevolving habitats. | Prevents accidental claims that these mechanisms have already been empirically exercised. |
| `NEG-002` | evidence limitation | `tests/` and `outputs/smoke/` | Current tests and outputs verify determinism, bounded resources, and basic event emission only. They do not yet verify any of the stronger artificial-life research mechanisms. | Keeps the evidence layer honest and makes clear that most current claims remain design-level rather than experimental. |

## Current Interpretation

At this stage, the negative-results ledger is mostly a limitation ledger.

That is appropriate.

The project should prefer explicit absence-of-evidence records over silent
inflation of what a smoke run supposedly proves.

