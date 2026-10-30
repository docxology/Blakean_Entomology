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
| Public `blake` | Acquisition and recovery, source custody, portable schemas and explicit conversions, normalization and distinct retrieval profiles, generic counting/statistics/proximity/composition/concentration, rooted hierarchy/layout, annotation/run custody and offline workspace. |
| Private `Blakean_Federalism` | Political query selections, institutional models and comparisons, interpretation, manuscript and its own fixed evidence epochs. |
| Private `Blakean_Entomology` | Invertebrate vocabulary, query-channel policy, conditional taxon mapping, contextual adjudication, domain figures, selected image readings and manuscript. |

Entomology imports `blake.applications`, `blake.studies` and explicit
`blake.methods` modules. It consumes the public portable schema rather than an
undocumented SQLite layout. Domain code delegates generic algorithms upstream;
the classification reference neither infers a phylogeny nor adjudicates a Blake
occurrence. See [project status](PROJECT_STATUS.md) and the
[private style guide](style-guide.md).

## Separate current runtime from captured evidence

The current runtime selects Blake 0.4.0 at Git
`45171a099a6a658c52ab689501de646a28485653` through `pyproject.toml` and
`uv.lock`. Its installation and workflow qualification are recorded in
[verification.json](../research/verification.json). Upstream `main` is a moving
branch, so an application adopts an exact reviewed commit rather than silently
following it.

The historical 31-page 0.2.0 paper and its installed analytical/figure/preparation
epoch use `d020f47767996a061b6f60e93a82da9386a7926c`. The current 0.3.0
paper preparation, contextual-review extension and installed production
qualification use the exact 0.4.0 SDK above. Completed mathematical replay is
retained only while every consumed source module, input and semantic export
still matches; current figures and paper preparation receive fresh epochs. The historical corpus pin and
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
