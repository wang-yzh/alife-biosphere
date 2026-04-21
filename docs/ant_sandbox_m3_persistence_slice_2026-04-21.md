# Ant Sandbox M3 Persistence Slice 2026-04-21

## Purpose

This note records the first colony-persistence slice for the ant-sandbox
branch.

It answers:

```text
Has the colony moved beyond a fixed immortal worker set into a bounded living
population?
```

## What Changed

Added in this pass:

- ant death by age
- nest-funded ant replenishment
- food patch regrowth
- `scripts/run_ant_sandbox_persistence_probe.py`

The colony can now:

- lose individuals
- replace individuals
- continue for longer runs without becoming a frozen fixed population

## What To Run

```text
/Users/qlqwpy/Documents/游乐园/.venv/bin/python -m pytest
/Users/qlqwpy/Documents/游乐园/.venv/bin/python scripts/run_ant_sandbox_persistence_probe.py
```

## What This Supports

This slice supports the narrower claim that the ant-sandbox branch now has a
first bounded persistence loop rather than only a one-shot worker swarm.

## What It Does Not Support Yet

This slice does not yet support claims about:

- optimal long-run colony balance
- stable role differentiation
- disturbance recovery in the colony sense

## Next Practical Step

The next useful extension is:

- tune long-run colony stability
- expose colony persistence in the sandbox observer
- begin disturbance recovery in local space
