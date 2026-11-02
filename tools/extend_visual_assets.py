#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["click>=8.1", "pydantic==2.11.9"]
# ///
# ─── How to run ───
# Use the locked application environment: uv run --no-sync python -m tools.extend_visual_assets
# Supply --request, its independently held --request-sha256, and an unused --output.
# ──────────────────
"""Close exact quotations and original images into a new illustrated asset epoch."""

import json
from pathlib import Path

import click
from blake.methods.models import Digest, EvidenceError, FrozenModel, ResearchError
from blake.methods.runs import digest, read_regular, reserve
from blake.methods.storage import publish_bytes, verify_file
from PIL import Image

from blakean_entomology.casebook import selection_text
from blakean_entomology.publication_contract import PinnedInput
from blakean_entomology.publication_data import pinned_bytes
from blakean_entomology.publication_transport_models import PublicationError
from blakean_entomology.visual_models import VisualWitnesses
from blakean_entomology.workflows import require_private_output
from tools.manuscript_assets import AdditionalAssets, AdditionalInput, AssetFile


class VisualAssetRequest(FrozenModel):
    parent: PinnedInput
    witnesses: PinnedInput
    atlas_sha256: Digest


def extend_visual_assets(request: VisualAssetRequest, output: Path) -> AdditionalAssets:
    """Verify primary text/image joins before reserving or writing output."""
    original = AdditionalInput(request.parent.path, request.parent.sha256)
    prior = original.load(request.atlas_sha256)
    ledger_raw = pinned_bytes(request.witnesses)
    witnesses = VisualWitnesses.model_validate_json(ledger_raw)
    require_private_output(output, request.parent.path)
    require_private_output(output, request.witnesses.path)
    payloads = {
        item.path: read_regular(verify_file(original.directory, item.path, item.size, item.sha256))
        for item in (*prior.files, *prior.source_files)
    }
    additions: dict[str, bytes] = {"visual-witnesses.json": ledger_raw}
    known_sources = {entry.path for entry in prior.source_files}
    for witness in witnesses.witnesses:
        if witness.source.path not in known_sources or witness.image.path not in known_sources:
            raise EvidenceError("visual_parent_membership", witness.key)
        source = verify_file(
            original.directory,
            witness.source.path,
            witness.source.size,
            witness.source.sha256,
        )
        if selection_text(read_regular(source), witness.selection) != witness.quotation:
            raise EvidenceError("visual_quotation_source", witness.key)
        image = verify_file(
            original.directory, witness.image.path, witness.image.size, witness.image.sha256
        )
        with Image.open(image) as captured:
            captured.verify()
        additions[witness.image_name] = read_regular(image)
    additions["sources/visual-revision/visual-witnesses.json"] = ledger_raw
    additions["sources/visual-revision/parent-additional-assets.json"] = read_regular(
        original.directory / "additional-assets.json"
    )
    producer_paths = (
        Path(__file__),
        Path(__file__).parents[1] / "src/blakean_entomology/visual_models.py",
        Path(__file__).parents[1] / "src/blakean_entomology/casebook.py",
    )
    for source in producer_paths:
        additions["sources/visual-revision/producer/" + source.name] = read_regular(source)
    producer = {
        "parent_sha256": request.parent.sha256,
        "witnesses_sha256": request.witnesses.sha256,
        "atlas_sha256": request.atlas_sha256,
        "selected_witnesses": [w.key for w in witnesses.witnesses],
        "new_candidate_decisions": 0,
        "scope": "Exact selected-text and whole-image reuse; no new biological identification",
    }
    additions["sources/visual-revision/production.json"] = (
        json.dumps(producer, indent=2) + "\n"
    ).encode()
    if set(payloads) & set(additions):
        raise EvidenceError("visual_asset_collision", "Use the pre-illustration parent closure")
    reserve(output)
    files: list[AssetFile] = []
    sources: list[AssetFile] = []
    for name, raw in {**payloads, **additions}.items():
        entry = publish_bytes(output / name, raw)
        target = sources if name.startswith("sources/") else files
        target.append(AssetFile(path=name, size=entry.size, sha256=entry.sha256))
    manifest = AdditionalAssets(
        schema_version=prior.schema_version,
        epoch="illustrated-arguments-20261102",
        atlas_sha256=prior.atlas_sha256,
        files=tuple(files),
        source_files=tuple(sources),
        image_paths=prior.image_paths,
        producer_receipts=(
            *prior.producer_receipts,
            "sources/visual-revision/production.json",
        ),
        source_ledgers=(
            *prior.source_ledgers,
            "sources/visual-revision/visual-witnesses.json",
        ),
        geometry_binding=prior.geometry_binding,
        replacements=prior.replacements,
    )
    _ = original.load(request.atlas_sha256)
    if pinned_bytes(request.witnesses) != ledger_raw:
        raise EvidenceError("visual_ledger_changed", str(request.witnesses.path))
    for entry in (*manifest.files, *manifest.source_files):
        _ = verify_file(output, entry.path, entry.size, entry.sha256)
    _ = publish_bytes(
        output / "additional-assets.json",
        (manifest.model_dump_json(indent=2) + "\n").encode(),
    )
    _ = AdditionalInput(output, digest(read_regular(output / "additional-assets.json"))).load(
        request.atlas_sha256
    )
    return manifest


@click.command()
@click.option("--request", "request_path", type=click.Path(path_type=Path), required=True)
@click.option("--request-sha256", required=True)
@click.option("--output", type=click.Path(path_type=Path), required=True)
def main(request_path: Path, request_sha256: str, output: Path) -> None:
    """Publish one independently pinned visual-input closure."""
    try:
        raw = pinned_bytes(PinnedInput(path=request_path, sha256=request_sha256))
        request = VisualAssetRequest.model_validate_json(raw)
        result = extend_visual_assets(request, output)
    except (OSError, ValueError, ResearchError, PublicationError) as error:
        raise click.ClickException(str(error)) from error
    click.echo(f"{len(result.files)} assets; three source-specific illustrated arguments.")


if __name__ == "__main__":
    main()
