# Ant Sandbox M13 Branch Comparison Spec v1

## Purpose

M13 makes forked futures comparable.

Open evolution cannot be judged from one run. The project needs to compare
branches that share a parent checkpoint and then diverge under changed seeds,
pressures, or later ecological conditions.

## Core Question

For one parent checkpoint:

```text
what different ecological futures become possible?
```

The answer should not be one fitness number.

It should be a structured comparison of survival, resource use, lineage
structure, spatial use, and ecological novelty.

## Scope

M13 should implement:

- a branch comparison script
- JSON summary output
- Markdown summary output
- provenance-aware branch grouping
- first branch-divergence metrics

M13 should not implement:

- open-endedness final scoring
- automatic scientific conclusions
- successor organisms
- new mutation operators
- new combat behavior

## Proposed Script

Add:

```text
scripts/run_ant_sandbox_branch_comparison.py
```

Example:

```bash
uv run python scripts/run_ant_sandbox_branch_comparison.py \
  --checkpoints \
  outputs/ant_sandbox_infinite_experiment/root/checkpoint_final.json \
  outputs/ant_sandbox_infinite_experiment/root_seed_11/checkpoint_final.json \
  outputs/ant_sandbox_infinite_experiment/root_seed_99/checkpoint_final.json
```

Optional output:

```bash
uv run python scripts/run_ant_sandbox_branch_comparison.py \
  --input-dir outputs/ant_sandbox_infinite_experiment \
  --output-dir outputs/ant_sandbox_branch_comparison/root_family
```

## Output Contract

Default output:

```text
outputs/ant_sandbox_branch_comparison/<comparison-id>/
  comparison.json
  comparison.md
```

The JSON file is the machine-readable contract.

The Markdown file is the human handoff artifact.

## Required Provenance Fields

For each branch:

- `branch_id`
- `run_id`
- `parent_branch_id`
- `parent_run_id`
- `parent_checkpoint`
- `forked_from_tick`
- `start_tick`
- `final_tick`
- `seed`
- `inheritance_mode`
- `mutation_rate`
- `mutation_step`

## Required Outcome Metrics

For each branch:

- alive count by colony
- births by colony
- deaths by colony
- unloads by colony
- pickups by colony
- nest food by colony
- total food remaining
- depleted source count
- contested source count
- combat start count
- max generation
- genome count
- mutated birth count
- unique lineage count
- total event count

## First Spatial Metrics

Branch comparison should include simple spatial signatures:

- occupied cell count over final alive ants
- trail cell count by colony
- home trail cell count by colony
- food trail cell count by colony
- top food source by pickup count

These are not final open-endedness metrics.

They are the first measurable branch fingerprints.

## First Divergence Metrics

For each pair of branches from the same parent:

- final alive delta
- unload delta
- nest food delta
- generation delta
- trail cell delta
- lineage count delta

Do not call the largest positive delta the winner.

The point is divergence, not ranking.

## Markdown Report Shape

The report should include:

1. Comparison id
2. Parent checkpoint family
3. Branch table
4. Outcome table
5. Spatial signature table
6. Pairwise divergence notes
7. Cautions

The caution section should explicitly say:

```text
These metrics show branch differences. They do not prove open-ended evolution.
```

## Tests

Required tests:

- comparison loads multiple checkpoint files
- comparison preserves provenance
- comparison emits JSON and Markdown
- pairwise branch deltas are computed
- branches from unrelated parents are flagged or grouped separately

Targeted test path:

```text
tests/test_ant_sandbox_branch_comparison.py
```

## Acceptance Criteria

M13 is complete when:

- three forks from one parent can be compared in one report
- comparison includes provenance and metrics
- no single scalar is used as universal fitness
- report is understandable without reading raw event logs

## Failure Modes

Stop if:

- branch comparison ignores fork metadata
- all conclusions are based on total food return
- unrelated checkpoints are silently compared as one family
- comparison requires manual JSON inspection

## Execution Note

This milestone turns M11 from a runtime feature into an experimental method.

After M13, the project can ask which branch histories create new ecological
opportunities.
