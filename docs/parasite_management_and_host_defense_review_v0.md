# Parasite Management And Host Defense Review v0

## Purpose

This note narrows the antagonist question from:

```text
How should parasites exist in the biosphere?
```

to a harder and more practical one:

```text
How should the world remain ecologically informative once parasites,
host defense, and local collapse are all possible?
```

We already have:

- parasite entry conditions,
- graph-sensitive spread,
- mimic / jammer / thief roles.

What was still missing is a focused review on:

- resistance vs tolerance,
- host defense tradeoffs,
- demographic feedback,
- parasite management without sterilizing the world.

## Short Answer

The literature supports a balanced position:

```text
Parasites should be dangerous enough to reshape lineages and ecology,
but not so absolute that they erase diversity or trivialize every treatment.
```

For the biosphere, that means:

- defense must be costly;
- hosts should be allowed both resistance and tolerance strategies;
- parasite pressure should remain local and demographic, not purely global;
- protection can come from behavior, habitat structure, and symbiotic or
  archive-like support, not only direct "immune power."

## 1. Resistance And Tolerance Must Be Separated

### [Howick and Lazzaro 2014, "Genotype and diet shape resistance and tolerance across distinct phases of bacterial infection"](https://bmcecolevol.biomedcentral.com/articles/10.1186/1471-2148-14-56)

Main result:

- host defense is not one thing;
- resistance and tolerance are distinct strategies with different costs and
  dynamics.

What we should take from it:

- the best host is not always the one that suppresses parasite load most
  aggressively;
- hosts can survive by reducing damage, not only by reducing parasite burden.

Design implication:

- the biosphere should not collapse host defense into a single "anti-parasite"
  score;
- later host-defense variables should distinguish:
  - resistance
  - tolerance

### [King and Bonsall 2017, "The evolutionary and coevolutionary consequences of defensive microbes for host-parasite interactions"](https://bmcecolevol.biomedcentral.com/articles/10.1186/s12862-017-1030-z)

Main result:

- protective third parties can alter host-parasite coevolution;
- defense may be indirect and still evolutionarily powerful.

What we should take from it:

- host defense need not be internal only;
- partner-mediated protection is a legitimate ecological mechanism.

Design implication:

- later versions of the biosphere can allow:
  - protective partners,
  - clade-level defensive archives,
  - or habitat-mediated defense effects.

## 2. Parasite Pressure Should Be Demographic, Not Abstract

### [Tellier et al. 2016, "Host–parasite coevolution: why changing population size matters"](https://www.sciencedirect.com/science/article/pii/S0944200616300071)

Main result:

- host-parasite coevolution is strongly shaped by changing population size;
- parasites often experience extreme bottlenecks.

What we should take from it:

- parasite pressure should not be modeled as a static fog over the map;
- host and parasite demography both matter.

Design implication:

- antagonist probes should track:
  - local host density,
  - antagonist density,
  - bottleneck episodes,
  - recolonization lag.

### [Rafaluk et al. 2015, "Rapid evolution of virulence leading to host extinction under host-parasite coevolution"](https://bmcecolevol.biomedcentral.com/articles/10.1186/s12862-015-0407-0)

Main result:

- virulence can evolve fast enough to drive host extinction.

What we should take from it:

- parasite settings can easily become too strong;
- "interesting antagonism" and "trivial extinction machine" are close neighbors.

Design implication:

- virulence and spread need bounded default ranges;
- antagonist controls must include severity ladders, not only on/off.

## 3. Host Defense Is A Tradeoff, Not A Free Improvement

### [Kamiya et al. 2016, "Coevolutionary feedback elevates constitutive immune defence: a protein network model"](https://bmcecolevol.biomedcentral.com/articles/10.1186/s12862-016-0667-3)

Main result:

- constitutive defense can evolve under coevolutionary pressure;
- but stronger defense trades off against other life-history components.

What we should take from it:

- defense cannot be a free stat increase;
- background protection should cost energy, growth, or flexibility.

Design implication:

- later host-defense mechanisms should pay in:
  - energy
  - reproduction readiness
  - developmental flexibility

### [King et al. 2022, "Microbial protection favors parasite tolerance and alters host-parasite coevolutionary dynamics"](https://www.sciencedirect.com/science/article/pii/S0960982222001257)

Main result:

- protection can shift hosts toward tolerance rather than resistance;
- coevolutionary feedback changes when protection is mediated indirectly.

What we should take from it:

- the world should not assume one canonical defense trajectory;
- support systems can redirect, not just amplify, host defense.

Design implication:

- later antagonist-defender systems should allow:
  - resistance-heavy worlds,
  - tolerance-heavy worlds,
  - and mediated-defense worlds.

## 4. Spatial Management Matters

### [Tellier and Brown 2011, "Spatial heterogeneity, frequency-dependent selection and polymorphism in host-parasite interactions"](https://pmc.ncbi.nlm.nih.gov/articles/PMC3273489/)

Main result:

- spatial heterogeneity supports polymorphism in host-parasite systems.

What we should take from it:

- well-mixed parasite pressure is a bad default for diversity.

Design implication:

- refuge and frontier structure should matter for parasite outcomes;
- parasite pressure should vary across habitats, not just globally.

### [Deshpande et al. 2025, "Landscape structure as a driver of eco-evolution in host-parasite systems"](https://pmc.ncbi.nlm.nih.gov/articles/PMC12137051/)

Main result:

- topology changes virulence evolution qualitatively.

What we should take from it:

- graph design is part of parasite management.

Design implication:

- later parasite probes should compare graph families rather than treating the
  graph as fixed scenery.

## 5. Practical Parasite-Management Rules For The Biosphere

The literature suggests five practical rules.

### Rule 1. Use local parasite pressure first

Start with habitat-local antagonist dynamics.

Avoid:

- globally uniform parasite pressure
- instant worldwide infection states

### Rule 2. Bound virulence and spread separately

Virulence and mobility should be independent parameters.

Why:

- a parasite that harms strongly but spreads poorly is different from one that
  spreads well but harms weakly.

### Rule 3. Keep at least one non-parasite refuge path

Why:

- without refuges, parasite treatments will often collapse into extinction
  controls rather than informative ecology.

### Rule 4. Model defense as a tradeoff

Defense should cost:

- energy
- time
- information
- or reproductive readiness

Otherwise host defense becomes a free answer key.

### Rule 5. Separate management from sterilization

Good parasite management means:

- parasites remain ecologically real,
- hosts remain under pressure,
- but diversity and recovery remain possible.

It does **not** mean:

- remove parasite impact whenever it becomes inconvenient.

## 6. Recommended Minimal Metrics

For the first parasite-aware probes, log at least:

- `parasite_occupancy_by_habitat`
- `host_density_near_parasites`
- `parasite_spread_rate`
- `parasite_local_extinction_rate`
- `host_integrity_loss_near_parasites`
- `host_reproduction_ready_suppression`
- `refuge_escape_rate`
- `recolonization_lag_after_parasite_bloom`

## 7. Bottom Line

The key design lesson is:

```text
Parasite management should preserve coevolutionary pressure,
not eliminate it.
```

If we get that balance right, parasites become engines of structure rather than
mere extinction buttons.
