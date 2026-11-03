# AGENTS.md — `tests/`

**Audience:** agents adding or changing tests.

One module per area: `test_geometry*` for original-codepoint geometry and its assets,
`test_composition*` for the composition epochs and their figures, `test_native_*` for the
pinned template/SDK path and its PDFs, `test_review_planning*`, `test_sensitivity*`,
`test_atlas`, `test_casebook`, `test_taxonomy`, `test_visual_*`, `test_workflows` and
`test_expanded_manuscript` for the manuscript. `pyproject.toml` collects `tests` only, so
fixtures under `research/history/` are deliberately outside collection.

## Rules

- **The gate is the block in [README.md](../README.md), not a pytest default.** It runs pytest
  with branch coverage over the package *and* `tools`, then two separate coverage reports with
  their own floors (`--fail-under 90` for the application, `--fail-under 60` for the tools),
  then ruff and basedpyright. The floors live in those commands; `pyproject.toml` sets only
  `testpaths` and `-ra`.
- **A workflow without a rejecting control is half a test.** The root guide's rule: run the
  affected real workflow with a positive case *and* its control. A test that can only pass is
  the thing this repository keeps replacing.
- **Some tests exercise `tools/` directly** — `test_composition_figures.py`,
  `test_extend_geometry_assets.py`, `test_geometry_assets.py` — so a tool change can break the
  suite while the package is untouched, and a package-only run does not clear a tool.
- **No mock framework.** As of 2026-11-03 `grep -rn 'unittest.mock\|MagicMock' tests/` finds
  nothing: the tests build real inputs and run the real writers. Keep it that way.
- **A documentation edit is not a test edit.** The root guide is explicit that documentation
  needs link, command and evidence-claim review rather than a test that pins prose. Do not add
  a test to freeze a sentence in a guide.

## What is absent here

No `tests/conftest.py` and no shared fixture module — each module builds what it needs. No CI:
`.github/` holds `dependabot.yml` only, so this suite runs only when a person or a lane runs
it, and a green run is evidence of that run and no other.
