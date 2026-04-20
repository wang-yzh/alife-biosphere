# Claim To Evidence Table v1

## Purpose

This file maps current project claims to currently available evidence.

The goal is not to make the project look mature.
The goal is to separate:

- what is actually supported now
- what is only scaffold-supported
- what is still design-only

## Status Labels

- `supported_now`
- `partially_supported`
- `unsupported_yet`

## Table

| Claim ID | Claim | Status | Current evidence | Missing evidence |
| --- | --- | --- | --- | --- |
| `C-001` | The M0 scaffold runs deterministically under the default seed and config. | `supported_now` | `tests/test_simulation_smoke.py`; `outputs/smoke/summary.json`; `outputs/smoke/events.json` | none for the narrow scaffold claim |
| `C-002` | The scaffold emits structured events and serializes run outputs. | `supported_now` | `outputs/smoke/config.json`; `outputs/smoke/events.json`; `outputs/smoke/summary.json`; `src/alife_biosphere/io.py`; `tests/test_simulation_smoke.py` | none for the narrow scaffold claim |
| `C-003` | Basic habitat resource and organism integrity bounds hold under smoke conditions. | `supported_now` | `tests/test_world_invariants.py` | stronger stress tests outside smoke conditions |
| `C-004` | Config objects round-trip and basic validation works. | `supported_now` | `tests/test_config.py` | broader config coverage once more parameters exist |
| `C-005` | The project has a coherent mechanism design for inheritance, trust, archive structure, disturbance, and warning. | `partially_supported` | the mechanism documents under `docs/`, especially `world_design_v1.md`, `inheritance_architecture_v0.md`, `warning_metrics_and_uncertainty_design_v1.md`, `archive_domain_tags_and_provenance_design_v1.md` | running implementations and probe results for those mechanisms |
| `C-006` | The current executable scaffold already demonstrates ecological selection, rescue, lineage branching, or group organization. | `unsupported_yet` | none | actual implementations and probe outputs for those mechanisms |
| `C-007` | Vertical inheritance improves adaptation. | `unsupported_yet` | design rationale only | inheritance implementation plus ablation results |
| `C-008` | Bounded archive use is superior to naive copying. | `unsupported_yet` | theory and mechanism rationale only | archive implementation plus visibility / validation ablations |
| `C-009` | The project has evidence for higher-level individuality. | `unsupported_yet` | none; the project only has a claim standard | group-level reproduction, fitness decoupling, and controlled evidence |
| `C-010` | Warning metrics are currently reliable indicators in this project. | `unsupported_yet` | none; only warning-design rationale exists | warning outputs, retrospective scoring, false-alarm and miss accounting |

## Current Reading

The table shows that the project is presently strongest on:

- executable scaffold claims
- design coherence claims

It is currently weak on:

- mechanism efficacy claims
- evolutionary claims
- group-level claims
- archive and warning performance claims

That is the correct state of the evidence at this stage.

