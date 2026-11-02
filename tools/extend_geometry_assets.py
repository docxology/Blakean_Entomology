"""Extend a retained asset closure with a newly qualified geometry epoch."""

from pathlib import Path

import click
from blake.methods.models import EvidenceError, ResearchError
from blake.methods.runs import digest, read_regular, reserve
from blake.methods.storage import publish_bytes, verify_file

from blakean_entomology.atlas_models import AtlasReceipt
from blakean_entomology.workflows import require_private_output
from tools.geometry_asset_contract import (
    GeometryAssetBinding,
    verify_geometry_assets,
    verify_geometry_epoch,
)
from tools.manuscript_assets import AdditionalAssets, AdditionalInput, AssetFile


def extend_assets(
    original: AdditionalInput,
    geometry: Path,
    binding: GeometryAssetBinding,
    atlas_path: Path,
    atlas_sha256: str,
    output: Path,
) -> AdditionalAssets:
    """Verify both parents before writing; retain their original bytes and receipts."""
    for source in (original.directory, geometry, atlas_path):
        require_private_output(output, source)
    raw_atlas = read_regular(atlas_path)
    if digest(raw_atlas) != atlas_sha256:
        raise EvidenceError("geometry_asset_atlas_pin", str(atlas_path))
    atlas = AtlasReceipt.model_validate_json(raw_atlas)
    prior = original.load(atlas_sha256)
    captions = verify_geometry_epoch(geometry, binding, atlas)
    payloads = {
        f.path: read_regular(verify_file(original.directory, f.path, f.size, f.sha256))
        for f in (*prior.files, *prior.source_files)
    }
    additions = {
        "sources/geometry/" + p.relative_to(geometry).as_posix(): read_regular(p)
        for p in geometry.rglob("*")
        if p.is_file()
    }
    if any(p.is_symlink() for p in geometry.rglob("*")):
        raise EvidenceError("geometry_asset_symlink", str(geometry))
    additions.update(
        (f"{name}.{suffix}", read_regular(geometry / f"figures/{name}.{suffix}"))
        for name in ("source-footprint", "review-exposure")
        for suffix in ("png", "svg", "pdf")
    )
    additions["sources/geometry-parent-assets.json"] = read_regular(
        original.directory / "additional-assets.json"
    )
    if set(payloads) & set(additions):
        raise EvidenceError("geometry_asset_collision", "Retain a new noncolliding asset epoch")
    if prior.geometry_binding is not None:
        raise EvidenceError("geometry_asset_parent", "Select the original nongeometry parent")
    reserve(output)
    files: list[AssetFile] = []
    sources: list[AssetFile] = []
    for name, raw in {**payloads, **additions}.items():
        written = publish_bytes(output / name, raw)
        entry = AssetFile(path=name, size=written.size, sha256=written.sha256)
        (sources if name.startswith("sources/") else files).append(entry)
    manifest = AdditionalAssets(
        schema_version=2,
        epoch="manuscript-geometry-20261101-v1",
        atlas_sha256=atlas_sha256,
        files=tuple(files),
        source_files=tuple(sources),
        image_paths=(*prior.image_paths, "source-footprint.png", "review-exposure.png"),
        producer_receipts=(*prior.producer_receipts, "sources/geometry/geometry-receipt.json"),
        source_ledgers=(*prior.source_ledgers, "sources/geometry/geometry-request.json"),
        replacements={**prior.replacements, **captions},
        geometry_binding=binding,
    )
    _ = original.load(atlas_sha256)
    _ = verify_geometry_epoch(geometry, binding, atlas)
    if read_regular(atlas_path) != raw_atlas:
        raise EvidenceError("geometry_asset_source_changed", str(atlas_path))
    _ = verify_geometry_assets(output, binding, atlas)
    for entry in (*files, *sources):
        _ = verify_file(output, entry.path, entry.size, entry.sha256)
    _ = publish_bytes(
        output / "additional-assets.json", (manifest.model_dump_json(indent=2) + "\n").encode()
    )
    _ = AdditionalInput(output, digest((output / "additional-assets.json").read_bytes())).load(
        atlas_sha256
    )
    return manifest


@click.command()
@click.option("--original", type=click.Path(path_type=Path), required=True)
@click.option("--original-sha256", required=True)
@click.option("--geometry", type=click.Path(path_type=Path), required=True)
@click.option("--request-sha256", required=True)
@click.option("--report-sha256", required=True)
@click.option("--receipt-sha256", required=True)
@click.option("--atlas", "atlas_path", type=click.Path(path_type=Path), required=True)
@click.option("--atlas-sha256", required=True)
@click.option("--output", type=click.Path(path_type=Path), required=True)
def main(
    original: Path,
    original_sha256: str,
    geometry: Path,
    request_sha256: str,
    report_sha256: str,
    receipt_sha256: str,
    atlas_path: Path,
    atlas_sha256: str,
    output: Path,
) -> None:
    """Close two retained parents into one unused private preparation input."""
    try:
        result = extend_assets(
            AdditionalInput(original, original_sha256),
            geometry,
            GeometryAssetBinding(
                request_sha256=request_sha256,
                report_sha256=report_sha256,
                receipt_sha256=receipt_sha256,
            ),
            atlas_path,
            atlas_sha256,
            output,
        )
    except (OSError, ValueError, ResearchError) as error:
        raise click.ClickException(str(error)) from error
    click.echo(f"{len(result.image_paths)} manuscript images; no new original-image readings.")


if __name__ == "__main__":
    main()
