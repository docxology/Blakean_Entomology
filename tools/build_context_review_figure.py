#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["click>=8.1", "matplotlib>=3.7", "pydantic==2.11.9"]
# ///
# ─── How to run ───
# 1. Install uv: https://docs.astral.sh/uv/
# 2. In the admitted Entomology project and locked external environment:
#    uv run python tools/build_context_review_figure.py --help
# 3. Supply a trusted run SHA, authored decisions and a fresh private output.
# ──────────────────
"""Plot selected contextual decisions while retaining original source roles."""

import csv
import io
from pathlib import Path
from typing import Literal, Protocol, TypedDict

import click
import matplotlib
from blake.methods.models import Digest, FileReceipt, FrozenModel, ResearchError
from blake.methods.runs import digest, read_regular, reserve, write_new
from blake.methods.storage import publish_bytes
from matplotlib.axis import Tick
from matplotlib.container import BarContainer
from matplotlib.figure import Figure
from matplotlib.image import AxesImage
from matplotlib.legend import Legend
from matplotlib.text import Text

from blakean_entomology.models import Decision
from blakean_entomology.review_contexts import ContextAudit, summarize_contexts
from blakean_entomology.workflows import require_private_output

matplotlib.use("Agg")


class ContextFigureReceipt(FrozenModel):
    """Close the exact audit, drawing code and all raster/vector/tabular outputs."""

    run_sha256: Digest
    decisions_sha256: Digest
    audit_generator_sha256: Digest
    figure_generator_sha256: Digest
    files: tuple[FileReceipt, ...]
    scope: str = (
        "Purposively selected category-span decisions; no sample prevalence or species inference"
    )


class PlotAxes(Protocol):
    """Finite interface for the actual drawing operations, including every kwarg."""

    def imshow(
        self, X: list[list[int]], *, cmap: str, vmin: int, aspect: Literal["auto"]
    ) -> AxesImage: ...
    def set_yticks(self, ticks: range, labels: tuple[str, ...] | list[str]) -> list[Tick]: ...
    def set_xticks(self, ticks: range, labels: list[str]) -> list[Tick]: ...
    def tick_params(self, *, axis: Literal["both"], labelsize: int) -> None: ...
    def text(
        self,
        x: float,
        y: float,
        s: str,
        *,
        ha: Literal["center"] = ...,
        va: Literal["center"] = ...,
        fontsize: int,
        color: str = ...,
    ) -> Text: ...
    def set_title(
        self, label: str, *, loc: Literal["left"], fontsize: int, fontweight: str
    ) -> Text: ...
    def barh(
        self,
        y: range,
        width: list[int],
        *,
        color: str,
        label: str,
        left: list[int] | None = ...,
        edgecolor: str = ...,
        hatch: str = ...,
    ) -> BarContainer: ...
    def set_xlabel(self, xlabel: str, *, fontsize: int) -> Text: ...
    def set_xlim(self, left: float, right: float) -> tuple[float, float]: ...
    def legend(
        self,
        *,
        loc: Literal["upper left"],
        bbox_to_anchor: tuple[float, float],
        fontsize: int,
        frameon: bool,
    ) -> Legend: ...


class PlotFigure(Protocol):
    """Structural library boundary; real render tests exercise the implementation."""

    def add_axes(self, rect: tuple[float, float, float, float]) -> PlotAxes: ...
    def suptitle(self, t: str, *, fontsize: int, fontweight: str) -> Text: ...
    def supxlabel(self, t: str, *, fontsize: int) -> Text: ...
    def savefig(
        self, fname: io.BytesIO, *, format: str, dpi: int, metadata: dict[str, str | None] | None
    ) -> None: ...


def new_figure() -> PlotFigure:
    """Check structural compatibility without an unchecked cast."""
    matplotlib.rcParams["svg.hashsalt"] = "blake-context-review-v1"
    return Figure(figsize=(7.1, 6.5))


class FormatMetadata(TypedDict):
    """Require metadata policy for every admitted publication format."""

    png: None
    svg: dict[str, str | None]
    pdf: dict[str, str | None]


def image_bytes(figure: PlotFigure, kind: Literal["png", "svg", "pdf"]) -> bytes:
    """Serialize this one diagram in the three declared publication formats."""
    buffer = io.BytesIO()
    metadata: FormatMetadata = {
        "png": None,
        "svg": {"Date": None},
        "pdf": {"CreationDate": None, "ModDate": None},
    }
    figure.savefig(buffer, format=kind, dpi=240, metadata=metadata[kind])
    return buffer.getvalue()


def plot_contexts(audit: ContextAudit) -> PlotFigure:
    """Draw explicit zero cells and a separate immutable source-cohort comparison."""
    terms = tuple(dict.fromkeys(cell.term_id for cell in audit.cells))
    values = {(cell.term_id, cell.decision): cell.candidates for cell in audit.cells}
    matrix = [[values[term, decision] for decision in Decision] for term in terms]
    figure = new_figure()
    axis = figure.add_axes((0.09, 0.23, 0.49, 0.62))
    cohorts = figure.add_axes((0.76, 0.23, 0.20, 0.62))
    _ = axis.imshow(matrix, cmap="Greys", vmin=0, aspect="auto")
    _ = axis.set_yticks(range(len(terms)), terms)
    _ = axis.set_xticks(
        range(6),
        [
            "Animal\nliteral",
            "Animal\nfigurative",
            "Associated",
            "Non-\nanimal",
            "Editorial",
            "Uncertain",
        ],
    )
    _ = axis.tick_params(axis="both", labelsize=8)
    maximum = max(max(row) for row in matrix)
    for row, cells in enumerate(matrix):
        for column, count in enumerate(cells):
            _ = axis.text(
                column,
                row,
                str(count),
                ha="center",
                va="center",
                fontsize=9,
                color="white" if count > maximum / 2 else "#202020",
            )
    _ = axis.set_title("A  Assigned dispositions", loc="left", fontsize=11, fontweight="bold")
    labels = [f"{c.role}\n{c.plane}" for c in audit.cohorts]
    animal = [c.animal_candidates for c in audit.cohorts]
    other = [c.candidates - c.animal_candidates for c in audit.cohorts]
    _ = cohorts.barh(range(len(labels)), animal, color="#8f3236", label="Animal-coded")
    _ = cohorts.barh(
        range(len(labels)),
        other,
        left=animal,
        color="#dedede",
        edgecolor="#555555",
        hatch="...",
        label="Other disposition",
    )
    _ = cohorts.set_yticks(range(len(labels)), labels)
    _ = cohorts.tick_params(axis="both", labelsize=8)
    _ = cohorts.set_xlabel("Selected candidate IDs", fontsize=9)
    _ = cohorts.set_xlim(0, max(c.candidates for c in audit.cohorts) * 1.22)
    for position, cohort in enumerate(audit.cohorts):
        _ = cohorts.text(
            cohort.candidates + 0.6, position, f"n={cohort.candidates}", va="center", fontsize=8
        )
    _ = cohorts.set_title("B  Source roles", loc="left", fontsize=11, fontweight="bold")
    _ = cohorts.legend(loc="upper left", bbox_to_anchor=(-0.16, -0.15), fontsize=8, frameon=False)
    _ = figure.suptitle(
        f"Contextual review | {audit.summary.reviewed_hits} selected decisions",
        fontsize=13,
        fontweight="bold",
    )
    _ = figure.supxlabel(
        "Zero cells mean no assigned decision of that kind, not zero retrieved candidates.\n"
        + "Animal-coded = literal + figurative; source roles never change. "
        + "Selection is purposive, not representative.",
        fontsize=8,
    )
    return figure


def generate(audit: ContextAudit, output: Path) -> ContextFigureReceipt:
    """Publish an unused epoch and write its completion marker after all payloads."""
    require_private_output(output, Path(__file__))
    figure = plot_contexts(audit)
    payloads = {"context-review.json": (audit.model_dump_json(indent=2) + "\n").encode()}
    formats: tuple[Literal["png", "svg", "pdf"], ...] = ("png", "svg", "pdf")
    for kind in formats:
        payloads["context-review." + kind] = image_bytes(figure, kind)
    for name, rows, fields in (
        ("context-review-cells.csv", audit.cells, ("term_id", "decision", "candidates")),
        (
            "context-review-cohorts.csv",
            audit.cohorts,
            ("role", "plane", "candidates", "animal_candidates"),
        ),
    ):
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(row.model_dump() for row in rows)
        payloads[name] = stream.getvalue().encode()
    reserve(output)
    members = tuple(publish_bytes(output / name, raw) for name, raw in payloads.items())
    receipt = ContextFigureReceipt(
        run_sha256=audit.run_sha256,
        decisions_sha256=audit.decisions_sha256,
        audit_generator_sha256=audit.generator_sha256,
        figure_generator_sha256=digest(read_regular(Path(__file__))),
        files=members,
    )
    _ = write_new(output / "figures.json", (receipt.model_dump_json(indent=2) + "\n").encode())
    return receipt


@click.command()
@click.option("--run", "directory", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--run-sha256", required=True)
@click.option("--decisions", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--output", type=click.Path(path_type=Path), required=True)
def main(directory: Path, run_sha256: str, decisions: Path, output: Path) -> None:
    """Keep the four explicit Click flags rather than hide the pinned CLI boundary."""
    try:
        require_private_output(output, directory)
        require_private_output(output, decisions)
        audit = summarize_contexts(directory, decisions, run_sha256)
        receipt = generate(audit, output)
    except ResearchError as error:
        raise click.ClickException(str(error)) from error
    click.echo(receipt.model_dump_json())


if __name__ == "__main__":
    main()
