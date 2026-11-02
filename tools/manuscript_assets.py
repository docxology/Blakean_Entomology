"""Typed admission of explicitly pinned manuscript assets and source ledgers."""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Literal

from blake.methods.models import Digest, EvidenceError, FileReceipt, FrozenModel
from blake.methods.runs import digest, read_regular, safe_directory
from blake.methods.storage import verify_file
from pydantic import ConfigDict, Field, model_validator

from tools.geometry_asset_contract import GEOMETRY_TOKENS, GeometryAssetBinding


class AssetFile(FileReceipt):
    """The shared receipt with strict boundary membership."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")


class AdditionalAssets(FrozenModel):
    """Explicit caller-pinned assets and their source/provenance closure."""

    schema_version: Literal[1, 2] = 1
    epoch: str = Field(min_length=1)
    atlas_sha256: Digest
    files: tuple[AssetFile, ...] = Field(min_length=1)
    image_paths: tuple[str, ...] = Field(min_length=1)
    source_files: tuple[AssetFile, ...] = Field(min_length=1)
    producer_receipts: tuple[str, ...] = Field(min_length=1)
    source_ledgers: tuple[str, ...] = Field(min_length=1)
    geometry_binding: GeometryAssetBinding | None = None
    replacements: dict[
        Literal[
            "NAME_COVERAGE_TABLE",
            "LITERAL_PAIR_TABLE",
            "CONTEXT_REVIEW_TABLE",
            "SOURCE_CHANNEL_TABLE",
            "CONTEXT_REVIEW_CAPTION",
            "CONTEXT_REVIEW_TOTAL",
            "CONTEXT_REVIEW_REMAINING",
            "CONTEXT_REVIEW_NEW",
            "SELECTED_IMAGE_WITNESSES",
            "GEOMETRY_SOURCE_CAPTION",
            "GEOMETRY_REVIEW_CAPTION",
        ],
        str,
    ] = Field(default_factory=dict)

    @model_validator(mode="after")
    def geometry_profile(self) -> "AdditionalAssets":
        if (self.schema_version == 2) != (self.geometry_binding is not None) or (
            self.geometry_binding is None
            and any(token in self.replacements for token in GEOMETRY_TOKENS)
        ):
            raise EvidenceError("geometry_asset_profile", "Geometry requires a schema-2 binding")
        return self


@dataclass(frozen=True, slots=True)
class AdditionalInput:
    """One optional additional directory bound to a caller-held manifest digest."""

    directory: Path
    sha256: str

    def load(self, atlas_sha256: str) -> AdditionalAssets:
        """Reject every unsafe or unbound member before output reservation."""
        safe_directory(self.directory)
        raw = read_regular(self.directory / "additional-assets.json")
        if digest(raw) != self.sha256:
            raise EvidenceError("additional_asset_pin", str(self.directory))
        manifest = AdditionalAssets.model_validate_json(raw)
        if manifest.atlas_sha256 != atlas_sha256:
            raise EvidenceError("additional_asset_binding", str(self.directory))
        names = [f.path for f in manifest.files]
        sources = [f.path for f in manifest.source_files]
        images = list(manifest.image_paths)
        if (
            len(set(names + sources)) != len(names + sources)
            or len(set(images)) != len(images)
            or not set(images).issubset(names)
            or any(
                not re.fullmatch(r"[a-z0-9][a-z0-9-]*\.(png|jpg|svg|pdf|csv|json)", n)
                for n in names
            )
            or any(not n.startswith("sources/") for n in sources)
            or any(not n.endswith((".png", ".jpg")) for n in images)
            or set(names)
            & {
                "retrieval-sensitivity.png",
                "invertebrate-reference.png",
                "invertebrate-reference.svg",
                "corpus-atlas.png",
                "corpus-atlas.svg",
            }
            or not set(manifest.producer_receipts + manifest.source_ledgers).issubset(sources)
            or len(set(manifest.producer_receipts)) != len(manifest.producer_receipts)
            or len(set(manifest.source_ledgers)) != len(manifest.source_ledgers)
        ):
            raise EvidenceError("additional_asset_membership", str(self.directory))
        for member in (*manifest.files, *manifest.source_files):
            _ = verify_file(self.directory, member.path, member.size, member.sha256)
        actual: set[str] = set()
        for path in self.directory.rglob("*"):
            if path.is_symlink():
                raise EvidenceError("additional_asset_symlink", str(path))
            if path.is_file():
                actual.add(path.relative_to(self.directory).as_posix())
        if actual != set(names + sources + ["additional-assets.json"]):
            raise EvidenceError("additional_asset_directory_membership", str(self.directory))
        return manifest


class PreparationReceipt(FrozenModel):
    schema_version: Literal[1] = 1
    atlas_sha256: Digest
    figures_sha256: Digest
    casebook_sha256: Digest
    reference_sha256: Digest
    manuscript_sha256: Digest
    bibliography_sha256: Digest
    generator_sha256: Digest
    presentation_sha256: Digest
    figure_tool_sha256: Digest
    files: tuple[FileReceipt, ...]
    helper_sources: tuple[FileReceipt, ...] = ()
    additional_assets_sha256: Digest | None = None
    additional_assets: AdditionalAssets | None = None
    qualification: Literal["prepared Markdown only; no native PDF or independent acceptance"] = (
        "prepared Markdown only; no native PDF or independent acceptance"
    )
