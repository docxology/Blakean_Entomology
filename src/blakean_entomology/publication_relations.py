"""Concise graphical readings tied one-to-one to the unchanged authored casebook."""

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True, slots=True)
class CaseRelation:
    case_id: str
    relation: str
    reading: str
    alternative: str


RELATIONS: Final = (
    CaseRelation(
        "care-and-route",
        "PROVISION",
        "Light and sound offer the emmet a route; homecoming remains unreported.",
        "The watchman's office can also imply ordered social roles.",
    ),
    CaseRelation(
        "thought-and-injury",
        "ATTENTION AFTER INJURY",
        "An injury becomes a reciprocal human/fly analogy.",
        "The speaker's consolation can displace the injured fly.",
    ),
    CaseRelation(
        "hidden-agent",
        "HIDDEN HARM",
        "Secret love destroys; the agent's anatomy remains invisible.",
        "Erotic, pathological and animal senses remain live.",
    ),
    CaseRelation(
        "brain-tree",
        "FEEDING ON MYSTERY",
        "Insects feed on mystery in a tree rooted in the human brain.",
        "Beneficiary and figure of obscurity are both possible.",
    ),
    CaseRelation(
        "press-and-positions",
        "UNEQUAL POSITIONS",
        "Dancing life around the press contrasts with suffering human grapes within.",
        "Transformation does not erase unequal positions.",
    ),
    CaseRelation(
        "cherishing",
        "CHERISHING",
        "The Clay's care adds nourishment to protection against injury.",
        "Maternal and nuptial language makes this care particular.",
    ),
    CaseRelation(
        "joined-body",
        "AGGREGATION",
        "A joined body raises the problem of collective embodiment.",
        "Text and a catalog's visual alternative cannot fix one universal function.",
    ),
)
