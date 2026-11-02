"""Real pinned files and command controls for the geometry producer."""

import json
import subprocess
import sys
from contextlib import chdir
from pathlib import Path

import pytest
from blake.methods.runs import digest
from blake.methods.storage import verify_file
from blake.studies import StudySpec
from test_application import inputs as inputs

from blakean_entomology.core import analyze, load_run
from blakean_entomology.geometry_io import source_geometry_csv
from blakean_entomology.geometry_models import GeometryReport, GeometryRequest
from blakean_entomology.geometry_run import GeometryReceipt, publish_geometry
from blakean_entomology.models import Decision, ReviewDecision
from blakean_entomology.workflows import load_pinned_bundle


@pytest.fixture
def geometry_files(inputs, tmp_path: Path) -> dict[str, Path]:
    bundle, pin, original_spec, run = inputs
    spec = StudySpec.model_validate(
        original_spec.model_dump()
        | {"terms": tuple(t.model_dump() | {"group": "insect"} for t in original_spec.terms)}
    )
    _ = analyze(bundle, pin, spec, run)
    run_sha = digest((run / "run.json").read_bytes())
    _receipt, _summary, hits = load_run(run, run_sha)
    hit = hits[0]
    source = next(
        p for p in load_pinned_bundle(bundle, pin).passages if p.passage_id == hit.passage_id
    )
    decisions, windows, vocabulary, request = (
        tmp_path / name
        for name in ("decisions.jsonl", "windows.json", "vocabulary.json", "request.json")
    )
    decision = ReviewDecision(
        run_sha256=run_sha,
        hit_id=hit.hit_id,
        decision=Decision.UNCERTAIN,
        reviewer="Synthetic reviewer",
        rationale="Synthetic control",
    )
    _ = decisions.write_text(decision.model_dump_json() + "\n")
    _ = windows.write_text(
        json.dumps(
            [
                {
                    "batch_id": "event-a",
                    "hit": hit.model_dump(mode="json"),
                    "window_start": 0,
                    "window_end": len(source.text),
                    "window_sha256": digest(source.text.encode()),
                    "text": source.text,
                }
            ]
        )
    )
    _ = vocabulary.write_text(spec.model_dump_json())
    data = GeometryRequest(
        corpus_pin=pin,
        run_sha256=run_sha,
        decisions_sha256=digest(decisions.read_bytes()),
        windows_sha256=digest(windows.read_bytes()),
        vocabulary_sha256=digest(vocabulary.read_bytes()),
    )
    _ = request.write_text(data.model_dump_json())
    return {
        "bundle": bundle,
        "run": run,
        "decisions": decisions,
        "windows": windows,
        "vocabulary": vocabulary,
        "request": request,
        "output": tmp_path / "analysis_output/geometry",
    }


def test_library_emits_complete_source_bound_geometry(geometry_files, tmp_path: Path) -> None:
    paths = geometry_files
    with chdir(tmp_path):
        report = publish_geometry(
            paths["request"],
            digest(paths["request"].read_bytes()),
            paths["bundle"],
            paths["run"],
            paths["decisions"],
            paths["windows"],
            paths["vocabulary"],
            paths["output"],
        )
    receipt = GeometryReceipt.model_validate_json(
        (paths["output"] / "geometry-receipt.json").read_bytes()
    )
    assert receipt.installed_sdk is None  # Source overlay is explicitly source-only.
    assert receipt.producers["blake/methods/intervals.py"]
    assert receipt.inputs["run"] == digest((paths["run"] / "run.json").read_bytes())
    for entry in receipt.files:
        _ = verify_file(paths["output"], entry.path, entry.size, entry.sha256)
    restored = GeometryReport.model_validate_json(
        (paths["output"] / "geometry-report.json").read_bytes()
    )
    assert restored == report
    csv = source_geometry_csv(report).decode()
    assert "unavailable" in csv
    assert len(csv.splitlines()) == len(report.sources) + 1
    assert report.reviewed_hits == report.documented_window_events == 1


@pytest.mark.parametrize(
    "failure",
    [
        None,
        "request",
        "decisions",
        "window",
        "vocabulary",
        "run",
        "corpus",
        "sdk",
        "outside",
        "occupied",
        "symlink",
    ],
)
def test_real_geometry_cli_refuses_unbound_or_occupied_input(
    geometry_files,
    tmp_path: Path,
    failure,
) -> None:
    paths = dict(geometry_files)
    original = json.loads(paths["request"].read_bytes())
    if failure == "decisions":
        _ = paths["decisions"].write_bytes(paths["decisions"].read_bytes() + b"\n")
    elif failure == "window":
        raw = json.loads(paths["windows"].read_bytes())
        raw[0]["window_start"] = True
        _ = paths["windows"].write_text(json.dumps(raw))
        original["windows_sha256"] = digest(paths["windows"].read_bytes())
    elif failure == "vocabulary":
        raw = json.loads(paths["vocabulary"].read_bytes())
        raw["terms"][0]["group"] = "motion"
        _ = paths["vocabulary"].write_text(json.dumps(raw))
        original["vocabulary_sha256"] = digest(paths["vocabulary"].read_bytes())
    elif failure == "run":
        original["run_sha256"] = "0" * 64
    elif failure == "corpus":
        original["corpus_pin"]["index_sha256"] = "0" * 64
    elif failure == "sdk":
        original["sdk_commit"] = "0" * 40
    elif failure == "outside":
        paths["output"] = tmp_path / "outside"
    elif failure == "occupied":
        paths["output"].mkdir(parents=True)
        _ = (paths["output"] / "retain").write_text("retained")
    elif failure == "symlink":
        target = tmp_path / "retain"
        target.mkdir()
        paths["output"].parent.mkdir()
        paths["output"].symlink_to(target)
    _ = paths["request"].write_text(json.dumps(original))
    expected = "0" * 64 if failure == "request" else digest(paths["request"].read_bytes())
    command = [
        sys.executable,
        "-B",
        "-m",
        "blakean_entomology.geometry_cli",
        "--request-sha256",
        expected,
    ]
    for key in ("request", "bundle", "run", "decisions", "windows", "vocabulary", "output"):
        command.extend(("--" + key, str(paths[key])))
    result = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True, check=False)
    if failure is None:
        assert result.returncode == 0, result.stderr
        assert (paths["output"] / "geometry-receipt.json").is_file()
    else:
        assert result.returncode != 0
        assert not (paths["output"] / "geometry-receipt.json").exists()
        if failure == "occupied":
            assert (paths["output"] / "retain").read_text() == "retained"
        if failure == "symlink":
            assert not tuple((tmp_path / "retain").iterdir())
