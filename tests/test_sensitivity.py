"""Real source controls for separately labeled NFKC and literal analyses."""

from pathlib import Path

import pytest
from blake.methods.models import EvidenceError, ProjectionCorpusPin, ResearchError
from blake.methods.profiles import RetrievalProfile
from blake.methods.proximity import ProximityGrid
from blake.methods.search_models import SearchRequest
from blake.studies import StudySpec, StudyTerm
from blake.text_search.models import Passage
from test_application import inputs as inputs

from blakean_entomology.sensitivity import (
    PAIRS,
    WIDTHS,
    ProximityBinding,
    analyze_sensitivity,
    default_proximity_grid,
    literal_proximity_from_bundle,
)


@pytest.fixture
def sources(tmp_path: Path) -> tuple[Passage, ...]:
    units = tuple(
        Passage(
            passage_id=identity,
            work_id=work,
            author_id="william-blake-1757-1827",
            title=work,
            edition_id=identity,
            edition="test",
            copy_id=identity,
            locator="section",
            locator_kind="section",
            source_url="https://example.org",
            rights="synthetic",
            text_role=role,
            source_plane="reading",
            text=text,
        )
        for identity, work, role, text in (
            ("p1", "w1", "primary", "ﬂy ﬂy"),
            ("p2", "w1", "primary", "ﬂy ﬂy"),
            ("p3", "w2", "primary", "zero matches"),
            ("p4", "w3", "primary", "..."),
            ("e1", "w4", "editorial", "fly"),
        )
    )
    path = tmp_path / "passages.jsonl"
    path.write_text("".join(unit.model_dump_json() + "\n" for unit in units))
    return tuple(Passage.model_validate_json(line) for line in path.read_text().splitlines())


def specification() -> StudySpec:
    return StudySpec(
        study_id="test",
        title="synthetic",
        terms=(
            StudyTerm(term_id="fly", group="x", forms=("fly", "ﬂy")),
            StudyTerm(term_id="overlap", group="x", forms=("fly",)),
            StudyTerm(term_id="absent", group="x", forms=("absent",)),
        ),
    )


def test_nfkc_overlap_duplicates_zero_strata(sources) -> None:
    result = analyze_sensitivity(sources, specification())
    assert result.profile == RetrievalProfile.NFKC_TOKENS_V2.value
    assert tuple(unit.passage_id for unit in result.units) == ("p1", "p2", "p3", "p4")
    queries = {query.query_id: query for query in result.queries}
    assert queries["fly"].copy_retaining.occurrences == 4
    assert queries["overlap"].copy_retaining.occurrences == 4
    assert queries["fly"].exact_text.occurrences == 2
    assert queries["fly"].copy_retaining.tokens == 6
    assert queries["absent"].copy_retaining.occurrences == 0
    zero = next(row for row in result.strata if row.dimension == "work" and row.key == ("w3",))
    assert zero.source_units == 1 and zero.tokens == 0
    assert all(query.measure.rate_per_10000_tokens is None for query in zero.queries)


def test_sensitivity_recomputes_changed_text(sources) -> None:
    original = analyze_sensitivity(sources, specification())
    changed = (sources[0].model_copy(update={"text": "absent"}), *sources[1:])
    current = analyze_sensitivity(changed, specification())
    assert current.inventory_sha256 != original.inventory_sha256
    assert current.units[0].occurrences["absent"] == 1
    assert current.units[0].occurrences["fly"] == 0


def test_empty_primary_membership_rejected(sources) -> None:
    with pytest.raises(ResearchError, match="statistics_inventory"):
        analyze_sensitivity((sources[-1],), specification())


def binding_for(pin) -> ProximityBinding:
    return ProximityBinding(
        bundle_manifest_sha256=pin.bundle_manifest_sha256,
        projection_pin=ProjectionCorpusPin(
            upstream_commit="separate-public-code-commit",
            captured_manifest_sha256=pin.captured_manifest_sha256,
            projection_manifest_sha256=pin.projection_manifest_sha256,
            projection_relative_path="test",
            index_sha256=pin.index_sha256,
            unresolved_images=0,
            scope_note="synthetic",
        ),
    )


def test_literal_bundle_defaults_and_explicit_grid(inputs) -> None:
    bundle, pin, _spec, _output = inputs
    binding = binding_for(pin)
    defaults = default_proximity_grid()
    assert len(defaults.requests) == len(PAIRS) * len(WIDTHS)
    result = literal_proximity_from_bundle(bundle, binding)
    assert result.grid == defaults
    assert result.scanned_source_units == 3
    assert all(row.eligible_source_units == 2 for row in result.rows)
    custom = ProximityGrid(
        requests=(
            SearchRequest(
                terms=("emmet", "bee"),
                mode="all",
                window_words=8,
                role="primary",
                plane="reading",
                limit=1,
                context_chars=0,
            ),
        )
    )
    selected = literal_proximity_from_bundle(bundle, binding, custom)
    assert selected.rows[0].matched_source_units == 2
    assert "literal ALL" in selected.method


@pytest.mark.parametrize(
    "field", ["captured_manifest_sha256", "projection_manifest_sha256", "index_sha256"]
)
def test_literal_pin_mismatch(inputs, field) -> None:
    bundle, pin, _spec, _output = inputs
    binding = binding_for(pin)
    altered = binding.model_copy(
        update={"projection_pin": binding.projection_pin.model_copy(update={field: "0" * 64})}
    )
    with pytest.raises(EvidenceError, match="corpus_pin_mismatch"):
        literal_proximity_from_bundle(bundle, altered)


def test_literal_corruption(inputs) -> None:
    bundle, pin, _spec, _output = inputs
    (bundle / "passages.jsonl").write_bytes(b"changed")
    with pytest.raises(ValueError, match="checksum"):
        literal_proximity_from_bundle(bundle, binding_for(pin))


def test_other_author_primary_is_excluded(sources) -> None:
    other = sources[0].model_copy(update={"passage_id": "other", "author_id": "another-author"})
    result = analyze_sensitivity((*sources, other), specification())
    assert "other" not in {unit.passage_id for unit in result.units}
    assert sum(unit.tokens for unit in result.units) == 6
