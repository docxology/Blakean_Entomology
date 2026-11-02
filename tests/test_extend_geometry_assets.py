"""Real asset-extension success and refusal before a completion marker."""

import os
import subprocess
import sys
from contextlib import chdir
from pathlib import Path

import pytest
from blake.methods.models import ResearchError
from blake.methods.runs import digest
from test_application import inputs as inputs
from test_geometry_assets import geometry_assets as geometry_assets
from test_geometry_workflow import geometry_files as geometry_files

from tools.extend_geometry_assets import extend_assets
from tools.manuscript_assets import AdditionalAssets, AdditionalInput


@pytest.fixture
def parents(geometry_assets, tmp_path: Path) -> tuple[AdditionalInput, Path, Path]:
    directory, _binding, atlas = geometry_assets
    atlas_path = tmp_path / "atlas.json"
    atlas_path.write_text(atlas.model_dump_json())
    old = tmp_path / "old-assets"
    (old / "sources").mkdir(parents=True)
    payloads = {
        "selected.png": (directory / "source-footprint.png").read_bytes(),
        "sources/ledger.json": b'{"scope":"synthetic source ledger"}',
    }
    entries = {}
    for name, raw in payloads.items():
        (old / name).write_bytes(raw)
        entries[name] = {"path": name, "size": len(raw), "sha256": digest(raw)}
    value = AdditionalAssets.model_validate(
        {
            "epoch": "retained-test-parent",
            "atlas_sha256": digest(atlas_path.read_bytes()),
            "files": [entries["selected.png"]],
            "source_files": [entries["sources/ledger.json"]],
            "image_paths": ["selected.png"],
            "producer_receipts": ["sources/ledger.json"],
            "source_ledgers": ["sources/ledger.json"],
        }
    )
    path = old / "additional-assets.json"
    path.write_text(value.model_dump_json())
    return (
        AdditionalInput(old, digest(path.read_bytes())),
        atlas_path,
        directory / "sources/geometry",
    )


def test_extension_closes_both_parents(parents, geometry_assets, tmp_path: Path) -> None:
    old, atlas, geometry = parents
    _directory, binding, _data = geometry_assets
    output = tmp_path / "analysis_output/extension"
    with chdir(tmp_path):
        result = extend_assets(old, geometry, binding, atlas, digest(atlas.read_bytes()), output)
    assert result.schema_version == 2 and result.geometry_binding == binding
    assert result.image_paths == ("selected.png", "source-footprint.png", "review-exposure.png")
    assert (output / "sources/geometry-parent-assets.json").read_bytes() == (
        old.directory / "additional-assets.json"
    ).read_bytes()
    assert (
        AdditionalInput(output, digest((output / "additional-assets.json").read_bytes())).load(
            digest(atlas.read_bytes())
        )
        == result
    )


@pytest.mark.parametrize(
    "failure", ["atlas_pin", "parent_pin", "geometry_pin", "unknown", "occupied"]
)
def test_extension_refuses_unbound_or_occupied_parent(
    parents, geometry_assets, tmp_path: Path, failure
) -> None:
    old, atlas, geometry = parents
    _directory, binding, _data = geometry_assets
    output = tmp_path / "analysis_output/refused"
    atlas_pin = digest(atlas.read_bytes())
    if failure == "atlas_pin":
        atlas_pin = "0" * 64
    elif failure == "parent_pin":
        old = AdditionalInput(old.directory, "0" * 64)
    elif failure == "geometry_pin":
        binding = binding.model_copy(update={"report_sha256": "0" * 64})
    elif failure == "unknown":
        (geometry / "unbound.txt").write_text("unbound")
    else:
        output.mkdir(parents=True)
        (output / "retain").write_text("retain")
    expected = {
        "atlas_pin": "geometry_asset_atlas_pin",
        "parent_pin": "additional_asset_pin",
        "geometry_pin": "geometry_asset_pin",
        "unknown": "geometry_asset_membership",
        "occupied": "occupied_output",
    }
    with (
        chdir(tmp_path),
        pytest.raises((ValueError, ResearchError, OSError), match=expected[failure]),
    ):
        extend_assets(old, geometry, binding, atlas, atlas_pin, output)
    assert not (output / "additional-assets.json").exists()
    if failure == "occupied":
        assert (output / "retain").read_text() == "retain"


@pytest.mark.parametrize("bad_pin", [False, True])
def test_real_extension_cli(parents, geometry_assets, tmp_path: Path, bad_pin: bool) -> None:
    old, atlas, geometry = parents
    _directory, binding, _data = geometry_assets
    output = tmp_path / "analysis_output/cli"
    args = [sys.executable, "-B", "-m", "tools.extend_geometry_assets"]
    options = {
        "original": str(old.directory),
        "original-sha256": old.sha256,
        "geometry": str(geometry),
        "request-sha256": binding.request_sha256,
        "report-sha256": binding.report_sha256,
        "receipt-sha256": binding.receipt_sha256,
        "atlas": str(atlas),
        "atlas-sha256": "0" * 64 if bad_pin else digest(atlas.read_bytes()),
        "output": str(output),
    }
    for name, value in options.items():
        args.extend(("--" + name, value))
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        args,
        cwd=tmp_path,
        env=dict(os.environ, PYTHONPATH=str(root)),
        capture_output=True,
        text=True,
        check=False,
    )
    if bad_pin:
        assert result.returncode != 0 and "geometry_asset_atlas_pin" in result.stderr
        assert not output.exists()
    else:
        assert result.returncode == 0, result.stderr
        assert (output / "additional-assets.json").is_file()
