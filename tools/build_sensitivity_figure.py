# /// script
# requires-python = ">=3.11"
# dependencies = ["click>=8.1", "matplotlib>=3.10", "pydantic==2.11.9"]
# ///
# Run from the private project with an external interpreter:
# uv run --no-project --python <external-python> tools/build_sensitivity_figure.py --help
"""Plot validated aggregate receipts; no corpus text or interpretive coding is exported."""

import io
from collections import Counter
from pathlib import Path
from typing import Final

import click
from blake.methods.models import Digest, EvidenceError, FrozenModel, ResearchError
from blake.methods.profiles import RetrievalProfile, describe_profile
from blake.methods.runs import digest, read_regular, reserve, write_new
from blake.methods.statistics import analyze_inventory
from blake.methods.statistics_models import QuerySummary
from blake.methods.storage import publish_bytes
from pydantic import TypeAdapter

from blakean_entomology.sensitivity import default_proximity_grid
from blakean_entomology.workflows import (
    ProximityReceipt,
    SensitivityReceipt,
    require_private_output,
)

RATE: Final = TypeAdapter(float)
SELECTED: Final = ("worm", "fly", "spider", "polypus", "bee", "ant", "caterpillar", "butterfly")


class FigureSummary(FrozenModel):
    sensitivity_source: str
    sensitivity_sha256: Digest
    proximity_source: str
    proximity_sha256: Digest
    generator_sha256: Digest
    application_code_sha256: Digest
    bundle_manifest_sha256: Digest
    scanned_source_units: int
    primary_units: int
    work_groups: int
    nfkc_tokens: int
    exact_text_units: int
    exact_text_tokens: int
    literal_tokens: int
    query_categories: int
    selected: tuple[QuerySummary, ...]
    changed_by_exact_text: tuple[QuerySummary, ...]
    proximity: ProximityReceipt


def validate_inputs(sensitivity: SensitivityReceipt, proximity: ProximityReceipt) -> None:
    """Reconcile declared profiles, complete counted inventory and paired corpus identity."""
    stats, study = sensitivity.statistics, proximity.study
    expected_nfkc = describe_profile(RetrievalProfile.NFKC_TOKENS_V2)
    expected_literal = describe_profile(RetrievalProfile.LITERAL_CASEFOLD_V1)
    if (
        sensitivity.profile.semantics != expected_nfkc
        or proximity.profile.semantics != expected_literal
        or stats.profile != expected_nfkc.profile.value
        or stats.tokenization != expected_nfkc.tokens
        or stats.unicode_version != sensitivity.profile.unicode
        or sensitivity.profile.unicode != proximity.profile.unicode
        or sensitivity.profile.python != proximity.profile.python
    ):
        raise EvidenceError("figure_profile", "Require separate declared NFKC and literal profiles")
    pin, projected = sensitivity.corpus_pin, proximity.binding.projection_pin
    if (
        pin.bundle_manifest_sha256 != proximity.binding.bundle_manifest_sha256
        or pin.captured_manifest_sha256 != projected.captured_manifest_sha256
        or pin.projection_manifest_sha256 != projected.projection_manifest_sha256
        or pin.index_sha256 != projected.index_sha256
        or study.corpus_pin != projected
        or sensitivity.application_code_sha256 != proximity.application_code_sha256
    ):
        raise EvidenceError("figure_pin", "Receipts must bind the same corpus and producer epoch")
    if analyze_inventory(stats.units, stats.query_ids, sensitivity.profile) != stats:
        raise EvidenceError(
            "figure_inventory", "Recomputed complete inventory differs from receipt"
        )
    units_by_work = Counter(unit.work_id for unit in stats.units)
    if (
        study.grid != default_proximity_grid()
        or study.scanned_source_units < len(stats.units)
        or sum(unit.tokens for unit in stats.units) <= 0
        or any(
            row.eligible_source_units != len(stats.units)
            or row.eligible_source_families != len(units_by_work)
            or {facet.work_id: facet.source_units for facet in row.facets} != units_by_work
            or row.eligible_word_tokens <= 0
            for row in study.rows
        )
    ):
        raise EvidenceError(
            "figure_denominator", "Require matching work/unit strata and explicit grid"
        )
    if not set(SELECTED).issubset(stats.query_ids):
        raise EvidenceError("figure_categories", "Required private figure categories are absent")


def summarize(sensitivity_path: Path, proximity_path: Path) -> FigureSummary:
    """Parse and independently reconcile both receipts before selecting plotted aggregates."""
    sensitivity_raw = read_regular(sensitivity_path)
    proximity_raw = read_regular(proximity_path)
    sensitivity = SensitivityReceipt.model_validate_json(sensitivity_raw)
    proximity = ProximityReceipt.model_validate_json(proximity_raw)
    validate_inputs(sensitivity, proximity)
    stats = sensitivity.statistics
    by_query = {query.query_id: query for query in stats.queries}
    representative = stats.queries[0]
    return FigureSummary(
        sensitivity_source=str(sensitivity_path),
        sensitivity_sha256=digest(sensitivity_raw),
        proximity_source=str(proximity_path),
        proximity_sha256=digest(proximity_raw),
        generator_sha256=digest(Path(__file__).read_bytes()),
        application_code_sha256=sensitivity.application_code_sha256,
        bundle_manifest_sha256=sensitivity.corpus_pin.bundle_manifest_sha256,
        scanned_source_units=proximity.study.scanned_source_units,
        primary_units=len(stats.units),
        work_groups=len({unit.work_id for unit in stats.units}),
        nfkc_tokens=sum(unit.tokens for unit in stats.units),
        exact_text_units=representative.exact_text.source_units,
        exact_text_tokens=representative.exact_text.tokens,
        literal_tokens=proximity.study.rows[0].eligible_word_tokens,
        query_categories=len(stats.query_ids),
        selected=tuple(by_query[name] for name in SELECTED),
        changed_by_exact_text=tuple(
            query
            for query in stats.queries
            if query.copy_retaining.occurrences != query.exact_text.occurrences
        ),
        proximity=proximity,
    )


def plot(summary: FigureSummary) -> bytes:
    """Render private selection and labels; every numerical label comes from receipts."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    plt.rcParams.update({"font.size": 9, "axes.titlesize": 11, "axes.labelsize": 9})
    figure = plt.figure(figsize=(6.7, 9.0), layout="constrained")
    grid = figure.add_gridspec(3, 1, height_ratios=(1.15, 1.15, 0.9))
    rates = figure.add_subplot(grid[0, 0])
    concentration = figure.add_subplot(grid[1, 0])
    windows = figure.add_subplot(grid[2, 0])
    positions = np.arange(len(summary.selected))
    pooled = [
        RATE.validate_python(query.copy_retaining.rate_per_10000_tokens)
        for query in summary.selected
    ]
    balanced = [
        RATE.validate_python(query.work_balanced_rate_per_10000_tokens)
        for query in summary.selected
    ]
    _ = rates.barh(
        positions - 0.18, pooled, height=0.34, color="#16697a", label="Copy-retaining pooled"
    )
    _ = rates.barh(
        positions + 0.18, balanced, height=0.34, color="#d28b36", label="Equal work-group mean"
    )
    labels = [
        f"{query.query_id}  (n={query.copy_retaining.occurrences})" for query in summary.selected
    ]
    _ = rates.set_yticks(positions, labels)
    rates.invert_yaxis()
    _ = rates.set_title("A  Category rates depend on the weighting", loc="left", fontweight="bold")
    _ = rates.set_xlabel("Category-span candidates per 10,000 NFKC tokens")
    _ = rates.legend(loc="lower right", frameon=False, fontsize=9)
    shares = [100 * (query.maximum_work_occurrence_share or 0) for query in summary.selected]
    _ = concentration.barh(positions, shares, color="#74546c")
    _ = concentration.set_yticks(positions, [query.query_id for query in summary.selected])
    concentration.invert_yaxis()
    _ = concentration.set_xlim(0, 100)
    _ = concentration.set_title(
        "B  Largest work-group share of each category", loc="left", fontweight="bold"
    )
    _ = concentration.set_xlabel("Share of copy-retaining category counts (%)")
    for position, share in enumerate(shares):
        measured = summary.selected[position].maximum_work_occurrence_share is not None
        label = f"{share:.1f}%" if measured else "n/a"
        _ = concentration.text(share + 1, position, label, va="center", fontsize=10)
    requests = summary.proximity.study.grid.requests
    pairs = tuple(dict.fromkeys(request.terms for request in requests))
    widths = tuple(dict.fromkeys(request.window_words for request in requests))
    values = [
        [
            next(
                row.matched_source_units
                for row in summary.proximity.study.rows
                if row.request.terms == pair and row.request.window_words == width
            )
            for width in widths
        ]
        for pair in pairs
    ]
    _ = windows.imshow(values, cmap="Blues", aspect="auto", vmin=0)
    _ = windows.set_yticks(range(len(pairs)), [" + ".join(pair) for pair in pairs])
    _ = windows.set_xticks(
        range(len(widths)),
        [str(width) if width is not None else "Whole source unit" for width in widths],
    )
    windows.xaxis.tick_top()
    _ = windows.axvline(len(widths) - 1.5, color="#c47724", linewidth=4)
    for row, cells in enumerate(values):
        for column, value in enumerate(cells):
            _ = windows.text(
                column,
                row,
                str(value),
                ha="center",
                va="center",
                fontsize=14,
                color="white" if value > max(max(cells) for cells in values) / 2 else "#152536",
            )
    _ = windows.set_title(
        "C  Literal pairs: matched units by word-window width",
        loc="left",
        fontweight="bold",
        pad=22,
    )
    _ = figure.suptitle(
        f"Blakean Entomology | {summary.primary_units} primary units, "
        + f"{summary.work_groups} recorded work groups",
        fontsize=12,
        fontweight="bold",
    )
    _ = figure.supxlabel(
        f"NFKC: {summary.nfkc_tokens:,} tokens; exact-text: {summary.exact_text_units} units / "
        + f"{summary.exact_text_tokens:,} tokens.\n"
        + f"Literal: {summary.literal_tokens:,} tokens. Whole units have no finite word limit.\n"
        + "Copies and category overlap retained; no animal census or independent sample.",
        fontsize=8.5,
    )
    for axis in (rates, concentration):
        axis.spines[["top", "right"]].set_visible(False)
    buffer = io.BytesIO()
    figure.savefig(buffer, format="png", dpi=180, facecolor="white")
    plt.close(figure)
    return buffer.getvalue()


def build_figure(sensitivity: Path, proximity: Path, output: Path) -> FigureSummary:
    """Validate first, reserve exclusively, and publish the aggregate summary last."""
    require_private_output(output, sensitivity)
    require_private_output(output, proximity)
    summary = summarize(sensitivity, proximity)
    image = plot(summary)
    reserve(output)
    _ = publish_bytes(output / "sensitivity.png", image)
    _ = write_new(output / "summary.json", (summary.model_dump_json(indent=2) + "\n").encode())
    return summary


@click.command()
@click.option("--sensitivity", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--proximity", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--output", type=click.Path(path_type=Path), required=True)
def main(sensitivity: Path, proximity: Path, output: Path) -> None:
    """Build a private aggregate figure from a compatible pair of typed receipts."""
    try:
        _ = build_figure(sensitivity, proximity, output)
    except (OSError, ValueError, ResearchError) as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(str(output / "sensitivity.png"))


if __name__ == "__main__":
    main()
