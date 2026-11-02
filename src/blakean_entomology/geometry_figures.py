"""Source occupancy and review geometry from a pinned, complete analytical report."""

import json
from pathlib import Path

from blake.methods.models import EvidenceError, FileReceipt
from blake.methods.runs import reserve
from blake.methods.storage import publish_bytes

from .geometry_models import GeometryReport
from .geometry_plotting import PlotFigure, figure_bytes, new_figure, plot_theme, plotting_runtime
from .geometry_review_figure import review_geometry_figure


def occupancy_figure(report: GeometryReport) -> PlotFigure:
    """Show all source facets, unstacked channel unions and declared positional examples."""
    figure = new_figure((6.3, 8.0))
    _ = figure.text(
        0.04, 0.965, "Where the vocabulary occupies captured text", fontsize=13, weight="bold"
    )
    _ = figure.text(
        0.04,
        0.93,
        f"{report.candidate_hits:,} retained category-span candidates; original source codepoints, "
        + "copies retained.",
        fontsize=8,
    )
    _ = figure.text(0.04, 0.887, "A  Disjoint source facets", fontsize=10, weight="bold")
    headings = (
        (0.04, "Plane / role"),
        (0.32, "Units"),
        (0.40, "Codepoints"),
        (0.55, "Hits"),
        (0.66, "Union %"),
        (0.78, "Overlap cp"),
        (0.91, "Excess cp"),
    )
    for x, label in headings:
        _ = figure.text(x, 0.855, label, fontsize=7.3, weight="bold")
    for row, cohort in enumerate(report.cohorts):
        y = 0.822 - row * 0.043
        values = (
            f"{cohort.plane} / {cohort.role}",
            str(cohort.source_units),
            f"{cohort.codepoints:,}",
            f"{cohort.measure.records:,}",
            "unavailable"
            if cohort.pooled_occupancy is None
            else f"{100 * cohort.pooled_occupancy:.3f}",
            f"{cohort.measure.overlap_codepoints:,}",
            f"{cohort.measure.excess_codepoints:,}",
        )
        for (x, _), value in zip(headings, values, strict=True):
            _ = figure.text(x, y, value, fontsize=7)
    _ = figure.text(
        0.04,
        0.55,
        "Primary eligibility: Blake author + primary role + reading plane; "
        + f"{report.primary.source_units} units / "
        + f"{report.primary.work_groups} recorded work groups.\n"
        + "Complete author facets, zero-hit units and weighting are in the source table.",
        fontsize=7.5,
    )
    axis = figure.add_axes((0.23, 0.325, 0.68, 0.15))
    denominator = report.primary.codepoints
    widths = [
        100 * c.measure.union_codepoints / denominator if denominator else 0.0
        for c in report.primary_channels
    ]
    _ = axis.barh(list(range(len(widths))), widths, color="0.7", edgecolor="0.15")
    _ = axis.set_yticks(
        list(range(len(widths))),
        labels=[c.channel.replace("_", " ") for c in report.primary_channels],
        fontsize=8,
    )
    maximum = max(widths, default=0.0)
    _ = axis.set_xlim(0.0, max(0.1, maximum * 1.1))
    _ = axis.set_ylim(len(widths) - 0.5, -0.5)
    _ = axis.set_xlabel("Occupied original codepoints / all primary codepoints (%)", fontsize=7.5)
    _ = axis.set_title(
        "B  Channel unions overlap; bars are not a partition", loc="left", fontsize=9
    )
    by_source = {s.passage_id: s for s in report.sources}
    if report.illustrative_source_ids:
        strips = figure.add_axes((0.32, 0.11, 0.59, 0.12))
        for row, key in enumerate(report.illustrative_source_ids):
            source = by_source[key]
            _ = strips.plot([0.0, 1.0], [float(row), float(row)], color="0.8", linewidth=0.5)
            for hit in source.hits:
                _ = strips.plot(
                    [hit.interval.start / source.codepoints],
                    [float(row)],
                    color="0.15",
                    marker="|",
                    markersize=4,
                    linewidth=0,
                )
        _ = strips.set_yticks(
            list(range(len(report.illustrative_source_ids))),
            labels=[
                f"{key.removeprefix('archive:')}\n{by_source[key].codepoints:,} cp"
                for key in report.illustrative_source_ids
            ],
            fontsize=6.9,
        )
        _ = strips.set_xticks([0.0, 0.5, 1.0], labels=["0", "0.5", "1"], fontsize=7.5)
        _ = strips.set_xlim(0.0, 1.0)
        _ = strips.set_ylim(len(report.illustrative_source_ids) - 0.5, -0.5)
        _ = strips.set_title("C  Declared illustrative units: match starts", loc="left", fontsize=9)
    _ = figure.text(
        0.04,
        0.02,
        "Overlap cp: support covered by at least two records. "
        + "Excess cp: summed lengths minus union.\n"
        + "XML includes markup and editorial prose; its occupancy is not verse density.\n"
        + "No organism, independent-scene, contextual-review or image-coverage estimate follows.",
        fontsize=7,
    )
    return figure


def validate_geometry_figures(report: GeometryReport) -> None:
    """Refuse unreadable or empty figure contracts before reserving their epoch."""
    _ = GeometryReport.model_validate(report)
    if len(report.cohorts) > 6 or not any(s.reviewed_hits for s in report.sources):
        raise EvidenceError(
            "geometry_figure_scope", "Require at most six facets and a nonempty review"
        )
    if sum(bool(s.reviewed_hits) for s in report.sources) > 32:
        raise EvidenceError("geometry_figure_scope", "Reviewed source plate exceeds 32 rows")


def render_geometry_figures(report: GeometryReport, destination: Path) -> tuple[FileReceipt, ...]:
    """Preserve complete data and captions beside both vector/raster presentations."""
    validate_geometry_figures(report)
    reserve(destination)
    files: list[FileReceipt] = []
    captions = {
        "source-footprint": (
            f"{report.candidate_hits:,} category-source-span candidates "
            f"across {len(report.sources)} retained units. "
            f"Primary: {report.primary.source_units} units, {report.primary.codepoints:,} "
            "original codepoints. Union length counts each codepoint once per source; overlap area "
            "and excess summed length have different multiplicity meanings. Channel unions are "
            "unstacked. Declared positional examples are illustrative, not representative. "
            "Raw XML includes apparatus and markup; source occupancy is not an animal census."
        ),
        "review-exposure": (
            f"{report.reviewed_hits} authored decisions; "
            f"{report.unreviewed_hits:,} candidates remain "
            f"unreviewed. {report.documented_window_events} retained window events; "
            f"{sum(s.reviewed_without_documented_window for s in report.sources)} "
            "reviewed IDs lack "
            "equivalent machine-readable window custody. All reviewed source units are shown. "
            "Ticks make selected starts visible; outlines preserve actual window extents. "
            "Same-source enlargements retain exact original offsets. Repeated reading adds no "
            "independent scenes; no reading credit is inferred from generated snippets."
        ),
    }
    with plot_theme():
        for name, builder in (
            ("source-footprint", occupancy_figure),
            ("review-exposure", review_geometry_figure),
        ):
            figure = builder(report)
            for kind in ("png", "svg", "pdf"):
                entry = publish_bytes(destination / f"{name}.{kind}", figure_bytes(figure, kind))
                files.append(
                    FileReceipt(
                        path=f"{destination.name}/{entry.path}",
                        size=entry.size,
                        sha256=entry.sha256,
                    )
                )
            figure.clear()
        runtime = plotting_runtime()
    entry = publish_bytes(
        destination / "plotting-runtime.json", (json.dumps(runtime, indent=2) + "\n").encode()
    )
    files.append(
        FileReceipt(path=f"{destination.name}/{entry.path}", size=entry.size, sha256=entry.sha256)
    )
    entry = publish_bytes(
        destination / "captions.json", (json.dumps(captions, indent=2) + "\n").encode()
    )
    files.append(
        FileReceipt(path=f"{destination.name}/{entry.path}", size=entry.size, sha256=entry.sha256)
    )
    return tuple(files)
