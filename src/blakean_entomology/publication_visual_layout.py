"""Complete-image and measured quotation layout for the three visual arguments."""

from dataclasses import dataclass
from pathlib import Path

from PIL import Image

from .publication_canvas import INK, OCHRE, TEAL, Box, Sheet
from .publication_transport_models import PublicationError
from .visual_models import IllustratedEvidence, VisualWitness


@dataclass(frozen=True, slots=True)
class ImageFrame:
    x: int
    y: int
    width: int
    height: int


def whole_image(canvas: Sheet, source: Path, frame: ImageFrame) -> None:
    """Fit the complete source with its proportions and margins intact."""
    with Image.open(source) as original, original.convert("RGB") as image:
        image.thumbnail((frame.width, frame.height), Image.Resampling.LANCZOS)
        x = frame.x + (frame.width - image.width) // 2
        y = frame.y + (frame.height - image.height) // 2
        canvas.image.paste(image, (x, y))
        canvas.draw.rectangle(
            (x - 2, y - 2, x + image.width + 2, y + image.height + 2),
            outline=OCHRE,
            width=2,
        )


def witness_panel(canvas: Sheet, evidence: IllustratedEvidence, witness: VisualWitness) -> None:
    """Keep an inspected whole impression next to its exact textual locator."""
    whole_image(canvas, evidence.image(witness), ImageFrame(90, 340, 930, 1360))
    bottom = canvas.text(Box(100, 1740, 900), witness.locator, 30)
    bottom = canvas.text(Box(100, bottom + 30, 900), witness.credit, 27)
    if bottom > 2020:
        raise PublicationError("visual_credit_height", witness.key)


def quotation(canvas: Sheet, witness: VisualWitness) -> int:
    """Use the pinned serif italic face for a source-preserving verse excerpt."""
    font = canvas.font_path.with_name("LiberationSerif-Italic.ttf")
    if not font.is_file() or font.is_symlink():
        raise PublicationError("visual_quote_font", str(font))
    italic = Sheet(canvas.image, canvas.draw, font)
    canvas.draw.line((1110, 340, 1110, 810), fill=OCHRE, width=5)
    bottom = italic.text(Box(1150, 350, 900), witness.quotation, 47)
    if bottom > 825:
        raise PublicationError("visual_quotation_height", witness.key)
    return bottom


def argument(canvas: Sheet, witness: VisualWitness) -> None:
    """Separate the proposed reading, its live rival and its biological ceiling."""
    for y, label, body, color in (
        (870, "READ THE RELATION", witness.reading, TEAL),
        (1210, "KEEP THE COUNTERREADING", witness.alternative, OCHRE),
        (1550, "CLASSIFY CONDITIONALLY", witness.classification_limit, INK),
    ):
        canvas.draw.line((1120, y, 2090, y), fill=color, width=4)
        bottom = canvas.text(Box(1130, y + 25, 930), label, 31)
        bottom = canvas.text(Box(1130, bottom + 20, 930), body, 36)
        if bottom > y + 310:
            raise PublicationError("visual_argument_height", witness.key)
