# Blakean Entomology

Private research on **invertebrate lives and imagery in William Blake**: worm,
fly, spider, emmet/ant, bee, beetle, moth, caterpillar, snail, Polypus and the
wider field of small, creeping, collective and uncertain bodies. “Entomology”
is the research heading; the scope includes all invertebrates.

Start with [project status](docs/PROJECT_STATUS.md),
[agent guidance](AGENTS.md), the [article](docs/manuscript/blakean-entomology.md),
the [current private working-draft PDF](Blakean_Entomology.pdf) and
the [documentation map](docs/README.md).

## Current application and paper

Entomology **0.8.0** selects public Blake **0.7.0**, exact Git
`263d7c83abe6f1309a64af3285a683c1b7672269`, through
[pyproject.toml](pyproject.toml) and [uv.lock](uv.lock).
Blake supplies reusable corpus custody and methods. This application owns
vocabulary, query-channel policy, contextual judgments, conditional reference
mappings, domain graphics, image readings and literary argument.
Federalism is an architectural sibling, with no runtime dependency.
[Lineage and responsibility](docs/project-lineage.md).

The new [original-codepoint geometry](docs/research/interval-geometry.md)
separates candidate records, occupied text, overlap depth, overlapping pairs
and documented reading windows. It retains every source facet and zero-hit
unit. Two analytical figures show source support and the bounded exposure of
existing reviewed candidates. The analysis creates no new decision, animal
attestation, complete-work reading or image inspection.

The paper develops provision, feeding, webs, prisons and collective embodiment
through copy-specific contexts and live alternatives. Rodney M. Baine's
*The Scattered Portions: William Blake's Biological Symbolism* is cited as a
verified bibliographic predecessor. **Its relevant chapter remains unread and
unavailable; its formal title and boundaries remain unverified.**
The complete Hoagwood review and selected Hutchings material have their own
reading ceilings. [Scholarship and access record](docs/research/biological-symbolism.md).

Current manuscript production uses the actual pinned
[docxology/template](https://github.com/docxology/template) hydration,
validation, formalism/cross-reference filters and PDF/web writers. Physical
page 1 is an authentic complete-recto Blake cover; distinct graphical abstracts
occupy pages 2–4, followed by contents on page 5.
The [native contract](docs/manuscript/README.md) and
[host SDK profiles](docs/native-sdk.md) bind each new edition independently.
The current 45-page candidate replaces the three schematic opening graphics
with quotation-led arguments using complete impressions of *The Fly*, *A Dream*
and *Thel*. A word/context/lineage table and clearer reference/atlas figures keep
historical names, grammatical uses and conditional modern classification
distinct. The abstracts and interpretive captions are revised. The
[illustrated-argument contract](docs/research/illustrated-arguments.md) closes
quotation/image joins and their real refusing controls. Native production has
completed. The exact 45-page PDF/HTML passed independent working-draft output review, and both dated and current PDFs were copied byte-for-byte to Downloads. Source review's test-size finding was closed by an AST-preserving split and 20 passing affected tests; this owner correction is not fresh independent software reapproval. Publication and exact scopes are recorded in
[project status](docs/PROJECT_STATUS.md). The accepted 44-page 0.7 edition and
its earlier correction verdicts remain historical evidence.

The retained 40-page 0.4.0 native edition and earlier standalone editions keep
their original [native qualification](research/template-native-20261030.json),
[analytical producers](research/paper-advancement-20261029.json) and failures.
A later SDK or documentation update does not relabel those bytes.

## Corpus and review denominator

- **2,067 retained source units**, with source-author, role and plane distinctions.
- **102 search categories / 376 explicit forms**, including historical spelling
  and compound families.
- **36,039 category-source-span candidates**, including **2,498** in the declared
  Blake-primary reading scope. These are not animal, species or unique-scene totals.
- All **918 category/role/plane cells**, including zeros, original offsets,
  denominators and the complete private queue.
- **47 reviewed / 35,992 unreviewed**, retaining the eleven-decision seed plus the
  additive 36-decision study. The recorded labels are 2 literal animal,
  27 figurative animal, 4 associated, 6 non-animal, 4 editorial and 4 uncertain.
  [Contextual review](docs/research/context-review-20261029.md).
- Nine selected original objects with bounded image readings.
  [Visual witnesses](docs/research/visual-evidence.md). The wider image inventory
  remains unreviewed.

The purposive review contains overlapping windows and repeated witnesses; it
supplies no prevalence, classifier accuracy, independent-sample or
specialist-consensus estimate. A reference lineage is conditional modern
classification, not a sequence-inferred phylogeny or a species identification
in Blake. [Research protocol](docs/research-protocol.md).

The final canonical normal-installed gate passed **464 tests**, with **90.80% application / 67.33% tools** suite-only statement/branch coverage. Typing, lint, formatting and dependency checks pass. [Exact current qualification](research/visual-installed-20261102.json).

## Run locally

Keep source, environments, both Python prefixes, caches and temporary files on
mounted GitVault. Use the existing external Python 3.11.17 runtime and supported
repository admission. Bind external `TMPDIR`, outer `TMPPREFIX`,
`UV_CACHE_DIR` and `UV_LINK_MODE=copy` before source-work commands.

~~~bash
uv sync --locked --python 3.11.17
uv run --locked python -c 'import pathlib,sys; print(pathlib.Path(sys.prefix).resolve()); print(pathlib.Path(sys.base_prefix).resolve())'
~~~

Both prefixes must resolve on GitVault. The default development group includes
the plotting/recovery dependencies needed by the complete tests. A clone contains
source and authored research, not the ignored provider corpus. Restore the exact
authorized bundle to replay the baseline:

~~~bash
uv run --locked blake-entomology analyze --bundle local_data/corpus/v1 \
  --pin research/corpus-pin.json --vocabulary research/vocabulary.json \
  --output analysis_output/replay-new
uv run --locked blake-entomology verify-run analysis_output/replay-new
~~~

A deliberately new capture needs a new upstream recovery/export, portable import,
pin and unused destination. Preserve the old producer and
[corpus pin](research/corpus-pin.json). Blake's active acquisition/NLP/vision
capabilities use its separately qualified `full` extra; portable methods do not
load that stack.

## Geometry, composition and review

For geometry, obtain the request SHA from the independently retained admission
record and the documented-window file from its bound custody. Use an unused
output epoch:

~~~bash
uv run --locked blake-entomology geometry \
  --request research/geometry-study-20261101.json \
  --request-sha256 "$GEOMETRY_REQUEST_SHA256" \
  --bundle local_data/corpus/v1 --run analysis_output/baseline-v3 \
  --decisions research/context-review-combined-20261029.jsonl \
  --windows "$DOCUMENTED_WINDOWS" --vocabulary research/vocabulary.json \
  --output analysis_output/geometry-new --figures
~~~

[The geometry contract](docs/research/interval-geometry.md) defines original
Python-codepoint coordinates, source-local grouping, multiplicity and the
difference between missing reading-window custody and zero exposure.
Retained [composition](docs/research/composition-analysis.md),
[proximity and sensitivity](docs/research/shared-methods-analysis.md) outputs
keep their original producers and distinct denominators.

The [request-pinned planner](docs/research/review-planning.md) selected a blank
25-candidate workload from 2,498 scoped hits, excluding 37 existing scoped
decisions. Planning adds no adjudication. For authored review, copy the immutable
queue and preserve its header and evidence columns. Animal decisions require a
verification locator as well as reviewer and rationale:

~~~bash
uv run --locked blake-entomology review \
  --run analysis_output/baseline-v3 \
  --run-sha256 12d0312378460493f894618e6dfc44b36593d8c9f85dfd2cf45f443a09af2633 \
  --decisions research/context-review-combined-20261029.jsonl \
  --output analysis_output/context-review-replay-new.json
~~~

Blank cells remain unreviewed. Wrong-run, duplicate/unknown IDs, altered source
fields and partial annotations refuse. A decision never changes source authorship.

## Verification and scope

~~~bash
uv run --locked pytest -c pyproject.toml tests -q
uv run --locked ruff check src tests tools
uv run --locked ruff format --check src tests tools
uv run --locked basedpyright
~~~

The current normal-installed suite passed **464 tests**. Separate
statement-and-branch coverage is **90.80% application / 67.33% tools**, against
90% / 60% floors. The explicit project configuration keeps historical test
trees outside collection. Full package typing and the changed-tool scopes have
their own records; the default strict command covers `src`.

The [verification index](research/verification.json) and
[current-source index](research/current-source.json) locate published
qualification records. Unit coverage, real analytical production, actual native
writers and output acceptance remain separate evidence; no old counters or
one-shot grant are reassigned. New paper bytes require fresh PDF/HTML inspection.

Remaining work includes contextual adjudication, edition reconciliation, the
image inventory, direct Baine access, specialist criticism, accessibility and
venue decisions. [Scoped tasks](docs/PROJECT_STATUS.md) give useful next units.
Private-main publication supplies no public item-level rights clearance.
[Privacy and custody](PRIVACY.md).
