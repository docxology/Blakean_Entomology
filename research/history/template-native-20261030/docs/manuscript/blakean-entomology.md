---
title: "Blakean Entomology: Small Lives, Uncertain Bodies, and the Work of Attention"
author:
  - Daniel Ari Friedman
date: "29 October 2026 · Private research draft 0.3.0"
lang: en
---

Selected textual and material witnesses are read alongside an exhaustive search
of declared forms in a pinned corpus. Corpus-wide contextual and visual review
remains incomplete.

# Abstract

William Blake's small lives make relations consequential: a lost emmet needs a
route home; a fly becomes a human analogy after injury; feeding insects inhabit
a tree rooted in the human brain; and a Polypus joins persons within a collective
body. This article distinguishes three relations across these scenes: provision
that enables another life, feeding that uses a living body, and aggregation that
reorganizes its members' powers. Care, appetite, predation, cruelty and metaphor
intersect without becoming morally interchangeable. Copy-specific readings of
four short poems, {{SELECTED_IMAGE_WITNESSES}} selected historical scans, local prophetic and prose
passages, and bounded scholarship test this argument against rival readings.
A reproducible concordance preserves the breadth that close reading necessarily
selects: 102 query categories retrieve 36,039 category-source-span candidates
across 2,067 captured units, including 2,498 candidates in 199 identified
Blake-primary reading units. Within that primary scope, 82 name-family categories
contribute 1,239 candidates. Their pooled and equal nonempty-group compositions
differ by total variation 0.222387 across 26 positive groups, whereas token-rate
comparisons retain all 33 eligible groups. Twelve literal-pair experiments expose
source dependence and distance. A purposive contextual extension validates {{CONTEXT_REVIEW_TOTAL}} authored decisions, including 36 new agent judgments, while retaining {{CONTEXT_REVIEW_REMAINING}} unreviewed candidates. These are distributions of retrieval mass, not
an adjudicated animal census or complete oeuvre. Modern classification, lexical
matching and material interpretation remain distinct. The resulting argument
locates ethical force in particular acts of hearing, sustaining, injuring and
joining, while its explicit zeros and unresolved cases direct further reading.

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

The argument follows three relations rather than a stable bestiary: provision
that enables another life, feeding that uses a living body, and aggregation that
reorganizes its members' powers. A glow-worm's assistance and the Clay's nurture
make dependence answerable; a worm's destructive intimacy and the wine-press's
suffering prevent abundance from guaranteeing reciprocity. The Polypus asks what
happens to distinct capacities when lives join. Each relation can intersect the
others, but neither a shared animal name nor a biological analogy supplies a
single moral verdict.

# 2. Existing questions and the article's contribution

The study does not claim to discover that Blake writes about invertebrates.
Janelle A. Schwartz's chapter on Blake and taxonomy explicitly addresses the
varied worm and its relation to decay and generation. Only its publisher abstract
and bibliographic information were accessible in this pass; the chapter's full
argument has not been read here. Its existence rules out presenting a worm-based
approach as an unprecedented research subject. [@schwartz-2012, chapter 4, publisher abstract only].

Caroline Dauphin's discussion of the Polypus connects its changing poetic forms
with problems of generation, bodily boundaries and collectivity. The earlier selected
paragraphs 3–6 and 21–25, now extended through paragraphs 7–28 and 49–50, inform the present question: how can an aggregated body
become both an image of connection and a threat to distinct lives? Her historical
genealogy is a scholarly interpretation, not independently established by the
search totals reported here. [@dauphin-2026-expanded, paragraphs 3–28 and 49–50].

Perkins's complete article on animal rights and “Auguries of Innocence” and
Srigley's complete article on “The Sick Rose” now supply substantive, divergent
readings of injury. Material scholarship by Essick and Viscomi and selected Fara
sections place reproduction, generation and the terms of observation beside the
poems; their limited reading scopes are specified below. Gould, Baker and Erasmus
Darwin offer historically available comparisons, with no demonstrated reading or
influence chain from these books to Blake. [@perkins-1999; @srigley-1992;
@essick-viscomi-2002; @fara-2020]

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

## 3.1. The animal name and the material page

An animal word and a depicted animal are different kinds of evidence. A transcription can establish that a poem names a fly without establishing that a particular mark in its design depicts one. Conversely, a visually prominent body can matter without supplying an additional lexical occurrence. The illuminated page makes this distinction productive: lettering, vegetation, figures and coloured grounds guide the movement through the poem, sometimes offering an analogy and sometimes withholding the object that a reader expects to find. The relevant question is therefore not simply whether the picture confirms the text, but what each medium enables the reader to notice, and what remains uncertain after they have been considered together.

Material scholarship also discourages treating colour as a transparent record of a single original conception. Essick and Viscomi distinguish impressions printed in one ink and subsequently coloured from colour printing, in which colour is transferred from the plate. They also show how cropping, straightening and mounting can conceal the relation between an impression and its sheet. Their argument concerns printing processes and bibliographical evidence; it does not license assigning an intention to each difference between two digital reproductions. [@essick-viscomi-2002, pp. 74–76, 91–92] Here the complete captured scans remain available beside the resized figures. Details are enlarged only with their crop boundaries recorded. None has been rotated or recoloured.

The distinction matters particularly for small lives. Enlarging a minute shape may make its outlines easier to inspect while also detaching it from the proportions and verbal setting through which it becomes meaningful. The four *Songs* impressions reproduced here belong to copy Y at the Metropolitan Museum of Art. Their text is checked in that copy; they do not inherit the copy-A reading credit of the earlier casebook. The *Thel* comparison likewise names each physical witness. This is an addition of seven selected visual witnesses, not a representative sample of all copies or a visual census of Blake's animals. [@blake-songs-y-2026; @blake-thel-f-2026; @blake-thel-o-2026]

## 3.2. A reference classification, not a phylogeny of poetic names {#sec:reference}

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

The earlier casebook read all verse lines of these four poems in copy A.
The present comparison adds separate complete transcriptions in copy Y and the
four Met impressions reproduced below. The copy-A textual credits remain intact;
no full-copy reading or all-copy visual comparison follows.

## 4.1. Assistance has several agents

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

In copy Y's “A Dream,” orange-brown lettering occupies almost the entire designed field, while curling stems, tufts and leaves pass around and between its stanzas. Blue washes gather along parts of the margins. The reader's route through speech is also a route through this vegetation. A small upright, pale figure at the lower right becomes clearer in a bounded enlargement, but its identity is less secure than the text's naming of the glow-worm and beetle. It would be misleading to turn every adjacent mark into an insect. What can be seen with greater confidence is a page that makes the written journey dense with branching and interlacing forms. [@blake-songs-y-2026, plate 26, object 26, physical lines 3–22; Met 17.10.26]

William Gould's *An Account of English Ants* supplies a historically available contrast, without establishing that Blake read this book. At the beginning of chapter VIII, Gould presents ant labour as an example of public care and an admonition to human indolence. But that moral use coexists with a demand for repeated observation. Later in the chapter he disputes inherited accounts of winter granaries among the English ants he has examined, while reserving the possibility of different behaviour elsewhere. [@gould-1747, pp. 66–68, 78–81] Natural history here is capable both of making social examples and of correcting exemplary stories. Blake's lost mother need not be reduced to either a lesson in industriousness or a report about ant behaviour. Her interrupted journey places need before usefulness, although the glow-worm's assigned watch still permits a reading through established social offices.

![A Dream. Bentley plate 26; Archive object 26; Erdman E16; accession 17.10.26. Vegetation passes around and between the stanzas; the small lower-right figure remains uncertain. William Blake, Songs of Innocence and of Experience, copy Y; work [1794], printed ca. 1825 (Archive: 1825). The Metropolitan Museum of Art, Rogers Fund, 1917. Public Domain / Open Access (CC0). Whole captured scan proportionally resized; no recolouring, rotation or taxon identification from ornament.](assets/met-347935-whole.png){#fig:songs_dream height=155mm}

## 4.2. A human consolation and an injured fly

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

“The Fly” makes the relation between text and design more difficult. In copy Y, a large adult figure bends towards a small child and holds its raised hands. At the left another figure raises a racket towards a shuttlecock-like object. Trees enclose the group, and the poem occupies two upper columns. The most legible bodies are thus human bodies engaged in play and support, not an anatomically resolved fly. [@blake-songs-y-2026, plate 40, object 40, physical lines 3–22; Met 17.10.40] These actions can intensify the analogy between human and insect play. They can also expose a disparity: the child is visibly supported, whereas the creature brushed away has no comparable helper within the depicted scene. Neither possibility proves that the adult illustrates the speaking “I.” The design instead keeps care, diversion and vulnerability beside a poem whose ending returns to the speaker's happiness. The fly's fate remains less fully told than the human argument made from it.

![The Fly. Bentley plate 40; Archive object 40; Erdman E23; accession 17.10.40. Human support and racket play coexist with the poem’s named fly; the shuttlecock-like mark is not identified as a fly. William Blake, Songs of Innocence and of Experience, copy Y; work [1794], printed ca. 1825 (Archive: 1825). The Metropolitan Museum of Art, Rogers Fund, 1917. Public Domain / Open Access (CC0). Whole captured scan proportionally resized; no recolouring, rotation or taxon identification from ornament.](assets/met-347974-whole.png){#fig:songs_fly height=155mm}

## 4.3. A worm whose identity remains unsettled

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

The design of “The Sick Rose” offers bodies without making the poem a diagnostic report. In copy Y, thorned stems and serrated leaves enclose the text; small bent figures occupy the upper vegetation. A larger exposed human form curves out of the lower blossom beside a narrow, bent, apparently segmented shape. A detail crop permits closer inspection of that adjacency, but not a secure species identification. The bodily and botanical forms overlap too closely for the design to supply a simple labelled predator and host. [@blake-songs-y-2026, plate 39, object 39, physical lines 3–10; Met 17.10.39] In the verse, the worm's destructive movement is explicit while its invisibility is part of the problem. Giving the design an unqualified zoological label would prematurely close the uncertainty through which the verbal address works.

Michael Srigley supplies a substantial counterreading to a straightforward encounter with an insect. He connects the nocturnal worm to traditions of spectral beings and to Paracelsian explanations of illnesses produced by disordered imagination. On his account, sexual repression and solitary fantasy make the destructive love intelligible. The article reconstructs several possible channels through which Blake might have encountered such ideas, but does not demonstrate a particular act of reading the proposed source. [@srigley-1992, pp. 4–8] Its historical hypothesis should remain a hypothesis. Nevertheless, it changes the question: the creature may embody the damage of a social and imaginative relation rather than describe an external organism entering an otherwise innocent world.

That alternative need not expel the animal word from consideration. The poem can be an invertebrate passage precisely because the worm's available senses are being made unstable. A literal animal reading must explain the secret love; a sexual or psychological reading must explain why this injury takes worm-like, nocturnal and mobile form. The two stanzas are not a code with one expendable noun. Their second-person address also matters: the rose is told of its sickness and destruction, but does not answer. The reader hears an attribution of harm rather than an exchange in which both parties describe their relation.

![The Sick Rose. Bentley plate 39; Archive object 39; Erdman E23; accession 17.10.39. Human, floral and narrow bent forms overlap; the design does not diagnose the invisible worm. William Blake, Songs of Innocence and of Experience, copy Y; work [1794], printed ca. 1825 (Archive: 1825). The Metropolitan Museum of Art, Rogers Fund, 1917. Public Domain / Open Access (CC0). Whole captured scan proportionally resized; no recolouring, rotation or taxon identification from ornament.](assets/met-347973-whole.png){#fig:songs_rose height=155mm}

## 4.4. Feeding on a compromised growth

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

“The Human Abstract” resists the opposite simplification, in which insects always stand for persecuted innocence. Its caterpillar and fly feed on Mystery after Cruelty has prepared a snare, watered the ground and brought forth rooted Humility. The final stanza locates the tree in the human brain. In copy Y, an aged, bearded figure raises his arms amid cord-like forms under the text; a dark trunk and projecting growths occupy the margins. These visible relations support an interpretation of entanglement, without requiring the figure to be named or the cords to be identified as an insect web. [@blake-songs-y-2026, plate 47, object 47, physical lines 3–26; Met 17.10.47]

The opening attack on pity that depends upon making another person poor prevents compassion from remaining an unexamined virtue. Read beside “A Dream,” it asks whether assistance answers a prior need or benefits from maintaining dependence. The feeding insects are implicated in a growth whose nourishment is morally compromised; they do not independently explain its origin. This distinction keeps appetite from becoming either automatic guilt or automatic innocence. What matters is the relation between feeding, the conditions that sustain it, and the voice that makes those conditions intelligible.

![The Human Abstract. Bentley plate 47; Archive object 47; Erdman E27; accession 17.10.47. An aged figure raises his arms among cord-like forms; neither a character name nor an insect web is inferred. William Blake, Songs of Innocence and of Experience, copy Y; work [1794], printed ca. 1825 (Archive: 1825). The Metropolitan Museum of Art, Rogers Fund, 1917. Public Domain / Open Access (CC0). Whole captured scan proportionally resized; no recolouring, rotation or taxon identification from ornament.](assets/met-348001-whole.png){#fig:songs_abstract height=155mm}

## 4.5. Bodies on leaves, figures in flight: edition-specific witnesses

Two leaves from *For Children: The Gates of Paradise*, copy E, complicate a reading of Blake's invertebrates as either zoological specimens or freely interchangeable symbols. Yale's frontispiece, *What is Man!* (B1978.43.1484), places an arched, segmented creature above a leaf bearing a human-faced, tapering body. The juxtaposition makes larval and human forms available to the same act of looking. It does not identify a species, demonstrate a biological transformation, or establish that the two bodies are successive states of one individual. The human face matters: comparison does not require an observer to erase the particular being whose vulnerability makes the comparison consequential [@ycba-gates-man-1793].

The accompanying text must be kept specific to its witness. The inspected copy-E impression carries the question and a publication inscription dated 17 May 1793. It does not carry the light-and-organ couplet that ASU's Erdman transcription presents under the frontispiece of *For the Sexes* (E260). The latter transcription also places “The Catterpiller on the Leaf / Reminds thee of thy Mothers Grief” before the numbered *Keys* (E268). The spelling is already represented in the declared retrieval vocabulary; this reading supplies no newly discovered lexical form. More importantly, a later textual frame is not silently printed onto an earlier photographed leaf. The mother's grief directs attention to embodied dependence, while the face and leaf keep that dependence materially visible. Neither observation turns an emblematic body into a taxonomic identification [@blake-gates-asu].

Yale's *Alas!* (B1978.43.1492) supplies a different difficulty. A larger human figure raises a hat; small airborne forms occupy the space above, while another small humanoid figure lies below. The gesture and the fallen body invite comparison with the casual force of the hand in *The Fly*, but that is a proposed reading across works, not proof that the smaller figures are flies. Human proportions, aerial movement and insect association can coexist without resolving into one literal animal referent. A record can preserve that association while declining a species or order-level assignment [@ycba-gates-alas-1793].

Here, too, numbering and text diverge across documentary frames. The museum calls the object plate 9; the photographed leaf displays 7 below the image and a separate handwritten 8 above it. ASU's *For the Sexes* transcription labels the corresponding passage 7 (E263), surrounding *Alas!* with additional wording about the figures and the divine image. Those additions are not visible on the inspected copy-E leaf. A usable locator therefore records the work, copy, accession and numbering system together. “Plate 7” alone cannot do the work of all four.

Höltgen places *Gates* beside emblem-book practices while stressing how its compressed captions complicate a conventional emblem's explanatory closure. That argument offers a relevant counterweight to treating the designs as illustrated natural history: a caption, an image and an interpretation are related evidence, not synonyms. The present comparison adopts neither a general influence claim nor a complete decoding of Blake's figures [@hoeltgen2002].

Höltgen's specific reading gives the alternative more force: his butterfly-girls and the youth's capture place the scene within a mortal, spiritless material existence. That is a serious challenge to treating aerial motion as uncomplicated liberation. His quoted expanded wording is a different documentary frame from this early leaf's sparse caption. The photograph cannot settle his whole interpretation, nor can the interpretation establish a taxon. The conjunction of gesture, fallen body and later verbal framing remains a literary argument rather than a recovered observation of insects. [@hoeltgen2002]

These two selected objects extend the visual casebook rather than the fixed corpus analysis. Their official photographs and object records have separate hashes, credits and rights statements. Museum-supplied recto crops retain the complete engraved designs and captions; the wider captures with calibration targets remain available for inspection. The two objects count as two witnesses, not as multiple witnesses for each digital rendition. They add no baseline text hits and no formal textual adjudications. Their methodological contribution is narrower: preserve an association when it is warranted, preserve an unresolved identity when it is not, and make the edition-specific evidence recoverable.

![Two objects from *For Children: The Gates of Paradise*, copy E, catalogued 1793. Left: *What is Man!*, frontispiece, B1978.43.1484. Right: *Alas!*, museum plate 9, B1978.43.1492; the leaf displays 7 below the image and handwritten 8 above. The later wording discussed in the text is not present on these photographed leaves. Yale Center for British Art, Paul Mellon Collection; museum records label both Public Domain and link CC0. Museum-provided recto crops, with complete designs and captions; no author recolouring or reconstruction. These are selected literary and visual witnesses, not species identifications.](assets/gates-copy-e-comparison.jpg){#fig:gates_copy_e width=98%}

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

This juxtaposition changes how the wine-press inventory can be used. The abundance of named life around the press does not ensure that every participant occupies a position of reciprocal benefit. The inventory must remain beside the human grapes and their suffering. [@blake-milton-a, object 24, physical lines 2–42] Nor does the mere presence of predation establish cruelty in the same sense as a deliberately inflicted injury. The article can instead follow three separate relations: the provision that enables another life, the feeding that uses a living body, and the aggregation that reorganizes its members' powers. Their overlap is an interpretive problem, not evidence that they are morally identical.

# 6. Taxonomic uncertainty and collective bodies

## 6.1. Recognition through the infant analogy

The earlier bounded reading of copy B, objects 6–7, physical lines 3–14 and 2–18,
remains a separate textual witness. It established the movement from a bruising
foot to positive nurture, with maternal and nuptial language qualifying any
universal social doctrine. The following F/O comparison extends that local
question through independently identified material witnesses. [@blake-thel-b]

The Worm's presentation in *The Book of Thel* brings analogy into the act of recognition. Thel asks what she sees, calls it weak, compares it to an infant, and hears weeping where articulate speech is unavailable. In both reproduced impressions of Bentley plate 6, an infant-like body rests among long leaves below a floating figure and beside a standing, gowned figure with extended arms. The bodily scale and placement make vulnerability visible before they permit any zoological resolution. [@blake-thel-f-2026, object 6, physical lines 2–13; @blake-thel-o-2026, object 5, physical lines 4–15] The scene can awaken concern by translating another life into a familiar human form. It can also make that concern conditional upon resemblance to a child. Recognition through analogy is consequently an ethical achievement with a limit, rather than transparent access to the Worm's own experience.

The response attributed to the Clay changes the situation. Thel's statement that no one cherishes the helpless being is answered by care already becoming active. In the following reproduced plate from copy O, a reclining figure and an infant appear below the poem and in front of a larger seated figure. The spoken acknowledgment distinguishes a prohibition on wilful bruising from the positive provision of milk and oil. [@blake-thel-o-2026, object 6, Bentley plate 7, physical lines 3–19] A community of care is measured here by what sustains a dependent life, not merely by punishment after injury. Yet maternal, nuptial and hierarchical language shapes that provision. The passage cannot by itself guarantee equal participation or make an obligation to nurture independent of its gendered terms.

Perkins places the infant Worm within a contemporary rhetoric that mobilized tenderness towards humble creatures, while preserving the possibility of irony in the poem's surrounding world. [@perkins-1999, pp. 5–6] That caution helps prevent the scene from becoming a frictionless model of mutual flourishing. Care can be real within the local exchange even if its speakers cannot settle Thel's larger unease. The selected plates support an account of this exchange; they do not settle the meaning of every stage of her journey.

The copies themselves also require different forms of attention. Rosenwald 1798A is copy F, object 6; Rosenwald 1798B is copy O, object 5. Both are Bentley plate 6, corresponding to Erdman plate 4. Object 6 in O is instead Bentley plate 7. In the matched reproductions, F gives the standing figure a conspicuous yellow gown against a relatively continuous ochre upper field, while O shows a paler gown and a more extensively lined and coloured setting. O's painted enclosure is more pronounced. These are observations about the captured images. Unequal reproduction conditions, paper condition and colour management prevent attributing every tonal difference to an intentional revision. The repeated arrangement is an anchor for comparison, not permission to merge the two impressions into a single generic image of *Thel*.

![One plate in two material witnesses. William Blake, The Book of Thel (work imprint 1789), Bentley plate 6 / Erdman plate 4. Left: copy F, Archive object 6, LOC Rosenwald 1798A; Archive printing 1795, LOC ca. 1794 (1794 watermark). Right: copy O, Archive object 5, LOC digital Rosenwald 1798B; Archive c. 1818, LOC ca. 1815 (1815 watermarks). O is bound with Milton D under Archive catalogue no. 1810; that volume number differs from its digital subresource. Library of Congress, Rare Book and Special Collections Division, Lessing J. Rosenwald Collection. Historical public-domain artwork; LOC states no known US copyright or other restrictions, with user determination required. Whole scans proportionally resized; neither physical scale nor photographic colour is calibrated.](assets/thel-bentley6-two-copies.png){#fig:thel_copies width=98%}

![Care beyond the prohibition of injury. William Blake, The Book of Thel (imprint 1789), copy O, Archive object 6, Bentley plate 7 / Erdman plate 5; LOC digital Rosenwald 1798B, bound with Milton D, Archive catalogue no. 1810. Archive printing c. 1818; LOC ca. 1815. A reclining figure reaches towards an infant-like body beneath the selected Clay/Worm exchange. Library of Congress, Rare Book and Special Collections Division, Lessing J. Rosenwald Collection. Historical public-domain artwork; LOC no-known-US-restrictions statement retains user-determination qualification. Whole captured scan proportionally resized. This is the following plate, not a second copy of Bentley plate 6.](assets/thel-o-006-whole.png){#fig:thel_care height=165mm}

## 6.2. Generation and the powers of a collective body

The historical polypus should first complicate the word “individual.” In the second edition of *Zoonomia* examined here, Erasmus Darwin describes young polyps branching from a parent's side and subsequently separating. He compares them with vegetable buds and interprets their generation through a theory that assigns formative priority to the male. Elsewhere in the same discussion, gnats and tadpoles become examples of bodily transformation, while the polypus remains associated with budding. These statements belong to Darwin's historical physiology, including assumptions that cannot be accepted as modern zoological description. [@darwin-zoonomia-1796, vol. I, section XXXIX.II.3 and XXXIX.IV.2] They nevertheless show why generation could bring together questions about attachment, separation, sexual difference and the production of new powers.

Dauphin's extended Blake discussion traces the poetic reworking of this complex into vegetation and collective bodies. Her reading connects the multiplication of organic forms to a danger of losing distinct identity. Her argument also insists that the scientific creature and its poetic transformations are not interchangeable. [@dauphin-2026-expanded, paragraphs 7–28] It is useful as an account of transformation across discourses. It does not independently establish that any particular branching ornament in an illuminated book depicts a polypus, nor prove a single direct route from Darwin to every occurrence in Blake. The reproduction of a *Thel* infant and the mention of a prophetic Polypus remain different evidential objects.

In the selected *Milton* passage, the joining of every born man into one Polypus is situated within vegetated nerves, wailing souls and changes in perception. The figure is named Orc in the same sentence; the surrounding lines relate Orc, Satan and Luvah rather than leave a stable zoological emblem. [@blake-milton-a, object 28, physical lines 24–35] The problem is not simply that many lives are connected. It is what connection does to their capacities to perceive, act and remain distinguishable. The emmet's helpers retain separate offices and answer a particular voice; the prophetic passage joins persons within a body whose powers exceed any isolated participant. That contrast is locally supported, but the named transformations make a universal opposition between good networks and bad organisms too blunt.

Erasmus Darwin's later *Temple of Nature* further unsettles a simple opposition between scientific materialism and ethical attention. Its third canto brings human pride down towards kinship with emmets and worms after considering insect construction, sensation and volition. Its fourth canto presents feeding across animal and vegetable life as pervasive destruction, extending appetite to creatures conventionally imagined as gentle. [@darwin-temple-1803, canto III, lines 411–434; canto IV, lines 1–66] Kinship and violence therefore inhabit the same natural history. Fara's reading of these passages emphasizes the coexistence of ethical cooperation, progressive development and an account of death that regulates abundance. Her analysis also distinguishes Erasmus's historical explanations from the later theory of his grandson. [@fara-2020, paragraphs 21–23, printed pp. 10–12]

Dauphin's account of the changing Polypus makes it especially important to
distinguish the biological animal, the poetic figure and later iconographic
interpretation. The Archive's copy-A Milton descriptions also retain alternative
identifications: object 24 can be described through caterpillar/centipede and
beetle/bee/hornet alternatives, while object 31 permits vegetable/Polypus
possibilities. A catalog's alternatives cannot become several confirmed
depicted species. Those copy-A descriptions have been read; the corresponding Milton
images have not been inspected in this expansion. [@dauphin-2026-expanded];
[Archive Milton A](https://raw.githubusercontent.com/blakearchive/data/7063e9ea8b13d18bd5a585e87610164fd75d3f60/works/milton.a.xml).

Historical lexicography remains an acquisition task. The comparison advanced
here asks what joining permits and suppresses in a particular scene. It does not
equate Blake's changing collective figures with modern political institutions.

# 7. Instruments, cruelty and the problem of evidence

## 7.1. Making a creature visible

The failed demonstration in *An Island in the Moon* is sharper when placed beside practical microscopy rather than an undifferentiated idea of science. In the second edition of Henry Baker's *The Microscope Made Easy*, the observer must suit illumination to the object, examine it in different positions and distinguish the image projected by a solar microscope from the body's natural colour. Baker also asks that a living animal be squeezed or disturbed as little as possible. His preparation instructions combine methods of holding creatures alive with pinning or other restraint when size requires it. [@baker-1743, pp. 53–58] The manual does not stand outside human use of animals; it makes the conditions of useful visibility explicit, including the tension between preserving a creature's behaviour and securing it for inspection.

In Blake's chapter 10, by contrast, the speaker offers a louse, flea, butterfly or cockchafer before water, a smearing handkerchief, broken apparatus and a panicked account of escaped pestilence displace the promised demonstration. The sequence is not a successful observation followed by an abstract objection to empirical knowledge. It is a performance in which the promised objects never become reliable shared evidence. [@blake-erdman-retained-expansion, E462, provider record 474, chapter 10 only] Baker's practical cautions make the failure legible without making his manual a demonstrated source for the satire. Both texts allow the means of seeing to matter; they give those means very different dramatic and argumentative functions.

## 7.2. Injury, judgment and the limits of metaphor

“Auguries of Innocence” poses a further difficulty: what should follow when injury has been noticed? Perkins argues that its animal auguries voice innocence confronting cruelty and threatening consequences that exceed ordinary causal explanation. He also warns that treating a tormented creature solely as a metaphor can diminish attention to the animal's suffering. These are interpretive positions, not an uncontested identification of the poem's voice. [@perkins-1999, pp. 7–10] They encourage keeping literal injury present while examining the form in which a speaker makes it consequential.

The boy who kills the fly is threatened with the spider's enmity. This is not simply a food-chain statement: the two-line address assigns a consequence to a human act. Yet the creature associated with catching flies becomes the figure through which killing a fly is answered. Elsewhere the caterpillar repeats maternal grief, and the prohibition on killing moth or butterfly is attached to judgment. [@blake-erdman-retained-expansion, E490–491, records 502–503; “Auguries,” lines 33–40] The sequence crosses animal behaviour, familial feeling and eschatological warning without making them interchangeable. A consistently gentle insect world would have no place for the spider's enmity; a purely predatory one would lose the address to the boy. The poems considered here make small lives matter through those unresolved relations between attention, use, obligation and response. Their ethical force depends on retaining the differences that a single animal-symbol key would erase.

The sequence also includes gnat, bee, cricket and emmet, but a lexical resemblance
need not name an animal. The *Mite* at E492 is an amount extracted from labour,
not an arachnid. Broad retrieval preserves that negative control. Its retained
locator is record 504; this expansion adds no new reading credit for that page.
The distinction between use, deliberate cruelty and metaphor requires a speaker,
a predication and a setting, not merely a noun. [@blake-erdman-retained-expansion]

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

### Composition across name families

The current installed composition run independently recomputes the full captured atlas, the primary counted inventory and the earlier literal grid before producing the new composition and proximity exports. Numerical equality preserves the historical producers; a separate run binds the current SDK and application source bytes. The checks add no contextual animal decisions or image identifications.

The historical registry partitions into 82 name-family categories, four broad
labels, 15 associated channels and one motion channel. “Name-family” here means
the registry groups for worms, insects, arachnids, myriapods, molluscs,
crustaceans and ambiguous life. It preserves historical retrieval policy rather
than imposing a new biological classification. Thus it retains *blindworm*,
*spinner*, *sponge*, derivatives of *worm*, and the noun/verb ambiguity of *fly*.
It must not be read as a set of adjudicated animal nouns. The other channels
retain generic labels, products, structures, parts and actions in their own
declared groups.

For each name-family category, the complete matrix reports candidate counts,
matched retained units, the eligible unit denominator and NFKC token denominator
in every recorded group, including zeros. Within-group composition divides each
category's count by that group's sum of name-family category candidates. Pooled
composition divides pooled category counts by the total name-channel mass. The
equal-group composition averages the normalized profiles of groups with positive
name-channel mass. A group containing no name-family candidate has undefined
composition; it remains a zero in coverage exports and is excluded from this
particular mean. This differs from equal-work token rates, whose denominator is
text length and whose zero-match groups can contribute defined zero rates.

We measure profile differences by total variation: one half of the sum of
absolute differences between corresponding category shares. The same distance
compares the full pooled profile with the profile remaining after omission of
each entire recorded group. These distances express redistribution of
category-candidate mass, not uncertainty about Blake's oeuvre. Concentration is
also reported as the smallest number of descending-count groups needed to
account for one half or four fifths of a category's mass, and as inverse
Herfindahl concentration. The latter is an effective number of equally weighted
groups, not a number of independent works.

Categories and overlapping spans remain separate throughout. A compound and
its component may each contribute a category candidate; the denominator is a
sum of category candidates, not distinct animal words or organisms. Exact-text
sensitivity comes from the shared SDK's grouping of identical complete source
units. It does not remove repeated poems embedded in different whole texts.

The relationship analysis declares twelve exploratory pairs of singular literal
terms and applies complete word envelopes of 8, 32 and 64 words. Whole-unit
co-presence is a separate scope. Public SDK matching and proximity APIs retain
original text boundaries and count matching units before any display cap.
Their 644,245 original-text word tokens remain distinct from the NFKC
denominator. These literal pairs do not expand to every form of their similarly
named categories: *emmet* is narrower than the *ant* family, and *caterpillar*
does not silently include historical alternative spellings.

Let $c_{gw}$ be the category-candidate count for name family $g$ in group $w$,
and $m_w=\sum_g c_{gw}$. The three profiles are

$$
p_{gw}=\frac{c_{gw}}{m_w},\qquad
P_g=\frac{\sum_w c_{gw}}{\sum_w m_w},\qquad
Q_g=\frac{1}{|W_+|}\sum_{w\in W_+}p_{gw},\quad W_+=\{w:m_w>0\}.
$$

For normalized profiles $P,Q$, total variation is

$$
\operatorname{TV}(P,Q)=\frac12\sum_g|P_g-Q_g|.
$$

For a positive category, let $s_{gw}=c_{gw}/\sum_v c_{gv}$. Its effective number
of groups is inverse concentration,

$$
N_{\mathrm{eff},g}=\left(\sum_w s_{gw}^{\,2}\right)^{-1}.
$$

A zero-mass category has no defined concentration; Appendix A displays that state
explicitly. These formulas describe retained category mass, including shared
and nested spans, rather than independent works or individual animals.

The 82 name-family categories yield 1,239 primary category-span candidates in
26 of the 33 recorded groups. Thirty-eight categories have positive counts;
44 remain zero in this primary inventory. The associated channels contribute
1,087 further candidates, the motion channel 156, and broad labels 16. Their
sum reproduces the 2,498 primary candidates. Name-family queries therefore
account for 49.60% of the primary category-candidate mass, rather than all of
the concordance. Exact whole-text grouping reduces name-family candidates
from 1,239 to 1,238. The changed category is *mussel*, from 13 to 12. That
narrow change does not establish that the remaining copies represent distinct
contexts.

The pooled and equal nonempty-group name compositions have total variation
0.222387. The *fly* share rises from 14.7700% pooled to 24.3951% under equal
composition weighting, a change of +9.6251 percentage points. *Worm* falls from
37.7724% to 33.7732%, or −3.9992 points. *Beetle* falls from 5.0040% to
1.7664%, and *Polypus* from 5.8918% to 3.5986%. These changes answer a
different question from the earlier rate comparison: they redistribute a fixed
name-channel profile rather than comparing candidates per text token.

Two smaller categories expose the cost of normalizing sparse groups. *Mussel*
rises from 1.0492% pooled to 7.6923% in the equal-group profile. Its one
candidate in `ahania` and twelve in `america` exhaust the name-channel mass in
those two groups, so each contributes a complete within-group share to that
category. A bounded inspection of the retrieved *Ahania* context finds the
surface “muscles” among bodily formations, not a contextual mollusc
identification. Similarly, the single *mayfly* candidate contributes one half
of the name-channel profile in `but828`; it is the normalized sequence
“may … fly” in the captured *Genesis* transcription. The surrounding reference
is to fowl and flight. These inspected retrieval ambiguities explain why
equal weighting cannot serve as an automatic correction toward a truer animal
census. They also caution that the recorded author/role field is an eligibility
rule, not a fresh attribution of every transcribed word to Blake.[^contexts]

The three largest omission effects are `songsie` (total variation 0.119982),
`thel` (0.103325) and `milton` (0.079001). They remove, respectively, 217, 203
and 168 name-family category candidates from the pooled profile. These groups
do not simply contribute the most textual mass: `thel` contains 23,019 NFKC
tokens, whereas `jerusalem` contains 197,560 tokens and its omission distance
is 0.051693. Composition influence depends on a group's lexical profile as
well as its size. *Worm* remains the largest pooled category after every
single-group omission. That finite robustness of the leading category coexists
with substantial changes in the rest of the profile.

Concentration measures further distinguish visibility from breadth. *Worm*
and *fly* each occur in 15 recorded groups, but their effective group counts
are 5.008 and 2.889. Five groups are needed to accumulate four fifths of
*worm* candidates, compared with four for *fly*. *Polypus* occurs in three
groups and has an effective count of 2.030; two groups suffice for four fifths
of its candidates. These numbers locate concentrations in this retained
collection. They do not count distinct literary episodes or establish the
independence of copies.

![Composition and group influence. The sixteen largest share shifts compare the pooled name-channel profile with the mean of 26 nonempty-group profiles (1,239 category candidates); all 33 groups remain eligible for omission. The twelve largest omission distances describe redistribution of this finite inventory. Parentheses retain candidate counts. Complete data and all omissions are supplemental; no sampling inference or animal adjudication is implied.](assets/02-composition-influence.png){#fig:composition_influence width=98%}

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

### Twelve source-sensitive literal pairs

The literal-pair audit makes source dependence visible alongside distance.
*Worm + fly* matches four units from one group at eight words, 28 units from
three groups at 32 words, and 66 units from six groups at whole-unit scope.
At 32 words its 28 units divide into four `jerusalem`, eight `songsie` and
sixteen `vda` units. Thus a comparatively large unit count can be supplied
by very few recorded groups. These cells identify where a contextual comparison
should begin; they do not establish 28 distinct nearby encounters.

The contrasts differ across pairs. *Worm + beetle* increases from four units
at eight words to 31 at 32 words, with no further increase at 64 words or
whole-unit scope. Its 32-word matches comprise four `milton`, thirteen `s-inn`
and fourteen `songsie` units. *Emmet + beetle* matches only the four `milton`
units through 64 words but reaches 31 units at whole-unit scope. A shared
source document therefore supports a much broader relation than a nearby
word envelope in the latter case. *Spider + fly* has no eight-word match,
sixteen 32-word matches entirely in `vda`, and 24 whole-unit matches from
three groups.

Other contrasts resist a simple relationship graph. *Bee + beetle*,
*gnat + fly*, *Polypus + worm* and *scorpion + centipede* have zero matches
through 64 words but respectively four, five, eight and four whole-unit
matches. *Flea + louse* matches five units from two groups at every declared
scope. *Moth + butterfly* matches one unit from one group throughout.
*Caterpillar + fly* returns zero even at whole-unit scope under the declared
singular literal spelling, despite 36 primary candidates in the broader
*caterpillar* category. A zero in this experiment is consequently a result
of a stated query, eligibility rule and source inventory, not an absence claim
about Blake or the scene discussed elsewhere in this article.

Appendix B prints all twelve pairs, including every zero, with matched units and
contributing group counts. The full 82-by-33 matrix and twelve-pair source matrix
remain vector/CSV supplements; neither is reduced to unreadable page labels here.

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

Unverified Archive XML supplies
32,066 of all 36,039 candidates, or 88.98%, including 11,597 name-family,
12,485 associated, 5,993 motion and 1,991 broad-label candidates. Its 51
positive name-family categories exceed the primary reading scope's 38, but
this additional retrieval reach includes markup and modern catalog language.
It cannot enlarge the number of Blake-authored animal attestations by simple
addition. Mixed Erdman material, four mixed XML units and unverified reading
documents remain separately reported, with their own token and unit denominators.

![Query channels across source cohorts. Panel counts and within-cohort shares distinguish 82 name families, four broad labels, fifteen associated channels and one motion channel. Every role/plane/author cohort retains source-unit and NFKC-token denominators. These disjoint cohorts describe retrieval populations, with markup and editorial language retained separately; they are not stages of complete-oeuvre coverage.](assets/04-query-channel-source-audit.png){#fig:query_channels width=98%}

Positive/declared category totals are tabulated separately below; they are not printed within the preceding panel. Each entry is a count of positive categories divided by the complete declared channel. The bound data location is `assets/source-channels.csv`, columns `observed_categories` and `categories`; neither column counts reviewed animals.

{{SOURCE_CHANNEL_TABLE}}

## 8.6. Reading coverage is a different denominator {#sec:reading_coverage}

The new casebook records {{CASEBOOK_CASES}} bounded interpretive cases and
{{COMPLETE_POEMS}} complete short-poem transcriptions: “A Dream,” “The Fly,”
“The Human Abstract” and “The Sick Rose,” all in copy A. It separately records
the inspected Milton and Thel passages and the modern catalog alternative.
Ordered line IDs and selected-text hashes close those reading claims. These are
reading receipts, not additional candidate decisions. The
{{HISTORICAL_REVIEWED}} historical decisions remain on their original run.
{{HISTORICAL_UNREVIEWED}} candidates were unreviewed in that historical eleven-decision epoch. None has been reclassified or rebound to this atlas. The atlas still has zero authored decisions. The additive baseline review described next reaches {{CONTEXT_REVIEW_TOTAL}} decisions and leaves {{CONTEXT_REVIEW_REMAINING}} candidates unreviewed. Across the visual casebook, {{SELECTED_IMAGE_WITNESSES}} selected historical originals have been inspected. The corpus-wide
image inventory remains unreviewed. Four complete copy-Y poem transcriptions and
selected Thel F/O passages belong to the additive expansion ledger; they inherit
no credit from the earlier copy-A and Thel-B readings.

This separation also sets a limit on the argument. The small lyric sequence can
now be discussed through its ending, whereas the Polypus and wine-press cases
remain local passages. The contrast between practical assistance, conditional
consolation, secret destruction, nurture and bodily aggregation has support in
these selected contexts. It has not been established as a distribution of
functions across all of Blake. The machine audit supplies the next places to
read, and preserves the places where it cannot yet support a claim.

[^contexts]: Fresh local inspection was limited to the SDK's 120-character
    context on each side of two hits. *Ahania*: `archive:ahania.a`, reading-layer
    locator lines 1–259, original character interval [5617,5624), source SHA-256
    `fa95577f5790fc5d2cba1ff08822d79b59d2399f352e2a7f477d891868395761`.
    *Genesis*: `archive:but828.1`, reading-layer locator lines 1–230, interval
    [3089,3114), source SHA-256
    `ef98f4fa8c09feca8dee00110b7a844a7af1a1bf8ddbc7edd9b5aefc96fd6967`.
    The broad reading-layer line ranges are unit locators, not exact verse-line
    locators for these hits. Neither inspection credits a complete work or design.

## 8.7. Contextual decisions test the concordance without becoming a census {#sec:context_review}

A new, declared batch of {{CONTEXT_REVIEW_NEW}} candidate IDs was inspected in
bounded original-source windows and coded by a research agent on 29 October
2026. Selection preceded coding and deliberately included personified animals,
concrete animal senses, products, motion verbs and modern catalog descriptions.
It was purposive rather than random. Each judgment names the reviewer,
rationale, original interval, inspected window, window hash and exact historical
run pin. It therefore supports inspection and disagreement, not a claim of
specialist consensus, classifier accuracy or animal prevalence.

The actual review command validates {{CONTEXT_REVIEW_TOTAL}} decisions after
combining the new batch with the unchanged eleven historical decisions:
{{CONTEXT_REVIEW_REMAINING}} of the original 36,039 candidates remain unreviewed.
The combined dispositions are shown below. Literal and figurative animal codes
retain their separate meanings; the distinction concerns the selected use of a
word, not a division between scientifically true and false poetry.

{{CONTEXT_REVIEW_TABLE}}

![{{CONTEXT_REVIEW_CAPTION}}](assets/context-review.png){#fig:context_review width=98%}

The new 36 IDs occupy 23 retained source units and 23 recorded work groups.
The combined 47 occupy 28 source units and 25 groups. These are documentary
counts, not independent poetic events. Two new same-source window pairs overlap:
the busy-bee and spider/friendship proverbs in *The Marriage of Heaven and Hell*
(E29-06/19), and the dungeon spiders and eternal worm in *The French Revolution*
(E29-17/27). The *Milton* emmet returns to the wine-press inventory already
represented by historical Erdman seeds; the new “Auguries” fly window also
contains historical spider/bee aphorisms. Distinct candidate IDs and 36 distinct
window hashes preserve these relations rather than converting repetition into
independent observations. Selection IDs and exact memberships are in the dated
study ledger.

Disambiguation changes what a retrieval can support. Four new primary-reading
candidates use *fly/flies* as a verb: personified Strife moves abroad, Hermes flies
before Jupiter, Pestilence leaves a broken bottle, and the Genesis transcription
speaks of fowl flying. Nearby insects or buzzing do not turn the selected verb
into an animal noun. Four additional matches belong to modern XML design
descriptions: birds, angels, Justice and an eagle supply the movement. These are
coded editorial while their original source role remains unverified. A semantic
judgment does not promote a catalog description into Blake-authored verse.

Positive animal coding also needs a rival reading. The bee's lack of sorrow is
an ethical proverb, not an assay of insect emotion; the wise emmet's dance in the
wine-press belongs to a structure explicitly joined to war and printing. The
selected dungeon spiders can have a concrete animal sense within political
allegory without supplying a natural-history observation. Conversely, honey
bees that sing in a transformed landscape, the Spider created to help the
Daughters' labour of pity, and the eternal worm in a chained skeleton remain
uncertain between available literal and figurative modes. Leaving those three
new judgments open is a result of contextual reading rather than a missing
keyword rule.

The associated codes sharpen the article's account of provision and capture.
Honey on infant lips and the Lilly's honey-bearing perfume connect nourishment
to vulnerable bodies without asserting a bee at the matched span. Oothoon's
silken nets, proposed for catching girls, make a different relation possible:
a connective material can enable confinement. The Web of Life in *Gates*
joins sexual strife, tears and kinship without identifying a spider. Thus neither
material production nor a network is sufficient evidence of care. What matters
is who can act, who is sustained, and who becomes an object of another's
activity. The single disposition labels expose semantic boundaries; they do
not exhaust the passages' literary functions.

These decisions remain attached to the original baseline run. The later atlas,
its 102-category/376-form vocabulary audit, and the 82-family composition epoch
are unchanged and gain no retroactive adjudication. The new figure is a
description of authored decisions and their source channels, not a validation of
all candidates. The next defensible extension is an independently reviewed,
explicitly designed batch across further works and senses, retaining the
unresolved labels and the entire unreviewed denominator.


# 9. What remains before a comprehensive account

The software establishes complete matching of the declared forms within the
pinned units. A comprehensive literary account still requires candidate
adjudication, work/copy reconciliation, examination of source boundaries,
assessment of unlisted or unnamed animals, and a systematic visual inventory.
Long-range discussion can exceed the saved 120-character context envelope;
review must return to the complete source unit and, where necessary, its
neighbours and physical object. Animal-coded candidates from editorial source cohorts remain exploratory
until the quoted text's author and location have been established separately.

Mike Goode's discussion of digital fragmentation is pertinent to the research
design: retrieving a textual fragment can detach it from the verbal-visual work.
The present concordance is therefore a navigation instrument. An argument
requires returning from its fragments to their material and textual relations.
Only selected opening sections of Goode's essay were read here. [@goode-2016]

{{SELECTED_IMAGE_WITNESSES}} selected originals provide differential material witnesses, not a representative
visual census. The unresolved corpus image identifiers, other copies and
unnamed forms still require systematic inventory. The additional image readings create no textual decisions. The separate 36-case baseline batch supplies explicit, contestable decisions while preserving {{CONTEXT_REVIEW_REMAINING}} unreviewed candidates.

The article's provisional claim is consequently bounded but substantive:
invertebrate figures let these selected Blake passages test the relation between
attention to a life and the forms that connect, classify or absorb it. The
counterexamples are part of that claim. Sympathy, mockery, appetite, predation,
work and aggregation cannot be replaced by one stable animal-symbol dictionary.
The corpus application makes the further tests of this reading inspectable.

# References and reading status

The source ledger distinguishes complete short-poem readings from local
passages and from whole works. The four complete copy-A *Songs* transcriptions
and selected *Milton* A / *Thel* B windows remain historical credit. This expansion
adds four complete copy-Y poem transcriptions and seven selected scans, plus
local *Thel* F/O, *Island* and “Auguries” passages. It does not credit a complete
book, all copies or a comprehensive visual inventory.

Perkins (1999) and Srigley (1992) have now been read as complete journal articles
by the research owner. The earlier Perkins fetch failure remains in the frozen
ledger as acquisition history. Essick and Viscomi (2002) are used only for selected
opening and registration sections (pp. 74–76, 90–92); Dauphin's extended reading
covers paragraphs 7–28 and 49–50 alongside the earlier 3–6 and 21–25. Fara is
cited under the 2020 online publication date; its issue and PDF citation carry
2016 (Spring–Fall, nos. 66–67). Only paragraphs 15–23 were read.
[@perkins-1999; @srigley-1992; @essick-viscomi-2002;
@dauphin-2026-expanded; @fara-2020]

Gould (1747) is limited to the title and printed pp. 66–68, 78–81; Baker (1743,
second edition) to complete selected paragraphs on pp. 53–58; *Zoonomia* to the
1796 second edition, I.XXXIX.II.3 and IV.2; and *The Temple of Nature* (1803) to
III.411–434 and IV.1–66. These are historical comparisons, with neither whole-book
credit nor a proved influence chain. Schwartz remains publisher-abstract only;
Goode remains selected opening sections. Reading a scholar's article grants no
automatic credit for its cited books, manuscripts or images.
[@gould-1747; @baker-1743; @darwin-zoonomia-1796; @darwin-temple-1803;
@schwartz-2012; @goode-2016]

The additive reading, image-provenance and claim ledgers preserve source URLs,
selected paragraphs or ordered physical line IDs, source hashes and rival
readings. Original failed accesses and earlier decisions remain intact. New
source captures and binaries stay in private local custody.

The present edition adds two selected copy-E Gates objects, bounded ASU E260/E263/E268 passages, and Höltgen's selected Gates discussion; none receives complete-book or complete-article credit. The 36 new candidate windows carry separate agent-review credit and do not extend these complete-poem claims. [@hoeltgen2002; @blake-gates-asu]

# Appendix A. Complete name-family coverage

The table covers all 82 name-family categories in the 199-unit primary reading
scope (33 recorded work groups). Counts are category-source-span candidates;
matched units and positive groups retain copies. Half-mass groups is the minimum
number of descending-count groups accounting for at least half of a category’s
mass; a dash marks undefined concentration for a zero category. Associated
channels and broad labels are separate from this name-family table.

{{NAME_COVERAGE_TABLE}}

# Appendix B. Twelve literal-pair controls

Cells give matched units followed by contributing groups in parentheses.
Eight-, 32- and 64-word complete envelopes differ from whole-unit co-presence.
All cells use 199 eligible units and 644,245 original-text word tokens; singular
literal spellings do not inherit expanded category forms.

{{LITERAL_PAIR_TABLE}}

# Appendix C. Material-witness concordance

| Witness | Bentley / Erdman | Archive object | Repository identity | Printing date evidence |
|---|---|---:|---|---|
| A Dream, Songs Y | 26 / E16 | 26 | Met 17.10.26 | [1794], ca. 1825 |
| The Fly, Songs Y | 40 / E23 | 40 | Met 17.10.40 | [1794], ca. 1825 |
| The Sick Rose, Songs Y | 39 / E23 | 39 | Met 17.10.39 | [1794], ca. 1825 |
| The Human Abstract, Songs Y | 47 / E27 | 47 | Met 17.10.47 | [1794], ca. 1825 |
| Thel F, III | 6 / plate 4 | 6 | LOC 1798A | Archive 1795; LOC ca. 1794 |
| Thel O, III | 6 / plate 4 | 5 | LOC digital 1798B; bound volume 1810 | Archive c. 1818; LOC ca. 1815 |
| Thel O, Clay exchange | 7 / plate 5 | 6 | LOC digital 1798B; bound volume 1810 | Archive c. 1818; LOC ca. 1815 |
| What is Man!, Gates Children E | Museum plate 1; later E260 text separate | Not reconciled | YCBA B1978.43.1484 | Catalogued 1793; inscription 17 May 1793 |
| Alas!, Gates Children E | Museum plate 9; printed 7; handwritten 8; later E263 passage 7 separate | Not reconciled | YCBA B1978.43.1492 | Catalogued 1793 |

# Bibliography

The following references identify the cited scholarship, historical witnesses
and captured classification resources. The source ledgers retain exact reading
ceilings and snapshot hashes.

::: {#refs}
:::
