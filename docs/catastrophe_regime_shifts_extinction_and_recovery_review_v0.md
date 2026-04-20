# Catastrophe, Regime Shifts, Extinction, And Recovery Review v0

## Purpose

This note extends the literature program toward one of the most "historical"
questions for `alife_biosphere`:

```text
What happens when the world does not merely fluctuate,
but undergoes a real ecological or evolutionary break?
```

The goal is to move beyond ordinary disturbance and ask how the biosphere should
represent:

- catastrophic transitions,
- extinction selectivity,
- survival without real recovery,
- and long recovery phases that reshape who matters in the world.

In practice, this note asks:

1. When is a collapse more than a bad local shock?
2. Why is extinction rarely random?
3. Why do some survivors fail to re-expand after surviving?
4. Why is recovery usually a staged rebuilding process rather than a simple
   bounce-back?

## Short Answer

The literature points to a clear and very useful view:

```text
catastrophes do not just remove organisms.
they reorder opportunity, reset ecological structure unevenly,
and often create a long interval where survival, persistence,
and recovery come apart.
```

For our project, that means:

- extinction should not be treated as an undifferentiated loss count;
- some lineages should survive yet still fail to matter later;
- recovery should be staged and selective;
- system history should include real intervals of ecological simplification and
  rebuilding.

## Core Papers

## 1. Scheffer et al. (2001), "Catastrophic shifts in ecosystems"

Why it matters:

- this is still one of the best general sources for abrupt regime shifts
- it helps distinguish gradual pressure from threshold-driven reorganization

The key lesson:

```text
systems can absorb pressure for a long time and then reorganize abruptly once a
critical threshold is crossed
```

This matters because it tells us not to model all large changes as smooth.

For `alife_biosphere`, it suggests:

- some changes should be threshold-like;
- the same world may look stable until a regime boundary is crossed;
- pre-collapse diagnostics matter.

Design implication:

- regime shifts should be representable separately from ordinary disturbances
- some habitat or world variables should allow threshold behavior

Useful translation into biosphere terms:

- `regime_shift_threshold`
- `state_shift_event`
- `pre_collapse_instability`

## 2. Barnosky et al. (2012), "Approaching a state shift in Earth's biosphere"

Why it matters:

- this paper scales the state-shift idea up to the biosphere level
- it is useful for thinking about whole-world transitions rather than only local
  habitat changes

The key lesson:

```text
distributed ecological systems can approach a large-scale transition when
multiple pressures accumulate across the whole biosphere
```

This is important to us because our project is explicitly trying to build not
just habitats, but a world with history.

Design implication:

- the biosphere should support multi-habitat stress accumulation
- world-scale regime diagnostics may later matter in addition to local metrics

Useful translation into biosphere terms:

- `global_transition_pressure`
- `world_state_shift_risk`
- `multi_patch_synchrony`

## 3. McKinney (1997), "Extinction Vulnerability and Selectivity"

Why it matters:

- this is a strong general review for one of the most important cautions:
  extinction is rarely random
- it bridges ecological and paleontological thinking in a way that fits our
  project well

The key lesson:

```text
the traits that make lineages vulnerable or resilient are structured,
and those structures shape what kind of world remains after collapse
```

For `alife_biosphere`, this means:

- a catastrophe should not affect all lineages equally;
- vulnerability should depend on traits, roles, and position in the world;
- extinctions can homogenize the system if selective pressure repeatedly removes
  the same kinds of forms.

Design implication:

- extinction selectivity should be logged and analyzable
- lineages should differ in vulnerability by ecology, role, or dependence

Useful translation into biosphere terms:

- `extinction_vulnerability`
- `selective_loss_pattern`
- `post_extinction_homogenization`

## 4. Jablonski (2001), "Lessons from the past: evolutionary impacts of mass extinctions"

Why it matters:

- this paper makes the strongest general case that mass extinctions do more than
  intensify ordinary turnover
- it emphasizes selectivity, disruption, and redirected diversification

The key lesson:

```text
major extinctions do not merely shrink the old world.
they redirect which trajectories remain available.
```

This is highly relevant to our project because we care not only about survival,
but about what kinds of futures become easier or harder after crisis.

Design implication:

- post-extinction opportunity structure should be part of recovery design
- recovery should be allowed to produce unexpected new dominant lineages

Useful translation into biosphere terms:

- `post_extinction_opportunity_shift`
- `recovery_trajectory_divergence`
- `new_dominant_role_emergence`

## 5. Erwin (2001), "Lessons from the past: biotic recoveries from mass extinctions"

Why it matters:

- this is one of the most important recovery papers for our purposes
- it directly argues that recovery is more complicated than "empty niches refill"

The key lesson:

```text
recovery is often delayed, stepwise, and structurally constrained.
ecospace may need to be rebuilt, not just repopulated.
```

This is a major design clue for `alife_biosphere`.

It suggests that after catastrophe:

- simple occupancy return is not enough;
- ecological structure may stay impoverished for long intervals;
- different parts of the system recover at different rates.

Design implication:

- recovery should be multi-phase:
  - survival interval
  - early reoccupation
  - ecospace rebuilding
  - later diversification

Useful translation into biosphere terms:

- `survival_interval`
- `recovery_phase`
- `ecospace_rebuild_score`
- `stagewise_recovery`

## 6. Jablonski (2002), "Survival without recovery after mass extinctions"

Why it matters:

- this paper gives one of the most useful cautionary concepts for our project:
  "dead clade walking"
- it distinguishes surviving the event from participating in the future

The key lesson:

```text
a lineage can survive a catastrophe yet fail to recover, diversify, or remain
important afterward
```

This is extremely relevant for us because otherwise we may over-credit mere
survival.

Design implication:

- later analyses should distinguish:
  - event survival
  - post-event persistence
  - post-event reexpansion
  - post-event innovation

Useful translation into biosphere terms:

- `dead_clade_walking_flag`
- `survival_without_recovery`
- `post_event_reexpansion_failure`

## 7. Chen and Benton (2012),
"The timing and pattern of biotic recovery following the end-Permian mass extinction"

Why it matters:

- this paper is especially useful for the stepwise rebuilding idea
- it argues that ecosystem recovery can proceed from low to high trophic levels
  across long timescales

The key lesson:

```text
recovery can be trophically staged,
with simple or opportunistic forms returning before more complex ecological
structure reappears
```

This matters to us because we already plan:

- trophic asymmetry
- ecosystem engineering
- group structure

It suggests these may return in order, not all at once, after catastrophe.

Design implication:

- recovery metrics should distinguish:
  - occupancy recovery
  - trophic recovery
  - functional recovery

Useful translation into biosphere terms:

- `trophic_recovery_stage`
- `functional_recovery_score`
- `complexity_return_lag`

## 8. Sahney and Benton (2008), "Recovery from the most profound mass extinction of all time"

Why it matters:

- this gives a more explicit picture of post-extinction ecological rebuilding
- it is especially useful for thinking about cosmopolitan opportunists and
  subsequent restructuring

What we should take from it:

- early recovery can be dominated by widespread disaster forms
- fast taxonomic return can coexist with ecologically shallow recovery

This is a direct warning against superficial metrics.

Design implication:

- we should distinguish:
  - taxonomic recovery
  - ecological recovery
  - structural recovery

Suggested fields:

- `disaster_taxon_role`
- `ecological_shallowness_score`
- `cosmopolitan_opportunist_load`

## What This Means For Our Project

The literature suggests that `alife_biosphere` should not treat catastrophe as:

- one bad timestep
- one drop in population
- one temporary stress multiplier

The stronger historical interpretation is:

```text
catastrophe can simplify the world,
reshape selectivity,
create survivors that never truly return,
and force a slow rebuilding of ecological organization
```

That is much more useful if we want the world to have real history.

## Direct Design Consequences

## 1. Extinction should be selective, not uniform

Later catastrophe logic should allow vulnerability to depend on:

- trophic role
- habitat dependence
- developmental strategy
- memory or archive dependence
- group dependence

Suggested fields:

- `extinction_vulnerability`
- `catastrophe_sensitivity_profile`
- `resilience_class`

## 2. Survival and recovery must be split analytically

This is one of the strongest practical lessons.

Suggested metrics:

- event survival rate
- post-event persistence
- reexpansion success
- post-event innovation rate

Suggested event types:

- `catastrophe_survived`
- `recovery_failed`
- `reexpansion_started`
- `dead_clade_walking_detected`

## 3. Recovery should be staged

Following Erwin and Chen/Benton, later biosphere histories should distinguish:

- survival interval
- opportunist interval
- structural rebuild interval
- mature recovery interval

Suggested fields:

- `recovery_stage`
- `survival_interval_length`
- `functional_rebuild_progress`

## 4. Catastrophes should alter opportunity structure

Following Jablonski, catastrophe should not just subtract lineages.

It should also change:

- who can dominate later
- what roles are open
- what constraints remain

Suggested fields:

- `open_role_count_after_collapse`
- `post_event_role_vacancy`
- `trajectory_reset_score`

## 5. Whole-world transitions should be possible, but rare

Following Barnosky and regime-shift work:

- local collapse is common enough
- world-scale transition should be harder, but possible

Suggested fields:

- `global_transition_pressure`
- `biosphere_regime_state`
- `synchronized_patch_failure`

## Proposed Additions To The Existing Design

### New fields

- `extinction_vulnerability`
- `catastrophe_sensitivity_profile`
- `survival_interval_length`
- `recovery_stage`
- `dead_clade_walking_flag`
- `global_transition_pressure`
- `trajectory_reset_score`

### New event types

- `catastrophe_event`
- `state_shift_event`
- `catastrophe_survived`
- `dead_clade_walking_detected`
- `recovery_failed`
- `functional_recovery_advanced`

### New metrics

- event survival rate
- post-event reexpansion success
- dead-clade-walking frequency
- functional recovery lag
- trophic recovery lag
- post-extinction homogenization
- world transition severity

## Proposed Probe Design

The first catastrophe-focused probe can stay relatively small.

A reasonable first probe is:

```text
established multi-habitat world
-> introduce selective catastrophe with different sensitivity profiles
-> measure immediate survival
-> track survival interval, opportunist phase, and later rebuilding
-> compare lineages that survive but fail to re-expand against those that
   become dominant in recovery
```

The first useful question is:

```text
Does the world display staged recovery and selective long-run restructuring,
or does it simply bounce back numerically?
```

That is enough to justify catastrophe-aware history.

## Build Recommendations

This literature review suggests three near-term design tasks.

### 1. Add catastrophe as a world-history mechanism, not only a stressor

Reason:

- large historical transitions should be distinguishable from ordinary shocks

### 2. Separate event survival from recovery success

Reason:

- otherwise we will overestimate the historical importance of mere survivors

### 3. Track functional rebuilding, not only population rebound

Reason:

- ecological recovery often lags far behind numerical return

## Bottom Line

The catastrophe literature tells us that a world becomes historically serious
when collapse changes more than numbers.

For `alife_biosphere`, the stronger target is:

```text
a world where catastrophes reshape selectivity,
create survival without recovery,
open new roles,
and force stepwise rebuilding of ecological structure
```

That is the version of catastrophe worth building.

## Sources

- Scheffer, M., Carpenter, S., Foley, J. A., Folke, C., Walker, B. (2001).
  "Catastrophic Shifts in Ecosystems."
  [Nature](https://www.nature.com/articles/35098000)
- Barnosky, A. D. et al. (2012).
  "Approaching a state shift in Earth's biosphere."
  [Nature](https://www.nature.com/articles/nature11018)
  and [PubMed](https://pubmed.ncbi.nlm.nih.gov/22678279/)
- McKinney, M. L. (1997).
  "Extinction Vulnerability and Selectivity: Combining Ecological and
  Paleontological Views."
  [Annual Reviews](https://www.annualreviews.org/doi/10.1146/annurev.ecolsys.28.1.495)
- Jablonski, D. (2001).
  "Lessons from the past: evolutionary impacts of mass extinctions."
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/11344284/)
- Erwin, D. H. (2001).
  "Lessons from the past: biotic recoveries from mass extinctions."
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC33225/)
- Jablonski, D. (2002).
  "Survival without recovery after mass extinctions."
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC123034/)
- Chen, Z.-Q., Benton, M. J. (2012).
  "The timing and pattern of biotic recovery following the end-Permian mass
  extinction."
  [Nature Geoscience](https://www.nature.com/articles/ngeo1475)
- Sahney, S., Benton, M. J. (2008).
  "Recovery from the most profound mass extinction of all time."
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2596898/)
