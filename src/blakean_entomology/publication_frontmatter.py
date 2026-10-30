"""Native first-four-page composition, credits and measured abstract assets."""

import hashlib
import json
from pathlib import Path

from PIL import Image

from .publication_canvas import Box, sheet
from .publication_data import AbstractData
from .publication_graphics import draw_abstracts


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
    captions = (
        "String retrieval, source eligibility and contextual judgment are separate operations. "
        + f"The explicitly reviewed {data.context.summary.reviewed_hits} decisions are purposive, "
        + f"and {data.context.summary.unreviewed_hits:,} candidates remain unreviewed.",
        "The retained seven-case book supplies the graphical readings and alternatives; "
        + "concise paraphrases are tied to exact case IDs. Full readings and "
        + "source windows remain in the article and contextual casebook.",
        f"Primary name-family profiles use {len(data.composition.category_ids)} "
        + "declared categories "
        + f"and {data.composition.name_category_candidates:,} category-source-span candidates. "
        + "The upper bars pool candidates; lower bars weight nonempty recorded groups equally. "
        + "These are compositional descriptions, not biological abundance or significance tests.",
    )
    titles = (
        "From names to contextual judgment",
        "Encounters and counterreadings",
        "Weighting and the limits of classification",
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
        "reading_scope": (
            "Retained bounded data/readings; no new decisions, species or prevalence claim"
        ),
    }
    raw = (json.dumps(values, indent=2, ensure_ascii=False) + "\n").encode()
    _ = (destination / "frontmatter-data.json").write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()
