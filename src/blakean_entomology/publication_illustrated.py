"""Three quotation-led graphical arguments with original Blake impressions."""

from .publication_abstract_details import offered_route, review_coverage, weighting_contrast
from .publication_canvas import Box, Sheet
from .publication_data import AbstractData
from .publication_transport_models import PublicationError
from .publication_visual_layout import argument, quotation, witness_panel
from .visual_models import WitnessKey


def _opening(canvas: Sheet, data: AbstractData, key: WitnessKey) -> None:
    if data.visuals is None:
        raise PublicationError("illustrated_source_required", key)
    witness = data.visuals.witness(key)
    _ = canvas.text(Box(90, 65, 2030), witness.title, 61)
    _ = canvas.text(
        Box(95, 175, 1990),
        "An image, an utterance, and an interpretation are different kinds of evidence.",
        35,
    )
    witness_panel(canvas, data.visuals, witness)
    _ = quotation(canvas, witness)
    argument(canvas, witness)


def fly(canvas: Sheet, data: AbstractData) -> None:
    """Read reciprocal likeness through the complete copy-Y impression."""
    _opening(canvas, data, "fly")
    review_coverage(canvas, data)


def dream(canvas: Sheet, data: AbstractData) -> None:
    """Distinguish capacities in the offered route from a rescue actually narrated."""
    _opening(canvas, data, "dream")
    offered_route(canvas)


def worm(canvas: Sheet, data: AbstractData) -> None:
    """Keep a literary comparison and finite weighting result distinct from a clade."""
    _opening(canvas, data, "thel")
    weighting_contrast(canvas, data)
