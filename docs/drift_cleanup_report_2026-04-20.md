# Drift Cleanup Report 2026-04-20

## Purpose

This report records the first documentation cleanup pass performed in the
working-copy library.

The original project was backed up before edits.
Cleanup work was then applied only in the copied library.

## What Was Audited

The audit focused on:

- entry-point documents
- broken or stale document references
- status summaries that no longer matched the actual library
- historical notes that could be mistaken for current project contracts

## Drift That Was Corrected

### 1. Entry-map drift

Problem:

- the library had many strong documents, but no dedicated `docs/` entry map

Fix:

- added `docs/README.md` as the documentation library index
- added `document_catalog_v1.md` as a structured whole-library catalog

### 2. Re-entry summary drift

Problem:

- `README.md` and `current_build_status_and_next_steps.md` did not provide a
  single shared entry path for the cleaned library
- `current_build_status_and_next_steps.md` used an exact document count that
  would drift again immediately after cleanup

Fix:

- added `docs/README.md` to the re-entry path
- removed the brittle exact markdown-file count from the active summary

### 3. Library-inventory drift

Problem:

- `library_inventory_and_gap_map_v1.md` still described several document types
  as missing even though they now exist:
  - unified bibliography
  - terminology index
  - experiment ledger
  - negative-results ledger
  - claim-to-evidence table
  - ablation history
  - unresolved-question status separation

Fix:

- rewrote those sections so they now describe coordination and population gaps
  rather than falsely claiming the documents do not exist

### 4. Historical follow-up drift

Problem:

- `literature_backlog_v1.md` referenced three expected follow-up documents that
  were never created as standalone files

Fix:

- replaced those placeholder references with the integrated documents that
  later absorbed the same role

### 5. Historical-note drift

Problem:

- `artificial_life_positioning_from_classic_papers.md` and
  `repository_architecture_v0.md` could be misread as current-control
  documents even though both are now historical
- `world_design_v0.md` and `build_plan_v0.md` were still important historical
  files, but they did not yet identify themselves clearly as superseded
  baselines

Fix:

- added explicit status notes that mark them as historical and point readers to
  the current controlling documents

## Remaining Intentional Historical Material

The cleanup pass did not rewrite every early document into `v1` form.

The following files remain intentionally historical:

- `artificial_life_positioning_from_classic_papers.md`
- `world_design_v0.md`
- `build_plan_v0.md`
- `repository_architecture_v0.md`

They are still useful for provenance and design lineage.
They are not the current implementation contract.

## Ongoing Rule

If a future document introduces a new project-wide control role, it should also
be added to:

- `docs/README.md`
- `docs/document_catalog_v1.md`
- `README.md`
- `current_build_status_and_next_steps.md`

That is the minimum coordination rule needed to keep entry-point drift small.
