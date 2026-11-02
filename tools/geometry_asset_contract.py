"""Join a new geometry epoch to its atlas and copied manuscript graphics."""

from pathlib import Path
from typing import Literal

from blake.methods.models import Digest, EvidenceError, FrozenModel
from blake.methods.runs import digest, read_regular
from blake.methods.storage import verify_file
from pydantic import TypeAdapter

from blakean_entomology.atlas_models import AtlasReceipt
from blakean_entomology.geometry_models import GeometryReport, GeometryRequest
from blakean_entomology.geometry_run import GeometryReceipt
from blakean_entomology.publication_profiles import CURRENT_SDK_COMMIT

CaptionName = Literal["source-footprint", "review-exposure"]
CaptionToken = Literal["GEOMETRY_SOURCE_CAPTION", "GEOMETRY_REVIEW_CAPTION"]
GEOMETRY_TOKENS = ("GEOMETRY_SOURCE_CAPTION", "GEOMETRY_REVIEW_CAPTION")


class GeometryAssetBinding(FrozenModel):
    """Caller-held byte identities; the source epoch stays in ignored custody."""

    request_sha256: Digest
    report_sha256: Digest
    receipt_sha256: Digest


def _pinned(directory: Path, name: str, expected: str) -> bytes:
    raw = read_regular(directory / name)
    if digest(raw) != expected:
        raise EvidenceError("geometry_asset_pin", name)
    return raw


def verify_geometry_epoch(
    source: Path, binding: GeometryAssetBinding, atlas: AtlasReceipt
) -> dict[CaptionToken, str]:
    """Refuse a closed but unrelated analysis before manuscript reservation."""
    request = GeometryRequest.model_validate_json(
        _pinned(source, "geometry-request.json", binding.request_sha256)
    )
    receipt = GeometryReceipt.model_validate_json(
        _pinned(source, "geometry-receipt.json", binding.receipt_sha256)
    )
    report = GeometryReport.model_validate_json(
        _pinned(source, "geometry-report.json", binding.report_sha256)
    )
    names = tuple(f.path for f in receipt.files)
    required = {
        "geometry-request.json",
        "geometry-report.json",
        "geometry-sources.csv",
        "figures/captions.json",
        "figures/plotting-runtime.json",
        *(
            f"figures/{name}.{suffix}"
            for name in ("source-footprint", "review-exposure")
            for suffix in ("png", "svg", "pdf")
        ),
    }
    if set(names) != required or len(names) != len(required):
        raise EvidenceError("geometry_asset_membership", "Require the complete figure epoch")
    paths = tuple(source.rglob("*"))
    if any(p.is_symlink() for p in paths) or {
        p.relative_to(source).as_posix() for p in paths if p.is_file()
    } != required | {"geometry-receipt.json"}:
        raise EvidenceError("geometry_asset_membership", "Unexpected geometry source member")
    for entry in receipt.files:
        _ = verify_file(source, entry.path, entry.size, entry.sha256)
    if (
        receipt.inputs.get("request") != binding.request_sha256
        or receipt.inputs.get("run") != request.run_sha256
        or receipt.inputs.get("bundle") != request.corpus_pin.bundle_manifest_sha256
        or receipt.inputs.get("decisions") != request.decisions_sha256
        or receipt.inputs.get("windows") != request.windows_sha256
        or receipt.inputs.get("vocabulary") != request.vocabulary_sha256
        or receipt.installed_sdk is None
        or receipt.installed_sdk.commit != request.sdk_commit
        or request.sdk_commit != CURRENT_SDK_COMMIT
        or receipt.installed_sdk.version != "0.7.0"
        or report.run_sha256 != request.run_sha256
    ):
        raise EvidenceError("geometry_asset_identity", "Request, report and producer differ")
    historical = atlas.historical_review
    if (
        request.corpus_pin != atlas.corpus_pin
        or historical is None
        or request.run_sha256 != historical.run_sha256
        or report.candidate_hits != atlas.candidates
        or report.primary.measure.records != atlas.primary_candidates
        or len(report.sources) != atlas.scanned_units
        or sum(c.measure.overlapping_pairs for c in report.cohorts)
        != atlas.overlapping_candidate_pairs
    ):
        raise EvidenceError("geometry_asset_atlas", "Geometry and retained atlas differ")
    measured = {(c.role, c.plane, c.author_id): c for c in report.cohorts}
    if len(measured) != len(report.cohorts) or set(measured) != {
        (c.role, c.plane, c.author_id) for c in atlas.cohorts
    }:
        raise EvidenceError("geometry_asset_cohorts", "Source facet membership differs")
    for cohort in atlas.cohorts:
        value = measured[cohort.role, cohort.plane, cohort.author_id]
        if (
            value.source_units != cohort.source_units
            or value.work_groups != cohort.work_groups
            or value.measure.records != sum(q.copy_retaining.occurrences for q in cohort.categories)
        ):
            raise EvidenceError("geometry_asset_cohorts", "Source facet denominator differs")
    captions = TypeAdapter(dict[CaptionName, str]).validate_json(
        read_regular(source / "figures/captions.json"), strict=True
    )
    if set(captions) != {"source-footprint", "review-exposure"}:
        raise EvidenceError("geometry_asset_captions", "Require both derived captions")
    return {
        "GEOMETRY_SOURCE_CAPTION": captions["source-footprint"],
        "GEOMETRY_REVIEW_CAPTION": captions["review-exposure"],
    }


def verify_geometry_assets(
    directory: Path, binding: GeometryAssetBinding, atlas: AtlasReceipt
) -> dict[CaptionToken, str]:
    """Also require every manuscript rendition to match the admitted source master."""
    source = directory / "sources/geometry"
    captions = verify_geometry_epoch(source, binding, atlas)
    for name in ("source-footprint", "review-exposure"):
        for suffix in ("png", "svg", "pdf"):
            if read_regular(directory / f"{name}.{suffix}") != read_regular(
                source / f"figures/{name}.{suffix}"
            ):
                raise EvidenceError("geometry_asset_figure", name)
    return captions
