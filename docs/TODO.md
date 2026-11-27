# Blakean_Entomology — canonical backlog

Open, owner-local work only. Completed work belongs in `CHANGELOG.md` and Git history.

## Workflowz review — 2026-11-10

No concrete, independently closable improvement survived the bounded evidence review. The packet covers 8 project files and excerpts from 20 source files, including 15 marker-hit files, out of 101 source candidates and 332 files overall. Inspected areas include corpus-pin validation and immutable output writing, CLI error boundaries, native transport/schema refusal, illustrated-output generation, review planning, geometry/visual asset commands, and tests that explicitly reject silent numerical, metadata, image, and taxonomy fallbacks. Marker hits in the supplied tests describe intentional rejecting controls, not production substitutes; archived historical snapshots were excluded from current-production findings.

The Python runtime is recorded exactly as `3.11.17` at `.python-version:1`, but this bounded review does not establish a constraint where changing it to the preferred `3.15.2` is required, nor does it establish that such a change is compatible with the actual lockfile, deployment, fixtures, or pinned Blake/template producers. Accordingly, no runtime-upgrade task is asserted without that evidence. `pyproject.toml` and `uv.lock` contents were not supplied, despite their presence in the inventory; no dependency currency or compatibility claim is made.

Coverage limit: README content was supplied only through line 116, the manuscript and most production modules were not excerpted, and no commands were run. The next evidence-based trigger is a packet containing the complete maintained `pyproject.toml`, `uv.lock`, `docs/public-reproduction.md`, `tests/AGENTS.md`, and full source/probe output for a specifically suspected substitute, pin inconsistency, or validation gap. Re-review then against the stated positive case and rejecting-control contract; do not infer a task from keywords alone.
