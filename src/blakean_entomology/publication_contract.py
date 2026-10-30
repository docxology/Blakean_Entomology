"""Strict source custody shared by the application and compatible native worker."""

from pathlib import Path
from typing import Annotated, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

from .publication_wire import SDK_COMMIT, TEMPLATE_COMMIT, Member

SHA256 = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]


class Contract(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")


class PinnedInput(Contract):
    """One caller-held source pin; paths are explicit invocation inputs."""

    path: Path
    sha256: SHA256


class NativeRequest(Contract):
    """Join a closed preparation to its independently pinned graphical inputs."""

    schema_version: Literal[1] = 1
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
    sdk_commit: Literal["45171a099a6a658c52ab689501de646a28485653"] = SDK_COMMIT


class NativeStage(Contract):
    """The native worker's complete admitted source inventory."""

    schema_version: Literal[1] = 1
    template_commit: Literal["efce6d6f5b3c4e8e2bbf92d8250855a0a9389ae8"] = TEMPLATE_COMMIT
    sdk_commit: Literal["45171a099a6a658c52ab689501de646a28485653"] = SDK_COMMIT
    source_date_epoch: Literal[1793318400] = 1793318400
    template_sources: dict[str, SHA256]
    source_order: tuple[Literal["00_frontmatter.md", "10_article.md"], ...]
    request_sha256: SHA256
    inputs: tuple[Member, ...]
    sources: tuple[Member, ...]
    frontmatter_data_sha256: SHA256


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
    qualification: Literal["actual template writers; physical-page acceptance is separate"] = (
        "actual template writers; physical-page acceptance is separate"
    )
