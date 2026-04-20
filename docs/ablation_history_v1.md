# Ablation History v1

## Purpose

This file tracks proposed, completed, and pending ablations for
`alife_biosphere`.

At the current stage, almost all ablations are still planned rather than run.
That is fine.
The point of this file is to stop proposed controls from being forgotten once
the codebase becomes busier.

## Status Labels

- `planned`
- `completed`
- `superseded`

## Table

| Ablation ID | Ablation | Status | Source document | Notes |
| --- | --- | --- | --- | --- |
| `ABL-001` | no-copy vs unconditional-copy vs validated-copy | `planned` | `build_plan_v1.md` | core archive / inheritance comparison |
| `ABL-002` | no signaling vs honest-only vs deception-enabled vs covert-signaling-enabled | `planned` | `build_plan_v1.md` | signaling control family |
| `ABL-003` | no disturbance vs synchronized disturbance vs asynchronous disturbance vs asynchronous disturbance without refuges | `planned` | `build_plan_v1.md` | disturbance and refuge control family |
| `ABL-004` | baseline graph vs modular graph vs dendritic graph | `planned` | `build_plan_v1.md` | topology family comparison |
| `ABL-005` | binary trust vs graded trust | `planned` | `adaptive_cycle_and_trust_mechanisms_v1.md` | trust representation comparison |
| `ABL-006` | one-observation trust vs short-window aggregated trust | `planned` | `adaptive_cycle_and_trust_mechanisms_v1.md` | trust memory comparison |
| `ABL-007` | no verification vs verify-when-uncertain vs always verify | `planned` | `adaptive_cycle_and_trust_mechanisms_v1.md` | verification policy comparison |
| `ABL-008` | signal cost only vs history-based honesty | `planned` | `adaptive_cycle_and_trust_mechanisms_v1.md` | honesty mechanism comparison |
| `ABL-009` | domain-aware archive vs domain-blind archive | `planned` | `archive_domain_tags_and_provenance_design_v1.md` | archive domain-tag comparison |
| `ABL-010` | full provenance vs source-id-only provenance | `planned` | `archive_domain_tags_and_provenance_design_v1.md` | provenance chain comparison |
| `ABL-011` | domain-specific source trust vs global source trust | `planned` | `archive_domain_tags_and_provenance_design_v1.md` | trust generalization comparison |
| `ABL-012` | validation-sensitive archive ranking vs popularity ranking | `planned` | `archive_domain_tags_and_provenance_design_v1.md` | archive ranking comparison |

## Completed Ablations

None formally completed yet.

That absence is expected at the current scaffold stage and is recorded here so
that "planned" does not quietly turn into "assumed done."

