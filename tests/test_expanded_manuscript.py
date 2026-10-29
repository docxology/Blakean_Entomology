"""Real additional-asset preparation, including rejecting publication controls."""

import json
import subprocess
from contextlib import chdir
from pathlib import Path

import pytest
from blake.methods.models import ResearchError
from test_application import inputs as inputs
from test_research_figures import (
    AdditionalInput,
    generate_figures,
    legacy_manuscript,
    prepare,
    prepare_command,
    prepare_inputs,
)
from test_research_figures import (
    figure_data as figure_data,
)

from blakean_entomology.core import digest
from blakean_entomology.models import EvidenceError


@pytest.fixture
def expanded_inputs(figure_data, tmp_path) -> tuple[Path, Path, Path, Path]:
    """Use tiny actual PNG bytes and source receipts, without historic image bodies."""
    figures = tmp_path / "analysis_output/figures"
    generate_figures(figure_data, figures, tmp_path)
    manuscript = legacy_manuscript(figure_data.parent)
    manuscript.write_text(
        manuscript.read_text()
        + "\n![Selected [1794]](assets/selected.png)\n\n$$p_{gw}=\\frac{c_{gw}}{m_w}$$\n"
    )
    additional = tmp_path / "additional"
    (additional / "sources").mkdir(parents=True)
    image = (figures / "corpus-atlas.png").read_bytes()
    (additional / "selected.png").write_bytes(image)
    source = b'{"source":"synthetic real-file fixture"}\n'
    (additional / "sources/ledger.json").write_bytes(source)
    manifest = {
        "schema_version": 1,
        "epoch": "real-file-test",
        "atlas_sha256": digest(figure_data.read_bytes()),
        "files": [{"path": "selected.png", "size": len(image), "sha256": digest(image)}],
        "image_paths": ["selected.png"],
        "source_files": [
            {"path": "sources/ledger.json", "size": len(source), "sha256": digest(source)}
        ],
        "producer_receipts": ["sources/ledger.json"],
        "source_ledgers": ["sources/ledger.json"],
        "replacements": {},
    }
    (additional / "additional-assets.json").write_text(json.dumps(manifest))
    return figure_data, figures, manuscript, additional


def test_expanded_preparation_copies_exact_bytes(expanded_inputs, tmp_path) -> None:
    # Given actual base figures and one explicitly pinned additional PNG.
    atlas, figures, _manuscript, extra = expanded_inputs
    args = prepare_inputs(atlas, figures, tmp_path / "analysis_output/article")
    expected = digest((extra / "additional-assets.json").read_bytes())
    # When the real preparation adapter publishes a new epoch.
    with chdir(tmp_path):
        receipt = prepare(*args, additional=AdditionalInput(extra, expected))
    # Then the copied bytes and all provenance receipts are bound in completion.
    assert (args[-1] / "assets/selected.png").read_bytes() == (extra / "selected.png").read_bytes()
    assert receipt.additional_assets_sha256 == expected
    assert receipt.additional_assets is not None
    assert receipt.additional_assets.source_ledgers == ("sources/ledger.json",)


def test_expanded_real_cli(expanded_inputs, tmp_path) -> None:
    # Given the real command and its independent expected manifest digest.
    atlas, figures, _manuscript, extra = expanded_inputs
    output = tmp_path / "analysis_output/cli"
    command = prepare_command(atlas, figures, output) + [
        "--additional-assets",
        str(extra),
        "--additional-assets-sha256",
        digest((extra / "additional-assets.json").read_bytes()),
    ]
    # When executed as a real child process.
    result = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True)
    # Then preparation completes with the additional input manifest copied unchanged.
    assert result.returncode == 0, result.stderr
    assert (output / "additional-assets.json").read_bytes() == (
        extra / "additional-assets.json"
    ).read_bytes()


@pytest.mark.parametrize(
    "failure",
    [
        "pin",
        "binding",
        "malformed",
        "traversal",
        "symlink",
        "collision",
        "duplicate",
        "occupied",
        "corrupt_asset",
        "corrupt_source",
        "unknown_file",
        "unknown_image",
        "missing_source",
        "duplicate_image",
        "undeclared_producer",
        "unknown_field",
        "closing_token",
        "opening_token_in_math",
        "malformed_image",
    ],
)
def test_expanded_refuses_before_reservation(expanded_inputs, tmp_path, failure) -> None:
    # Given one independently malformed boundary or occupied output.
    atlas, figures, manuscript, extra = expanded_inputs
    output = tmp_path / "analysis_output/rejected"
    path = extra / "additional-assets.json"
    manifest = json.loads(path.read_bytes())
    expected = digest(path.read_bytes())
    if failure == "pin":
        expected = "0" * 64
    elif failure == "occupied":
        output.mkdir()
        (output / "retained").write_bytes(b"retain")
    elif failure == "corrupt_asset":
        (extra / "selected.png").write_bytes(b"corrupt")
    elif failure == "corrupt_source":
        (extra / "sources/ledger.json").write_bytes(b"corrupt")
    elif failure == "unknown_file":
        (extra / "unlisted.png").write_bytes(b"unlisted")
    elif failure == "unknown_image":
        manuscript.write_text(manuscript.read_text() + "\n![Unknown](assets/unknown.png)\n")
    elif failure == "malformed_image":
        manuscript.write_text(manuscript.read_text() + "\n![unclosed caption(assets/unknown.png)\n")
    elif failure in ("closing_token", "opening_token_in_math"):
        manuscript.write_text(
            manuscript.read_text()
            + ("\nstray }}\n" if failure == "closing_token" else "\n$ {{unfinished $\n")
        )
    elif failure == "symlink":
        original = extra / "selected.png"
        target = tmp_path / "actual.png"
        original.rename(target)
        original.symlink_to(target)
    else:
        if failure == "binding":
            manifest["atlas_sha256"] = "0" * 64
        elif failure == "traversal":
            manifest["files"][0]["path"] = "../selected.png"
        elif failure == "collision":
            manifest["files"][0]["path"] = "corpus-atlas.png"
            manifest["image_paths"] = ["corpus-atlas.png"]
        elif failure == "duplicate":
            manifest["files"].append(manifest["files"][0])
        elif failure == "missing_source":
            manifest["source_files"] = []
        elif failure == "duplicate_image":
            manifest["image_paths"].append("selected.png")
        elif failure == "undeclared_producer":
            manifest["producer_receipts"] = ["sources/unknown.json"]
        elif failure == "unknown_field":
            manifest["unexpected"] = "reject"
        path.write_text("{}" if failure == "malformed" else json.dumps(manifest))
        expected = digest(path.read_bytes())
    args = prepare_inputs(atlas, figures, output)
    # When admission validates every artifact before reserving output.
    with chdir(tmp_path), pytest.raises((EvidenceError, ResearchError, ValueError, OSError)):
        prepare(*args, additional=AdditionalInput(extra, expected))
    # Then no output is created, and an existing output is unchanged.
    if failure == "occupied":
        assert {p.name: p.read_bytes() for p in output.iterdir()} == {"retained": b"retain"}
    else:
        assert not output.exists()
