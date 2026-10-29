"""Real publication preparation, byte custody and rejecting controls."""

import json
import subprocess
import sys
from contextlib import chdir
from pathlib import Path

import pytest
from blake.methods.models import ResearchError
from test_application import inputs as inputs
from test_taxonomy import REFERENCE, SOURCES, STAGE

from blakean_entomology.atlas import atlas_from_passages
from blakean_entomology.core import digest, vocabulary
from blakean_entomology.models import EvidenceError
from blakean_entomology.workflows import load_pinned_bundle

# Exercise the same tool modules imported by their real executable script paths.
sys.path.insert(0, str(STAGE / "tools"))
from build_reference_figures import FigureReceipt, build_figures  # noqa: E402
from prepare_research_manuscript import prepare  # noqa: E402

CASEBOOK = STAGE / "research/reading-ledger-advancement-v1.json"


@pytest.fixture
def figure_data(inputs, tmp_path) -> Path:
    bundle, pin, _spec, _output = inputs
    snapshot = load_pinned_bundle(bundle, pin)
    atlas = atlas_from_passages(
        snapshot.passages,
        vocabulary(),
        pin,
        digest(REFERENCE.read_bytes()),
        (STAGE / "research/seed-review-summary.json").read_bytes(),
    )
    path = tmp_path / "atlas.json"
    path.write_text(atlas.model_dump_json())
    return path


def generate_figures(atlas, output, tmp_path) -> FigureReceipt:
    with chdir(tmp_path):
        return build_figures(
            atlas,
            digest(atlas.read_bytes()),
            REFERENCE,
            SOURCES,
            digest(REFERENCE.read_bytes()),
            output,
        )


def test_real_reference_and_atlas_figures(figure_data, tmp_path) -> None:
    # Given a separately counted real three-unit synthetic bundle.
    output = tmp_path / "analysis_output/figures"
    # When the actual plotting tool publishes both figures.
    receipt = generate_figures(figure_data, output, tmp_path)
    # Then each vector/raster artifact is closed and counts retain their unit.
    assert receipt.count_unit == "category-source-span candidates"
    assert "3 captured units" in receipt.atlas_caption
    assert "2 primary reading units" in receipt.tree_caption
    assert len(receipt.files) == 5
    for artifact in receipt.files:
        raw = (output / artifact.path).read_bytes()
        assert digest(raw) == artifact.sha256
        if artifact.path.endswith(".png"):
            assert raw.startswith(b"\x89PNG\r\n\x1a\n")
        elif artifact.path.endswith(".svg"):
            assert b"<svg" in raw
    assert "not a sequence-inferred phylogeny" in receipt.tree_caption


@pytest.mark.parametrize(
    "failure", ["pin", "binding", "vocabulary", "outside", "occupied", "symlink"]
)
def test_rejects_unsafe_figure_inputs(figure_data, tmp_path, failure) -> None:
    # Given a changed binding or unsafe publication path.
    output = tmp_path / "analysis_output/figures"
    atlas_pin = digest(figure_data.read_bytes())
    if failure == "pin":
        atlas_pin = "0" * 64
    elif failure in ("binding", "vocabulary"):
        raw = json.loads(figure_data.read_bytes())
        raw["reference_sha256" if failure == "binding" else "vocabulary_sha256"] = "0" * 64
        figure_data.write_text(json.dumps(raw))
        atlas_pin = digest(figure_data.read_bytes())
    elif failure == "outside":
        output = tmp_path / "public"
    elif failure == "occupied":
        output.mkdir(parents=True)
        (output / "retain.txt").write_text("retain")
    else:
        output.parent.mkdir()
        target = tmp_path / "untouched"
        target.mkdir()
        output.symlink_to(target, target_is_directory=True)
    # When the real generator runs without mocked collaborators.
    with chdir(tmp_path), pytest.raises(EvidenceError):
        build_figures(
            figure_data, atlas_pin, REFERENCE, SOURCES, digest(REFERENCE.read_bytes()), output
        )
    # Then existing destinations remain intact and no fallback picture appears.
    if failure == "occupied":
        assert (output / "retain.txt").read_text() == "retain"


def prepare_command(atlas, figures, output) -> list[str]:
    return [
        sys.executable,
        str(STAGE / "tools/prepare_research_manuscript.py"),
        "--manuscript",
        str(STAGE / "docs/manuscript/blakean-entomology.md"),
        "--bibliography",
        str(STAGE / "docs/manuscript/references.bib"),
        "--atlas",
        str(atlas),
        "--atlas-sha256",
        digest(atlas.read_bytes()),
        "--figures",
        str(figures),
        "--figures-sha256",
        digest((figures / "figures.json").read_bytes()),
        "--casebook",
        str(CASEBOOK),
        "--casebook-sha256",
        digest(CASEBOOK.read_bytes()),
        "--reference",
        str(REFERENCE),
        "--reference-sha256",
        digest(REFERENCE.read_bytes()),
        "--sources",
        str(SOURCES),
        "--output",
        str(output),
    ]


def prepare_inputs(
    atlas, figures, output
) -> tuple[Path, Path, Path, str, Path, str, Path, str, Path, Path, str, Path]:
    return (
        STAGE / "docs/manuscript/blakean-entomology.md",
        STAGE / "docs/manuscript/references.bib",
        atlas,
        digest(atlas.read_bytes()),
        figures,
        digest((figures / "figures.json").read_bytes()),
        CASEBOOK,
        digest(CASEBOOK.read_bytes()),
        REFERENCE,
        SOURCES,
        digest(REFERENCE.read_bytes()),
        output,
    )


def test_preparation_roundtrip_and_real_cli(figure_data, tmp_path) -> None:
    # Given closed figures, exact reading credit and the authored article.
    figures = tmp_path / "analysis_output/figures"
    generate_figures(figure_data, figures, tmp_path)
    output = tmp_path / "analysis_output/article"
    # When preparing Markdown in-process and exercising its real CLI on a fresh output.
    with chdir(tmp_path):
        receipt = prepare(*prepare_inputs(figure_data, figures, output))
    result = subprocess.run(
        prepare_command(figure_data, figures, tmp_path / "analysis_output/cli"),
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    # Then hydration, bibliographic closure and all copied assets are real files.
    assert result.returncode == 0, result.stderr
    text = (output / "blakean-entomology.md").read_text()
    assert "{{" not in text
    assert "37 admitted NCBI" in text
    assert "raw counts" in text
    assert "no native PDF" in receipt.qualification
    assert (output / "contextual-casebook.md").read_text().count("Selected-text SHA-256") == 9
    assert len(receipt.files) == 8


@pytest.mark.parametrize(
    "failure",
    ["pin", "binding", "figure_bytes", "token", "token_syntax", "citation", "figure_membership"],
)
def test_rejects_false_manuscript_inputs(figure_data, tmp_path, failure) -> None:
    # Given an independently generated figure packet and one corrupt input.
    figures = tmp_path / "analysis_output/figures"
    generate_figures(figure_data, figures, tmp_path)
    args = list(prepare_inputs(figure_data, figures, tmp_path / "analysis_output/rejected"))
    if failure == "pin":
        args[3] = "0" * 64
    elif failure == "binding":
        raw = json.loads((figures / "figures.json").read_bytes())
        raw["atlas_sha256"] = "0" * 64
        (figures / "figures.json").write_text(json.dumps(raw))
        args[5] = digest((figures / "figures.json").read_bytes())
    elif failure == "figure_bytes":
        (figures / "corpus-atlas.png").write_bytes(b"changed")
    else:
        manuscript = tmp_path / "article.md"
        source = (STAGE / "docs/manuscript/blakean-entomology.md").read_text()
        edits = {
            "token": "\n{{INVENTED_COUNT}}",
            "token_syntax": "\n{{unfinished",
            "citation": "\n[@invented-source]",
            "figure_membership": "\n![Extra](assets/extra.png)",
        }
        manuscript.write_text(source + edits[failure])
        args[0] = manuscript
    # When the preparation boundary checks it.
    with chdir(tmp_path), pytest.raises((EvidenceError, ValueError, ResearchError)):
        prepare(*args)
    # Then no renderable output packet is published.
    assert not (tmp_path / "analysis_output/rejected").exists()


def test_real_figure_cli_rejects_changed_pin(figure_data, tmp_path) -> None:
    # Given a valid atlas and wrong caller-held digest.
    command = [
        sys.executable,
        str(STAGE / "tools/build_reference_figures.py"),
        "--atlas",
        str(figure_data),
        "--atlas-sha256",
        "0" * 64,
        "--reference",
        str(REFERENCE),
        "--reference-sha256",
        digest(REFERENCE.read_bytes()),
        "--sources",
        str(SOURCES),
        "--output",
        str(tmp_path / "analysis_output/rejected"),
    ]
    # When driving the actual executable script.
    result = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True)
    # Then failure is explicit and nonzero.
    assert result.returncode != 0
    assert "atlas_pin" in result.stderr
