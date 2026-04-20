# Archive Domain Tags And Provenance Design v1

## Purpose

This document freezes a first design position for domain tags and provenance in
the future `CulturalArchive`.

It answers four practical questions:

1. Why should archive capsules carry domain tags?
2. Why is provenance more than a convenience field?
3. How should source trust interact with domains and copying chains?
4. What metadata is the minimum needed to keep archive use scientifically
   interpretable?

This note exists because the literature already rules out a naive archive.

A useful archive cannot be:

- domainless
- provenance-free
- globally trusted
- infinitely visible

## 1. Why Domain Tags Matter

The archive is supposed to transmit compact useful structure.
But "useful" is always relative to some context.

The literature already gives three strong reasons to encode that context.

### [Brand et al. 2021, "Trusting the experts: The domain-specificity of prestige-biased social learning"](https://pmc.ncbi.nlm.nih.gov/articles/PMC8357104/)

Main result:

- learners preferred domain-specific prestige cues over domain-general prestige

What we should take from it:

- success in one domain should not automatically produce global authority

### [Hertz et al. 2021, "Trusting and learning from others: immediate and long-term effects of learning from observation and advice"](https://pmc.ncbi.nlm.nih.gov/articles/PMC8527195/)

Main result:

- advice-like information and observed behavior are not handled the same way
- long-run social reliance diverges between learners

What we should take from it:

- archive items should record how they were produced and learned

### [Rendell et al. 2010, "Why Copy Others? Insights from the Social Learning Strategies Tournament"](https://pmc.ncbi.nlm.nih.gov/articles/PMC2989663/)

Main result:

- social learning performs well partly because the copied information has
  already been filtered by population success

What we should take from it:

- archive value depends on source filtering and validation history

These results together imply:

```text
archive trust must be domain-sensitive and provenance-sensitive
```

## 2. Why Provenance Matters

If we lose provenance, we lose the ability to answer the questions that make
the archive scientifically meaningful.

Without provenance we cannot reliably ask:

- who first generated this capsule?
- in which habitat family did it work?
- was it learned directly, copied, recombined, or compressed?
- how many copying hops separate current use from original discovery?
- did it succeed because of the source domain, or because it was later refined?

Provenance is therefore not a bookkeeping luxury.
It is what keeps culture interpretable as a causal channel.

## 3. The Archive Should Not Store Generic "Skills"

The first archive ontology should stay narrow.

Recommended capsule types:

- protocol fragment
- migration heuristic
- repair or harvest routine
- signaling convention fragment
- habitat caution pattern

Each capsule should be compact and contextual.

What to avoid:

- whole-agent snapshots
- domainless "best strategy" entries
- opaque embeddings with no recoverable ancestry

## 4. Minimal Domain Taxonomy

The domain system should be simple enough for early implementation and rich
enough to block naive overgeneralization.

Recommended domain axes:

## 4.1 Habitat family tag

Examples:

- nursery
- refuge
- frontier
- volatile

Why:

- a capsule that helps in one habitat family may fail badly in another

## 4.2 Protocol family tag

Examples:

- harvest
- avoidance
- migration
- coordination
- archive-use

Why:

- source trust should not automatically transfer across protocol families

## 4.3 Risk profile tag

Examples:

- low-risk
- high-risk
- deception-sensitive
- parasite-sensitive

Why:

- some capsules are only useful when organisms can tolerate the associated
  danger or noise

## 4.4 Life-stage tag

Examples:

- juvenile
- mature
- reproductive

Why:

- developmental capsules should not be confused with adult exploitation
  capsules

## 4.5 Social-mode tag

Examples:

- solo
- kin-group
- signal-dependent
- archive-dependent

Why:

- some routines depend on cooperation or local signaling context

## 5. Provenance Fields

Every archive capsule should carry at least:

```text
capsule_id
capsule_type
source_id
source_kind
origin_lineage_id
origin_habitat_id
origin_tick
domain_tags
parent_capsule_ids
copy_chain_depth
derivation_mode
validation_count
validation_success_count
last_validation_tick
last_success_tick
recency_score
visibility_state
```

### Key fields

- `source_kind`
  direct experience, peer copy, archive copy, recombination, or compression

- `parent_capsule_ids`
  allows recombined or refined capsules to keep ancestry

- `copy_chain_depth`
  tells us how far the capsule is from original lived discovery

- `derivation_mode`
  direct, copied, refined, recombined, or compressed

- `validation_success_count`
  prevents reuse count from masquerading as quality

- `visibility_state`
  lets archive overload and gating be measured rather than hidden

## 6. Source Trust Must Be Domain-Specific

This is the most important design choice in the document.

Recommended structure:

```text
source_trust[source_id, domain_key]
```

Not:

```text
source_trust[source_id]
```

Why:

- a source can be reliable in migration capsules and weak in signaling capsules
- a source can be reliable in frontier habitats and unreliable in refuge life
- a source may be trustworthy for juvenile development and poor for
  reproductive behavior

This follows directly from the domain-specific prestige literature and from the
broader social-learning results already collected.

## 7. Provenance Chains And Trust Decay

The archive should not treat all copies as equal.

Trust should degrade or at least become more uncertain with:

- copy_chain_depth
- stale validation
- domain mismatch
- repeated failure in new habitats

This does not mean "old is bad."
It means:

- older or repeatedly copied structure should require stronger validation

## 8. Minimal Rules For Visibility And Gating

Domain tags and provenance only matter if access is constrained.

Recommended first rules:

- visibility should be bounded to a small number of candidate capsules
- domain match should affect ranking or visibility
- stale unvalidated capsules should sink in visibility
- capsules with high mismatch history should not stay globally prominent

This makes the archive behave like an ecological information market rather than
an infinite menu.

## 9. Recommended Capsule Ranking Inputs

When the archive shows candidate capsules, ranking should consider:

- domain match score
- source trust in that domain
- validation success rate
- recency
- copy_chain_depth penalty
- current habitat or life-stage relevance

This is the minimum needed to keep archive use from becoming random or
prestige-only.

## 10. What Must Be Logged For Archive Science

The event layer should record:

- archive_access_event
- visible_capsule_set
- selected_capsule_id
- domain_match_score
- source_trust_before
- validation_result
- source_trust_after
- capsule_retained_or_discarded

Without this, we will not be able to tell whether archive use helped because of:

- domain matching
- source quality
- accidental copying luck
- later refinement

## 11. Recommended Failure Modes To Measure

The archive should be designed so that these failure modes remain visible:

### 11.1 Cross-domain misuse

A capsule works in one domain and gets copied into another where it fails.

Metric ideas:

- `cross_domain_failure_rate`
- `domain_mismatch_penalty`

### 11.2 Archive poisoning

Low-quality or deceptive capsules spread because provenance and validation are
too weak.

Metric ideas:

- `archive_poisoning_rate`
- `stale_capsule_visibility_share`

### 11.3 Prestige overreach

A source succeeds in one domain and gets overtrusted in many unrelated ones.

Metric ideas:

- `cross_domain_trust_leak`
- `domain_specificity_benefit`

### 11.4 Provenance amnesia

Useful or harmful capsules can no longer be traced to origin or derivation
mode.

Metric ideas:

- `provenance_completeness`
- `opaque_capsule_fraction`

## 12. Minimum Experimental Comparisons

These should become explicit archive ablations later.

### 12.1 Domain tags on versus off

Compare:

- domain-aware archive
- domain-blind archive

Expected:

- domain-aware archive should reduce cross-domain failure

### 12.2 Provenance on versus shallow provenance

Compare:

- full provenance chain
- source-id only

Expected:

- full provenance should improve poisoning resistance and interpretation quality

### 12.3 Domain-specific source trust versus global source trust

Compare:

- `source_trust[source_id, domain]`
- `source_trust[source_id]`

Expected:

- domain-specific trust should reduce prestige overreach and harmful transfer

### 12.4 Validation-sensitive ranking versus popularity ranking

Compare:

- success-weighted ranking
- reuse-count ranking

Expected:

- validation-sensitive ranking should outperform popularity ranking under
  changing habitats

## 13. Design Decision

This document supports four concrete decisions.

1. Archive capsules must carry domain tags.

2. Archive capsules must carry provenance fields and derivation mode.

3. Source trust must be domain-specific rather than global.

4. Archive ranking should use validation and domain match, not only reuse or
   source identity.

These decisions keep the archive from collapsing into an opaque and
scientifically uninterpretable memory heap.

