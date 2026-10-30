"""Measured raster layout for the source-derived publication diagrams."""

from dataclasses import dataclass
from pathlib import Path
from typing import Final

from PIL import Image, ImageDraw, ImageFont

from .publication_wire import PublicationError

INK: Final = "#173239"
PAPER: Final = "#fffdf7"
TEAL: Final = "#327c83"
OCHRE: Final = "#ac792d"
RED: Final = "#a8413c"
PALE: Final = "#e8efec"


@dataclass(frozen=True, slots=True)
class Box:
    x: int
    y: int
    width: int


@dataclass(frozen=True, slots=True)
class Sheet:
    """Own an in-memory drawing surface; callers close its image after publication."""

    image: Image.Image
    draw: ImageDraw.ImageDraw
    font_path: Path

    def text(self, box: Box, text: str, size: int = 38) -> int:
        """Wrap by measured glyph width and refuse text outside the canvas."""
        font = ImageFont.truetype(str(self.font_path), size)
        y = box.y
        for paragraph in text.split("\n"):
            line = ""
            for word in paragraph.split():
                if font.getlength(word) > box.width:
                    raise PublicationError("diagram_word_width", word)
                proposed = (line + " " + word).strip()
                if font.getlength(proposed) > box.width:
                    self.draw.text((box.x, y), line, font=font, fill=INK)
                    y += round(size * 1.32)
                    line = word
                else:
                    line = proposed
            if y + size * 1.32 > self.image.height:
                raise PublicationError("diagram_height", text)
            self.draw.text((box.x, y), line, font=font, fill=INK)
            y += round(size * 1.32)
        return y

    def panel(self, box: tuple[int, int, int, int], accent: str = TEAL) -> None:
        """Draw a labelled-card frame with a redundant structural accent."""
        self.draw.rounded_rectangle(box, radius=24, fill=PALE, outline=accent, width=4)
        self.draw.rectangle((box[0], box[1] + 24, box[0] + 12, box[3] - 24), fill=accent)


def sheet(font_path: Path) -> Sheet:
    """A fixed print-scale canvas with typography supplied by pinned template sources."""
    image = Image.new("RGB", (2200, 2360), PAPER)
    return Sheet(image, ImageDraw.Draw(image), font_path)
