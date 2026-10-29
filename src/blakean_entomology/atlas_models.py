"""Text-free corpus atlas: explicit denominators, lexical forms and review epochs."""

from typing import Literal, Self

from blake.methods.models import Digest, EvidenceError, FrozenModel
from blake.methods.profiles import RuntimeProfile
from blake.methods.statistics_models import QuerySummary, Stratum
from blake.studies import StudyDenominator, StudyRow
from pydantic import Field, model_validator

from .models import CorpusPin


class FormCoverage(FrozenModel):
    term_id: str
    form: str
    normalized_tokens: tuple[str, ...]
    equivalent_form_candidates: int = Field(ge=0)
    exact_surface_candidates: int = Field(ge=0)
    primary_equivalent_form_candidates: int = Field(ge=0)
    primary_exact_surface_candidates: int = Field(ge=0)


class VocabularyOverlap(FrozenModel):
    normalized_tokens: tuple[str, ...]
    forms: tuple[str, ...]
    categories: tuple[str, ...]


class CoverageCohort(FrozenModel):
    role: str
    plane: str
    author_id: str
    source_units: int = Field(gt=0)
    tokens: int = Field(ge=0)
    exact_text_units: int = Field(gt=0)
    work_groups: int = Field(gt=0)
    inventory_sha256: Digest
    categories: tuple[QuerySummary, ...]
    works: tuple[Stratum, ...]


class ReviewEpoch(FrozenModel):
    run_sha256: Digest
    decisions_sha256: Digest
    candidate_hits: int = Field(ge=0)
    reviewed_hits: int = Field(ge=0)
    unreviewed_hits: int = Field(ge=0)
    transferred_to_atlas: Literal[False] = False

    @model_validator(mode="after")
    def reconcile(self) -> Self:
        if self.reviewed_hits + self.unreviewed_hits != self.candidate_hits:
            raise EvidenceError("review_denominator", self.run_sha256)
        return self


class AtlasReceipt(FrozenModel):
    schema_version: Literal[1] = 1
    epoch: Literal["invertebrate-atlas-v1"] = "invertebrate-atlas-v1"
    application_code_sha256: Digest
    corpus_pin: CorpusPin
    vocabulary_sha256: Digest
    reference_sha256: Digest
    methods_sha256: Digest
    profile: RuntimeProfile
    count_unit: Literal["category-source-span candidates"] = "category-source-span candidates"
    scanned_units: int = Field(gt=0)
    candidates: int = Field(ge=0)
    primary_candidates: int = Field(ge=0)
    distinct_source_spans: int = Field(ge=0)
    multiply_categorized_spans: int = Field(ge=0)
    overlapping_candidate_pairs: int = Field(ge=0)
    category_count: int = Field(gt=0)
    explicit_form_count: int = Field(gt=0)
    denominators: tuple[StudyDenominator, ...]
    category_role_plane: tuple[StudyRow, ...]
    forms: tuple[FormCoverage, ...]
    normalized_alias_groups: tuple[VocabularyOverlap, ...]
    cohorts: tuple[CoverageCohort, ...]
    historical_review: ReviewEpoch | None
    historical_review_summary_sha256: Digest | None
    current_epoch_authored_decisions: Literal[0] = 0
    corpus_images_reviewed: Literal[False] = False
    limits: str = (
        "Counts retain copies and category overlap. Equal-work coverage averages within-work "
        "matched-unit fractions, including zero-match work groups. Exact-text grouping removes "
        "identical whole source units only. Recorded work IDs are not independent literary works. "
        "Historical decisions remain on their original run; this atlas adds no animal decisions."
    )

    @model_validator(mode="after")
    def denominators_reconcile(self) -> Self:
        if (
            self.candidates != sum(r.occurrences for r in self.category_role_plane)
            or self.scanned_units != sum(d.passages for d in self.denominators)
            or self.scanned_units != sum(c.source_units for c in self.cohorts)
            or self.distinct_source_spans > self.candidates
            or self.multiply_categorized_spans > self.distinct_source_spans
            or len(self.forms) != self.explicit_form_count
        ):
            raise EvidenceError("atlas_denominators", self.epoch)
        primary = tuple(
            c
            for c in self.cohorts
            if (c.role, c.plane, c.author_id) == ("primary", "reading", "william-blake-1757-1827")
        )
        if len(primary) != 1 or self.primary_candidates != sum(
            q.copy_retaining.occurrences for q in primary[0].categories
        ):
            raise EvidenceError("atlas_primary", self.epoch)
        for cohort in self.cohorts:
            if len(cohort.categories) != self.category_count or any(
                q.copy_retaining.source_units != cohort.source_units
                or q.copy_retaining.tokens != cohort.tokens
                or q.exact_text.source_units != cohort.exact_text_units
                for q in cohort.categories
            ):
                raise EvidenceError("atlas_cohort", cohort.author_id)
        if (self.historical_review is None) != (self.historical_review_summary_sha256 is None):
            raise EvidenceError("atlas_review_binding", self.epoch)
        return self
