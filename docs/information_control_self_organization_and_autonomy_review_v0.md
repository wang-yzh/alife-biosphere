# Information, Control, Self-Organization, And Autonomy Review v0

## Purpose

This note extends the literature program toward a very deep question for
`alife_biosphere`:

```text
What would make the biosphere feel less like a simulator being pushed from the
outside, and more like a system that is in some sense organizing and preserving
itself from within?
```

The goal is not to force one grand theory onto the project.
The goal is to collect a set of ideas that clarify:

- control from the organism's point of view,
- self-maintaining organization,
- internal versus external regulation,
- and the boundary between a system and its environment.

In practice, this note asks:

1. What is autonomy in a life-like system?
2. Why is control not the same as reward optimization?
3. Why does self-organization matter beyond mere complexity?
4. What should we take, carefully, from information-theoretic and free-energy
   approaches?

## Short Answer

The literature suggests a layered answer:

```text
an autonomous system is not just one that moves.
it is one that helps maintain the conditions of its own continued existence.
```

A system starts to look more life-like when:

- it has internal organization that matters for staying alive;
- it has some control over its own future sensorimotor possibilities;
- it maintains a nontrivial boundary between itself and the environment;
- and its behavior cannot be understood only as externally scripted task
  pursuit.

For our project, this means:

- survival and self-maintenance should remain central;
- internal control should be measured, not only success on external tasks;
- habitat interaction should preserve a system/environment distinction;
- self-organization should be treated as an empirical question, not a poetic
  label.

## Core Papers

## 1. Maturana and Varela (1980), "Autopoiesis and Cognition"

Why it matters:

- this is the classical source for autopoiesis
- it pushes the strongest version of the idea that living systems are
  self-producing and operationally closed

The key lesson we should reuse:

```text
a living system is not just a thing located somewhere.
it is an organization that continually produces and maintains itself.
```

This matters for `alife_biosphere` because it pushes us past the default agent
template:

```text
fixed entity
+ environment observations
+ action selection
```

and toward a stronger question:

```text
what part of the system is actively preserving the conditions under which the
organism remains itself?
```

We should not over-import autopoiesis literally.
But it gives us a valuable design direction:

- internal maintenance should matter
- organisms should not be reducible to task performers
- identity should depend on self-preserving organization

Design implication:

- integrity, maintenance, repair, and self-producing processes should matter
- some event types should describe preservation, not just action

Useful translation into biosphere terms:

- `self_maintenance_load`
- `repair_success`
- `identity_persistence`
- `organizational_failure`

## 2. Moreno and Mossio autonomy line

Why it matters:

- this line of work modernizes and sharpens autonomy beyond simple autopoiesis
- it emphasizes closure of constraints and organizational dependence

The key lesson:

```text
autonomy is not isolation.
it is a pattern where internal processes depend on one another in a way that
helps sustain the whole system.
```

This is highly useful for us because our project already thinks in terms of:

- energy
- matter
- integrity
- information
- development
- inheritance

Autonomy suggests that these should not be independent meters only.
They should participate in coupled sustaining structure.

Design implication:

- world design should eventually track whether internal processes support or
  undermine system continuation
- autonomy should be treated as organizational, not merely spatial

Useful translation into biosphere terms:

- `closure_score`
- `internal_dependency_index`
- `maintenance_coupling_strength`

## 3. Klyubin, Polani, Nehaniv (2005), "Empowerment"

Why it matters:

- this is one of the cleanest information-theoretic ideas that is directly
  useful to artificial-life systems
- it gives an agent-centered measure of how much influence an organism has over
  future perceivable states

The key lesson:

```text
control can be measured by the number and distinctness of future sensorimotor
states an agent can bring about and perceive.
```

This is extremely relevant to our project.

It suggests a way to think about control that is not:

- task reward
- hand-designed objective
- one-off benchmark success

Instead, empowerment asks:

```text
how much meaningful control does the organism have over its local future?
```

Design implication:

- some habitats or states may be intrinsically empowering or disempowering
- internal adaptation can be evaluated partly by future controllability
- organisms that preserve action possibilities may be more robust and more
  evolvable

Useful translation into biosphere terms:

- `local_empowerment`
- `action_reachability`
- `future_sensorimotor_span`
- `control_loss_after_shock`

## 4. Friston (2010, 2012), free-energy principle line

Why it matters:

- this is one of the strongest theoretical attempts to unify action,
  perception, and self-organization
- it is ambitious and controversial, but still useful as a conceptual source

The key lesson we should take carefully:

```text
persisting systems tend to avoid uncontrolled dispersion into arbitrary states;
they maintain themselves in a restricted set of viable states.
```

For our purposes, the most useful takeaway is not the full formal apparatus.
It is the idea that life-like systems:

- have viability constraints,
- rely on prediction or structured coupling,
- and act in ways that reduce destructive uncertainty.

Design implication:

- viability should be framed as occupancy of constrained alive states
- organisms should sometimes act to maintain predictability or recover
  controllable structure

Useful translation into biosphere terms:

- `viability_band`
- `prediction_stability`
- `state_dispersion_risk`
- `uncertainty_recovery`

## 5. Kirchhoff et al. (2018), "The Markov blankets of life"

Why it matters:

- this gives a more explicit boundary-oriented discussion of autonomy
- it is useful because our world will need system/environment boundaries that
  are neither mystical nor trivial

The key lesson:

```text
a living system can be analyzed as having a boundary that mediates what counts
as internal state, external state, and interaction
```

This matters for us because `alife_biosphere` will eventually have:

- organisms
- groups
- habitats
- archives

and each may need a different kind of boundary.

Design implication:

- boundaries should be explicit in the data model and event model
- not every state variable belongs to the same level
- group or colony boundaries may become analyzable objects later

Useful translation into biosphere terms:

- `boundary_integrity`
- `internal_state_vector`
- `external_coupling_strength`
- `group_boundary_score`

## What This Means For Our Project

The literature suggests that `alife_biosphere` should eventually care about
more than:

- reproduction
- occupancy
- adaptation

It should also care about:

- self-maintenance
- internal control
- viable-state preservation
- organizational persistence

The strongest project-level interpretation is:

```text
the biosphere should support systems whose behavior helps maintain their own
continued existence and future possibility structure,
not only systems that briefly exploit an opportunity and disappear
```

That is a very important distinction.

## Direct Design Consequences

## 1. Self-maintenance should be first-class, not only resource bookkeeping

It is not enough to track:

- energy
- matter
- integrity

We should later ask how these variables interact to preserve organism identity.

Suggested fields:

- `self_maintenance_load`
- `repair_dependency_score`
- `organizational_stability`

## 2. Control should be measured from the organism perspective

Empowerment suggests that the system should eventually measure whether an
organism has many usable future options or is trapped in brittle states.

Suggested metrics:

- local empowerment
- reachable viable states
- control loss under stress

## 3. Viability should be treated as a bounded state region

The free-energy / autonomy line suggests that living systems occupy restricted
viable states rather than arbitrary trajectories.

Suggested fields:

- `viability_band`
- `dispersion_risk`
- `alive_state_margin`

## 4. Boundaries should become explicit

This is important later for:

- group individuality
- distributed memory
- archive access
- habitat-mediated regulation

Suggested fields:

- `boundary_integrity`
- `internal_external_coupling`
- `group_boundary_score`

## 5. Self-organization should be operationalized, not merely claimed

We should avoid using "self-organized" to mean "complex-looking."

Better indicators might include:

- persistence without centralized control
- distributed maintenance
- recovery after perturbation
- re-emergence of coordinated structure

Suggested metrics:

- decentralized_recovery_score
- distributed_control_index
- self_repair_success

## Proposed Additions To The Existing Design

### New fields

- `self_maintenance_load`
- `organizational_stability`
- `local_empowerment`
- `viability_band`
- `boundary_integrity`
- `internal_dependency_index`

### New event types

- `self_maintenance_event`
- `organizational_failure`
- `repair_event`
- `control_loss_event`
- `boundary_breach_event`

### New metrics

- local empowerment
- viable-state occupancy
- organizational persistence
- distributed control index
- self-maintenance efficiency
- recovery of autonomy after shock

## Proposed Probe Design

The first autonomy-focused probe should stay narrow.

A reasonable first probe is:

```text
same world
-> compare agents that maximize immediate extraction
   with agents that preserve local controllability and maintenance capacity
-> introduce disturbance
-> measure persistence, recovery, and future option retention
```

The first useful question is:

```text
Do organisms that preserve local control and self-maintenance survive and adapt
better over longer horizons than organisms that exploit short-term gain only?
```

That is enough to justify autonomy-oriented metrics.

## Build Recommendations

This literature review suggests three near-term design tasks.

### 1. Add a self-maintenance section to the core design

Reason:

- otherwise survival stays too close to ordinary reward-style resource tracking

### 2. Reserve a place for organism-centric control metrics

Reason:

- empowerment-like quantities could later become a useful diagnostic signal

### 3. Make system boundaries more explicit in future group and archive design

Reason:

- autonomy depends partly on what is inside, outside, and mediating interaction

## Bottom Line

The information and autonomy literature tells us that the strongest life-like
systems are not just ones that perform tasks.

They are systems that:

```text
maintain themselves,
preserve usable future options,
and keep their organization going under disturbance
```

That is the standard this literature adds to `alife_biosphere`.

## Sources

- Maturana, H. R., Varela, F. J. (1980).
  "Autopoiesis and Cognition: The Realization of the Living."
  [Springer](https://link.springer.com/book/10.1007/978-94-009-8947-4)
  and [organism.earth mirror](https://www.organism.earth/library/document/autopoiesis-and-cognition)
- Winning, J., Bechtel, W. (2016).
  "Review of Biological Autonomy."
  [Cambridge Core](https://www.cambridge.org/core/journals/philosophy-of-science/article/review-of-biological-autonomy-alvaro-moreno-and-matteo-mossio-biological-autonomy-dordrecht-springer-2015-221-pp-12900/5ED9A22C2A08D25ECAE9376D5079D2C2)
- Klyubin, A. S., Polani, D., Nehaniv, C. L. (2005).
  "Empowerment: A Universal Agent-Centric Measure of Control."
  [University of Hertfordshire repository](https://herts-repo-prod.herts.cdl.cosector.com/id/eprint/282/)
- Friston, K. (2012).
  "A Free Energy Principle for Biological Systems."
  [MDPI Entropy](https://www.mdpi.com/1099-4300/14/11/2100)
- Kirchhoff, M., Parr, T., Palacios, E., Friston, K., Kiverstein, J. (2018).
  "The Markov blankets of life: autonomy, active inference and the free energy principle."
  [Royal Society / ResearchGate entry](https://www.researchgate.net/publication/322547090_The_Markov_blankets_of_life_autonomy_active_inference_and_the_free_energy_principle)
