# Prepare the expanded Entomology manuscript

The expanded source integrates selected textual readings, seven historical image
witnesses and finite composition/proximity analyses. The previous 14-page edition
at `analysis_output/advancement-native-20261028-04/Blakean_Entomology.pdf` and its
`research/advancement-installed-20261028.json` receipt remain historical. They do
not qualify this new source. Root owns the final SDK pin in `pyproject.toml` and
`uv.lock`, installed replay, native output, page inspection and acceptance.

## Inputs and custody

Use a repository lease, the existing external interpreter, and external TMP/cache
roots. `local_data/` and `analysis_output/` remain ignored private custody. The
additive metadata lives in `research/*-expansion-v1.json`; exact images, captured
source bodies, selected readings and producer code live beneath
`local_data/manuscript-expansion-v1/`. No source binary belongs in Git.

The image delivery is bound to SHA-256
`5073511850b76515930f0283f03e956a35af6968176e95914526b226558d4d15`.
The analytical candidate delivery is bound to
`9ef02317c0bc6ee9fb314331d364707dda25e8db7300d48d6f350f1bc973ac3a`.
The current local additional-asset manifest explicitly labels that historical
producer. It is preparation staging, with no installed-new-code claim. The
four original copy-Y JPGs and three Thel JPGs are retained byte-for-byte; whole
scan derivatives and the matched F/O sheet retain their derivation receipts.
See [visual evidence](../research/visual-evidence.md).

## Preparation contract

The legacy three-figure API remains available for a minimal authored manuscript.
The expanded main manuscript additionally requires both `--additional-assets`
and `--additional-assets-sha256`. `additional-assets.json` is a strict typed
manifest. Its flat asset receipts, exact Markdown image membership, source-file
receipts, producer receipts, source ledgers, atlas pin and two table replacements
are verified before output reservation. Unknown fields, changed bytes, unsafe
paths, symlinks, duplicate/colliding names, missing sources and occupied outputs
refuse explicitly. Source bytes are checked again before the completion marker.
A failed publication after reservation retains its partial output without a
completion marker.

The additional directory is closed: every regular file is declared, with only
`additional-assets.json` excluded from its own payload list. Image paths identify
exact displayed images; other declared files are supplements. Sources are copied
into private staging without flattening copy or object identities. The preparation
receipt binds the authored Markdown, bibliography, all asset manifests, copied
bytes, source-ledger hashes and historical producer receipts.

From the project root under the supported lease, with the existing external
runtime and source `PYTHONPATH` selected by root, choose a fresh output name:

```zsh
atlas=analysis_output/advancement-atlas-20261028-01/atlas.json
figures=analysis_output/advancement-figures-20261028-01
additional=local_data/manuscript-expansion-v1
atlas_sha=$(uv run --locked python -c 'import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$atlas")
figures_sha=$(uv run --locked python -c 'import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$figures/figures.json")
additional_sha=$(uv run --locked python -c 'import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$additional/additional-assets.json")
casebook_sha=$(uv run --locked python -c 'import hashlib; print(hashlib.sha256(open("research/reading-ledger-advancement-v1.json","rb").read()).hexdigest())')
reference_sha=$(uv run --locked python -c 'import hashlib; print(hashlib.sha256(open("research/reference-taxonomy-v1.json","rb").read()).hexdigest())')
uv run --locked python tools/prepare_research_manuscript.py \
  --manuscript docs/manuscript/blakean-entomology.md \
  --bibliography docs/manuscript/references.bib \
  --atlas "$atlas" --atlas-sha256 "$atlas_sha" \
  --figures "$figures" --figures-sha256 "$figures_sha" \
  --additional-assets "$additional" --additional-assets-sha256 "$additional_sha" \
  --casebook research/reading-ledger-advancement-v1.json --casebook-sha256 "$casebook_sha" \
  --reference research/reference-taxonomy-v1.json --reference-sha256 "$reference_sha" \
  --sources local_data/reference-sources --output analysis_output/expanded-preparation-new
```

The exact available base-figure directory and executed command are recorded in
the editorial handoff. The example must be rebound to root's fresh producer
before final output. A caller-held expected digest is an admission input; do not
replace a known expected digest merely to silence a mismatch.

## Refreshing the analytical epoch

After root reproduces integrated analyses in `analysis_output/composition-expansion-01`
and `analysis_output/composition-figures-expansion-01`, build a new additional
asset directory. Verify the new run/figure manifests first. Preserve the image
packet and its seven original JPG hashes. Regenerate Appendix A directly from
`composition.json` in `category_ids` order: category, candidates, matched units,
positive work groups and minimum groups for half mass. Preserve all 82 rows and
undefined zero-mass concentration. Appendix B follows the twelve declared pairs
and windows in `literal-pairs.csv`, printing units and matched work groups.

The closed editorial scratch recipe `scripts/stage_assets.py` accepts explicit
DATA, FIGURES and a new unoccupied DESTINATION. It checks the supplied producer
hashes and semantic denominators, preserves every source/producer receipt and
creates a new manifest. Its default inputs are the historical candidate; root
must supply fresh paths and label the new producer explicitly. Numeric prose
must be compared with the new semantic outputs before render; a changed result
requires an editorial change rather than silently retaining this epoch's numbers.
The four complete vector/CSV figures remain supplements. The main text uses only
composition influence and query-channel audit; the full 82-by-33 matrix must not
be reduced to tiny A4 labels.

## Native output remains root work

Pandoc citeproc should consume the hydrated Markdown, copied bibliography and
resource directory. `print-header.tex` retains the existing source control for
layout. Inspect every physical page of the fresh output, especially the four
separate Songs scans, the matched Thel sheet, captions, Appendix A and long source
locators. The source requests generous whole-plate sizes; those requests do not
certify final print legibility. No native PDF was produced by editorial integration.
