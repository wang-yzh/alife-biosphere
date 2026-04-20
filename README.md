# Alife Biosphere

This project starts a clean artificial-life research line after archiving:

- `maze_novelty`
- `market_novelty`

The goal is not to build another benchmark trainer. The goal is to build a
persistent world where:

- organisms are born, compete, reproduce, disperse, and die
- populations differentiate across habitats instead of collapsing immediately
  to one winner
- disturbance, recovery, and recolonization can happen without hidden resets
- habitats retain traces of occupancy, depletion, and recovery history

Current status:

- design phase
- M0 executable scaffold exists
- ecology-first north star: `docs/ecology_north_star_v1.md`
- baseline world design: `docs/world_design_v0.md`
- mechanism-rich predecessor design: `docs/world_design_v1.md`
- current world design: `docs/world_design_v2.md`
- observable target phenomena and red flags:
  `docs/observable_phenomena_and_failure_modes_v1.md`
- the genetics literature pass is in
  `docs/genetics_bibliography_v0.md`
- the first inheritance mechanism proposal is in
  `docs/inheritance_architecture_v0.md`
- the formal dual-inheritance / recombination models review is in
  `docs/formal_dual_inheritance_and_recombination_models_review_v0.md`
- the first literature gap review is in
  `docs/literature_gap_review_v0.md`
- the second literature gap review is in
  `docs/literature_secondary_gaps_v1.md`
- the resilience / regime-shift / signaling review is in
  `docs/resilience_regime_shift_and_signal_review_v1.md`
- the substrate / semantics / development blind-spot review is in
  `docs/substrate_artificial_chemistry_and_semantic_closure_review_v0.md`
- the open-endedness measurement review is in
  `docs/open_endedness_measurement_review_v0.md`
- the group reproduction / higher-level selection review is in
  `docs/group_reproduction_and_higher_level_selection_review_v0.md`
- the higher-level individuality claim standard is in
  `docs/higher_level_individuality_claim_standard_v0.md`
- the genotype–phenotype map / developmental constraints review is in
  `docs/genotype_phenotype_map_and_developmental_constraints_review_v0.md`
- the adaptive-cycle / trust mechanism note is in
  `docs/adaptive_cycle_and_trust_mechanisms_v1.md`
- the connectedness / trust-channel design note is in
  `docs/connectedness_and_trust_channel_design_v1.md`
- the antagonist lifecycle / parasite design review is in
  `docs/antagonist_lifecycle_and_parasite_design_review_v0.md`
- the parasite management / host-defense review is in
  `docs/parasite_management_and_host_defense_review_v0.md`
- the integrated research synthesis is in
  `docs/research_synthesis_v1.md`
- the warning / uncertainty design note is in
  `docs/warning_metrics_and_uncertainty_design_v1.md`
- the archive domain / provenance design note is in
  `docs/archive_domain_tags_and_provenance_design_v1.md`
- the unified bibliography is in
  `docs/unified_bibliography_v1.md`
- the unresolved-question register is in
  `docs/unresolved_question_register_v1.md`
- the disagreement / caution register is in
  `docs/disagreement_and_caution_register_v1.md`
- the theory contradiction map is in
  `docs/theory_contradiction_map_v1.md`
- the terminology index is in
  `docs/terminology_index_v1.md`
- the library inventory / gap map is in
  `docs/library_inventory_and_gap_map_v1.md`
- the experiment ledger is in
  `docs/experiment_ledger_v1.md`
- the negative-results ledger is in
  `docs/negative_results_ledger_v1.md`
- the claim-to-evidence table is in
  `docs/claim_to_evidence_table_v1.md`
- the ablation history is in
  `docs/ablation_history_v1.md`
- the minimal M1/M2 metric bundle note is in
  `docs/minimal_metric_bundle_for_m1_m2.md`
- the archive visibility / overload thresholds review is in
  `docs/archive_visibility_and_overload_thresholds_review_v0.md`
- baseline build plan: `docs/build_plan_v0.md`
- mechanism-heavy predecessor build plan: `docs/build_plan_v1.md`
- current build plan: `docs/build_plan_v2.md`
- current M1 ecology spec: `docs/m1_ecology_kernel_spec_v2.md`
- current working status: `docs/current_build_status_and_next_steps.md`
- documentation library index: `docs/README.md`
- documentation catalog: `docs/document_catalog_v1.md`

Near-term build order:

1. Ecology kernel
2. Reproduction and lineage
3. Disturbance and recovery
4. Habitat history and ecological memory
5. Niche formation and long-run ecology probes
6. Optional higher-order mechanisms

Non-goals for the first version:

- realistic economics
- photorealistic worlds
- large neural models
- leaderboard optimization

Active library for re-entry:

1. `docs/README.md`
2. `docs/current_build_status_and_next_steps.md`
3. `docs/ecology_north_star_v1.md`
4. `docs/world_design_v2.md`
5. `docs/observable_phenomena_and_failure_modes_v1.md`
6. `docs/build_plan_v2.md`
7. `docs/m1_ecology_kernel_spec_v2.md`
8. `docs/document_catalog_v1.md`
9. `docs/claim_to_evidence_table_v1.md`
10. `docs/experiment_ledger_v1.md`
11. `docs/negative_results_ledger_v1.md`
12. `docs/ablation_history_v1.md`

Background support:

- the remaining files in `docs/` are topic reviews, cautions, and detailed
  mechanism notes that back the active library, but are not required for a
  first-pass handoff.

## Development

Recommended local workflow:

```bash
python -m pip install -e ".[dev]"
python -m pytest
python scripts/run_smoke.py
python scripts/run_ecology_probe.py
```

Repository workflow:

- contribution guide: `CONTRIBUTING.md`
- CI workflow: `.github/workflows/ci.yml`
- PR template: `.github/pull_request_template.md`
