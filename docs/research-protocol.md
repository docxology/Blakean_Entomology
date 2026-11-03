# Research protocol

Use [PROJECT_STATUS.md](PROJECT_STATUS.md) for the current completion record and
bounded next tasks. This protocol defines research acceptance independently of
software, rendering and delivery.

## Question and scope

How does Blake use small and invertebrate life to think about perception, embodied
vulnerability, predation, labour, generation and collective life? The title uses
*entomology* as a literary research heading. The declared scope includes all
invertebrates, including spiders, worms, snails, shellfish and polyps; it does not
identify every small creature as an insect or attribute modern taxonomy to Blake.

The retrieval target is every match of the versioned explicit vocabulary in every
retained passage. The interpretive target is every relevant animal discussion,
including figurative uses, after contextual review. These targets differ. Synonyms,
unnamed animals, images and unrepresented editions require further evidence.

## Corpus planes

Keep primary reading passages, unverified reading passages, mixed/editorial Erdman
pages, and raw XML as separate populations. XML can contain catalog descriptions,
markup, variant readings and scholarly commentary. A candidate in that plane is
never automatically a Blake-authored occurrence. A passage ID is a captured source
unit, not a unique work, plate, species, independent witness or scholarly reading.

All source units are searched without a display cap. Exact repeated source copies
remain visible. Text hashes identify identical passage text but do not establish
edition equivalence; no pooled count is a species census or inferential sample.
Complete term-by-role-by-plane zero cells accompany nonzero counts. Zero retrieval
means absence from this vocabulary in these bytes, not absence from Blake.

## Vocabulary

`research/vocabulary.json` and its packaged copy record explicit forms, groups and
ambiguities. Match using Blake's versioned Unicode normalization and original
source spans. Do not stem silently. `ant` must not match `giant`; `fly` as a verb
must remain a candidate until reviewed. Declared forms include `emmet`, `emmett`,
`catterpiller`, `polypus`, `earth-worm`, `tape-worm` and `glow-worm`. Split and joined
forms are explicit. Each form belongs to a named search category. An occurrence
may belong to multiple categories; category sums are not a unique-span total.

Direct animal names, generic animal words, products/structures and associated
actions form separate groups. Honey, silk, web and hive are contextual leads, not
organisms. Wings, crawling and stings also occur outside invertebrate discussion.
Serpents and birds are excluded as taxonomic targets but may matter in context.
Additions are versioned and rerun, preserving the earlier vocabulary and result.

## Annotation

The generated review queue contains every hit and immutable occurrence identity.
Review records bind to the exact run receipt and use these decisions:

| Decision | Meaning |
|---|---|
| `animal_literal` | An invertebrate is discussed as an animal in context. |
| `animal_figurative` | Invertebrate reference used in metaphor, vision or personification. |
| `associated` | A structure, product or action relevant to invertebrates. |
| `non_animal` | Verb, monetary unit, unrelated proper name or another false positive. |
| `editorial` | Modern description, apparatus or another source-author boundary. |
| `uncertain` | Insufficient context or unresolved identity; state the reason. |

Blank decisions remain unreviewed. Do not prefill all candidates as animal
references. A valid decision requires reviewer and rationale; accepted animal
evidence additionally requires verification locator. A classification never
changes the upstream authorship label. Inspect adjacent source context, identify
speaker and setting, distinguish explicit names from catalog alternatives, and
retain rival readings. Every animal decision is about the cited span, not an
automatic endorsement of a whole passage, edition, or numerical analysis.

## Completion gates

The modern reference is a separate versioned classification resource, verified
against captured NCBI names, ranks and lineages. Resolved lineage, broad group,
ambiguous mapping, non-taxon and outside-scope states do not adjudicate lexical
hits. Its shared tree layout carries no branch lengths, time inference or
monophyly proof. The vocabulary audit and separate gap-probe epoch preserve
all earlier forms and decisions. See
[the advancement method](research/invertebrate-advancement.md) and
[the style guide](style-guide.md).

New reading credit is recorded in the advancement ledger with selected-text and
source hashes. Full short-poem transcription credit requires every verse line
in that captured object. It does not grant whole-book or physical-image credit.
Neither prose interpretation nor mapping metadata automatically writes a review
decision. Figure and prepared-manuscript completion receipts close their input
and output hashes. Native page inspection and selected-original checks were
completed for the historical 31-page working draft. Every subsequent edition
needs separate native and physical-page evidence; their exact scopes are indexed
in [project status](PROJECT_STATUS.md). New paper bytes require fresh native and
physical-page qualification.

The pipeline can establish exhaustive matching of its declared terms within the
pinned snapshot. A comprehensive literary article additionally requires reviewing
all relevant candidates, edition/object checks, an image inventory, and assessment
of vocabulary omissions. None is inferred from a green software test. Report
unreviewed candidates, unavailable sources and visual ambiguity explicitly.

The current manuscript uses the actual pinned docxology/template pipeline. Its
cover, three graphical abstracts and contents have an explicit physical-page
contract in the [render guide](manuscript/README.md). Native numbered sections,
figures, tables, equations and formalisms retain stable source identifiers.
Their mathematical definitions describe existing counting contracts; they do
not certify a literary interpretation or create a candidate decision. The
[Baine and Hutchings source record](research/biological-symbolism.md) distinguishes
book metadata, inspected criticism, selected primary text and unavailable chapters.
