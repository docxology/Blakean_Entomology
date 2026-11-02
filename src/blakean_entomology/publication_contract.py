"""Strict source custody shared by the application and compatible native worker."""

from pathlib import Path
from typing import Annotated, ClassVar, Literal, Self

from blake.methods.installed_models import InstalledGitPackage
from pydantic import BaseModel, ConfigDict, Field, model_validator

from .publication_profiles import CURRENT_SDK_COMMIT, TEMPLATE_COMMIT, sdk_profile, sdk_version
from .publication_transport_models import Member

SHA256 = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]


class Contract(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")


class PinnedInput(Contract):
    """One caller-held source pin; paths are explicit invocation inputs."""

    path: Path
    sha256: SHA256


class NativeRequest(Contract):
    """Join a closed preparation to its independently pinned graphical inputs."""

    schema_version: Literal[1, 2, 3] = 3
    prepared: PinnedInput
    atlas: PinnedInput
    composition: PinnedInput
    casebook: PinnedInput
    cover: PinnedInput
    cover_provenance: PinnedInput
    config: PinnedInput
    preamble: PinnedInput
    web_css: PinnedInput
    template_commit: Literal["efce6d6f5b3c4e8e2bbf92d8250855a0a9389ae8"] = TEMPLATE_COMMIT
    sdk_commit: str = CURRENT_SDK_COMMIT

    @model_validator(mode="after")
    def selected_profile(self) -> Self:
        if not sdk_profile(self.schema_version, self.sdk_commit):
            raise ValueError("native_sdk_profile: schema and SDK selection differ")
        return self


class NativeStage(Contract):
    """The native worker's complete admitted source inventory."""

    schema_version: Literal[1, 2, 3] = 3
    template_commit: Literal["efce6d6f5b3c4e8e2bbf92d8250855a0a9389ae8"] = TEMPLATE_COMMIT
    sdk_commit: str = CURRENT_SDK_COMMIT
    sdk_identity: InstalledGitPackage | None = None
    source_date_epoch: Literal[1793318400] = 1793318400
    template_sources: dict[str, SHA256]
    source_order: tuple[Literal["00_frontmatter.md"], Literal["10_article.md"]]
    request_sha256: SHA256
    inputs: tuple[Member, ...]
    sources: tuple[Member, ...]
    frontmatter_data_sha256: SHA256

    @model_validator(mode="after")
    def selected_profile(self) -> Self:
        if not sdk_profile(self.schema_version, self.sdk_commit):
            raise ValueError("native_sdk_profile: schema and SDK selection differ")
        if self.schema_version == 1:
            if self.sdk_identity is not None:
                raise ValueError("native_sdk_identity: historical profile has no installed receipt")
        elif (
            self.sdk_identity is None
            or self.sdk_identity.commit != self.sdk_commit
            or self.sdk_identity.package != "blake"
            or self.sdk_identity.distribution != "blake"
            or self.sdk_identity.version != sdk_version(self.schema_version, self.sdk_commit)
        ):
            raise ValueError("native_sdk_identity: require the selected installed Blake receipt")
        return self


class NativeResult(Contract):
    """Observed writer/runtime/source results, before independent page acceptance."""

    template_commit: str
    template_sources: dict[str, str]
    imported_template_sources: dict[str, str]
    template_sources_unchanged: Literal[True] = True
    runtime_prefix: str
    runtime_base_prefix: str
    runtime_version: str
    writer_calls: tuple[str, str]
    semantic_preflight: str
    resolved_inputs: tuple[Member, ...]
    output_checks: tuple[Member, ...]
    outputs: tuple[Member, ...]
    pdf: str
    html: str
    declared_sdk_commit: str | None = None
    host_sdk_commit: str | None = None
    host_sdk_identity_sha256: str | None = None
    qualification: Literal["actual template writers; physical-page acceptance is separate"] = (
        "actual template writers; physical-page acceptance is separate"
    )
