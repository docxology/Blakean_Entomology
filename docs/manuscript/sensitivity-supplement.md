# Supplement: What changes when the counted unit changes?

This supplement extends the source-unit and vocabulary discussion in §3 of
*Blakean Entomology* and the limits in §8. It uses the private preliminary
shared-methods receipts at
`analysis_output/shared-methods-preliminary/sensitivity.json` and
`analysis_output/shared-methods-preliminary/proximity.json`. Their measurements
are descriptive checks on the declared retrieval experiment. They add no
contextual decisions, complete-reading credit or visual identifications to
`research/reading-ledger.json` or the historical seed review.

## S1. A category is not an animal observation

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

## S2. Work weighting changes the question

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

## S3. Exact-text deduplication is a narrow check

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

## S4. Proximity exposes the scale of co-occurrence

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
copy-specific work already specified in §8. The contrast between a short window
and a whole-unit search makes that requirement visible before co-occurrence is
mistaken for an interpretive association.

## Figure S1 caption

**Retrieval sensitivity within the pinned Blake-primary reading inventory.**
Panel A compares pooled category rates with the equally weighted mean of
recorded work-group rates; parenthetical counts retain copies. Panel B gives
the largest work-group share of each selected category. Panel C counts source
units matching four raw singular literal pairs at four finite word-window widths
and at whole-unit scope. The final column is visually separated because it has
no finite word limit. NFKC and literal denominators are displayed separately.
Exact-text grouping removes one complete duplicate unit, not all repeated textual
or bibliographic evidence. The figure contains project-authored aggregate data,
not provider text or images. It does not present an adjudicated animal census.

Figure generation and receipt validation are documented in
`docs/research/shared-methods-analysis.md`; the private preliminary render is
`analysis_output/shared-methods-figure-02/sensitivity.png`. A final rerender must
name its own input receipts and retain their hashes.


The current article uses the independently copied installed receipts in
`analysis_output/shared-methods-v4/` and the portrait print figure in
`analysis_output/shared-methods-figure-v5/`. The earlier preliminary renders above
remain historical evidence. The current figure is 170.18 by 228.6 mm at 180 dpi;
its generator and input hashes are recorded in `research/shared-methods-results.json`.
