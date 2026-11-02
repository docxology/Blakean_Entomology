"""Admit the existing analyses and selected Blake object for graphical abstracts."""

import hashlib
from dataclasses import dataclass
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field

from .atlas_models import AtlasReceipt
from .casebook import Casebook
from .composition import CompositionAudit
from .publication_contract import NativeRequest, PinnedInput
from .publication_transport_models import PublicationError
from .review_contexts import ContextAudit
from .visual_models import IllustratedEvidence, load_visuals


def pinned_bytes(source: PinnedInput) -> bytes:
    """Read one regular file and require its caller-held digest."""
    if source.path.is_symlink() or not source.path.is_file():
        raise PublicationError("source_file", str(source.path))
    raw = source.path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != source.sha256:
        raise PublicationError("source_pin", str(source.path))
    return raw


class Recto(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)
    sha256: str
    bytes: int = Field(ge=1)


class ObjectImages(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)
    museum_recto: Recto


class CoverObject(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)
    id: str
    accession: str
    title: str
    work: str
    copy_id: str = Field(alias="copy")
    catalogue_date: str
    creator: str
    credit: str
    source: str
    rights: str
    images: ObjectImages


class Provenance(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)
    objects: tuple[CoverObject, ...]
    current_selected_original_objects: int = Field(ge=1)


class DataPin(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)
    name: str
    sha256: str
    size: int = Field(ge=0)


class CompositionSidecar(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)
    atlas_sha256: str
    data: tuple[DataPin, ...]


@dataclass(frozen=True, slots=True)
class AbstractData:
    """Actual retained data, without adding contextual or biological decisions."""

    atlas: AtlasReceipt
    composition: CompositionAudit
    context: ContextAudit
    casebook: Casebook
    cover: CoverObject
    selected_originals: int
    visuals: IllustratedEvidence | None = None


def load_abstract_data(request: NativeRequest) -> AbstractData:
    """Require exact input and preparation/sidecar joins before drawing."""
    atlas = AtlasReceipt.model_validate_json(pinned_bytes(request.atlas))
    composition = CompositionAudit.model_validate_json(pinned_bytes(request.composition))
    book = Casebook.model_validate_json(pinned_bytes(request.casebook))
    provenance = Provenance.model_validate_json(pinned_bytes(request.cover_provenance))
    cover_raw = pinned_bytes(request.cover)
    candidates = tuple(
        obj for obj in provenance.objects if obj.images.museum_recto.sha256 == request.cover.sha256
    )
    if len(candidates) != 1 or candidates[0].images.museum_recto.bytes != len(cover_raw):
        raise PublicationError("cover_binding", str(request.cover.path))
    prepared = request.prepared.path.parent
    context = ContextAudit.model_validate_json(
        (prepared / "assets/context-review.json").read_bytes()
    )
    sidecar = CompositionSidecar.model_validate_json(
        (prepared / "assets/02-composition-influence.json").read_bytes()
    )
    matches = tuple(d for d in sidecar.data if d.name == "composition.json")
    if (
        context.summary.candidate_hits != atlas.candidates
        or sum(context.summary.decisions.values()) != context.summary.reviewed_hits
        or sidecar.atlas_sha256 != request.atlas.sha256
        or len(matches) != 1
        or matches[0].sha256 != request.composition.sha256
        or request.composition.path.stat().st_size != matches[0].size
        or sum(c.candidates for c in composition.categories) != composition.name_category_candidates
        or context.summary.reviewed_hits + context.summary.unreviewed_hits
        != context.summary.candidate_hits
    ):
        raise PublicationError("abstract_data_binding", str(prepared))
    return AbstractData(
        atlas,
        composition,
        context,
        book,
        candidates[0],
        provenance.current_selected_original_objects,
        load_visuals(prepared / "assets"),
    )
