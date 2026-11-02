"""Typed figure API qualification complements the existing real CLI controls."""

import pytest
from blake.methods.models import ResearchError
from test_application import inputs as inputs
from test_composition_tools import composition_inputs as composition_inputs

from blakean_entomology.composition_workflow import generate
from blakean_entomology.core import digest
from tools.build_composition_figures import FigureSidecar, FiguresManifest, render


def test_all_four_composition_figures_close_real_data(composition_inputs, tmp_path) -> None:
    packet = tmp_path / "analysis_output/packet"
    generate(composition_inputs, packet, tmp_path / "analysis_output")
    pin = digest((packet / "run.json").read_bytes())
    output = tmp_path / "analysis_output/figures"
    render(packet, pin, output, tmp_path / "analysis_output")
    manifest = FiguresManifest.model_validate_json((output / "figures.json").read_bytes())
    assert manifest.analytical_run_sha256 == pin
    assert len(manifest.files) == 16
    for entry in manifest.files:
        raw = (output / entry.path).read_bytes()
        assert (len(raw), digest(raw)) == (entry.size, entry.sha256)
    for sidecar in output.glob("0*.json"):
        value = FigureSidecar.model_validate_json(sidecar.read_bytes())
        assert value.analytical_run_sha256 == pin
        assert len(value.data) == 9
        assert len(value.files) == 3
        assert value.producer.code_sha256 == manifest.producer.code_sha256


@pytest.mark.parametrize("failure", ("run_pin", "changed_csv"))
def test_direct_plotter_refuses_changed_inputs(composition_inputs, tmp_path, failure) -> None:
    packet = tmp_path / "analysis_output/packet"
    generate(composition_inputs, packet, tmp_path / "analysis_output")
    pin = digest((packet / "run.json").read_bytes())
    if failure == "run_pin":
        pin = "0" * 64
    else:
        (packet / "name-work-matrix.csv").write_bytes(b"changed")
    output = tmp_path / "analysis_output/refused"
    with pytest.raises((ValueError, ResearchError)):
        render(packet, pin, output, tmp_path / "analysis_output")
    assert not output.exists()
