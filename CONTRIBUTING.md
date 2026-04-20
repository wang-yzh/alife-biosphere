# Contributing

## Purpose

This repository is being developed as an ecology-first artificial biosphere.

The main rule for contributions is simple:

```text
Prefer changes that make the world more like a sustained ecosystem.
Defer changes that only make the mechanism stack more elaborate.
```

## Ground Rules

- Keep the ecology-first north star in mind.
- Do not introduce advanced mechanisms before the base ecology earns them.
- Every meaningful mechanism change should come with at least one test, probe,
  or clearly inspectable event path.
- Do not inflate claims beyond the current evidence.
- Keep generated outputs out of git unless there is a specific reason to commit
  one.

## Development Setup

The repository currently assumes Python 3.11+.

Recommended local commands:

```bash
python -m pip install -e ".[dev]"
python -m pytest
python scripts/run_smoke.py
python scripts/run_ecology_probe.py
```

If you are using the shared local environment from the workspace, the existing
virtualenv also works:

```bash
/Users/qlqwpy/Documents/游乐园/.venv/bin/python -m pytest
```

## Branching

Use short-lived branches off `main`.

Recommended branch name patterns:

- `feature/<topic>`
- `fix/<topic>`
- `docs/<topic>`
- `experiment/<topic>`

Examples:

- `feature/m3-recolonization-summary`
- `fix/movement-cooldown-bug`
- `docs/roadmap-refresh`

## Commits

Prefer small commits with clear intent.

Good commit messages:

- `Add deterministic disturbance hook`
- `Record parent-child birth lineage events`
- `Tighten ecology probe summaries`

Avoid vague messages like:

- `update`
- `misc`
- `fix stuff`

## Pull Request Expectations

Each PR should explain:

1. What changed
2. Why it changed
3. How to inspect or verify it
4. Whether it moves the project toward the ecology-first north star

## Required Checks Before Merging

At minimum:

```bash
python -m pytest
python scripts/run_smoke.py
```

When the change affects ecology behavior directly, also run:

```bash
python scripts/run_ecology_probe.py
```

## Ecology Guard Checklist

Before merging, ask:

- Does this make the world more ecological or just more complex?
- Does it help persistence, turnover, recolonization, lineage history, or
  habitat history?
- Is the change observable in runs, not only in code or metrics?
- Does the evidence support the claim being made?
- Are we accidentally scripting the phenomenon instead of letting it emerge?

## Documentation Rule

Update docs when project state changes materially.

At minimum, consider whether the change requires updates to:

- `README.md`
- `docs/current_build_status_and_next_steps.md`
- `docs/claim_to_evidence_table_v1.md`
- `docs/experiment_ledger_v1.md`
- `docs/ablation_history_v1.md`

## Releases And Versioning

Use lightweight milestone-oriented tags instead of pretending the project is a
stable product already.

Suggested tag style:

- `v0.1.0` for the first public scaffold
- `v0.2.0` for a completed M1 ecology kernel
- `v0.3.0` for the first stable reproduction/lineage slice

Patch releases should be reserved for verification-safe fixes that do not
change the intended milestone meaning.
