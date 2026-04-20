# Signaling, Trust, And Deception Review v0

## Purpose

This note is the third targeted literature follow-up from
`docs/literature_backlog_v1.md`.

The goal is to clarify how signaling should enter `alife_biosphere`.

In practice, this note asks:

1. Why should low-bandwidth signaling matter at all?
2. Why is trust never simply "on" or "off"?
3. Why should deception, mimicry, and jamming be treated as normal ecological
   possibilities rather than edge cases?

## Short Answer

The literature supports a very usable position:

```text
Signals can matter even when they are tiny.
Signals are rarely perfectly honest.
Noise, mistrust, and deception are different failure modes.
And stable communication systems often require cost, context, or repeated
interaction structure.
```

For our project, that means:

- communication should begin simple, not rich;
- trust should be conditional and costly;
- archive access should not assume honest signaling;
- mimic, jammer, and parasite roles should be expected rather than bolted on
  later.

## Core Papers

## 1. Johnstone and Grafen (1992), "Error-prone signalling"

Why it matters:

- this is a strong entry point for separating communication failure from
  deception
- it reminds us that a broken signal channel is not the same thing as an
  adversarial signal channel

What we should take from it:

- a signal can fail because of noise, not because of cheating
- receivers should be modeled as making decisions under uncertainty
- reliability is a graded property, not a binary one

Design implication:

We should separate at least three cases:

- honest but noisy signaling
- low-reliability signaling without adversary intent
- actively deceptive signaling

That means our future communication system should not collapse all signal
failure into a single variable.

Useful translation into biosphere terms:

- `message_noise`
- `message_loss`
- `signal_reliability`
- `receiver_confidence`

## 2. Johnstone and Grafen (1993), "Dishonesty and the handicap principle"

Why it matters:

- this is the key caution against naive "all stable signals are honest"
  thinking
- it argues that stable signaling systems may be honest only on average

This is extremely relevant to us.

If we later build:

- kin-recognition cues
- archive admission signals
- danger warnings
- role markers

then we should expect that:

```text
some deception can persist at equilibrium
```

What we should take from it:

- honest communication is often partial, not perfect
- receivers should not trust signals unconditionally
- signal cost and context matter

Design implication:

Trust should not be a free always-correct mechanism.

Instead, the system should make room for:

- false positives
- false negatives
- mixed signaling strategies
- context-dependent trust

Useful translation into biosphere terms:

- `signal_cost`
- `trust_threshold`
- `deception_penalty`
- `signal_history_window`
- `trust_mode` such as kin-based, history-based, or reputation-based

## 3. Skyrms (2008/2009), "Evolution of signalling systems with multiple senders and receivers"

Why it matters:

- this is the cleanest bridge from abstract signaling games to our kind of
  multi-agent world
- it shows that even simple signaling channels can meaningfully reshape
  collective dynamics

What we should take from it:

- meaning can emerge from repeated interaction with simple signals
- communication networks matter, not only one sender and one receiver
- group coordination can arise from low-bandwidth signaling

This is important because we do not need full language to justify communication
in the biosphere.

We only need:

```text
simple signals
+ repeated interactions
+ differential consequences of acting on or ignoring them
```

Design implication:

- start with tiny message primitives
- log who signaled whom and under what context
- allow signaling to affect timing, coordination, and access decisions

Useful translation into biosphere terms:

- `signal_token`
- `sender_id`
- `receiver_id`
- `message_context`
- `coordination_success`

## 4. Skyrms broader signaling-game perspective

Why it matters:

- signaling-game work helps us think about convention formation
- this matters if lineages later evolve:
  - role markers
  - archive trust cues
  - warnings
  - coalition entry signals

What we should take from it:

- useful signal systems can emerge without rich semantics
- repeated coordination can stabilize simple conventions
- conventions can remain fragile when incentives diverge

Design implication:

- signaling should begin with a small finite alphabet
- role and context should shape interpretation
- communication metrics should measure convention stability, not just frequency

## What This Means For Our Project

The literature supports adding communication early, but in a constrained way.

The correct interpretation for `alife_biosphere` is:

```text
start with minimal signaling,
make trust conditional,
distinguish noise from deception,
and expect exploitative roles to emerge whenever signaling affects access,
coordination, or inheritance.
```

This is better than two common mistakes:

```text
mistake 1: no communication until late stages
mistake 2: communication is assumed honest by default
```

## Direct Design Consequences

## 1. We should begin with low-bandwidth message primitives

The first signaling system does not need rich syntax.

A small alphabet is enough:

- `warn`
- `invite`
- `claim_kin`
- `claim_safe`
- `silence`

These are not full meanings yet.
They are just signal tokens with ecological consequences.

Suggested field:

```text
signal_token
```

## 2. Trust should be a mechanism, not a constant

If signaling matters, then trust matters.

Trust should depend on some combination of:

- kin similarity
- past interaction history
- local role compatibility
- signal cost paid
- recent deception outcomes

Suggested fields:

- `trust_threshold`
- `signal_cost`
- `receiver_confidence`
- `reputation_trace`

## 3. Noise and deception should be logged separately

This is one of the most important implementation consequences.

We should not use a single catch-all "bad communication" flag.

Instead distinguish:

- transmission noise
- receiver misclassification
- deliberate deceptive signaling
- jamming or interference

Suggested event types:

- `signal_sent`
- `signal_received`
- `signal_failed`
- `deception_event`
- `jamming_event`

## 4. Archive access should eventually use signaling under uncertainty

This literature is especially relevant for future archive design.

If organisms can seek archive access or social transfer, then the system should
expect:

- honest requests
- false kin claims
- low-cost bluffing
- denial through jamming or crowding

That means archive access should later become a signaling problem, not only a
permission flag.

## 5. Mimics and jammers should be first-class antagonist candidates

The communication literature, together with later parasite literature, suggests
that exploiters should not all attack through direct harm.

Some should attack information channels:

- mimic
- jammer
- false alarm sender
- false trust claimant

Suggested roles to reserve:

- `mimic`
- `jammer`
- `spoofer`

## Proposed Additions To The Existing Design

### New fields

- `signal_token`
- `signal_cost`
- `message_noise`
- `receiver_confidence`
- `trust_threshold`
- `reputation_trace`

### New event types

- `signal_sent`
- `signal_received`
- `signal_failed`
- `deception_event`
- `jamming_event`
- `trust_granted`
- `trust_denied`

### New metrics

- coordination success rate
- false-positive trust rate
- false-negative trust rate
- deception success rate
- convention stability
- message robustness under noise

## Proposed Probe Design

The first signaling probe should stay simple.

A reasonable first probe is:

```text
small population
-> one useful coordination opportunity
-> one low-bandwidth signaling channel
-> compare honest-only, noisy, and deceptive regimes
-> measure coordination, exploitation, and trust calibration
```

The first useful question is:

```text
Does even minimal signaling change ecological outcomes,
and can trust mechanisms separate honest, noisy, and deceptive conditions?
```

That is enough to justify a real signaling layer.

## Build Recommendations

This literature review suggests three near-term build tasks.

### 1. Reserve a tiny signaling interface early

Reason:

- otherwise later communication will arrive as a bolt-on instead of a native
  ecological mechanism

### 2. Separate noise, mistrust, and deception in the event model

Reason:

- they imply different controls and different failure stories

### 3. Treat future archive access as an information problem

Reason:

- archive use will likely become one of the highest-value targets for deception

## Bottom Line

The signaling literature tells us something both simple and important:

```text
communication becomes evolutionarily interesting
as soon as organisms can gain from being believed
and can lose from believing the wrong thing
```

That means `alife_biosphere` should eventually include:

- simple signals
- conditional trust
- noisy channels
- deceptive roles

not because those are fancy extras,
but because they are the normal ecological consequences of meaningful
information flow.

## Sources

- Johnstone, R. A., Grafen, A. (1992). "Error-prone signalling."
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/1354361/)
- Johnstone, R. A., Grafen, A. (1993). "Dishonesty and the handicap principle."
  [Oxford Biology](https://www.biology.ox.ac.uk/publication/386583/scopus)
  and [author PDF](https://users.ox.ac.uk/~grafen/cv/dishonest.pdf)
- Skyrms, B. (2009). "Evolution of signalling systems with multiple senders and receivers."
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2689717/)
