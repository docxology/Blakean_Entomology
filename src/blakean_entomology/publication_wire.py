"""Hash-bound stdlib transport for the separately selected template runtime."""

import configparser
import csv
import hashlib
import re
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Final, assert_never

from typing_extensions import override

TEMPLATE_COMMIT: Final = "efce6d6f5b3c4e8e2bbf92d8250855a0a9389ae8"
SDK_COMMIT: Final = "45171a099a6a658c52ab689501de646a28485653"


@dataclass(slots=True)
class PublicationError(Exception):
    """Typed refusal; Python/Click must be able to attach its traceback."""

    code: str
    detail: str

    @override
    def __str__(self) -> str:
        return f"{self.code}: {self.detail}"


@dataclass(frozen=True, slots=True)
class Member:
    path: str
    size: int
    sha256: str

    def __post_init__(self) -> None:
        if (
            Path(self.path).is_absolute()
            or ".." in Path(self.path).parts
            or not self.path
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
    source_date_epoch: int
    source_order: tuple[str, ...]
    inputs: tuple[Member, ...]
    sources: tuple[Member, ...]
    template_sources: dict[str, str]
    variables: dict[str, str]


def read_transport(stage: Path, expected: str) -> NativeTransport:
    """A caller-held INI hash closes the CSV inventory, variables and Pydantic plan."""
    raw = (stage / "native-transport.ini").read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise PublicationError("native_transport_pin", str(stage))
    config = configparser.ConfigParser(interpolation=None)
    config.read_string(raw.decode())
    meta = config["native"]
    if meta["template_commit"] != TEMPLATE_COMMIT or meta["sdk_commit"] != SDK_COMMIT:
        raise PublicationError("native_declared_pin", str(stage))
    if meta["source_order"] != "00_frontmatter.md,10_article.md":
        raise PublicationError("native_source_order", str(stage))
    for name, key in (("native-wire.csv", "wire_sha256"), ("native-stage.json", "stage_sha256")):
        if hashlib.sha256((stage / name).read_bytes()).hexdigest() != meta[key]:
            raise PublicationError("native_transport_member", name)
    inputs: list[Member] = []
    sources: list[Member] = []
    templates: dict[str, str] = {}
    with (stage / "native-wire.csv").open(newline="") as stream:
        for row in csv.reader(stream):
            if len(row) != 4:
                raise PublicationError("native_transport_row", str(row))
            role = Role(row[0])
            record = Member(row[1], int(row[2]), row[3])
            match role:
                case Role.INPUT:
                    inputs.append(record)
                case Role.SOURCE:
                    sources.append(record)
                case Role.TEMPLATE:
                    if record.path in templates:
                        raise PublicationError("native_transport_duplicate", record.path)
                    templates[record.path] = record.sha256
                case _:
                    assert_never(role)
    variables: dict[str, str] = {}
    with (stage / "manuscript_variables.csv").open(newline="") as stream:
        for row in csv.reader(stream):
            if len(row) != 2 or row[0] in variables:
                raise PublicationError("native_variable_row", str(row))
            variables[row[0]] = row[1]
    return NativeTransport(
        meta["template_commit"],
        int(meta["source_date_epoch"]),
        tuple(meta["source_order"].split(",")),
        tuple(inputs),
        tuple(sources),
        templates,
        variables,
    )
