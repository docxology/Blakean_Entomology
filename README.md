# Blakean Entomology

Private research on **invertebrate lives and imagery in William Blake**: worm,
fly, spider, emmet/ant, bee, beetle, moth, caterpillar, snail, Polypus and the wider
field of small, creeping, collective and uncertain bodies.

Read the [working article](docs/manuscript/blakean-entomology.md),
[research protocol](docs/research-protocol.md), and
[source intake](research/source-intake-2026-10-28.md). This project adapts the
evidence architecture of [Blakean Federalism](https://github.com/docxology/Blakean_Federalism)
and uses the [shared Blake corpus and methods](https://github.com/docxology/blake).

## Shared-method application 0.2.0

Generic annotation custody, run verification, search, proximity and descriptive
statistics now come from `blake.methods`. The application retains its vocabulary,
contextual policy and literary argument. Its code dependency is pinned separately
from its unchanged historical corpus pin.

The new article compares pooled and equal-work rates, exact-text repetition and
finite versus whole-unit co-occurrence. See [analytical extension](docs/research/shared-methods-analysis.md)
and [current result identities](research/shared-methods-transition.json). The
historical eleven decisions keep their original run; the new run has no newly
adjudicated candidates.

```bash
uv run blake-entomology sensitivity --bundle local_data/corpus/v1 \
  --pin research/corpus-pin.json --output analysis_output/sensitivity-new.json
uv run blake-entomology proximity-study --bundle local_data/corpus/v1 \
  --binding research/proximity-binding.json --output analysis_output/proximity-new.json
uv run blake-entomology build-search-workspace --bundle local_data/corpus/v1 \
  --binding research/proximity-binding.json --output analysis_output/workspace-new
```

The first two outputs are text-free, profile-labeled receipts. The workspace
contains full texts and stays private and ignored. Install the optional `recovery`
extra for recovered-source export; ordinary analysis and review use the small
shared core. The development group includes recovery and plotting dependencies
needed by the complete test suite.

## What runs now

- A pinned independent corpus snapshot with **2,067 source units** in three planes.
- **102 search categories and 376 explicit forms**, including historical spelling
  and compound families, plus separately labeled contextual imagery.
- Uncapped retrieval: **36,039 category/source/span candidates**, including
  **2,498 Blake-primary candidates**. These include non-animal senses and are
  not animal or species totals.
- All **918 category/role/plane cells**, including zero-result categories, exact
  source offsets, provenance, denominators and a complete private review queue.
- An explicit seed review of **11 candidates**: eight figurative animal cases,
  two non-animal senses and one uncertain case. Four admitted animal cases remain
  exploratory because their source units are mixed/editorial. **36,028 candidates
  remain unreviewed**; there is no whole-oeuvre completeness verdict.
- A source-grounded article draft covering “A Dream,” “The Fly,” “The Sick Rose,”
  “The Human Abstract,” *Thel*, the wine-press inventories, *Four Zoas*, *An Island
  in the Moon*, *Auguries*, and Polypus.

“Entomology” is the research title; the operational scope includes all
invertebrates. Spiders, worms, molluscs and uncertain historical forms retain
their own groups. Taxonomic and rhetorical classifications require context.

## Corpus and methods belong upstream

Blake owns acquisition, recovery, passage schemas, normalization, the portable
application snapshot and generic lexical engine. This application owns its
vocabulary, review decisions, interpretations and paper. It imports
`blake.applications`, `blake.studies` and `blake.methods`; it does not copy Federalism's SQLite
reader, search code, institutional model or historical acceptance claims.
[Detailed lineage](docs/project-lineage.md).

The [corpus pin](research/corpus-pin.json) binds the exported manifest, source
capture, recovered projection and index. The
[baseline summary](research/baseline-summary.json) contains text-free aggregates;
[baseline run receipt](research/baseline-run.json) binds all private outputs.
The [seed review](research/seed-review.jsonl) and
[its summary](research/seed-review-summary.json) bind decisions to that exact run.
Provider expression and the full review queue remain ignored.

## Run locally

Keep source, Python, environments, caches and temporary files on GitVault. From
the canonical `Username/docxology/Private/Blakean_Entomology` checkout:

```bash
export GITVAULT_ROOT="$(cd ../../../.. && pwd)"
export UV_PYTHON_INSTALL_DIR="$GITVAULT_ROOT/Local/runtimes/uv-python"
export UV_CACHE_DIR="$GITVAULT_ROOT/Local/caches/uv"
export TMPDIR="$GITVAULT_ROOT/Local/tmp"
export UV_LINK_MODE=copy
uv sync --locked --python 3.11
uv run --python 3.11 python -c 'import pathlib,sys; print(pathlib.Path(sys.prefix).resolve()); print(pathlib.Path(sys.base_prefix).resolve())'
```

Both reported prefixes must resolve on the mounted GitVault. Acquire the
supported repository lease for canonical project writes and gates. A clone alone
contains no provider corpus. Restore the exact ignored application bundle from
authorized local custody to replay the baseline:

```bash
uv run blake-entomology analyze \
  --bundle local_data/corpus/v1 \
  --pin research/corpus-pin.json \
  --vocabulary research/vocabulary.json \
  --output analysis_output/replay-001
uv run blake-entomology verify-run analysis_output/replay-001
```

For a deliberately new corpus epoch, prepare a recovered projection in the
upstream Blake environment, then import to a new directory and new pin:

```bash
uv run blake-entomology import-corpus \
  --source ../../Public/blake/blake_data \
  --destination local_data/corpus/new-epoch \
  --pin-output local_data/new-corpus-pin.json
```

The recovered projection is bound to its producer runtime and lock. If those
differ, export from the qualified upstream environment using
`python -m blake.applications export`; loading the portable bundle does not
require the old producer runtime. Never replace the baseline pin silently.
The shared-method package installs a small core. Acquisition, NLP and vision use
Blake's explicit `full` extra. The methods-only profile supports portable-bundle
analysis and review without loading that stack. The full legacy workflow is
qualified separately under Python 3.11.

## Review candidates

The private run contains `hits.jsonl`, `counts.csv`, `summary.json`, `report.md`
and `review-queue.csv`. A completion `run.json` binds every artifact. Existing
output directories and files are refused. Candidate IDs are stable for the
category, source identity, text hash and span. Inspect full source context before
writing separate decisions in the
[JSONL decision format](research/seed-review.jsonl).

You can also copy `review-queue.csv` outside the immutable run directory and edit
that copy in a spreadsheet. Keep the header and evidence columns unchanged; fill
`decision`, `reviewer`, `rationale` and, for animal decisions,
`verification_locator`. Pass the edited `.csv` to the same `--decisions` option
with the exact `--run-sha256`. Blank annotation cells remain unreviewed. Altered
source fields, duplicate or unknown candidate IDs, and partial annotations without
a decision are refused. Never edit the queue inside the original run.

```bash
uv run blake-entomology review \
  --run analysis_output/baseline-v3 \
  --run-sha256 12d0312378460493f894618e6dfc44b36593d8c9f85dfd2cf45f443a09af2633 \
  --decisions research/seed-review.jsonl \
  --output analysis_output/seed-review-replay.json
```

Each decision requires an explicit reviewer and rationale. Animal decisions also
require a verification locator. Wrong-run, duplicate and unknown IDs are refused;
no decision changes an upstream authorship role. A blank decision is unreviewed.
Review summaries record the current application producer separately from the
historical analysis producer.

## Verification and scope

```bash
uv run pytest tests -q --cov=blakean_entomology --cov-branch --cov-fail-under=90
uv run ruff check src tests
uv run ruff format --check src tests
uv run basedpyright
```

Tests use real files, a real offline source recovery/import, real CLI invocations,
and corruption/overwrite/role controls. Source and pin overlap guards are tested
with controls that fail when those guards are removed. The shared engine also
rejects a deliberately introduced 1,000-hit cap.

The [reading ledger](research/reading-ledger.json) states actual reading ceilings
and unavailable sources. Images have not received a systematic visual census.
Lexical completeness within the declared snapshot, contextual review completion,
edition reconciliation and iconographic coverage remain separate claims.
[Privacy and custody](PRIVACY.md).
