# Ant Sandbox Open Evolution Engineering Plan v1

## Purpose

This is the engineering plan for moving the ant sandbox from a stable colony
world toward an open-ended ecological evolution system.

The current ants are the first organism layer.

They are not the final subject.

The intended route is:

```text
ants survive in local space
-> ants modify the environment
-> modified environment creates new exploitable niches
-> new life layers depend on those niches
-> multiple branches discover different ecological structures
-> long-run comparison measures expanding possibilities
```

## Core Interpretation

Open evolution in this project means:

```text
new ecological possibilities can accumulate from earlier ecological activity
```

It does not mean:

- higher score over time
- larger mutation operators
- more species added by hand for spectacle
- scripted tech trees
- culture or symbolic intelligence
- combat as the main source of complexity

The core question is:

```text
Does one stable ecological pattern create conditions that make another
stable pattern possible?
```

## Current Base

The project currently has:

- local 2D ant movement
- three colonies
- terrain and walls
- pheromone trails
- food source depletion and reseeding
- hunger, feeding, starvation, old-age death
- nest-food-driven reproduction
- lineage, parent, genome, and generation bookkeeping
- bounded mutation and inheritance ablation controls
- checkpoint, resume, and fork runtime

This is enough to begin open-evolution infrastructure.

It is not enough to claim open-ended evolution yet.

## Execution Principle

Every new open-evolution feature must pass this chain:

```text
state representation
-> deterministic runtime behavior
-> observer visibility
-> branch comparison
-> documented interpretation
```

If a feature cannot be observed or compared across forks, it should not be
treated as an evolutionary result.

## Master Milestone Order

The next phase is:

```text
M12 checkpoint observer
M13 branch comparison ledger
M14 niche substrate
M15 open-endedness metrics
M16 first successor life layer
M17 multi-niche open evolution run
```

This order is intentional.

The project must be able to observe and compare long-run branches before adding
more ecology layers.

## M12 Checkpoint Observer

Goal:

```text
make saved and forked worlds visually inspectable
```

Why it comes first:

- checkpointed runs are now possible but still not first-class visual objects
- forked branches need provenance visible in the observer
- long-run claims are not trustworthy if the branch state is only JSON

Deliverable:

- branch-aware observer script
- final-state checkpoint renderer
- optional replay segment from checkpoint to target tick
- provenance labels in the UI

Detailed spec:

- `ant_sandbox_m12_checkpoint_observer_spec_v1.md`

## M13 Branch Comparison Ledger

Goal:

```text
compare alternate futures from the same parent checkpoint
```

Why it comes second:

- open evolution is branch-relative
- one run can be interesting but not evidential
- forks are the cleanest way to test whether different possibilities are being
  discovered

Deliverable:

- branch comparison script
- `comparison.json`
- `comparison.md`
- provenance-aware comparison table

Detailed spec:

- `ant_sandbox_m13_branch_comparison_spec_v1.md`

## M14 Niche Substrate

Goal:

```text
add environmental materials that can become future ecological opportunities
```

Why it comes third:

- new life layers need something to live from
- ecological niches should arise from world activity, not from decorative
  species injection
- ants must first become ecological engineers

First target materials:

- multiple food classes
- corpses
- waste or residue
- terrain-dependent trail persistence
- local resource conversion
- seasonal or pulse resources

Detailed spec:

- `ant_sandbox_m14_niche_substrate_spec_v1.md`

## M15 Open-Endedness Metrics

Goal:

```text
measure whether branches accumulate new stepping stones
```

Why it comes fourth:

- open-endedness must not collapse into one fitness score
- the project needs metrics before it adds successor organisms
- metrics will prevent false claims from impressive visuals

First metric families:

- branch divergence
- niche occupancy
- lineage persistence
- resource-chain depth
- traffic-loop novelty
- ecological dependency

Detailed spec:

- `ant_sandbox_m15_open_endedness_metrics_spec_v1.md`

## M16 First Successor Life Layer

Goal:

```text
introduce the first organism type that depends on ant-created conditions
```

Why it comes fifth:

- adding species before niche substrate would be arbitrary
- successor life should be a consequence of ant ecology
- the first non-ant organism should validate ecological dependency

Candidate first successor organisms:

- decomposer that feeds on corpses or waste
- fungus that grows along persistent trails or near nests
- scavenger that follows dead ants and abandoned food
- seed plant that depends on ant transport or disturbed ground

Detailed spec:

- `ant_sandbox_m16_successor_life_layer_spec_v1.md`

## M17 Multi-Niche Open Evolution Run

Goal:

```text
run long forked worlds where ants and successor life create different
ecological histories
```

Required prerequisites:

- M12 observer
- M13 comparison
- M14 niche substrate
- M15 metrics
- M16 successor life

Acceptance target:

- multiple forked branches from the same checkpoint show different stable
  ecological structures
- at least one structure depends on a niche created by earlier ant activity
- comparison reports the difference without reducing it to one score

## What Not To Build Yet

Do not prioritize:

- elaborate combat
- symbolic planning
- culture
- language
- social institutions
- heavy genomes
- neural controllers
- many species at once
- visual polish without new experimental meaning

These may become relevant later, but they are not the next bottleneck.

## Engineering Rules

Every milestone must include:

- code path
- script path
- output path
- observer or readable report
- tests for deterministic or structural invariants
- status-document update

Every claim must be classified as:

- implemented
- observed in one run
- observed across forks
- observed across seeds
- not yet supported

## First Execution Sequence

Assuming I execute the next work, I would do:

1. Implement M12 final-state checkpoint observer.
2. Add a short replay mode from checkpoint to target tick.
3. Implement M13 branch comparison JSON and Markdown.
4. Run three forks from one checkpoint.
5. Use comparison output to decide the first M14 niche substrate.
6. Add one environmental residue type.
7. Add metrics only after the residue is visible and measurable.

## Promotion Gate To Successor Life

M16 should not start until:

- branches can be observed
- branches can be compared
- at least one niche substrate exists
- the substrate changes ant traffic or survival in measurable ways

If these are not true, adding a decomposer or fungus would only be cosmetic.

## One-Sentence Handoff

The next engineering phase is not "make smarter ants".

It is:

```text
make ant activity create persistent ecological opportunities,
then make future branches and future organisms exploit those opportunities.
```
