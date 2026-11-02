"""Exclusive geometry epochs with complete before/after input and producer binding."""

import sys
from pathlib import Path
from typing import Literal

from blake.methods.installed import verify_installed_git
from blake.methods.installed_models import InstalledGitPackage
from blake.methods.models import Digest, FileReceipt
from blake.methods.runs import read_regular, reserve
from blake.methods.storage import publish_bytes, verify_file

from . import __version__
from .geometry import analyze_geometry
from .geometry_io import read_geometry_inputs, source_geometry_csv
from .geometry_models import GeometryModel, GeometryReport
from .geometry_producer import geometry_producers
from .models import EvidenceError
from .workflows import require_private_output


class GeometryReceipt(GeometryModel):
    schema_version: Literal[1] = 1
    application_version: str
    inputs: dict[str, Digest]
    producers: dict[str, Digest]
    files: tuple[FileReceipt, ...]
    python: str
    prefix: str
    base_prefix: str
    installed_sdk: InstalledGitPackage | None
    scope: str = (
        "Source-bound support analysis of one retained candidate/review run. An absent "
        "installed_sdk records source-only qualification. New reading, scientific, "
        "native manuscript and release acceptance require separate evidence."
    )


def publish_geometry(
    request_path: Path,
    expected_request_sha256: str,
    bundle: Path,
    run: Path,
    decisions: Path,
    windows: Path,
    vocabulary: Path,
    output: Path,
    *,
    figures: bool = False,
) -> GeometryReport:
    """Admit every input before reserving output; write the completion receipt last."""
    require_private_output(output, bundle)
    producers = geometry_producers(figures=figures)
    inputs = read_geometry_inputs(
        request_path, expected_request_sha256, bundle, run, decisions, windows, vocabulary
    )
    sdk_commit = inputs.request.sdk_commit
    sdk = verify_installed_git("blake", sdk_commit) if sdk_commit is not None else None
    report = analyze_geometry(
        inputs.passages,
        inputs.hits,
        inputs.decisions,
        inputs.windows,
        inputs.spec,
        run_sha256=inputs.request.run_sha256,
        illustrative_source_ids=inputs.request.illustrative_source_ids,
        window_pairs=inputs.request.window_pairs,
    )
    renderer = None
    if figures:
        from .geometry_figures import render_geometry_figures, validate_geometry_figures

        validate_geometry_figures(report)
        renderer = render_geometry_figures
    reserve(output)
    artifacts = [
        publish_bytes(output / "geometry-request.json", read_regular(request_path)),
        publish_bytes(
            output / "geometry-report.json", (report.model_dump_json(indent=2) + "\n").encode()
        ),
        publish_bytes(output / "geometry-sources.csv", source_geometry_csv(report)),
    ]
    if renderer is not None:
        artifacts.extend(renderer(report, output / "figures"))
    after = read_geometry_inputs(
        request_path, expected_request_sha256, bundle, run, decisions, windows, vocabulary
    )
    if inputs.input_hashes != after.input_hashes or producers != geometry_producers(
        figures=figures
    ):
        raise EvidenceError("geometry_source_changed", "Input or producer changed during export")
    if sdk is not None:
        final_sdk = verify_installed_git("blake", sdk.commit)
        if sdk.model_dump(exclude={"imported_modules"}) != final_sdk.model_dump(
            exclude={"imported_modules"}
        ):
            raise EvidenceError("geometry_sdk_changed", "Installed SDK changed during export")
        sdk = final_sdk
    for entry in artifacts:
        _ = verify_file(output, entry.path, entry.size, entry.sha256)
    receipt = GeometryReceipt(
        application_version=__version__,
        inputs=inputs.input_hashes,
        producers=producers,
        files=tuple(artifacts),
        python=sys.version,
        prefix=sys.prefix,
        base_prefix=sys.base_prefix,
        installed_sdk=sdk,
    )
    _ = publish_bytes(
        output / "geometry-receipt.json", (receipt.model_dump_json(indent=2) + "\n").encode()
    )
    return report
