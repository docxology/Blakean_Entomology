"""Three distinct graphical arguments from existing data and bounded case readings."""

from pathlib import Path

from .models import Decision
from .publication_canvas import INK, OCHRE, RED, TEAL, Box, Sheet, sheet
from .publication_data import AbstractData
from .publication_relations import RELATIONS
from .publication_wire import PublicationError


def retrieval(sheet: Sheet, data: AbstractData) -> None:
    """Separate matching, source eligibility and contextual judgments."""
    atlas, review = data.atlas, data.context
    _ = sheet.text(Box(100, 80, 2000), "NAMES ARE THE BEGINNING", 66)
    _ = sheet.text(
        Box(100, 190, 2000),
        "A concordance finds strings. Source custody and contextual reading "
        + "answer different questions.",
        40,
    )
    facets = "; ".join(
        f"{plane.replace('_', ' ')}: "
        + "/".join(sorted({c.role for c in atlas.cohorts if c.plane == plane}))
        for plane in sorted({c.plane for c in atlas.cohorts})
    )
    cards = (
        (
            "1  RETRIEVE",
            f"{atlas.category_count} declared categories / "
            + f"{atlas.explicit_form_count} explicit forms\n"
            + f"{atlas.scanned_units:,} retained source units\n"
            + f"{atlas.candidates:,} category-source-span candidates",
            TEAL,
        ),
        (
            "2  KEEP SOURCE FACETS",
            facets + "\nOriginal source roles and planes stay attached to every hit.",
            OCHRE,
        ),
        (
            "3  READ THE CONTEXT",
            f"{review.summary.reviewed_hits} explicitly reviewed decisions; "
            + f"{review.summary.unreviewed_hits:,} remain unreviewed.\n"
            + "Literal and figurative animals, associated material, non-animal senses, "
            + "editorial language and uncertainty remain distinct.",
            RED,
        ),
    )
    for index, (title, text, color) in enumerate(cards):
        y = 400 + index * 480
        sheet.panel((100, y, 2100, y + 380), color)
        _ = sheet.text(Box(155, y + 35, 1880), title, 49)
        _ = sheet.text(Box(155, y + 125, 1850), text, 42)
        if index < len(cards) - 1:
            sheet.draw.line((1100, y + 390, 1100, y + 460), fill=INK, width=7)
            sheet.draw.polygon(((1078, y + 440), (1122, y + 440), (1100, y + 470)), fill=INK)
    counts = review.summary.decisions
    labels = (
        "Literal animal",
        "Figurative animal",
        "Associated",
        "Non-animal",
        "Editorial",
        "Uncertain",
    )
    keys = (
        Decision.ANIMAL_LITERAL,
        Decision.ANIMAL_FIGURATIVE,
        Decision.ASSOCIATED,
        Decision.NON_ANIMAL,
        Decision.EDITORIAL,
        Decision.UNCERTAIN,
    )
    for index, (label, key) in enumerate(zip(labels, keys, strict=True)):
        x = 110 + (index % 3) * 700
        y = 1890 + (index // 3) * 130
        _ = sheet.text(Box(x, y, 660), f"{counts[key]}  {label}", 41)
    _ = sheet.text(
        Box(100, 2200, 2000),
        "Purposive agent judgments, with overlapping categories and repeated witnesses. "
        + "No prevalence, classifier accuracy, organism or species count.",
        32,
    )


def encounters(sheet: Sheet, data: AbstractData) -> None:
    """Compare literary relations and alternatives rather than catalogue locators."""
    if {c.case_id for c in data.casebook.cases} != {r.case_id for r in RELATIONS}:
        raise PublicationError(
            "casebook_graphic_membership", "Require every declared case exactly once"
        )
    _ = sheet.text(Box(100, 70, 2000), "CARE, FEEDING, AND JOINED POWERS", 59)
    _ = sheet.text(
        Box(100, 175, 2000),
        "Seven retained casebook readings. The same small body need not "
        + "do the same moral work.",
        40,
    )
    _ = sheet.text(Box(115, 325, 540), "RELATION / CASE", 34)
    _ = sheet.text(Box(730, 325, 690), "PROPOSED READING", 34)
    _ = sheet.text(Box(1500, 325, 600), "LIVE ALTERNATIVE", 34)
    for index, relation in enumerate(RELATIONS):
        y = 420 + index * 244
        sheet.draw.line((100, y - 20, 2100, y - 20), fill=TEAL, width=3)
        _ = sheet.text(Box(115, y, 540), relation.relation, 40)
        _ = sheet.text(Box(115, y + 140, 540), relation.case_id, 27)
        _ = sheet.text(Box(730, y, 690), relation.reading, 36)
        _ = sheet.text(Box(1500, y, 600), relation.alternative, 34)
    _ = sheet.text(
        Box(100, 2210, 2000),
        "Source-bound interpretations, with complete locators in the article "
        + "and casebook companion. These relations neither identify modern species "
        + "nor add contextual review decisions.",
        31,
    )


def weighting(sheet: Sheet, data: AbstractData) -> None:
    """Show query-channel scope and the measured effect of compositional weighting."""
    audit = data.composition
    _ = sheet.text(Box(100, 80, 2000), "WHAT CHANGES WHEN GROUPS COUNT EQUALLY?", 55)
    _ = sheet.text(
        Box(100, 180, 2000),
        "Shares describe the selected name-family candidate profile. "
        + "They do not describe the abundance of animals in Blake.",
        40,
    )
    sheet.panel((100, 360, 2100, 670))
    _ = sheet.text(
        Box(155, 395, 1880),
        f"{len(audit.category_ids)} name-family categories / "
        + f"{audit.name_category_candidates:,} primary candidates / "
        + f"{audit.nonempty_name_work_groups} nonempty recorded work groups",
        46,
    )
    _ = sheet.text(
        Box(155, 540, 1880),
        f"All {data.atlas.category_count} query categories instead yield "
        + f"{data.atlas.primary_candidates:,} primary candidates.",
        39,
    )
    _ = sheet.text(Box(100, 760, 2000), "POOL CANDIDATES  /  WEIGHT NONEMPTY GROUPS EQUALLY", 41)
    top = sorted(audit.categories, key=lambda c: c.candidates, reverse=True)[:8]
    scale = 1240
    for index, row in enumerate(top):
        y = 880 + index * 118
        _ = sheet.text(Box(110, y, 470), row.category.replace("_", " "), 36)
        pooled = row.pooled_share or 0.0
        equal = row.equal_nonempty_group_share or 0.0
        sheet.draw.rectangle((600, y, 600 + round(scale * pooled), y + 28), fill=TEAL)
        sheet.draw.rectangle((600, y + 36, 600 + round(scale * equal), y + 64), fill=OCHRE)
        _ = sheet.text(Box(1560, y, 540), f"{pooled:.1%} / {equal:.1%}", 33)
    tv = audit.pooled_vs_equal_nonempty_tv
    if tv is None:
        raise PublicationError("composition_undefined", "No nonempty profile for this abstract")
    _ = sheet.text(
        Box(100, 1900, 2000),
        f"Total variation = {tv:.6f}\n"
        + "Finite profile distance; not a significance test or an independence estimate.",
        43,
    )
    _ = sheet.text(
        Box(100, 2160, 2000),
        "Two bars per category: upper teal = pooled; lower ochre = equal-group. "
        + "The eight largest pooled categories are displayed; full coverage and zero "
        + f"categories remain in the {len(audit.category_ids)}-row appendix.",
        32,
    )


def draw_abstracts(data: AbstractData, output: Path, font: Path) -> tuple[Path, ...]:
    """Draw actual high-resolution diagrams, without recomputing the shared methods."""
    paths: list[Path] = []
    for number, draw in enumerate((retrieval, encounters, weighting), start=1):
        canvas = sheet(font)
        with canvas.image:
            draw(canvas, data)
            target = output / f"graphical-abstract-{number}.png"
            canvas.image.save(target, dpi=(300, 300))
        paths.append(target)
    return tuple(paths)
