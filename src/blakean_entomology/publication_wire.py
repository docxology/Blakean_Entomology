"""Hash-bound stdlib transport for the separately selected template runtime."""

import configparser
import csv
import hashlib
from pathlib import Path
from typing import Final, assert_never

from .publication_profile import verify_host_profile
from .publication_transport_models import Member, NativeTransport, PublicationError, Role

TEMPLATE_COMMIT: Final = "efce6d6f5b3c4e8e2bbf92d8250855a0a9389ae8"
SDK_COMMIT: Final = "45171a099a6a658c52ab689501de646a28485653"
CURRENT_SDK_COMMIT: Final = "d34876e021a8f2e654b96f1c23f7ec43d8d958c2"


def sdk_profile(schema: int, commit: str) -> bool:
    """Historical bytes stay readable; new staging has an explicit current profile."""
    return (schema, commit) in ((1, SDK_COMMIT), (2, CURRENT_SDK_COMMIT))


def read_transport(stage: Path, expected: str) -> NativeTransport:
    """A caller-held INI hash closes the CSV inventory, variables and Pydantic plan."""
    try:
        return _read_transport(stage, expected)
    except (OSError, UnicodeError, ValueError, KeyError, csv.Error, configparser.Error) as error:
        raise PublicationError("native_transport_contract", str(stage)) from error


def _read_transport(stage: Path, expected: str) -> NativeTransport:
    raw = (stage / "native-transport.ini").read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise PublicationError("native_transport_pin", str(stage))
    config = configparser.ConfigParser(interpolation=None)
    config.read_string(raw.decode())
    meta = config["native"]
    try:
        schema = int(meta.get("schema_version", "1"))
    except ValueError as error:
        raise PublicationError("native_schema", str(stage)) from error
    if meta["template_commit"] != TEMPLATE_COMMIT or not sdk_profile(schema, meta["sdk_commit"]):
        raise PublicationError("native_declared_pin", str(stage))
    if meta["source_order"] != "00_frontmatter.md,10_article.md":
        raise PublicationError("native_source_order", str(stage))
    if meta["source_date_epoch"] != "1793318400":
        raise PublicationError("native_source_date_epoch", str(stage))
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
    identity = None
    if schema == 2:
        identity = Member(
            "installed-sdk.json", int(meta["sdk_identity_size"]), meta["sdk_identity_sha256"]
        )
        path = stage / identity.path
        if (
            identity not in inputs
            or path.is_symlink()
            or path.stat().st_size != identity.size
            or hashlib.sha256(path.read_bytes()).hexdigest() != identity.sha256
        ):
            raise PublicationError("native_sdk_identity", str(stage))
        verify_host_profile(stage, meta["sdk_commit"], tuple(inputs))
    return NativeTransport(
        meta["template_commit"],
        meta["sdk_commit"],
        identity,
        int(meta["source_date_epoch"]),
        tuple(meta["source_order"].split(",")),
        tuple(inputs),
        tuple(sources),
        templates,
        variables,
    )
