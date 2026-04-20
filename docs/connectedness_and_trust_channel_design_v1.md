# Connectedness And Trust Channel Design v1

## Purpose

This note turns two unresolved design questions into a more concrete position:

1. What should `connectedness` mean in a small biosphere?
2. Why should `direct trust` and `archive/source trust` be modeled as separate
   channels?

This is not a full theory review.
It is a design clarification note aimed at preventing two common mistakes:

- reducing connectedness to one graph statistic
- collapsing all trust into one undifferentiated reputation score

## 1. Connectedness Is Not One Number

### [Landi et al. 2018, "Complexity and stability of ecological networks: a review of the theory"](https://link.springer.com/article/10.1007/s10144-018-0628-3)

Main result:

- ecological network complexity is described through multiple structural
  families rather than one canonical metric
- common measures include:
  - size
  - connectance
  - linkage density
  - weighted connectance
  - degree / strength distributions
  - modularity
  - nestedness
- the review explicitly emphasizes that consensus is lacking on any single
  complexity-stability law

What we should take from it:

- using one scalar called `connectedness` would be an over-compression
- different metrics capture different structural risks and opportunities

Design implication:

- our `connectedness` should be a proxy family, not a single field

### [Fletcher et al. 2013, "Network modularity reveals critical scales for connectivity in ecology and evolution"](https://www.nature.com/articles/ncomms3572)

Main result:

- modularity analysis can reveal critical mesoscales in movement and gene-flow
  networks
- including modularity changed conclusions about patch importance and suggested
  higher metapopulation viability than analyses that ignored hidden modules

What we should take from it:

- mesoscale structure matters
- local connectivity and global connectivity are not enough; hidden modules can
  change rescue and movement dynamics

Design implication:

- we should track module structure or at least within-module versus
  between-module traffic

### [Grilli et al. 2016, "Modularity and stability in ecological communities"](https://www.nature.com/articles/ncomms12031)

Main result:

- modularity is not uniformly stabilizing
- for some parameter regimes it has moderate stabilizing effects
- anti-modularity can be strongly destabilizing
- the same modularity level can have different effects depending on interaction
  sign and strength statistics

What we should take from it:

- modularity is informative but not morally "good"
- the effect of connectedness depends on what is flowing through the network

Design implication:

- connectedness metrics should stay paired with interaction-type summaries
- we should avoid any rule like `higher modularity = better`

## 2. A Cheap Connectedness Profile For Our Biosphere

For a small artificial-life world, the most defensible approach is a profile of
cheap structural summaries.

Recommended `connectedness_profile`:

```text
connectedness_profile =
  {
    weighted_interaction_density,
    degree_or_strength_inequality,
    module_separation,
    corridor_concentration,
    redundancy_score
  }
```

### 2.1 Weighted interaction density

Meaning:

- how much interaction actually occurs, not only how many possible links exist

Possible proxy:

- normalized count or weight of realized interaction events per habitat or group

### 2.2 Degree or strength inequality

Meaning:

- whether connectivity is broadly shared or concentrated in a few hubs

Possible proxy:

- Gini-like inequality over partner counts or interaction weights

Why it matters:

- worlds with the same density can differ sharply in fragility if one relies on
  a few bridging actors

### 2.3 Module separation

Meaning:

- whether local structure is organized into semi-autonomous clusters

Possible proxy:

- ratio of within-cluster to between-cluster interactions

Why it matters:

- too little separation can destroy diversity
- too much separation can kill rescue flow

### 2.4 Corridor concentration

Meaning:

- whether movement or information passes through a few critical edges

Possible proxy:

- share of migration or signaling flow carried by top-k edges

Why it matters:

- rescue may appear available in principle while actually depending on one
  brittle corridor

### 2.5 Redundancy score

Meaning:

- whether the system has alternative paths for migration, help, or information

Possible proxy:

- count or weight of non-identical viable paths between refuge and frontier
  zones

Why it matters:

- connectedness without redundancy can be highly brittle

## 3. What We Should Not Do With Connectedness

Three modeling mistakes would be easy here.

### Mistake 1. Treat raw edge count as sufficient

Raw connectivity ignores weight, role concentration, and modular structure.

### Mistake 2. Treat modularity as automatically stabilizing

The literature does not support that simplification.

### Mistake 3. Ignore what kind of link is being measured

Migration, conflict, signaling, and archive reliance should not be pooled into a
single generic graph without type labels.

## 4. Trust Is Also Not One Channel

The second unresolved design problem is trust.

The literature now points to a clear separation:

- trust formed from direct counterpart interaction
- trust formed from broadcast, advice, prestige, or archive sources

These channels differ in how evidence is generated, how quickly it arrives, and
how widely it should generalize.

### [Fareri et al. 2012, "Effects of Direct Social Experience on Trust Decisions and Neural Reward Circuitry"](https://pmc.ncbi.nlm.nih.gov/articles/PMC3472892/)

Main result:

- direct prior social experience strongly shaped later trust decisions
- experience-consistent outcomes reinforced those priors in subsequent trust
  interactions

What we should take from it:

- direct embodied interaction leaves a different trust trace from abstract
  source cues

Design implication:

- repeated interaction trust should have its own update path

### [Hertz et al. 2021, "Trusting and learning from others: immediate and long-term effects of learning from observation and advice"](https://pmc.ncbi.nlm.nih.gov/articles/PMC8527195/)

Main result:

- people were more likely to immediately follow explicit advice than to copy an
  observed choice
- this effect depended on trust in the adviser
- long-run responses split between those who kept relying on social
  information and those who reverted to trial-and-error learning

What we should take from it:

- intentionally broadcast information is handled differently from observed
  behavior
- source trust matters especially for advice-like channels

Design implication:

- archive or broadcast capsules should not be treated as equivalent to direct
  partner experience

### [Brand et al. 2021, "Trusting the experts: The domain-specificity of prestige-biased social learning"](https://pmc.ncbi.nlm.nih.gov/articles/PMC8357104/)

Main result:

- learners strongly preferred domain-specific prestige cues over
  domain-general prestige when both were available

What we should take from it:

- source reliability should be at least partly domain-specific

Design implication:

- archive-source trust should carry domain tags
- success in one protocol family should not grant universal trust

### [Rendell et al. 2010, "Why Copy Others? Insights from the Social Learning Strategies Tournament"](https://pmc.ncbi.nlm.nih.gov/articles/PMC2989663/)

Main result:

- social learning performed well partly because population filtering had
  already occurred before copying

What we should take from it:

- source trust in the archive is partially second-hand trust

Design implication:

- archive trust should include provenance and validation history, not only
  source identity

## 5. Why Direct Trust And Archive Trust Must Be Separate

There are four concrete reasons.

### 5.1 Evidence origin is different

Direct trust comes from:

- repeated interaction
- realized outcomes
- partner-specific reciprocity

Archive trust comes from:

- advice-like or prestige-like information
- third-party filtering
- source attribution and copying history

### 5.2 Update speed is different

Direct trust may update quickly after one strong interaction.

Archive trust often needs:

- provenance checks
- validation episodes
- domain matching

### 5.3 Generalization scope is different

Direct trust should often stay narrow:

- this partner
- this group role
- this context

Archive trust can generalize a bit more, but only within a relevant domain:

- this source in this protocol family
- this archive stream in this habitat family

### 5.4 Failure cost is different

A deceptive partner may waste one episode.

A deceptive archive source can poison many offspring, learners, or habitats at
once if left unchecked.

## 6. A Minimal Dual-Channel Trust Design

For the first mechanism design, trust should be split as:

```text
direct_trust[partner_or_role]
source_trust[source_id, domain]
```

## 6.1 Direct trust

Best used for:

- repeated partner interactions
- local coordination
- kin or in-group cooperation
- retaliation or forgiveness

Suggested evidence inputs:

- actual local outcomes
- reciprocity
- deception detection in repeated contact

## 6.2 Source trust

Best used for:

- archive capsules
- broadcast messages
- prestige-like cues
- advice-like recommendations

Suggested evidence inputs:

- source provenance
- domain match
- validation success or failure
- recency
- copying chain depth

## 6.3 Do not over-unify

The first version should not let:

- one deceptive archive source immediately destroy direct trust in all partners
- one honest direct partner automatically become trusted in all archive domains

That would erase the asymmetry the literature points to.

## 7. Recommended Experimental Variables

For connectedness:

- `interaction_density`
- `module_separation`
- `corridor_concentration`
- `redundancy_score`
- `bridge_actor_dependence`

For dual trust channels:

- `direct_trust_decay`
- `source_trust_decay`
- `domain_specificity_strength`
- `archive_provenance_depth`
- `verification_budget`
- `broadcast_to_observation_bias`

## 8. Recommended Metrics

### Connectedness metrics

- `weighted_interaction_density`
- `strength_inequality`
- `module_separation`
- `corridor_load`
- `path_redundancy`

### Direct-trust metrics

- `partner_reliability`
- `forgiveness_rate`
- `retaliation_delay`
- `trust_recovery_lag`

### Source-trust metrics

- `domain_matched_transfer_gain`
- `cross_domain_failure_rate`
- `archive_poisoning_rate`
- `validation_precision`
- `source_trust_drift`

## 9. Design Decision

This note supports two concrete decisions.

1. `connectedness` should be implemented as a profile of cheap network
   summaries, not one scalar.

2. `trust` should be implemented as at least two linked but distinct channels:
   direct interaction trust and archive/source trust.

These decisions reduce the chance that the biosphere will accidentally collapse
complex social structure into one overcompressed variable.

