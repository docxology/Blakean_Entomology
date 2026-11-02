"""Source-specific quotation and complete-image bindings for illustrated arguments."""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Self

from blake.methods.models import EvidenceError, FileReceipt, FrozenModel
from blake.methods.runs import digest, read_regular
from blake.methods.storage import verify_file
from pydantic import Field, model_validator

from .casebook import ReadingSelection

WitnessKey = Literal["fly", "dream", "thel"]


class VisualWitness(FrozenModel):
    """One image/text association; it makes no zoological identification."""

    key: WitnessKey
    title: str = Field(min_length=1)
    source: FileReceipt
    selection: ReadingSelection
    quotation: str = Field(min_length=1)
    image: FileReceipt
    image_name: str = Field(pattern=r"^[a-z][a-z-]+\.jpg$")
    locator: str = Field(min_length=1)
    credit: str = Field(min_length=1)
    citation_key: str = Field(pattern=r"^[a-z][a-z0-9-]+$")
    reading: str = Field(min_length=1)
    alternative: str = Field(min_length=1)
    classification_limit: str = Field(min_length=1)

    @model_validator(mode="after")
    def quotation_identity(self) -> Self:
        if digest(self.quotation.encode()) != self.selection.selected_text_sha256:
            raise EvidenceError("visual_quotation_digest", self.key)
        return self


class VisualWitnesses(FrozenModel):
    schema_version: Literal[1] = 1
    epoch: Literal["illustrated-arguments-20261102"] = "illustrated-arguments-20261102"
    witnesses: tuple[VisualWitness, ...]
    new_candidate_decisions: Literal[0] = 0
    new_taxonomic_identifications: Literal[0] = 0

    @model_validator(mode="after")
    def exact_membership(self) -> Self:
        if tuple(w.key for w in self.witnesses) != ("fly", "dream", "thel"):
            raise EvidenceError("visual_witness_membership", self.epoch)
        if len({w.image_name for w in self.witnesses}) != len(self.witnesses):
            raise EvidenceError("visual_image_membership", self.epoch)
        return self


@dataclass(frozen=True, slots=True)
class IllustratedEvidence:
    """Admitted source-specific records and their complete reproduced images."""

    directory: Path
    manifest: VisualWitnesses

    def witness(self, key: WitnessKey) -> VisualWitness:
        return next(w for w in self.manifest.witnesses if w.key == key)

    def image(self, witness: VisualWitness) -> Path:
        return self.directory / witness.image_name


def load_visuals(assets: Path) -> IllustratedEvidence:
    """Admit every image before a graphical-abstract producer can use it."""
    manifest = VisualWitnesses.model_validate_json(read_regular(assets / "visual-witnesses.json"))
    for witness in manifest.witnesses:
        _ = verify_file(assets, witness.image_name, witness.image.size, witness.image.sha256)
    return IllustratedEvidence(assets, manifest)
