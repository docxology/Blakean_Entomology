"""Concurrent real-file mutation cannot replace already verified in-memory evidence."""

import json
import sys
from pathlib import Path

import pytest
from test_application import inputs as inputs

from blakean_entomology.core import analyze, digest, load_run
from blakean_entomology.models import EvidenceError


@pytest.mark.parametrize("boundary", ["require_run_pin", "verify_artifacts"])
def test_parse_the_checked_bytes_after_real_path_mutation(inputs, boundary: str) -> None:
    bundle, pin, spec, output = inputs
    analyze(bundle, pin, spec, output)
    run_pin = digest((output / "run.json").read_bytes())
    before_receipt, before_summary, before_hits = load_run(output, run_pin)
    target = output / ("run.json" if boundary == "require_run_pin" else "summary.json")
    replacement = json.loads(target.read_text())
    if boundary == "require_run_pin":
        replacement["corpus_pin"]["index_sha256"] = "0" * 64
    else:
        replacement["total_occurrences"] = 0
    changed: list[Path] = []

    def schedule(frame, event, _argument) -> None:
        if event == "return" and frame.f_code.co_name == boundary and not changed:
            target.write_text(json.dumps(replacement))
            changed.append(target)

    previous = sys.getprofile()
    sys.setprofile(schedule)
    try:
        receipt, summary, hits = load_run(output, run_pin)
    finally:
        sys.setprofile(previous)
    assert changed == [target]
    assert receipt == before_receipt and summary == before_summary and hits == before_hits
    with pytest.raises(EvidenceError):
        load_run(output, run_pin)
