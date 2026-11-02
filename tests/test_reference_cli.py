"""Direct reference-figure CLI and undefined-denominator refusal controls."""

import subprocess
import sys

import pytest
from test_application import inputs as inputs
from test_research_figures import figure_data as figure_data
from test_taxonomy import REFERENCE, SOURCES, STAGE

from blakean_entomology.core import digest
from blakean_entomology.models import EvidenceError


def test_real_figure_cli_rejects_changed_pin(figure_data, tmp_path) -> None:
    # Given a valid atlas and wrong caller-held digest.
    command = [
        sys.executable,
        str(STAGE / "tools/build_reference_figures.py"),
        "--atlas",
        str(figure_data),
        "--atlas-sha256",
        "0" * 64,
        "--reference",
        str(REFERENCE),
        "--reference-sha256",
        digest(REFERENCE.read_bytes()),
        "--sources",
        str(SOURCES),
        "--output",
        str(tmp_path / "analysis_output/rejected"),
    ]
    # When driving the actual executable script.
    result = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True)
    # Then failure is explicit and nonzero.
    assert result.returncode != 0
    assert "atlas_pin" in result.stderr


def test_plotting_refuses_an_undefined_denominator() -> None:
    from tools.reference_plotting import plotted_fraction

    assert plotted_fraction(0.0) == 0.0
    assert plotted_fraction(1.0) == 1.0
    with pytest.raises(EvidenceError, match="atlas_plot_denominator"):
        plotted_fraction(None)
