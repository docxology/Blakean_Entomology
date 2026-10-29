# Reproduce the Entomology manuscript

## Reviewed paper and current runtime

The [private root PDF](../../Blakean_Entomology.pdf) is the retained 31-page
working draft with eleven figures, twenty references and the 82-category
appendix. Its SHA-256 is
`4e244ef84d85324fc2b7bb742862c2c9c21be6574b10ed574b0f0f06e7a6f4a3`.
The original native output remains
`analysis_output/entomology-native-expansion-02/Blakean_Entomology.pdf`.

That paper's actual Pandoc citeproc and two XeLaTeX passes used the installed
SDK `d020f47767996a061b6f60e93a82da9386a7926c`. The
[expansion receipt](../../research/expansion-installed-20261028.json) binds its
installed tests, assets, preparation, native writer and physical-page QA. A later
bounded independent working-draft review also inspected the exact PDF and selected
originals. The earlier 14-page edition and prior procedural rejections remain
history; no old verdict is rewritten.

The current application runtime selects Blake 0.4.0 at
`45171a099a6a658c52ab689501de646a28485653`. Read
[current verification](../../research/verification.json) for that later
qualification. Keeping the reviewed PDF unchanged does not claim a new native
0.4 render or repeat the original analytical inference. Current task scopes,
including the nonblocking Figure 11 caption clarification, are in
[PROJECT_STATUS.md](../PROJECT_STATUS.md).

## Inputs and preparation

Use the supported repository lease, external CPython 3.11, external caches/TMP
and a fresh unoccupied output name. Verify both interpreter prefixes on GitVault.
Restore the ignored corpus and original image captures from authorized custody;
a source clone alone cannot recreate them.

The retained installed epoch uses:

| Input | Bound identity |
|---|---|
| Additional asset directory | `local_data/manuscript-expansion-installed-v1` |
| Additional manifest SHA-256 | `672e08b78788a2e47caa0f59ff19771402e785cd01c214cb3d186c375a77a1df` |
| Prepared article | `analysis_output/article-installed-expansion-01` |
| Preparation receipt SHA-256 | `e02a096014d50320157893d862963ea5b2a4d8767d8ed517a5008ba56299a02e` |

The additional assets bind nine data exports and seven original JPGs. The
historical atlas/base-figure epoch remains distinct from the later composition
epoch. Reading the same data or reusing an image does not grant new review credit.
Originals, derivations, rights notes and selected-text receipts are described in
[visual evidence](../research/visual-evidence.md).

`tools/prepare_research_manuscript.py` delegates typed input/receipt admission to
`tools/manuscript_assets.py` and content hydration to
`tools/manuscript_content.py`. Its receipt binds both helpers. For a fresh
preparation, pass the trusted atlas, base figures, additional assets, casebook and
reference with their expected hashes. Use the CLI's `--help` for the current
argument contract. Verify those expected hashes from the trusted epoch record
before admission; a new digest learned from changed bytes is not a repair.

The preparer checks source/data/figure bindings, complete image membership,
citations, count-token resolution and producer closure before publishing its
completion marker. Occupied or mismatched inputs refuse. For changed analytics,
create fresh analytical and figure epochs first, then build a new closed asset
directory and compare all semantic exports before hydrating prose. Preserve all
82 appendix rows and the twelve declared pair controls while their epoch is
unchanged; a changed result requires an explicit editorial revision.

## Actual native writer route

The example below reads the retained prepared article and writes a fresh
`native-new` directory. For a new epoch, explicitly substitute its newly
prepared article directory. Create the new native directory before execution:

~~~bash
cd analysis_output/article-installed-expansion-01
pandoc blakean-entomology.md --standalone --citeproc \
  --bibliography references.bib --resource-path . --to latex \
  --include-in-header ../../docs/manuscript/print-header.tex \
  --variable papersize=a4 --variable geometry:margin=20mm \
  --variable fontsize=11pt --variable colorlinks=true \
  --variable linkcolor=Maroon --variable urlcolor=Maroon \
  --output ../native-new/Blakean_Entomology.tex
xelatex -interaction=nonstopmode -halt-on-error -file-line-error \
  -no-shell-escape -output-directory ../native-new ../native-new/Blakean_Entomology.tex
xelatex -interaction=nonstopmode -halt-on-error -file-line-error \
  -no-shell-escape -output-directory ../native-new ../native-new/Blakean_Entomology.tex
~~~

Bind `SOURCE_DATE_EPOCH`, UTC, `TEXMFVAR` and `TEXMFCONFIG` externally; the retained
recipe used `SOURCE_DATE_EPOCH=1793145600`. Keep each raw exit and log. Two passes
are required for the reference-bearing native document. The final retained log
has five Underfull warnings and an unused table-captionsetup warning; it is not
described as warning-free.

Inspect every physical page of a new paper, especially whole-plate images, the
matched *Thel* sheet, captions, appendix rows and long bibliography locators.
Source-stage, installed-package, native, selected-image, physical-page,
independent-review and scientific qualifications are separate.

## Historical handoffs and distribution

The [pre-alignment guide at the reviewed source](https://github.com/docxology/Blakean_Entomology/blob/b1be36ab3bc3f9ceada1b520c1e85b0ac72b016f/docs/manuscript/README.md)
retains the source-stage command examples and pending-owner language as history.
Its old pending statements are superseded by the qualified epoch above; they are
not active implementation tasks. Earlier preimages remain under
`research/history/`.

Keep this manuscript and its permitted delivery artifacts private. Raw provider
expression, original image captures, full queues and analytical working data
retain their ignored custody and item-level rights boundaries. See
[PRIVACY.md](../../PRIVACY.md) before changing any distribution surface.
