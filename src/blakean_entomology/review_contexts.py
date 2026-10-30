"""Describe authored contextual decisions without changing source eligibility."""

from collections import Counter
from pathlib import Path

from blake.methods.models import Digest, EvidenceError, FrozenModel
from blake.methods.runs import digest, read_regular
from pydantic import Field

from .core import load_run, review
from .models import Decision, ReviewDecision, ReviewSummary, is_animal_decision


class ContextCell(FrozenModel):
    """One explicit term-by-decision cell, including a zero."""

    term_id: str
    decision: Decision
    candidates: int = Field(ge=0)


class ContextCohort(FrozenModel):
    """Keep the source role and plane independent of the contextual judgment."""

    role: str
    plane: str
    candidates: int = Field(ge=0)
    animal_candidates: int = Field(ge=0)


class ContextAudit(FrozenModel):
    """Text-free aggregation of an explicitly bound, purposively selected review."""

    run_sha256: Digest
    decisions_sha256: Digest
    summary: ReviewSummary
    cells: tuple[ContextCell, ...]
    cohorts: tuple[ContextCohort, ...]
    work_groups: int = Field(ge=1)
    source_units: int = Field(ge=1)
    generator_sha256: Digest
    scope: str = (
        "Authored category-source-span decisions only. Source roles remain unchanged. "
        "Purposive selection gives no prevalence, accuracy, distinct-scene or species estimate."
    )


def summarize_contexts(
    directory: Path, decisions_path: Path, expected_run_sha256: str
) -> ContextAudit:
    """Reuse core custody/policy and expose the same pinned run's source facets."""
    raw = read_regular(decisions_path)
    decisions = tuple(
        ReviewDecision.model_validate_json(line) for line in raw.splitlines() if line.strip()
    )
    if not decisions:
        raise EvidenceError("context_review_empty", str(decisions_path))
    summary = review(directory, decisions_path, expected_run_sha256)
    # The pinned second load supplies metadata absent from ReviewSummary. Both
    # loads require the same immutable run rather than accepting an unbound queue.
    _run, _counts, hits = load_run(directory, expected_run_sha256)
    if digest(raw) != summary.decisions_sha256 or read_regular(decisions_path) != raw:
        raise EvidenceError("context_review_changed", str(decisions_path))
    by_id = {hit.hit_id: hit for hit in hits}
    selected = tuple(by_id[decision.hit_id] for decision in decisions)
    counts = Counter(
        (hit.term_id, decision.decision) for hit, decision in zip(selected, decisions, strict=True)
    )
    cohorts = Counter((hit.text_role, hit.source_plane) for hit in selected)
    animal_cohorts = Counter(
        (hit.text_role, hit.source_plane)
        for hit, decision in zip(selected, decisions, strict=True)
        if is_animal_decision(decision.decision)
    )
    return ContextAudit(
        run_sha256=expected_run_sha256,
        decisions_sha256=digest(raw),
        summary=summary,
        cells=tuple(
            ContextCell(term_id=term, decision=decision, candidates=counts[term, decision])
            for term in sorted({hit.term_id for hit in selected})
            for decision in Decision
        ),
        cohorts=tuple(
            ContextCohort(
                role=role,
                plane=plane,
                candidates=count,
                animal_candidates=animal_cohorts[role, plane],
            )
            for (role, plane), count in sorted(cohorts.items())
        ),
        work_groups=len({hit.work_id for hit in selected}),
        source_units=len({hit.passage_id for hit in selected}),
        generator_sha256=digest(read_regular(Path(__file__))),
    )
