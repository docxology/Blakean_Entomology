# Blakean Entomology

Research on **invertebrate lives and imagery in William Blake**: worm,
fly, spider, emmet/ant, bee, beetle, moth, caterpillar, snail, Polypus and the
wider field of small, creeping, collective and uncertain bodies. “Entomology”
is the research heading; the scope includes all invertebrates.

Start with [project status](docs/PROJECT_STATUS.md),
[agent guidance](AGENTS.md), the [article](docs/manuscript/blakean-entomology.md),
the [published 1.0.0 working-paper PDF](Blakean_Entomology.pdf) and
the [documentation map](docs/README.md).

## Public 1.0.0 edition

Entomology **1.0.0** selects public Blake **0.7.0**, exact Git
`263d7c83abe6f1309a64af3285a683c1b7672269`, through
[pyproject.toml](pyproject.toml) and [uv.lock](uv.lock). Blake owns reusable
corpus custody and methods; this application owns its vocabulary, contextual
judgments, conditional classification, domain figures and literary argument.
Federalism remains an independent sibling, with no runtime dependency.
[Lineage and responsibility](docs/project-lineage.md).

The 42-page native candidate has an authentic whole-recto Blake cover,
three distinct graphical abstracts on physical pages 2–4, and contents on page 5.
The Fly joins injury and reciprocal questions to the full review denominator;
A Dream distinguishes the emmet, glow-worm and beetle's offered capacities;
Thel sets the Worm–infant comparison beside measured lexical weighting effects.
Complete original impressions, exact quotations, locators and counterreadings
remain visible. The 11 mm margins and 4 mm footer spacing retain 10-point body
type. The actual pinned [template writers](docs/manuscript/README.md) own
hydration, citations, numbering and PDF/HTML production.

The author-approved 1.0.0 edition is published at [Zenodo](https://doi.org/10.5281/zenodo.23900583) and [GitHub v1.0.0](https://github.com/docxology/Blakean_Entomology/releases/tag/v1.0.0). [Publication facts](publication.json) bind the exact approved PDF; [distribution terms](LICENSE-PAPER.md) preserve authored and third-party rights. Publication does not establish specialist scientific acceptance.

The [geometry contract](docs/research/interval-geometry.md) separates records,
occupied text, overlap and documented reading windows. No corpus, vocabulary,
review label, source identity or analytical input changed in this revision.
Rodney M. Baine's *The Scattered Portions: William Blake's Biological Symbolism*
remains cited as a verified bibliographic predecessor; its relevant chapter
remains unavailable and unread. [Reading and access limits](docs/research/biological-symbolism.md).

The normally installed Python 3.11.17 candidate passes **474 tests**,
strict typing, Ruff and formatting. Separate suite-only statement/branch
coverage is **91.07% application / 67.33% tools**; all 45
application and 163 exact SDK runtime/resource members match their sources.
Native, independent review, canonical consumer and delivery evidence remain
separate in the [current qualification](research/review-candidate-1.0.0.json) and [project status](docs/PROJECT_STATUS.md).
The earlier 45-page 0.8.0 edition and failed footer attempt retain their own
bytes and receipts; this revision does not rename an analytical producer.

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

The current normal-installed candidate passes **474 tests**. See the [current qualification](research/review-candidate-1.0.0.json) for exact source, runtime, output and independent-review bindings.

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

The current normal-installed suite passed **474 tests**. Separate
statement-and-branch coverage is **91.07% application / 67.33% tools**, against
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
Public distribution covers only the selected author-approved payload.
[Privacy and custody](PRIVACY.md).

## Related projects and editions

| Project | GitHub | Zenodo |
|---|---|---|
| Corpus and shared methods | [blake](https://github.com/docxology/blake) | [Paper 0.5.0](https://doi.org/10.5281/zenodo.23921364) |
| Invertebrate readings and concordance | [Blakean Entomology](https://github.com/docxology/Blakean_Entomology) | [1.0.0](https://doi.org/10.5281/zenodo.23900583) |
| Political argument and institutional models | [Blakean Federalism](https://github.com/docxology/Blakean_Federalism) | [1.0.0](https://doi.org/10.5281/zenodo.23900617) |

[Publication and reproduction verification](docs/public-reproduction.md) records the completed publication and separates
immutable release inputs from later documentation and remaining research.
