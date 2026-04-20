# Dormancy, Seed Banks, Latency, And Temporal Persistence Review v0

## Purpose

This note targets one of the last major time-structure gaps in
`alife_biosphere`:

```text
How can a lineage remain present in the world
without remaining continuously active?
```

The goal is to connect:

- dormancy,
- diapause,
- seed banks,
- latent propagules,
- temporal dispersal,
- and temporal rescue

into one practical design story.

In practice, this note asks:

1. Why is dormancy more than inactivity?
2. How can latent stages buffer extinction and preserve diversity?
3. Why should time act like another dispersal axis?
4. What would it mean for the biosphere to have living temporal memory?

## Short Answer

The literature points to a strong combined picture:

```text
dormancy is a strategy for surviving bad times by delaying expression,
not merely pausing metabolism.
```

It also suggests:

```text
seed banks and dormant propagules act like temporal storage systems:
they preserve lineages, genotypes, and ecological options across time.
```

And importantly:

```text
temporal persistence can change population dynamics, coexistence,
local extinction risk, recolonization, and even the pace of evolution itself.
```

For our project, this means:

- dormancy should be a real life-history state, not a death substitute;
- the world should support latent but revivable lineage presence;
- temporal rescue should be distinguished from spatial rescue;
- and dormant stores should be treated as a powerful source of persistence,
  diversity, and delayed historical return.

## Core Papers

## 1. Cohen (1966), "Optimizing reproduction in a randomly varying environment"

Why it matters:

- this is the classic theoretical starting point for delayed germination and
  dormancy as bet hedging
- it remains one of the most important formal arguments in the whole area

The key lesson:

```text
when environments are unpredictably variable,
it can be optimal not to activate all propagules immediately.
```

This is a major design clue for `alife_biosphere`.

It means dormancy is not just what organisms do when they are damaged.
It can be a strategic allocation choice under uncertainty.

Design implication:

- propagule activation should later be partial and context-sensitive
- the world should support spreading risk across time

Useful translation into biosphere terms:

- `activation_fraction`
- `dormancy_bet_hedging_score`
- `temporal_risk_spread`

## 2. Cohen (1967), correlated information and delayed germination

Why it matters:

- this follow-up is useful because it adds information and cue structure
- it shows that dormancy decisions can depend on how informative current cues
  are about future conditions

The key lesson:

```text
dormancy strategy depends not only on risk,
but on how much present signals predict future payoff.
```

This is very relevant to the biosphere because it suggests dormant exit should
not be random by default.

Design implication:

- later dormancy exit should be cue-sensitive
- poor cue reliability may favor longer latency

Useful translation into biosphere terms:

- `cue_to_future_reliability`
- `dormancy_exit_threshold`
- `reactivation_signal_quality`

## 3. Templeton and Levin (1979), "Evolutionary consequences of seed pools"

Why it matters:

- this is one of the classic papers for seed pools as evolutionary structure
- it is especially useful because it focuses on how persistent pools alter
  population and genetic dynamics

The key lesson:

```text
seed or propagule pools do not only buffer demography.
they also reshape effective population structure and evolutionary timing.
```

This is extremely important for `alife_biosphere`.

It means dormant stores should not be treated as simple backup copies.
They change:

- which variants reappear,
- how fast lineages turn over,
- and how strongly present selection filters the future.

Design implication:

- dormant banks should later affect effective lineage persistence and temporal
  genetic structure

Useful translation into biosphere terms:

- `dormant_bank_load`
- `temporal_gene_flow`
- `effective_lineage_persistence`

## 4. Evans and Dennehy (2005), "Germ banking: bet-hedging and variable release from egg and seed dormancy"

Why it matters:

- this is probably the most useful broad review for the biosphere
- it unifies seed banks, delayed egg hatching, embryonic diapause, and related
  strategies under one frame

The key lesson:

```text
dormancy should be thought of as germ banking:
a temporal storage strategy with ecological, demographic, and evolutionary
consequences.
```

This is almost exactly the language the biosphere needs.

It suggests that dormant forms can:

- alter age structure,
- preserve diversity,
- transmit past genotypes forward,
- and buffer catastrophic bad periods.

Design implication:

- the biosphere should support a generalized latent propagule bank
- the bank should have age structure, decay, and exit rules

Useful translation into biosphere terms:

- `propagule_bank_size`
- `bank_age_distribution`
- `reactivation_rate`
- `latent_decay_rate`

## 5. Cáceres (1997), "Temporal variation, dormancy, and coexistence: A field test of the storage effect"

Why it matters:

- this is one of the clearest empirical demonstrations of dormancy supporting
  coexistence
- it gives a strong bridge from theory to ecological consequence

The key lesson:

```text
long-lived dormant stages can buffer competitors against exclusion when
recruitment fluctuates through time.
```

This is very relevant to `alife_biosphere`.

It means dormancy may support coexistence not only by helping one lineage
survive, but by preventing competitive exclusion under temporal fluctuation.

Design implication:

- dormant banks should later interact with coexistence metrics
- the world should distinguish active abundance from latent persistence

Useful translation into biosphere terms:

- `storage_effect_strength`
- `latent_coexistence_support`
- `active_vs_latent_abundance`

## 6. Hairston and Kearns (2002), "Temporal dispersal"

Why it matters:

- this is one of the clearest papers for the phrase "temporal dispersal"
- it makes dormant egg banks feel structurally comparable to spatial dispersal

The key lesson:

```text
dormancy is not only delayed activity;
it is dispersal across time.
```

This is an especially important conceptual upgrade for the biosphere.

It means habitat graphs alone are not enough.
The project may also need:

- temporal corridors,
- temporal rescue,
- and historically layered reactivation.

Design implication:

- the biosphere should later treat dormant banks as temporal connectivity
  structures
- lineage persistence should be measured across active and latent phases

Useful translation into biosphere terms:

- `temporal_dispersal_distance`
- `temporal_rescue_effect`
- `historical_reactivation_depth`

## 7. Hairston et al. (1999), "Rapid evolution revealed by dormant eggs"

Why it matters:

- this is one of the strongest empirical cases showing that dormant banks are
  not only demographic buffers
- they can preserve historical genotype snapshots and reveal evolutionary
  change over time

The key lesson:

```text
dormant propagules can store past evolutionary states and later reconnect them
to the present.
```

This is highly relevant to `alife_biosphere`.

It suggests that dormant banks may act as:

- temporal memory,
- evolutionary archive,
- and delayed competitor return.

Design implication:

- dormant stores should later preserve lineage states with age structure
- reactivation can reintroduce older strategies into newer worlds

Useful translation into biosphere terms:

- `historical_state_reactivation`
- `temporal_memory_depth`
- `old_lineage_return_risk`

## 8. Lennon and Jones (2011), "Microbial seed banks"

Why it matters:

- this is one of the best modern dormancy reviews, especially for broad
  ecological and evolutionary consequence
- it shows that dormancy is common, costly, and deeply consequential

The key lesson:

```text
microbial dormancy can maintain rare taxa, stabilize ecosystem functions,
and preserve diversity through difficult periods.
```

This is a very useful bridge because it moves dormancy out of plant-only
thinking.

Design implication:

- dormancy should be treated as phylogenetically and ecologically general
- latent banks should be able to preserve rare or low-abundance forms

Useful translation into biosphere terms:

- `rare_lineage_preservation`
- `latent_diversity_reserve`
- `ecosystem_stability_from_dormancy`

## What This Means For Our Project

The literature suggests that `alife_biosphere` should not treat persistence as:

- continuous active survival,
- or immediate replacement after loss.

The stronger temporal-ecology interpretation is:

```text
lineages can persist through time in active and latent forms,
and latent forms can preserve opportunity, diversity, and historical structure
across bad periods.
```

That means the biosphere should eventually distinguish at least:

### 1. Active organisms

- currently acting, sensing, reproducing

### 2. Dormant propagules

- alive in latent form
- not currently acting
- but still part of future population structure

### 3. Dead lineages

- no remaining active or latent continuity

This is much better than treating non-active forms as simple deletion.

## Direct Design Consequences

## 1. Dormancy should be a real state, not near-death

Later worlds should allow:

- reversible low-activity states
- reduced maintenance cost
- delayed activation
- nonzero survival costs and decay

Suggested fields:

- `dormancy_state`
- `latent_decay_rate`
- `maintenance_in_dormancy`
- `reactivation_threshold`

## 2. Propagule banks should be explicit

This is one of the strongest practical lessons.

Suggested fields:

- `propagule_bank_size`
- `bank_age_distribution`
- `activation_fraction`
- `reactivation_rate`

Suggested event types:

- `dormancy_entered`
- `propagule_bank_updated`
- `dormant_state_reactivated`
- `latent_lineage_lost`

## 3. Temporal rescue should be distinct from spatial rescue

Later worlds should distinguish:

- rescue by immigrants from another patch
- rescue by locally stored dormant forms

Suggested fields:

- `temporal_rescue_effect`
- `spatial_rescue_effect`
- `latent_reactivation_contribution`

## 4. Dormancy should affect diversity and turnover metrics

Following Cáceres and Lennon/Jones:

- diversity should be measured for:
  - active pool
  - latent pool
  - combined pool

Suggested metrics:

- active diversity
- latent diversity
- combined temporal diversity
- coexistence stabilized by dormancy

## 5. Historical return should be allowed but costly

Following Hairston:

- older propagules reappearing can reconnect past and present
- this should not be free or riskless

Suggested fields:

- `historical_state_reactivation`
- `reactivation_age_penalty`
- `old_lineage_return_risk`

## Proposed Additions To The Existing Design

### New fields

- `dormancy_state`
- `propagule_bank_size`
- `bank_age_distribution`
- `activation_fraction`
- `latent_decay_rate`
- `temporal_rescue_effect`
- `historical_state_reactivation`
- `latent_diversity_reserve`

### New event types

- `dormancy_entered`
- `propagule_bank_updated`
- `dormant_state_reactivated`
- `latent_lineage_lost`
- `temporal_rescue_triggered`
- `historical_variant_returned`

### New metrics

- dormant-bank persistence
- temporal rescue frequency
- latent diversity reserve
- active-vs-latent occupancy
- reactivation lag
- coexistence supported by dormancy

## Proposed Probe Design

The first dormancy-focused probe can stay focused.

A reasonable first probe is:

```text
same lineage base
-> compare no dormancy, shallow dormancy, and age-structured propagule banking
-> introduce temporal bad periods and patch-level local extinction
-> measure persistence, reactivation, diversity, and rescue
```

The first useful question is:

```text
Does temporal storage allow lineages to survive fluctuation and recover later in
ways that neither continuous activity nor spatial recolonization alone can
provide?
```

That is enough to justify a full temporal-persistence layer.

## Build Recommendations

This literature review suggests three near-term design tasks.

### 1. Add a dormancy/propagule-bank section to the core design

Reason:

- persistence across bad periods is too important to remain implicit

### 2. Treat latent forms as part of population structure

Reason:

- dormant forms can shape both ecology and evolution even while inactive

### 3. Distinguish temporal rescue from spatial rescue

Reason:

- they are related but not interchangeable persistence mechanisms

## Bottom Line

The dormancy literature tells us that living systems can persist not only by
staying active, but by staying available.

For `alife_biosphere`, the stronger target is:

```text
a world where lineages can survive across time in latent form,
return after bad periods,
and use temporal storage as both an ecological buffer and an evolutionary
memory
```

That is the version of dormancy worth building toward.

## Sources

- Cohen, D. (1966).
  "Optimizing reproduction in a randomly varying environment."
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/6015423/)
  and [ScienceDirect](https://www.sciencedirect.com/science/article/pii/0022519366901883)
- Cohen, D. (1967).
  "Optimizing reproduction in a randomly varying environment when a correlation may exist between the conditions at the time a choice has to be made and the subsequent outcome."
  [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/0022519367900501)
- Templeton, A. R., Levin, D. A. (1979).
  "Evolutionary consequences of seed pools."
  [DOI referenced via seed-bank literature](https://doi.org/10.1086/283471)
- Evans, M. E. K., Dennehy, J. J. (2005).
  "Germ banking: bet-hedging and variable release from egg and seed dormancy."
  [University of Arizona page](https://experts.arizona.edu/en/publications/germ-banking-bet-hedging-and-variable-release-from-egg-and-seed-d/)
- Cáceres, C. E. (1997).
  "Temporal variation, dormancy, and coexistence: A field test of the storage effect."
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC23092/)
- Hairston, N. G. Jr., Kearns, C. M. (2002).
  "Temporal dispersal: ecological and evolutionary aspects of zooplankton egg banks and the role of sediment mixing."
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/21708742/)
- Hairston, N. G. Jr. et al. (1999).
  "Rapid evolution revealed by dormant eggs."
  [Nature](https://www.nature.com/articles/46731)
- Lennon, J. T., Jones, S. E. (2011).
  "Microbial seed banks: the ecological and evolutionary implications of dormancy."
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/21233850/)
  and [author PDF](https://lennonlab.github.io/assets/publications/Lennon_Jones_2011.pdf)
