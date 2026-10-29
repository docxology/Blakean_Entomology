"""Bounded reading receipts: transcription inspection is never image acceptance."""

from pathlib import Path
from typing import Literal, Self
from xml.etree import ElementTree as ET

from blake.methods.models import Digest, EvidenceError, FrozenModel
from blake.methods.runs import digest, read_regular
from pydantic import Field, model_validator

from .taxonomy_models import ReferenceSource


class ReadingSelection(FrozenModel):
    selection_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    object_id: str = Field(min_length=1)
    line_ids: tuple[str, ...]
    credit: Literal["complete_poem_transcription", "bounded_passage", "catalog_description"]
    selected_text_sha256: Digest
    locator: str = Field(min_length=1)
    limit: str = Field(min_length=1)


class ContextualCase(FrozenModel):
    case_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    selections: tuple[str, ...] = Field(min_length=1)
    interpretation: str = Field(min_length=1)
    rival_reading: str = Field(min_length=1)
    taxonomic_limit: str = Field(min_length=1)


class Casebook(FrozenModel):
    schema_version: Literal[1] = 1
    epoch: Literal["contextual-casebook-v1"] = "contextual-casebook-v1"
    sources: tuple[ReferenceSource, ...]
    selections: tuple[ReadingSelection, ...]
    cases: tuple[ContextualCase, ...]
    new_candidate_decisions: Literal[0] = 0
    whole_book_reading_credit: Literal[False] = False
    physical_images_inspected: Literal[False] = False

    @model_validator(mode="after")
    def case_membership(self) -> Self:
        sources = {s.source_id for s in self.sources}
        selections = {s.selection_id for s in self.selections}
        if len(sources) != len(self.sources) or len(selections) != len(self.selections):
            raise EvidenceError("casebook_duplicate", self.epoch)
        if len({c.case_id for c in self.cases}) != len(self.cases):
            raise EvidenceError("casebook_duplicate", self.epoch)
        if any(s.source_id not in sources for s in self.selections) or any(
            not set(c.selections).issubset(selections) for c in self.cases
        ):
            raise EvidenceError("casebook_membership", self.epoch)
        return self


def transcription_text(element: ET.Element) -> str:
    """Exclude inline editorial notes while preserving physical transcription tails."""
    return (element.text or "") + "".join(
        (transcription_text(child) if child.tag != "note" else "") + (child.tail or "")
        for child in element
    )


def selection_text(raw: bytes, selection: ReadingSelection) -> str:
    """Require exact ordered XML locators and truthful complete-poem boundaries."""
    root = ET.fromstring(raw)
    desc = next((d for d in root.findall(".//desc") if d.get("id") == selection.object_id), None)
    if desc is None:
        raise EvidenceError("reading_object", selection.object_id)
    if selection.credit == "catalog_description":
        if selection.line_ids:
            raise EvidenceError("catalog_lines", selection.selection_id)
        description = desc.find("illusdesc")
        if description is None:
            raise EvidenceError("reading_description", selection.object_id)
        return "".join(description.itertext())
    lines = tuple(desc.findall(".//phystext//l"))
    selected = tuple(e for e in lines if e.get("n") in selection.line_ids)
    if not selected or tuple(e.get("n") for e in selected) != selection.line_ids:
        raise EvidenceError("reading_lines", selection.selection_id)
    if selection.credit == "complete_poem_transcription":
        verse_ids = tuple(e.get("n") for e in desc.findall(".//phystext//lg/l"))
        if verse_ids != selection.line_ids:
            raise EvidenceError("incomplete_poem", selection.selection_id)
    return "\n".join(transcription_text(e) for e in selected)


def load_casebook(path: Path, sources: Path, expected_sha256: str) -> Casebook:
    """Verify every capture and selected-text hash without upgrading reading credit."""
    raw = read_regular(path)
    if digest(raw) != expected_sha256:
        raise EvidenceError("casebook_pin", str(path))
    casebook = Casebook.model_validate_json(raw)
    payloads: dict[str, bytes] = {}
    for source in casebook.sources:
        payload = read_regular(sources / source.filename)
        if digest(payload) != source.sha256 or len(payload) != source.size:
            raise EvidenceError("casebook_source_hash", source.source_id)
        payloads[source.source_id] = payload
    for selection in casebook.selections:
        text = selection_text(payloads[selection.source_id], selection)
        if digest(text.encode()) != selection.selected_text_sha256:
            raise EvidenceError("casebook_text_hash", selection.selection_id)
    return casebook
