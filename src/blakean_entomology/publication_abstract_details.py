"""Data-bound evidence summaries for the three illustrated arguments."""

from dataclasses import dataclass

from .publication_canvas import INK, OCHRE, PALE, TEAL, Box, Sheet
from .publication_data import AbstractData
from .publication_transport_models import PublicationError


@dataclass(frozen=True, slots=True)
class _WeightingMark:
    category: str
    pooled: float
    equal: float


def review_coverage(canvas: Sheet, data: AbstractData) -> None:
    """Show the complete candidate denominator without enlarging the reviewed share."""
    summary = data.context.summary
    canvas.draw.line((100, 1980, 2100, 1980), fill=TEAL, width=5)
    _ = canvas.text(Box(100, 2000, 2000), "FROM A RETRIEVED WORD TO A CONTEXTUAL DECISION", 31)
    columns = (
        ("CATEGORY / SOURCE / SPAN CANDIDATES", summary.candidate_hits),
        ("WITH AUTHORED REVIEW DECISIONS", summary.reviewed_hits),
        ("STILL UNREVIEWED", summary.unreviewed_hits),
    )
    for index, (label, count) in enumerate(columns):
        x = 100 + 700 * index
        _ = canvas.text(Box(x, 2060, 610), f"{count:,}", 62)
        _ = canvas.text(Box(x, 2150, 610), label, 26)
    total = summary.candidate_hits
    share = summary.reviewed_hits / total if total else None
    explanation = (
        f"Reviewed share: {100 * share:.2f}%. The bar uses the full candidate denominator; "
        + "a quotation or picture adds no adjudication."
        if share is not None
        else "No candidates in this selection: a reviewed fraction is undefined."
    )
    _ = canvas.text(Box(100, 2230, 2000), explanation, 29)
    canvas.draw.rectangle((100, 2320, 2100, 2335), fill=PALE, outline=INK, width=2)
    if share is not None and share > 0:
        canvas.draw.rectangle((100, 2320, 100 + 2000 * share, 2335), fill=TEAL)


def offered_route(canvas: Sheet) -> None:
    """Map the poem's offered capacities while leaving its unreported outcome open."""
    canvas.draw.line((100, 1980, 2100, 1980), fill=TEAL, width=5)
    _ = canvas.text(Box(100, 2000, 2000), "THREE NAMED BEINGS; DIFFERENT CAPACITIES", 31)
    roles = (
        ("Emmet", "heard in trouble", "Needs a route home"),
        ("glow-worm", "lights the ground", "Offers visual guidance"),
        ("beetle", "goes his round", "Offers an audible guide"),
    )
    for index, (name, action, capacity) in enumerate(roles):
        x = 100 + 700 * index
        canvas.panel((x, 2060, x + 600, 2235))
        _ = canvas.text(Box(x + 25, 2080, 550), name, 43)
        _ = canvas.text(Box(x + 25, 2145, 550), action, 29)
        _ = canvas.text(Box(x + 25, 2190, 550), capacity, 26)
    _ = canvas.text(
        Box(100, 2260, 2000),
        "The text offers coordinated assistance, not a reported arrival. Read the whole "
        + "compound glow-worm: its suffix does not place it in an earthworm lineage.",
        29,
    )


def weighting_contrast(canvas: Sheet, data: AbstractData) -> None:
    """Compare actual lexical shares under two weighting rules on one percentage axis."""
    audit = data.composition
    tv = audit.pooled_vs_equal_nonempty_tv
    if tv is None:
        raise PublicationError("composition_undefined", "Require a finite name-family profile")
    marks: list[_WeightingMark] = []
    for row in audit.categories:
        pooled, equal = row.pooled_share, row.equal_nonempty_group_share
        if pooled is None or equal is None:
            raise PublicationError("composition_undefined", row.category)
        marks.append(_WeightingMark(row.category, pooled, equal))
    rows = sorted(marks, key=lambda mark: abs(mark.pooled - mark.equal), reverse=True)[:3]
    if not rows:
        raise PublicationError("composition_undefined", "Require at least one category")
    canvas.draw.line((100, 1980, 2100, 1980), fill=OCHRE, width=5)
    _ = canvas.text(
        Box(100, 2000, 2000),
        f"{audit.name_category_candidates:,} PRIMARY NAME-FAMILY CANDIDATES / "
        + f"{audit.nonempty_name_work_groups} NONEMPTY GROUPS",
        31,
    )
    _ = canvas.text(
        Box(100, 2050, 2000),
        "Largest weighting changes: circle = pooled; square = equal group; "
        + "axis = 0–100% of each profile.",
        27,
    )
    for index, row in enumerate(rows):
        y = 2120 + 49 * index
        _ = canvas.text(
            Box(100, y - 12, 720),
            f"{row.category.replace('_', ' ')}: {100 * row.pooled:.1f}% → "
            + f"{100 * row.equal:.1f}%",
            25,
        )
        left = 900 + 1150 * row.pooled
        right = 900 + 1150 * row.equal
        canvas.draw.line((900, y + 5, 2050, y + 5), fill=PALE, width=3)
        canvas.draw.line((left, y + 5, right, y + 5), fill=INK, width=3)
        canvas.draw.ellipse((left - 9, y - 4, left + 9, y + 14), fill=TEAL)
        canvas.draw.rectangle((right - 8, y - 3, right + 8, y + 13), fill=OCHRE)
    _ = canvas.text(
        Box(100, 2280, 2000),
        f"Full-profile TV = {tv:.6f}; these are lexical weighting effects. "
        + "The Worm–infant comparison identifies neither a clade nor an ancestral relation.",
        28,
    )
