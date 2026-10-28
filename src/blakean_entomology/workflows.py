"""Private, immutable application receipts for reciprocal shared-method workflows."""

import json
from pathlib import Path
from typing import Literal

from blake.applications import ApplicationBundle, load_bundle
from blake.methods.compatibility import bundle_to_projection
from blake.methods.models import Artifact, Digest, FrozenModel
from blake.methods.profiles import RetrievalProfile, RuntimeProfile, runtime_profile
from blake.methods.proximity import ProximityGrid, ProximityStudy
from blake.methods.runs import digest, safe_directory, write_new
from blake.methods.statistics_models import CountedStatistics
from blake.methods.workspace import WorkspaceBranding, build_search_workspace_passages
from blake.studies import StudySpec

from . import __version__
from .models import CorpusPin, EvidenceError
from .producer import application_code_sha256
from .sensitivity import (
    ProximityBinding,
    analyze_sensitivity,
    literal_proximity_from_bundle,
    load_proximity_bundle,
)


class SensitivityReceipt(FrozenModel):
    schema_version: Literal[1] = 1
    application_version: str
    application_code_sha256: Digest
    corpus_pin: CorpusPin
    spec_sha256: Digest
    profile: RuntimeProfile
    statistics: CountedStatistics
    eligibility: Literal["Blake-author primary reading units"] = (
        "Blake-author primary reading units"
    )


class ProximityReceipt(FrozenModel):
    schema_version: Literal[1] = 1
    application_version: str
    application_code_sha256: Digest
    binding: ProximityBinding
    profile: RuntimeProfile
    study: ProximityStudy


class WorkspaceReceipt(FrozenModel):
    schema_version: Literal[1] = 1
    application_version: str
    application_code_sha256: Digest
    binding: ProximityBinding
    files: tuple[Artifact, ...]


def require_private_output(output: Path, bundle: Path) -> None:
    """Confine new workflow outputs to this application's private analysis tree."""
    safe_directory(output)
    root = Path.cwd() / "analysis_output"
    if ".." in output.parts or not output.absolute().is_relative_to(root):
        raise EvidenceError("private_output_required", str(root))
    source = bundle.resolve()
    target = output.resolve()
    if source.is_relative_to(target) or target.is_relative_to(source):
        raise EvidenceError("overlapping_output", str(output))
    if output.exists():
        raise EvidenceError("occupied_output", str(output))


def load_pinned_bundle(bundle: Path, pin: CorpusPin) -> ApplicationBundle:
    """Verify all portable bundle receipts and the trusted application corpus pin."""
    snapshot = load_bundle(bundle, pin.bundle_manifest_sha256)
    manifest = snapshot.manifest
    if (
        manifest.captured_manifest_sha256 != pin.captured_manifest_sha256
        or manifest.projection_manifest_sha256 != pin.projection_manifest_sha256
        or manifest.index_sha256 != pin.index_sha256
    ):
        raise EvidenceError("corpus_pin_mismatch", str(bundle))
    return snapshot


def sensitivity_workflow(
    bundle: Path, pin: CorpusPin, spec: StudySpec, output: Path
) -> SensitivityReceipt:
    """Publish a text-free, source-bound NFKC count sensitivity receipt."""
    require_private_output(output, bundle)
    snapshot = load_pinned_bundle(bundle, pin)
    registry = json.dumps(
        spec.model_dump(mode="json"), sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode()
    receipt = SensitivityReceipt(
        application_version=__version__,
        application_code_sha256=application_code_sha256(),
        corpus_pin=pin,
        spec_sha256=digest(registry),
        profile=runtime_profile(RetrievalProfile.NFKC_TOKENS_V2),
        statistics=analyze_sensitivity(snapshot.passages, spec),
    )
    _ = load_pinned_bundle(bundle, pin)
    _ = write_new(output, (receipt.model_dump_json(indent=2) + "\n").encode())
    return receipt


def proximity_workflow(
    bundle: Path, binding: ProximityBinding, output: Path, grid: ProximityGrid | None = None
) -> ProximityReceipt:
    """Publish literal proximity under its own explicitly distinct profile."""
    require_private_output(output, bundle)
    study = literal_proximity_from_bundle(bundle, binding, grid)
    receipt = ProximityReceipt(
        application_version=__version__,
        application_code_sha256=application_code_sha256(),
        binding=binding,
        profile=runtime_profile(RetrievalProfile.LITERAL_CASEFOLD_V1),
        study=study,
    )
    _ = load_proximity_bundle(bundle, binding)
    _ = write_new(output, (receipt.model_dump_json(indent=2) + "\n").encode())
    return receipt


def workspace_workflow(bundle: Path, binding: ProximityBinding, output: Path) -> Path:
    """Publish a private offline workspace after a final full bundle revalidation."""
    require_private_output(output, bundle)
    snapshot = load_proximity_bundle(bundle, binding)

    def revalidate() -> None:
        _ = load_proximity_bundle(bundle, binding)

    producer = application_code_sha256()
    index = build_search_workspace_passages(
        bundle_to_projection(snapshot.passages),
        binding.projection_pin,
        output,
        branding=WorkspaceBranding(
            title="Blakean Entomology — private source search",
            brand="Blakean Entomology",
            footer="Private source-bound workspace",
        ),
        producer_version=__version__,
        private_output_root=Path.cwd() / "analysis_output",
        revalidate=revalidate,
    )
    artifacts = tuple(
        Artifact(
            name=name,
            size=(output / name).stat().st_size,
            sha256=digest((output / name).read_bytes()),
        )
        for name in ("search-manifest.json",)
    )
    receipt = WorkspaceReceipt(
        application_version=__version__,
        application_code_sha256=producer,
        binding=binding,
        files=artifacts,
    )
    _ = write_new(
        output / "application-run.json", (receipt.model_dump_json(indent=2) + "\n").encode()
    )
    return index
