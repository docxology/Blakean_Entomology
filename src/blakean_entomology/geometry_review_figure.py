"""All reviewed source units, with separately documented reading-window support."""

from blake.methods.intervals import interval_measure

from .geometry_models import GeometryReport
from .geometry_plotting import PlotFigure, new_figure


def review_geometry_figure(report: GeometryReport) -> PlotFigure:
    """Draw every reviewed unit; unknown windows are explicit counts, not zeros."""
    figure = new_figure((6.3, 8.0))
    selected = tuple(s for s in report.sources if s.reviewed_hits)
    _ = figure.text(0.04, 0.965, "What review has covered", fontsize=14, weight="bold")
    unknown = sum(s.reviewed_without_documented_window for s in selected)
    _ = figure.text(
        0.04,
        0.93,
        f"Reviewed IDs: {report.reviewed_hits}; source units: {len(selected)}; "
        + f"documented window events: {report.documented_window_events}.\n"
        + f"Reviewed IDs with unavailable window coordinates: {unknown}.",
        fontsize=8,
    )
    axis = figure.add_axes((0.32, 0.39, 0.56, 0.49))
    for row, source in enumerate(selected):
        y = float(row)
        _ = axis.plot([0.0, 1.0], [y, y], color="0.85", linewidth=0.5)
        for window in source.windows:
            span = window.interval
            _ = axis.broken_barh(
                [(span.start / source.codepoints, (span.end - span.start) / source.codepoints)],
                (y - 0.27, 0.54),
                facecolors="none",
                edgecolors="0.25",
                linewidth=0.6,
            )
        for hit in source.hits:
            if hit.decision is not None:
                _ = axis.plot(
                    [hit.interval.start / source.codepoints],
                    [y],
                    color="0.05",
                    marker="|",
                    markersize=4,
                    linewidth=0,
                )
        _ = axis.text(
            1.03,
            y,
            f"{source.reviewed_hits} / {source.documented_window_events} / "
            + f"{source.reviewed_without_documented_window}",
            fontsize=7,
            va="center",
        )
    _ = axis.set_yticks(
        list(range(len(selected))),
        labels=[s.passage_id.removeprefix("archive:") for s in selected],
        fontsize=7.2,
    )
    _ = axis.set_xticks([0.0, 0.5, 1.0], labels=["0", "0.5", "1"], fontsize=8)
    _ = axis.set_xlim(0.0, 1.0)
    _ = axis.set_ylim(len(selected) - 0.5, -0.5)
    _ = axis.set_xlabel("Source-relative original-codepoint position", fontsize=8)
    _ = figure.text(0.32, 0.905, "A  Every source unit containing an authored decision", fontsize=9)
    _ = figure.text(0.885, 0.905, "R / W / U", fontsize=7)
    by_event = {w.batch_id: (s, w) for s in selected for w in s.windows}
    for index, (left, right) in enumerate(report.window_pairs):
        source, first = by_event[left]
        _, second = by_event[right]
        start = min(first.interval.start, second.interval.start)
        end = max(first.interval.end, second.interval.end)
        detail = figure.add_axes((0.32, 0.205 - index * 0.14, 0.56, 0.07))
        for row, event in enumerate((first, second)):
            _ = detail.broken_barh(
                [(float(event.interval.start), float(event.interval.end - event.interval.start))],
                (row - 0.25, 0.5),
                facecolors="0.85",
                edgecolors="0.3",
                linewidth=0.7,
            )
            hit = next(h for h in source.hits if h.hit_id == event.hit_id)
            _ = detail.plot(
                [float(hit.interval.start), float(hit.interval.end)],
                [float(row), float(row)],
                color="0.05",
                linewidth=2,
            )
        _ = detail.set_yticks([0, 1], labels=[left, right], fontsize=7)
        _ = detail.set_xticks([float(start), float(end)], labels=[str(start), str(end)], fontsize=7)
        _ = detail.set_xlim(float(start), float(end))
        _ = detail.set_ylim(1.6, -0.6)
        union = interval_measure((first.interval, second.interval))
        _ = detail.set_title(
            f"B{index + 1}  {source.passage_id}: two windows, {union:,} cp union",
            loc="left",
            fontsize=8,
        )
    _ = figure.text(
        0.04,
        0.017,
        "R / W / U: reviewed IDs / window events / IDs without window coordinates.\n"
        + "Ticks: reviewed starts; outlines: documented windows. No independent-scene count.",
        fontsize=7.2,
    )
    return figure
