# Blakean Entomology

Start with [project status and scoped next work](docs/PROJECT_STATUS.md),
[agent guidance](AGENTS.md), the [article source](docs/manuscript/blakean-entomology.md)
and the [current private paper](Blakean_Entomology.pdf).

The **0.4.0** application prepares its working paper through the actual pinned
[docxology/template](https://github.com/docxology/template) hydration, validation,
PDF and web writers. Its layout uses an authentic Blake cover, three distinct
graphical abstracts on physical pages 2–4, and contents beginning on page 5.
Native counters resolve sections, figures, tables, equations and justified
formalisms. See the [native production contract](docs/manuscript/README.md).

The article examines provision, feeding and collective embodiment while keeping
their symbolic and ethical alternatives active. Baine's *The Scattered Portions:
William Blake's Biological Symbolism* is cited as a bibliographic predecessor;
the actual insect chapter remains unavailable for direct reading. Inspected
Hoagwood criticism, selected Hutchings paragraphs and a copy-specific *Visions*
transcription deepen the argument without creating contextual decisions or
image-reading credit. [Sources and reading limits](docs/research/biological-symbolism.md).

The executable shared core remains Blake 0.4.0 at exact Git
`45171a099a6a658c52ab689501de646a28485653`. Its public repository may receive
later guide-only commits without changing this selected code. The application
retains its fixed corpus, 47-decision study and nine selected original objects.
Its modern reference tree is conditional classification, with no inferred
phylogeny or literary species identity.

[Current verification](research/verification.json) binds the installed source,
tests, separate application/tool coverage, actual native outputs and independent
acceptance. The [dated qualification](research/template-native-20261030.json)
keeps source, runtime, rendered-page and private-publication claims separate.
The new presentation consumes retained analytical exports under their original
producers; it does not claim a fresh composition analysis.

The accepted 37-page 0.3.0 standalone edition, earlier 31-page 0.2.0 edition,
their original qualification/failure receipts and analytical epochs remain
preserved. A new native workflow does not relabel their producing environments.
See [lineage](docs/project-lineage.md), [composition methods](docs/research/composition-analysis.md),
[visual evidence](docs/research/visual-evidence.md) and
[the historical qualification](research/paper-advancement-20261029.json).

Private research on **invertebrate lives and imagery in William Blake**: worm,
fly, spider, emmet/ant, bee, beetle, moth, caterpillar, snail, Polypus and the wider
field of small, creeping, collective and uncertain bodies.

Read the [working article](docs/manuscript/blakean-entomology.md),
[research protocol](docs/research-protocol.md), and
[source intake](research/source-intake-2026-10-28.md). This project adapts the
evidence architecture of [Blakean Federalism](https://github.com/docxology/Blakean_Federalism)
and uses the [shared Blake corpus and methods](https://github.com/docxology/blake).

## Shared-method application

Generic annotation custody, run verification, search, proximity and descriptive
statistics now come from `blake.methods`. The application retains its vocabulary,
contextual policy and literary argument. Its code dependency is pinned separately
from its unchanged historical corpus pin.

The new article compares pooled and equal-work rates, exact-text repetition and
finite versus whole-unit co-occurrence. See [analytical extension](docs/research/shared-methods-analysis.md)
and [current result identities](research/shared-methods-transition.json). The
historical eleven decisions retain their original run. The later contextual
study adds 36 separately authored decisions on that same pinned baseline; see
[the review contract](docs/research/context-review-20261029.md). The retrieval
sensitivity run itself does not adjudicate candidates.

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
- **47 reviewed candidates and 35,992 unreviewed**, combining the unchanged
  eleven-decision seed with 36 new agent-authored decisions. Combined labels are
  2 literal animals, 27 figurative animals, 4 associated, 6 non-animal, 4 editorial
  and 4 uncertain. Twenty-five animal decisions are primary and four remain
  exploratory. The batch is purposive, contains overlapping contexts and repeated
  witnesses, and supplies no prevalence or accuracy estimate. [Context study](docs/research/context-review-20261029.md).
- A source-grounded article draft covering “A Dream,” “The Fly,” “The Sick Rose,”
  “The Human Abstract,” *Thel*, the wine-press inventories, *Four Zoas*, *An Island
  in the Moon*, *Auguries*, and Polypus.

“Entomology” is the research title; the operational scope includes all
invertebrates. Spiders, worms, molluscs and uncertain historical forms retain
their own groups. Taxonomic and rhetorical classifications require context.

## Corpus and methods belong upstream

Blake owns acquisition, recovery, portable schemas and conversion, normalization,
distinct retrieval profiles, generic statistics/proximity/composition/concentration,
hierarchy/layout and run/annotation custody. This application owns its
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

Keep source, Python, environments, caches and temporary files on the mounted
GitVault. Acquire the supported repository lease, then run from the canonical
`Username/docxology/Private/Blakean_Entomology` checkout:

```bash
export GITVAULT_ROOT="$(cd ../../../.. && pwd)"
export UV_PYTHON_INSTALL_DIR="$GITVAULT_ROOT/Local/runtimes/uv-python"
export UV_CACHE_DIR="$GITVAULT_ROOT/Local/caches/uv"
export TMPDIR="$GITVAULT_ROOT/Local/tmp"
export UV_LINK_MODE=copy
uv sync --locked --python 3.11
uv run --locked --python 3.11 python -c 'import pathlib,sys; print(pathlib.Path(sys.prefix).resolve()); print(pathlib.Path(sys.base_prefix).resolve())'
```

Both reported prefixes must resolve on the mounted GitVault. A clone alone
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
analysis and review without loading that stack. The optional acquisition/NLP/vision workflow is qualified separately under Python 3.11.

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

The current 47-decision replay uses
`research/context-review-combined-20261029.jsonl` with the same trusted baseline
run pin and a fresh output path. The command above deliberately demonstrates the
unchanged historical seed. [Current batch and figure commands](docs/research/context-review-20261029.md).

Each decision requires an explicit reviewer and rationale. Animal decisions also
require a verification locator. Wrong-run, duplicate and unknown IDs are refused;
no decision changes an upstream authorship role. A blank decision is unreviewed.
Review summaries record the current application producer separately from the
historical analysis producer.

## Verification and scope

```bash
uv run --locked pytest -c pyproject.toml tests -q
uv run --locked ruff check src tests tools
uv run --locked ruff format --check src tests tools
uv run --locked basedpyright
```

The explicit project configuration and active `tests/` scope keep archived
historical tests outside the current suite. Final branch-aware coverage combines
the installed suite with the declared real publication workflows and checks
application 90% and tools 60% separately; unit-suite-only counters do not establish
that combined gate. Use the [native guide](docs/manuscript/README.md) and its
current qualification receipt for the actual coverage databases and commands.

Tests use real files, a real offline source recovery/import, real CLI invocations,
and corruption/overwrite/role controls. Source and pin overlap guards are tested
with controls that fail when those guards are removed. The shared engine also
rejects a deliberately introduced 1,000-hit cap.

The [reading ledger](research/reading-ledger.json) states actual reading ceilings
and unavailable sources. Images have not received a systematic visual census.
Lexical completeness within the declared snapshot, contextual review completion,
edition reconciliation and iconographic coverage remain separate claims.
[Privacy and custody](PRIVACY.md). Completed engineering and remaining contextual,
image, edition, editorial and scientific work are separated in the
[project status](docs/PROJECT_STATUS.md).
