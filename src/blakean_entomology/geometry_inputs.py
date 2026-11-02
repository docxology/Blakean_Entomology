"""Verify original source slices and independently retained reading windows."""

from collections.abc import Mapping

from blake.methods.annotations import validate_decision_membership
from blake.methods.runs import digest
from blake.studies import StudyHit, StudySpec
from blake.text_search.models import Passage

from .composition import CHANNELS
from .geometry_models import DocumentedWindow
from .models import EvidenceError, ReviewDecision


def validate_geometry_inputs(
    passages: tuple[Passage, ...],
    hits: tuple[StudyHit, ...],
    decisions: tuple[ReviewDecision, ...],
    windows: tuple[DocumentedWindow, ...],
    spec: StudySpec,
    run_sha256: str,
) -> Mapping[str, Passage]:
    """Reject coercion, missing identities, changed facets and unsupported reading credit."""
    if not passages or len({p.passage_id for p in passages}) != len(passages):
        raise EvidenceError(
            "geometry_source_membership", "Require unique nonempty source inventory"
        )
    if len({h.hit_id for h in hits}) != len(hits):
        raise EvidenceError("geometry_hit_membership", "Duplicate candidate ID")
    for passage in passages:
        _ = Passage.model_validate(passage.model_dump(), strict=True)
    _ = StudySpec.model_validate(spec.model_dump(), strict=True)
    if any(term.group not in CHANNELS for term in spec.terms):
        raise EvidenceError("geometry_registry", "Unknown application registry channel")
    source_by_id = {p.passage_id: p for p in passages}
    terms = {t.term_id: t for t in spec.terms}
    hashes = {p.passage_id: digest(p.text.encode()) for p in passages}
    for hit in hits:
        _ = StudyHit.model_validate(hit.model_dump(), strict=True)
        source = source_by_id.get(hit.passage_id)
        term = terms.get(hit.term_id)
        if source is None or term is None or term.group not in CHANNELS:
            raise EvidenceError("geometry_hit_membership", hit.hit_id)
        if not 0 <= hit.start < hit.end <= len(source.text):
            raise EvidenceError("geometry_hit_extent", hit.hit_id)
        hit_facets = (
            hit.work_id,
            hit.title,
            hit.edition_id,
            hit.copy_id,
            hit.locator,
            hit.rights,
            hit.author_id,
            hit.text_role,
            hit.source_plane,
            hit.source_sha256,
        )
        source_facets = (
            source.work_id,
            source.title,
            source.edition_id,
            source.copy_id,
            source.locator,
            source.rights,
            source.author_id,
            source.text_role,
            source.source_plane,
            source.source_sha256,
        )
        if (
            hit_facets != source_facets
            or hit.source_url != str(source.source_url)
            or hit.text_sha256 != hashes[hit.passage_id]
            or hit.expression != source.text[hit.start : hit.end]
            or hit.group != term.group
            or hit.blake_primary
            != (
                source.author_id == "william-blake-1757-1827"
                and source.text_role == "primary"
                and source.source_plane == "reading"
            )
        ):
            raise EvidenceError("geometry_source_slice", hit.hit_id)
    validate_decision_membership(decisions, hits, run_sha256)
    reviewed = {d.hit_id for d in decisions}
    candidates = {h.hit_id: h for h in hits}
    if len({w.batch_id for w in windows}) != len(windows):
        raise EvidenceError("geometry_window_membership", "Duplicate reading event ID")
    for original in windows:
        window = DocumentedWindow.model_validate(original)
        _ = StudyHit.model_validate(window.hit.model_dump(), strict=True)
        hit = candidates.get(window.hit.hit_id)
        if hit is None or hit != window.hit or hit.hit_id not in reviewed:
            raise EvidenceError("geometry_window_membership", window.batch_id)
        source = source_by_id[hit.passage_id]
        if (
            not 0
            <= window.window_start
            <= hit.start
            < hit.end
            <= window.window_end
            <= len(source.text)
        ):
            raise EvidenceError("geometry_window_extent", window.batch_id)
        actual = source.text[window.window_start : window.window_end]
        if actual != window.text or digest(actual.encode()) != window.window_sha256:
            raise EvidenceError("geometry_window_slice", window.batch_id)
    return source_by_id
