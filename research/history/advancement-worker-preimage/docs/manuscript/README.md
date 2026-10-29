# Render the working article

For the advancement article, first run `tools/prepare_research_manuscript.py`
with the pinned atlas, figure, reference and casebook receipts. The authored
Markdown now contains strict count/caption tokens; rendering that source directly
would leave unresolved data. Preparation publishes a fresh standalone Markdown,
references and independent assets under `analysis_output/`. Its manifest is a
Markdown preparation receipt, not native PDF acceptance. Concrete current packet
commands are in `coordination/entomology-agent/ROOT_COMMANDS.md`; root owns the
final SDK pin, render, physical-page inspection and Downloads copy.

The command below records the earlier simple render profile. For the prepared
advancement input use `--citeproc --bibliography <prepared>/references.bib`,
`--resource-path <prepared>` and the prepared Markdown path. Use a new destination
and retain all input/output hashes. No agent has run the final advancement PDF.

The canonical article is [blakean-entomology.md](blakean-entomology.md). The
initial PDF uses Pandoc 3.12.1 and XeLaTeX from TeX Live 2026, A4 paper, 20 mm
margins and 11 point body type. It contains no provider images. This is a simple
standalone draft profile; Federalism's native template layout and its visual
acceptance do not transfer to this article.

After binding TMPDIR to existing GitVault storage, select a new output directory:

```bash
mkdir analysis_output/paper-new
pandoc docs/manuscript/blakean-entomology.md \
  --standalone --pdf-engine=xelatex \
  --resource-path docs/manuscript \
  --include-in-header docs/manuscript/print-header.tex \
  --variable papersize=a4 --variable geometry:margin=20mm \
  --variable fontsize=11pt --variable colorlinks=true \
  --variable linkcolor=Maroon --variable urlcolor=Maroon \
  --output analysis_output/paper-new/Blakean_Entomology.pdf
pdfinfo analysis_output/paper-new/Blakean_Entomology.pdf
pdftoppm -r 90 -png analysis_output/paper-new/Blakean_Entomology.pdf \
  analysis_output/paper-new/page
```

Inspect every rendered page and keep the result bound to the input and output
hashes. A successful render is not a critical-edition, accessibility or scholarly
acceptance verdict. PDF metadata contains the render time; byte-identical future
PDF output is not assumed. The analytical artifacts have a separate verified
byte-for-byte installed-wheel replay.


The 0.2 article adds the portrait sensitivity figure and a source-bound analytical
section. Its historical baseline and eleven authored decisions retain their old
run pin; the new implementation receives a separate run receipt. Keep the figure
at its full content width so its smallest printed labels remain legible.
