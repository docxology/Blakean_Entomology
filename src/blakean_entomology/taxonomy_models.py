"""Private biological reference and conditional lexical-association contracts."""

from datetime import date
from enum import StrEnum
from typing import Literal, Self, assert_never

from blake.methods.models import Digest, EvidenceError, FrozenModel
from pydantic import Field, HttpUrl, model_validator


class MappingStatus(StrEnum):
    RESOLVED = "resolved_lineage"
    BROAD = "broad_group"
    AMBIGUOUS = "ambiguous_mapping"
    NON_TAXON = "non_taxon"
    OUTSIDE = "outside_scope"


class ReferenceSource(FrozenModel):
    source_id: str = Field(min_length=1)
    filename: str = Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
    url: HttpUrl
    accessed: date
    sha256: Digest
    size: int = Field(gt=0)
    locator: str = Field(min_length=1)
    claim_limit: str = Field(min_length=1)


class Ancestor(FrozenModel):
    tax_id: int = Field(gt=0)
    name: str = Field(min_length=1)
    rank: str = Field(min_length=1)


class ReferenceTaxon(Ancestor):
    source_id: str = Field(min_length=1)
    lineage: tuple[Ancestor, ...]
    url: HttpUrl


class LexicalMapping(FrozenModel):
    term_id: str = Field(min_length=1)
    status: MappingStatus
    taxon_ids: tuple[int, ...] = ()
    certainty: Literal["conditional_modern_sense"] = "conditional_modern_sense"
    rationale: str = Field(min_length=1)
    evidence_locators: tuple[str, ...] = Field(min_length=1)
    alternatives_exhaustive: Literal[False] = False

    @model_validator(mode="after")
    def association_shape(self) -> Self:
        if not self.rationale.strip() or any(not v.strip() for v in self.evidence_locators):
            raise EvidenceError("mapping_rationale", self.term_id)
        if len(set(self.taxon_ids)) != len(self.taxon_ids):
            raise EvidenceError("duplicate_mapping_target", self.term_id)
        # Every arm returns; the post-match assert_never is checked by strict types.
        match self.status:  # noqa: MATCH_OK
            case MappingStatus.RESOLVED:
                if len(self.taxon_ids) != 1:
                    raise EvidenceError("resolved_mapping_target", self.term_id)
                return self
            case MappingStatus.BROAD:
                if not self.taxon_ids:
                    raise EvidenceError("broad_mapping_target", self.term_id)
                return self
            case MappingStatus.AMBIGUOUS:
                return self  # An unresolved label need not have any animal target.
            case MappingStatus.NON_TAXON | MappingStatus.OUTSIDE:
                if self.taxon_ids:
                    raise EvidenceError("non_taxon_target", self.term_id)
                return self
        assert_never(self.status)


class TaxonomyReference(FrozenModel):
    schema_version: Literal[1] = 1
    reference_id: Literal["invertebrate-reference-2026-10-28-v1"]
    vocabulary_sha256: Digest
    root_tax_id: Literal[33208] = 33208
    interpretation: Literal["compressed NCBI reference classification; no inferred phylogeny"]
    sources: tuple[ReferenceSource, ...] = Field(min_length=1)
    taxa: tuple[ReferenceTaxon, ...] = Field(min_length=1)
    mappings: tuple[LexicalMapping, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def membership(self) -> Self:
        sources = {s.source_id for s in self.sources}
        taxa = {t.tax_id: t for t in self.taxa}
        if len(sources) != len(self.sources) or len(taxa) != len(self.taxa):
            raise EvidenceError("reference_duplicate", self.reference_id)
        if len({s.filename for s in self.sources}) != len(self.sources):
            raise EvidenceError("reference_source_duplicate", self.reference_id)
        if self.root_tax_id not in taxa or any(t.source_id not in sources for t in self.taxa):
            raise EvidenceError("reference_source_membership", self.reference_id)
        if len({m.term_id for m in self.mappings}) != len(self.mappings):
            raise EvidenceError("mapping_duplicate", self.reference_id)
        for mapping in self.mappings:
            if any(t not in taxa for t in mapping.taxon_ids):
                raise EvidenceError("dangling_taxon_mapping", mapping.term_id)
        return self
