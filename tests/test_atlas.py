"""Independent arithmetic, zero cells, source separation and real CLI safety."""

import json
import subprocess
import sys

import pytest
from blake.studies import StudySpec, StudyTerm
from pydantic import ValidationError
from test_application import inputs as inputs
from test_taxonomy import REFERENCE, SOURCES

from blakean_entomology.atlas import atlas_from_passages
from blakean_entomology.atlas_models import AtlasReceipt, ReviewEpoch
from blakean_entomology.core import digest, vocabulary
from blakean_entomology.workflows import load_pinned_bundle


@pytest.fixture
def atlas(inputs) -> AtlasReceipt:
    bundle, pin, spec, _output = inputs
    passages = load_pinned_bundle(bundle, pin).passages
    return atlas_from_passages(passages, spec, pin, "f" * 64)


def test_counts_have_independent_arithmetic(atlas) -> None:
    # Given two identical nine-word units: An Emmet saw a bee the worm can fly.
    primary = next(c for c in atlas.cohorts if c.role == "primary")
    ant = next(q for q in primary.categories if q.query_id == "ant")
    # When using the public rate and exact whole-text summaries.
    rate = ant.copy_retaining.rate_per_10000_tokens
    # Then copies and denominator changes are explicit and independently checkable.
    assert primary.source_units == 2
    assert primary.tokens == 18
    assert ant.copy_retaining.occurrences == 2
    assert rate == pytest.approx(20000 / 18)
    assert ant.exact_text.occurrences == 1
    assert ant.exact_text.tokens == 9
    assert ant.work_balanced_coverage_fraction == 1
    assert (
        next(q for q in primary.categories if q.query_id == "spider").copy_retaining.occurrences
        == 0
    )
    assert len(atlas.category_role_plane) == 6 * 9
    assert atlas.current_epoch_authored_decisions == 0
    assert atlas.corpus_images_reviewed is False


def test_normalized_aliases_and_overlap(inputs) -> None:
    # Given equivalent declared forms and two overlapping category names.
    bundle, pin, _spec, _output = inputs
    passages = load_pinned_bundle(bundle, pin).passages
    spec = StudySpec(
        study_id="separate-control",
        title="Synthetic audit",
        terms=(
            StudyTerm(term_id="ant", group="insect", forms=("Emmet", "emmet", "absent")),
            StudyTerm(term_id="alias", group="insect", forms=("emmet",)),
        ),
    )
    # When all forms are audited under an explicitly separate registry.
    result = atlas_from_passages(passages, spec, pin, "f" * 64)
    # Then equivalent aliases do not multiply one category's candidates.
    assert result.candidates == 4
    assert result.distinct_source_spans == 2
    assert result.multiply_categorized_spans == 2
    assert result.forms[0].exact_surface_candidates == 2
    assert result.forms[2].equivalent_form_candidates == 0
    assert result.normalized_alias_groups[0].categories == ("alias", "ant")


def test_zero_token_and_zero_match_work_groups(inputs) -> None:
    # Given a counted unit with punctuation, a positive unit and a zero-match work.
    bundle, pin, spec, _output = inputs
    p = load_pinned_bundle(bundle, pin).passages[0]
    passages = (
        p.model_copy(update={"passage_id": "a", "work_id": "a", "text": "Emmet"}),
        p.model_copy(update={"passage_id": "b", "work_id": "b", "text": "grass grass grass"}),
        p.model_copy(update={"passage_id": "c", "work_id": "c", "text": "!"}),
    )
    # When the shared descriptive engine aggregates the primary cohort.
    result = atlas_from_passages(passages, spec, pin, "f" * 64)
    q = next(q for q in result.cohorts[0].categories if q.query_id == "ant")
    # Then zero-token rates are undefined while zero-match work coverage is included.
    assert q.copy_retaining.rate_per_10000_tokens == 2500
    assert q.work_balanced_rate_per_10000_tokens == 5000
    assert q.work_balanced_coverage_fraction == pytest.approx(1 / 3)
    assert q.rate_work_groups == 2
    assert result.cohorts[0].works[-1].queries[0].measure.rate_per_10000_tokens is None


@pytest.mark.parametrize(
    "change",
    [
        {"count_unit": "animals"},
        {"scanned_units": 999},
        {"primary_candidates": 999},
        {"candidates": 999},
        {"multiply_categorized_spans": 999},
        {"current_epoch_authored_decisions": 11},
        {"corpus_images_reviewed": True},
        {"historical_review_summary_sha256": "a" * 64},
    ],
)
def test_rejects_misleading_aggregation(atlas, change) -> None:
    # Given an atlas falsely relabelled or aggregated.
    raw = atlas.model_dump(mode="json")
    raw.update(change)
    # When admitted as a new typed receipt.
    with pytest.raises(ValidationError):
        AtlasReceipt.model_validate(raw)
    # Then a lexical audit cannot be promoted to a census or historical review.


def test_rejects_misleading_cohort(atlas) -> None:
    # Given one cohort's denominator changed independently of its public measures.
    raw = atlas.model_dump(mode="json")
    raw["cohorts"][0]["tokens"] += 1
    # When admitted as an atlas.
    with pytest.raises(ValidationError, match="atlas_cohort"):
        AtlasReceipt.model_validate(raw)
    # Then the displayed population cannot silently drift.


def test_historical_review_remains_on_its_pin(inputs) -> None:
    # Given the retained historical summary and independent current counted units.
    old = (REFERENCE.parent / "seed-review-summary.json").read_bytes()
    bundle, pin, spec, _output = inputs
    # When historical context is supplied to the atlas.
    result = atlas_from_passages(load_pinned_bundle(bundle, pin).passages, spec, pin, "f" * 64, old)
    # Then no decision is transferred or subtracted from this current population.
    assert result.historical_review is not None
    assert result.historical_review.reviewed_hits == 11
    assert result.historical_review.unreviewed_hits == 36028
    assert result.historical_review.transferred_to_atlas is False
    assert result.historical_review.run_sha256.startswith("12d03123")


def test_rejects_false_historical_denominator() -> None:
    # Given a historical record whose reviewed and unreviewed totals disagree.
    # When the review epoch is parsed.
    with pytest.raises(ValidationError, match="review_denominator"):
        ReviewEpoch(
            run_sha256="a" * 64,
            decisions_sha256="b" * 64,
            candidate_hits=10,
            reviewed_hits=11,
            unreviewed_hits=0,
        )
    # Then the false review coverage is rejected.


def atlas_command(inputs, tmp_path, output) -> list[str]:
    bundle, pin, _spec, _out = inputs
    pin_path = tmp_path / "pin.json"
    if not pin_path.exists():
        pin_path.write_text(pin.model_dump_json())
    return [
        sys.executable,
        "-m",
        "blakean_entomology.cli",
        "corpus-atlas",
        "--bundle",
        str(bundle),
        "--pin",
        str(pin_path),
        "--reference",
        str(REFERENCE),
        "--sources",
        str(SOURCES),
        "--reference-sha256",
        digest(REFERENCE.read_bytes()),
        "--output",
        str(output),
    ]


@pytest.mark.parametrize("failure", [None, "occupied", "outside", "symlink", "pin"])
def test_real_atlas_cli_safety(inputs, tmp_path, failure) -> None:
    # Given real portable inputs and a new private output path.
    output = tmp_path / "analysis_output/atlas.json"
    command = atlas_command(inputs, tmp_path, output)
    if failure == "occupied":
        output.parent.mkdir()
        output.write_text("retain")
    elif failure == "outside":
        command[-1] = str(tmp_path / "outside.json")
    elif failure == "symlink":
        output.parent.mkdir()
        untouched = tmp_path / "untouched"
        untouched.write_text("retain")
        output.symlink_to(untouched)
    elif failure == "pin":
        path = tmp_path / "pin.json"
        raw = json.loads(path.read_bytes())
        raw["index_sha256"] = "0" * 64
        path.write_text(json.dumps(raw))
    # When driving the actual command in a subprocess.
    result = subprocess.run(command, cwd=tmp_path, text=True, capture_output=True)
    # Then outputs are exclusive, confined and source-bound.
    if failure is None:
        assert result.returncode == 0, result.stderr
        record = AtlasReceipt.model_validate_json(output.read_bytes())
        assert record.scanned_units == 3
        assert record.category_count == len(vocabulary().terms)
    else:
        assert result.returncode != 0
        if failure in ("occupied", "symlink"):
            assert output.read_text() == "retain"


@pytest.mark.parametrize("bad_pin", [False, True])
def test_real_reference_cli(tmp_path, bad_pin) -> None:
    # Given actual captured records and either the correct or wrong pin.
    command = [
        sys.executable,
        "-m",
        "blakean_entomology.cli",
        "verify-reference",
        "--reference",
        str(REFERENCE),
        "--sources",
        str(SOURCES),
        "--reference-sha256",
        "0" * 64 if bad_pin else digest(REFERENCE.read_bytes()),
    ]
    # When invoking the public application command.
    result = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True)
    # Then the validated tree or an explicit rejection is returned.
    assert (result.returncode == 0) != bad_pin
    if not bad_pin:
        assert len(json.loads(result.stdout)["nodes"]) == 37
