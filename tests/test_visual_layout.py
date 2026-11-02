"""Measured physical image coverage and real graphical-layout refusals."""

from dataclasses import replace

import pytest
from PIL import Image, ImageColor
from test_native_graphics import abstract_data as abstract_data
from test_native_graphics import figure_data as figure_data
from test_native_graphics import inputs as inputs
from test_visual_assets import admitted_visuals as admitted_visuals
from test_visual_assets import illustrated_font as illustrated_font
from test_visual_assets import visual_inputs as visual_inputs

from blakean_entomology.publication_canvas import PAPER, sheet
from blakean_entomology.publication_frontmatter import frontmatter_markdown
from blakean_entomology.publication_illustrated import fly
from blakean_entomology.publication_transport_models import PublicationError
from blakean_entomology.publication_visual_layout import (
    ImageFrame,
    argument,
    quotation,
    whole_image,
    witness_panel,
)


def test_whole_image_keeps_every_corner_and_proportion(tmp_path, illustrated_font) -> None:
    source = tmp_path / "source.png"
    with Image.new("RGB", (500, 1000)) as photo:
        for box, colour in (
            ((0, 0, 250, 500), "red"),
            ((250, 0, 500, 500), "blue"),
            ((0, 500, 250, 1000), "green"),
            ((250, 500, 500, 1000), "yellow"),
        ):
            photo.paste(colour, box)
        photo.save(source)
    canvas = sheet(illustrated_font)
    with canvas.image:
        whole_image(canvas, source, ImageFrame(50, 60, 300, 200))
        assert canvas.image.getpixel((155, 65)) == (255, 0, 0)
        assert canvas.image.getpixel((245, 65)) == (0, 0, 255)
        assert canvas.image.getpixel((155, 255)) == (0, 128, 0)
        assert canvas.image.getpixel((245, 255)) == (255, 255, 0)
        assert canvas.image.getpixel((70, 160)) == ImageColor.getrgb(PAPER)


@pytest.mark.parametrize("failure", ("font", "quote", "credit", "argument"))
def test_layout_refuses_missing_font_or_overfull_panels(
    admitted_visuals, illustrated_font, failure
) -> None:
    witness = admitted_visuals.witness("fly")
    canvas = sheet(illustrated_font)
    with canvas.image, pytest.raises(PublicationError):
        match failure:
            case "font":
                illustrated_font.with_name("LiberationSerif-Italic.ttf").rename(
                    illustrated_font.with_name("retained.ttf")
                )
                quotation(canvas, witness)
            case "quote":
                quotation(canvas, witness.model_copy(update={"quotation": "many words " * 35}))
            case "credit":
                witness_panel(
                    canvas, admitted_visuals, witness.model_copy(update={"credit": "credit " * 70})
                )
            case "argument":
                argument(canvas, witness.model_copy(update={"reading": "a relation " * 60}))


def test_production_refuses_to_invent_missing_visual_sources(
    abstract_data, illustrated_font
) -> None:
    absent = replace(abstract_data, visuals=None)
    canvas = sheet(illustrated_font)
    with canvas.image, pytest.raises(PublicationError, match="illustrated_source_required"):
        fly(canvas, absent)
    with pytest.raises(PublicationError, match="illustrated_source_required"):
        frontmatter_markdown(absent)
