"""Independent real-file/subprocess refusal controls for composition epochs.

Size policy (# noqa: SIZE_OK): user-owned real CLI suite includes publication and
malformed-input controls.
"""

import json
import subprocess
import sys
from pathlib import Path
from types import FrameType

import pytest
from blake.methods.runs import digest, verify_artifacts
from blake.studies import StudySpec
from test_application import inputs as inputs
from test_sensitivity import binding_for

from blakean_entomology.atlas import atlas_from_passages
from blakean_entomology.composition import CompositionAudit
from blakean_entomology.composition_workflow import (
    EXPORTS,
    CompositionInputs,
    CompositionRun,
    generate,
    table,
    verify_destination,
)
from blakean_entomology.models import CorpusPin
from blakean_entomology.workflows import (
    load_pinned_bundle,
    proximity_workflow,
    sensitivity_workflow,
)

TOOLS = Path(__file__).parents[1] / "tools"


@pytest.fixture
def composition_inputs(
    inputs: tuple[Path, CorpusPin, StudySpec, Path], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> CompositionInputs:
    bundle, pin, spec, _ = inputs
    spec = spec.model_copy(
        update={"terms": tuple(t.model_copy(update={"group": "insect"}) for t in spec.terms)}
    )
    monkeypatch.chdir(tmp_path)
    atlas = atlas_from_passages(load_pinned_bundle(bundle, pin).passages, spec, pin, "f" * 64)
    # Deliberately historical producer identities; replay must not relabel these bytes.
    raw = atlas.model_dump(mode="json")
    raw["application_code_sha256"] = "a" * 64
    raw["methods_sha256"] = "b" * 64
    atlas_path = tmp_path / "atlas.json"
    atlas_path.write_text(json.dumps(raw))
    pin_path = tmp_path / "pin.json"
    pin_path.write_text(pin.model_dump_json())
    vocabulary = tmp_path / "vocabulary.json"
    vocabulary.write_text(spec.model_dump_json())
    sensitivity = tmp_path / "analysis_output/sensitivity.json"
    proximity = tmp_path / "analysis_output/proximity.json"
    sensitivity_workflow(bundle, pin, spec, sensitivity)
    proximity_workflow(bundle, binding_for(pin), proximity)
    return CompositionInputs(
        atlas=atlas_path,
        atlas_sha256=digest(atlas_path.read_bytes()),
        sensitivity=sensitivity,
        bundle=bundle,
        pin=pin_path,
        vocabulary=vocabulary,
        proximity=proximity,
    )


def invoke(inputs: CompositionInputs, output: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "blakean_entomology.cli",
            "composition-audit",
            "--atlas",
            str(inputs.atlas),
            "--atlas-sha256",
            inputs.atlas_sha256,
            "--sensitivity",
            str(inputs.sensitivity),
            "--bundle",
            str(inputs.bundle),
            "--pin",
            str(inputs.pin),
            "--vocabulary",
            str(inputs.vocabulary),
            "--proximity",
            str(inputs.proximity),
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def plot(
    packet: Path, output: Path, expected: str | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(TOOLS / "build_composition_figures.py"),
            "--packet",
            str(packet),
            "--run-sha256",
            expected or digest((packet / "run.json").read_bytes()),
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def test_real_cli_roundtrip_and_independent_counts(
    composition_inputs: CompositionInputs, tmp_path: Path
) -> None:
    output = tmp_path / "analysis_output/new"
    before = composition_inputs.atlas.read_bytes()
    result = invoke(composition_inputs, output)
    assert result.returncode == 0, result.stderr
    run = CompositionRun.model_validate_json((output / "run.json").read_bytes())
    assert len(verify_artifacts(output, run.files, EXPORTS)) == 9
    audit = CompositionAudit.model_validate_json((output / "composition.json").read_bytes())
    # Two identical 9-token source copies: Emmet, bee, worm and fly each once.
    assert (audit.source_units, audit.tokens, audit.name_category_candidates) == (2, 18, 8)
    assert audit.work_groups == audit.nonempty_name_work_groups == 1
    assert audit.pooled_vs_equal_nonempty_tv == 0
    ant = next(c for c in audit.categories if c.category == "ant")
    assert (ant.candidates, ant.exact_text_candidates, ant.pooled_share) == (2, 1, 0.25)
    assert run.producer_epochs.historical_atlas_application == "a" * 64
    assert run.producer_epochs.current_atlas_application != "a" * 64
    assert "blake.methods/composition.py" in run.source_origin.code
    assert composition_inputs.atlas.read_bytes() == before
    assert invoke(composition_inputs, output).returncode != 0
    rendered = plot(output, tmp_path / "analysis_output/figures")
    assert rendered.returncode == 0, rendered.stderr
    figures = tmp_path / "analysis_output/figures"
    for png in figures.glob("*.png"):
        assert png.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    assert (
        len(list(figures.glob("*.png")))
        == len(list(figures.glob("*.svg")))
        == len(list(figures.glob("*.pdf")))
        == 4
    )
    manifest = json.loads((figures / "figures.json").read_bytes())
    for f in manifest["files"]:
        raw = (figures / f["path"]).read_bytes()
        assert len(raw) == f["size"] and digest(raw) == f["sha256"]
    assert plot(output, figures).returncode != 0


@pytest.mark.parametrize(
    "failure",
    [
        "atlas-pin",
        "malformed",
        "pin",
        "profile",
        "registry",
        "actual-counts",
        "actual-proximity",
        "source-bytes",
        "outside",
        "occupied",
        "symlink",
    ],
)
def test_real_cli_refuses_bad_inputs(
    composition_inputs: CompositionInputs, tmp_path: Path, failure: str
) -> None:
    i = composition_inputs
    out = tmp_path / "analysis_output/refused"
    if failure == "atlas-pin":
        i = i.model_copy(update={"atlas_sha256": "0" * 64})
    elif failure == "malformed":
        i.atlas.write_bytes(b"{malformed}")
        i = i.model_copy(update={"atlas_sha256": digest(i.atlas.read_bytes())})
    elif failure in ("pin", "profile", "registry", "actual-counts", "actual-proximity"):
        path = {
            "pin": i.pin,
            "profile": i.sensitivity,
            "registry": i.vocabulary,
            "actual-counts": i.sensitivity,
            "actual-proximity": i.proximity,
        }[failure]
        raw = json.loads(path.read_bytes())
        if failure == "pin":
            raw["index_sha256"] = "0" * 64
        elif failure == "profile":
            raw["profile"]["semantics"]["tokens"] = "false"
        elif failure == "registry":
            raw["terms"][0]["forms"] = ["changed"]
        elif failure == "actual-counts":
            raw["statistics"]["inventory_sha256"] = "0" * 64
        else:
            raw["study"]["scanned_source_units"] += 1
        path.write_text(json.dumps(raw))
    elif failure == "source-bytes":
        (i.bundle / "passages.jsonl").write_bytes(b"changed")
    elif failure == "outside":
        out = tmp_path / "outside"
    elif failure == "occupied":
        out.mkdir()
        (out / "sentinel").write_bytes(b"retain")
    else:
        target = tmp_path / "retained"
        target.mkdir()
        (target / "sentinel").write_bytes(b"retain")
        out.symlink_to(target, target_is_directory=True)
    result = invoke(i, out)
    assert result.returncode != 0, result.stdout
    if failure in ("occupied", "symlink"):
        assert (out / "sentinel").read_bytes() == b"retain"
    else:
        assert not out.exists()


@pytest.mark.parametrize(
    "failure", ["hash", "malformed", "duplicate", "unsafe", "data-hash", "data-shape"]
)
def test_real_plotter_refuses_before_publication(
    composition_inputs: CompositionInputs, tmp_path: Path, failure: str
) -> None:
    packet = tmp_path / "analysis_output/packet"
    generate(composition_inputs, packet, tmp_path / "analysis_output")
    expected = None
    raw = json.loads((packet / "run.json").read_bytes())
    if failure == "hash":
        expected = "0" * 64
    elif failure == "malformed":
        (packet / "run.json").write_bytes(b"{}")
    elif failure in ("duplicate", "unsafe"):
        if failure == "duplicate":
            raw["files"].append(raw["files"][0])
        else:
            raw["files"][0]["name"] = "../escape"
        (packet / "run.json").write_text(json.dumps(raw))
    else:
        member = packet / "name-work-matrix.csv"
        member.write_bytes(b"work_id,category\nmalformed,shape\n")
        if failure == "data-shape":
            entry = next(a for a in raw["files"] if a["name"] == member.name)
            entry.update(size=member.stat().st_size, sha256=digest(member.read_bytes()))
            (packet / "run.json").write_text(json.dumps(raw))
    out = tmp_path / "analysis_output/rejected-figure"
    result = plot(packet, out, expected)
    assert result.returncode != 0, result.stdout
    assert not out.exists()


def test_runtime_import_does_not_load_matplotlib() -> None:
    command = [
        sys.executable,
        "-c",
        "import blakean_entomology.cli,sys; assert 'matplotlib' not in sys.modules",
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr


def test_destination_overlaps_and_empty_table(tmp_path: Path) -> None:
    root = tmp_path / "owned"
    root.mkdir()
    for out, sources in (
        (root, ()),
        (root / "child", (root / "child/source",)),
        (root / "child", (root,)),
    ):
        with pytest.raises(ValueError):
            verify_destination(out, root, sources)
    with pytest.raises(ValueError):
        table(())


@pytest.mark.parametrize("phase", ["computation", "publication"])
def test_real_source_change_blocks_completion(
    composition_inputs: CompositionInputs, tmp_path: Path, phase: str
) -> None:
    output = tmp_path / "analysis_output" / "interrupted"
    previous = sys.getprofile()
    changed: list[str] = []

    def change_input(frame: FrameType, event: str, arg: None) -> None:
        trigger = "make_payloads" if phase == "computation" else "write_new"
        if event == "call" and frame.f_code.co_name == trigger and not changed:
            composition_inputs.pin.write_bytes(composition_inputs.pin.read_bytes() + b"\n")
            changed.append(phase)

    sys.setprofile(change_input)
    try:
        with pytest.raises(ValueError, match="composition_changed"):
            generate(composition_inputs, output, tmp_path / "analysis_output")
    finally:
        sys.setprofile(previous)
    assert changed == [phase]
    assert not (output / "run.json").exists()
    if phase == "computation":
        assert not output.exists()
    else:
        assert {p.name for p in output.iterdir()} == EXPORTS
