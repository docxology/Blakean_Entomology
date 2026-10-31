# Entomology agent guide

This private application owns invertebrate vocabulary, contextual decisions,
reference mappings, selected image readings and its manuscript. Public
[Blake](https://github.com/docxology/blake) owns corpus custody and reusable
methods. Begin with [project status and task scopes](docs/PROJECT_STATUS.md).

## Choose the relevant contract

| Change | Read before editing |
|---|---|
| Corpus, vocabulary, review decisions or count interpretation | [Research protocol](docs/research-protocol.md), [contextual batch contract](docs/research/context-review-20261029.md), [lineage](docs/project-lineage.md), and the exact input pin |
| Planning a review workload | [Request-pinned planning](docs/research/review-planning.md), the exact request/source/decision pins and [current software qualification](research/review-planning-20261030.json); preserve the original run and all review labels. |
| Composition, atlas, reference mappings or figures | [Composition contract](docs/research/composition-analysis.md), [reference and atlas](docs/research/invertebrate-advancement.md), [style guide](docs/style-guide.md) |
| Scholarly prose, bibliography or images | [Style guide](docs/style-guide.md), [biological-symbolism scholarship](docs/research/biological-symbolism.md), [visual witnesses](docs/research/visual-evidence.md), source and reading ledgers |
| Manuscript preparation, PDF or delivery | [Render guide](docs/manuscript/README.md), [current verification](research/verification.json), [privacy](PRIVACY.md) |

## Work in the right layer

- Import generic acquisition, recovery, portable schemas, matching, statistics,
  proximity, composition, concentration, hierarchy, review planning and custody from `blake`.
  Put a reusable algorithm change upstream and qualify its exact new pin before
  adopting it here. Use explicit schema conversion from
  `blake.methods.schema_conversion`.
- Use the actual pinned docxology/template hydration, validation, PDF and web
  writers for current manuscripts. Keep native numbering and cross-references
  in the authored grammar; the application owns its frontmatter and domain
  diagrams. Read the render guide before changing that boundary.
- Keep channel/category selections, ambiguous animal senses, review policy,
  domain visual encodings and literary interpretation in this application.
  Federalism is an architectural sibling, not a runtime dependency.
- Follow the mounted GitVault operating contract. Use the supported repository
  lease for this private identity and matching worktree/common store. Keep
  environments, caches and temporary files external, and verify both
  `sys.prefix` and `sys.base_prefix` before Python gates.
- Treat `pyproject.toml` and `uv.lock` as the current executable SDK selection.
  Keep the reviewed paper's historical producer, corpus pin, vocabulary,
  decisions and sealed receipts intact when the current runtime advances.
- Write new result epochs to new destinations. Admission pins come from trusted
  caller-held records; completion receipts close artifacts after successful
  publication. Retain failed attempts and explicit unavailable states.

## Finish a change

Run the [README verification commands](README.md#verification-and-scope) and
the affected real workflow with a positive case and its rejecting control.
Use the repository's declared tools and scope coverage to the code exercised.
Documentation edits need link, command and evidence-claim review rather than
tests that pin prose.

For a paper change, preserve the preceding source and prepare and render a new
epoch through the actual template. The current layout requires an authentic
Blake cover on physical page 1, three distinct graphical abstracts on pages
2–4, and contents beginning on page 5. A reset printed page counter does not
prove physical placement. Check citations, native counters and every
affected physical page, and bind the new PDF separately from earlier outputs.
The [status index](docs/PROJECT_STATUS.md) defines which research tasks remain
open; code success does not close them. Verify private visibility and exact
local/remote `main` identity at delivery. Keep raw provider expression and source
captures in their ignored private custody.
