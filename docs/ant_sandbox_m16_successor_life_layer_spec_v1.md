# Ant Sandbox M16 Successor Life Layer Spec v1

## Purpose

M16 introduces the first non-ant organism layer.

This should happen only after:

- checkpoint branches are observable
- branches are comparable
- at least one niche substrate exists
- early open-endedness metrics can distinguish divergence from collapse

The successor life layer must depend on ant-created conditions.

If it can live without ants, it is not the right first successor.

## Core Rule

The first successor organism is not a new main character.

It is evidence that ant ecology can create a niche for something else.

## Candidate First Successors

### Decomposer

Depends on:

- corpses
- residue

Behavior:

- appears near corpses or high-residue cells
- consumes substrate
- may leave enriched soil or fungal substrate later

Why it is strong:

- directly matches the open-evolution idea that waste or death becomes another
  organism's resource
- low cognitive complexity
- easy to observe and measure

### Fungus

Depends on:

- residue
- nest-adjacent waste
- persistent traffic corridors
- damp or slow terrain if later added

Behavior:

- grows in patches
- spreads locally
- may alter trail persistence or food quality later

Why it is strong:

- creates spatial structures
- can become food, hazard, or symbiont later

### Scavenger

Depends on:

- corpses
- abandoned food fragments

Behavior:

- moves locally toward corpse or fragment substrate
- competes indirectly with ants for remains

Why it is weaker as first target:

- requires another mobile agent system
- easier to overbuild

### Seed Plant

Depends on:

- ant transport
- disturbed ground
- waste or residue

Behavior:

- emerges where ants move or deposit material
- creates future food classes

Why it should probably come later:

- introduces longer timescales
- needs a plant lifecycle and resource model

## Recommended First Choice

Start with:

```text
decomposer
```

Reason:

- corpses are a natural M14 substrate
- decomposers can be non-mobile or weakly spreading
- they create a clear dependency chain:

```text
ant death -> corpse -> decomposer -> enriched residue
```

This is the smallest real example of a derived niche.

## M16A Decomposer Data Model

Possible fields:

- `decomposer_id`
- `x`
- `y`
- `energy`
- `age`
- `source_corpse_id`
- `generation`
- `alive`

Simpler alternative:

- represent decomposer patches as grid cells rather than individual organisms

Recommendation:

```text
use patch/cell representation first
```

Reason:

- avoids adding a second mobile-agent system too early
- makes dependency and persistence easier to observe

## M16A Behavior

Initial decomposer patch behavior:

- can appear on corpse cells after a delay
- consumes corpse energy while present
- decays without substrate
- spreads weakly to adjacent high-residue cells
- leaves enriched residue after consuming corpse material

Initial non-behavior:

- no combat
- no intelligence
- no mutation
- no direct ant behavior changes unless explicitly tested

## Observer Requirements

Show:

- decomposer patches
- corpse substrate
- enriched residue
- dependency events

The visual goal is:

```text
the viewer can see that death created a new local ecology
```

## Event Requirements

Add events such as:

- `decomposer_emerge`
- `decomposer_feed`
- `decomposer_spread`
- `decomposer_decay`
- `residue_enriched`

Each event should include:

- tick
- location
- source substrate
- branch metadata through checkpoint context

## Metrics

Report:

- decomposer patch count
- decomposer occupied cells
- corpse-to-decomposer conversion count
- average decomposer duration
- enriched residue cells
- dependency edge count: `corpse -> decomposer`

## Tests

Required tests:

- decomposer can emerge only where substrate exists
- decomposer state survives checkpoint round-trip
- decomposer decays without substrate
- observer payload includes decomposer layer
- dependency metrics count corpse-to-decomposer links

Targeted test path:

```text
tests/test_ant_sandbox_successor_life.py
```

## Acceptance Criteria

M16 is complete when:

- one non-ant life layer exists
- it depends on ant-generated substrate
- it is visible in observer
- it is checkpointed
- branch comparison can report it
- M15 metrics can count at least one dependency edge

## Failure Modes

Stop if:

- successor life appears independently of ant activity
- successor life is only a decorative overlay
- successor life immediately dominates the simulation
- implementation requires complex agency before dependency is proven

## Execution Note

The first successor layer should be boring but real.

The project should prefer:

```text
one weak decomposer that proves derived niche formation
```

over:

```text
many dramatic organisms with unclear ecological dependency
```
