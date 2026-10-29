"""Application custody and explicit contextual review contracts."""

from enum import StrEnum
from typing import Literal, Self, assert_never

from blake.methods.models import Artifact as Artifact
from blake.methods.models import BundleCorpusPin as CorpusPin
from blake.methods.models import Digest, FrozenModel
from blake.methods.models import EvidenceError as EvidenceError
from pydantic import Field, model_validator

__all__ = [
    "Artifact",
    "CorpusPin",
    "Decision",
    "EvidenceError",
    "ReviewDecision",
    "ReviewSummary",
    "RunReceipt",
    "is_animal_decision",
]


class RunReceipt(FrozenModel):
    schema_version: Literal[1] = 1
    application: Literal["blakean-entomology"] = "blakean-entomology"
    application_version: str
    application_code_sha256: Digest
    corpus_pin: CorpusPin
    spec_sha256: Digest
    methods_sha256: Digest
    normalization: str
    files: tuple[Artifact, ...]
    scope: str = (
        "Exhaustive category-span retrieval for the declared vocabulary and pinned bytes. "
        "All candidates remain unreviewed until an explicitly bound review."
    )


class Decision(StrEnum):
    ANIMAL_LITERAL = "animal_literal"
    ANIMAL_FIGURATIVE = "animal_figurative"
    ASSOCIATED = "associated"
    NON_ANIMAL = "non_animal"
    EDITORIAL = "editorial"
    UNCERTAIN = "uncertain"


def is_animal_decision(decision: Decision) -> bool:
    """Keep animal coding explicit when the review vocabulary changes."""
    match decision:
        case Decision.ANIMAL_LITERAL | Decision.ANIMAL_FIGURATIVE:
            return True
        case Decision.ASSOCIATED | Decision.NON_ANIMAL | Decision.EDITORIAL | Decision.UNCERTAIN:
            return False
    assert_never(decision)


class ReviewDecision(FrozenModel):
    run_sha256: Digest
    hit_id: str = Field(min_length=1)
    decision: Decision
    reviewer: str = Field(min_length=1)
    rationale: str = Field(min_length=1)
    verification_locator: str = ""

    @model_validator(mode="after")
    def require_animal_locator(self) -> Self:
        if is_animal_decision(self.decision):
            if not self.verification_locator.strip():
                raise EvidenceError("animal_locator_required", self.hit_id)
        if not self.reviewer.strip() or not self.rationale.strip():
            raise EvidenceError("reviewer_and_rationale_required", self.hit_id)
        return self


class ReviewSummary(FrozenModel):
    application_version: str
    application_code_sha256: Digest
    run_sha256: Digest
    decisions_sha256: Digest
    candidate_hits: int = Field(ge=0)
    reviewed_hits: int = Field(ge=0)
    unreviewed_hits: int = Field(ge=0)
    decisions: dict[Decision, int]
    primary_animal_hits: int = Field(ge=0)
    exploratory_animal_hits: int = Field(ge=0)
    note: str = (
        "Animal decisions do not change source authorship labels. Counts retain category "
        "overlap and repeated editions; they are not distinct organisms or species."
    )
