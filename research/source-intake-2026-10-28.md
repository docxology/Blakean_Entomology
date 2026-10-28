# Blakean Entomology: lexical scope and evidence intake

Observed 2026-10-28. Research memo for the new private application; no manuscript acceptance verdict and no claim of whole-oeuvre completeness.

## Scope decision

Use **Blakean Entomology** as the project title and explain its operational breadth: invertebrate lives and imagery in Blake, including insects, arachnids, myriapods, worms, molluscs, and biologically ambiguous forms. Entomology in its narrow biological sense covers insects; the requested corpus extends beyond that sense. Smithsonian descriptions distinguish insects from spiders and other arthropods, supporting separate biological groups in the annotation vocabulary. Do not make the title an excuse to drop the snail, centipede, scorpion, or Polypus. [Smithsonian, What Is an Insect?, transcript](https://naturalhistory.si.edu/education/teaching-resources/life-science/what-insect), especially body-plan paragraphs; [Smithsonian, Insect Zoo Audio Description Tour](https://naturalhistory.si.edu/visit/accessibility/audio-and-visual-description/insect-zoo-audio-description-tour), class descriptions.

The research question is a census and interpretation of **mentions and discussions**, not a census of insects living in Blake's environment. Literal, anthropomorphic, metaphorical, mythic, material/product, and disputed cases need separate labels. None is automatically an observation of a biological species. Keep the original term; assign the broadest defensible biological grouping and permit `uncertain` rather than forcing a species.

## What was actually read and inspected

- Verified the external GitVault volume was mounted before writing this memo.
- Read source interfaces in `blake/recovery_text.py`, `blake/text_search/models.py`, and relevant scope-filter references. Inspected the beginning of the recovery manifest and selected search/model documentation.
- Machine-screened the retained combined Erdman reading with case-insensitive word patterns; inspected selected surrounding passages, not every page. Queried the retained API JSON for page IDs. No full-volume reading credit is claimed.
- Opened official pinned Archive XML for `milton.a`, `songsie.a`, and `thel.b` with web tools; read header material and targeted search windows described below. Did not inspect physical plate images. No complete reading credit is claimed for those files.
- Read the Smithsonian insect transcript and departmental overview; inspected search-returned class descriptions from its Insect Zoo tour. No historical natural-history volume was read.
- Checked existing Federalism research filenames for inherited evidence conventions. Federalism's accepted claims and reading credit do not transfer to Entomology.

Local snapshot identity, from existing retained files (not a new live recovery):

| Input | SHA-256 |
|---|---|
| `blake_data/recovery/sources/erdman/pages.json` | `61c846e4b3122eb9eca6797805bf80d976a6712c179183504b1a465c2ef6f370` |
| `blake_data/recovery/texts/erdman-complete.txt` | `d7664a0ef08db356a958e327d1527992c3d8909a3cadf8363553da77df2265d5` |
| `blake_data/recovery/passages.jsonl` | `24d123e41b67fefe53a4ad6e5bf9fc6f1b9c42d6556db89fb935e3ec01bb85c3` |

The recovery manifest identifies Archive commit `7063e9ea8b13d18bd5a585e87610164fd75d3f60` and explicitly marks oeuvre coverage `not_established`. The hashes above identify the bytes screened, not complete semantic validation of those bytes.

## Primary-source anchors for expansion

| Anchor | Exact locator | Intake consequence |
|---|---|---|
| *Milton*, copy A | Archive object 24; XML line IDs `milton.a.illbk.24.13`–`.24.22`; Erdman plate 27 [29], E124, API record 134 | Retrieve the named inventory including earth-worm, beetle, emmet, centipede, spider, spinner, earwig, maggot, flea, louse, bug, tape-worm, slug, grasshopper, scorpion, gnat, wasp, hornet, bee. |
| *Milton*, copy A | XML description of object 24; object 31 description and line IDs `.28.31`–`.28.32` | Catalog alternatives and the mythic Polypus require uncertainty labels. |
| “A Dream,” *Songs*, copy A | XML `songsie.a.illbk.27.05`, `.27.16`, `.27.20`–`.27.21`; E16, record 26 | Include emmet, glow-worm, beetle, and the unpunctuated possessive form `beetles`. |
| “The Fly,” *Songs*, copy A | XML object 33, `.33.03`–`.33.22` | Noun occurrences and human analogy require separate mention/function fields. |
| “The Human Abstract,” *Songs*, copy A | XML `.41.17`–`.41.18` | Preserve Blake's `Catterpiller` spelling. |
| “The Sick Rose,” *Songs*, copy A | XML `.48.04`–`.48.05`; description of object 48 | A worm mention and a flight verb share a passage; catalog images vary by copy. |
| *The Book of Thel*, copy B | XML `.06.03`–`.06.09`, `.07.10`–`.07.12`; object 7 description | Retain personification; do not infer a zoological identification from the term alone. |
| *The Four Zoas*, Night IX | E404, API record 416, manuscript page 136, lines 29–34 | Similar animal inventory is a distinct work context, not a duplicate edition to erase. |
| *An Island in the Moon*, chapter 10 | E462, record 474 | Microscopy scene supplies cock chafer, louse, flea, butterfly candidates. |
| “Auguries of Innocence” | E490–492, records 502–504 | Include chafer and cricket; review `Mite` as a monetary homonym rather than an animal. |
| *The Four Zoas*, Night II | E323, record 335 | Include snail; retain context before interpreting mockery of Los. |
| Description of illustrations to Milton's *Il Penseroso* | E685, record 697, numbered description 10 | Include Blake's prose discussion of insects; distinguish quoted Milton verse from Blake's description. |

Official pinned primary XML:

- [Milton A](https://raw.githubusercontent.com/blakearchive/data/7063e9ea8b13d18bd5a585e87610164fd75d3f60/works/milton.a.xml), targeted text and descriptions listed above. Its object 24 description offers caterpillar **or** centipede, and beetle **or** bee **or** hornet. These are alternatives, not separately confirmed depicted animals. Object 31 may depict vegetation or a Polypus. Record catalog wording separately from a fresh visual judgment.
- [Songs A](https://raw.githubusercontent.com/blakearchive/data/7063e9ea8b13d18bd5a585e87610164fd75d3f60/works/songsie.a.xml), targeted objects 27, 33, 41, 48. The description associates emmet with ant, and distinguishes the worm depiction in different copies of “The Sick Rose.” This establishes a useful local synonym and a copy-sensitivity warning, not a full iconographic census.
- [Thel B](https://raw.githubusercontent.com/blakearchive/data/7063e9ea8b13d18bd5a585e87610164fd75d3f60/works/thel.b.xml), targeted objects 6–7. The Worm is personified in both text and description; biological assignment remains interpretive.
- [Erdman reader API](https://erdman.blakearchive.org/api/pages), retained JSON identified above. New web access to this endpoint failed; E locators above were checked against the retained API response, not re-fetched pages. Some retained page text contains quotations, annotations, and non-Blake material.

## Lexicon design

The following lists are **query candidates**, not assertions that every word occurs in Blake. Keep zero-hit terms in the search manifest. A zero is absence only in the declared snapshot, planes, and lexical rules. Spelling expansions are editorial project choices unless a specific attestation is recorded above.

| Concept group | Candidate forms and compound handling |
|---|---|
| Worm, broad historical/mythic sense | worm, worms, worm's, worms'; wormlike, worm-like; earthworm, earth-worm, earth worm; tapeworm, tape-worm, tape worm; silkworm, silk-worm, silk worm; glowworm, glow-worm, glow worm; bookworm, book-worm; blindworm, blind-worm; cutworm, cut-worm; jointed worm, winding worm. Keep compounds assigned to distinct concepts rather than summing the same span twice. |
| Ant/emmet | ant, ants, ant's, ants'; emmet, emmets, emmet's; emmett, emmetts, emmett's; emmitt, emmitts; pismire, pismires, pismire's; ant-hill, anthill, ant hill. `Emmett` is a user-supplied search expansion; this pass attested `Emmet`, not that alternate spelling. |
| Fly | fly, flies, fly's, flies'; fly-like; housefly/house-fly/house fly; dragonfly/dragon-fly/dragon fly; gadfly/gad-fly/gad fly; mayfly/may-fly; firefly/fire-fly; horsefly/horse-fly. Search inflected motion verbs in a separate high-noise channel if requested; never count them as animal nouns automatically. |
| Bee/wasp | bee, bees, bee's, bees'; honeybee/honey-bee/honey bee; bumblebee/bumble-bee/bumble bee; humblebee/humble-bee/humble bee; wasp, wasps; hornet, hornets. |
| Beetles/chafer | beetle, beetles, beetle's; gold beetle, golden beetle; chafer, chafers, chafer's; cockchafer/cock-chafer/cock chafer; scarab, scarabs; weevil, weevils; ladybird, ladybirds. |
| Moth/butterfly/larva | moth, moths, moth's; moth-like, mothlike, moth-labourd; butterfly, butterflies, butterfly's; caterpillar, caterpillars; caterpiller, caterpillers; catterpillar, catterpillars; catterpiller, catterpillers; maggot, maggots; grub, grubs; larva, larvae; chrysalis, chrysalises, chrysalides; cocoon, cocoons. |
| Other insects | flea, fleas; louse, lice; gnat, gnats; midge, midges; grasshopper, grasshoppers; cricket, crickets, cricket's; locust, locusts; earwig, earwigs; bug, bugs; cockroach, cockroaches; roach, roaches; termite, termites; cicada, cicadas; mosquito, mosquitoes. |
| Arachnids | spider, spiders, spider's; ground-spider/ground spider; spinner, spinners, golden spinner; scorpion, scorpions; mite, mites; tick, ticks. |
| Myriapods | centipede, centipedes; millipede, millipedes; millepede, millepedes; hundred-footed, thousand-footed. |
| Molluscs | snail, snails, snail's; slug, slugs; oyster, oysters; mussel, mussels; muscle, muscles as historical candidate; cockle, cockles; clam, clams; whelk, whelks; limpet, limpets; nautilus, nautili; octopus, octopi; cuttlefish/cuttle-fish; squid, squids. Do not infer modern molluscan identity for Polypus. |
| Other worm groups | leech, leeches; earthworm forms above; worm terms remain a broad historical category unless the context resolves them. |
| Crustaceans | crab, crabs; lobster, lobsters; shrimp, shrimps; prawn, prawns; crayfish/cray-fish; crawfish/craw-fish; barnacle, barnacles; woodlouse, woodlice; sowbug/sow-bug. |
| Cnidarian/poriferan and indeterminate | polypus, polypuses, polypi, polypus's; polyp, polyps; polype, polypes; hydra, hydras; coral, corals; sponge, sponges; zoophyte, zoophytes; animalcule, animalcules; medusa, medusae. A mythic Hydra or human-medical polyp is not automatically an invertebrate animal occurrence. |
| General or contextual channel | insect, insects; invertebrate, invertebrates; vermin; creeping thing(s), creeping creature(s); swarm(s), hive(s), honeycomb(s), honey, wax, silk, web(s), cobweb(s), spin/spun/spinning, sting(s), sting/ stung, shell(s), shelly, pearl(s), wing(s), winged/wingd, hum(s), crawl/crawling. These are leads for context expansion and material imagery, not animal-denoting tokens by default. |

Use Unicode-aware whole-token boundaries with explicit apostrophe handling; preserve punctuation and exact original character offsets in the receipt. Casefold for retrieval while keeping original case in outputs. Allow hyphen, space, line-break, and closed compound forms through declared expansions. Do not silently normalize the retained text. Longest matching compounds should be recognized before generic heads; record overlapping aliases so overlap can be audited. Avoid arbitrary stems: `ant` must not match `want`, `plant`, `giant`, `infant`, or `inhabitant`; `bee` must not match `been`; `moth` must not match `mother`; `fly` must not match `flying` unless that expansion is explicitly selected.

## Ambiguities that must stay visible

- `fly`/`flies` can be an animal noun, motion verb, or another sense. “The Sick Rose” is a useful same-context negative control for the flight verb even though it contains a genuine worm mention. A lexical hit should not become an animal count without adjudication.
- `mite` can mean a small coin/amount; the retained “Auguries” E492 example is a negative biological case. `cricket` may be an animal or a game; `bug` is not necessarily a modern true bug; `roach`, `crab`, `muscle`, `sponge`, `spinner`, `shell`, and `coral` require contextual reading.
- A possessive without an apostrophe may look plural (`Emmets`, `beetles`, `Crickets`, `Chafers`). Preserve the attested string and encode possessive/plural uncertainty; avoid inventing grammatical normalization.
- A glow-worm or silk-worm compound must not automatically become an annelid because its head is `worm`. A blindworm may name a vertebrate. A worm becoming a serpent remains relevant transformation imagery, but serpent, snake, viper, newt, toad, bat, mole, and rat are not zoological invertebrates. Keep them as contextual relations rather than admitted invertebrate taxa.
- Metaphorical humans, mythic entities, symbolic parasites, and material products are core interpretive material for this application. Preserve them with explicit function labels; do not discard all figurative uses as false positives.
- Polypus is especially risky: the official Archive description itself leaves a vegetable/animal alternative. This pass does not resolve its historical zoological reference. Dictionary attempts did not establish a usable scholarly definition: Oxford returned HTTP 403; Johnson's scholarly edition exposed the search interface without an entry. Treat historical lexicography as pending, not completed reading.
- Contextual words such as silk, honey, web, swarm, pearl, or shell can recover discussions without a nearby animal name. They produce high-noise candidate sets and need a second screening channel, clearly separate from named-animal counts.

## Minimum annotation and completeness contracts

Each candidate should retain a stable mention ID, source-plane and text-role labels, work/edition/copy/page or XML element locator, source URL and SHA-256, exact matched span and offset, lexicon version/hash, context, reviewer decision, reason, biological group, rhetorical function, and links to related mentions/images. Suggested decisions: `pending`, `include`, `exclude`, `uncertain`; keep the last three distinct and require a rationale. Inclusion does not imply literal reference.

Report at least these denominators separately: indexed source records, examined works, copies/editions, lexical hits, compound-resolved mention spans, adjudicated included mentions, uncertain mentions, excluded homonyms, and image candidates. The all-copy total repeats textual content; it cannot stand in for unique Blake passages or works. The Erdman page total cannot stand in for unique works either. Similar *Milton* and *Four Zoas* inventories are separate compositional contexts; duplicate copies of one poem are a different kind of repetition.

Run a named-animal channel and contextual imagery channel across retained primary reading, exploratory Erdman, and XML description planes separately. Broad retrieval should admit unverified sources for review, preserving their status. Existing primary scope deliberately excludes unsegmented Erdman material; dropping exploratory planes would omit much of the longer works, prose, and letters relevant to the requested census. Conversely, searching all XML indiscriminately retrieves curatorial descriptions, notes, quoted source authors, and multiple copies. Never label that whole set “Blake's words.”

Completeness is a matrix, not a boolean: source inventory coverage, transcription availability, authorship/reading segmentation, alias coverage, adjudication completion, work/copy deduplication, and iconographic review. This pass establishes a research-ready seed list and several difficult controls. It establishes neither all-Blake coverage nor an adjudicated total. A defensible next claim is “exhaustive lexical retrieval within the pinned, declared corpus and lexicon,” followed by explicit residual gaps; a whole-oeuvre claim requires additional source reconciliation and visual review.

Potential meaningful controls for implementation: all named words from the declared *Milton* inventory retrievable; historical `Catterpiller` retrieved; `louse` expands to `lice`; hyphen/space/newline/closed compounds resolved without double counting; `ant` excludes substrings; the same flight-verb context produces a candidate whose biological decision can remain excluded; monetary `Mite` remains visible but excluded; a second edition of one poem does not inflate a work-level total; ambiguous iconographic alternatives remain one uncertain candidate. These are proposed controls, not tests run in this memo.
