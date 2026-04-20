# Disagreement And Caution Register v1

## Purpose

This note collects the main disagreements, caution points, and unstable
interpretations that recur across the `alife_biosphere` library.

It does not try to settle every debate.
It exists to stop the project from quietly acting as if all important questions
have already been resolved.

The register focuses on disagreements that materially affect:

- how we describe results
- which mechanisms we prioritize
- which metrics we trust
- which claims we should avoid making too early

## 1. How To Read This Register

Each item has four parts:

- the point of disagreement or caution
- why it matters to this project
- the current working lean
- what would move the question forward

`current working lean` is not a final truth.
It is the best current interpretation of the library as a whole.

## 2. Core Disagreements And Cautions

## D1. Diversity Is Not The Same As Open-Endedness

Disagreement / caution:

- ongoing novelty, large variation, or long runtime do not automatically imply
  open-ended evolution

Why it matters:

- this project will likely generate visually rich traces before it generates
  anything that deserves stronger evolutionary claims

Current working lean:

- treat diversity, novelty, persistence, and structural innovation as separate
  axes
- do not collapse them into one open-endedness score

What would move this forward:

- long-run evidence that new organizational modes keep appearing rather than
  only recycled variation

## D2. Stability Is Not The Same As Resilience

Disagreement / caution:

- a smooth system is not necessarily resilient
- a fluctuating system is not necessarily failing

Why it matters:

- if we optimize for visual smoothness, we may erase the very disturbance and
  recovery structure the project needs

Current working lean:

- distinguish:
  - stability
  - resilience
  - adaptability
  - transformability

What would move this forward:

- repeated disturbance probes showing which structures preserve recoverability
  rather than mere constancy

## D3. Founder Events Matter, But Bottlenecks Alone Are Not Enough

Disagreement / caution:

- small colonizing groups can matter
- but bottlenecks alone do not justify strong lineage-innovation stories

Why it matters:

- migration events in the biosphere will be easy to overinterpret

Current working lean:

- founder events become interesting only when:
  - habitat context changes
  - selection changes after entry
  - descendant lineage persists or differentiates

What would move this forward:

- controls comparing same-habitat recolonization, novel-habitat colonization,
  and different bottleneck widths

## D4. Group Formation Is Not The Same As Higher-Level Individuality

Disagreement / caution:

- co-location, cooperation, and group persistence are all weaker than
  higher-level individuality

Why it matters:

- this is one of the easiest places for artificial-life projects to overclaim

Current working lean:

- use the weakest defensible claim
- group-level individuality requires much stronger evidence than stable group
  presence

What would move this forward:

- evidence of group reproduction, fitness decoupling, and breakdown resistance

## D5. Communication Does Not Become Honest Just Because It Is Costly

Disagreement / caution:

- stable signaling can be honest or deceptive
- message cost alone is not a sufficient explanation of honesty

Why it matters:

- the project could easily implement a shallow "energy fee" model and assume
  the signaling problem is solved

Current working lean:

- trust, verification, repeated interaction, and trade-offs matter more than
  message cost alone

What would move this forward:

- probes comparing:
  - signal cost only
  - repeated-interaction trust
  - verification-sensitive signaling

## D6. Archive Size Is Not Monotonic With Archive Quality

Disagreement / caution:

- more available cultural material is not automatically better
- popularity is not the same as adaptive value

Why it matters:

- a naive archive will drift toward infinite visibility and prestige loops

Current working lean:

- archive access should stay bounded, validated, and domain-sensitive

What would move this forward:

- archive visibility ablations under changing habitats and misleading sources

## D7. Direct Trust And Source Trust Should Not Be Collapsed

Disagreement / caution:

- direct interaction evidence and archive/source evidence do not support the
  same kind of trust update

Why it matters:

- collapsing them into one reputation score would erase an important social
  asymmetry in the project

Current working lean:

- keep:
  - direct partner trust
  - archive/source trust
  as distinct channels

What would move this forward:

- side-by-side comparison of split-channel trust against a single trust score

## D8. Adaptive Cycles Are Useful, But Hard Phase Labels Are Premature

Disagreement / caution:

- adaptive-cycle thinking is useful
- but the idealized four-phase picture should not be forced too early onto a
  small evolving world

Why it matters:

- premature phase labels can turn suggestive patterns into false certainty

Current working lean:

- use proxy profiles first
- defer strong phase classification

What would move this forward:

- repeated long-run trajectories where the same proxy bundles recur in stable
  patterns

## D9. Warning Signals Are Valuable, But Fragile

Disagreement / caution:

- early-warning metrics can be informative
- but they are noisy, model-sensitive, and vulnerable to false positives and
  misses

Why it matters:

- the project could easily turn warning diagnostics into overconfident regime
  detectors

Current working lean:

- treat warning outputs as typed, uncertain candidates rather than truth labels

What would move this forward:

- retrospective scoring of warning candidates against realized outcomes across
  many runs

## D10. Connectedness Is Not One Scalar

Disagreement / caution:

- edge count, density, modularity, and redundancy do not mean the same thing

Why it matters:

- rescue flow, parasite spread, and local diversity can respond very
  differently to different network summaries

Current working lean:

- connectedness should remain a profile of cheap summaries, not one number

What would move this forward:

- experiments showing which connectedness proxies best align with failure and
  recovery behavior

## D11. Antagonists Are Not Just Noise

Disagreement / caution:

- parasites and exploiters can destroy structure
- but they can also be engines of complexity and evolvability

Why it matters:

- it would be easy to remove antagonism too early as a nuisance

Current working lean:

- antagonists should stay in scope as mechanism candidates, not only failure
  cases

What would move this forward:

- comparisons of worlds with and without antagonistic pressure under matched
  ecological conditions

## D12. Partial Observability Is Not An Optional Difficulty Setting

Disagreement / caution:

- many interpretations become unrealistic if organisms get full world state

Why it matters:

- signaling, trust, archive use, and rescue all change qualitatively under
  partial observability

Current working lean:

- partial observability should be treated as normal background structure

What would move this forward:

- explicit comparison between local-observation and omniscient baselines

## 3. Most Important Current Caution

Across the whole library, the strongest repeated caution is:

```text
do not overclaim from vivid behavior, short runs, or one metric family
```

This is the most consistent warning across:

- higher-level individuality
- open-endedness
- signaling
- warning metrics
- founder effects
- archive use

## 4. What This Register Does Not Yet Solve

This file still does not provide:

- a full contradiction map for every topic
- a confidence score for every project assumption
- claim-to-evidence accounting for actual run results

Those remain separate coordination tasks.

