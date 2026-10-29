"""Source verification and private mapping policy; tree mechanics belong to Blake."""

from pathlib import Path
from typing import Final
from xml.etree import ElementTree as ET

from blake.methods.hierarchy import EvidenceTree, EvidenceTreeNode
from blake.methods.models import EvidenceError
from blake.methods.runs import digest, read_regular
from blake.studies import StudySpec
from pydantic import HttpUrl

from .taxonomy_models import Ancestor, MappingStatus, ReferenceTaxon, TaxonomyReference

FOCAL_TARGETS: Final = {"fly": 7147, "spider": 6893, "ant": 36668, "bee": 3042114}
GROUP_ANCESTORS: Final = {
    "insect": 50557,
    "arachnid": 6854,
    "myriapod": 61985,
    "mollusc": 6447,
    "crustacean": 197562,
}


def vocabulary_digest(spec: StudySpec) -> str:
    """Use the study's canonical vocabulary identity without changing its epoch."""
    import json

    return digest(
        json.dumps(
            spec.model_dump(mode="json"),
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode()
    )


def ncbi_records(raw: bytes, source_id: str) -> tuple[ReferenceTaxon, ...]:
    """Project only explicit taxon records and LineageEx; never guess identifiers."""
    root = ET.fromstring(raw)
    records: list[ReferenceTaxon] = []
    for record in root.findall("Taxon"):
        tax_id = int(record.findtext("TaxId", "0"))
        records.append(
            ReferenceTaxon(
                tax_id=tax_id,
                name=record.findtext("ScientificName", ""),
                rank=record.findtext("Rank", ""),
                source_id=source_id,
                lineage=tuple(
                    Ancestor(
                        tax_id=int(a.findtext("TaxId", "0")),
                        name=a.findtext("ScientificName", ""),
                        rank=a.findtext("Rank", ""),
                    )
                    for a in record.findall("LineageEx/Taxon")
                ),
                url=HttpUrl(
                    f"https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id={tax_id}"
                ),
            )
        )
    if not records or len({t.tax_id for t in records}) != len(records):
        raise EvidenceError("ncbi_records", source_id)
    return tuple(records)


def reference_tree(
    reference: TaxonomyReference, selected: tuple[int, ...] | None = None
) -> EvidenceTree:
    """Compress omitted ancestors, then delegate rooted-tree validation to core."""
    taxa = (
        reference.taxa
        if selected is None
        else tuple(t for t in reference.taxa if t.tax_id in selected)
    )
    retained = {t.tax_id for t in taxa}
    if selected is not None and (set(selected) != retained or len(selected) != len(retained)):
        raise EvidenceError("tree_selection", str(selected))
    if reference.root_tax_id not in retained:
        raise EvidenceError("tree_root", reference.reference_id)
    return EvidenceTree(
        nodes=tuple(
            EvidenceTreeNode(
                node_id=str(t.tax_id),
                label=t.name,
                parent_id=next(
                    (str(a.tax_id) for a in reversed(t.lineage) if a.tax_id in retained), None
                ),
            )
            for t in taxa
        )
    )


def validate_mappings(reference: TaxonomyReference, spec: StudySpec) -> None:
    """Reject false certainty, cross-domain targets, and missing study categories."""
    taxa = {t.tax_id: t for t in reference.taxa}
    mappings = {m.term_id: m for m in reference.mappings}
    if reference.vocabulary_sha256 != vocabulary_digest(spec) or set(mappings) != {
        t.term_id for t in spec.terms
    }:
        raise EvidenceError("mapping_vocabulary", spec.study_id)
    for term in spec.terms:
        mapping = mappings[term.term_id]
        if term.group in ("associated", "motion") and mapping.status != MappingStatus.NON_TAXON:
            raise EvidenceError("associated_is_not_taxon", term.term_id)
        required = GROUP_ANCESTORS.get(term.group)
        if required is not None:
            for target in mapping.taxon_ids:
                taxon = taxa[target]
                if required not in {taxon.tax_id, *(a.tax_id for a in taxon.lineage)}:
                    raise EvidenceError("mapping_lineage", term.term_id)
        expected = FOCAL_TARGETS.get(term.term_id)
        if expected is not None and mapping.taxon_ids != (expected,):
            raise EvidenceError("focal_mapping", term.term_id)
    worm = mappings.get("worm")
    if worm is not None and (
        worm.status != MappingStatus.AMBIGUOUS or not {6340, 6157, 6231}.issubset(worm.taxon_ids)
    ):
        raise EvidenceError("worm_is_polyphyletic_label", "worm")


def load_reference(
    path: Path, source_directory: Path, expected_sha256: str, spec: StudySpec
) -> TaxonomyReference:
    """Require the caller's reference pin and each independently captured source."""
    raw = read_regular(path)
    if digest(raw) != expected_sha256:
        raise EvidenceError("reference_pin", str(path))
    reference = TaxonomyReference.model_validate_json(raw)
    records: dict[tuple[str, int], ReferenceTaxon] = {}
    for source in reference.sources:
        payload = read_regular(source_directory / source.filename)
        if digest(payload) != source.sha256 or len(payload) != source.size:
            raise EvidenceError("reference_source_hash", source.source_id)
        if source.filename.endswith(".xml"):
            records.update(
                ((t.source_id, t.tax_id), t) for t in ncbi_records(payload, source.source_id)
            )
    for taxon in reference.taxa:
        if records.get((taxon.source_id, taxon.tax_id)) != taxon:
            raise EvidenceError("taxon_source_projection", taxon.name)
        if taxon.rank in ("species", "subspecies"):
            raise EvidenceError("species_not_supported", taxon.name)
    validate_mappings(reference, spec)
    _ = reference_tree(reference)
    return reference
