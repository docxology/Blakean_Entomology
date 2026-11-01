# Entomology authoring and evidence guide

Apply the [shared Blake conventions](https://github.com/docxology/blake/blob/d34876e021a8f2e654b96f1c23f7ec43d8d958c2/docs/style-guide.md)
for method profiles, source roles, immutable epochs, count units and evidence
claims. This private addendum owns biological vocabulary and literary readings.
The current 0.6.0 software selects the exact public 0.6.0 source linked above.
The retained 0.4.0 PDF/HTML used public SDK
`45171a099a6a658c52ab689501de646a28485653` and the separately pinned
docxology/template framework. Matching version numbers do not identify the
same package; review planning creates no new native edition. The historical 0.2.0 paper and analytical epoch used
`d020f47767996a061b6f60e93a82da9386a7926c`; the shared guide body is
byte-identical at those two historical commits. Keep the original producer attached to
its retained bytes rather than transferring it to the current paper. See [project status](PROJECT_STATUS.md) for
current qualification and open research tasks.

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

## Manuscript preparation

Use the [native render guide](manuscript/README.md). Hydrate declared data tokens
with pinned inputs, then call `tools/render_manuscript.py` with an admitted
request and explicitly selected compatible template checkout/runtime. The
request pins preparation, analyses, authentic recto/provenance, configuration,
preamble and project web stylesheet. Verify resolved YAML values and actual
PDF metadata as well as Markdown token substitution.

Keep cover, graphical abstracts and TOC choices in source configuration and
preamble. Verify physical pages rather than relying on printed counter resets.
The three graphical abstracts distinguish candidate retrieval/source facets,
the retained seven-case literary argument and weighting/classification limits.
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
