# Antagonist Lifecycle And Parasite Design Review v0

## Purpose

This note closes a practical design gap:

```text
How should antagonists enter the biosphere as real ecological actors,
instead of appearing as decorative "enemy roles"?
```

The project already has scattered references to:

- parasites
- thieves
- mimics
- jammers

What was missing is a lifecycle-oriented design synthesis:

- what counts as an antagonist,
- what minimal lifecycle makes it ecologically meaningful,
- how topology and demography should shape it,
- and which claims we should avoid making too early.

## Short Answer

The literature supports a disciplined first step:

```text
Start with parasites as the reference antagonist.
Treat thieves, mimics, and jammers as later role specializations,
not four unrelated systems.
```

Why:

- parasites already force us to think about host dependence, transmission,
  bottlenecks, topology, and demographic feedback;
- once the parasite lifecycle is coherent, the other roles become interpretable
  variations on access, deception, and exploitation.

## 1. What Counts As An Antagonist

For this project, an antagonist should satisfy at least one of:

1. gains from the state, behavior, or signal infrastructure produced by others;
2. imposes fitness cost on another actor or group;
3. depends on a host, target, or exploited infrastructure for persistence;
4. changes ecological or communication structure in a way that alters selection
   for everyone else.

That definition is intentionally broader than "a creature that attacks."

It includes:

- parasite
- thief
- mimic
- jammer

But it excludes:

- generic environmental hazard
- exogenous researcher-imposed penalty

The point is that antagonists must be endogenous ecological entities.

## 2. Why Parasites Should Come First

### [Zaman et al. 2014, "Coevolution Drives the Emergence of Complex Traits and Promotes Evolvability"](https://journals.plos.org/plosbiology/article?id=10.1371%2Fjournal.pbio.1002023)

Main result:

- host-parasite coevolution increased trait complexity and evolvability relative
  to controls without parasites.

What we should take from it:

- antagonists are not just stressors;
- they can actively expand the reachable design space.

Design implication:

- adding parasites is not only about making life harder;
- it is also a route to richer adaptation dynamics.

### [Acosta and Zaman 2022, "Ecological Opportunity and Necessity: Biotic and Abiotic Drivers Interact During Diversification of Digital Host-Parasite Communities"](https://www.frontiersin.org/articles/10.3389/fevo.2021.750772/full)

Main result:

- biotic antagonism and abiotic complexity affect diversification differently;
- abundance, diversity, and complexity should not be collapsed into one output.

What we should take from it:

- parasite pressure deserves its own controlled treatment;
- "the world got more complex" is not an adequate summary.

Design implication:

- parasite-on vs parasite-off should be a standard control family;
- antagonist metrics should remain separate from generic world complexity
  metrics.

## 3. Topology And Demography Matter

### [Tellier and Brown 2011, "Spatial heterogeneity, frequency-dependent selection and polymorphism in host-parasite interactions"](https://pmc.ncbi.nlm.nih.gov/articles/PMC3273489/)

Main result:

- spatial heterogeneity and limited coupling between demes help maintain
  polymorphism in host-parasite systems.

What we should take from it:

- well-mixed antagonism would erase exactly the diversity structure we want.

Design implication:

- parasite pressure must be habitat-local before it is global;
- migration and transmission should be bounded by graph structure.

### [Deshpande et al. 2025, "Landscape structure as a driver of eco-evolution in host-parasite systems"](https://pmc.ncbi.nlm.nih.gov/articles/PMC12137051/)

Main result:

- graph topology qualitatively changes virulence evolution and diversification.

What we should take from it:

- topology is not a visualization detail;
- the same antagonist can behave very differently on different habitat graphs.

Design implication:

- later antagonist probes must compare topology families;
- "parasite strength" is not meaningful without graph context.

### [Morgan et al. 2007, "Differential impact of simultaneous migration on coevolving hosts and parasites"](https://link.springer.com/article/10.1186/1471-2148-7-1)

Main result:

- migration affects hosts and parasites differently;
- coevolutionary dynamics depend on how both sides move through space.

What we should take from it:

- do not assume host migration and antagonist spread are symmetric processes.

Design implication:

- antagonists should later get their own spread parameters, not just reuse host
  movement logic.

### [Živković et al. 2019, "Neutral genomic signatures of host-parasite coevolution"](https://bmcecolevol.biomedcentral.com/articles/10.1186/s12862-019-1556-3)

Main result:

- demographic coupling shapes the signatures of host-parasite coevolution.

What we should take from it:

- demographic history is part of antagonistic dynamics, not a side detail.

Design implication:

- antagonist probes should record:
  - bottleneck episodes,
  - local extinctions,
  - recolonization timing,
  - and occupancy synchronization.

### [Ebert and Fields 2020, "Host–parasite co-evolution and its genomic signature"](https://www.nature.com/articles/s41576-020-0269-1)

Main result:

- host-parasite systems are often shaped by balancing selection, rare advantage,
  and fluctuating dynamics, not only arms races.

What we should take from it:

- a parasite system should not be judged only by who "wins";
- sustained polymorphism and time-lagged selection are equally interesting.

Design implication:

- later antagonist metrics should include:
  - persistence,
  - polymorphism,
  - occupancy lag,
  - and role turnover.

## 4. Operationalizing "Parasite"

### [Stepney and Hickinbotham 2021, "What is a Parasite? Defining reaction and network properties in an open ended automata chemistry"](https://pure.york.ac.uk/portal/en/publications/what-is-a-parasite-defining-reaction-and-network-properties-in-an/)

Main contribution:

- parasitism should be defined from interaction and network properties rather
  than from narrative labels.

What we should take from it:

- we need an operational test for antagonism.

For our biosphere, a parasite-like role should require:

1. positive payoff from host-associated interaction;
2. net cost to host integrity, resources, trust, or coordination;
3. dependence on host presence, signals, or infrastructure;
4. inability to persist at the same level without that exploited context.

That gives us something measurable instead of a lore label.

## 5. The Minimal Antagonist Ladder

To keep the design sane, antagonists should arrive in stages.

### Stage A. Opportunistic thief

Definition:

- steals local resources or benefits from occupied habitats;
- does not yet require communication or identity tricks.

Why first:

- easiest to implement and reason about;
- tests whether local exploitation meaningfully changes selection.

### Stage B. Host-dependent parasite

Definition:

- gains only when specific hosts or host-rich habitats are present;
- reduces host viability or local reproductive readiness.

Why second:

- introduces real dependence and coevolution;
- still simpler than signal deception.

### Stage C. Mimic

Definition:

- exploits trust, kin tags, or archive/source cues by false resemblance.

Why later:

- only meaningful once trust channels and signaling already exist.

### Stage D. Jammer

Definition:

- reduces reliability of signaling or archive transmission without necessarily
  stealing direct resources.

Why later:

- depends on communication architecture being real, not symbolic decoration.

## 6. Recommended First Lifecycle

The first real antagonist lifecycle should be parasite-like, but simple:

```text
encounter host or host-rich habitat
-> bind to host context or local host-produced trace
-> extract payoff or reduce host state
-> replicate or spread conditionally
-> decay quickly if hosts disappear
```

This gives us four key properties:

- dependence
- harm
- spread
- fragility outside host context

That is enough to make antagonists ecologically meaningful.

## 7. What We Should Measure

### Occupancy And Spread

- antagonist occupancy by habitat
- spread rate across graph edges
- antagonist local extinction rate
- recolonization lag

### Host Impact

- host integrity loss near antagonist presence
- host reproduction-ready suppression
- host migration response
- local host lineage turnover

### Dependence

- antagonist persistence without hosts
- host-density dependence of antagonist growth
- trace-dependence if antagonists exploit signals or habitat memory

### Diversity And Role Change

- antagonist role frequency
- mimic success rate
- jammer impact on signal reliability
- host/antagonist diversification coupling

## 8. What We Should Not Do

Do not start with:

- one generic "enemy" class;
- a free-standing parasite that survives equally well without hosts;
- globally mixed antagonist pressure;
- rich deceptive signaling before trust channels exist.

Those would create drama, but not good ecology.

## 9. Direct Design Consequences

1. M8 in `build_plan_v1.md` should begin with parasites or thieves, not all
   antagonist roles at once.
2. Antagonist spread must remain graph-dependent.
3. Antagonist events must be reconstructable from logs and interaction edges.
4. Parasite pressure should be local and history-dependent before it becomes a
   global treatment.
5. Host and antagonist movement parameters should remain separable.

## Bottom Line

The strongest design lesson is:

```text
Parasites should enter the biosphere as dependent ecological actors,
not as generic enemies.
```

If we get that right, then thief, mimic, and jammer roles can later be added as
coherent antagonist specializations rather than disconnected mechanics.
