---
title: "Blakean Entomology: Small Lives, Uncertain Bodies, and the Work of Attention"
author:
  - Daniel Ari Friedman
date: "28 October 2026 · Private research draft 0.2.0"
lang: en
---

The exact shared SDK source pin is recorded in `pyproject.toml` and `uv.lock`. Source-grounded
readings and a complete lexical retrieval experiment within a declared snapshot;
contextual adjudication and copy-specific image review remain in progress.

# Abstract

William Blake's invertebrates range from the lost emmet of “A Dream” to the
expanding Polypus of the prophetic books. Their significance cannot be recovered
by treating every animal name as a fixed symbol or every search result as a
Blake-authored observation. This article develops a source-bound inquiry into
invertebrate lives, figures, products and collective forms across a captured
Blake corpus. A reusable corpus and lexical engine belong to the public Blake
methods repository; the present private application owns its vocabulary,
contextual decisions and interpretation. The declared vocabulary includes
historical spellings, explicit compounds, and distinct channels for animal names
and associated imagery. Preliminary readings identify three recurrent problems:
the obligation to attend to vulnerable life, the instability of human/animal
comparisons, and the difference between coordinated plurality and engulfing
aggregation. Work weighting and finite word windows expose the dependence of lexical prominence
and co-occurrence on the retained source units. The wine-press inventories and the Polypus prevent these problems
from resolving into a uniformly benevolent bestiary. Search results retain
source-copy repetition, editorial boundaries, exact spans and zero cells. They
support a comprehensive review program while remaining distinct from an
adjudicated census of all invertebrate discussions in Blake. A captured modern
reference classification separates lexical discovery from biological
identification. A source-role atlas audits the declared vocabulary, and a bounded
casebook records exactly which short poems and local passages were read.

# 1. Why begin with small lives?

The emmet's difficulty in “A Dream” is practical: she is lost, tired and separated
from her family. The poem makes that difficulty audible before a glow-worm
offers light and a beetle's movement offers a route home. The speaker contributes
sympathy, but does not perform the entire rescue. Distributed capacities become
useful because they respond to a particular creature's need. The animal scene
therefore gives this article a question more precise than whether Blake likes
insects: what forms of attention and association make another being's life
possible? The reading concerns “A Dream,” E16, checked against retained Erdman
record 26 and Archive *Songs* copy A, object 27, especially physical text lines
5, 16 and 20–21. [Archive source](https://raw.githubusercontent.com/blakearchive/data/7063e9ea8b13d18bd5a585e87610164fd75d3f60/works/songsie.a.xml).

“Entomology” names the inquiry rather than restricting it to the modern class
Insecta. Worms, spiders, centipedes, scorpions, snails and Polypus belong within
the requested field. Their differences matter. A glow-worm's compound name must
not turn it into an earthworm, and a mythic Polypus must not acquire a modern
species identity through a database field. The project records Blake's expression
first and biological classification, when warranted, separately. Ambiguous
boundaries between animal, vegetable, human and collective life can themselves
be literary evidence.

This breadth also prevents a familiar selection bias. Reading only the short
lyrics privileges the fly, worm and emmet while overlooking prophetic inventories,
prose, manuscripts, annotations and visual descriptions. Reading all source
planes together creates the opposite error: a curator's image description or
editorial note can become a false Blake quotation. The present method retrieves
broadly while preserving the distinction between a captured lead and an admitted
interpretive claim.

# 2. Existing questions and the article's contribution

The study does not claim to discover that Blake writes about invertebrates.
Janelle A. Schwartz's chapter on Blake and taxonomy explicitly addresses the
varied worm and its relation to decay and generation. Only its publisher abstract
and bibliographic information were accessible in this pass; the chapter's full
argument has not been read here. Its existence rules out presenting a worm-based
approach as an unprecedented research subject. [Publisher abstract, chapter 4,
pp. 113–148](https://academic.oup.com/minnesota-scholarship-online/book/17469/chapter-abstract/175003012).

Caroline Dauphin's discussion of the Polypus connects its changing poetic forms
with problems of generation, bodily boundaries and collectivity. Selected
paragraphs 3–6 and 21–25 inform the present question: how can an aggregated body
become both an image of connection and a threat to distinct lives? Her historical
genealogy is a scholarly interpretation, not independently established by the
search totals reported here. [Dauphin, 2026](https://publis-shs.univ-rouen.fr/eriac/1132.html).

The contribution attempted here is a reproducible relation between broad
retrieval and situated reading. Every admitted interpretation should be traceable
to a particular source span, edition and review decision. Every declared search
form should remain inspectable, including zero-result forms and noisy expansions.
This is useful precisely where a polished argument might otherwise hide its
selection of examples. The method does not remove interpretive judgment; it
makes the decisions through which a concordance becomes an argument available
for examination.

# 3. Sources, units and retrieval

The corpus is an independently copied, private application bundle exported by
the public `blake` repository. Its pin identifies the captured manifest, recovered
projection, SQLite index and portable bundle manifest separately. Original
passage bodies, source hashes, author identities, edition/copy fields, locators,
rights and roles survive export. Export verifies the consumed input bytes before
and after the copy. A Git repository's code, a source capture and an application's
result epoch remain separate objects.

The baseline searches 2,067 captured units: 540 reading documents, 796 nonempty
Erdman pages and 731 raw XML units. Of the reading documents, 199 carry the
identified Blake author and primary role; 341 remain unverified. The Erdman pages
and four XML parts are mixed/editorial source material. The 727 Archive XML
documents remain unverified as whole units because they combine text, apparatus,
metadata and descriptions. These counts describe source units, not 2,067 distinct
works or independent historical witnesses. The counts and identities are bound
in `research/corpus-pin.json` and the text-free baseline summary.

The initial vocabulary has 102 categories and 376 explicit forms. Historical
forms include *Emmet* and *Catterpiller*. The user-specified *emmett* is an explicit
candidate spelling, not silently asserted as an attested Blake form. Compound
families include earth-worm, tape-worm, glow-worm, silk-worm, honey bee and cock
chafer. The implementation uses the existing Blake Unicode normalization and
retains original character offsets. Whole-token matching prevents *ant* from
matching *giant* and *bee* from matching *been*. It does not silently stem *fly*
into every motion verb.

Separate contextual categories include web, silk, honey, hive, shell, wing,
swarm, sting and spinning. These help recover discussion that does not name an
animal, but they introduce many unrelated cases. A wing can belong to an angel
or bird; a spinner can be a human worker; a sting can belong to a plant. Such
forms cannot supply an insect total without contextual review.

The engine emits every category/source/span candidate without a display cap,
plus all nine role/plane cells for every category, including zeros. Equivalent
forms in one category share an identical source span; different categories may
overlap. Thus *honey bee* can yield a compound candidate and a *bee* candidate.
Neither category sums nor repeated printed copies become distinct animal
observations. Exact-text grouping is reported separately and does not establish
that nonidentical editions are independent witnesses.

The first run returns 36,039 category-span candidates, including 2,498 in the
Blake-primary reading scope. These totals deliberately include contextual leads
and non-animal senses. They are measurements of the declared retrieval program,
not a count of invertebrate mentions. Candidate totals for selected categories
illustrate why source planes must remain separate:

| Category | Reading units, all roles | Mixed Erdman pages | Raw XML |
|---|---:|---:|---:|
| Worm and declared derivatives | 468 | 85 | 2,354 |
| Ant / emmet family | 37 | 8 | 230 |
| Fly / flies | 211 | 61 | 4,881 |
| Spider | 78 | 20 | 617 |
| Bee | 45 | 10 | 104 |
| Polypus family | 73 | 22 | 110 |
| Snail | 0 | 2 | 93 |

The table's reading column includes unverified passages. Its XML column includes
catalog prose, code-like identifiers, apparatus and repeated source descriptions.
The snail's absence from the reading plane does not erase the Four Zoas passage
at E323. Nor can a large XML fly count establish that Blake describes thousands
of flies. The different planes serve different discovery functions.

## 3.1. A reference classification, not a phylogeny of poetic names {#sec:reference}

The modern reference contains {{REFERENCE_TAXA}} admitted NCBI taxon records and
an explicit mapping policy for all {{ATLAS_CATEGORIES}} historical search
categories. Each admitted name, rank and ancestry is checked against two
retained EFetch responses, identified by retrieval URL, access date and SHA-256.
The schematic compresses omitted ancestors while preserving captured ancestry.
Its layout comes from the shared validated evidence-tree API. This operation
uses no sequence alignment, evolutionary model or dating analysis. NCBI explains
that its classification uses literature-based curation and that its Common Tree
is an abbreviated classification display. These captured records are a versioned
reference, subject to revision, rather than a final nomenclatural authority.
[@ncbi-taxonomy-2026; @ncbi-classification-limit]

Conditional modern animal senses connect *fly* to Diptera, *spider* to Araneae,
*ant/emmet* to Formicidae and *bee* to Anthophila. These are reference lineages,
not decisions that every retrieved token refers to an organism in that lineage.
Anthophila is more selective than treating all Apoidea as bees. The explicit
*emmett* and *emmitt* query expansions remain unattested in these captured
matches; they have not been erased from the old registry. The old `insect`
retrieval group for *larva* is retained historically, while the mapping policy
marks the life-stage term as unresolved across animal groups. A query tag is
not a biological classification.

The five mapping states distinguish a resolved reference lineage, a broad group,
an ambiguous mapping, a non-taxon lead and an outside-scope label. *Worm* is a
polyphyletic literary term whose possible animal senses cross annelids,
flatworms, nematodes and insect forms; these examples are not exhaustive.
*Glow-worm* cannot be assigned to Annelida by its final word. *Blindworm* may fall
outside the invertebrate scope. *Polypus*, *zoophyte* and *animalcule* retain
historical and figurative uncertainty rather than acquiring species names.
Parts, products and actions such as *wing*, *silk*, *honey* and *spin* receive no
taxon target. No category total is allocated to a taxon by this policy, and
“invertebrates” is not presented as a clade.

![{{REFERENCE_CAPTION}}](assets/invertebrate-reference.png){#fig:invertebrate_reference width=96%}

# 4. Attention, analogy and injury

“A Dream” makes homecoming depend on several kinds of agency. The emmet speaks
her own distress; the dreamer hears it; the glow-worm can illuminate the ground;
the beetle provides an audible orientation. On the reading proposed here, the
poem's coordination is organized around an unresolved need. The closing
imperative offers a route home; it does not narrate a completed rescue. The
glow-worm's office as watchman also leaves an alternative reading through
assigned social roles. Both readings must account for the sequence of distress,
the speaker's tear, practical advice and the ending. This is an interpretive proposal about the poem's
sequence, not a biological claim about ant navigation or a measured social
network. The glow-worm's familiar association with illumination is insufficient
by itself: what matters is when and for whom its capacity becomes useful.

“The Fly” makes another relation possible through the thoughtlessness of a human
hand. Its human/animal comparison can support sympathy, but the comparison also
raises a difficulty: does the speaker attend to the fly's life or use it to think
about his own mortality? The poem's alternating questions give reason to retain
both possibilities. A review record should therefore distinguish an explicit
fly reference from its rhetorical function and from the reader's judgment about
the speaker. The source anchor is Archive *Songs* copy A, object 33; the retained
Erdman text begins at E23, record 33. In this advancement the complete copy-A
physical transcription, lines 3–22, was read: the final happiness follows an
explicit conditional relation between thought and life. It is the speaker's
conclusion, not testimony from the fly about its injury. Full-poem transcription
credit does not include the design, other copies or all of *Songs*.
[@blake-songs-a, object 33, physical lines 3–22]

“The Sick Rose” offers a compact retrieval control. The worm is an explicit
animal-form reference; *flies* is the verb describing its movement, not evidence
for a second animal named a fly. Both spans belong in the candidate concordance,
but they require different decisions. The worm's invisibility and destructive
intimacy also prevent a species identification from resolving the poem. A
literal insect, a figure for desire, and a more general destructive agent are
interpretive alternatives to evaluate, not labels the tokenizer can settle.
Source: *Songs* copy A, object 48; E23, record 33. The complete two-stanza
transcription was read for the present casebook. Its movement from sickness to
the found bed and destructive secret love offers no diagnostic anatomy with
which to resolve the agent. [@blake-songs-a, object 48, physical lines 3–10]

The caterpillar and fly of “The Human Abstract” complicate a uniformly tender
reading. They feed within an account of fear, cruelty and mystery that ends in
the human brain. A contextual annotation must preserve the predication and
setting rather than importing the sympathy of “A Dream” because both passages
contain insects. Reading the complete transcription in this pass makes the final
location of the sought tree in the human brain part of the feeding scene's
context. The caterpillar and fly therefore cannot supply an empirical plant-host
relation through their nouns alone. Source: *Songs* copy A, object 41, physical
lines 3–26, especially 17–18 and 23–26; E27, record 37.
[@blake-songs-a, object 41]

# 5. Inventories of life around the wine-press

The large inventory in *Milton* names the earth-worm, beetle, emmet, centipede,
spider, spinner, earwig, maggot, flea, louse, bug, tape-worm, slug, grasshopper,
scorpion, gnat, wasp, hornet and honey bee. It places them among seeds, roots,
plants and vertebrates around Luvah's wine-presses. Source: plate 27 [29],
E124, record 134; Archive copy A, object 24, physical text lines 13–22.
[Pinned XML](https://raw.githubusercontent.com/blakearchive/data/7063e9ea8b13d18bd5a585e87610164fd75d3f60/works/milton.a.xml).

The passage combines dance and celebration with disease, death and the violent
labour of the press. The human grapes' suffering makes a simple ecological
harmony reading inadequate. The same assemblage can display abundant life and
unequal exposure to torment. This article accordingly asks who moves, sings,
feeds or suffers in an animal scene, and whether those positions can change.
An occurrence count alone answers none of these questions. The newly inspected
object24 lines 2–42 sharpen the distinction between positions *around* and *in*
the press. Its opening joins war to printing; the late human grapes do not
participate in the surrounding dance. The nettle that stings and the creeping
weeds also provide non-taxon controls inside the same context. These verbs
cannot be assigned to insects by an associated-imagery search category.
[@blake-milton-a, object 24, physical lines 2–42]

The related Four Zoas inventory at E404, manuscript page 136, lines 29–34,
belongs to another compositional context. It should be connected to the Milton
inventory for comparison while retaining both work identities. This is a
different operation from recognizing repeated copies of a single poem. The
protocol therefore preserves source repetition and separately records relations
between passages. A future account of revision or reuse needs textual and
manuscript scholarship beyond exact-text deduplication.

The snail passage at E323 supplies a further counterweight. Worm, snail, emmet
and beetle participate in mockery of Los. Their smallness does not ensure
innocence, nor does the presence of Los ensure a stable human superiority. The
scene motivates reading agency and evaluative position alongside animal name.
Source: retained Erdman record 335, opening lines of E323.

# 6. Taxonomic uncertainty and collective bodies

In *The Book of Thel*, the Worm is addressed and personified rather than simply
displayed as a natural-history specimen. The relation between a vulnerable form,
the Clay and Thel's response requires attention to the sequence of speakers.
The present source intake anchors that discussion to copy B, objects 6–7,
physical text lines 3–14 and 2–18 respectively in the new bounded reading.
Thel's later acknowledgment distinguishes knowing that injury is punished from
learning that the form is positively cherished with milk and oil. Care therefore
extends beyond avoiding the bruising foot. The Clay's maternal and nuptial speech
also constrains the terms of this local care; it is not automatically a universal
social doctrine. This reading does not claim all copies or settle the Worm's
biological identity. [@blake-thel-b, objects 6–7]
[Pinned XML](https://raw.githubusercontent.com/blakearchive/data/7063e9ea8b13d18bd5a585e87610164fd75d3f60/works/thel.b.xml).

Polypus intensifies the problem. Its inclusion in an invertebrate inquiry is
necessary, yet a fixed modern zoological classification would lose what the
poetic figure does to the boundaries of bodies and individuality. The initial
working comparison is between association that helps distinct beings live, as
in the proposed reading of “A Dream,” and aggregation that absorbs or renders
indistinct its participants. The comparison is a research question, not an
equation of Blake's creatures with modern political institutions.

Dauphin's account of the changing Polypus makes it especially important to
distinguish the biological animal, the poetic figure and later iconographic
interpretation. The Archive's copy-A Milton descriptions also retain alternative
identifications: object 24 can be described through caterpillar/centipede and
beetle/bee/hornet alternatives, while object 31 permits vegetable/Polypus
possibilities. A catalog's alternatives cannot become several confirmed
depicted species. The present pass has inspected those descriptions, not the
physical images. [Dauphin, selected paragraphs](https://publis-shs.univ-rouen.fr/eriac/1132.html);
[Archive Milton A](https://raw.githubusercontent.com/blakearchive/data/7063e9ea8b13d18bd5a585e87610164fd75d3f60/works/milton.a.xml).

The new textual reading of copy A, object28, physical lines 24–35, checks the
joining of every man into one Polypus against the surrounding nerves, Orc and
transformation language. The separately captured object31 description remains
modern catalog prose. An editorial vegetation/animal alternative cannot identify
the poem's collective body; the poem cannot establish a fresh visual judgment
about the catalogued form. Historical lexicography remains an acquisition task.
[@blake-milton-a, objects 28 and 31]

# 7. Instruments, cruelty and the problem of evidence

The microscopy scene in *An Island in the Moon*, chapter 10, E462, offers louse,
flea, butterfly and cock chafer to spectators amid malfunctioning apparatus and
social performance. The scene makes looking itself part of the inquiry. An
animal noun names a proposed demonstration; it does not prove a successful
observation by a character, much less by Blake. Retained record 474 includes
the scene and distinguishes its speech and action from the later song material.

“Auguries of Innocence” supplies related but distinct ethical tests. The fly,
spider, chafer, caterpillar, moth, butterfly, gnat, bee, cricket and emmet appear
within a poem that moves among suffering, perception and human conduct. Context
matters even for the lexicon: the *Mite* at E492 concerns an amount extracted from
labour, not an arachnid. A broad concordance must retrieve that case and a careful
review must decline to count it as an animal. The relevant retained pages are
E490–492, records 502–504.

These examples locate the method's responsibility. Broad search should expose
difficult cases rather than eliminate them invisibly. Contextual annotation
should then state what was checked and why a classification was made. Neither
software validation nor a fluent caption can replace source inspection.

# 8. Source repetition, work balance and lexical distance

The shared-method implementation permits two further analyses of the same pinned
bundle. The NFKC experiment retains the original categories and recomputes all
primary counts. A separate literal experiment applies explicitly declared word
windows. Both have immutable source-bound receipts; their different profiles and
denominators remain separately named. The historical baseline and its eleven
authored decisions retain their original run identity. Fresh replay leaves the
five analytical baseline artifacts byte-identical; its new producer receipt does
not repin those decisions or add contextual animal classifications.

## 8.1. A category is not an animal observation

The sensitivity inventory contains the 199 identified Blake-primary reading
units, grouped by 33 recorded work identifiers. These are a restricted subset
of the bundle's 2,067 captured units. The vocabulary still has 102 categories;
its 2,498 primary category-span candidates include direct names, compounds,
products, structures and actions. The counting unit remains a category attached
to a source span. Two categories can refer to overlapping language, while one
category can retrieve both animal and non-animal senses.

This distinction matters for the readings already proposed in §§4–7. The
*fly* category cannot decide whether a retrieved form names an animal or describes
motion. The lexical relation between a compound and one of its components does
not establish two creatures. Likewise, the *web* and *honey* channels can help
locate relevant discussion without establishing a speaker, a maker or an animal
subject. Normalization and explicit forms improve reproducibility of discovery;
they do not resolve these interpretive relations. The animal and non-animal
contrasts already discussed in §4 therefore remain review tasks, rather than
exceptions that can be subtracted automatically from a total.

## 8.2. Work weighting changes the question

The pooled rate divides a category's copy-retaining count by all 644,247 NFKC
word tokens in the eligible inventory. The work-balanced rate first calculates
a rate within each positive-token work group and then averages the 33 rates
with equal weight. A work group with no occurrence contributes a zero rate.
These quantities answer different questions: frequency in the retained textual
mass, and the average of the recorded work-group frequencies. Neither treats the
33 identifiers as a random sample of independent works.

| Category | Retained candidates | Pooled rate | Equal-work mean rate | Largest work-group share |
|---|---:|---:|---:|---:|
| worm | 468 | 7.264 | 10.972 | 36.5% |
| fly | 183 | 2.841 | 5.392 | 56.3% |
| spider | 78 | 1.211 | 0.702 | 46.2% |
| polypus | 73 | 1.133 | 0.466 | 54.8% |
| bee | 44 | 0.683 | 0.358 | 40.9% |
| ant | 37 | 0.574 | 0.263 | 37.8% |
| caterpillar | 36 | 0.559 | 0.625 | 41.7% |
| butterfly | 20 | 0.310 | 0.371 | 80.0% |

Rates are category-span candidates per 10,000 NFKC tokens, rounded only for
presentation. The *worm* and *fly* rates increase under equal-work weighting,
whereas *polypus*, *spider*, *bee* and *ant* decrease. This reversal prevents a
single ordering from serving as a context-free account of prominence. The
largest recorded work-group shares further locate the dependency: `thel`
contributes 171 of the 468 *worm* candidates; `songsie` contributes 103 of 183
*fly* candidates; and `milton` contributes 40 of 73 *polypus* candidates.
These are counts across retained source units within each group, not counts of
distinct lines or independently inspected passages. The 80% *butterfly* share
belongs to `thel` and comprises 16 of 20 retained candidates. It does not, by
itself, establish that the work contains 16 different butterfly passages.

The leave-one-work-out calculations offer a related diagnostic. Removing one
recorded group at a time gives pooled *fly* rates from 1.411 to 3.828 and
*polypus* rates from 0.581 to 1.288 per 10,000 remaining tokens. These are
finite-inventory omission ranges, not confidence intervals or uncertainty
estimates for Blake's oeuvre. Their value is to expose which claims about
relative prominence depend on the retained group composition. They support
returning to the different settings of the short lyrics, the inventories and
the Polypus discussed in §§4–6; they do not establish a common function across
those settings.

## 8.3. Exact-text deduplication is a narrow check

Grouping complete source units by identical text removes one unit from this
inventory: the two `america` records `archive:america.n` and
`archive:america.n--878c90904184` share 2,941 NFKC tokens. The exact-text inventory
therefore contains 198 units and 641,306 tokens. The eight selected category
counts in the table are unchanged, but their pooled rates change because the
denominator changes. Across all categories, the candidate sum falls from 2,498
to 2,489 through five changes:

| Category | Copy-retaining count | Exact-text count |
|---|---:|---:|
| crawl | 26 | 25 |
| flight_verbs | 156 | 153 |
| insect | 14 | 13 |
| mussel | 13 | 12 |
| wing | 532 | 529 |

The first column names the actual registry categories; the presence of *insect*
and *mussel* means these changes should not all be described as contextual-action
changes. Exact-text equality detects an identical complete unit. It cannot detect
all repeated poems embedded in nonidentical copies, near-identical editions,
shared passages within different works, or differences in editorial boundaries.
The small change in this check therefore supplies no evidence that the remaining
copies or reading positions are independent. In particular, unchanged counts do
not turn the concentration results into an edition-controlled comparison.

## 8.4. Proximity exposes the scale of co-occurrence

A separate experiment searches the raw singular literal pairs shown below.
These are not expansions of the NFKC categories: *emmet* is one explicit literal
term, while the category named *ant* has a broader declared form inventory;
*fly* in a literal pair does not include every form in the *fly* category.
The literal engine retains original-text word boundaries and has a denominator
of 644,245 word tokens. The NFKC denominator is 644,247. These profile labels and
denominators remain separate even though the two experiments use the same 199
eligible source units in this bundle.

| Literal pair | 8 words | 16 words | 32 words | 64 words | Whole source unit |
|---|---:|---:|---:|---:|---:|
| worm + fly | 4 | 4 | 28 | 28 | 66 |
| bee + flower | 0 | 0 | 0 | 0 | 30 |
| spider + web | 13 | 13 | 13 | 13 | 33 |
| emmet + grass | 27 | 27 | 27 | 27 | 36 |

Cells count matched source units, with copies retained. A finite window requires
a complete word envelope containing both terms. The last column removes that
finite-distance requirement; it is a different scope, not a point at 200 words
or an extrapolated infinity. Thus the *worm + fly* increase from 28 units at
32 words to 66 whole units cannot be read as 38 additional nearby encounters.
The *bee + flower* contrast is sharper: no finite window through 64 words matches,
while 30 complete source units contain both literals. That result identifies
a dependence on source-unit extent, not the absence of bee–flower relations in
Blake. Singular forms, unrepresented variants, source coverage and unreviewed
senses all constrain recall.

The early plateaus for *spider + web* and *emmet + grass* likewise do not count
13 and 27 independent scenes. Repeated copies can reproduce one textual
relationship across several stored units. Establishing distinct passages,
speakers, functions or material witnesses would require the contextual and
copy-specific work already specified in §9. The contrast between a short window
and a whole-unit search makes that requirement visible before co-occurrence is
mistaken for an interpretive association.


![Retrieval sensitivity within the pinned primary reading inventory. A compares pooled and equal-work category rates; B shows each category's largest work-group share; C counts source units for literal singular pairs across finite windows and whole-unit scope. Counts retain copies and overlapping categories. No panel measures independent reading positions or adjudicated animals.](assets/retrieval-sensitivity.png){#fig:retrieval_sensitivity width=98%}

## 8.5. A complete vocabulary audit has several kinds of zero {#sec:atlas}

The new atlas recomputes the unchanged {{ATLAS_CATEGORIES}} categories and
{{ATLAS_FORMS}} explicit forms across {{ATLAS_UNITS}} captured units. It returns
{{ATLAS_CANDIDATES}} category-source-span candidates, including
{{ATLAS_PRIMARY_CANDIDATES}} in {{ATLAS_PRIMARY_UNITS}} primary reading units.
All role/plane zero cells remain in the data. The form audit records both
casefolded surface-form counts and normalized-equivalent counts, separately for
the primary scope and all planes. {{ZERO_NORMALIZED_FORMS}} declared forms have
no normalized-equivalent match anywhere in the captured inventory;
{{ZERO_SURFACE_FORMS}} have no exact casefolded surface match. A split or
hyphenated form can be covered through an equivalent declared token sequence,
so these are different questions. {{ALIAS_GROUPS}} normalized alias groups expose
this redundancy rather than multiplying one category's hits.

The audit retains {{ATLAS_DISTINCT_SPANS}} distinct exact source intervals.
{{OVERLAP_PAIRS}} candidate pairs have intersecting intervals, including nested
compound/head matches. Equal intervals and intersecting intervals are different
diagnostics; neither is a number of organisms. No automatic taxonomic allocation
is computed from these spans. The independently bound gap-probe registry tests
new recall leads while preserving the original vocabulary, baseline and query
epochs. Even a zero-result gap probe would describe only these bytes and forms.

The [atlas](#fig:corpus_atlas) makes eligibility and repetition visible. Its first
panel separates source-role/plane populations; its second shows matched-unit
fractions within every recorded primary work group. The adjacent equal-work
mean gives each recorded group one contribution, including zero-match groups.
The pooled fraction weights retained units instead. This is a descriptive
comparison, not edition reconciliation or a comparison of independent works.
Whole-text grouping leaves {{PRIMARY_EXACT_UNITS}} primary units; it does not
remove repeated poems embedded in different copy texts. The snail's primary zero
and exploratory positives exemplify why these populations cannot be collapsed.

![{{ATLAS_CAPTION}}](assets/corpus-atlas.png){#fig:corpus_atlas width=98%}

## 8.6. Reading coverage is a different denominator {#sec:reading_coverage}

The new casebook records {{CASEBOOK_CASES}} bounded interpretive cases and
{{COMPLETE_POEMS}} complete short-poem transcriptions: “A Dream,” “The Fly,”
“The Human Abstract” and “The Sick Rose,” all in copy A. It separately records
the inspected Milton and Thel passages and the modern catalog alternative.
Ordered line IDs and selected-text hashes close those reading claims. These are
reading receipts, not additional candidate decisions. The
{{HISTORICAL_REVIEWED}} historical decisions remain on their original run, with
{{HISTORICAL_UNREVIEWED}} candidates still unreviewed there; none has been
reclassified or rebound to this atlas. The new atlas has zero authored decisions,
and corpus images remain unreviewed.

This separation also sets a limit on the argument. The small lyric sequence can
now be discussed through its ending, whereas the Polypus and wine-press cases
remain local passages. The contrast between practical assistance, conditional
consolation, secret destruction, nurture and bodily aggregation has support in
these selected contexts. It has not been established as a distribution of
functions across all of Blake. The machine audit supplies the next places to
read, and preserves the places where it cannot yet support a claim.

# 9. What remains before a comprehensive account

The software establishes complete matching of the declared forms within the
pinned units. A comprehensive literary account still requires candidate
adjudication, work/copy reconciliation, examination of source boundaries,
assessment of unlisted or unnamed animals, and a systematic visual inventory.
Long-range discussion can exceed the saved 120-character context envelope;
review must return to the complete source unit and, where necessary, its
neighbours and physical object. Editorial animal decisions remain exploratory
until the quoted text's author and location have been established separately.

Mike Goode's discussion of digital fragmentation is pertinent to the research
design: retrieving a textual fragment can detach it from the verbal-visual work.
The present concordance is therefore a navigation instrument. An argument
requires returning from its fragments to their material and textual relations.
Only selected opening sections of Goode's essay were read here.
[“Google Blake”](https://romantic-circles.org/praxis/pedagogical_blake/praxis.2016.pedagogical_blake.goode).

The article's provisional claim is consequently bounded but substantive:
invertebrate figures let these selected Blake passages test the relation between
attention to a life and the forms that connect, classify or absorb it. The
counterexamples are part of that claim. Sympathy, mockery, appetite, predation,
work and aggregation cannot be replaced by one stable animal-symbol dictionary.
The corpus application makes the further tests of this reading inspectable.

# References and reading status

- Blake, William. *Songs of Innocence and of Experience*, copy A. William Blake
  Archive, pinned XML at commit `7063e9ea8b13d18bd5a585e87610164fd75d3f60`.
  Four complete short-poem transcriptions checked in the advancement casebook;
  no complete copy-reading or image-inspection claim. [@blake-songs-a]
- Blake, William. *Milton*, copy A. Same Archive commit. Selected inventory,
  Polypus and object-description windows checked; no image inspection claim.
  [@blake-milton-a]
- Blake, William. *The Book of Thel*, copy B. Same Archive commit. Selected
  objects 6–7 checked; no complete edition comparison. [@blake-thel-b]
- Blake, William. *The Complete Poetry and Prose*, edited by David V. Erdman.
  Retained Archive reader API response, SHA-256 in the source-intake ledger.
  Selected page contexts checked; mixed edition text is not uniformly Blake's.
- Dauphin, Caroline. 2026. “A Genealogy of the Polypus, from William Blake to
  H.P. Lovecraft: The Root of All Evil?” *Lectures du monde anglophone* 7.
  Selected paragraphs 3–6 and 21–25; not a complete article reading.
- Goode, Mike. 2016. “Google Blake.” *Romantic Circles Praxis*. Selected opening
  sections on fragmentation and pedagogy; not a complete essay reading.
- Schwartz, Janelle A. 2012. “Art Thou but a Worm? Blake and the Question
  Concerning Taxonomy.” In *Worm Work: Recasting Romanticism*, 113–148.
  [Chapter DOI](https://doi.org/10.5749/minnesota/9780816673209.003.0004). Publisher abstract only;
  full chapter unavailable in this pass.

Additional located scholarship, including David Perkins's “Animal Rights and
‘Auguries of Innocence’” (*Blake/An Illustrated Quarterly* 33.1, 1999), remains
an acquisition task. Its PDF fetch failed in this pass; no complete reading or
argumentative credit is assigned. See `research/reading-ledger.json` for exact
ceilings, unavailable material and source URLs. The advancement ledger
`research/reading-ledger-advancement-v1.json` adds precisely bounded new reading
credit while preserving that historical ledger.

# Captured reference resources

The following references identify the newly captured classification, policy and
primary-text resources. Exact snapshot hashes and claim limits accompany the
source manifest; catalog descriptions remain distinct from Blake's transcription.

::: {#refs}
:::
