# Render the working article

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
