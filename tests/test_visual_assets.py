"""Real source joins and complete-image publication, including refusing controls."""

import json
import shutil
from contextlib import chdir
from pathlib import Path

import matplotlib
import pytest
from blake.methods.models import FileReceipt, ResearchError
from PIL import Image

from blakean_entomology.casebook import ReadingSelection
from blakean_entomology.core import digest
from blakean_entomology.publication_transport_models import PublicationError
from blakean_entomology.visual_models import (
    IllustratedEvidence,
    VisualWitness,
    VisualWitnesses,
    load_visuals,
)
from tools.extend_visual_assets import VisualAssetRequest, extend_visual_assets
from tools.manuscript_assets import AdditionalAssets, AdditionalInput, AssetFile


@pytest.fixture
def visual_inputs(tmp_path) -> tuple[Path, Path]:
    parent = tmp_path / "parent"
    (parent / "sources").mkdir(parents=True)
    xml = (
        b'<root><desc id="poem"><phystext><lg><l n="1">A small life</l>'
        b'<l n="2">Calls for care.</l></lg></phystext></desc></root>'
    )
    (parent / "sources/poem.xml").write_bytes(xml)
    witnesses = []
    files = []
    for i, key in enumerate(("fly", "dream", "thel")):
        path = parent / f"sources/{key}.jpg"
        with Image.new("RGB", (90, 150), ("#ac792d", "#327c83", "#a8413c")[i]) as image:
            image.putpixel((5, 5), (255, 255, 255))
            image.save(path, quality=95)
        raw = path.read_bytes()
        image_receipt = FileReceipt(path=f"sources/{key}.jpg", size=len(raw), sha256=digest(raw))
        files.append(AssetFile(**image_receipt.model_dump()))
        witnesses.append(
            VisualWitness(
                key=key,
                title="Source-bound argument",
                source=FileReceipt(path="sources/poem.xml", size=len(xml), sha256=digest(xml)),
                selection=ReadingSelection(
                    selection_id=key,
                    source_id="poem",
                    object_id="poem",
                    line_ids=("1", "2"),
                    credit="bounded_passage",
                    selected_text_sha256=digest(b"A small life\nCalls for care."),
                    locator="Object poem, lines 1-2",
                    limit="Fixture selection only",
                ),
                quotation="A small life\nCalls for care.",
                image=image_receipt,
                image_name=f"{key}-recto.jpg",
                locator="Object poem, lines 1-2.",
                credit="Synthetic test image, not a Blake original.",
                citation_key="fixture-source",
                reading="An expressed need invites a response.",
                alternative="A response is not proof of arrival.",
                classification_limit="No animal identification follows.",
            )
        )
    xml_receipt = AssetFile(path="sources/poem.xml", size=len(xml), sha256=digest(xml))
    (parent / "sources/ledger.json").write_bytes(b"{}")
    files.extend((xml_receipt, AssetFile(path="sources/ledger.json", size=2, sha256=digest(b"{}"))))
    raw = (parent / "sources/fly.jpg").read_bytes()
    (parent / "existing.jpg").write_bytes(raw)
    manifest = AdditionalAssets(
        epoch="fixture",
        atlas_sha256="a" * 64,
        files=(AssetFile(path="existing.jpg", size=len(raw), sha256=digest(raw)),),
        image_paths=("existing.jpg",),
        source_files=tuple(files),
        producer_receipts=("sources/ledger.json",),
        source_ledgers=("sources/ledger.json",),
    )
    (parent / "additional-assets.json").write_text(manifest.model_dump_json())
    ledger = tmp_path / "visuals.json"
    ledger.write_text(VisualWitnesses(witnesses=tuple(witnesses)).model_dump_json())
    return parent, ledger


def visual_request(parent: Path, ledger: Path) -> VisualAssetRequest:
    return VisualAssetRequest.model_validate(
        {
            "parent": {
                "path": parent,
                "sha256": digest((parent / "additional-assets.json").read_bytes()),
            },
            "witnesses": {"path": ledger, "sha256": digest(ledger.read_bytes())},
            "atlas_sha256": "a" * 64,
        }
    )


@pytest.fixture
def admitted_visuals(visual_inputs, tmp_path) -> IllustratedEvidence:
    parent, ledger = visual_inputs
    output = tmp_path / "analysis_output/visuals"
    with chdir(tmp_path):
        extend_visual_assets(visual_request(parent, ledger), output)
    return load_visuals(output)


@pytest.fixture
def illustrated_font(tmp_path) -> Path:
    fonts = Path(matplotlib.get_data_path()) / "fonts/ttf"
    target = tmp_path / "fonts"
    target.mkdir()
    shutil.copy2(fonts / "DejaVuSans.ttf", target / "regular.ttf")
    shutil.copy2(fonts / "DejaVuSerif-Italic.ttf", target / "LiberationSerif-Italic.ttf")
    return target / "regular.ttf"


def test_actual_source_and_image_closure(admitted_visuals) -> None:
    evidence = admitted_visuals
    for witness in evidence.manifest.witnesses:
        assert (
            evidence.image(witness).read_bytes()
            == (evidence.directory / witness.image.path).read_bytes()
        )
        assert evidence.witness(witness.key) == witness
    manifest = evidence.directory / "additional-assets.json"
    closed = AdditionalInput(evidence.directory, digest(manifest.read_bytes())).load("a" * 64)
    assert len(closed.image_paths) == 1
    assert len(closed.files) == 5


@pytest.mark.parametrize(
    "failure",
    (
        "quote_digest",
        "quote_source",
        "membership",
        "image",
        "parent_pin",
        "ledger_pin",
        "occupied",
        "symlink",
    ),
)
def test_visual_admission_refuses_changed_inputs(visual_inputs, tmp_path, failure) -> None:
    parent, ledger = visual_inputs
    value = json.loads(ledger.read_bytes())
    if failure in ("quote_digest", "quote_source"):
        value["witnesses"][0]["quotation"] = "Invented words"
        if failure == "quote_source":
            value["witnesses"][0]["selection"]["selected_text_sha256"] = digest(b"Invented words")
        ledger.write_text(json.dumps(value))
    elif failure == "membership":
        value["witnesses"][0]["source"]["path"] = "sources/missing.xml"
        ledger.write_text(json.dumps(value))
    elif failure == "image":
        (parent / "sources/fly.jpg").write_bytes(b"broken")
    elif failure == "symlink":
        original = parent / "sources/fly.jpg"
        retained = tmp_path / "retained.jpg"
        original.rename(retained)
        original.symlink_to(retained)
    request = visual_request(parent, ledger)
    if failure in ("parent_pin", "ledger_pin"):
        field = "parent" if failure == "parent_pin" else "witnesses"
        request = request.model_copy(
            update={field: getattr(request, field).model_copy(update={"sha256": "0" * 64})}
        )
    output = tmp_path / "analysis_output/rejected"
    if failure == "occupied":
        output.mkdir(parents=True)
        (output / "retain.txt").write_text("retained")
    with chdir(tmp_path), pytest.raises((ResearchError, ValueError, PublicationError)):
        extend_visual_assets(request, output)
    assert not (output / "additional-assets.json").exists()
    if failure == "occupied":
        assert (output / "retain.txt").read_text() == "retained"


@pytest.mark.parametrize("failure", ("order", "duplicate_image"))
def test_visual_model_refuses_ambiguous_membership(visual_inputs, failure) -> None:
    _, ledger = visual_inputs
    value = json.loads(ledger.read_bytes())
    if failure == "order":
        value["witnesses"].reverse()
    else:
        value["witnesses"][1]["image_name"] = value["witnesses"][0]["image_name"]
    with pytest.raises((ResearchError, ValueError)):
        VisualWitnesses.model_validate(value)


def test_load_visuals_rejects_an_image_changed_after_admission(admitted_visuals) -> None:
    path = admitted_visuals.image(admitted_visuals.witness("fly"))
    path.write_bytes(b"changed")
    with pytest.raises((ResearchError, ValueError)):
        load_visuals(admitted_visuals.directory)
