# Private corpus and research custody

The GitHub repository is private. Provider texts, full concordances, review queues,
copied corpus bundles and generated reports live only under ignored `local_data/`
or `analysis_output/`. A Git clone recovers the code, vocabulary, research protocol,
paper and text-free aggregates; it does not recover the corpus.

The corpus stays under the custody of the upstream [Blake project](https://github.com/docxology/blake).
Import creates an independent, hash-bound application snapshot; it does not link
or modify the upstream source files. Archive transcriptions, editorial XML and
images retain their provider terms. The underlying public-domain Blake work and a
modern provider edition are distinct rights questions.

No corpus symlinks, hard links, submodules, Git LFS source files, images, or long
provider excerpts belong in this repository. Source URLs and exact locators are
recorded for verification. Locally generated contexts remain private. Only
project-authored synthesis, selected brief quotations, review decisions keyed by
opaque occurrence IDs, and text-free aggregate counts are candidates for Git.

The manifest SHA in `research/corpus-pin.json` is the trusted application input.
A changed corpus requires a new import directory and a deliberate new pin. A
changed vocabulary or method generates a new result. Existing outputs are never
silently overwritten. Git alone is not a backup of ignored research data.
