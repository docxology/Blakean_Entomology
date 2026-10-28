"""Real CLI and file-custody controls for the reciprocal workflows."""

import json
import subprocess
import sys
from pathlib import Path

import pytest
from blake.methods.proximity import ProximityGrid
from blake.methods.search_models import SearchRequest
from blake.studies import StudySpec, scan_passages
from test_application import inputs as inputs
from test_sensitivity import binding_for

from blakean_entomology.models import CorpusPin
from blakean_entomology.workflows import SensitivityReceipt, load_pinned_bundle, workspace_workflow


@pytest.fixture
def workflow_inputs(
    inputs, tmp_path, monkeypatch
) -> tuple[Path, CorpusPin, StudySpec, Path, Path, Path]:
    bundle, pin, spec, _output = inputs
    monkeypatch.chdir(tmp_path)
    pin_path = tmp_path / "pin.json"
    pin_path.write_text(pin.model_dump_json())
    binding_path = tmp_path / "binding.json"
    binding_path.write_text(binding_for(pin).model_dump_json())
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(spec.model_dump_json())
    return bundle, pin, spec, pin_path, binding_path, spec_path


def command_line(command, fixture, output) -> list[str]:
    bundle, _pin, _spec, pin_path, binding_path, spec_path = fixture
    options = (
        ["--pin", str(pin_path), "--vocabulary", str(spec_path)]
        if command == "sensitivity"
        else ["--binding", str(binding_path)]
    )
    return [
        sys.executable,
        "-m",
        "blakean_entomology.cli",
        command,
        "--bundle",
        str(bundle),
        *options,
        "--output",
        str(output),
    ]


@pytest.mark.parametrize("command", ["sensitivity", "proximity-study", "build-search-workspace"])
def test_cli_positive(workflow_inputs, tmp_path, command) -> None:
    output = (
        tmp_path
        / "analysis_output"
        / ("workspace" if command == "build-search-workspace" else "receipt.json")
    )
    result = subprocess.run(
        command_line(command, workflow_inputs, output), capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    if command == "build-search-workspace":
        assert "Blakean Entomology" in (output / "index.html").read_text()
        receipt = json.loads((output / "application-run.json").read_text())
        assert receipt["files"][0]["name"] == "search-manifest.json"
        assert len(receipt["application_code_sha256"]) == 64
    else:
        receipt = json.loads(output.read_text())
        assert len(receipt["application_code_sha256"]) == 64
        assert "context" not in receipt
        expected = (
            "nfkc-casefold-source-spans-v2"
            if command == "sensitivity"
            else "casefold-literal-source-spans-v1"
        )
        assert receipt["profile"]["semantics"]["profile"] == expected
    if command == "sensitivity":
        bundle, pin, spec, *_rest = workflow_inputs
        receipt = SensitivityReceipt.model_validate_json(output.read_bytes())
        assert (
            receipt.spec_sha256
            == scan_passages(load_pinned_bundle(bundle, pin).passages, spec).spec_sha256
        )
        assert receipt.statistics.units[0].tokens > 0


@pytest.mark.parametrize("command", ["sensitivity", "proximity-study", "build-search-workspace"])
@pytest.mark.parametrize("failure", ["wrong-pin", "occupied", "outside", "symlink"])
def test_cli_rejects_bad_custody(workflow_inputs, tmp_path, command, failure) -> None:
    output = tmp_path / "analysis_output" / "receipt.json"
    if failure == "wrong-pin":
        pin_file = workflow_inputs[3 if command == "sensitivity" else 4]
        record = json.loads(pin_file.read_text())
        target = record if command == "sensitivity" else record["projection_pin"]
        target["index_sha256"] = "0" * 64
        pin_file.write_text(json.dumps(record))
    elif failure == "occupied":
        output.parent.mkdir()
        output.write_bytes(b"retain")
    elif failure == "outside":
        output = tmp_path / "outside.json"
    else:
        output.parent.mkdir()
        destination = tmp_path / "untouched.json"
        destination.write_bytes(b"retain")
        output.symlink_to(destination)
    result = subprocess.run(
        command_line(command, workflow_inputs, output), capture_output=True, text=True
    )
    assert result.returncode != 0
    expected = {
        "wrong-pin": "corpus_pin_mismatch",
        "occupied": "occupied_output",
        "outside": "private_output_required",
        "symlink": "symlink_directory",
    }[failure]
    assert expected in result.stderr
    if failure in {"occupied", "symlink"}:
        assert output.read_bytes() == b"retain"
    else:
        assert not output.exists()


def test_cli_explicit_grid(workflow_inputs, tmp_path) -> None:
    output = tmp_path / "analysis_output" / "custom.json"
    grid_path = tmp_path / "grid.json"
    grid = ProximityGrid(
        requests=(
            SearchRequest(
                terms=("emmet", "bee"), mode="all", window_words=8, limit=1, context_chars=0
            ),
        )
    )
    grid_path.write_text(grid.model_dump_json())
    result = subprocess.run(
        [*command_line("proximity-study", workflow_inputs, output), "--grid", str(grid_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert len(json.loads(output.read_text())["study"]["rows"]) == 1


def test_output_cannot_modify_bundle(workflow_inputs, tmp_path) -> None:
    from blakean_entomology.workflows import require_private_output

    bundle = tmp_path / "analysis_output" / "bundle"
    bundle.mkdir(parents=True)
    with pytest.raises(ValueError, match="overlapping_output"):
        require_private_output(bundle / "new.json", bundle)


def test_workspace_revalidates_after_rendering_started(workflow_inputs, tmp_path) -> None:
    bundle, pin, *_rest = workflow_inputs
    output = tmp_path / "analysis_output" / "workspace"
    previous = sys.getprofile()
    events = []

    def corrupt_on_render(frame, event, arg) -> None:
        if event == "call" and frame.f_code.co_name == "unicode_search_tables":
            (bundle / "passages.jsonl").write_bytes(b"changed during rendering")
            events.append("corrupted")

    # Runtime tracing changes a real source file; no production callable is replaced.
    sys.setprofile(corrupt_on_render)
    try:
        with pytest.raises(ValueError, match="checksum"):
            workspace_workflow(bundle, binding_for(pin), output)
    finally:
        sys.setprofile(previous)
    assert events == ["corrupted"]
    assert not output.exists()
