"""Three quotation-led graphical arguments with original Blake impressions."""

from .publication_canvas import OCHRE, TEAL, Box, Sheet
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
    _ = canvas.text(
        Box(100, 2070, 2000),
        f"The corpus preserves {data.atlas.candidates:,} category-source-span candidates; "
        + f"{data.context.summary.reviewed_hits} have authored decisions and "
        + f"{data.context.summary.unreviewed_hits:,} remain unreviewed.",
        36,
    )
    _ = canvas.text(
        Box(100, 2225, 2000),
        "A counted word is a lead to a scene. "
        + "Neither the analogy nor the image identifies a species.",
        30,
    )


def dream(canvas: Sheet, data: AbstractData) -> None:
    """Distinguish capacities in the offered route from a rescue actually narrated."""
    _opening(canvas, data, "dream")
    cells = (
        ("Emmet", "needs a way home"),
        ("glow-worm", "offers light"),
        ("beetle", "supplies an audible route"),
    )
    for index, (name, relation) in enumerate(cells):
        x = 100 + 700 * index
        canvas.draw.line((x, 2080, x + 620, 2080), fill=TEAL, width=6)
        _ = canvas.text(Box(x, 2105, 620), name, 40)
        _ = canvas.text(Box(x, 2170, 620), relation, 32)
    _ = canvas.text(
        Box(100, 2290, 2000),
        "The final imperative offers homecoming; it does not report the wanderer's arrival.",
        28,
    )


def worm(canvas: Sheet, data: AbstractData) -> None:
    """Keep a literary comparison and finite weighting result distinct from a clade."""
    _opening(canvas, data, "thel")
    tv = data.composition.pooled_vs_equal_nonempty_tv
    if tv is None:
        raise PublicationError("composition_undefined", "Require a finite name-family profile")
    canvas.draw.line((100, 2075, 2100, 2075), fill=OCHRE, width=5)
    _ = canvas.text(
        Box(100, 2100, 2000),
        f"{data.composition.name_category_candidates:,} primary name-family candidates / "
        + f"{data.composition.nonempty_name_work_groups} nonempty groups. "
        + f"Pooled versus equal-group composition: TV = {tv:.6f}.",
        35,
    )
    _ = canvas.text(
        Box(100, 2250, 2000),
        "Changing a weighting rule changes a lexical profile, "
        + "not the ancestry of the beings named.",
        30,
    )
