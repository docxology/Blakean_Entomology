"""Numerical calibration and refusing controls for the illustrated evidence strips."""

from dataclasses import replace
from pathlib import Path

import pytest
from PIL import ImageColor
from test_native_graphics import abstract_data as abstract_data
from test_native_graphics import figure_data as figure_data
from test_native_graphics import inputs as inputs
from test_visual_assets import admitted_visuals as admitted_visuals
from test_visual_assets import illustrated_font as illustrated_font
from test_visual_assets import visual_inputs as visual_inputs

from blakean_entomology.models import Decision
from blakean_entomology.publication_abstract_details import review_coverage, weighting_contrast
from blakean_entomology.publication_canvas import OCHRE, PALE, TEAL, sheet
from blakean_entomology.publication_data import AbstractData
from blakean_entomology.publication_frontmatter import frontmatter_markdown
from blakean_entomology.publication_transport_models import PublicationError


@pytest.mark.parametrize("reviewed", (0, 25, 100))
def test_review_bar_keeps_its_full_denominator(
    abstract_data: AbstractData, illustrated_font: Path, reviewed: int
) -> None:
    # Given 100 candidates and an independently selected reviewed count.
    summary = abstract_data.context.summary.model_copy(
        update={
            "candidate_hits": 100,
            "reviewed_hits": reviewed,
            "unreviewed_hits": 100 - reviewed,
            "decisions": {
                key: reviewed if key == Decision.ANIMAL_LITERAL else 0 for key in Decision
            },
            "primary_animal_hits": reviewed,
        }
    )
    data = replace(
        abstract_data, context=abstract_data.context.model_copy(update={"summary": summary})
    )
    canvas = sheet(illustrated_font)
    # When the real strip draws a proportional bar.
    with canvas.image:
        review_coverage(canvas, data)
        # Then 25 percent ends at x=600, rather than being enlarged for visibility.
        assert canvas.image.getpixel((500, 2327)) == ImageColor.getrgb(
            TEAL if reviewed >= 25 else PALE
        )
        assert canvas.image.getpixel((700, 2327)) == ImageColor.getrgb(
            TEAL if reviewed == 100 else PALE
        )


def test_empty_selection_has_no_invented_review_share(
    abstract_data: AbstractData, illustrated_font: Path
) -> None:
    # Given an empty declared selection, not a fully reviewed positive population.
    summary = abstract_data.context.summary.model_copy(
        update={
            "candidate_hits": 0,
            "reviewed_hits": 0,
            "unreviewed_hits": 0,
            "decisions": {key: 0 for key in Decision},
            "primary_animal_hits": 0,
        }
    )
    data = replace(
        abstract_data, context=abstract_data.context.model_copy(update={"summary": summary})
    )
    canvas = sheet(illustrated_font)
    # When rendered, the undefined fraction cannot create colored progress.
    with canvas.image:
        review_coverage(canvas, data)
        assert canvas.image.getpixel((1100, 2327)) == ImageColor.getrgb(PALE)


def test_weighting_marks_use_the_same_declared_percentage_axis(
    abstract_data: AbstractData, illustrated_font: Path
) -> None:
    # Given an explicit 25 percent versus 75 percent contrast.
    row = abstract_data.composition.categories[0].model_copy(
        update={
            "pooled_share": 0.25,
            "equal_nonempty_group_share": 0.75,
            "difference_percentage_points": -50,
        }
    )
    data = replace(
        abstract_data,
        composition=abstract_data.composition.model_copy(
            update={"categories": (row,), "pooled_vs_equal_nonempty_tv": 0.5}
        ),
    )
    canvas = sheet(illustrated_font)
    # When the real drawing maps each fraction to its common horizontal scale.
    with canvas.image:
        weighting_contrast(canvas, data)
        # Then the two distinct marks occur at independently calculated coordinates.
        assert canvas.image.getpixel((1187, 2125)) == ImageColor.getrgb(TEAL)
        assert canvas.image.getpixel((1762, 2125)) == ImageColor.getrgb(OCHRE)


@pytest.mark.parametrize("undefined", (None, 0))
def test_absent_composition_is_refused(
    abstract_data: AbstractData, illustrated_font: Path, undefined: float | None
) -> None:
    # Given either undefined composition or an empty category selection.
    composition = abstract_data.composition.model_copy(
        update={"pooled_vs_equal_nonempty_tv": undefined, "categories": ()}
    )
    canvas = sheet(illustrated_font)
    # When an actual plot is requested, no numerical fallback is invented.
    with canvas.image, pytest.raises(PublicationError, match="composition_undefined"):
        weighting_contrast(canvas, replace(abstract_data, composition=composition))


def test_caption_refuses_an_undefined_composition(abstract_data: AbstractData) -> None:
    # Given the caption's numerical input is undefined.
    data = replace(
        abstract_data,
        composition=abstract_data.composition.model_copy(
            update={"pooled_vs_equal_nonempty_tv": None}
        ),
    )
    # When authored frontmatter is requested, the same condition is refused.
    with pytest.raises(PublicationError, match="composition_undefined"):
        frontmatter_markdown(data)


@pytest.mark.parametrize("field", ("pooled_share", "equal_nonempty_group_share"))
def test_incomplete_category_share_is_refused(
    abstract_data: AbstractData, illustrated_font: Path, field: str
) -> None:
    # Given a defined global contrast with one missing category-specific share.
    row = abstract_data.composition.categories[0].model_copy(update={field: None})
    data = replace(
        abstract_data,
        composition=abstract_data.composition.model_copy(update={"categories": (row,)}),
    )
    canvas = sheet(illustrated_font)
    # When drawing it, no zero or other substitute is silently inserted.
    with canvas.image, pytest.raises(PublicationError, match="composition_undefined"):
        weighting_contrast(canvas, data)
