# Render the Entomology manuscript

The current local edition is `analysis_output/advancement-native-20261028-04/Blakean_Entomology.pdf` (14 pages).
Its exact source, installed SDK, atlas, figures, native calls and root page-QA
scopes are recorded in `research/advancement-installed-20261028.json`.
The SDK is pinned to `21b1c002ef7588b9c908fb60fd6111c4eb548358`. Application version `0.2.0` is separate
from that SDK identity. Binary outputs stay private and ignored.

The article uses YAML title/author metadata, generated count/caption tokens,
Pandoc citations and explicit figure anchors. The reference is a captured NCBI
classification with conditional lexical associations; no sequence-inferred tree
or animal identification is claimed. The source-role atlas prints the exact
count units, zeros, work weighting and historical review boundary.

## Inputs and preparation

Use the documented locked GitVault setup and repository lease. Both Python
prefixes and caches must be external. Restore the exact ignored corpus bundle
and `local_data/reference-sources/` from authorized local custody. Source URLs,
checksums and reading limits are in `research/primary-source-snapshot-v1.json`.
A clean source clone does not contain those scientific inputs. Changed captures
must form a new epoch rather than satisfying an old checksum silently.

Choose unused output paths. From the project root, run the actual installed CLI
and the project-owned preparation tools:

```bash
reference_sha=$(uv run --locked python -c 'from pathlib import Path; from hashlib import sha256; print(sha256(Path("research/reference-taxonomy-v1.json").read_bytes()).hexdigest())')
casebook_sha=$(uv run --locked python -c 'from pathlib import Path; from hashlib import sha256; print(sha256(Path("research/reading-ledger-advancement-v1.json").read_bytes()).hexdigest())')
uv run --locked blake-entomology verify-reference \
  --reference research/reference-taxonomy-v1.json --sources local_data/reference-sources \
  --reference-sha256 "$reference_sha"
uv run --locked blake-entomology corpus-atlas \
  --bundle local_data/corpus/v1 --pin research/corpus-pin.json \
  --reference research/reference-taxonomy-v1.json --sources local_data/reference-sources \
  --reference-sha256 "$reference_sha" --historical-summary research/seed-review-summary.json \
  --output analysis_output/reproduce-atlas/atlas.json
atlas_sha=$(uv run --locked python -c 'from pathlib import Path; from hashlib import sha256; print(sha256(Path("analysis_output/reproduce-atlas/atlas.json").read_bytes()).hexdigest())')
uv run --locked python tools/build_reference_figures.py \
  --atlas analysis_output/reproduce-atlas/atlas.json --atlas-sha256 "$atlas_sha" \
  --reference research/reference-taxonomy-v1.json --sources local_data/reference-sources \
  --reference-sha256 "$reference_sha" --output analysis_output/reproduce-figures
figures_sha=$(uv run --locked python -c 'from pathlib import Path; from hashlib import sha256; print(sha256(Path("analysis_output/reproduce-figures/figures.json").read_bytes()).hexdigest())')
uv run --locked python tools/prepare_research_manuscript.py \
  --manuscript docs/manuscript/blakean-entomology.md \
  --bibliography docs/manuscript/references.bib \
  --atlas analysis_output/reproduce-atlas/atlas.json --atlas-sha256 "$atlas_sha" \
  --figures analysis_output/reproduce-figures --figures-sha256 "$figures_sha" \
  --casebook research/reading-ledger-advancement-v1.json --casebook-sha256 "$casebook_sha" \
  --reference research/reference-taxonomy-v1.json --reference-sha256 "$reference_sha" \
  --sources local_data/reference-sources --output analysis_output/reproduce-article
```

Preparation rejects unknown tokens, missing citations, changed assets and wrong
pins. It emits hydrated Markdown, three PNG figure inputs, SVG masters, references
and a bounded casebook. The five historical analytical artifacts and eleven
original decisions are not overwritten or rebound by this process.

## Native output and verification

Pandoc 3.12.1 and XeLaTeX from TeX Live 2026 produced the current edition. Its
retained native transaction generated standalone LaTeX with citeproc and ran two
actual XeLaTeX passes. The equivalent direct PDF command is:

```bash
mkdir analysis_output/reproduce-native
pandoc analysis_output/reproduce-article/blakean-entomology.md \
  --standalone --citeproc --pdf-engine=xelatex \
  --bibliography analysis_output/reproduce-article/references.bib \
  --resource-path analysis_output/reproduce-article \
  --include-in-header docs/manuscript/print-header.tex \
  --variable papersize=a4 --variable geometry:margin=20mm --variable fontsize=11pt \
  --variable colorlinks=true --variable linkcolor=Maroon --variable urlcolor=Maroon \
  --output analysis_output/reproduce-native/Blakean_Entomology.pdf
pdfinfo analysis_output/reproduce-native/Blakean_Entomology.pdf
pdftoppm -r 120 -png analysis_output/reproduce-native/Blakean_Entomology.pdf \
  analysis_output/reproduce-native/page
```

Bind TMPDIR and caches to GitVault before rendering. Preserve failures and inspect
every physical page, especially the full-page reference, portrait atlas, figures,
URLs and captions. Native generation, root manual inspection and independent
acceptance are separate scopes. Future PDF byte identity is not presumed across
unrecorded renderer versions. No provider images appear in this article; a corpus
image census remains pending. Source-stage and initial layout epochs remain
historical, including the observed float overflow and the original wide atlas.
