# Ant Sandbox Handoff Plan v1

## Purpose

This is the handoff plan for a new maintainer or implementation agent taking
over the active `alife_biosphere` branch.

The project should be handed off as:

```text
an instinct-first, three-colony ant sandbox
with local movement, terrain, pheromones, death, reproduction,
genome bookkeeping, mutation controls, and checkpointed experiment branches
```

It should not be handed off as:

```text
a generic artificial-life framework
a graph ecology prototype
a combat game
a mutation-first evolution demo
```

The current strategic target is open-ended evolution through long-running,
branchable ecological experiments. The immediate engineering target is to make
those branches observable, comparable, and hard to misinterpret.

## Current State In One Page

The active branch is:

```text
experiment/ant-sandbox-world
```

The current verified status:

- `M1 spatial realism`: pass
- `M2 foraging loop`: pass
- `M3 pheromone effectiveness`: pass
- `M4 colony persistence`: pass
- `M5 role differentiation`: pass
- `M6 disturbance recovery`: pass
- `M10A simple lifecycle`: pass
- `M10B genome contract`: pass
- `M10C mutation and ablation controls`: pass
- `M11 infinite experiment runtime`: pass

The project now supports:

- local 2D ant movement
- three colonies: `Wei`, `Shu`, `Wu`
- terrain and walls
- food source depletion and reseeding
- pheromone trails
- hunger, feeding, starvation, old-age death
- nest-food-driven reproduction
- parent, lineage, genome, and generation bookkeeping
- bounded mutation and `clone / mutate / resample` controls
- checkpoint, resume, and fork runtime

Latest full verification at handoff:

```text
uv run pytest
55 passed
```

## Required First Read

Read these files in order:

1. `../README.md`
2. `docs/README.md`
3. `docs/ant_sandbox_status_v1.md`
4. `docs/ant_sandbox_m10a_lifecycle_slice_2026-04-24.md`
5. `docs/ant_sandbox_m10b_genome_v1_slice_2026-04-24.md`
6. `docs/ant_sandbox_m10c_mutation_ablation_slice_2026-04-24.md`
7. `docs/ant_sandbox_m11_infinite_experiment_runtime_slice_2026-04-24.md`
8. `docs/ant_sandbox_world_design_v2.md`
9. `docs/ant_sandbox_build_plan_v2.md`

Do not start from old habitat-graph ecology documents unless you are checking
project history. They are background, not the active implementation contract.

## Required First Run

Before editing, run:

```bash
uv run pytest
```

Generate the replay observer:

```bash
uv run python scripts/run_ant_sandbox_observer.py
```

Open:

```text
outputs/ant_sandbox_observer/observer.html
```

Run a checkpointed branch:

```bash
uv run python scripts/run_ant_sandbox_infinite_experiment.py \
  --branch-id handoff_root \
  --target-tick 600 \
  --checkpoint-every 200
```

Fork it:

```bash
uv run python scripts/run_ant_sandbox_infinite_experiment.py \
  --checkpoint outputs/ant_sandbox_infinite_experiment/handoff_root/checkpoint_final.json \
  --branch-id handoff_seed_99 \
  --seed 99 \
  --additional-ticks 300
```

The receiver should not claim the handoff is understood until both the replay
observer and checkpoint fork have been run locally.

## Handoff Decision

The next maintainer should continue from `M12`, not from mutation or from
adding new organisms prematurely.

The current immediate sequence is:

```text
M13 branch comparison ledger
M14 niche and resource expansion
M15 open-endedness metrics
M16 first successor life layer
```

This ordering matters.

If the project adds mutation, combat, or more species before branch visibility
and comparison exist, the results will become anecdotal. The system will look
more complex but become less interpretable.

The controlling post-`M11` engineering plan is:

- `ant_sandbox_open_evolution_engineering_plan_v1.md`
- `ant_sandbox_m12_checkpoint_observer_spec_v1.md`
- `ant_sandbox_m13_branch_comparison_spec_v1.md`
- `ant_sandbox_m14_niche_substrate_spec_v1.md`
- `ant_sandbox_m15_open_endedness_metrics_spec_v1.md`
- `ant_sandbox_m16_successor_life_layer_spec_v1.md`

## M12 Checkpoint Observer

Goal:

```text
make checkpointed branches visible without replaying only from default config
```

Required behavior:

- load `checkpoint_final.json`
- render final world state
- optionally render a replay segment from a checkpoint to a later tick
- display branch id, parent branch id, fork tick, seed, and target tick
- preserve existing ant-world visual style

Acceptance criteria:

- a branch created by `run_ant_sandbox_infinite_experiment.py` can be opened in
  an observer
- the observer labels the branch provenance
- the observer does not hide that it is viewing a forked history

Do not make this a complex dashboard first. The first version should be a
branch-aware observation window.

## M13 Branch Comparison Ledger

Goal:

```text
compare alternate futures from the same checkpoint
```

Required branch metrics:

- final alive count by colony
- total births by colony
- total deaths by colony
- total unloads by colony
- food remaining
- nest food by colony
- max generation
- genome count
- mutation count
- branch duration
- parent checkpoint and fork tick

Minimum useful output:

```text
outputs/ant_sandbox_branch_comparison/
  comparison.json
  comparison.md
```

Acceptance criteria:

- at least three forks from one checkpoint can be compared in one table
- comparison includes provenance, not only final scores
- no single scalar is treated as "fitness"

## M14 Niche And Resource Expansion

Goal:

```text
create more ecological opportunities without forcing a target behavior
```

Candidate additions:

- multiple food classes with different handling costs
- seasonal food availability
- terrain-dependent trail decay
- hidden or low-value resource patches that become useful later
- waste or dead-body residue as future resource substrate
- localized safe zones and risky shortcuts

Acceptance criteria:

- ants can discover and exploit more than one persistent resource type
- at least one resource type changes the map's long-run traffic structure
- branch comparison can show different futures exploiting different resources

Do not start with flight, tool use, or symbolic learning. Those are too large
for the current substrate.

## M15 Open-Endedness Metrics

Goal:

```text
measure whether branches accumulate new stepping stones
```

Candidate metrics:

- distinct occupied spatial corridors over time
- distinct exploited food classes
- lineage survival depth
- branch-to-branch behavioral divergence
- new stable traffic loops
- resource dependency chains
- recovery after resource relocation

Required caution:

```text
open-endedness is not equal to higher score
```

The project should track novelty, persistence, and ecological dependency, not
only food return.

## Non-Negotiable Guardrails

Do not re-center the project on:

- culture
- language
- symbolic planning
- human-like intelligence
- large combat systems
- mutation without comparison
- beautiful UI without experimental meaning

Do preserve:

- local movement
- visible world behavior
- instinct-first control
- environmental traces
- colony-level pressure
- branchable experiment history
- tests before claims
- documentation updates with every conceptual shift

## Reviewer Brief

The reviewer should focus on these failure modes:

- a new feature makes the world look richer but reduces interpretability
- a run is described as evolutionary without branch comparison
- mutation is treated as the main source of open-endedness
- observer visuals imply behavior that the simulation does not actually model
- checkpoint and fork metadata are missing from outputs
- old habitat-graph assumptions leak back into ant-sandbox documents

The reviewer should ask:

```text
Can a new maintainer reproduce this run,
fork it,
observe it,
compare it,
and explain what changed?
```

If not, the feature is not handoff-safe.

## First Week Plan

Day 1:

- run the full tests
- generate the replay observer
- run one checkpointed branch
- fork that branch once
- read the required first-read documents

Day 2:

- implement or inspect M12 checkpoint observer entrypoint
- verify branch metadata is visible
- document any mismatch between checkpoint state and observer display

Day 3:

- implement the first M13 branch comparison JSON
- compare three forks from one parent checkpoint

Day 4:

- add markdown summary output for branch comparison
- update status docs and experiment ledger

Day 5:

- decide whether M14 should start with multiple food classes, seasonal
  availability, or terrain-dependent trail decay

## Stop Conditions

Stop and realign if:

- all branches converge to the same behavior with no measurable divergence
- event logs or checkpoints become too large to inspect
- observer output cannot identify which branch it is showing
- a proposed feature needs many hidden global rules
- test results pass but visual behavior clearly contradicts the claim

## Minimal Definition Of A Successful Handoff

A receiver has successfully taken over when they can:

- explain the current project in one paragraph
- run the observer
- run and fork a checkpointed experiment
- identify the next milestone as M13
- state why mutation is not currently the main priority
- update docs when changing the project direction

Until then, the project is not actually handed off.
