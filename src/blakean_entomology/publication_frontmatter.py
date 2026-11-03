"""Native first-four-page composition, credits and measured abstract assets."""

import hashlib
import json
from pathlib import Path

from PIL import Image

from .publication_canvas import Box, sheet
from .publication_data import AbstractData
from .publication_graphics import draw_abstracts
from .publication_transport_models import PublicationError


def cover(data: AbstractData, source: Path, target: Path, font: Path) -> None:
    """Reproduce the complete museum recto proportionally, with a separate credit strip."""
    canvas = sheet(font)
    with canvas.image, Image.open(source) as original:
        with original.convert("RGB") as resized:
            resized.thumbnail((2000, 2010), Image.Resampling.LANCZOS)
            canvas.image.paste(resized, ((2200 - resized.width) // 2, 15))
        _ = canvas.text(
            Box(100, 2055, 2000),
            f"{data.cover.creator}, {data.cover.title}; "
            + f"{data.cover.work}, copy {data.cover.copy_id} ({data.cover.catalogue_date}).",
            34,
        )
        _ = canvas.text(
            Box(100, 2165, 2000),
            f"{data.cover.credit}. {data.cover.accession}. "
            + "Public Domain / CC0 museum record. Complete recto; no recolouring "
            + "or reconstructed image content.",
            30,
        )
        canvas.image.save(target, dpi=(300, 300))


def frontmatter_markdown(data: AbstractData) -> str:
    """Use native figure counters and source-only page hooks before the native TOC."""
    if data.visuals is None:
        raise PublicationError("illustrated_source_required", "Frontmatter")
    tv = data.composition.pooled_vs_equal_nonempty_tv
    if tv is None:
        raise PublicationError("composition_undefined", "Graphical abstract caption")
    details = (
        f"The lower panel separates {data.context.summary.candidate_hits:,} candidates, "
        + f"{data.context.summary.reviewed_hits} authored review decisions and "
        + f"{data.context.summary.unreviewed_hits:,} unreviewed candidates. Its proportional "
        + "bar keeps the complete candidate denominator; neither the image nor the analogy "
        + "adds a contextual decision.",
        "The lower cards separate the emmet's need, the glow-worm's light and the beetle's "
        + "audible route. These are capacities offered in the text, not a reported rescue "
        + "or observed insect behavior. A compound name must be read before classification.",
        "The lower plot shows the three largest absolute category-share changes under "
        + "pooled and equal nonempty-group weighting. Circles and squares share a 0–100% "
        + f"axis; full-profile total variation is {tv:.6f}. Lexical profiles and the "
        + "Worm–infant comparison establish no species identity or ancestral relation.",
    )
    captions = tuple(
        f"{w.title}. “{' / '.join(w.quotation.splitlines())}” "
        + f"{w.locator} {w.credit} [@{w.citation_key}]. "
        + "The panels distinguish a reading, a rival and a conditional classification. "
        + detail
        for w, detail in zip(data.visuals.manifest.witnesses, details, strict=True)
    )
    titles = (
        "The Fly: likeness and injury",
        "A Dream: hearing and a route home",
        "Thel: comparison, care and classification",
    )
    lines = [r"\setcounter{page}{2}", r"\thispagestyle{plain}", ""]
    for number, (title, caption) in enumerate(zip(titles, captions, strict=True), start=1):
        lines.extend(
            (
                f"# Graphical abstract {number}: {title} {{.unnumbered .unlisted}}",
                "",
                f"![{caption}](../figures/graphical-abstract-{number}.png)"
                + f"{{#fig:graphical_abstract_{number} width=98%}}",
                "",
                r"\clearpage",
                "",
            )
        )
    lines.extend((r"\Econtents", "", r"\clearpage", ""))
    return "\n".join(lines)


def publish_frontmatter(data: AbstractData, destination: Path, resources: tuple[Path, Path]) -> str:
    """Publish diagrams, source-derived values and structured figure alternatives."""
    original, font = resources
    _ = draw_abstracts(data, destination, font)
    cover(data, original, destination / "cover.png", font)
    values = {
        "atlas": data.atlas.model_dump(mode="json"),
        "composition": data.composition.model_dump(mode="json"),
        "context": data.context.model_dump(mode="json"),
        "casebook": data.casebook.model_dump(mode="json"),
        "cover": data.cover.model_dump(mode="json"),
        "selected_originals": data.selected_originals,
        "visual_witnesses": data.visuals.manifest.model_dump(mode="json") if data.visuals else None,
        "reading_scope": (
            "Retained bounded data/readings; no new decisions, species or prevalence claim"
        ),
    }
    raw = (json.dumps(values, indent=2, ensure_ascii=False) + "\n").encode()
    _ = (destination / "frontmatter-data.json").write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()
