# Dual Inheritance, Recombination, And Forgetting Review v0

## Purpose

This note is the fourth targeted literature follow-up from
`docs/literature_backlog_v1.md`.

The goal is to clarify how inheritance should work once `alife_biosphere` moves
past simple parent-to-child transfer.

In practice, this note asks:

1. Why should vertical and horizontal inheritance be separated?
2. Why is archive access not automatically beneficial?
3. Why do recombination, filtering, and forgetting matter as much as storage?

## Short Answer

The literature supports a very useful position:

```text
Inheritance should not be treated as one channel.
Vertical inheritance, horizontal transmission, and ecological inheritance have
different dynamics, different costs, and different failure modes.

A useful archive is not a free infinite memory.
It must have bandwidth limits, filtering, copying costs, and forgetting or
obsolescence.
```

For our project, that means:

- archive access should be costly and conditional;
- vertical and horizontal transfer should be logged separately;
- recombination should be explicit rather than assumed;
- forgetting is not a bug but part of ecological realism.

## Core Papers

## 1. Cavalli-Sforza and Feldman (1978),
"A dual inheritance model of the human evolutionary process I"

Why it matters:

- this is the formal starting point for dual inheritance in the sense we need
- it makes clear that cultural and genetic transmission are distinct channels
  that jointly shape phenotype

What we should take from it:

- inherited structure does not need to travel through one mechanism only
- the same trait outcome can be influenced by multiple transmission routes
- transmission logic should be made explicit rather than buried in one
  controller update rule

This is highly relevant to us because our future system already implies at least
three different inheritance routes:

- vertical inheritance from parent lineage
- horizontal transfer through archive or peers
- ecological inheritance through habitat memory

Design implication:

We should log those channels separately from the beginning.

Useful translation into biosphere terms:

- `inheritance_mode`
- `vertical_capsule_count`
- `horizontal_capsule_count`
- `ecological_memory_exposure`

## 2. Feldman and Cavalli-Sforza (1975),
"Models for cultural inheritance: a general linear model"

Why it matters:

- this paper reinforces that cultural transmission is not a vague extra layer
- it is modelable as a transmission process with its own structure

What we should take from it:

- transmission weights matter
- who learns from whom matters
- cultural dynamics need not mirror biological inheritance

Design implication:

- social transfer should specify source selection, not just "archive was used"
- transmission opportunities should be structured by exposure and availability

Useful translation into biosphere terms:

- `teacher_availability`
- `archive_visibility_limit`
- `copy_fidelity`
- `social_exposure_count`

## 3. Henrich and McElreath (2007), "Dual-Inheritance Theory"

Why it matters:

- this is the clean modern synthesis for what dual inheritance means in
  practice
- it gives us a usable conceptual separation between biological and cultural
  transmission without forcing us to imitate human anthropology literally

What we should take from it:

- cultural transmission runs on different timescales than vertical inheritance
- social learning can produce cumulative change without replacing lineage
  structure
- the transmission channel itself changes what kinds of adaptation are possible

Design implication:

- archive learning should not be treated as just delayed reproduction
- vertical and horizontal channels should be allowed to conflict or cooperate
- social transmission should have its own bias and cost structure

Useful translation into biosphere terms:

- `transmission_bias`
- `archive_access_fee`
- `copy_time_budget`
- `vertical_horizontal_balance`

## 4. Henrich, Boyd, Richerson (2008),
"Five Misunderstandings About Cultural Evolution"

Why it matters:

- this is especially useful as a warning document
- it helps prevent naive archive design

What we should take from it:

- cumulative adaptive culture does not require perfect discrete meme-like units
- successful transmission does not automatically mean adaptive value
- copying processes are shaped by multiple biases and selective contexts

This matters directly to us because otherwise we may accidentally assume:

```text
more copied capsules = better archive
```

That is not justified.

Design implication:

- archive success should not be measured only by reuse count
- copied capsules can spread for the wrong reasons
- evaluation should track downstream ecological value, not only transmission

Useful translation into biosphere terms:

- `capsule_reuse_count`
- `capsule_downstream_success`
- `transmission_bias_type`

## 5. Fay et al. (2019),
"Increasing population size can inhibit cumulative cultural evolution"

Why it matters:

- this is one of the most useful corrections for archive romanticism
- it shows that more available models can actually hurt cumulative improvement

What we should take from it:

- more access is not automatically more useful
- filtering burden matters
- population size and transmission opportunity interact in nontrivial ways

This is directly relevant to our future archive.

Without constraints, archive design will drift toward:

```text
large archive
-> many visible capsules
-> free access
```

But this literature suggests that overload and search burden can reduce
effective cumulative benefit.

Design implication:

- archive visibility should be bounded
- access should have time or energy cost
- archive filtering should be part of the mechanism, not just UI

Useful translation into biosphere terms:

- `archive_visibility_limit`
- `archive_filter_width`
- `archive_search_cost`
- `copy_time_budget`

## What This Means For Our Project

The literature suggests that our future inheritance design should be explicitly
multi-channel.

The most defensible interpretation for `alife_biosphere` is:

```text
vertical inheritance carries lineage continuity,
horizontal transfer increases adaptive reach,
ecological inheritance carries environmental memory,
and all three should remain bounded, lossy, and selectively structured.
```

That is much better than treating archive use as:

```text
free extra memory
```

or treating parent-to-child transfer as:

```text
the only inheritance route that matters
```

## Direct Design Consequences

## 1. We should log inheritance channels separately

At minimum, later runs should distinguish:

- parent-to-child vertical transfer
- peer or archive-mediated horizontal transfer
- habitat-mediated ecological inheritance

Suggested fields:

- `inheritance_mode`
- `vertical_transfer_size`
- `horizontal_transfer_size`
- `ecological_inheritance_score`

## 2. Archive access should have cost, bandwidth, and visibility constraints

This is one of the strongest practical implications.

We should not allow:

- unlimited visible capsules
- free instant copying
- no search burden
- permanent perfect memory

Suggested fields:

- `archive_access_fee`
- `archive_visibility_limit`
- `copy_time_budget`
- `copy_fidelity`

## 3. Recombination should be explicit

If archive and inheritance both matter, recombination will matter.

Organisms may later need to combine:

- parent-derived capsules
- archive-derived capsules
- recently consolidated lifetime experience

If recombination is real, it should be represented as a mechanism, not hidden
inside a generic update.

Suggested fields:

- `capsule_recombination_rate`
- `recombination_parent_count`
- `recombination_success`

Suggested event type:

```text
recombination_event
```

## 4. Forgetting and obsolescence should be first-class

The literature strongly suggests that useful cultural systems are not endless
accumulation machines.

We should allow:

- archive decay
- relevance loss
- cost of maintaining obsolete material
- forgetting under bandwidth pressure

Suggested fields:

- `archive_obsolescence_rate`
- `capsule_last_used_tick`
- `forgetting_pressure`

Suggested event types:

- `capsule_pruned`
- `capsule_obsolete`

## 5. Archive value should be measured by downstream effect, not only copying

We need to know whether a capsule actually helps.

That means measuring:

- post-transfer survival or adaptation
- ecological role occupancy after transfer
- persistence of transferred structure

not only:

- number of copies
- number of accesses

Suggested metrics:

- transfer benefit
- transfer burden
- archive overload rate
- capsule downstream success
- retention after transfer

## Proposed Additions To The Existing Design

### New fields

- `inheritance_mode`
- `archive_access_fee`
- `archive_visibility_limit`
- `copy_time_budget`
- `copy_fidelity`
- `capsule_recombination_rate`
- `archive_obsolescence_rate`
- `forgetting_pressure`

### New event types

- `vertical_inheritance_event`
- `horizontal_transfer_event`
- `recombination_event`
- `capsule_pruned`
- `capsule_obsolete`
- `archive_access_denied`

### New metrics

- vertical transfer benefit
- horizontal transfer benefit
- archive overload rate
- copy burden
- capsule retention rate
- downstream ecological benefit after transfer

## Proposed Probe Design

The first dual-inheritance probe should stay narrow.

A reasonable first probe is:

```text
same world
-> compare no archive, bounded archive, and free archive
-> compare vertical-only vs mixed transfer
-> compare with and without forgetting
-> measure adaptation, overload, and persistence
```

The first useful question is:

```text
Does bounded horizontal transfer improve lineage performance
without making archive use a free substitute for lived experience?
```

That is enough to validate the first archive layer.

## Build Recommendations

This literature review suggests three near-term build tasks.

### 1. Separate inheritance channels in the event schema

Reason:

- otherwise later analysis will collapse fundamentally different mechanisms into
  one reuse statistic

### 2. Design archive access around scarcity, not abundance

Reason:

- the literature does not support "bigger archive is better" as a default

### 3. Include forgetting from the first archive design

Reason:

- otherwise the archive will become a static omniscient store and distort the
  ecology

## Bottom Line

The dual-inheritance literature tells us that inheritance is not one thing.

For `alife_biosphere`, the right target is:

```text
a bounded inheritance ecology
where vertical, horizontal, and ecological channels coexist,
interact, conflict, and decay
```

That is much closer to the world we say we want than:

```text
parent memory plus a free global archive
```

## Sources

- Cavalli-Sforza, L. L., Feldman, M. W. (1978).
  "A dual inheritance model of the human evolutionary process I:
  Basic postulates and a simple model."
  [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0140175078800025)
- Feldman, M. W., Cavalli-Sforza, L. L. (1975).
  "Models for cultural inheritance: a general linear model."
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/16431675/)
- Henrich, J., McElreath, R. (2007).
  "Dual-Inheritance Theory: The Evolution of Human Cultural Capacities and
  Cultural Evolution."
  [Harvard PDF page](https://henrich.fas.harvard.edu/publications/dual-inheritance-theory-evolution-human-cultural-capacities-and-cultural)
- Henrich, J., Boyd, R., Richerson, P. J. (2008).
  "Five Misunderstandings About Cultural Evolution."
  [Harvard page](https://henrich.fas.harvard.edu/publications/five-misunderstandings-about-cultural-evolution)
- Fay, N., De Kleine, N., Walker, B., Caldwell, C. A. (2019).
  "Increasing population size can inhibit cumulative cultural evolution."
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6452720/)
