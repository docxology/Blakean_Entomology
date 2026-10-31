# Native manuscript production

The retained 0.4 article was prepared through the actual pinned
[docxology/template](https://github.com/docxology/template) framework. Blake owns
corpus custody and reusable methods. Entomology owns source selection, animal
judgments, literary interpretation, graphical abstracts and publication inputs.

## Source and runtime contract

Use the locked external CPython 3.11 environment for the application and an
explicit compatible external template environment for native writers. Verify
both interpreter prefixes on mounted GitVault. The clean template checkout must
be at efce6d6f5b3c4e8e2bbf92d8250855a0a9389ae8 for the recorded native
profile. The retained paper's SDK is
45171a099a6a658c52ab689501de646a28485653. Current 0.5.0 software selects
36b874e76d7e0549d0ea6b9f0713ced7fb41afa8; its review-planning qualification performs
no native render. Reproducing the retained epoch uses its recorded producer.
The retained `NativeRequest`, `NativeStage` and worker transport currently admit only SDK `45171a099a6a658c52ab689501de646a28485653`. A request declaring the current `36b874…` pin is rejected. The transport's declared pin does not itself verify the actual imported SDK; do not relabel a current installation as the retained producer. A current-SDK native run first needs separately reviewed contract admission and actual SDK identity enforcement in `publication_contract.py`, `publication.py` and `publication_wire.py`, then fresh source/software/native/output qualification. A new request alone does not implement that prerequisite. Federalism is an architectural sibling,
with no runtime dependency here.

Use the supported private-repository lease. Keep TMPDIR, outer TMPPREFIX,
uv/Python caches, Matplotlib and TeX paths external. Never overwrite a prepared
or native epoch. Failed epochs retain raw errors and partial files.

## Retained native profile: prepare and admit

Run tools/prepare_research_manuscript.py with independently held atlas, reference,
base-figure, casebook and additional-assets pins, the current authored Markdown
and bibliography, and a fresh ignored analysis_output destination. Preparation
publishes hydrated Markdown, copied assets, references and preparation.json.
This is a source result, not a native render. Native admission requires its
authored-source and bibliography hashes to remain current.

Create NativeRequest JSON using src/blakean_entomology/publication_contract.py.
Every input has an explicit path and caller-held SHA256: preparation receipt,
atlas, composition export, casebook, complete museum recto, object provenance,
config, preamble and `web_css`. The stylesheet is a required pinned input.
Retained mathematical exports keep their original producer receipt; a new
presentation does not become a fresh numerical execution.

~~~sh
uv run python tools/render_manuscript.py \
  --request "$REQUEST" --request-sha256 "$REQUEST_SHA256" \
  --template-root "$TEMPLATE_ROOT" --template-python "$TEMPLATE_PYTHON" \
  --output analysis_output/new-native-epoch
~~~

The prepare-only option closes a fresh source stage without native acceptance.
Wrong request/input/template pins, changed members and occupied destinations
are refusing cases.

## Actual framework execution

The ordinary installed application produces the authentic-image cover and
three source-derived graphical abstracts. A thin worker in the separately
selected template runtime reads a hash-bound CSV/INI transport of the admitted
plan. It uses real framework manuscript hydration, prevalidate_for_render, the
shipped formalism.lua, pandoc-crossref and `PDFRenderer.render_combined`.
`EntomologyWebRenderer` inherits the actual `WebRenderer.render_combined`; its
only extension is the pinned CSS embedding step, which calls the native base
step and framework `embed_css` with admitted `web.css`. The PDF writer owns
Pandoc, BibTeX and TeX. HTML retains native citeproc, image/registry processing,
MathJax and base styling; keep its complete web directory and assets.

The framework hydrates Markdown and copies YAML. The adapter applies the real
framework substitution and confined atomic writer to the resolved YAML, then
runs native configuration/token validation. The admitted tokenized configuration
stays unchanged. Checking only the missing-key list does not prove that the
resolved configuration contains its values.

Project CSS gives each wide table one horizontal scroll container. Native table
layout, caption wrapping to the container width and a caption fixed at its left
edge retain readable captions while the data scroll. Verify actual horizontal
wheel behavior and settled frames at mobile and desktop widths; a desktop table
that fits should remain unscrolled.

Source configuration and preamble delay the native TOC until after the three
abstracts. Verify physical cover1, abstracts2–4 and TOC5 in the actual PDF.
Printed counters alone do not establish physical page order.

## Native syntax

Use stable sec:, fig:, tbl: and eq: labels and Pandoc bracket references.
Let native counters number body sections, figures, tables and equations. Write
formalism Divs and references as follows:

~~~markdown
::: {.definition #def:example title="A precise title"}
A source-grounded definition.
:::

The preceding contract is [@def:example].
~~~

Use proposition / prop: for justified propositions. Displayed equations use
dollar-delimited math followed by an eq: ID. Cardinality and absolute values
use \lvert...\rvert. Put a caption immediately beneath each table:
: Caption {#tbl:example}. Keep appendix headings explicitly unnumbered with
stable section labels. Do not create a second project numbering engine.

Numbered targets use native ordinal references. Deliberately unnumbered
appendices use descriptive Markdown anchor links, for example
`[Appendix A](#sec:appendix_a)`; do not request their ordinal with
`[@sec:appendix_a]`. The same distinction applies to other unnumbered headings.

One final unnumbered References heading and empty refs Div give both editions
a bibliography location. The actual PDF injector suppresses natbib's duplicate
heading. Duplicate/undeclared labels and undefined references must fail the
real filter preflight even when an underlying native filter only warns.

## Qualification and closure

native-stage.json binds admitted inputs and project production code. The
transport closes those bytes for the selected runtime. native-render-receipt.json
is written only after both actual writers succeed, actual `pdfinfo` reports the
admitted resolved title and a positive physical page count, PDF text and HTML
contain no unresolved declared-token syntax, and every original stage, project
and template source member revalidates. Raw reader outputs are retained. A
valid PDF with a literal title token must fail specifically at the title check.
The receipt records imported template modules, runtime prefixes, resolved
manuscripts, output checks and artifact hashes.

Run full normally installed tests, strict package and changed-tool checks,
lint and separate application 90% / infrastructure 60% branch-aware coverage.
Exercise actual native CLI success/refusal and native semantic controls.
Inspect new source figures and every final physical page; obtain independent
acceptance bound to the exact final receipt/PDF. These are distinct from
specialist scientific review, complete image-corpus review or public release.

## Retained 0.4.0 production qualification

Use `uv run --no-sync pytest -c pyproject.toml tests` for the normally installed
suite. The explicit configuration prevents a parent GitVault pytest root from
collecting historical project trees. Strict checks cover the package and the
changed application tools `render_manuscript.py` and
`prepare_research_manuscript.py`. Check `native_template_worker.py` and
`native_web.py` at Python 3.14 with the selected project source/tools and
pinned template on the checker's import path. This is not a strict-check claim
for every unchanged tool.

Keep unit, actual preparation/render-CLI, retained-data figure production and
native-runtime preflight/CSS counters in separate databases. Trace real
operations; the final PDF need not be rebuilt to obtain counters. Combine only
segments whose consumed source bytes still match their before/after manifests,
retaining every original database and report with `coverage combine --keep`.
Map the normally installed application package to `src/blakean_entomology` in
the coverage path aliases. Preserve older-source counters outside that union.

The combined gate has separate branch-aware denominators: covered statements
plus covered branches divided by all statements plus branches. The unit-only
database is not the full production qualification. With the externally bound
`COMBINED_COVERAGE` and `COVERAGE_CONFIG` paths, run:

~~~sh
uv run --no-sync coverage report --rcfile "$COVERAGE_CONFIG" \
  --data-file "$COMBINED_COVERAGE" --include '*/blakean_entomology/*' \
  --fail-under 90
uv run --no-sync coverage report --rcfile "$COVERAGE_CONFIG" \
  --data-file "$COMBINED_COVERAGE" --include '*/tools/*' \
  --fail-under 60
~~~

Retain both the initial failing coverage union and its completed real-production
qualification. Declare excluded and unexecuted surfaces, interpreter identities,
source bindings, raw positive/refusal commands and both complete denominators
in the [retained native qualification](../../research/template-native-20261030.json). Retained analytical exports keep their
historical producer; figure-only consumption does not become numerical replay.

The retained 0.3 draft used a standalone print path. Its accepted 37-page PDF and
sealed evidence keep that historical scope; they are never relabelled as a
template-native build.

## Software-only review-planning epoch

Current software passed 303 installed tests and the declared
separate application/tool coverage floors; its exact Git SDK and real
planning/refusal commands are in
[the software qualification](../../research/review-planning-20261030.json).
The retained PDF/HTML and their original producer remain unchanged. No old
coverage database, native receipt, page review or one-shot production grant
is reassigned to this software epoch. Changed manuscript or renderer inputs
require their own source, native and physical/browser-output qualification.
