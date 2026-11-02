"""Refuse internally contradictory geometry and lost source/window membership."""

import pytest
from pydantic import ValidationError
from test_geometry import RUN, compute
from test_geometry import geometry_inputs as geometry_inputs

from blakean_entomology.geometry_models import GeometryReport, SourceGeometry, SpanMeasure
from blakean_entomology.models import EvidenceError


def test_window_with_changed_selected_hit_refuses(geometry_inputs) -> None:
    passages, hits, decisions, windows, spec = geometry_inputs
    altered = windows[0].model_copy(update={"hit": hits[0]})
    with pytest.raises(EvidenceError, match="geometry_window_membership"):
        compute((passages, hits, decisions, (altered,), spec))


def test_coherent_window_that_excludes_its_selected_hit_refuses(geometry_inputs) -> None:
    passages, hits, decisions, windows, spec = geometry_inputs
    altered = windows[0].model_copy(update={"window_start": 4, "window_end": 8, "text": "d ef"})
    with pytest.raises(EvidenceError, match="geometry_window_extent"):
        compute((passages, hits, decisions, (altered,), spec))


@pytest.mark.parametrize(
    "update",
    [
        {"union_codepoints": 999},
        {"overlap_codepoints": 999},
        {"overlapping_pairs": 999},
        {"source_components": 999},
    ],
)
def test_impossible_measure_refuses(geometry_inputs, update) -> None:
    measure = compute(geometry_inputs).sources[0].measure
    with pytest.raises(ValidationError, match="geometry_measure_bounds"):
        SpanMeasure.model_validate(measure.model_dump() | update)


@pytest.mark.parametrize(
    "update",
    [
        {"candidate_hits": 999},
        {"reviewed_hits": 2},
        {"unreviewed_hits": 999},
        {"documented_window_events": 999},
        {"sources": ()},
        {"cohorts": ()},
    ],
)
def test_contradictory_report_refuses(geometry_inputs, update) -> None:
    report = compute(geometry_inputs)
    with pytest.raises(ValidationError, match="geometry_report_membership"):
        GeometryReport.model_validate(report.model_dump() | update)


def test_invalid_registry_and_empty_source_refuse(geometry_inputs) -> None:
    passages, hits, decisions, windows, spec = geometry_inputs
    altered = spec.model_copy(
        update={"terms": (spec.terms[0].model_copy(update={"group": "unknown"}),)}
    )
    with pytest.raises(EvidenceError, match="geometry_registry"):
        compute((passages, (), (), (), altered))
    with pytest.raises(ValidationError):
        compute(((passages[0].model_copy(update={"text": ""}),), (), (), (), spec))
    # An unavailable primary cohort has no denominator, not an artificial zero rate.
    report = compute(((passages[-1],), (), (), (), spec))
    assert report.run_sha256 == RUN
    assert report.primary.equal_unit_occupancy is None


@pytest.mark.parametrize(
    "update",
    [
        {"codepoints": 1},
        {"reviewed_hits": 2},
        {"reviewed_union_codepoints": 0},
        {"unreviewed_union_codepoints": 0},
        {"documented_window_events": 2},
        {"documented_window_codepoints": 0},
        {"reviewed_without_documented_window": 1},
    ],
)
def test_inconsistent_source_extents_refuse(geometry_inputs, update) -> None:
    source = next(s for s in compute(geometry_inputs).sources if s.passage_id == "first")
    with pytest.raises(ValidationError, match="geometry_source_support"):
        SourceGeometry.model_validate(source.model_dump() | update)
