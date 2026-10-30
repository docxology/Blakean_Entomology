"""Real contextual aggregation and publication controls on a tiny retained run."""

import json
import subprocess
import sys
from contextlib import chdir
from pathlib import Path

import pytest
from test_application import inputs as inputs

from blakean_entomology.core import analyze, digest, load_run
from blakean_entomology.models import Decision, EvidenceError, ReviewDecision
from blakean_entomology.review_contexts import summarize_contexts

TOOLS = Path(__file__).parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
from build_context_review_figure import generate  # noqa: E402


@pytest.fixture
def review_inputs(inputs, tmp_path) -> tuple[Path, Path, str]:
    """Create actual primary/editorial candidates and explicit synthetic decisions."""
    bundle, pin, spec, run = inputs
    analyze(bundle, pin, spec, run)
    run_sha = digest((run / "run.json").read_bytes())
    _, _, hits = load_run(run, run_sha)
    selected = tuple(
        next(h for h in hits if h.passage_id == source and h.term_id == "fly")
        for source in ("p1", "e1")
    )
    labels = (Decision.ANIMAL_LITERAL, Decision.ANIMAL_FIGURATIVE)
    decisions = tuple(
        ReviewDecision(
            run_sha256=run_sha,
            hit_id=hit.hit_id,
            decision=label,
            reviewer="Synthetic test reviewer",
            rationale="Explicit synthetic control",
            verification_locator="Synthetic fixture " + hit.passage_id,
        )
        for hit, label in zip(selected, labels, strict=True)
    )
    path = tmp_path / "decisions.jsonl"
    path.write_text("\n".join(d.model_dump_json() for d in decisions) + "\n")
    return run, path, run_sha


def test_contexts_keep_original_source_eligibility(review_inputs) -> None:
    # Given the same animal word in primary and editorial source units.
    run, decisions, pin = review_inputs
    # When explicit animal decisions are aggregated.
    audit = summarize_contexts(run, decisions, pin)
    # Then the editorial animal stays exploratory and source roles stay separate.
    assert audit.summary.primary_animal_hits == audit.summary.exploratory_animal_hits == 1
    assert {(c.role, c.plane, c.candidates) for c in audit.cohorts} == {
        ("primary", "reading", 1),
        ("editorial", "erdman", 1),
    }


def test_contexts_include_unassigned_zero_dispositions(review_inputs) -> None:
    # Given two authored labels for one retained category.
    # When that bounded decision set is summarized.
    audit = summarize_contexts(*review_inputs)
    # Then all six dispositions exist and empty ones are actual zero cells.
    assert len(audit.cells) == 6
    assert {c.decision: c.candidates for c in audit.cells} == {
        Decision.ANIMAL_LITERAL: 1,
        Decision.ANIMAL_FIGURATIVE: 1,
        Decision.ASSOCIATED: 0,
        Decision.NON_ANIMAL: 0,
        Decision.EDITORIAL: 0,
        Decision.UNCERTAIN: 0,
    }


def test_contexts_retain_identical_text_in_distinct_source_units(review_inputs) -> None:
    # Given identical synthetic text retained as two independently identified units.
    run, path, pin = review_inputs
    _, _, hits = load_run(run, pin)
    selected = tuple(
        next(h for h in hits if h.passage_id == source and h.term_id == "worm")
        for source in ("p1", "p2")
    )
    path.write_text(
        "\n".join(
            ReviewDecision(
                run_sha256=pin,
                hit_id=h.hit_id,
                decision=Decision.ANIMAL_LITERAL,
                reviewer="Synthetic",
                rationale="Retained source-copy control",
                verification_locator="Synthetic " + h.passage_id,
            ).model_dump_json()
            for h in selected
        )
        + "\n"
    )
    # When reviewed candidate IDs are counted rather than deduplicating text.
    audit = summarize_contexts(run, path, pin)
    # Then the two units remain two reviewed candidate IDs within one group.
    assert (audit.source_units, audit.work_groups, audit.summary.reviewed_hits) == (2, 1, 2)


@pytest.mark.parametrize("failure", ["wrong_pin", "empty", "unknown_candidate", "duplicate"])
def test_contexts_refuse_unbound_decisions(review_inputs, failure) -> None:
    # Given one unsafe decision boundary over a real immutable run.
    run, path, pin = review_inputs
    if failure == "wrong_pin":
        pin = "0" * 64
    elif failure == "empty":
        path.write_text("")
    elif failure == "unknown_candidate":
        rows = [json.loads(line) for line in path.read_bytes().splitlines()]
        rows[0]["hit_id"] = "not-an-admitted-hit"
        path.write_text("\n".join(json.dumps(row) for row in rows))
    else:
        path.write_bytes(path.read_bytes() + path.read_bytes().splitlines()[0] + b"\n")
    # When the public review audit is invoked.
    with pytest.raises(EvidenceError):
        summarize_contexts(run, path, pin)
    # Then core membership/pin errors cannot become plotted adjudications.


def test_context_figure_closes_all_actual_formats(review_inputs, tmp_path) -> None:
    # Given an actual source-role-preserving audit.
    audit = summarize_contexts(*review_inputs)
    target = tmp_path / "analysis_output/context"
    # When the real Agg/PDF/SVG drawing producer publishes once.
    with chdir(tmp_path):
        receipt = generate(audit, target)
    # Then every exported byte is bound, including real raster and vector formats.
    assert len(receipt.files) == 6
    for member in receipt.files:
        assert digest((target / member.path).read_bytes()) == member.sha256
    assert (target / "context-review.png").read_bytes().startswith(b"\x89PNG")
    assert (target / "context-review.pdf").read_bytes().startswith(b"%PDF")
    assert b"<svg" in (target / "context-review.svg").read_bytes()
    # A second actual render must preserve every data/raster/vector byte.
    with chdir(tmp_path):
        again = generate(audit, tmp_path / "analysis_output/context-again")
    for first, repeated in zip(receipt.files, again.files, strict=True):
        assert first.sha256 == repeated.sha256, first.path


def test_context_real_cli_rejects_wrong_run_before_output(review_inputs, tmp_path) -> None:
    # Given a wrong caller-held pin and no output directory.
    run, decisions, _ = review_inputs
    output = tmp_path / "analysis_output/rejected"
    # When the actual command is executed in a child process.
    result = subprocess.run(
        [
            sys.executable,
            "-B",
            str(TOOLS / "build_context_review_figure.py"),
            "--run",
            str(run),
            "--run-sha256",
            "0" * 64,
            "--decisions",
            str(decisions),
            "--output",
            str(output),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    # Then it refuses without publishing a figure or completion receipt.
    assert result.returncode == 1, result.stderr
    assert not output.exists()
