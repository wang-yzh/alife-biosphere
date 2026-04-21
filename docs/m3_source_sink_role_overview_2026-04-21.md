# M3 Source Sink Role Overview 2026-04-21

## Purpose

This note records the first multi-run source/sink role overview for the current
small world.

It answers:

```text
Across several deterministic probe seeds, which habitats behave more like
recovery sources, and which behave more like disturbance sinks?
```

## What Changed

This slice adds a multi-run aggregation layer on top of the existing
disturbance-recovery summaries.

Added in this pass:

- `summarize_source_sink_roles(...)` in `src/alife_biosphere/reporting.py`
- `scripts/run_source_sink_probe.py`
- per-habitat role summaries across multiple seeds
- per-family role summaries across multiple seeds
- ranked `top_source_habitats`
- ranked `top_sink_habitats`

## What To Run

```text
/Users/qlqwpy/Documents/游乐园/.venv/bin/python -m pytest
/Users/qlqwpy/Documents/游乐园/.venv/bin/python scripts/run_source_sink_probe.py
```

## Current Probe Setup

The current source/sink probe aggregates five seeds:

```text
7, 11, 13, 17, 19
```

with the same small-world disturbance configuration used by the current
ecology probe.

## Current Observed Role Pattern

At the time of writing:

- `refuge` is source-leaning
- `nursery` is sink-leaning
- `frontier_a` is the strongest sink habitat in the current aggregate
- `wild_a` is currently the strongest source habitat

Current top source habitats:

```text
wild_a      4
frontier_a  2
frontier_b  2
refuge      2
```

Current top sink habitats:

```text
frontier_a  5
wild_a      3
nursery_b   2
wild_b      2
nursery_a   1
```

Current family-level pattern:

```text
refuge   -> source_leaning
nursery  -> sink_leaning
frontier -> sink_leaning
wild     -> sink_leaning (but mixed, with strong source behavior from wild_a)
```

## What This Supports

This slice supports the narrower claim that the current map is beginning to
differentiate into ecological roles rather than acting as a uniform board.

In particular, it supports the interpretation that:

- some habitats repeatedly supply recolonization
- some habitats repeatedly absorb disturbance and collapse
- family-level structure is beginning to matter

## What It Does Not Support

This slice does not yet support claims about:

- robust role stability across many more seeds
- role stability after major parameter changes
- long-run ecosystem stationarity
- strong niche formation

## Why This Matters For The Sandbox

This is one of the first outputs that makes the map feel like a real place.

Instead of only saying:

```text
something recovered somewhere
```

we can now say:

```text
this part of the map tends to send recoveries outward,
while that part tends to suffer collapses and wait to be refilled
```

That is the beginning of a watchable ecological geography.

## Next Practical Step

The next useful step is either:

- a minimal visual observer that shows occupancy, lineage, and disturbance over
  time

or:

- stronger multi-run role summaries with more seeds and confidence bands
