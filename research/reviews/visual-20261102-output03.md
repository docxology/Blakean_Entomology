# Entomology native03 acceptance

**PASS_WITH_LIMITATIONS — exact PDF/HTML working-draft output only.**

The two editorial commas were removed from Table 2 without changing its words or interpretation. Independent XML extraction confirms Songs Y `songsie.y.illbk.39.05` reads “That flies in the night” with no terminal comma, and Thel F `thel.f.illbk.06.04` contains “like an infant wrapped” with no comma after “infant”. The three graphical-abstract quotations remain exact ordered selections from their captured XML.

This is a fresh acceptance of native03, not software/source reapproval. The original independent-final02 source **REQUEST_CHANGES / SRC-01** and its failures remain unchanged. The separately corrected test module and reported 20 tests were not audited or rerun here. Federalism was outside this review and receives no new verdict.

## Exact identity

| Object | SHA-256 |
|---|---|
| Caller manifest, 165 members | `faf914816b82e15ca77196a1856e43e32b113d5794c86202cb17b9e889323314` |
| Native03 PDF, 45 physical pages | `363275bd52e56b895432f3fb7ea63d6c9ee17a2b0bf7346c6a2aebc28f0e1b95` |
| Native03 HTML | `0241152bb71cea3c2182be448beefc1ad4b557afd45c5ef3dc42bc39f01dd453` |
| Native03 receipt | `8ab356aaa7306b0fbb497358ee4ff0eb497ecadfe54716f178e3a3322933b432` |
| Accepted parent PDF, native02 | `c0a86f1249b741d19363d325d47a87bf0516de9a8152128ba962b238fd3cad74` |
| Accepted parent HTML, native02 | `90fb1170c301590f46a4dffae53133dd347aebcbae2859d41cce81b9a291910f` |

Paths are in VERDICT.json. Both admission and final verification matched all 165 members. The title is **Blakean Entomology**, subtitle **Small Lives, Uncertain Bodies, and the Work of Attention**, dated **2 November 2026**, edition **0.8.0**. The HTML opening explicitly prints the version; the PDF cover prints title/date and the version is bound by its resolved native configuration, not visibly printed on that cover. The PDF metadata creation timestamp is the retained reproducibility timestamp, not the execution date.

The pinned native receipt records template `efce6d6f5b3c4e8e2bbf92d8250855a0a9389ae8`, normal host SDK `263d7c83abe6f1309a64af3285a683c1b7672269`, external Python 3.14 prefixes and the actual PDFRenderer / native-base WebRenderer calls. Those producer identities were retained; no new renderer or software qualification was run by this auditor.

## Scenarios, invocations and binary observations

Every command directory retains prelaunch argv/environment, PID, raw stdout/stderr and completion. Exact invocations are in its prelaunch.json.

| Scenario / invocation | Binary observable | Artifact |
|---|---|---|
| Supplied first-command Python prefix/global-guidance intake; commands000–003 | Both prefixes external; actual ancestor/project/render/style and original PDF/browser guidance read before semantic intake | GUIDANCE_COMPLETE; commands/000-guidance through 003-intake |
| SHA-256/member verification, commands004 and017 | Expected manifest SHA; 165/165 initial and final byte/hash matches | initial-input-verification.json; final-input-verification.json |
| Fresh Poppler of actual native03 and actual native02: `pdftoppm -r 72 -png PDF PREFIX`, commands005/010 | 45 fresh rasters each; parent rasters equal prior independently accepted, manifest-bound rasters; only page9 differs | current-page-01.png through45; parent-page-01.png through45; page-acceptance-chain.json |
| Fresh enlarged page9: `pdftoppm -f 9 -l 9 -scale-to 2200 -png PDF PREFIX`, command006 | Current physical9 generated at2200px; corrected expressions and table fit inspected directly | enlarged-09.png; visual-observations.json |
| `pdftotext -layout` and `pdfinfo`, commands007/015; structural checks016 | Exact title,45 pages, cover1/abstracts2–4/contents5; no undefined native reference/citation warnings | current-pdf.txt; commands/015-pdfinfo/stdout.log; output-delta-validation.json |
| Independent raw HTML/article and asset comparison, commands009/014/016 | HTML and hydrated article differ only by the two comma deletions; all58 figure-directory members unchanged; references/config/preamble/frontmatter unchanged | html-delta.diff; output-delta-validation.json |
| Independent XML parsing and digest/image joins, command014 | Three exact graphical selections and2 corrected fragments match; original image hashes equal adopted aliases | quotation-proof.json |
| Fresh real Chromium, `bun browser-check.mjs PACKET OWNED_ROOT`, command013 | Desktop1440/mobile390;18/18 loaded images each, natural proportions;74 MathJax containers,0 errors;0 missing anchors/duplicate IDs/unresolved tokens; document width contained | browser/desktop-dom.json; mobile-dom.json; both snapshots; RESULT.json |
| Same Chromium gate with an in-memory nonexistent anchor at each width, command013 | Actual gate throws “missing anchor”; exactly the injected target detected; unmodified page passes again after removing it | browser/desktop-negative-control.json; mobile-negative-control.json |
| Real horizontal wheel on Table2 at both widths, command013 | ScrollLeft0→300; caption x unchanged; document contained | browser/desktop-wheel.json; mobile-wheel.json; before/after PNGs |
| Normal owned-page/browser closure, command013 | browser.close completed and logged command returned0; SSD profile retained | browser/CLOSED.json; commands/013-browser/completion.json |

## What was visually viewed

The acceptance chain covers **all45 physical pages**. Fresh current/parent rasters independently establish44 byte-identical pages at72dpi, including their equality to the prior independently accepted rasters. Physical9 was inspected directly at2200px. This is a raster-level identity statement at the declared resolution, not a claim of identical PDF object structure.

Current pages1–5,10,12,13,15,16,20,21,43,45 were also opened individually. The cover retains the complete authentic recto; the distinct Fly, Dream and Thel graphical abstracts occupy2–4; contents begins5. The material images retain visible complete boundaries/proportions, captions, credits and copy locators. Page9 visibly has the corrected punctuation, native Table2 number and citations without clipping or overlap. Page10 preserves conditional reference branches and excludes inferred sequence/language ancestry. The bibliography and reading ceilings remain present. This is bounded selection/layout review, not full critical-edition collation.

Fresh browser evidence includes36 per-image screenshots plus2 openings and4 table screenshots. Each capture followed two animation-frame turns after scrolling; table-wheel captures followed eight. **15 named browser screenshots were actually opened**, listed in visual-observations.json; capture of the others is not claimed as visual inspection. The current mobile Thel screenshot shows the complete image and caption. The prior owner's blank transition-frame screenshot remains preserved and is not used as positive evidence.

At390px the graphical panels' embedded labels are small, with real caption text and full-size figure links available. Table2 requires horizontal scrolling at both tested widths; actual wheel motion works and its wrapped caption stays fixed. These are functional layout observations, not keyboard or assistive-technology certification.

## Boundaries and retained failures

The ledger remains47 reviewed /35,992 unreviewed. Baine's relevant chapter remains unavailable and unread. No new species identification, animal adjudication, complete-oeuvre/image-corpus credit, inferred genetic phylogeny or language genealogy follows from this acceptance. Analytical production was not replayed; its unchanged adopted bytes retain their original producers.

No specialist Blake scholarship, whole-paper scientific acceptance, rights clearance, accessibility certification, offline MathJax, hosted CI, canonical integration, Git publication, remote readback, Downloads delivery or release is certified. Integration/publication/delivery remain root-owned.

Command004 successfully verified all165 inputs, then a discovery read incorrectly treated the additional-assets `source_files` field as a directory and raised FileNotFoundError. That raw failure is retained. Commands008–009 discovered the actual manifest paths, and command014 completed source validation against them; command017 reran all165 inputs at finish. One functions.exec orchestration cell had an extra closing token and failed before launching any shell command; the corrected cell launched command011 once. Neither failure is concealed or used as positive evidence.

No candidate edits, Git operations, installation, canonical lease, server, user tab or manuscript renderer were used. Evidence and the isolated profile remain solely in this owned review root. EVIDENCE-MANIFEST.json closes the settled artifacts, excluding itself and its own closing-command spool from recursive self-hashing.
