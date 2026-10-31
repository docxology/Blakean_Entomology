# Corpus, methods and application lineage

Entomology is a private application of the public
[Blake corpus and methods](https://github.com/docxology/blake). The upstream
[corpus-and-methods working paper](https://doi.org/10.5281/zenodo.23770249)
describes infrastructure and evidence limits; this application's animal
vocabulary, contextual decisions and literary argument remain local.

[Blakean Federalism](https://github.com/docxology/Blakean_Federalism) supplies an
architectural precedent: explicit corpus pins, independent ignored local inputs,
source and reading ledgers, falsifiable checks and an argument distinct from
retrieval counts. It is a sibling project, not an import dependency or a source
of transferred review credit.

| Owner | Responsibility |
|---|---|
| Public `blake` | Acquisition and recovery, source custody, portable schemas and explicit conversions, normalization and distinct retrieval profiles, generic counting/statistics/proximity/composition/concentration, rooted hierarchy/layout, deterministic review planning, annotation/run custody and offline workspace. |
| Private `Blakean_Federalism` | Political query selections, institutional models and comparisons, interpretation, manuscript and its own fixed evidence epochs. |
| Public `docxology/template` | Generic manuscript hydration, pre-render validation, formalism/cross-reference filters and native PDF/web writers. |
| Private `Blakean_Entomology` | Invertebrate vocabulary, query-channel policy, conditional taxon mapping, contextual adjudication, domain figures, selected image readings, frontmatter and manuscript. |

Entomology imports `blake.applications`, `blake.studies` and explicit
`blake.methods` modules. It consumes the public portable schema rather than an
undocumented SQLite layout. Domain code delegates generic algorithms upstream;
the classification reference neither infers a phylogeny nor adjudicates a Blake
occurrence. See [project status](PROJECT_STATUS.md) and the
[private style guide](style-guide.md).

## Separate current runtime from captured evidence

The current 0.5.0 software selects Blake 0.5.0 at Git
`36b874e76d7e0549d0ea6b9f0713ced7fb41afa8` through `pyproject.toml` and
`uv.lock`. Its installation and workflow qualification are recorded in
[verification.json](../research/verification.json). Upstream `main` is a moving
branch, so an application adopts an exact reviewed commit rather than silently
following it.

The historical 31-page 0.2.0 paper and its installed analytical/figure/preparation
epoch use `d020f47767996a061b6f60e93a82da9386a7926c`. The 0.3.0
contextual-review extension uses Blake 0.4.0 at
`45171a099a6a658c52ab689501de646a28485653`.
The 0.4.0 paper uses that same SDK and a new installed/native qualification;
its docxology/template source is independently pinned to
`efce6d6f5b3c4e8e2bbf92d8250855a0a9389ae8`. The application calls the
actual framework hydration, validation, PDF and web interfaces. Federalism's
rendering precedent supplies no runtime dependency or transferred acceptance. The retained mathematical runs keep their actual recorded analytical producers.
The 0.4.0 authoring rebuild consumes their exact hash-bound exports and creates
new frontmatter/preparation/native epochs; it does not claim a new mathematical
replay. A later numerical run requires a new producer closure and comparison. The historical corpus pin and
eleven seed decisions keep their producing identities. The additive 36-decision
study is recorded separately; the combined baseline review has 47 decisions and
35,992 unreviewed candidates. The later atlas gains no retroactive decisions. A later runtime or documentation
change does not retroactively alter them. A changed method or selection needs a
new run; a changed capture additionally needs an independent import and deliberate
new pin. See the [render and epoch guide](manuscript/README.md).

The initial [parity receipt](../research/federalism-parity.json) verifies exact
equality of 2,067 portable passage payloads against Federalism's qualified
historical SQLite import while retaining its original index hash. This closes
that shared input seam, not Federalism's analyses or Entomology's interpretation.
Different query registries and retrieval profiles retain their own denominators
and contracts even when input bytes match.

Federalism's institutional model, political claims, quotation ledger, releases
and acceptance records stay with Federalism. Provider expression and full private
outputs stay in the ignored custody described in [PRIVACY.md](../PRIVACY.md).
