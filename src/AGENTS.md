# AGENTS.md — `src/`

**Audience:** agents editing the installable application package.

`src/blakean_entomology/` is the application: it asks this repository's own questions —
invertebrate vocabulary, eligibility, contextual decisions, reference-taxonomy
interpretation — and calls the shared, pinned methods in `blake` for corpus custody,
statistics, proximity and portable schemas. The reusable algorithm belongs upstream; the
question and the domain policy stay here.

The reader's view is [README.md](../README.md). The repository contract is
[the root guide](../AGENTS.md); the documentation map is [docs/README.md](../docs/README.md);
the current software state and the scoped next work are
[project status](../docs/PROJECT_STATUS.md). Read those before this file.

## Rules

- **Upstream the reusable part.** A change to a shared method goes to `blake` and arrives
  here as a qualified pin — the root guide states the rule, and
  [native SDK admission](../docs/native-sdk.md) records the selection this tree currently
  makes. Do not re-implement corpus custody, statistics or schema conversion here.
- **The application owns the question.** Vocabulary, category selection, review policy and
  literary interpretation are this package's. Moving one of those decisions upstream removes
  the boundary the paper rests on ([research protocol](../docs/research-protocol.md),
  [style guide](../docs/style-guide.md)).
- **A result is bound to its producer.** `core.py`, `producer.py`, `geometry_producer.py` and
  `composition_workflow.py` exist to bind an output to the inputs and the producer that made
  it; a new epoch writes to a new destination rather than over a receipt. Custody and
  immutability rules live in [maintenance](../docs/maintenance.md), not here.
- **Text-free exports are a declared boundary.** `atlas_models.py`, `composition_workflow.py`
  and `geometry_io.py` state that their exports carry no corpus text. Cutting a quotation into
  a receipt does not relax that; it removes it.
- **Admission and rendering are separate jobs.** The `publication*.py` modules admit, validate
  and wire — `publication_custody.py` states it holds no rendering engine — while the actual
  pinned template writers run in `tools/native_template_worker.py`. Read the root guide before
  moving that line.
- **The CLI is the entry point.** `pyproject.toml` declares
  `blake-entomology = "blakean_entomology.cli:main"`. Run `blake-entomology --help` for the
  current command set instead of trusting a list in prose, this file included.
- **Lint and types are gates, not advice.** The run block in [README.md](../README.md) covers
  `ruff check`, `ruff format --check`, `basedpyright` and the two coverage reports. Copy it.

## What this directory does not have

No CI that exercises it: `.github/` holds `dependabot.yml` only, so nothing runs the suite
unless a person or a lane does. No coverage floor in `pyproject.toml` either — the floors are
arguments in the verification commands in [README.md](../README.md).
