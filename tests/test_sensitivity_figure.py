"""Real receipt and CLI guards for the private aggregate figure."""

import json
import subprocess
import sys
from pathlib import Path

import pytest
from blake.studies import StudySpec, StudyTerm
from test_application import inputs as inputs
from test_sensitivity import binding_for

from blakean_entomology.workflows import proximity_workflow, sensitivity_workflow


@pytest.fixture
def figure_inputs(inputs, tmp_path, monkeypatch) -> tuple[Path, Path]:
    bundle, pin, _spec, _output = inputs
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("MPLCONFIGDIR", str(tmp_path / "matplotlib"))
    spec = StudySpec(
        study_id="synthetic-figure",
        title="Synthetic",
        terms=tuple(
            StudyTerm(term_id=name, group="synthetic", forms=(name,))
            for name in (
                "worm",
                "fly",
                "spider",
                "polypus",
                "bee",
                "ant",
                "caterpillar",
                "butterfly",
            )
        ),
    )
    sensitivity = tmp_path / "analysis_output" / "sensitivity.json"
    proximity = tmp_path / "analysis_output" / "proximity.json"
    sensitivity_workflow(bundle, pin, spec, sensitivity)
    proximity_workflow(bundle, binding_for(pin), proximity)
    return sensitivity, proximity


def invoke(paths, output) -> subprocess.CompletedProcess[str]:
    script = Path(__file__).parents[1] / "tools" / "build_sensitivity_figure.py"
    return subprocess.run(
        [
            sys.executable,
            str(script),
            "--sensitivity",
            str(paths[0]),
            "--proximity",
            str(paths[1]),
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
    )


def test_real_figure_roundtrip_and_overwrite(figure_inputs, tmp_path) -> None:
    output = tmp_path / "analysis_output" / "figure"
    result = invoke(figure_inputs, output)
    assert result.returncode == 0, result.stderr
    image = (output / "sensitivity.png").read_bytes()
    summary = json.loads((output / "summary.json").read_text())
    assert image.startswith(b"\x89PNG\r\n\x1a\n")
    assert summary["primary_units"] == 2
    assert summary["scanned_source_units"] == 3
    repeated = invoke(figure_inputs, output)
    assert repeated.returncode != 0 and "occupied_output" in repeated.stderr
    assert (output / "sensitivity.png").read_bytes() == image


@pytest.mark.parametrize(
    "mutation,code",
    [
        ("pin", "figure_pin"),
        ("profile", "figure_profile"),
        ("inventory", "figure_inventory"),
        ("denominator", "figure_denominator"),
        ("categories", "figure_categories"),
    ],
)
def test_rejects_incompatible_receipts(figure_inputs, tmp_path, mutation, code) -> None:
    path = figure_inputs[0]
    raw = json.loads(path.read_text())
    if mutation == "pin":
        raw["corpus_pin"]["bundle_manifest_sha256"] = "0" * 64
    elif mutation == "profile":
        raw["profile"]["semantics"]["tokens"] = "mislabelled denominator"
    elif mutation == "inventory":
        raw["statistics"]["inventory_sha256"] = "0" * 64
    else:
        # A new valid one-unit inventory cannot share the two-unit proximity denominator.
        from blake.methods.statistics import analyze_inventory

        from blakean_entomology.workflows import SensitivityReceipt

        parsed = SensitivityReceipt.model_validate(raw)
        units = parsed.statistics.units[:1]
        query_ids = parsed.statistics.query_ids
        if mutation == "categories":
            query_ids = tuple(query for query in query_ids if query != "butterfly")
            units = tuple(
                unit.model_copy(
                    update={"occurrences": {query: unit.occurrences[query] for query in query_ids}}
                )
                for unit in parsed.statistics.units
            )
        raw["statistics"] = analyze_inventory(units, query_ids, parsed.profile).model_dump(
            mode="json"
        )
    path.write_text(json.dumps(raw))
    output = tmp_path / "analysis_output" / "rejected"
    result = invoke(figure_inputs, output)
    assert result.returncode != 0 and code in result.stderr
    assert not output.exists()


def test_figure_rejects_outside_private_output(figure_inputs, tmp_path) -> None:
    output = tmp_path / "public-figure"
    result = invoke(figure_inputs, output)
    assert result.returncode != 0 and "private_output_required" in result.stderr
    assert not output.exists()
