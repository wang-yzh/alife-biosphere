# Library Inventory And Gap Map v1

## Purpose

This note inventories the current `alife_biosphere` library as it exists today.

It does not add new theory.
It does not introduce a new mechanism proposal.
It tries to answer a simpler question:

```text
What kind of library do we already have,
and what kinds of material are still missing?
```

The inventory is organized into five layers:

- theory
- mechanism
- implementation
- evidence
- open questions

That layer split is useful because the project is no longer short on ideas.
It is becoming uneven instead:

- some layers are dense
- some layers are thin
- some are well-indexed
- some are still scattered

## 1. Current High-Level Assessment

| Layer | Current condition | Main strength | Main gap |
| --- | --- | --- | --- |
| theory | strong | broad thematic coverage | theory coordination is now much stronger; remaining work is selective rather than structural |
| mechanism | strong | many mechanism-specific notes | not enough cross-mechanism dependency mapping |
| implementation | moderate | M0 scaffold and implementation plans exist | thin experiment-operations layer |
| evidence | moderate | ledgers now exist and current scaffold evidence is registered | evidence population is still very sparse |
| open questions | strong | backlog and register exist | integration with evidence is still thin |

Short version:

```text
The library is rich in explanation,
respectable in mechanism thinking,
acceptable in implementation planning,
and now mainly limited by the thinness of its evidence rather than by missing
document types.
```

## 1.1 Gap Write-Off Summary

Several earlier gap lists have effectively been closed and should no longer be
treated as active blanks.

Closed or substantially closed:

- founder / lineage-turnover literature gap
- resilience / collapse / recovery literature gap
- signaling / trust / deception literature gap
- dual-inheritance / forgetting literature gap
- M1 kernel-spec documentation gap
- warning / uncertainty mechanism gap
- archive provenance / domain-tag design gap
- connectedness / trust-channel design gap
- higher-level individuality claim-standard gap
- archive visibility / overload threshold gap
- unified bibliography gap
- unresolved-question register gap
- disagreement / caution register gap
- terminology-index gap

What this means:

```text
The project no longer mainly lacks topics or coordination categories.
It mainly lacks accumulated evidence inside the categories that now exist.
```

## 1.2 Active Remaining Gaps Only

To avoid proliferating blank checklists, the current position is:

```text
the main document types now exist;
what remains is to populate them with real evidence.
```

The clearest remaining needs are:

- more real experiment entries
- more negative and null result entries
- claim updates tied to future outputs
- completed ablations rather than planned-only ablations

## 2. Theory Layer

## 2.1 What exists

The theory layer is the densest part of the library.

Representative files:

- `artificial_life_positioning_from_classic_papers.md`
- `major_transitions_and_group_individuality_review_v0.md`
- `cooperation_kin_selection_and_conflict_mediation_review_v0.md`
- `development_plasticity_and_life_history_review_v0.md`
- `memory_forgetting_and_distributed_memory_review_v0.md`
- `energy_flow_trophic_structure_and_ecosystem_engineering_review_v0.md`
- `information_control_self_organization_and_autonomy_review_v0.md`
- `evolvability_modularity_and_canalization_review_v0.md`
- `community_assembly_invasion_and_ecological_networks_review_v0.md`
- `resilience_collapse_and_recovery_review_v0.md`
- `signaling_trust_and_deception_review_v0.md`
- `spatial_ecology_metapopulation_and_dispersal_review_v0.md`
- `substrate_artificial_chemistry_and_semantic_closure_review_v0.md`
- `open_endedness_measurement_review_v0.md`
- `dual_inheritance_recombination_and_forgetting_review_v0.md`

This layer already covers most of the major idea families relevant to the
project:

- individuality transitions
- cooperation and conflict
- development and plasticity
- memory and forgetting
- energy and trophic structure
- autonomy and self-organization
- evolvability and modularity
- ecology and community assembly
- resilience and collapse
- signaling and deception
- spatial structure
- substrate and artificial chemistry
- measurement of open-ended dynamics
- multi-channel inheritance

## 2.2 What is strong here

- breadth is already good
- many reviews include design implications rather than only summaries
- the literature has been read with the project in mind instead of being stored
  as disconnected notes

## 2.3 What is still missing here

The main theory-layer gaps are not new themes.
They are now coordination and maintenance tasks around documents that already
exist.

### Missing item A. Bibliography upkeep discipline

The unified bibliography now exists.
What is still missing is stronger upkeep around:

- which reviews have already been folded into it
- which papers still remain only in local notes
- when a new reading should update the bibliography versus a topic review only

### Missing item B. Contradiction-to-design linkage

The contradiction map now exists.
What remains thin is the link between:

- literature disagreement
- concrete design cautions
- later implementation or metric choices

### Missing item C. Terminology drift control

The terminology index now exists.
The remaining risk is that later notes may still define terms locally instead
of reusing the shared glossary.

## 3. Mechanism Layer

## 3.1 What exists

Representative files:

- `world_design_v0.md`
- `world_design_v1.md`
- `inheritance_architecture_v0.md`
- `adaptive_cycle_and_trust_mechanisms_v1.md`
- `connectedness_and_trust_channel_design_v1.md`
- `warning_metrics_and_uncertainty_design_v1.md`
- `archive_domain_tags_and_provenance_design_v1.md`
- `minimal_metric_bundle_for_m1_m2.md`
- `higher_level_individuality_claim_standard_v0.md`
- `literature_to_mechanism_matrix_v0.md`
- `research_synthesis_v1.md`

This layer explains how theory is being translated into project structure.

It already includes:

- world ontology
- inheritance channel separation
- trust separation
- archive structure
- warning metric framing
- claim standards for higher-level individuality
- a synthesis-level mechanism summary

## 3.2 What is strong here

- the library is not stuck at abstract philosophy
- many key terms have at least one mechanism-facing document
- the project has already moved from "interesting ideas" to "candidate causal
  structures"

## 3.3 What is still missing here

### Missing item A. Cross-mechanism dependency map

Mechanisms exist, but the coupling between them is still spread across notes.

Examples:

- how trust interacts with archive ranking
- how disturbance interacts with connectedness proxies
- how group persistence interacts with rescue and founder history

### Missing item B. Optionality map

The mechanism layer mixes together:

- strong assumptions
- current working hypotheses
- exploratory possibilities

There is still no one place that says which parts are:

- central
- secondary
- speculative

### Missing item C. Code-to-mechanism traceability

The mechanism layer is ahead of the codebase.
That is fine at this stage, but it means:

- several mechanisms have no implementation anchor yet
- later contributors could read a mechanism note and still not know where it
  would live in the code or outputs

## 4. Implementation Layer

## 4.1 What exists

Representative documents:

- `build_plan_v0.md`
- `build_plan_v1.md`
- `repository_architecture_v0.md`
- `m1_biosphere_kernel_spec.md`
- `current_build_status_and_next_steps.md`

Representative non-document assets:

- `src/alife_biosphere/config.py`
- `src/alife_biosphere/rng.py`
- `src/alife_biosphere/habitat.py`
- `src/alife_biosphere/organism.py`
- `src/alife_biosphere/events.py`
- `src/alife_biosphere/world.py`
- `src/alife_biosphere/simulation.py`
- `src/alife_biosphere/io.py`
- `scripts/run_smoke.py`
- `tests/test_config.py`
- `tests/test_rng.py`
- `tests/test_simulation_smoke.py`
- `tests/test_world_invariants.py`

## 4.2 What is strong here

- there is a real M0 executable scaffold
- tests exist
- repository layout is not accidental
- there is already a kernel-specific spec for M1

## 4.3 What is still missing here

### Missing item A. Operations layer

The library now has ledgers and state summaries, but it still has very little
about:

- how experiments should be named
- how runs should be recorded
- how result folders should be structured
- how future contributors should interpret outputs

### Missing item B. Output-schema reference

There are mechanism notes about warning, archive provenance, and metrics, but
there is not yet a practical companion that explains:

- what output files exist
- which file stores what class of evidence
- which summary can be trusted for which conclusion

### Missing item C. Config catalogue

Configs exist in code, but the library does not yet have a concise catalogue of:

- which parameters are already real
- which ones are only discussed in design notes

That gap can cause theory and implementation to drift apart.

## 5. Evidence Layer

## 5.1 What exists

This is the thinnest layer in the current library.

Current evidence-like assets are mainly:

- test files
- `outputs/smoke/config.json`
- `outputs/smoke/events.json`
- `outputs/smoke/summary.json`
- `experiment_ledger_v1.md`
- `negative_results_ledger_v1.md`
- `claim_to_evidence_table_v1.md`
- `ablation_history_v1.md`

What that currently proves:

- the scaffold runs
- deterministic seeds work
- events are emitted
- basic world invariants hold in smoke conditions

## 5.2 What is missing here

This layer is now structurally present, but still thinly populated.

### Missing item A. More real experiment entries

The experiment ledger now exists.
What is missing is a larger set of actual probe entries beyond the scaffold
smoke baseline.

### Missing item B. More null and failed-result accumulation

The negative-results ledger now exists.
What is missing is a habit of recording weak signals, abandoned probes, and
mechanism failures as they happen.

### Missing item C. Faster claim updates

The claim-to-evidence table now exists.
What is missing is faster updating after each meaningful probe or mechanism
build.

### Missing item D. Completed ablation population

The ablation history now exists.
What is missing is a shift from planned-only ablations to completed,
interpretable comparisons.

## 5.3 Practical conclusion

The project is now evidence-poor relative to its theory depth.

That is acceptable for an early-stage research line.
But it is the clearest structural weakness in the current library.

## 6. Open-Questions Layer

## 6.1 What exists

The main explicit backlog file is:

- `literature_backlog_v1.md`
- `unresolved_question_register_v1.md`

Open questions also appear scattered through:

- `research_synthesis_v1.md`
- `adaptive_cycle_and_trust_mechanisms_v1.md`
- `warning_metrics_and_uncertainty_design_v1.md`
- `archive_domain_tags_and_provenance_design_v1.md`

## 6.2 What is missing here

### Missing item A. Question-to-evidence linkage

Status separation now exists through `unresolved_question_register_v1.md`.
What is still missing is tighter linkage between:

- each active question
- the next probe or ablation that would inform it
- the evidence file where the answer should later be recorded

## 7. The Actual Shape Of The Library

At the moment, the library looks like this:

```text
strong theory base
-> strong mechanism discussion
-> moderate implementation planning
-> moderate but thin evidence tracking
-> strong open-question tracking
```

This is a healthy early-stage pattern, but it is still incomplete.

## 8. What The Library Does Not Need Right Now

The project does not urgently need:

- many more new theory themes
- more topic breadth for its own sake
- more abstract framing documents without new coordination value

The theory side is already broad enough to support the current research
direction.

## 9. What The Library Most Clearly Lacks

If we rank missing layers by urgency:

1. evidence population and experiment throughput
2. output-schema / operations coordination
3. code-to-mechanism traceability and cross-mechanism dependency mapping

This is the cleanest current diagnosis of the library.
