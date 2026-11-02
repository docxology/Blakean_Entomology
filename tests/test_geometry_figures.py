"""Real artists, source extents and vector/raster receipts; empty plots must fail."""

from pathlib import Path

import pytest
from blake.methods.storage import verify_file
from matplotlib.figure import Figure
from test_geometry import RUN
from test_geometry import geometry_inputs as geometry_inputs

from blakean_entomology.geometry import analyze_geometry
from blakean_entomology.geometry_figures import (
    occupancy_figure,
    render_geometry_figures,
    validate_geometry_figures,
)
from blakean_entomology.geometry_models import GeometryReport
from blakean_entomology.geometry_review_figure import review_geometry_figure
from blakean_entomology.models import EvidenceError


@pytest.fixture
def figure_report(geometry_inputs) -> GeometryReport:
    passages, hits, decisions, windows, spec = geometry_inputs
    windows = (*windows, windows[0].model_copy(update={"batch_id": "event-b"}))
    return analyze_geometry(
        passages,
        hits,
        decisions,
        windows,
        spec,
        run_sha256=RUN,
        illustrative_source_ids=("first", "zero", "xml"),
        window_pairs=(("event-a", "event-b"),),
    )


def test_source_plot_has_every_channel_and_declared_candidate(figure_report) -> None:
    figure = occupancy_figure(figure_report)
    assert isinstance(figure, Figure)
    bars, strips = figure.axes
    assert len(bars.containers[0]) == len(figure_report.primary_channels) == 4
    expected = sum(
        len(s.hits)
        for s in figure_report.sources
        if s.passage_id in figure_report.illustrative_source_ids
    )
    assert len(strips.lines) == len(figure_report.illustrative_source_ids) + expected
    figure.clear()


def test_review_plot_preserves_actual_window_geometry(figure_report) -> None:
    figure = review_geometry_figure(figure_report)
    assert isinstance(figure, Figure)
    main, detail = figure.axes
    selected = [s for s in figure_report.sources if s.reviewed_hits]
    assert len(main.lines) == len(selected) + figure_report.reviewed_hits
    assert len(main.collections) == figure_report.documented_window_events == 2
    assert len(detail.collections) == len(detail.lines) == 2
    vertices = main.collections[0].get_paths()[0].vertices
    assert min(v[0] for v in vertices) == pytest.approx(1 / 8)
    assert max(v[0] for v in vertices) == pytest.approx(7 / 8)
    figure.clear()


def test_real_plot_products_are_complete_and_cannot_overwrite(
    figure_report, tmp_path: Path
) -> None:
    destination = tmp_path / "figures"
    receipts = render_geometry_figures(figure_report, destination)
    assert len(receipts) == 8  # Two plots, three formats, captions and runtime.
    for receipt in receipts:
        _ = verify_file(tmp_path, receipt.path, receipt.size, receipt.sha256)
        raw = (tmp_path / receipt.path).read_bytes()
        if receipt.path.endswith(".pdf"):
            assert raw.startswith(b"%PDF-")
        if receipt.path.endswith(".png"):
            assert raw.startswith(b"\x89PNG\r\n\x1a\n")
    before = {p.name: p.read_bytes() for p in destination.iterdir()}
    with pytest.raises((FileExistsError, EvidenceError)):
        _ = render_geometry_figures(figure_report, destination)
    assert {p.name: p.read_bytes() for p in destination.iterdir()} == before


def test_empty_review_refuses_before_plot_output(geometry_inputs, tmp_path: Path) -> None:
    passages, hits, _decisions, _windows, spec = geometry_inputs
    report = analyze_geometry(passages, hits, (), (), spec, run_sha256=RUN)
    with pytest.raises(EvidenceError, match="geometry_figure_scope"):
        _ = render_geometry_figures(report, tmp_path / "refused")
    assert not (tmp_path / "refused").exists()


def test_large_facet_plate_refuses(geometry_inputs) -> None:
    passages, hits, decisions, windows, spec = geometry_inputs
    extra = tuple(
        passages[0].model_copy(update={"passage_id": f"extra-{i}", "author_id": f"author-{i}"})
        for i in range(7)
    )
    report = analyze_geometry((*passages, *extra), hits, decisions, windows, spec, run_sha256=RUN)
    with pytest.raises(EvidenceError, match="geometry_figure_scope"):
        validate_geometry_figures(report)
