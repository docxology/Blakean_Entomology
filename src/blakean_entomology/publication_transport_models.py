"""Stdlib transport values; no SDK, Pydantic or renderer imports."""

import re
from dataclasses import dataclass
from enum import StrEnum
from pathlib import PurePosixPath


class PublicationError(Exception):
    """Typed refusal; Python/Click must be able to attach its traceback."""

    def __init__(self, code: str, detail: str) -> None:
        self.code: str = code
        self.detail: str = detail
        super().__init__(f"{code}: {detail}")


@dataclass(frozen=True, slots=True)
class Member:
    path: str
    size: int
    sha256: str

    def __post_init__(self) -> None:
        path = PurePosixPath(self.path)
        if (
            path.is_absolute()
            or ".." in path.parts
            or not path.parts
            or path.as_posix() != self.path
            or "\\" in self.path
            or self.size < 0
            or not re.fullmatch("[0-9a-f]{64}", self.sha256)
        ):
            raise PublicationError("stage_member_contract", self.path)


class Role(StrEnum):
    INPUT = "input"
    SOURCE = "source"
    TEMPLATE = "template"


@dataclass(frozen=True, slots=True)
class NativeTransport:
    template_commit: str
    sdk_commit: str
    sdk_identity: Member | None
    source_date_epoch: int
    source_order: tuple[str, ...]
    inputs: tuple[Member, ...]
    sources: tuple[Member, ...]
    template_sources: dict[str, str]
    variables: dict[str, str]
