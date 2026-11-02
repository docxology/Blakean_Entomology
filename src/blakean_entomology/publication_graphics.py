"""Produce three source-bound illustrated abstracts with complete Blake impressions."""

from pathlib import Path

from .publication_canvas import sheet
from .publication_data import AbstractData
from .publication_illustrated import dream, fly, worm


def draw_abstracts(data: AbstractData, output: Path, font: Path) -> tuple[Path, ...]:
    """Keep the distinct image/quotation arguments at the same native figure targets."""
    paths: list[Path] = []
    for number, draw in enumerate((fly, dream, worm), start=1):
        canvas = sheet(font)
        with canvas.image:
            draw(canvas, data)
            target = output / f"graphical-abstract-{number}.png"
            canvas.image.save(target, dpi=(300, 300))
        paths.append(target)
    return tuple(paths)
