# AGENTS.md — `tools/`

**Audience:** agents changing the standalone production scripts.

`tools/` holds the standalone, source-bound producers: the composition audit and its figures,
the contextual-review and sensitivity figures, the geometry and visual asset closures, the
reference and source-atlas plotters, and `native_template_worker.py`, which runs the actual
pinned template hydration, preflight, PDF and web writers. Each runs as a script with pinned
inputs — `python tools/audit_composition.py --help` prints the required paths and digests.

The repository contract is [the root guide](../AGENTS.md); the reader's view is
[README.md](../README.md). `docs/style-guide.md` names `tools/render_manuscript.py` as the
admitted rendering call, so where the docs and this file disagree, the docs win.

## Rules

- **Pinned in, pinned out.** A producer takes its inputs by path *and* digest
  (`--atlas` beside `--atlas-sha256`) and refuses to guess what it was given. Adding an input
  means adding its pin, not a default.
- **Portable, and nothing fetched.** These scripts are declared to install nothing and
  download nothing; corpus acquisition is a deliberate act elsewhere in the pipeline, never a
  side effect of rendering a figure.
- **New epochs, new destinations.** A producer never writes over a retained receipt; the
  re-render of an old figure belongs in a new directory
  ([maintenance](../docs/maintenance.md) owns custody).
- **The import direction is one-way.** Nothing under `src/` imports `tools/`; the tests do
  import some of these modules (`tests/test_composition_figures.py`,
  `tests/test_extend_geometry_assets.py`, `tests/test_geometry_assets.py`). A `tools/` module
  may use the package; the package may not reach back into `tools/`.
- **`geometry_asset_contract.py` is a contract, not a CLI.** It joins a new geometry epoch to
  its atlas and copied manuscript graphics, and is imported rather than invoked.
- **The template worker is the rendering boundary.** `native_template_worker.py` runs the
  pinned writers and `native_web.py` carries this repository's CSS extension; a change to
  either changes published bytes, so it needs the root guide's output-qualification rules, not
  just a green suite.
