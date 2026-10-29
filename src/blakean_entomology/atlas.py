"""Audit the full vocabulary and stratify source roles through shared statistics."""

from collections import Counter, defaultdict
from heapq import heappop, heappush
from pathlib import Path

from blake.methods.profiles import RetrievalProfile, runtime_profile
from blake.methods.runs import digest, read_regular, write_new
from blake.methods.statistics import analyze_inventory
from blake.methods.statistics_models import SourceUnit
from blake.studies import StudySpec, scan_passages
from blake.text_search.models import Passage
from blake.text_search.normalize import tokenize, tokens

from .atlas_models import (
    AtlasReceipt,
    CoverageCohort,
    FormCoverage,
    ReviewEpoch,
    VocabularyOverlap,
)
from .models import CorpusPin, ReviewSummary
from .producer import application_code_sha256
from .taxonomy import load_reference
from .workflows import load_pinned_bundle, require_private_output


def atlas_from_passages(
    passages: tuple[Passage, ...],
    spec: StudySpec,
    pin: CorpusPin,
    reference_sha256: str,
    historical_summary: bytes | None = None,
) -> AtlasReceipt:
    """Scan once; delegate every rate, work average and exact-text check to core."""
    study = scan_passages(passages, spec)
    profile = runtime_profile(RetrievalProfile.NFKC_TOKENS_V2)
    counts = Counter((h.passage_id, h.term_id) for h in study.hits)
    expressions = Counter((h.term_id, h.expression.casefold()) for h in study.hits)
    normalized = Counter((h.term_id, tokens(h.expression)) for h in study.hits)
    primary_expressions = Counter(
        (h.term_id, h.expression.casefold()) for h in study.hits if h.blake_primary
    )
    primary_normalized = Counter(
        (h.term_id, tokens(h.expression)) for h in study.hits if h.blake_primary
    )
    spans = Counter((h.passage_id, h.start, h.end) for h in study.hits)
    active_ends: list[int] = []
    previous_passage = ""
    overlapping_pairs = 0
    for hit in sorted(study.hits, key=lambda h: (h.passage_id, h.start, h.end)):
        if hit.passage_id != previous_passage:
            active_ends.clear()
            previous_passage = hit.passage_id
        while active_ends and active_ends[0] <= hit.start:
            _ = heappop(active_ends)
        overlapping_pairs += len(active_ends)
        heappush(active_ends, hit.end)
    query_ids = tuple(t.term_id for t in spec.terms)
    inventories: defaultdict[tuple[str, str, str], list[SourceUnit]] = defaultdict(list)
    for p in passages:
        inventories[(p.text_role, p.source_plane, p.author_id)].append(
            SourceUnit(
                passage_id=p.passage_id,
                work_id=p.work_id,
                title=p.title,
                edition_id=p.edition_id,
                copy_id=p.copy_id,
                text_sha256=digest(p.text.encode()),
                tokens=len(tokenize(p.text).terms),
                occurrences={q: counts[p.passage_id, q] for q in query_ids},
            )
        )
    cohorts: list[CoverageCohort] = []
    for (role, plane, author), units in sorted(inventories.items()):
        statistics = analyze_inventory(tuple(units), query_ids, profile)
        measure = statistics.queries[0]
        cohorts.append(
            CoverageCohort(
                role=role,
                plane=plane,
                author_id=author,
                source_units=measure.copy_retaining.source_units,
                tokens=measure.copy_retaining.tokens,
                exact_text_units=measure.exact_text.source_units,
                work_groups=len({u.work_id for u in units}),
                inventory_sha256=statistics.inventory_sha256,
                categories=statistics.queries,
                works=tuple(s for s in statistics.strata if s.dimension == "work"),
            )
        )
    aliases: defaultdict[tuple[str, ...], list[tuple[str, str]]] = defaultdict(list)
    forms: list[FormCoverage] = []
    for term in spec.terms:
        for form in term.forms:
            normalized_form = tokens(form)
            aliases[normalized_form].append((term.term_id, form))
            forms.append(
                FormCoverage(
                    term_id=term.term_id,
                    form=form,
                    normalized_tokens=normalized_form,
                    equivalent_form_candidates=normalized[term.term_id, normalized_form],
                    exact_surface_candidates=expressions[term.term_id, form.casefold()],
                    primary_equivalent_form_candidates=primary_normalized[
                        term.term_id, normalized_form
                    ],
                    primary_exact_surface_candidates=primary_expressions[
                        term.term_id, form.casefold()
                    ],
                )
            )
    historical = None
    if historical_summary is not None:
        old = ReviewSummary.model_validate_json(historical_summary)
        historical = ReviewEpoch(
            run_sha256=old.run_sha256,
            decisions_sha256=old.decisions_sha256,
            candidate_hits=old.candidate_hits,
            reviewed_hits=old.reviewed_hits,
            unreviewed_hits=old.unreviewed_hits,
        )
    return AtlasReceipt(
        application_code_sha256=application_code_sha256(),
        corpus_pin=pin,
        vocabulary_sha256=study.spec_sha256,
        reference_sha256=reference_sha256,
        methods_sha256=study.methods_sha256,
        profile=profile,
        scanned_units=study.scanned_passages,
        candidates=len(study.hits),
        primary_candidates=sum(h.blake_primary for h in study.hits),
        distinct_source_spans=len(spans),
        multiply_categorized_spans=sum(n > 1 for n in spans.values()),
        overlapping_candidate_pairs=overlapping_pairs,
        category_count=len(spec.terms),
        explicit_form_count=len(forms),
        denominators=study.denominators,
        category_role_plane=study.rows,
        forms=tuple(forms),
        cohorts=tuple(cohorts),
        normalized_alias_groups=tuple(
            VocabularyOverlap(
                normalized_tokens=k,
                forms=tuple(f for _, f in entries),
                categories=tuple(sorted({t for t, _ in entries})),
            )
            for k, entries in sorted(aliases.items())
            if len(entries) > 1
        ),
        historical_review=historical,
        historical_review_summary_sha256=(
            digest(historical_summary) if historical_summary is not None else None
        ),
    )


def atlas_workflow(
    bundle: Path,
    pin: CorpusPin,
    spec: StudySpec,
    reference: Path,
    reference_sources: Path,
    reference_sha256: str,
    output: Path,
    historical_summary: Path | None = None,
) -> AtlasReceipt:
    """Verify every input before and after computation; publish exclusively last."""
    require_private_output(output, bundle)
    _ = load_reference(reference, reference_sources, reference_sha256, spec)
    snapshot = load_pinned_bundle(bundle, pin)
    historical = read_regular(historical_summary) if historical_summary is not None else None
    receipt = atlas_from_passages(snapshot.passages, spec, pin, reference_sha256, historical)
    _ = load_pinned_bundle(bundle, pin)
    _ = load_reference(reference, reference_sources, reference_sha256, spec)
    if historical_summary is not None and read_regular(historical_summary) != historical:
        from .models import EvidenceError

        raise EvidenceError("historical_summary_changed", str(historical_summary))
    _ = write_new(output, (receipt.model_dump_json(indent=2) + "\n").encode())
    return receipt
