"""Source-local set oracles distinguish matching, review and reading exposure."""

from collections import Counter
from typing import TypeAlias

import pytest
from blake.methods.runs import digest
from blake.studies import StudyHit, StudySpec, StudyTerm, scan_passages
from blake.text_search.models import Passage
from pydantic import ValidationError

from blakean_entomology.geometry import analyze_geometry
from blakean_entomology.geometry_models import DocumentedWindow, GeometryReport
from blakean_entomology.models import Decision, EvidenceError, ReviewDecision

RUN = "a" * 64
GeometryInputs: TypeAlias = tuple[
    tuple[Passage, ...],
    tuple[StudyHit, ...],
    tuple[ReviewDecision, ...],
    tuple[DocumentedWindow, ...],
    StudySpec,
]


@pytest.fixture
def geometry_inputs() -> GeometryInputs:
    first = Passage(
        passage_id="first",
        work_id="work-a",
        author_id="william-blake-1757-1827",
        title="Synthetic source",
        edition_id="edition-a",
        edition="Synthetic edition",
        locator="section one",
        locator_kind="section",
        source_url="https://example.org/a",
        rights="Synthetic fixture",
        text_role="primary",
        source_plane="reading",
        text="ab cd ef",
        source_sha256="b" * 64,
    )
    passages = (
        first,
        first.model_copy(update={"passage_id": "copy", "edition_id": "edition-b"}),
        first.model_copy(update={"passage_id": "zero", "work_id": "work-b", "text": "zz zz zz"}),
        first.model_copy(
            update={
                "passage_id": "xml",
                "text_role": "unverified",
                "source_plane": "xml",
                "author_id": "unverified",
            }
        ),
    )
    spec = StudySpec(
        study_id="synthetic",
        title="Synthetic categories",
        terms=(
            StudyTerm(term_id="wide-a", group="insect", forms=("ab cd",)),
            StudyTerm(term_id="wide-b", group="associated", forms=("ab cd",)),
            StudyTerm(term_id="narrow", group="motion", forms=("cd",)),
            StudyTerm(term_id="last", group="generic", forms=("ef",)),
        ),
    )
    hits = scan_passages(passages, spec).hits
    chosen = next(h for h in hits if h.passage_id == "first" and h.term_id == "narrow")
    decision = ReviewDecision(
        run_sha256=RUN,
        hit_id=chosen.hit_id,
        decision=Decision.UNCERTAIN,
        reviewer="Synthetic reviewer",
        rationale="Synthetic control; no literary claim",
    )
    window = DocumentedWindow(
        batch_id="event-a",
        hit=chosen,
        window_start=1,
        window_end=7,
        window_sha256=digest(first.text[1:7].encode()),
        text=first.text[1:7],
    )
    return passages, hits, (decision,), (window,), spec


def compute(inputs: GeometryInputs) -> GeometryReport:
    return analyze_geometry(*inputs, run_sha256=RUN)


def test_source_local_geometry_has_independent_arithmetic(geometry_inputs) -> None:
    result = compute(geometry_inputs)
    source = next(s for s in result.sources if s.passage_id == "first")
    # [0,5),[0,5),[3,5),[6,8): union 7, sum 14, overlap area 5, three pairs.
    assert (
        source.measure.records,
        source.measure.union_codepoints,
        source.measure.summed_codepoints,
        source.measure.overlap_codepoints,
        source.measure.overlapping_pairs,
    ) == (4, 7, 14, 5, 3)
    assert source.measure.excess_codepoints == 7
    assert source.reviewed_union_codepoints == 2
    assert source.unreviewed_union_codepoints == 7
    assert source.documented_window_codepoints == 6
    assert source.reviewed_without_documented_window == 0
    assert result.candidate_hits == 12
    assert result.reviewed_hits == 1
    assert result.unreviewed_hits == 11
    assert result.primary.source_units == 3  # Includes the zero-hit primary unit.
    assert result.primary.codepoints == 24
    assert result.primary.measure.union_codepoints == 14
    assert result.primary.pooled_occupancy == pytest.approx(14 / 24)
    assert result.primary.equal_unit_occupancy == pytest.approx(7 / 12)
    assert result.primary.equal_work_occupancy == pytest.approx(7 / 16)
    assert sum(c.measure.union_codepoints for c in result.cohorts) == 21
    assert sum(c.measure.overlapping_pairs for c in result.cohorts) == 9


def test_every_source_matches_an_independent_codepoint_multiset(geometry_inputs) -> None:
    passages, hits, *_ = geometry_inputs
    result = compute(geometry_inputs)
    for source in result.sources:
        positions = Counter(
            x for h in hits if h.passage_id == source.passage_id for x in range(h.start, h.end)
        )
        local = [h for h in hits if h.passage_id == source.passage_id]
        assert source.measure.union_codepoints == len(positions)
        assert source.measure.overlap_codepoints == sum(n >= 2 for n in positions.values())
        assert source.measure.overlapping_pairs == sum(
            max(a.start, b.start) < min(a.end, b.end)
            for i, a in enumerate(local)
            for b in local[i + 1 :]
        )
        assert source.codepoints == len(
            next(p.text for p in passages if p.passage_id == source.passage_id)
        )


def test_no_window_is_unavailable_and_rereading_does_not_enlarge_area(geometry_inputs) -> None:
    passages, hits, decisions, windows, spec = geometry_inputs
    absent = compute((passages, hits, decisions, (), spec)).sources[1]
    first = next(
        s for s in compute((passages, hits, decisions, (), spec)).sources if s.passage_id == "first"
    )
    assert first.documented_window_codepoints is None
    assert first.reviewed_without_documented_window == 1
    assert absent.documented_window_codepoints is None
    repeated = windows + (windows[0].model_copy(update={"batch_id": "event-b"}),)
    source = next(
        s
        for s in compute((passages, hits, decisions, repeated, spec)).sources
        if s.passage_id == "first"
    )
    assert source.documented_window_events == 2
    assert source.documented_window_codepoints == 6
    assert source.reviewed_hits == 1


def test_channel_unions_are_not_a_partition(geometry_inputs) -> None:
    result = compute(geometry_inputs)
    channels = {c.channel: c.measure.union_codepoints for c in result.primary_channels}
    assert channels == {"name_family": 10, "associated": 10, "motion": 4, "broad_label": 4}
    assert sum(channels.values()) > result.primary.measure.union_codepoints
    overlap = {(x.left, x.right): x.codepoints for x in result.channel_intersections}
    assert overlap["name_family", "associated"] == 10
    assert overlap["associated", "motion"] == 4
    assert overlap["motion", "broad_label"] == 0


@pytest.mark.parametrize(
    "update",
    [
        {"start": True},
        {"start": 5, "end": 5},
        {"end": 999},
        {"text_sha256": "0" * 64},
        {"expression": "wrong"},
        {"author_id": "wrong"},
        {"passage_id": "absent"},
        {"group": "unknown"},
    ],
)
def test_invalid_hit_boundaries_or_facets_refuse(geometry_inputs, update) -> None:
    passages, hits, decisions, windows, spec = geometry_inputs
    with pytest.raises((ValidationError, EvidenceError)):
        compute(
            (passages, (hits[0].model_copy(update=update), *hits[1:]), decisions, windows, spec)
        )


@pytest.mark.parametrize(
    "update",
    [
        {"window_start": True},
        {"window_start": 5},
        {"window_end": 999},
        {"window_sha256": "0" * 64},
        {"text": "wrong"},
    ],
)
def test_invalid_documented_window_refuses(geometry_inputs, update) -> None:
    passages, hits, decisions, windows, spec = geometry_inputs
    with pytest.raises((ValidationError, EvidenceError)):
        compute((passages, hits, decisions, (windows[0].model_copy(update=update),), spec))


def test_empty_input_duplicate_ids_and_unbound_review_refuse(geometry_inputs) -> None:
    passages, hits, decisions, windows, spec = geometry_inputs
    for candidate in [
        ((), (), (), (), spec),
        (passages + passages[:1], hits, decisions, windows, spec),
        (passages, hits + hits[:1], decisions, windows, spec),
        (passages, hits, decisions * 2, windows, spec),
        (passages, hits, (), windows, spec),
        (
            passages,
            hits,
            (decisions[0].model_copy(update={"run_sha256": "c" * 64}),),
            windows,
            spec,
        ),
        (passages, hits, decisions, windows * 2, spec),
    ]:
        with pytest.raises((ValidationError, EvidenceError)):
            compute(candidate)


def test_zero_hits_preserve_denominator_and_undefined_primary(geometry_inputs) -> None:
    passages, _hits, _decisions, _windows, spec = geometry_inputs
    zero = next(p for p in passages if p.passage_id == "zero")
    result = compute(((zero,), (), (), (), spec))
    assert result.primary.measure.union_codepoints == 0
    assert result.primary.pooled_occupancy == result.primary.equal_unit_occupancy == 0
    xml = next(p for p in passages if p.passage_id == "xml")
    result = compute(((xml,), (), (), (), spec))
    assert result.primary.source_units == 0
    assert result.primary.pooled_occupancy is None
