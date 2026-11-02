"""Real-file native custody and measured graphical publication, without mocks."""

import hashlib
import json
from dataclasses import replace

import pytest
from PIL import Image
from test_application import inputs as inputs
from test_research_figures import figure_data as figure_data
from test_taxonomy import STAGE
from test_visual_assets import admitted_visuals as admitted_visuals
from test_visual_assets import illustrated_font as illustrated_font
from test_visual_assets import visual_inputs as visual_inputs

from blakean_entomology.atlas_models import AtlasReceipt
from blakean_entomology.casebook import Casebook
from blakean_entomology.composition import CompositionAudit, CompositionContrast
from blakean_entomology.models import Decision, ReviewSummary
from blakean_entomology.publication_canvas import Box, sheet
from blakean_entomology.publication_data import (
    AbstractData,
    CoverObject,
)
from blakean_entomology.publication_frontmatter import frontmatter_markdown, publish_frontmatter
from blakean_entomology.publication_transport_models import PublicationError
from blakean_entomology.review_contexts import ContextAudit


@pytest.fixture
def abstract_data(figure_data, admitted_visuals) -> AbstractData:
    atlas = AtlasReceipt.model_validate_json(figure_data.read_bytes())
    summary = ReviewSummary(
        application_version="fixture",
        application_code_sha256="a" * 64,
        run_sha256="b" * 64,
        decisions_sha256="c" * 64,
        candidate_hits=atlas.candidates,
        reviewed_hits=1,
        unreviewed_hits=atlas.candidates - 1,
        decisions={key: int(key == Decision.ANIMAL_LITERAL) for key in Decision},
        primary_animal_hits=1,
        exploratory_animal_hits=0,
    )
    context = ContextAudit(
        run_sha256=summary.run_sha256,
        decisions_sha256=summary.decisions_sha256,
        summary=summary,
        cells=(),
        cohorts=(),
        work_groups=1,
        source_units=1,
        generator_sha256="d" * 64,
    )
    row = CompositionContrast(
        category="worm",
        candidates=2,
        exact_text_candidates=2,
        matched_units=1,
        positive_work_groups=1,
        pooled_share=1.0,
        equal_nonempty_group_share=1.0,
        difference_percentage_points=0,
        minimum_groups_for_half=1,
        minimum_groups_for_four_fifths=1,
        effective_groups=1.0,
    )
    composition = CompositionAudit(
        category_ids=("worm",),
        source_units=1,
        tokens=2,
        work_groups=1,
        nonempty_name_work_groups=1,
        name_category_candidates=2,
        pooled_vs_equal_nonempty_tv=0,
        categories=(row,),
        omissions=(),
    )
    book = Casebook.model_validate_json(
        (STAGE / "research/reading-ledger-advancement-v1.json").read_bytes()
    )
    cover = CoverObject.model_validate(
        {
            "id": "fixture",
            "accession": "fixture",
            "title": "fixture",
            "work": "fixture",
            "copy": "fixture",
            "catalogue_date": "2026",
            "creator": "fixture",
            "credit": "fixture",
            "source": "https://example.org",
            "rights": "fixture",
            "images": {"museum_recto": {"sha256": "e" * 64, "bytes": 1}},
        }
    )
    return AbstractData(atlas, composition, context, book, cover, 1, admitted_visuals)


def test_frontmatter_is_drawn_from_real_typed_inputs(
    abstract_data, tmp_path, illustrated_font
) -> None:
    # Given actual admitted atlas data, authored cases and a real raster.
    original = tmp_path / "original.png"
    with Image.new("RGB", (70, 100), "#aabbcc") as image:
        image.save(original)
    font = illustrated_font
    target = tmp_path / "figures"
    target.mkdir()
    # When the real publication producer renders its complete front matter.
    data_sha = publish_frontmatter(abstract_data, target, (original, font))
    # Then actual image dimensions and the exact numerical/data companion close.
    assert hashlib.sha256((target / "frontmatter-data.json").read_bytes()).hexdigest() == data_sha
    values = json.loads((target / "frontmatter-data.json").read_bytes())
    assert values["atlas"]["candidates"] == abstract_data.atlas.candidates
    assert values["context"]["summary"]["reviewed_hits"] == 1
    for path in target.glob("*.png"):
        with Image.open(path) as image:
            assert image.size == (2200, 2360)
            assert image.getextrema()[0][0] < image.getextrema()[0][1]
    assert len(tuple(target.glob("*.png"))) == 4
    markdown = frontmatter_markdown(abstract_data)
    for witness in abstract_data.visuals.manifest.witnesses:
        assert f"[@{witness.citation_key}]" in markdown
        assert " / ".join(witness.quotation.splitlines()) in markdown
    assert markdown.count("{#fig:graphical_abstract_") == 3


@pytest.mark.parametrize("failure", ("word", "height", "undefined_composition"))
def test_real_diagram_refuses_unrepresentable_content(
    abstract_data, tmp_path, failure, illustrated_font
) -> None:
    # Given an actual fixed canvas or an undefined compositional profile.
    font = illustrated_font
    canvas = sheet(font)
    # When an actual boundary is exceeded.
    with canvas.image, pytest.raises(PublicationError):
        match failure:
            case "word":
                _ = canvas.text(Box(10, 10, 1), "long", 38)
            case "height":
                _ = canvas.text(Box(10, 2350, 100), "line", 38)
            case "undefined_composition":
                from blakean_entomology.publication_illustrated import worm

                worm(
                    canvas,
                    replace(
                        abstract_data,
                        composition=(
                            abstract_data.composition.model_copy(
                                update={"pooled_vs_equal_nonempty_tv": None}
                            )
                        ),
                    ),
                )
    # Then no fallback raster was published.
    assert not tuple(tmp_path.glob("*.png"))
