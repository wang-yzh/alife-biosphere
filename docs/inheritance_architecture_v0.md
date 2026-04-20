# Inheritance Architecture v0

## Purpose

This document translates the genetics literature into a concrete inheritance
architecture for the biosphere.

It is deliberately conservative.

The goal is not to imitate all of biology at once. The goal is to give us a
usable staged design that:

- preserves lineage meaning;
- allows cumulative structure to emerge;
- avoids brittle reward-hacking shortcuts;
- can be implemented incrementally.

## 1. Design Rule

The biosphere should not have one inheritance channel.

It should have multiple channels with different timescales:

```text
genetic inheritance      slow, structural, high durability
epigenetic inheritance   fast, low bandwidth, decaying
somatic learning         within-lifetime only
ecological inheritance   world modifications inherited indirectly
cultural inheritance     shared archive, costly access
```

If these channels are collapsed together, we will lose the ability to say what
actually caused adaptation.

## 2. Recommended First-Cut Ontology

### Genome

The long-lived heritable structure.

It should encode:

- sensing biases
- developmental biases
- action-module priors
- regulation between modules
- metabolic and reproductive costs

It should not directly store:

- full lifetime traces
- full learned policy state
- free archive contents

### Epigenome

A small set of inherited marks representing recent ancestral conditions.

Examples:

- chronic scarcity
- chronic crowding
- chronic hazard exposure
- high archive dependence

Properties:

- low bandwidth
- limited persistence
- explicitly decays by generation

### Soma Memory

The within-lifetime learned state.

Examples:

- recently successful protocol routes
- habitat familiarity
- trusted archive entries
- local avoidance patterns

Properties:

- can improve fitness
- can influence reproduction
- does not directly become genome

### Ecological Memory

Persistent environmental modifications.

Examples:

- depleted resource patches
- built shelters
- trails or markers
- altered hazard distributions

Properties:

- inherited indirectly
- often affects kin and non-kin differently

### Cultural Archive

A population or clade-level store of transmissible capsules.

Examples:

- compact protocol fragments
- habitat-specific heuristics
- migration motifs
- repair / harvest sequences

Properties:

- access must be costly
- visibility must be bounded
- should not be free omniscience

## 3. Genome Shape

The genome should be modular from the start.

Recommended initial gene families:

### 3.1 Sensor genes

Examples:

- local resource sensitivity
- hazard sensitivity
- crowding sensitivity
- kin-signal sensitivity
- archive-signal sensitivity

### 3.2 Regulator genes

Examples:

- threshold rules
- activation gates
- inhibition links
- developmental stage gates

### 3.3 Action-module genes

Examples:

- explore
- exploit
- repair
- reproduce
- migrate
- signal
- guard

### 3.4 Metabolic genes

Examples:

- base metabolism
- complexity cost multiplier
- learning cost sensitivity
- archive access cost sensitivity

### 3.5 Reproductive genes

Examples:

- maturity threshold
- offspring budget fraction
- bottleneck size
- parental investment tendency

### 3.6 Development genes

Examples:

- juvenile plasticity
- consolidation strength
- epigenetic sensitivity
- phenotype canalization strength

## 4. Gene Identity And Alignment

Every structural gene should carry:

```text
gene_id
innovation_id
module_type
origin_parent_gene_id
active_flag
parameter_payload
```

`innovation_id` is the most important field for future recombination.

Without it, crossover becomes positional and mostly meaningless.

## 5. Mutation Operators

Mutation should not be only scalar jitter.

Recommended mutation families:

### 5.1 Point mutation

- small parameter drift
- threshold changes
- mild bias changes

### 5.2 Toggle mutation

- activate / deactivate a module
- useful for latent structure and conditional complexity

### 5.3 Duplication

- copy a whole module or subgraph
- preserve ancestry link to source module

### 5.4 Divergence

- mutate a duplicated module more aggressively
- expected to drive specialization

### 5.5 Regulatory rewiring

- change which regulator gates which module
- should be limited and logged carefully

### 5.6 Deletion

- remove dead or costly structure
- necessary to prevent unchecked genome growth

## 6. Reproduction Order

### v0: clonal inheritance only

Use:

```text
single parent
+ mutation
+ duplication/divergence
```

Reason:

- easiest to interpret
- strongest lineage clarity
- least destructive

### v1: clonal + epigenetic carryover

Use:

```text
single parent
+ inherited epigenetic marks
+ limited developmental bias carryover
```

Reason:

- lets us test short-horizon inherited pressure memory
- still keeps ancestry clean

### v2: homologous crossover

Use only after:

- innovation ids are stable
- lineage logging is mature
- duplication/divergence is already working

Rule:

- align by `innovation_id`
- mismatched genes are treated as excess/disjoint, not forced into position

### v3: horizontal transfer

Use only after:

- populations are ecologically interacting
- module boundaries are meaningful
- archive and kin structure already exist

Candidate form:

- rare module transfer between co-located organisms
- possibly biased by kin, trust, or ecological stress

## 7. Epigenetic Design

Epigenetic marks should be simple enough to inspect directly.

Recommended structure:

```text
EpigeneticMark
- mark_type
- magnitude
- generation_ttl
- induction_source
```

Recommended mark types:

- scarcity
- crowding
- hazard
- archive_dependence
- migration_pressure

Effects:

- shift developmental thresholds
- raise or lower plasticity
- bias module activation priors

Hard rule:

- marks must decay
- they are not permanent pseudo-genes

## 8. Cultural Inheritance Design

The cultural archive is not a backup genome.

It should store compressed capsules with:

```text
capsule_id
origin_lineage_id
origin_habitat_family
trigger_signature
behavior_fragment
estimated_cost
estimated_benefit
reuse_count
decay_or_refresh_rule
```

Archive access should cost:

- time
- energy
- attention / information

This prevents culture from erasing selection.

## 9. Ecological Inheritance Design

World changes should themselves be treated as inherited structure.

Examples:

- a lineage depletes one habitat and leaves another rich
- a lineage creates a stable route between habitats
- a lineage leaves persistent signals that bias descendants

These are not copied through the genome, but through the world state.

Therefore the event log should preserve:

- constructor lineage
- affected habitat
- persistence duration
- descendant reuse events

## 10. What We Should Measure

Genetic metrics:

- lineage depth
- genome size
- duplication count
- deletion count
- innovation survival time
- mutational survivability

Epigenetic metrics:

- mark prevalence
- mean mark lifetime
- intergenerational carryover effect

Cultural metrics:

- capsule reuse count
- capsule survival time
- cumulative improvement
- archive overload rate

Ecological metrics:

- lineage-caused habitat persistence
- descendant reuse of altered habitats
- niche occupancy after environmental modification

## 11. Controls

We should plan controls before implementation.

Minimum inheritance controls:

```text
A. no inheritance
B. genome only
C. genome + epigenetic
D. genome + archive
E. genome + ecological inheritance
F. full system
```

Without these controls, the inheritance story will become anecdotal.

## 12. Recommended Implementation Order

### Step 1

Implement:

- modular genome
- clonal inheritance
- mutation + duplication + deletion
- lineage logging

### Step 2

Implement:

- explicit developmental stage
- decaying epigenetic marks

### Step 3

Implement:

- compressed cultural capsules
- costly archive access

### Step 4

Implement:

- homologous crossover
- optional horizontal transfer

## 13. Final Position

The most useful inheritance architecture for the first real biosphere is:

```text
slow modular genome
+ short-lived epigenetic bias
+ costly cultural archive
+ ecological inheritance through habitat change
```

This is strong enough to generate life-history structure without forcing us to
pretend that all adaptation is genetic.
