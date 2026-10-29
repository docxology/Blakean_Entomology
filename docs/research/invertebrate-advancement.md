# Invertebrate reference, corpus atlas and contextual casebook

This documents the reference/atlas/casebook research epoch used by the later
installed and reviewed manuscript. Its original source-stage handoff is retained
in Git history; [project status](../PROJECT_STATUS.md) and the
[render guide](../manuscript/README.md) identify completed qualification and the
remaining research tasks. The historical vocabulary, baseline, eleven decisions
and their run pin retain their exact identities.

## What the reference establishes

`research/reference-taxonomy-v1.json` contains 37 admitted NCBI records and one
conditional mapping for each of the 102 existing query categories. Two retained
EFetch XML responses supply names, ranks and complete `LineageEx` ancestry.
The loader checks raw source sizes/hashes, independently projects each admitted
record, and delegates rooted-tree validation to `blake.methods.hierarchy`.
There is no private generic tree validator or layout implementation.

NCBI IDs were checked against returned scientific names and ranks. The first
exploratory request also returned records unsuitable for the intended groups,
including species; those bytes remain in the capture, but those records were
not admitted. The supplementary request supplies checked Anthophila, Chilopoda,
Dermaptera, Cirripedia, Hydra and Clitellata records. The reference does not
admit species records. Preserving an exploratory capture differs from asserting
every returned record belongs in the reference.

The presentation is a compressed classification. Omitted intermediate nodes do
not make the retained children exclusive sister taxa, and equal edge spacing is
not distance or time. No sequence data were analysed. No contested monophyly
question is settled by the diagram. This bounded classification use requires no
adopted primary phylogenetic-paper topology; resolving a disputed relationship
would require its own literature acquisition and claim ledger. NCBI's captured
official classification-limit article and browser disclaimer constrain the use.

Modern conditional *fly*, *spider*, *ant/emmet* and *bee* senses connect to
Diptera, Araneae, Formicidae and Anthophila. The database establishes the reference
lineages; the lexical association policy is an explicit editorial research aid.
It does not establish that a Blake span names that group. Other entries retain
broad groups, uncertain alternatives or no animal target. Worm, Polypus,
animalcule and life-stage labels cannot be treated as interchangeable taxa.
The figure repeats Polypus's count beside two reference alternatives and says
explicitly that those counts must not be summed.

## Coverage audit and gap probes

The atlas scans the original 376 forms without a display limit. Its complete
role/plane table preserves all nine cells for every category, including zeros.
The full typed receipt is private because it is large; the closed export tables
make every category, explicit form and primary work group accessible without
opening the 65 MB receipt.

Form counts distinguish casefolded exact surface matches from NFKC-equivalent
matches. Both populations are reported for all source planes and for identified
Blake-primary reading alone. An XML match is not a Blake attestation. A primary
match is not a contextual animal decision. Unattested query variants remain in
the historical registry.

The audit measures 550 intersecting candidate-interval pairs across the captured
inventory. Equal, intersecting and distinct intervals are separate diagnostics.
Compound/head overlap must not become an organism total. All work, token and
exact whole-text summaries use public descriptive statistics and the named NFKC
profile. The prior literal experiment's 644,245 tokens remain distinct from the
NFKC inventory's 644,247 primary tokens.

The separate `vocabulary-gap-probes-v1.json` declares 21 forms in seven categories:
harvestman, daddy-long-legs, nematode, roundworm, crayfish plural variants,
antlion and silverfish. Its source-bound run returns zero candidates in the
2,067 captured units. This does not prove that Blake never discussed any such
creature. Initial proposed split plurals were rejected as additions because
their normalized sequences were already covered by historical hyphenated forms;
the failure receipt is retained. No gap probe replaces a historical query epoch.

## Reading credit

`research/reading-ledger-advancement-v1.json` adds four complete short-poem
transcription readings and five bounded passage/catalog selections. It closes
ordered line IDs and selected-text hashes. The seven interpretive cases retain
a rival reading and taxonomic limit. No case automatically writes candidate
decisions, changes the old reading ledger, credits a whole prophetic book or
identifies an animal in an uninspected image.

The prepared Markdown packet includes a readable `contextual-casebook.md`.
The article incorporates the offered route in “A Dream,” the conditional ending
of “The Fly,” the brain/tree conclusion in “The Human Abstract,” the Sick Rose
flight verb, differing positions at the wine-press, Thel's distinction between
protection and nourishment, and the separate poetic and catalog meanings of
Polypus. All are bounded by captured primary contexts.

## Reproduction

The application CLI exposes `verify-reference` and `corpus-atlas`. Both require
an explicit reference SHA-256 and retained source directory. Atlas outputs must
be new paths under the working directory's `analysis_output/` tree. Wrong pins,
changed sources, dangling mappings, false certainty, misleading units, occupied
destinations and symlink paths reject with nonzero exits.

`tools/build_reference_figures.py` consumes pinned reference and atlas receipts,
then publishes PNG, SVG and generated captions. `tools/reference_plotting.py`
owns the domain presentation; both files are hashed in the figure receipt.
`tools/prepare_research_manuscript.py` validates source/data/figure bindings,
citations and image membership, hydrates count tokens, and copies independent
render inputs. It does not run Pandoc or a native renderer. Use the current
[render guide](../manuscript/README.md) and CLI contracts for a new epoch. The
original `coordination/entomology-agent/ROOT_COMMANDS.md` remains a historical
delivery-packet recipe; its staging paths are not inferred from a source clone.
