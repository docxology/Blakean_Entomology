"""Private registry-channel policy and adapters over public composition methods."""

from typing import Annotated, Final, Literal

from blake.methods.composition import GroupedInventory, inventory_from_strata
from blake.methods.composition import composition_audit as audit_groups
from blake.methods.models import EvidenceError, FrozenModel
from blake.methods.statistics_models import QuerySummary, Stratum
from blake.studies import StudySpec
from pydantic import Field

Count = Annotated[int, Field(ge=0, strict=True)]
NAME_GROUPS: Final = frozenset(
    {
        "worm",
        "insect",
        "arachnid",
        "myriapod",
        "mollusc",
        "crustacean",
        "ambiguous_life",
    }
)
ChannelName = Literal["name_family", "broad_label", "associated", "motion"]
CHANNELS: Final[dict[str, ChannelName]] = {
    **dict.fromkeys(NAME_GROUPS, "name_family"),
    "generic": "broad_label",
    "associated": "associated",
    "motion": "motion",
}
LITERAL_PAIRS: Final[tuple[tuple[str, str], ...]] = (
    ("worm", "fly"),
    ("worm", "beetle"),
    ("emmet", "beetle"),
    ("spider", "fly"),
    ("spider", "beetle"),
    ("bee", "beetle"),
    ("gnat", "fly"),
    ("caterpillar", "fly"),
    ("polypus", "worm"),
    ("moth", "butterfly"),
    ("flea", "louse"),
    ("scorpion", "centipede"),
)
WIDTHS: Final[tuple[int | None, ...]] = (8, 32, 64, None)


class CompositionContrast(FrozenModel):
    category: str
    candidates: Count
    exact_text_candidates: Count
    matched_units: Count
    positive_work_groups: Count
    pooled_share: float | None
    equal_nonempty_group_share: float | None
    difference_percentage_points: float | None
    minimum_groups_for_half: int | None
    minimum_groups_for_four_fifths: int | None
    effective_groups: float | None


class OmissionEffect(FrozenModel):
    omitted_work_id: str
    omitted_source_units: Count
    omitted_tokens: Count
    removed_name_candidates: Count
    remaining_name_candidates: Count
    composition_tv_from_full: float | None
    leading_category: str | None


class CompositionAudit(FrozenModel):
    schema_version: Literal[1] = 1
    category_ids: tuple[str, ...]
    source_units: Count
    tokens: Count
    work_groups: Count
    nonempty_name_work_groups: Count
    name_category_candidates: Count
    pooled_vs_equal_nonempty_tv: float | None
    categories: tuple[CompositionContrast, ...]
    omissions: tuple[OmissionEffect, ...]
    limits: str = (
        "Shares divide sums of name-family category-source-span candidates, retaining "
        "nested and intersecting categories, copies, derivatives, homographs and verbs. "
        "Equal composition weights only groups with a positive name-channel sum; empty "
        "groups have undefined composition and remain in coverage exports. Total variation "
        "is a finite profile distance, not a significance test. Effective groups are "
        "inverse concentration, not a count of independent works."
    )


def inventory_from_atlas(spec: StudySpec, works: tuple[Stratum, ...]) -> GroupedInventory:
    """Select declared name-family channels, including every zero category/group."""
    if any(t.group not in CHANNELS for t in spec.terms):
        raise EvidenceError("composition_channel", "unknown registry channel")
    ids = tuple(t.term_id for t in spec.terms if t.group in NAME_GROUPS)
    return inventory_from_strata(ids, works)


def composition_audit(
    inventory: GroupedInventory, summaries: tuple[QuerySummary, ...]
) -> CompositionAudit:
    """Add domain labels without copying any generic composition arithmetic."""
    result = audit_groups(inventory, summaries)
    return CompositionAudit(
        category_ids=result.category_ids,
        source_units=result.source_units,
        tokens=result.tokens,
        work_groups=result.groups,
        nonempty_name_work_groups=result.nonempty_groups,
        name_category_candidates=result.category_candidates,
        pooled_vs_equal_nonempty_tv=result.pooled_vs_equal_nonempty_tv,
        categories=tuple(
            CompositionContrast(
                category=r.category,
                candidates=r.candidates,
                exact_text_candidates=r.exact_text_candidates,
                matched_units=r.matched_units,
                positive_work_groups=r.positive_groups,
                pooled_share=r.pooled_share,
                equal_nonempty_group_share=r.equal_nonempty_group_share,
                difference_percentage_points=r.difference_percentage_points,
                minimum_groups_for_half=r.minimum_groups_for_half,
                minimum_groups_for_four_fifths=r.minimum_groups_for_four_fifths,
                effective_groups=r.effective_groups,
            )
            for r in result.categories
        ),
        omissions=tuple(
            OmissionEffect(
                omitted_work_id=r.omitted_group_id,
                omitted_source_units=r.omitted_source_units,
                omitted_tokens=r.omitted_tokens,
                removed_name_candidates=r.removed_candidates,
                remaining_name_candidates=r.remaining_candidates,
                composition_tv_from_full=r.composition_tv_from_full,
                leading_category=r.leading_category,
            )
            for r in result.omissions
        ),
    )
