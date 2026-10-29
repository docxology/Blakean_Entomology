# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
# Run with existing project dependencies (no sync):
# uv run --no-sync python tools/build_composition_figures.py --help
"""Four grayscale figures with typed, pinned inputs and complete producer sidecars.

Size policy (# noqa: SIZE_OK): user-owned standalone renderer binds all four products
and typed plotting port.
"""

from __future__ import annotations

import csv
import io
from math import log1p
from pathlib import Path
from typing import Final, Literal, Protocol

import click
import matplotlib
from blake.methods.models import Artifact, Digest, EvidenceError, FileReceipt, FrozenModel
from blake.methods.profiles import RuntimeProfile
from blake.methods.proximity import ProximityStudy
from blake.methods.runs import (
    digest,
    read_regular,
    reserve,
    verify_artifacts,
    write_new,
)
from blake.methods.storage import publish_bytes
from matplotlib.axis import Tick
from matplotlib.container import BarContainer
from matplotlib.figure import Figure
from matplotlib.image import AxesImage
from matplotlib.lines import Line2D
from matplotlib.text import Text
from pydantic import TypeAdapter

from blakean_entomology.composition import CHANNELS, LITERAL_PAIRS, WIDTHS, CompositionAudit
from blakean_entomology.composition_workflow import (
    EXPORTS,
    CategoryChannelRow,
    ChannelRow,
    CompositionRun,
    InputBinding,
    MatrixRow,
    PairRow,
    PairWorkRow,
    SourceOrigin,
    encode,
    fingerprint,
    source_origin,
    verify_destination,
)


class PlotAxes(Protocol):
    """Finite typed contract for the documented Matplotlib operations used here.

    Matplotlib's generic **kwargs stubs are unknown. This interface names every
    accepted argument; real render tests exercise each operation and its outputs.
    """

    def imshow(self, X: list[list[float]], *, cmap: str, aspect: Literal["auto"]) -> AxesImage: ...
    def set_yticks(
        self, ticks: list[int], *, labels: tuple[str, ...] | list[str]
    ) -> list[Tick]: ...
    def set_xticks(
        self, ticks: list[int], *, labels: tuple[str, ...], rotation: int
    ) -> list[Tick]: ...
    def text(
        self,
        x: float,
        y: float,
        s: str,
        *,
        ha: Literal["center"],
        va: Literal["center"],
        fontsize: float,
        color: str,
    ) -> Text: ...
    def barh(self, y: list[int], width: list[float], *, color: str) -> BarContainer: ...
    def set_xlabel(self, xlabel: str) -> Text: ...
    def invert_yaxis(self) -> None: ...
    def axvline(self, x: float, *, color: str, linewidth: float) -> Line2D: ...


class PlotFigure(Protocol):
    """The rendering boundary has explicit format, metadata and layout parameters."""

    def add_axes(self, rect: tuple[float, float, float, float]) -> PlotAxes: ...
    def text(self, x: float, y: float, s: str) -> Text: ...
    def suptitle(self, t: str, *, fontsize: float) -> Text: ...
    def savefig(
        self, fname: io.BytesIO, *, format: str, dpi: int, metadata: dict[str, str | None] = ...
    ) -> None: ...
    def clear(self) -> None: ...


def new_figure(size: tuple[float, float]) -> PlotFigure:
    """Check structural compatibility with the real library, without casting."""
    return Figure(figsize=size)


STEMS: Final = (
    "01-name-family-matrix",
    "02-composition-influence",
    "03-literal-pair-source-dependence",
    "04-query-channel-source-audit",
)


class FigureSidecar(FrozenModel):
    question: str
    caption: str
    analytical_run_sha256: Digest
    atlas_sha256: Digest
    data: tuple[Artifact, ...]
    producer: SourceOrigin
    plotting_source: tuple[InputBinding, ...]
    profile: RuntimeProfile
    denominator: str
    limits: str
    files: tuple[FileReceipt, ...]


class FiguresManifest(FrozenModel):
    analytical_run_sha256: Digest
    files: tuple[FileReceipt, ...]
    producer: SourceOrigin
    plotting_source: tuple[InputBinding, ...]
    matplotlib: str
    visual_review: str = (
        "Producer render only; root retains native manuscript QA and independent review."
    )


class PlotData(FrozenModel):
    composition: CompositionAudit
    matrix: tuple[MatrixRow, ...]
    pairs: tuple[PairRow, ...]
    pairworks: tuple[PairWorkRow, ...]
    channels: tuple[ChannelRow, ...]
    category_channels: tuple[CategoryChannelRow, ...]


def csv_records(raw: bytes) -> list[dict[str, str]]:
    """Parse CSV through an explicit string boundary, rejecting malformed row widths."""
    rows: list[dict[str, str]] = []
    for row in csv.DictReader(io.StringIO(raw.decode())):
        if any(k is None or not isinstance(v, str) for k, v in row.items()):
            raise EvidenceError("composition_csv", "Malformed row")
        rows.append({str(k): str(v) for k, v in row.items()})
    return rows


def load_data(packet: Path, run: CompositionRun) -> PlotData:
    """Validate every artifact hash and complete matrix/pair membership before output."""
    raw = verify_artifacts(packet, run.files, EXPORTS)
    # Empty CSV fields encode undefined denominators; preserve them as None.
    matrix_rows = csv_records(raw["name-work-matrix.csv"])
    matrix = tuple(
        MatrixRow.model_validate({k: (None if v == "" else v) for k, v in r.items()})
        for r in matrix_rows
    )
    data = PlotData(
        composition=CompositionAudit.model_validate_json(raw["composition.json"]),
        matrix=matrix,
        pairs=TypeAdapter(tuple[PairRow, ...]).validate_python(
            csv_records(raw["literal-pairs.csv"])
        ),
        pairworks=TypeAdapter(tuple[PairWorkRow, ...]).validate_python(
            csv_records(raw["literal-pair-work.csv"])
        ),
        category_channels=TypeAdapter(tuple[CategoryChannelRow, ...]).validate_python(
            csv_records(raw["category-source-channels.csv"])
        ),
        channels=TypeAdapter(tuple[ChannelRow, ...]).validate_python(
            csv_records(raw["source-channels.csv"])
        ),
    )
    a = data.composition
    groups = tuple(o.omitted_work_id for o in a.omissions)
    keys = {(r.work_id, r.category) for r in matrix}
    pairkeys = {(r.pair, r.window_words) for r in data.pairs}
    if (
        len(keys) != len(matrix)
        or keys != {(w, c) for w in groups for c in a.category_ids}
        or len(matrix) != a.work_groups * len(a.category_ids)
        or sum(r.candidates for r in matrix) != a.name_category_candidates
        or a.source_units != run.source_census.primary_units
        or a.tokens != run.source_census.nfkc_tokens
        or len(pairkeys) != len(data.pairs)
        or not data.channels
        or len({(r.pair, r.window_words, r.work_id) for r in data.pairworks}) != len(data.pairworks)
        or any(r.eligible_units <= 0 for r in data.pairworks)
    ):
        raise EvidenceError(
            "composition_plot_inventory", "Complete reconciled plot inventory required"
        )
    expected_pairs = {
        ("+".join(pair), width if width is not None else "whole_unit")
        for pair in LITERAL_PAIRS
        for width in WIDTHS
    }
    workkeys = {(r.pair, r.window_words, r.work_id) for r in data.pairworks}
    cohorts = {(r.role, r.plane, r.author_id) for r in data.channels}
    channelkeys = {(r.role, r.plane, r.author_id, r.channel) for r in data.channels}
    categorykeys = {(r.role, r.plane, r.author_id, r.category) for r in data.category_channels}
    study = ProximityStudy.model_validate_json(raw["literal-relationships.json"])
    expected_rows = tuple(
        PairRow(
            pair="+".join(r.request.terms),
            window_words=r.request.window_words
            if r.request.window_words is not None
            else "whole_unit",
            matched_units=r.matched_source_units,
            eligible_units=r.eligible_source_units,
            matched_work_groups=r.matched_source_families,
            eligible_work_groups=r.eligible_source_families,
            literal_tokens=r.eligible_word_tokens,
        )
        for r in study.rows
    )
    expected_workrows = tuple(
        PairWorkRow(
            pair="+".join(r.request.terms),
            window_words=r.request.window_words
            if r.request.window_words is not None
            else "whole_unit",
            work_id=f.work_id,
            matched_units=f.matched_units,
            eligible_units=f.source_units,
            literal_tokens=f.word_tokens,
        )
        for r in study.rows
        for f in r.facets
    )
    if (
        pairkeys != expected_pairs
        or workkeys != {(p, w, g) for p, w in expected_pairs for g in groups}
        or data.pairs != expected_rows
        or data.pairworks != expected_workrows
        or any(
            r.eligible_units != a.source_units
            or r.literal_tokens != run.source_census.literal_tokens
            for r in data.pairs
        )
        or channelkeys != {(*c, ch) for c in cohorts for ch in set(CHANNELS.values())}
        or len(channelkeys) != len(data.channels)
        or len(categorykeys) != len(data.category_channels)
        or len(data.category_channels) != len(cohorts) * run.source_census.categories
        or sum(r.category_candidates for r in data.channels)
        != run.source_census.all_category_candidates
    ):
        raise EvidenceError("composition_plot_tables", "Incomplete pair/channel tables")
    for omission in a.omissions:
        rows = tuple(r for r in matrix if r.work_id == omission.omitted_work_id)
        if any(
            (r.eligible_source_units, r.nfkc_tokens)
            != (omission.omitted_source_units, omission.omitted_tokens)
            or r.matched_units > min(r.candidates, r.eligible_source_units)
            or r.candidates < 0
            or r.rate_per_10000_tokens
            != (10000 * r.candidates / r.nfkc_tokens if r.nfkc_tokens else None)
            or r.within_work_name_category_share
            != (
                r.candidates / omission.removed_name_candidates
                if omission.removed_name_candidates
                else None
            )
            for r in rows
        ):
            raise EvidenceError("composition_plot_matrix", "Matrix counts/denominators differ")
    for category in a.categories:
        rows = tuple(r for r in matrix if r.category == category.category)
        if (sum(r.candidates for r in rows), sum(r.matched_units for r in rows)) != (
            category.candidates,
            category.matched_units,
        ):
            raise EvidenceError("composition_plot_matrix", "Category counts differ")
    for channel in data.channels:
        members = tuple(
            r
            for r in data.category_channels
            if (r.role, r.plane, r.author_id, r.channel)
            == (channel.role, channel.plane, channel.author_id, channel.channel)
        )
        if (
            len(members),
            sum(r.candidates for r in members),
            sum(r.exact_text_candidates for r in members),
            sum(r.candidates > 0 for r in members),
        ) != (
            channel.categories,
            channel.category_candidates,
            channel.exact_text_category_candidates,
            channel.observed_categories,
        ):
            raise EvidenceError("composition_plot_channels", "Channel counts differ")
    return data


def axes(fig: PlotFigure, bounds: tuple[float, float, float, float]) -> PlotAxes:
    """Create one explicitly typed axes, avoiding untyped pyplot subplot unions."""
    return fig.add_axes(bounds)


def heatmap(
    ax: PlotAxes,
    values: list[list[float]],
    rows: SequenceLabels,
    columns: SequenceLabels,
    shades: list[list[float]] | None = None,
) -> None:
    """Print every zero alongside grayscale shading; labels retain source denominators."""
    shade_values = shades if shades is not None else values
    _ = ax.imshow(shade_values, cmap="Greys", aspect="auto")
    _ = ax.set_yticks(list(range(len(rows))), labels=rows)
    _ = ax.set_xticks(list(range(len(columns))), labels=columns, rotation=90)
    for i, row in enumerate(values):
        for j, value in enumerate(row):
            _ = ax.text(
                j,
                i,
                f"{value:.0f}",
                ha="center",
                va="center",
                fontsize=7,
                color="white"
                if shade_values[i][j] > max(max(r) for r in shade_values) * 0.6
                else "black",
            )


SequenceLabels = tuple[str, ...]


def render(packet: Path, expected_run_sha: str, output: Path, output_root: Path) -> None:
    """Publish PNG/SVG/PDF plus sidecars exclusively; completion marker is always last."""
    verify_destination(output, output_root, (packet,))
    run_raw = read_regular(packet / "run.json")
    if digest(run_raw) != expected_run_sha:
        raise EvidenceError("composition_run_pin", "analytical run SHA mismatch")
    run = CompositionRun.model_validate_json(run_raw)
    data = load_data(packet, run)
    origin = source_origin()
    plotting = fingerprint((Path(__file__),))
    matplotlib.rcParams["font.family"] = "serif"
    matplotlib.rcParams["svg.fonttype"] = "none"
    matplotlib.rcParams["pdf.fonttype"] = 42
    matplotlib.rcParams["svg.hashsalt"] = plotting[0].sha256
    artifacts: list[FileReceipt] = []
    reserve(output)

    def save(
        fig: PlotFigure, index: int, caption: str, profile: RuntimeProfile, denominator: str
    ) -> None:
        """Publish three formats and bind their exact bytes and analytical inputs."""
        files: list[FileReceipt] = []
        for extension in ("png", "svg", "pdf"):
            buffer = io.BytesIO()
            # Explicit metadata avoids wall-clock timestamps in vector formats.
            if extension == "pdf":
                fig.savefig(
                    buffer,
                    format=extension,
                    dpi=160,
                    metadata={"CreationDate": None, "ModDate": None},
                )
            elif extension == "svg":
                fig.savefig(buffer, format=extension, dpi=160, metadata={"Date": None})
            else:
                fig.savefig(buffer, format=extension, dpi=160)
            files.append(publish_bytes(output / f"{STEMS[index]}.{extension}", buffer.getvalue()))
        sidecar = FigureSidecar(
            question=caption,
            caption=caption,
            analytical_run_sha256=expected_run_sha,
            atlas_sha256=run.atlas_sha256,
            data=run.files,
            producer=origin,
            plotting_source=plotting,
            profile=profile,
            denominator=denominator,
            limits=data.composition.limits,
            files=tuple(files),
        )
        artifacts.extend(files)
        artifacts.append(publish_bytes(output / f"{STEMS[index]}.json", encode(sidecar)))
        fig.clear()

    a = data.composition
    groups = tuple(o.omitted_work_id for o in a.omissions)
    cells = {(r.work_id, r.category): r for r in data.matrix}
    headers = tuple(
        f"{w} n={cells[w, a.category_ids[0]].eligible_source_units}; "
        + f"T={cells[w, a.category_ids[0]].nfkc_tokens:,}"
        for w in groups
    )
    fig = new_figure((18, 20))
    ax = axes(fig, (0.12, 0.23, 0.86, 0.70))
    values = [[float(cells[w, c].matched_units) for w in groups] for c in a.category_ids]
    heatmap(
        ax,
        values,
        a.category_ids,
        headers,
        [[log1p(cells[w, c].rate_per_10000_tokens or 0) for w in groups] for c in a.category_ids],
    )
    _ = fig.suptitle("Name-family coverage: all categories and source groups", fontsize=17)
    _ = fig.text(
        0.1,
        0.02,
        "Cell = matched units / column n; shade = log(1 + candidates / 10,000 NFKC tokens).\n"
        + "T = NFKC tokens; category counts and rates remain in the CSV. Copies/overlaps retained.",
    )
    save(
        fig,
        0,
        "Complete name-family coverage by recorded source group",
        run.nfkc_profile,
        f"{a.source_units} units; {a.tokens} NFKC tokens; column n/T retained",
    )

    fig = new_figure((13, 8))
    left = axes(fig, (0.15, 0.22, 0.32, 0.65))
    right = axes(fig, (0.66, 0.22, 0.30, 0.65))
    contrasts = sorted(
        a.categories, key=lambda r: abs(r.difference_percentage_points or 0), reverse=True
    )[:16]
    shifts = [r.difference_percentage_points or 0 for r in contrasts]
    _ = left.barh(list(range(len(shifts))), shifts, color=".6")
    _ = left.set_yticks(
        list(range(len(shifts))), labels=[f"{r.category} ({r.candidates})" for r in contrasts]
    )
    left.invert_yaxis()
    _ = left.set_xlabel("Equal nonempty-group minus pooled\npercentage points")
    omitted = sorted(a.omissions, key=lambda r: r.composition_tv_from_full or 0, reverse=True)[:12]
    _ = right.barh(
        list(range(len(omitted))), [r.composition_tv_from_full or 0 for r in omitted], color=".6"
    )
    _ = right.set_yticks(list(range(len(omitted))), labels=[r.omitted_work_id for r in omitted])
    right.invert_yaxis()
    _ = right.set_xlabel("Omission total variation")
    _ = fig.suptitle("Composition shifts and whole-group omission influence", fontsize=17)
    _ = fig.text(
        0.08,
        0.06,
        f"{a.name_category_candidates} category candidates; "
        + f"{a.nonempty_name_work_groups}/{a.work_groups} nonempty groups; "
        + f"TV={a.pooled_vs_equal_nonempty_tv}.\n"
        + "Zero-mass profiles excluded from mean. Finite inventory; no independence inference.",
    )
    save(
        fig,
        1,
        "Pooled and equal nonempty-group composition, and group omission effects",
        run.nfkc_profile,
        f"{a.name_category_candidates} category candidates; "
        + f"{a.nonempty_name_work_groups} nonempty groups",
    )

    fig = new_figure((19, 9))
    left = axes(fig, (0.12, 0.31, 0.18, 0.57))
    right = axes(fig, (0.43, 0.31, 0.55, 0.57))
    pairs = tuple(dict.fromkeys(r.pair for r in data.pairs))
    widths = (8, 32, 64, "whole_unit")
    lookup = {(r.pair, r.window_words): r for r in data.pairs}
    heatmap(
        left,
        [[float(lookup[p, w].matched_units) for w in widths] for p in pairs],
        pairs,
        tuple(str(w) for w in widths),
    )
    local = {(r.pair, r.work_id): r for r in data.pairworks if r.window_words == 32}
    literalheaders = tuple(
        f"{w} n={local[pairs[0], w].eligible_units}; T={local[pairs[0], w].literal_tokens:,}"
        for w in groups
    )
    heatmap(
        right,
        [[float(local[p, w].matched_units) for w in groups] for p in pairs],
        pairs,
        literalheaders,
        [[local[p, w].matched_units / local[p, w].eligible_units for w in groups] for p in pairs],
    )
    _ = left.axvline(2.5, color="black", linewidth=2)
    _ = fig.suptitle("Literal pair locality and 32-word source dependence", fontsize=17)
    _ = fig.text(
        0.08,
        0.03,
        f"{run.source_census.primary_units} primary units; "
        + f"{run.source_census.literal_tokens:,} original-text tokens. "
        + "Singular literals; all zero groups retained.\n"
        + "Cell = matched units; right shade = within-group fraction. Whole-unit separated. "
        + "Copies may repeat one scene; no animal-sense decisions.",
    )
    save(
        fig,
        2,
        "Twelve declared literal pairs: word envelopes and contributing groups",
        run.literal_profile,
        f"{run.source_census.primary_units} units; "
        + f"{run.source_census.literal_tokens} original-text word tokens",
    )

    fig = new_figure((13, 6))
    ax = axes(fig, (0.27, 0.23, 0.70, 0.62))
    cohorts = tuple(dict.fromkeys((r.role, r.plane, r.author_id) for r in data.channels))
    channels = ("name_family", "broad_label", "associated", "motion")
    look = {(r.role, r.plane, r.author_id, r.channel): r for r in data.channels}
    labels = tuple(
        f"{c[0]} / {c[1]}\nn={look[*c, channels[0]].source_units}; "
        + f"T={look[*c, channels[0]].nfkc_tokens:,}"
        for c in cohorts
    )
    heatmap(
        ax,
        [[float(look[*c, ch].category_candidates) for ch in channels] for c in cohorts],
        labels,
        channels,
        [
            [
                look[*c, ch].category_candidates
                / sum(look[*c, x].category_candidates for x in channels)
                if sum(look[*c, x].category_candidates for x in channels)
                else 0
                for ch in channels
            ]
            for c in cohorts
        ],
    )
    _ = fig.suptitle("Query-channel candidates across disjoint source cohorts", fontsize=16)
    _ = fig.text(
        0.05,
        0.03,
        "Cell = category-span candidates; shade = within-cohort mass share. Cohort n/T retained.\n"
        + "XML/editorial candidates do not establish Blake animal attestations; "
        + "cohorts are not completeness stages.",
    )
    save(
        fig,
        3,
        "Declared query-channel mass across captured source cohorts",
        run.nfkc_profile,
        f"{run.source_census.captured_units} units across disjoint role/plane/author cohorts",
    )
    _ = verify_artifacts(packet, run.files, EXPORTS)
    if (
        read_regular(packet / "run.json") != run_raw
        or source_origin() != origin
        or fingerprint((Path(__file__),)) != plotting
    ):
        raise EvidenceError("composition_plot_changed", "Data/producer changed while rendering")
    manifest = FiguresManifest(
        analytical_run_sha256=expected_run_sha,
        files=tuple(artifacts),
        producer=origin,
        plotting_source=plotting,
        matplotlib=matplotlib.__version__,
    )
    _ = write_new(output / "figures.json", encode(manifest))


@click.command()
@click.option("--packet", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--run-sha256", required=True)
@click.option("--output", type=click.Path(path_type=Path), required=True)
def main(packet: Path, run_sha256: str, output: Path) -> None:
    """Render a new private figure epoch from a pinned composition completion marker."""
    try:
        render(packet, run_sha256, output, Path.cwd() / "analysis_output")
    except (OSError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(f"4 PNG/SVG/PDF figures and sidecars. {output}")


if __name__ == "__main__":
    main()
