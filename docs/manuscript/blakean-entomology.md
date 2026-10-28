# Blakean Entomology: Small Lives, Uncertain Bodies, and the Work of Attention

Daniel Ari Friedman

Private working article, version 0.1.0, 28 October 2026. Initial source-grounded
readings and a complete lexical retrieval experiment within a declared snapshot;
contextual adjudication and copy-specific image review remain in progress.

## Abstract

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
aggregation. The wine-press inventories and the Polypus prevent these problems
from resolving into a uniformly benevolent bestiary. Search results retain
source-copy repetition, editorial boundaries, exact spans and zero cells. They
support a comprehensive review program while remaining distinct from an
adjudicated census of all invertebrate discussions in Blake.

## 1. Why begin with small lives?

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

## 2. Existing questions and the article's contribution

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

## 3. Sources, units and retrieval

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

## 4. Attention, analogy and injury

“A Dream” makes homecoming depend on several kinds of agency. The emmet speaks
her own distress; the dreamer hears it; the glow-worm can illuminate the ground;
the beetle provides an audible orientation. On the reading proposed here, the
poem's coordination is organized around an unresolved need rather than a
single commanding animal. This is an interpretive proposal about the poem's
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
Erdman text begins at E23, record 33. Its continuation must be read with the
following page before interpreting the whole poem.

“The Sick Rose” offers a compact retrieval control. The worm is an explicit
animal-form reference; *flies* is the verb describing its movement, not evidence
for a second animal named a fly. Both spans belong in the candidate concordance,
but they require different decisions. The worm's invisibility and destructive
intimacy also prevent a species identification from resolving the poem. A
literal insect, a figure for desire, and a more general destructive agent are
interpretive alternatives to evaluate, not labels the tokenizer can settle.
Source: *Songs* copy A, object 48; E23, record 33.

The caterpillar and fly of “The Human Abstract” complicate a uniformly tender
reading. They feed within an account of fear, cruelty and mystery that ends in
the human brain. A contextual annotation must preserve the predication and
setting rather than importing the sympathy of “A Dream” because both passages
contain insects. Source: *Songs* copy A, object 41, lines 17–18; E27, record 37.

## 5. Inventories of life around the wine-press

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
An occurrence count alone answers none of these questions.

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

## 6. Taxonomic uncertainty and collective bodies

In *The Book of Thel*, the Worm is addressed and personified rather than simply
displayed as a natural-history specimen. The relation between a vulnerable form,
the Clay and Thel's response requires attention to the sequence of speakers.
The present source intake anchors that discussion to copy B, objects 6–7,
physical text lines 3–9 and 10–12 respectively. It does not claim a complete
reading of all copies or settle the Worm's biological identity.
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

## 7. Instruments, cruelty and the problem of evidence

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

## 8. What remains before a comprehensive account

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

## References and reading status

- Blake, William. *Songs of Innocence and of Experience*, copy A. William Blake
  Archive, pinned XML at commit `7063e9ea8b13d18bd5a585e87610164fd75d3f60`.
  Selected objects and contexts checked; no complete copy-reading claim.
- Blake, William. *Milton*, copy A. Same Archive commit. Selected inventory,
  Polypus and object-description windows checked; no image inspection claim.
- Blake, William. *The Book of Thel*, copy B. Same Archive commit. Selected
  objects 6–7 checked; no complete edition comparison.
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
ceilings, unavailable material and source URLs.
