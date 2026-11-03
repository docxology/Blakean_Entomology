# Entomology authoring and evidence guide

Apply the [shared Blake conventions](https://github.com/docxology/blake/blob/263d7c83abe6f1309a64af3285a683c1b7672269/docs/style-guide.md)
for method profiles, source roles, immutable epochs, count units and evidence
claims. [Project status](PROJECT_STATUS.md) identifies the current Entomology
edition and its exact Blake 0.7.0 source selection.
This application-specific addendum owns biological vocabulary, source grouping, documented
reading-window policy and literary interpretation. The retained 0.4.0 paper
keeps SDK `45171a099a6a658c52ab689501de646a28485653` and its original
native qualification. See [project status](PROJECT_STATUS.md) for each current
source, software, native and delivery scope.

## Biological language

Use *invertebrate* for the scope and *Insecta* only for the reference class.
Keep spiders, myriapods, molluscs, annelids, flatworms, nematodes, cnidarians and
sponges visible. “Invertebrates,” “worms,” “vermin,” life stages and historical
“zoophytes” are not interchangeable clades. No species identity follows from a
literary name. A reference lineage and a sequence-inferred phylogeny are different
objects. No figure here encodes time, branch lengths, support values or a claim
that every displayed grouping is monophyletic.

Record `resolved_lineage`, `broad_group`, `ambiguous_mapping`, `non_taxon` and
`outside_scope` explicitly. Even a resolved lineage means a conditional modern
animal sense, not an adjudication of Blake's referent. State rival historical,
metaphorical, medical and material senses. Body parts, products, verbs and actions
do not become taxa. Preserve source spelling, including *Catterpiller*, and query
variants such as *emmett* without manufacturing an attestation.

## Reading and interpretation

Begin with the complete available local context: speaker, predication, setting,
sequence and ending. Cite work, copy, Archive object and physical XML line IDs;
an Archive object number need not equal a printed or Erdman plate number. Keep
primary transcription and modern catalog description separate. Give full-poem
credit only after checking every verse line in the captured short poem. A
complete transcription reading is neither image inspection nor whole-book credit.

Separate what the text says from the proposed reading and a live alternative.
An offered route is not a narrated successful rescue; an animal analogy is not
evidence of animal cognition; a plant's sting is not an insect identification.
Do not add contextual review decisions through casebook prose. Candidate review
requires its own original run pin and occurrence identity.

## Figures and count syntax

Use “category-source-span candidates,” “matched retained source units,” or
“recorded work groups” beside numbers. Never label category sums “animals,”
“species,” or unique literary scenes. Print zero cells and source eligibility.
State NFKC and literal denominators separately. Work-balanced coverage averages
within-work matched-unit fractions, including zero-match groups; work-balanced
rates omit undefined zero-token rates. Exact whole-text grouping does not remove
poems embedded in nonidentical copies.

Solid reference branches show compressed captured ancestry. Separate lexical
associations spatially and encode ambiguity in both line style and words, with
colour as a secondary cue. State incomplete branch sampling and nonexhaustive
alternatives. Captions come from the bound atlas and reference, never hand-entered
counts. Keep PNG and SVG plus their generator, data and source hashes.

## Original-codepoint support and reading exposure

Use the [geometry contract](research/interval-geometry.md). Measure half-open
integer intervals in original `Passage.text` Python codepoints. Do not substitute
UTF-8 bytes, grapheme clusters or normalized matcher coordinates. Group by
original source before interval operations and retain all source facets,
zero-hit units and repeated copies.

Distinguish candidate records, summed match lengths, occupied union, support at
depth two or more, multiplicity excess and overlapping record pairs. Their
denominators and meanings differ. Unstack overlapping channels and label the
within-source intersection explicitly. Pooled, equal-unit and equal-recorded-work
occupancy are separate weighting policies, with zeros retained.

A contextual decision is an identity-bound judgment. A documented reading
window is bounded custody of text exposure, not measured attention or complete
reading. Show missing window coordinates as unavailable, never as zero.
Overlapping windows are not independent readings. Geometry creates no new
decision, animal attestation, original-image inspection or whole-work credit.
Captions and numerical labels must derive from the bound report.

## Manuscript preparation

Use the [native render guide](manuscript/README.md). Hydrate declared data tokens
with pinned inputs, then call `tools/render_manuscript.py` with an admitted
request and explicitly selected compatible template checkout/runtime. The
request pins preparation, analyses, authentic recto/provenance, configuration,
preamble and project web stylesheet. Verify resolved YAML values and actual
PDF metadata as well as Markdown token substitution.

Keep cover, graphical abstracts and TOC choices in source configuration and
preamble. Verify physical pages rather than relying on printed counter resets.
The three current graphical arguments pair complete Fly, Dream and Thel
impressions with copy-specific quotations, proposed readings, local alternatives
and biological limits. Follow [illustrated arguments](research/illustrated-arguments.md)
for the actual selection and caption contract. The seven-case casebook and
analytical weighting/classification figures remain distinct evidence objects.
An additional prose reading creates no casebook or adjudication record.

Use native `sec:`, `fig:`, `tbl:` and `eq:` labels and Pandoc bracket
references. Body headings have no manually typed number prefixes. Definition
and proposition Divs use native classes and stable `def:`/`prop:` IDs. The
framework assigns all formalism numbers. Use explicit math delimiters, including
`\lvert...\rvert` for cardinality. One unnumbered References heading and
`refs` target serve both editions; appendices retain stable unnumbered labels.

Numbered targets use native ordinal references. Deliberately unnumbered
appendices use descriptive Markdown anchor links, for example
`[Appendix A](#sec:appendix_a)`; do not request their ordinal with
`[@sec:appendix_a]`. The same distinction applies to other unnumbered headings.

Keep source capitalization and copy identifiers intact in bibliography titles.
Use explicit `n.d.` for a genuinely undated captured resource's publication
date, distinguishing it from the historical work's imprint. Preserve known years
and accurate volumeless-issue metadata rather than inventing missing fields.

Actual template validation/filter calls must reject unresolved tokens,
citations, duplicate/undefined labels and changed source members. Preserve
native PDF natbib/BibTeX and HTML citeproc evidence separately. Inspect table
captions before and during actual horizontal scrolling; project CSS retains
one scroll container and a wrapped caption at its left edge through the native
writer's pinned embedding seam.

Source tests, normally installed checks, retained mathematical producers, native
writer execution, physical-page/browser inspection and independent acceptance
remain separate results. New presentation preserves the producer identity of
retained mathematical exports. Historical sources and failed epochs stay
attached to their original evidence.

## Illustrated arguments

Keep a complete historical impression beside an exact, copy-specific quotation.
State the proposed relation, its strongest local alternative and the limit of a
conditional biological association. Repeat the quotation as real caption text;
name its physical transcription lines and primary citation. Do not classify
ornament or imply that an analogy diagnoses an organism. Body captions should
lead with the interpretive question or measured comparison while retaining
copy, object, accession, credit and rights qualifications. See the
[illustrated-argument contract](research/illustrated-arguments.md).
