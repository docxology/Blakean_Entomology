"""Real malformed files and signed packet boundaries; no mocking."""

import pytest
from blake.methods.profiles import RetrievalProfile, runtime_profile
from blake.methods.search import matching_spans
from blake.methods.search_models import SearchRequest
from blake.methods.statistics import analyze_inventory
from blake.methods.statistics_models import SourceUnit
from blake.studies import StudySpec, StudyTerm

from blakean_entomology.composition import (
    LITERAL_PAIRS,
    composition_audit,
    inventory_from_atlas,
)


def test_declared_name_channel_selection_preserves_zero_categories() -> None:
    spec = StudySpec(
        study_id="fixture",
        title="fixture",
        terms=(
            StudyTerm(term_id="worm", group="worm", forms=("worm",)),
            StudyTerm(term_id="spider", group="arachnid", forms=("spider",)),
            StudyTerm(term_id="wing", group="associated", forms=("wing",)),
        ),
    )
    unit = SourceUnit(
        passage_id="u",
        work_id="w",
        title="fixture",
        edition_id="e",
        copy_id=None,
        text_sha256="a" * 64,
        tokens=5,
        occurrences={"worm": 2, "spider": 0, "wing": 3},
    )
    shared = analyze_inventory(
        (unit,),
        ("worm", "spider", "wing"),
        runtime_profile(RetrievalProfile.NFKC_TOKENS_V2),
    )
    works = tuple(s for s in shared.strata if s.dimension == "work")
    inventory = inventory_from_atlas(spec, works)
    assert inventory.categories == ("worm", "spider")
    assert inventory.groups[0].counts == (2, 0)
    assert inventory.groups[0].matched_units == (1, 0)
    audit = composition_audit(inventory, shared.queries)
    assert audit.name_category_candidates == 2
    assert audit.nonempty_name_work_groups == 1
    assert audit.categories[0].positive_work_groups == 1
    assert audit.omissions[0].remaining_name_candidates == 0
    assert len(LITERAL_PAIRS) == len(set(LITERAL_PAIRS)) == 12
    invalid = spec.model_copy(
        update={"terms": (spec.terms[0].model_copy(update={"group": "unknown"}),)}
    )
    with pytest.raises(ValueError, match="unknown registry channel"):
        inventory_from_atlas(invalid, works)
    with pytest.raises(ValueError, match="complete disjoint group strata"):
        inventory_from_atlas(spec, tuple(s for s in shared.strata if s.dimension == "edition"))


def test_literal_window_independent_word_envelope_and_nested_control() -> None:
    # Tokens 1=worm, 2=a, 3=b, 4=fly; minimum complete envelope is exactly four.
    text = "worm a b fly"
    narrow = SearchRequest(terms=("worm", "fly"), mode="all", window_words=3, context_chars=0)
    wide = narrow.model_copy(update={"window_words": 4})
    assert matching_spans(text, narrow) == ()
    assert matching_spans(text, wide) == (("worm", 0, 4), ("fly", 9, 12))
    assert matching_spans("worms giant been butterfly", wide) == ()
    nested = SearchRequest(terms=("bee", "honey bee"), mode="all", window_words=2, context_chars=0)
    assert len(matching_spans("honey bee", nested)) == 2
    assert matching_spans("worm a b fly", wide.model_copy(update={"window_words": None}))
