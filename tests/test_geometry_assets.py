"""Real-file geometry/atlas/figure joins, including coherently rebound faults."""

import json
import shutil
from contextlib import chdir
from pathlib import Path

import pytest
from blake.methods.runs import digest
from blake.studies import StudySpec
from test_application import inputs as inputs
from test_geometry_workflow import geometry_files as geometry_files

from blakean_entomology.atlas import atlas_from_passages
from blakean_entomology.atlas_models import AtlasReceipt
from blakean_entomology.core import review
from blakean_entomology.geometry_run import publish_geometry
from blakean_entomology.models import EvidenceError
from blakean_entomology.publication_profiles import CURRENT_SDK_COMMIT
from blakean_entomology.workflows import load_pinned_bundle
from tools.geometry_asset_contract import GeometryAssetBinding, verify_geometry_assets


@pytest.fixture
def geometry_assets(
    geometry_files, tmp_path: Path
) -> tuple[Path, GeometryAssetBinding, AtlasReceipt]:
    paths = geometry_files
    data = json.loads(paths["request"].read_bytes())
    data["sdk_commit"] = CURRENT_SDK_COMMIT
    paths["request"].write_text(json.dumps(data))
    with chdir(tmp_path):
        _ = publish_geometry(
            paths["request"],
            digest(paths["request"].read_bytes()),
            paths["bundle"],
            paths["run"],
            paths["decisions"],
            paths["windows"],
            paths["vocabulary"],
            paths["output"],
            figures=True,
        )
    from blakean_entomology.geometry_models import GeometryRequest

    request = GeometryRequest.model_validate_json(paths["request"].read_bytes())
    snapshot = load_pinned_bundle(paths["bundle"], request.corpus_pin)
    summary = review(paths["run"], paths["decisions"], request.run_sha256)
    atlas = atlas_from_passages(
        snapshot.passages,
        StudySpec.model_validate_json(paths["vocabulary"].read_bytes()),
        request.corpus_pin,
        "a" * 64,
        summary.model_dump_json().encode(),
    )
    additional = tmp_path / "additional"
    shutil.copytree(paths["output"], additional / "sources/geometry")
    for name in ("source-footprint", "review-exposure"):
        for suffix in ("png", "svg", "pdf"):
            shutil.copy2(paths["output"] / f"figures/{name}.{suffix}", additional)
    binding = GeometryAssetBinding(
        request_sha256=digest((paths["output"] / "geometry-request.json").read_bytes()),
        report_sha256=digest((paths["output"] / "geometry-report.json").read_bytes()),
        receipt_sha256=digest((paths["output"] / "geometry-receipt.json").read_bytes()),
    )
    return additional, binding, atlas


def test_complete_normal_installed_geometry_assets(geometry_assets) -> None:
    directory, binding, atlas = geometry_assets
    captions = verify_geometry_assets(directory, binding, atlas)
    assert set(captions) == {"GEOMETRY_SOURCE_CAPTION", "GEOMETRY_REVIEW_CAPTION"}
    assert "1 authored decisions" in captions["GEOMETRY_REVIEW_CAPTION"]


@pytest.mark.parametrize(
    "failure", ["pin", "report_run", "sdk", "corpus", "atlas_run", "membership", "figure"]
)
def test_closed_but_unrelated_geometry_assets_refuse(geometry_assets, failure) -> None:
    directory, binding, atlas = geometry_assets
    source = directory / "sources/geometry"
    receipt_path = source / "geometry-receipt.json"
    receipt = json.loads(receipt_path.read_bytes())
    if failure == "pin":
        binding = binding.model_copy(update={"report_sha256": "0" * 64})
    elif failure == "report_run":
        report_path = source / "geometry-report.json"
        report = json.loads(report_path.read_bytes())
        report["run_sha256"] = "f" * 64
        report_path.write_text(json.dumps(report))
        pin = digest(report_path.read_bytes())
        binding = binding.model_copy(update={"report_sha256": pin})
        for entry in receipt["files"]:
            if entry["path"] == "geometry-report.json":
                entry.update(size=report_path.stat().st_size, sha256=pin)
    elif failure == "sdk":
        receipt["installed_sdk"]["commit"] = "f" * 40
    elif failure in {"corpus", "atlas_run"}:
        data = atlas.model_dump(mode="json")
        if failure == "corpus":
            data["corpus_pin"]["index_sha256"] = "f" * 64
        else:
            data["historical_review"]["run_sha256"] = "f" * 64
        atlas = AtlasReceipt.model_validate(data)
    elif failure == "membership":
        receipt["files"].pop()
    else:
        (directory / "source-footprint.png").write_bytes(b"unrelated graphic")
    if failure in {"report_run", "sdk", "membership"}:
        receipt_path.write_text(json.dumps(receipt))
        binding = binding.model_copy(update={"receipt_sha256": digest(receipt_path.read_bytes())})
    with pytest.raises(EvidenceError, match="geometry_asset"):
        verify_geometry_assets(directory, binding, atlas)
