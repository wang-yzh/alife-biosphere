# Minimal Metric Bundle For M1 And M2

## Purpose

This note turns the broader measurement literature into a practical rule:

```text
What absolutely must be logged and summarized during M1 and M2,
before more advanced inheritance or archive systems arrive?
```

This is a design document, not an implementation checklist only.
Its role is to stop a common failure mode:

```text
the world runs,
interesting things seem to happen,
but the event and metric layer is too weak to tell what actually changed
```

## Why This Matters

The existing literature already gives us the warning:

- [Bedau, Snyder, and Packard 1998](https://cseweb.ucsd.edu/~rik/alife6/papers/KI40.html) shows that diversity alone is not enough to characterize long-run evolutionary dynamics.
- [Dolson et al. 2019, MODES](https://direct.mit.edu/artl/article/25/1/50/2915/The-MODES-Toolbox-Measurements-of-Open-Ended) argues for multiple measurement families rather than one open-endedness score.
- [Taylor et al. 2016](https://pubmed.ncbi.nlm.nih.gov/27472417/) emphasizes plural hallmarks of open-ended evolution.
- [Holling 1973](https://doi.org/10.1146/annurev.es.04.110173.000245) distinguishes resilience from simple stability.
- [Scheffer et al. 2009](https://www.nature.com/articles/nature08227) and [Boettiger and Hastings 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3427498/) warn that warning signals are fragile and should not be treated as magical detectors.
- [West et al. 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4547252/) and [Shelton and Michod 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7133510/) make it clear that higher-level individuality needs group-specific metrics, not only organism success.

The practical implication is:

```text
M1 and M2 need a metric bundle that is deliberately richer than one scoreboard,
but still small enough to compute cheaply and inspect routinely.
```

## Design Rule

For M1 and M2, the metric bundle should satisfy four constraints:

1. cheap enough to compute on every probe run
2. derivable from append-only logs and bounded snapshots
3. meaningful before archive, parasite, and full group reproduction exist
4. extensible later without changing old event semantics

## The Five Required Metric Families

### 1. Population State

Purpose:

- detect collapse, crowding, and occupancy redistribution

Required M1 metrics:

- `alive_count`
- `dead_count`
- `alive_fraction`
- `occupancy_by_habitat`
- `occupancy_pressure_by_habitat`
- `movement_count`

Why these matter:

- they are the minimum needed to tell whether the graph topology and refuge
  structure are doing real work;
- they support the earliest resilience and assembly analysis.

Key literature:

- [Holling 1973](https://doi.org/10.1146/annurev.es.04.110173.000245)
- [Hraber and Milne 1997](https://www.sciencedirect.com/science/article/pii/S0304380097001117)

### 2. Lineage And Founder History

Purpose:

- make later inheritance claims possible

Required M1 metrics:

- `founder_count_by_habitat`
- `colonization_event_count`
- `founder_group_size`
- `lineage_presence_by_habitat`
- `lineage_turnover_rate`
- `lineage_survival_time`

Required M2 additions:

- `birth_count_by_lineage`
- `ancestor_depth`
- `founder_bottleneck_count`
- `post_colonization_adaptation_lag`

Why these matter:

- without them, migration is just motion;
- they are the minimum basis for founder-effect, rescue, and inheritance
  analyses.

Key literature:

- [Templeton 1980] (already discussed in founder review)
- [Maliet, Shelton, and Michod 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4528466/)
- [Black, Bourrat, and Rainey 2020](https://www.nature.com/articles/s41559-019-1086-9)

### 3. Lifecycle And Reproductive Readiness

Purpose:

- separate survival from readiness from actual reproduction

Required M1 metrics:

- `juvenile_count`
- `mature_count`
- `senescent_count`
- `reproduction_ready_count`
- `time_to_reproduction_ready`
- `death_reason_counts`

Required M2 additions:

- `birth_count`
- `offspring_survival_rate`
- `readiness_to_birth_lag`
- `maturation_rate`

Why these matter:

- M1 is not yet about full reproduction, but it must still tell us who becomes
  reproduction-eligible and under what ecological conditions;
- this is the bridge from simple survival ecology to heredity.

Key literature:

- [Libby and Rainey 2013](https://pubmed.ncbi.nlm.nih.gov/23735467/)
- [West et al. 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4547252/)

### 4. Disturbance, Recovery, And Refuge Use

Purpose:

- distinguish stability from resilience

Required M1 metrics:

- `disturbance_event_count`
- `disturbance_by_habitat`
- `post_shock_alive_fraction`
- `refuge_occupancy`
- `recovery_lag`
- `habitat_reoccupation_time`

Required M2 additions:

- `lineage_rebound_rate`
- `rescue_source_count`
- `post_shock_diversity_delta`
- `warning_signal_confidence`

Why these matter:

- we want a world that can reorganize without becoming either frozen or dead;
- these metrics let us tell "smooth" apart from "resilient."

Key literature:

- [Holling 1973](https://doi.org/10.1146/annurev.es.04.110173.000245)
- [Scheffer et al. 2009](https://www.nature.com/articles/nature08227)
- [Clements et al. 2019](https://www.nature.com/articles/s41467-019-09684-y)
- [Orr and Unckless 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4133041/)

### 5. Structural Change Proxies

Purpose:

- capture early open-endedness signals without overclaiming

Required M1 metrics:

- `new_habitat_role_occupations`
- `interaction_edge_count`
- `interaction_type_counts`
- `novel_movement_patterns`

Required M2 additions:

- `new_lineage_behavior_clusters`
- `role_differentiation_index`
- `group_persistence`
- `developmental_state_diversity`

Why these matter:

- they are the smallest bridge from ecology metrics to later open-endedness
  analysis;
- they let us detect "something structurally new happened" before archive and
  full group reproduction exist.

Key literature:

- [Bedau, Snyder, and Packard 1998](https://cseweb.ucsd.edu/~rik/alife6/papers/KI40.html)
- [Dolson et al. 2019](https://direct.mit.edu/artl/article/25/1/50/2915/The-MODES-Toolbox-Measurements-of-Open-Ended)
- [Taylor et al. 2016](https://pubmed.ncbi.nlm.nih.gov/27472417/)

## Event Requirements For This Metric Bundle

To compute the bundle above, M1 and M2 must log at least:

- `birth`
- `death`
- `move`
- `move_blocked`
- `harvest`
- `hazard_damage`
- `crowding_damage`
- `reproduction_ready`
- `reproduction_unready`
- `disturbance`
- `tick_summary`

And by M2:

- `maturation`
- `colonization_event`
- `group_join`
- `group_leave`
- `offspring_birth`

The core rule is simple:

```text
If a phenomenon matters enough to be discussed in the paper,
it should matter enough to have its own event or an unambiguous derivation path.
```

## What Should Stay Out Of The M1/M2 Bundle

Do not add these yet:

- full MODES complexity stack
- archive-specific cultural metrics
- parasite virulence metrics
- semantic-closure metrics
- full higher-level individuality metrics

Reason:

- they require mechanisms that do not yet exist;
- adding them too early creates noise and fake precision.

## Minimum Probe Tables

Every M1 or M2 probe should at minimum emit:

### `population_summary.csv`

- alive / dead counts
- occupancy by habitat
- movement counts
- readiness counts

### `lineage_summary.csv`

- lineage presence by habitat
- founder and colonization counts
- survival time

### `disturbance_summary.csv`

- disturbance counts
- refuge occupancy
- recovery lag

### `structure_summary.csv`

- interaction edge counts
- new occupation patterns
- simple novelty proxies

## Claim Discipline

This bundle supports a conservative claim ladder.

### With M1 only

Allowed claims:

- bounded non-collapse
- meaningful habitat differentiation
- refuge use and recovery structure
- nontrivial colonization dynamics

Not allowed:

- inheritance benefit
- cultural accumulation
- higher-level individuality
- open-ended evolution

### With M2

Allowed claims:

- reproduction-ready ecology
- first lineage accumulation effects
- early structural diversification

Still not allowed:

- strong open-endedness claims
- strong group-level selection claims
- cultural open-endedness claims

## Bottom Line

The right metric bundle for M1 and M2 is not large.
But it must be deliberate.

If we log the five families above from the beginning, then later inheritance,
archive, and group-level work will have a trustworthy baseline instead of a
story reconstructed after the fact.
