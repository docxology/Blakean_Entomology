# Entomology authoring and evidence guide

Apply the [shared Blake conventions](https://github.com/docxology/blake/blob/21b1c002ef7588b9c908fb60fd6111c4eb548358/docs/style-guide.md)
for method profiles, source roles, immutable epochs, count units and evidence
claims. This private addendum owns biological vocabulary and literary readings.
The shared guide is bound here to the exact public SDK source used by this project.

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

The authored article keeps the earlier source-bound sections and uses strict
`{{UPPERCASE_TOKENS}}` for new computed quantities and captions. Run
`tools/prepare_research_manuscript.py` to produce a fresh hydrated Markdown input,
copied figure assets, references and a completion manifest. Any unresolved token,
missing citation key, changed figure or mismatched source binding is an error.
Stable figure IDs use `{#fig:...}`. The standalone private renderer uses Markdown
links to those IDs; it does not assume a cross-reference filter is installed.
Use Pandoc bibliography citations for the new captured sources and `--citeproc`
at root's final render. Keep native layout choices in the print header.

Source-stage tests, aggregate figure inspection, installed-package replay,
native-page inspection and independent acceptance are separate results. Root
owns the final version, SDK pin, native PDF and Downloads delivery.
