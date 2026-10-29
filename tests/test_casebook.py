"""Complete-poem credit requires every physical verse line, never search hits."""

import json
import shutil

import pytest
from pydantic import ValidationError
from test_taxonomy import SOURCES, STAGE

from blakean_entomology.casebook import Casebook, load_casebook, selection_text
from blakean_entomology.core import digest
from blakean_entomology.models import EvidenceError

LEDGER = STAGE / "research/reading-ledger-advancement-v1.json"


@pytest.fixture
def casebook() -> Casebook:
    return load_casebook(LEDGER, SOURCES, digest(LEDGER.read_bytes()))


def test_complete_poems_are_actually_present(casebook) -> None:
    # Given the captured copy-specific primary texts and read selection ledger.
    poems = tuple(s for s in casebook.selections if s.credit == "complete_poem_transcription")
    # When their exact line selections are counted.
    sizes = {s.selection_id: len(s.line_ids) for s in poems}
    # Then only four bounded short-poem transcriptions receive full-poem credit.
    assert sizes == {"dream": 20, "fly": 20, "human-abstract": 24, "sick-rose": 8}
    assert len(casebook.cases) == 7
    assert casebook.whole_book_reading_credit is False
    assert casebook.physical_images_inspected is False
    assert casebook.new_candidate_decisions == 0


@pytest.mark.parametrize(
    "mutation", ["object", "lines", "incomplete", "catalog_lines", "description"]
)
def test_rejects_false_selection_credit(casebook, mutation) -> None:
    # Given one intentionally invalid selection in a real retained capture.
    selection = casebook.selections[0]
    if mutation == "object":
        selection = selection.model_copy(update={"object_id": "missing"})
    elif mutation == "lines":
        selection = selection.model_copy(update={"line_ids": ("missing",)})
    elif mutation == "incomplete":
        selection = selection.model_copy(update={"line_ids": selection.line_ids[:-1]})
    elif mutation == "catalog_lines":
        selection = selection.model_copy(update={"credit": "catalog_description"})
    else:
        selection = selection.model_copy(update={"credit": "catalog_description", "line_ids": ()})
        raw = b'<bad><desc id="songsie.a.illbk.27"/></bad>'
    raw = raw if mutation == "description" else (SOURCES / "songsie.a.xml").read_bytes()
    # When extracting the declared textual evidence.
    with pytest.raises(EvidenceError):
        selection_text(raw, selection)
    # Then missing material cannot be described as a complete read.


@pytest.mark.parametrize("mutation", ["hash", "text_hash", "pin"])
def test_rejects_changed_reading_sources(casebook, tmp_path, mutation) -> None:
    # Given independent copies and an explicit trusted ledger pin.
    directory = tmp_path / "sources"
    directory.mkdir()
    for source in casebook.sources:
        shutil.copyfile(SOURCES / source.filename, directory / source.filename)
    raw = casebook.model_dump(mode="json")
    if mutation == "hash":
        with (directory / "songsie.a.xml").open("ab") as handle:
            _ = handle.write(b"changed")
    elif mutation == "text_hash":
        raw["selections"][0]["selected_text_sha256"] = "0" * 64
    path = tmp_path / "ledger.json"
    path.write_text(json.dumps(raw))
    expected = "0" * 64 if mutation == "pin" else digest(path.read_bytes())
    # When reading the casebook.
    with pytest.raises(EvidenceError):
        load_casebook(path, directory, expected)
    # Then read credit cannot survive byte drift.


@pytest.mark.parametrize("mutation", ["source", "selection", "duplicate", "case", "credit"])
def test_rejects_casebook_membership(casebook, mutation) -> None:
    # Given a ledger with a false membership or promoted reading credit.
    raw = casebook.model_dump(mode="json")
    if mutation == "source":
        raw["selections"][0]["source_id"] = "missing"
    elif mutation == "selection":
        raw["cases"][0]["selections"] = ["missing"]
    elif mutation == "duplicate":
        raw["selections"].append(raw["selections"][0])
    elif mutation == "case":
        raw["cases"].append(raw["cases"][0])
    else:
        raw["physical_images_inspected"] = True
    # When parsed at the evidence boundary.
    with pytest.raises(ValidationError):
        Casebook.model_validate(raw)
    # Then no unbound interpretation enters the casebook.
