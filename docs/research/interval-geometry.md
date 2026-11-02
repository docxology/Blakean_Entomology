# Matched text and documented reading windows

This application measures original-source support of an existing candidate run
without rematching its vocabulary or adding contextual decisions.
[The research protocol](../research-protocol.md) defines animal judgments;
[the style guide](../style-guide.md) defines how to present these measurements.

## Coordinates and measures

Every span uses half-open integer coordinates `[start,end)` in the original
`Passage.text`, counted by Python codepoints. The frame is neither UTF-8 bytes,
grapheme clusters, normalized match text nor an illuminated-page area. Original
source slices, hashes, authorship, role and plane must still reconcile.

Intervals are grouped by passage ID before any set operation. Identical text in
different captured sources stays in separate frames. Public
[Blake interval methods](https://github.com/docxology/blake/blob/263d7c83abe6f1309a64af3285a683c1b7672269/docs/methods/intervals.md)
supply union, measure, depth support, intersection and record-pair counting.
This application supplies source grouping, channel eligibility, the reading
window policy and interpretation.

| Measure | Unit and meaning |
|---|---|
| Candidate records | Category-source-span identities, retaining category multiplicity |
| Summed codepoints | Sum of individual match lengths, including repeated coverage |
| Union codepoints | Original positions occupied by one or more matches |
| Overlap codepoints | Positions occupied by at least two match records |
| Excess codepoints | Summed lengths minus union length; multiplicity beyond the first |
| Overlapping pairs | Unordered pairs of distinct records with positive-length intersection |

The last three quantities differ. Three identical two-codepoint records have
union 2, depth-at-least-two area 2, excess 4 and three overlapping pairs.
Adjacent half-open intervals share no occupied position. Never add offsets
across different sources or call a category sum an animal count.

## Cohorts and weighting

Facets are the joint source role, plane and author identity. Every captured unit
and zero-hit unit remains in its declared facet. Blake-primary eligibility is
exactly `primary / reading / william-blake-1757-1827`; XML and mixed/editorial
material are not promoted into it.

For a source, occupancy is union support divided by original codepoint length.
Pooled occupancy divides total support by total length. Equal-unit occupancy
averages the source ratios, including zeros. Equal-work occupancy first averages
source ratios within each recorded work group and then averages those group
means. Exact fractions are used before the serialized floating values.
These are explicit weighting policies, not independent witnesses or estimates
of prevalence in Blake's complete oeuvre.

The four channels remain `name_family`, `broad_label`, `associated` and
`motion`. Channel unions can intersect and are therefore unstacked.
The source-local intersection matrix retains all channel pairs and zeros.

## Reviewed identities and reading exposure

The original decision ledger still has **47 reviewed and 35,992 unreviewed
candidates out of 36,039**. Identity labels partition the candidate records.
Their occupied text can overlap because different records may share positions.

The documented-window file supplies 36 retained reading events on 23 source
units for the additive study. The geometry report includes all 28 units with
reviewed candidates. Eleven reviewed identities lack documented-window
coordinates in this custody object: their reading exposure is **unavailable**,
not zero. A subtotal of documented windows is neither all reading nor measured
attention, comprehension or whole-work coverage.

The source-footprint figure retains all source facets, primary weighting and
the four channels. The review-exposure figure shows reviewed candidate support,
documented window support and unavailable custody for every reviewed unit,
with explicitly selected same-source window pairs. Figure choices are request
inputs rather than an undisclosed search for striking examples.

## Production and manuscript integration

[The tracked request](../../research/geometry-study-20261101.json) pins the
corpus, original run, decisions, windows, vocabulary, SDK and illustrative
selections. Hold its byte SHA independently before invoking the
[`geometry` CLI](../../src/blakean_entomology/geometry_cli.py).
The [README command](../../README.md#geometry-composition-and-review) gives all
required options. Output must be a new ignored epoch.

The completion receipt binds all analytical files, producer sources, exact
input hashes, runtime prefixes and the installed SDK when selected. A
source-only request records no installed claim. Current normal production is
`analysis_output/geometry-installed-20261101-01`; its original data, two
PNG/SVG/PDF figures and plotting/font receipts remain together.

[The asset extension tool](../../tools/extend_geometry_assets.py) verifies the
retained parent manifest, complete geometry epoch and atlas joins before
creating a new additional-assets closure. Request, report and receipt hashes
are explicit caller inputs. Captions are derived from those bound data.
Prior assets and analytical producer identities remain byte-for-byte parents;
an extension adds no original-image inspection.

Preparation verifies this closure before output, and current native staging
uses [schema 3](../native-sdk.md). A changed input, source, selection or method
requires a new epoch. Wrong pins, inconsistent source slices, contradictory
memberships, changed/missing/extra files, symlinked or occupied outputs and
crossed native profiles must refuse. Software, analytical production, actual
template writers, complete page/browser acceptance, scholarly criticism and
delivery remain separately qualified.
