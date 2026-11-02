"""Typed, finite Matplotlib port for source-coordinate figures."""

from __future__ import annotations

import io
from contextlib import AbstractContextManager
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Protocol

import matplotlib
from blake.methods.runs import digest
from matplotlib import font_manager
from matplotlib.axis import Tick
from matplotlib.collections import PolyCollection
from matplotlib.container import BarContainer
from matplotlib.figure import Figure
from matplotlib.image import AxesImage
from matplotlib.lines import Line2D
from matplotlib.text import Text

if TYPE_CHECKING:
    from matplotlib.typing import RcKeyType

matplotlib.use("Agg")


class StylePort(Protocol):
    def rc_context(self, rc: dict[RcKeyType, str | int]) -> AbstractContextManager[None]: ...


class FontPort(Protocol):
    def findfont(self, prop: font_manager.FontProperties) -> str: ...


def _style_port() -> StylePort:
    return matplotlib


def _font_port() -> FontPort:
    return font_manager


def plot_theme() -> AbstractContextManager[None]:
    return _style_port().rc_context(
        {"font.family": "DejaVu Sans", "pdf.fonttype": 42, "svg.hashsalt": "entomology-geometry-v1"}
    )


def plotting_runtime() -> dict[str, object]:
    fonts: dict[str, dict[str, str]] = {}
    for weight in ("normal", "bold"):
        path = Path(_font_port().findfont(font_manager.FontProperties(weight=weight)))
        fonts[weight] = {"path": str(path), "sha256": digest(path.read_bytes())}
    return {
        "matplotlib": matplotlib.__version__,
        "backend": matplotlib.get_backend(),
        "fonts": fonts,
        "scope": "Observed plotting/font identities; no image census.",
    }


class PlotAxes(Protocol):
    def plot(
        self,
        x: list[float],
        y: list[float],
        *,
        color: str,
        linewidth: float = ...,
        marker: str = ...,
        markersize: float = ...,
    ) -> list[Line2D]: ...
    def broken_barh(
        self,
        xranges: list[tuple[float, float]],
        yrange: tuple[float, float],
        *,
        facecolors: str,
        edgecolors: str,
        linewidth: float,
    ) -> PolyCollection: ...
    def barh(
        self, y: list[int], width: list[float], *, color: str, edgecolor: str
    ) -> BarContainer: ...
    def imshow(
        self,
        X: list[list[float]],
        *,
        cmap: str,
        vmin: float,
        vmax: float,
        aspect: Literal["auto"],
    ) -> AxesImage: ...
    def set_yticks(self, ticks: list[int], *, labels: list[str], fontsize: float) -> list[Tick]: ...
    def set_xticks(
        self, ticks: list[float], *, labels: list[str], fontsize: float
    ) -> list[Tick]: ...
    def set_xlim(self, left: float, right: float) -> tuple[float, float]: ...
    def set_ylim(self, bottom: float, top: float) -> tuple[float, float]: ...
    def set_xlabel(self, xlabel: str, *, fontsize: float) -> Text: ...
    def set_title(self, label: str, *, loc: Literal["left"], fontsize: float) -> Text: ...
    def text(
        self,
        x: float,
        y: float,
        s: str,
        *,
        fontsize: float,
        color: str = ...,
        va: Literal["center"] = ...,
        ha: Literal["center", "left", "right"] = ...,
    ) -> Text: ...


class PlotFigure(Protocol):
    def add_axes(self, rect: tuple[float, float, float, float]) -> PlotAxes: ...
    def text(
        self,
        x: float,
        y: float,
        s: str,
        *,
        fontsize: float,
        weight: Literal["normal", "bold"] = ...,
    ) -> Text: ...
    def savefig(
        self,
        fname: io.BytesIO,
        *,
        format: str,
        dpi: int,
        metadata: dict[str, str | None],
    ) -> None: ...
    def clear(self) -> None: ...


def new_figure(size: tuple[float, float]) -> PlotFigure:
    """Structural typing is checked against the actual library, without casting."""
    return Figure(figsize=size)


def figure_bytes(figure: PlotFigure, kind: Literal["png", "svg", "pdf"]) -> bytes:
    """Use one in-memory figure for deterministic raster/vector derivatives."""
    metadata: dict[str, str | None] = {"Creator": "Blakean Entomology"}
    if kind == "pdf":
        metadata |= {"CreationDate": None, "ModDate": None}
    elif kind == "svg":
        metadata["Date"] = None
    else:
        metadata = {"Software": "Blakean Entomology"}
    with io.BytesIO() as stream:
        with plot_theme():
            figure.savefig(stream, format=kind, dpi=300, metadata=metadata)
        return stream.getvalue()
