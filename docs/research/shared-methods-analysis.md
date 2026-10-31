# Shared-methods analytical extension: evidence and interpretation boundaries

**Historical analytical migration note.** The preliminary recipes and seed reading ceilings below belong to their named producer epochs. The frozen [seed ledger](../../research/reading-ledger.json) recorded Perkins as unread; the later [additive reading ledger](../../research/reading-ledger-expansion-v1.json) records the complete article reading without rewriting that seed. Use [project status](../PROJECT_STATUS.md), [composition qualification](composition-analysis.md) and [current review planning](review-planning.md) for current installed workflows. Source overlays in the old recipe are not installed-consumer qualification.

This note records a private, descriptive extension of the existing lexical
experiment. The source corpus, vocabulary, historical baseline receipts and seed
review were not changed. The manuscript supplement is
`docs/manuscript/sensitivity-supplement.md`; it extends §§3 and 8 of
`docs/manuscript/blakean-entomology.md` while referring back to the already bounded
readings in §§4–7. It does not credit additional reading or image inspection.

## Inputs and identities

The preliminary inputs are:

- `analysis_output/shared-methods-preliminary/sensitivity.json`: typed NFKC
  sensitivity receipt with complete counted inventory and all category summaries.
- `analysis_output/shared-methods-preliminary/proximity.json`: typed literal
  proximity receipt with the explicit projection pin, request grid and facets.
- `research/reading-ledger.json`: unchanged reading ceilings. In particular,
  Schwartz remains abstract-only, Perkins remains located but unread, Dauphin
  remains selected paragraphs, and Goode remains selected opening sections.
- `research/seed-review.jsonl`: historical annotation evidence; its run identity
  is not repinned to these new analysis receipts.

The paired bundle and projection pins are validated programmatically, not copied
from prose as executable inputs. Exact input-file hashes and the figure-generator
hash are written into the generated `summary.json`. The preliminary receipts name
application producer `0f548028120b7977a6323b0f6b7a4509ac1504f99045b2b9d515737653296194`.
A later producer epoch must be recorded as a new input pair; historical receipts
and annotations must not be rewritten to imitate it.

## What the figure generator checks

`tools/build_sensitivity_figure.py` reads both files as regular, nonsymlinked
inputs and parses the application receipt models. It requires the declared NFKC
and literal profile descriptions, consistent Unicode/runtime metadata, the same
portable manifest hash and captured/projection/index hashes, and one application
producer epoch. Public-code and Archive-data commits have different meanings and
are not equated.

The complete sensitivity inventory is recomputed using shared
`analyze_inventory`; all stored strata, query counts, rates, exact-text summaries
and co-occurrences must agree. The generator checks every literal row against the
same per-work and total eligible source-unit counts. The shared proximity model
reconciles facet tokens, rates, term totals, increasing windows and monotonicity.
The private figure requires exactly its declared four pairs and five scopes.
It does not substitute a numeric width for whole-unit scope.

The total scanned-bundle count is retained from the typed proximity receipt;
these two aggregate files alone cannot independently reconstruct all 2,067
source members. The upstream workflow verified the pinned bundle. Figure-level
validation checks complete primary count inventory and paired identities, rather
than claiming a second raw-corpus replay.

Before plotting, output is required to be a new location below the current
private project's `analysis_output`. Existing destinations, links and traversal
are refused. Publication writes a complete PNG and then the aggregate
`summary.json`. This summary includes all eight selected query summaries, every
category changed by exact-text grouping, both input hashes, generator hash and
the text-free proximity receipt. It contains no passage bodies, source contexts,
provider images or newly authored review decisions.

## Historical preliminary reproduction (source overlay)

Run from the private project, using the admitted external environment and
stage/public package binding used to create the receipts. Keep temporary files,
matplotlib configuration and the uv cache on GitVault. For example, with
`PYTHONPATH` already set to the intended public source and private `src`:

```bash
export MPLCONFIGDIR="$PWD/analysis_output/.matplotlib-cache"
uv run --no-project --python "$EXTERNAL_PYTHON" python tools/build_sensitivity_figure.py \
  --sensitivity analysis_output/shared-methods-preliminary/sensitivity.json \
  --proximity analysis_output/shared-methods-preliminary/proximity.json \
  --output analysis_output/shared-methods-figure-new
```

The generator uses the existing environment; this task installs no dependencies.
The private figure layout and selected categories are application policy. Count
aggregation and validation call the public methods; there is no new private
counting engine. The PNG is 340.36 by 241.3 mm at 180 dpi. It should be inspected at
its actual manuscript placement size before publication.

## Findings and limits

The primary inventory contains 199 units in 33 work groups. Its NFKC denominator
is 644,247 tokens. Exact complete-text grouping retains 198 units and 641,306
tokens, eliminating one 2,941-token duplicate of *America a Prophecy*:
`archive:america.n` and `archive:america.n--878c90904184`. Across all 102 categories,
2,498 candidate spans become 2,489. Five category counts change: `crawl` 26→25,
`flight_verbs` 156→153, `insect` 14→13, `mussel` 13→12, and `wing` 532→529.
The selected eight counts are unchanged, but their rates change with the token
denominator. This weak exact-text effect does not establish copy independence.

Pooled and equal-work rates describe different weightings of the captured
inventory. Largest-group shares are also copy-retaining; `thel` contributes
171/468 worm candidates and 16/20 butterfly candidates, `songsie` contributes
103/183 fly candidates, and `milton` contributes 40/73 polypus candidates.
These ratios motivate work/copy inspection without asserting distinct scenes,
authorial intent, species identity, or statistical independence.

The literal denominator is 644,245 original word tokens. The raw singular pairs
are `worm + fly`, `bee + flower`, `spider + web` and `emmet + grass`. In that order,
matched units at 8 words are 4, 0, 13 and 27; at 32 words they are 28, 0, 13 and 27;
at whole-unit scope they are 66, 30, 33 and 36. The finite widths are 8, 16, 32 and
64 words, followed by a distinct whole-unit category. Counts are copied source
units, not independent reading positions. Neither the literal singular searches
nor the broader NFKC vocabulary establish recall for unnamed, differently spelled,
visual or absent-source animal discussion.

## Guard and visual evidence

`tests/test_sensitivity_figure.py` uses real synthetic receipt files and real CLI
subprocesses. Wrong corpus identity, mislabeled profile, altered aggregate
inventory, and a valid one-unit inventory paired with a two-unit proximity
receipt all fail before output publication. Positive PNG/signature and summary
checks, overwrite preservation, and private-output confinement are included.

The first real preview is `analysis_output/shared-methods-figure-01/sensitivity.png`.
Its panels were visually inspected: rate bars and concentration labels are legible;
all 20 proximity cells have visible integer labels; the whole-unit column has a
separate boundary; both token denominators and the exact-text unit/token counts
are visible. A final generator revision receives a new output directory and its
own hash-bound summary. Figure inspection is not manuscript-page acceptance.

The final generator-bound preliminary render is
`analysis_output/shared-methods-figure-02/sensitivity.png`, with paired
`summary.json`. Its stored generator hash matches the current script. The second
render was inspected again after the final generator edits; all panel labels,
integer cells and denominator captions remain legible with no overlap or clipping.

An additional strict-all check of the standalone plotting script retains
Matplotlib's incomplete public `**kwargs` stub diagnostics. The application
source type gate remains separate and clean; this note does not claim that the
plotting script passes an unsuppressed strict-all type check. No source-level type
ignores or project-wide diagnostic suppression were introduced.


The retained article uses the independently copied installed receipts in
`analysis_output/shared-methods-v4/` and the portrait print figure in
`analysis_output/shared-methods-figure-v5/`. The earlier preliminary renders above
remain historical evidence. The current figure is 170.18 by 228.6 mm at 180 dpi;
its generator and input hashes are recorded in `research/shared-methods-results.json`.
