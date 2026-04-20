# Archive Visibility And Overload Thresholds Review v0

## Purpose

This note isolates one cultural-inheritance question that still lacked its own
design treatment:

```text
How much archive visibility is enough before social information becomes
counterproductive?
```

The project already has:

- archive trust,
- provenance,
- validation,
- forgetting,
- domain tags.

What was still missing is a threshold-oriented review for:

- visibility limits,
- search burden,
- copying opportunity,
- and overload dynamics.

## Short Answer

The literature supports a non-romantic view:

```text
More cultural availability is not automatically better.
Past a certain point, visibility, search burden, and copying opportunity can
reduce adaptive cultural performance.
```

For the biosphere, that means:

- archive visibility should be bounded by design;
- search cost should be explicit;
- copying opportunity and evaluation budget should be coupled;
- "richer archive" and "better culture" should never be treated as synonyms.

## 1. Population Size And Visibility Are Not Monotonic Goods

### [Fay et al. 2019, "Increasing population size can inhibit cumulative cultural evolution"](https://pmc.ncbi.nlm.nih.gov/articles/PMC6452720/)

Main result:

- larger populations did not necessarily improve cumulative culture;
- in their experiment, smaller populations showed stronger performance gains.

What we should take from it:

- more available exemplars can create interference rather than help;
- archive size and visibility cannot be assumed monotonic improvements.

Design implication:

- the archive should not expose everything to everyone;
- later probes should sweep visibility width explicitly.

### [Derex and Mesoudi 2020, "Cumulative Cultural Evolution within Evolving Population Structures"](https://www.sciencedirect.com/science/article/pii/S1364661320301078)

Main result:

- cumulative culture depends on population structure, not just population size;
- information flow is shaped by barriers, selective contact, and transmission
  opportunity.

What we should take from it:

- visibility is not only a count problem, it is a structure problem;
- archive channels should be treated as networked and filtered.

Design implication:

- archive access should later depend on:
  - habitat,
  - lineage proximity,
  - domain tags,
  - and source trust.

## 2. Search Burden Is Part Of The Mechanism

### [Roetzel 2019, "Information overload in the information age"](https://link.springer.com/article/10.1007/s40685-018-0069-z)

Main result:

- overload is not only about absolute information quantity;
- it emerges when available information outpaces filtering capacity and decision
  time.

What we should take from it:

- archive overload should be modeled as a ratio:
  available items / effective evaluation capacity.

Design implication:

- search burden should be explicit;
- if archive visibility rises, either copy time or evaluation budget should
  become binding.

### [Rendell et al. 2010, "Why Copy Others? Insights from the Social Learning Strategies Tournament"](https://pmc.ncbi.nlm.nih.gov/articles/PMC2989663/)

Main result:

- social learning can work well because it leverages population filtering,
  but only under specific opportunity structures.

What we should take from it:

- copying is useful when others have already done ecological filtering for you;
- if too many unfiltered candidates are visible, the advantage weakens.

Design implication:

- archive items should remain provenance-tagged and validation-sensitive;
- visibility should likely favor already-tested capsules over raw recent noise.

## 3. Copying Opportunity Should Be Coupled To Validation

### [Enquist et al. 2007, "Critical Social Learning: A Solution to Rogers's Paradox of Nonadaptive Culture"](https://www.researchgate.net/publication/227723473_Critical_Social_Learning_A_Solution_to_Rogers%27s_Paradox_of_Nonadaptive_Culture)

Main result:

- copying works when copied information is tested and rejected when it fails.

What we should take from it:

- visibility without validation is dangerous;
- copying should never be the terminal step.

Design implication:

- archive access should follow:

```text
see -> copy -> test -> retain/discard
```

### [Henrich et al. 2008, "Five Misunderstandings About Cultural Evolution"](https://docslib.org/doc/210579/five-misunderstandings-about-cultural-evolution)

Main result:

- transmission success is not the same as adaptive success;
- cultural spread can be biased for reasons other than ecological usefulness.

What we should take from it:

- archive popularity is not enough evidence that a capsule should stay visible.

Design implication:

- visibility rules should not be popularity-only;
- archive ranking should keep ecological validation in the loop.

## 4. The Biosphere Needs Visibility Thresholds, Not Unlimited Search

The literature points toward a very practical policy:

### Threshold variable family

- `archive_visibility_limit`
- `archive_search_cost`
- `copy_time_budget`
- `validation_budget`
- `visible_capsule_diversity`

### Recommended interpretation

- low visibility:
  underexposure, missed opportunities
- medium visibility:
  usable filtered access
- high visibility:
  overload, slower validation, weaker selection on cultural quality

This is not a hard universal curve, but it is the right experimental shape to
look for.

## 5. Recommended Probe Treatments

When archive systems arrive, the first threshold probe should compare:

```text
A. no archive
B. low visibility
C. medium visibility
D. high visibility
E. high visibility + increased search cost
F. high visibility + better provenance filtering
```

That lets us tell apart:

- pure visibility effects,
- overload effects,
- and mitigation through filtering.

## 6. Minimal Metrics

To study thresholds cleanly, log at least:

- `archive_visibility_limit`
- `visible_capsule_count`
- `archive_search_cost_paid`
- `copy_attempt_count`
- `validation_attempt_count`
- `retain_count`
- `discard_count`
- `archive_overload_rate`
- `archive_latency_to_useful_copy`
- `archive_domain_mismatch_rate`

## 7. Bottom Line

The strongest lesson is:

```text
Archive visibility should be treated as a scarce ecological opportunity,
not as a free convenience layer.
```

If we preserve that rule, the archive can become a real inheritance channel
instead of turning into a hidden answer key.
