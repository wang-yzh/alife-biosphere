# Memory, Forgetting, And Distributed Memory Review v0

## Purpose

This note extends the literature program toward one of the deepest recurring
questions in `alife_biosphere`:

```text
Where does memory actually live in a living system?
```

The goal is to move beyond treating memory as a single buffer or log.

In practice, this note asks:

1. Why is memory not just storage, but stabilization and reactivation?
2. Why is forgetting not simply failure?
3. How can memory exist above the individual, in groups, lineages, and habitats?
4. What should a proper memory stack look like in the biosphere?

## Short Answer

The literature points to a layered answer:

```text
memory is not one thing.
it can be:
- an individual trace,
- a consolidated behavioral bias,
- a distributed group pattern,
- a lineage-carried inheritance bias,
- or an ecological structure preserved in the habitat itself.
```

It also suggests:

```text
forgetting is not only loss.
it is often part of how a memory system stays selective, adaptive, and usable.
```

For our project, this means:

- we should not build one monolithic memory module;
- different layers of memory should have different persistence, cost, and access
  rules;
- habitat memory and collective memory are not metaphors, but real design
  targets;
- archive growth without pruning would be a broken memory ecology.

## Core Papers

## 1. Squire, Genzel, Wixted, Morris (2015), "Memory consolidation"

Why it matters:

- this is the cleanest broad review of consolidation as a process
- it gives us a very useful distinction between recent, fragile memory and
  longer-term stabilized memory

The key lesson:

```text
memory does not begin in its final form.
it is transformed from a labile trace into a more stable long-term form.
```

This is immediately relevant to `alife_biosphere`.

If an organism or lineage "remembers" something, that memory should not appear
fully formed the instant an event occurs.

Design implication:

- lifetime experience should begin as provisional local memory
- consolidation should be costly and delayed
- later inherited or archived structure should be treated as transformed memory,
  not raw episodic residue

Useful translation into biosphere terms:

- `recent_memory_load`
- `consolidation_cost`
- `consolidated_capsule_count`
- `memory_age`

## 2. Josselyn, Köhler, Frankland (2015), "Finding the engram"

Why it matters:

- this is the strongest conceptual source for engram-like persistence
- it defines memory not as a log entry, but as a physical persistent trace that
  can later be reactivated

What we should take from it:

- a memory trace should be selective
- it should be reactivatable
- it should have persistence beyond immediate use

We should not import neuroscience literally.
But the engram idea gives us a helpful design criterion:

```text
a real memory trace should survive long enough
to shape later behavior when relevant cues return
```

Design implication:

- biosphere memory should not be only replay history
- later capsules or priors should be cue-reactivated where possible
- memory strength should differ from mere frequency of occurrence

Useful translation into biosphere terms:

- `engram_like_trace_strength`
- `cue_reactivation_success`
- `trace_persistence`

## 3. Anderson and Hulbert (2021),
"Active Forgetting: Adaptation of Memory by Prefrontal Control"

Why it matters:

- this is one of the best clean statements that forgetting can be adaptive
- it helps us avoid a naive "more retained memory is always better" assumption

The key lesson:

```text
memory systems need selective forgetting
to reduce interference, overload, and bad retrieval competition
```

That is directly relevant to every future memory layer in the biosphere:

- organism memory
- archive memory
- group signaling memory
- lineage memory

Design implication:

- forgetting should be modeled as an active ecological function
- archive pruning and memory obsolescence should be features, not bugs
- some memory should be easier to suppress than to erase permanently

Useful translation into biosphere terms:

- `forgetting_pressure`
- `retrieval_interference`
- `capsule_suppression`
- `pruning_rate`

## 4. Bengtsson et al. (2003), "Reserves, resilience and dynamic landscapes"

Why it matters:

- this is one of the strongest ecological-memory papers for our purposes
- it gives a clear picture of memory living in landscape structure, species
  legacies, and surrounding patches

The key lesson:

```text
ecological memory is carried by species, interactions, and structures
that make reorganization after disturbance possible
```

This is exactly the version of ecological memory we need.

It means habitat memory is not:

```text
just one scalar history variable
```

It is more like:

```text
the persistence of traces that make certain futures easier to rebuild
```

Design implication:

- habitat memory should include remnant resources, occupancy traces, and support
  structures
- refuges and neighboring habitats can carry memory for disturbed zones

Useful translation into biosphere terms:

- `memory_field`
- `remnant_structure_score`
- `support_patch_link`
- `reorganization_potential`

## 5. Power et al. (2015), "What can ecosystems learn?"

Why it matters:

- this paper is unusually close to the kind of system we want
- it frames ecosystems as capable of a distributed, network-like form of memory

The key lesson:

```text
communities can "remember" past states through evolved interaction structure,
without any single unit containing the whole memory
```

This is a major design clue for `alife_biosphere`.

It suggests that memory can be distributed across:

- interaction strengths
- assembly rules
- ecological attractors
- historical coexistence structure

Design implication:

- the system should allow distributed ecological memory, not only local stored
  capsules
- community organization itself may store past experience

Useful translation into biosphere terms:

- `interaction_memory_score`
- `assembly_recall_pattern`
- `distributed_memory_strength`
- `ecological_attractor_bias`

## 6. Couzin et al. (2002), "Collective memory and spatial sorting in animal groups"

Why it matters:

- this is a clean example of memory existing at the group level
- it shows how group history can influence later collective behavior even when
  no single member explicitly stores the whole pattern

What we should take from it:

- collective memory can arise from self-organized structure
- group history can bias future group dynamics

Design implication:

- group state should sometimes carry persistent bias
- collective organization can itself be a memory substrate

Useful translation into biosphere terms:

- `collective_memory_score`
- `group_history_bias`
- `spatial_role_persistence`

## 7. Friedman, Johnson, Linksvayer (2020),
"Distributed physiology and the molecular basis of social life in eusocial insects"

Why it matters:

- this is one of the clearest modern statements that regulation can occur at the
  colony level in distributed form
- it supports our intuition that not all memory-like regulation belongs inside
  one organism

What we should take from it:

- colony-level regulation can emerge from linked interacting individuals
- physiological and behavioral regulation can be distributed

This is highly relevant if we later build:

- group-level inheritance
- role switching
- archive access through social interaction
- distributed group decisions

Design implication:

- groups should be allowed to carry state that no single organism fully owns
- some regulatory memory may be maintained through interaction patterns

Useful translation into biosphere terms:

- `group_regulatory_state`
- `distributed_state_persistence`
- `role_signal_reservoir`

## What This Means For Our Project

The literature suggests that `alife_biosphere` should eventually support a real
memory stack, not just "memory" in the singular.

The most useful layered view is:

### 1. Recent organism memory

- fast, local, fragile
- tied to immediate lifetime experience

### 2. Consolidated organism memory

- slower, more persistent
- available for reuse within a lifetime

### 3. Lineage memory

- inherited structure
- biases descendant behavior or development

### 4. Collective memory

- stored in group organization, coordination, or role structure

### 5. Archive memory

- explicit socially accessible retained structure
- filtered, costly, bounded

### 6. Ecological memory

- stored in habitat traces, remnants, occupancy history, and interaction
  structure

This is a much better fit for the project than one generic `memory.py`.

## Direct Design Consequences

## 1. We should stop thinking of memory as one module

Future design should explicitly distinguish:

- individual memory
- inherited memory
- collective memory
- ecological memory
- archive memory

Suggested field groups:

- `recent_memory_*`
- `consolidated_memory_*`
- `lineage_memory_*`
- `collective_memory_*`
- `ecological_memory_*`

## 2. Consolidation should be a real process

Raw experience should not immediately become high-value inherited structure.

Suggested fields:

- `consolidation_cost`
- `consolidation_success`
- `memory_age`
- `trace_stability`

Suggested event types:

- `memory_encoded`
- `memory_consolidated`
- `memory_reactivated`

## 3. Forgetting should be active and selective

This is a major practical implication.

We should later allow:

- suppression of interfering memories
- archive pruning
- obsolescence after environmental shift
- memory loss under resource stress

Suggested fields:

- `forgetting_pressure`
- `interference_load`
- `obsolescence_score`

Suggested event types:

- `memory_suppressed`
- `memory_pruned`
- `memory_obsolete`

## 4. Habitat memory should be richer than one scalar history

Ecological memory should likely include:

- remnant resources
- support structures
- old occupancy traces
- disturbance legacy
- links to nearby refuge or source habitats

Suggested fields:

- `remnant_structure_score`
- `occupancy_trace`
- `disturbance_legacy`
- `support_patch_link`

## 5. Group state should be allowed to store memory-like bias

Collective memory suggests that groups can retain useful organization without
fully central memory storage.

Suggested fields:

- `group_history_bias`
- `collective_memory_score`
- `group_regulatory_state`

## Proposed Additions To The Existing Design

### New fields

- `recent_memory_load`
- `consolidation_cost`
- `trace_persistence`
- `forgetting_pressure`
- `collective_memory_score`
- `group_history_bias`
- `remnant_structure_score`
- `ecological_attractor_bias`

### New event types

- `memory_encoded`
- `memory_consolidated`
- `memory_reactivated`
- `memory_suppressed`
- `memory_pruned`
- `memory_obsolete`

### New metrics

- consolidation success rate
- cue-reactivation success
- interference burden
- archive pruning efficiency
- collective memory persistence
- ecological memory contribution to recovery

## Proposed Probe Design

The first memory-focused probe can stay narrow.

A reasonable first probe is:

```text
same world
-> repeated disturbances or repeated cues
-> compare no consolidation, consolidation without pruning,
   and consolidation with selective forgetting
-> measure recall usefulness, overload, and recovery
```

The first useful question is:

```text
Does selective consolidation plus selective forgetting produce better later
adaptation than either raw logging or unlimited retention?
```

That is enough to justify a layered memory design.

## Build Recommendations

This literature review suggests three near-term design tasks.

### 1. Add a memory-stack section to the core design

Reason:

- otherwise different memory layers will keep getting mixed together

### 2. Make forgetting an explicit design object

Reason:

- unlimited memory would break the ecology and the archive

### 3. Treat habitat and group organization as possible memory substrates

Reason:

- some of the most important memory in living systems may be distributed rather
  than locally stored

## Bottom Line

The memory literature tells us that the right question is not:

```text
does the system remember?
```

It is:

```text
what remembers,
what gets stabilized,
what gets reactivated,
and what gets forgotten?
```

For `alife_biosphere`, the strongest answer will likely be:

```text
memory exists at multiple levels,
and the ecology of remembering and forgetting is itself part of the living
system
```

That is the version worth building toward.

## Sources

- Squire, L. R., Genzel, L., Wixted, J. T., Morris, R. G. (2015).
  "Memory consolidation."
  [PubMed Central](https://pmc.ncbi.nlm.nih.gov/articles/PMC4526749/)
- Josselyn, S. A., Köhler, S., Frankland, P. W. (2015).
  "Finding the engram."
  [Nature Reviews Neuroscience](https://www.nature.com/articles/nrn4000)
- Anderson, M. C., Hulbert, J. C. (2021).
  "Active Forgetting: Adaptation of Memory by Prefrontal Control."
  [Annual Reviews](https://www.annualreviews.org/content/journals/10.1146/annurev-psych-072720-094140)
- Bengtsson, J., Angelstam, P., Elmqvist, T., Emanuelsson, U., Folke, C.,
  Ihse, M., Moberg, F., Nyström, M. (2003).
  "Reserves, resilience and dynamic landscapes."
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/14627367/)
- Power, D. A., Watson, R. A., Szathmáry, E., Mills, R., Powers, S. T.,
  Doncaster, C. P. (2015).
  "What can ecosystems learn? Expanding evolutionary ecology with learning
  theory."
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4672551/)
- Couzin, I. D., Krause, J., James, R., Ruxton, G. D., Franks, N. R. (2002).
  "Collective Memory and Spatial Sorting in Animal Groups."
  [University of Bristol record](https://research-information.bris.ac.uk/en/publications/collective-memory-and-spatial-sorting-in-animal-groups)
- Friedman, D. A., Johnson, B. R., Linksvayer, T. A. (2020).
  "Distributed physiology and the molecular basis of social life in eusocial
  insects."
  [Arizona State University record](https://asu.elsevierpure.com/en/publications/distributed-physiology-and-the-molecular-basis-of-social-life-in-)
