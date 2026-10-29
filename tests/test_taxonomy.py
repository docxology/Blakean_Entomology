"""Real retained-source controls for conditional biological reference policy."""

import json
import shutil
from pathlib import Path

import pytest
from blake.methods.hierarchy import layout_evidence_tree
from pydantic import ValidationError

from blakean_entomology.core import digest, vocabulary
from blakean_entomology.models import EvidenceError
from blakean_entomology.taxonomy import (
    load_reference,
    ncbi_records,
    reference_tree,
    validate_mappings,
)
from blakean_entomology.taxonomy_models import LexicalMapping, TaxonomyReference

STAGE = Path(__file__).resolve().parents[1]
REFERENCE = STAGE / "research/reference-taxonomy-v1.json"
SOURCES = STAGE / "local_data/reference-sources"


@pytest.fixture
def reference() -> TaxonomyReference:
    return load_reference(REFERENCE, SOURCES, digest(REFERENCE.read_bytes()), vocabulary())


def test_real_lineages_and_shared_layout(reference) -> None:
    # Given the retrieved reference and its complete original vocabulary.
    tree = reference_tree(reference, (33208, 6656, 50557, 7147, 6893))
    # When the shared hierarchy positions the private reference.
    positions = {p.node_id: p for p in layout_evidence_tree(tree)}
    # Then only flies descend from Insecta in this selection.
    assert positions["6893"].depth == 2
    assert positions["7147"].depth == 3
    assert len(reference.mappings) == 102
    assert not any(t.rank == "species" for t in reference.taxa)


@pytest.mark.parametrize("selection", [(6893,), (33208, 999999), (33208, 33208)])
def test_rejects_invalid_tree_selection(reference, selection) -> None:
    # Given an incomplete, dangling or duplicate presentation selection.
    # When it crosses the selection boundary.
    with pytest.raises(EvidenceError):
        reference_tree(reference, selection)
    # Then no private fallback tree is substituted.


@pytest.mark.parametrize("raw", [b"<TaxaSet/>", b"<TaxaSet><Taxon/></TaxaSet>"])
def test_rejects_missing_ncbi_records(raw) -> None:
    # Given a missing or malformed database record.
    # When parsed as a source record.
    with pytest.raises((EvidenceError, ValidationError)):
        ncbi_records(raw, "control")
    # Then an identifier or name is never invented.


@pytest.mark.parametrize(
    "changes",
    [
        {"status": "resolved_lineage", "taxon_ids": []},
        {"status": "broad_group", "taxon_ids": []},
        {"status": "non_taxon", "taxon_ids": [7147]},
        {"taxon_ids": [7147, 7147]},
        {"certainty": "species_identified"},
        {"rationale": " "},
        {"evidence_locators": [" "]},
        {"alternatives_exhaustive": True},
    ],
)
def test_rejects_unsupported_mapping_certainty(reference, changes) -> None:
    # Given a curated association with one invalid scientific claim.
    raw = next(m for m in reference.mappings if m.term_id == "fly").model_dump(mode="json")
    raw.update(changes)
    # When the mapping is parsed.
    with pytest.raises(ValidationError):
        LexicalMapping.model_validate(raw)
    # Then false certainty fails at the boundary.


@pytest.mark.parametrize(
    "term,target,status",
    [
        ("fly", [6340], "resolved_lineage"),
        ("spider", [50557], "resolved_lineage"),
        ("bee", [7399], "resolved_lineage"),
        ("ant", [7041], "resolved_lineage"),
        ("worm", [6340], "resolved_lineage"),
        ("wing", [50557], "broad_group"),
    ],
)
def test_rejects_wrong_semantic_mapping(reference, term, target, status) -> None:
    # Given a wrong mapping including a same-domain ant/beetle substitution.
    raw = reference.model_dump(mode="json")
    for mapping in raw["mappings"]:
        if mapping["term_id"] == term:
            mapping.update(taxon_ids=target, status=status)
    modified = TaxonomyReference.model_validate(raw)
    # When private policy checks the mapping against the original vocabulary.
    with pytest.raises(EvidenceError):
        validate_mappings(modified, vocabulary())
    # Then an ambiguous worm is never forced into a single lineage.


@pytest.mark.parametrize(
    "mutation",
    [
        "dangling",
        "duplicate_taxon",
        "duplicate_source",
        "duplicate_filename",
        "missing_root",
        "duplicate_mapping",
        "source_membership",
    ],
)
def test_rejects_reference_membership(reference, mutation) -> None:
    # Given a structurally invalid reference.
    raw = reference.model_dump(mode="json")
    if mutation == "dangling":
        raw["mappings"][0]["taxon_ids"] = [999999]
    elif mutation == "duplicate_taxon":
        raw["taxa"].append(raw["taxa"][0])
    elif mutation == "duplicate_source":
        raw["sources"].append(raw["sources"][0])
    elif mutation == "duplicate_filename":
        raw["sources"][1]["filename"] = raw["sources"][0]["filename"]
    elif mutation == "missing_root":
        raw["taxa"] = raw["taxa"][1:]
    elif mutation == "duplicate_mapping":
        raw["mappings"].append(raw["mappings"][0])
    else:
        raw["taxa"][0]["source_id"] = "missing"
    # When membership is parsed.
    with pytest.raises(ValidationError):
        TaxonomyReference.model_validate(raw)
    # Then no partially connected biological reference is admitted.


@pytest.mark.parametrize("mutation", ["hash", "projection", "vocabulary", "species"])
def test_rejects_changed_source_or_projection(reference, tmp_path, mutation) -> None:
    # Given independent copies of captured input bytes.
    directory = tmp_path / "sources"
    directory.mkdir()
    for s in reference.sources:
        shutil.copyfile(SOURCES / s.filename, directory / s.filename)
    raw = reference.model_dump(mode="json")
    if mutation == "hash":
        with (directory / reference.sources[0].filename).open("ab") as handle:
            _ = handle.write(b"changed")
    elif mutation == "projection":
        raw["taxa"][0]["name"] = "invented"
    elif mutation == "vocabulary":
        raw["vocabulary_sha256"] = "0" * 64
    else:
        species = next(
            t
            for t in ncbi_records(
                (directory / reference.sources[0].filename).read_bytes(), "ncbi-main"
            )
            if t.rank == "species"
        )
        raw["taxa"].append(species.model_dump(mode="json"))
    path = tmp_path / "reference.json"
    path.write_text(json.dumps(raw))
    # When checked against the source and vocabulary boundaries.
    with pytest.raises(EvidenceError):
        load_reference(path, directory, digest(path.read_bytes()), vocabulary())
    # Then source drift cannot be relabelled as a valid reference.


def test_rejects_wrong_reference_pin() -> None:
    # Given the actual reference with the wrong caller pin.
    # When loading it.
    with pytest.raises(EvidenceError, match="reference_pin"):
        load_reference(REFERENCE, SOURCES, "0" * 64, vocabulary())
    # Then none of the derived data is trusted.
