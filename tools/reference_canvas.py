"""Finite typed Matplotlib boundary for reference and source-atlas presentation."""

import io
from typing import Literal, Protocol, overload

from matplotlib.axis import Tick
from matplotlib.figure import Figure
from matplotlib.image import AxesImage
from matplotlib.lines import Line2D
from matplotlib.text import Text


class ReferenceAxes(Protocol):
    def plot(
        self,
        x: list[float],
        y: list[float],
        *,
        color: str,
        linewidth: float = ...,
        marker: str = ...,
        markersize: float = ...,
        linestyle: str = ...,
        alpha: float = ...,
    ) -> list[Line2D]: ...
    def text(
        self,
        x: float,
        y: float,
        s: str,
        *,
        fontsize: float,
        color: str = ...,
        va: Literal["center", "bottom"] = ...,
        ha: Literal["center", "left", "right"] = ...,
        weight: Literal["bold"] = ...,
        bbox: dict[str, str | float] | None = ...,
    ) -> Text: ...
    def imshow(
        self,
        X: list[list[float]],
        *,
        aspect: Literal["auto"],
        cmap: str,
        vmin: float,
        vmax: float = ...,
    ) -> AxesImage: ...
    def set_xticks(
        self,
        ticks: list[int],
        *,
        labels: list[str],
        fontsize: float,
        rotation: float = ...,
        ha: Literal["right"] = ...,
    ) -> list[Tick]: ...
    def set_yticks(self, ticks: list[int], *, labels: list[str], fontsize: float) -> list[Tick]: ...
    def set_xlim(self, left: float, right: float) -> tuple[float, float]: ...
    def set_ylim(self, bottom: float, top: float) -> tuple[float, float]: ...
    def set_title(self, label: str, *, loc: Literal["left"], fontsize: float) -> Text: ...
    def set_axis_off(self) -> None: ...


class ReferenceFigure(Protocol):
    @overload
    def add_subplot(self) -> ReferenceAxes: ...
    @overload
    def add_subplot(self, nrows: int, ncols: int, index: int) -> ReferenceAxes: ...
    def suptitle(self, t: str, *, fontsize: float, weight: Literal["bold"]) -> Text: ...
    def supxlabel(self, t: str, *, fontsize: float) -> Text: ...
    def savefig(
        self,
        fname: io.BytesIO,
        *,
        format: str,
        dpi: int,
        facecolor: str,
        metadata: dict[str, str] | None,
    ) -> None: ...


def reference_figure(size: tuple[float, float]) -> ReferenceFigure:
    """Check the real library structurally without Any, casts or ignored diagnostics."""
    return Figure(figsize=size, layout="constrained")
