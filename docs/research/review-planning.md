# Request-pinned review planning

Review planning prepares a deterministic workload of retrieval leads. It makes
no literary judgment and changes no reviewed/unreviewed denominator. Public
Blake owns ranking, round-robin scheduling, global unit caps, serialization and
batch verification. This application owns the original run, decision vocabulary,
eligibility and independently pinned request.

## Declared inputs

The original run is `analysis_output/baseline-v3`, SHA-256
`12d0312378460493f894618e6dfc44b36593d8c9f85dfd2cf45f443a09af2633`.
Its trusted pin is retained in
[the dated contextual study](../../research/context-review-study-20261029.json)
and [contextual-review contract](context-review-20261029.md).
The independently pinned combined decision input is
[the 47-record JSONL](../../research/context-review-combined-20261029.jsonl),
SHA-256 `581a53bef6642ee1420cdc312b4f10696293952bb696ae3f588e6833f4478755`,
also recorded in the study and current-source ledger. These 47 decisions remain
47; the 35,992 baseline unreviewed candidates do not become reviewed by planning.

The checked-in request declares a target of 25, a retained seed, term/source-plane/
source-role strata, exact whole-text SHA units and at most one selected candidate
per exact-text unit. The target is a request, not an achieved count. Shortfall
remains explicit. This greedy plan is neither a probability sample nor a quota
optimizer, and shared units can starve strata. Equal whole texts do not reconcile
embedded poems or establish independent copies.

Scope must be explicit: `blake_primary_reading` requires the William Blake
author ID, primary source role and reading plane together; `all_sources`
retains every original source facet. An isolated `blake_primary` flag cannot
promote or demote a witness. All supplied authored decisions are validated
against the complete original run before filtering. Only reviewed IDs inside
the selected scope become exclusions. Global and in-scope counts remain separate
in `load_planning_input`; a planned batch adds no decision.

## Plan and independently verify

Run from this application's root with the qualified locked installed SDK.
Candidate-source overlays are development evidence and do not establish that
installed qualification. The request pin must come from a trusted external
record of the declared request, separately from the batch receipt pin.

The retained batch already exists. Verify it without trying to recreate it:

~~~sh
uv run --locked --no-sync blake-entomology verify-review \
  --request research/review-planning-request-v1.json \
  --request-sha256 "$REQUEST_SHA256" \
  --batch analysis_output/review-planning-20261030-01/batch \
  --batch-sha256 "$BATCH_RECEIPT_SHA256"
~~~

For a separate planning epoch, choose a genuinely unused directory under
`analysis_output/`; leave the request and retained batch unchanged:

~~~sh
: "${FRESH_BATCH:?Choose a new unused analysis_output directory}"
uv run --locked --no-sync blake-entomology plan-review \
  --request research/review-planning-request-v1.json \
  --request-sha256 "$REQUEST_SHA256" \
  --output "$FRESH_BATCH"
~~~

Retain that new batch's `run.json` hash independently before verifying its new
path. The request pin and batch pin are separate trusted inputs; do not infer a
new batch's authority from the retained example. An occupied destination must
refuse and must not be cleared to make a recipe succeed.

The batch contains exactly `plan.json`, selected `hits.jsonl`, a blank
`review-queue.csv` and final `run.json`. Keep provider contexts private under
ignored `analysis_output/`; keep notes and edited queue copies outside the
immutable batch. Occupied, symlinked and source-overlapping outputs refuse.

Verification rederives the original scoped pool and exclusions from the pinned
request and complete validated decisions. It checks the full verified plan spec,
including selection and exclusions. Matching a stored context-hash string alone
cannot authorize another policy. The core verifier admits its exact files,
recomputes the plan and checks selected fields/order and unchanged blank queue;
historical producer identity remains historical.

A later contextual review binds decisions to the **original source-run SHA**
and original hit IDs, rather than substituting the planning batch receipt.
Use the existing authored-review workflow; preserve uncertainty, source roles,
repetitions, locators, disagreements and all omitted candidates. Planning does
not confer reading credit, representativeness, accuracy or scholarly acceptance.

## Qualification boundaries

Real synthetic original runs, normal JSON/CSV admission and subprocess CLI
controls cover wrong request/source/decision/batch pins, globally invalid
out-of-scope judgments, facet-based eligibility, forged valid batches with a
different full policy, blank queues and private output custody. No mock loaders
or fabricated counters are used. Source-only checks remain distinct from fresh
normal installed qualification at the exact adopted public Git pin.

This operational unit changes no corpus, vocabulary, authored decision,
manuscript, bibliography, configuration, native renderer or retained paper.

## Qualified planned batch

The normal-installed 0.5.0 application, using public Blake 0.5.0 at `36b874e76d7e0549d0ea6b9f0713ced7fb41afa8`, selected 25 candidates; shortfall is 0. The complete source run contains 36,039 candidates and 47 validated authored decisions; the requested scope contains 2,498 candidates and 37 exclusions. The selected CSV keeps every judgment field blank and the original source-run and decision bytes unchanged. No authored decision was added.

Request SHA-256: `8d168da859205c9b6aee2bff385c1a5642614a4f1b8af695ec5c5d3a3a37d184`. Batch receipt SHA-256: `3682e77758361fcdb63b7728c0098dea571ab5a98362f3ba8f9aae1873cc1771`. Source-pool SHA-256: `7284c76b260f9ef6c5fe0b9924b8ff343a803ec211624681af4e92633e08682b`. The private batch is `analysis_output/review-planning-20261030-01/batch`. Actual CLI controls reject wrong request/batch pins, occupied/source-overlapping outputs and an otherwise core-valid batch with the same context hash but a different full selection policy.
