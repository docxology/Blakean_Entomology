"""Stdlib validation of the application's closed native SDK profile.

This checks the host's structured report and request/stage consistency. It does
not import or independently observe the SDK in the template worker's runtime.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias

from .publication_custody import checked_member, file_hash
from .publication_transport_models import Member, PublicationError

JSONValue: TypeAlias = "None | bool | int | float | str | list[JSONValue] | JSONObject"


@dataclass(frozen=True, slots=True)
class JSONObject:
    fields: dict[str, JSONValue]


def _load(path: Path) -> JSONObject:
    objects: list[JSONObject] = []

    def collect(pairs: list[tuple[str, JSONValue]]) -> JSONObject:
        fields = dict(pairs)
        if len(fields) != len(pairs):
            raise PublicationError("native_profile_json", "Duplicate JSON member")
        result = JSONObject(fields)
        objects.append(result)
        return result

    text = path.read_text()
    if not text.lstrip().startswith("{"):
        raise PublicationError("native_profile_json", "Require a JSON object")
    # The stdlib decoder supplies JSON primitives plus our typed object hook.
    # Its return is intentionally unused; the final postorder object is the root.
    json.loads(text, object_pairs_hook=collect)
    return objects[-1]


def _text(value: JSONValue) -> str:
    if not isinstance(value, str) or not value:
        raise PublicationError("native_profile_text", "Require a nonempty string")
    return value


def _object(value: JSONValue) -> JSONObject:
    if not isinstance(value, JSONObject):
        raise PublicationError("native_profile_object", "Require an object")
    return value


def _integer(value: JSONValue) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise PublicationError("native_profile_integer", "Require a nonnegative integer")
    return value


def _selection(record: JSONObject, commit: str) -> None:
    if (
        _integer(record.fields.get("schema_version")) != 2
        or _text(record.fields.get("sdk_commit")) != commit
    ):
        raise PublicationError("native_profile_selection", "Request/stage SDK selection differs")


def _identity(record: JSONObject, commit: str) -> None:
    fields = record.fields
    if set(fields) != {
        "distribution",
        "package",
        "version",
        "commit",
        "package_root",
        "direct_url_sha256",
        "metadata_sha256",
        "record_sha256",
        "files",
        "imported_modules",
    }:
        raise PublicationError("native_profile_identity", "SDK receipt fields differ")
    if (
        fields["commit"] != commit
        or fields["package"] != "blake"
        or fields["distribution"] != "blake"
    ):
        raise PublicationError("native_profile_identity", "SDK identity differs")
    _ = _text(fields["version"])
    if not Path(_text(fields["package_root"])).is_absolute():
        raise PublicationError("native_profile_identity", "Require an absolute package root")
    for name in ("direct_url_sha256", "metadata_sha256", "record_sha256"):
        if not re.fullmatch("[0-9a-f]{64}", _text(fields[name])):
            raise PublicationError("native_profile_identity", "Invalid metadata digest")
    files = fields["files"]
    imports = fields["imported_modules"]
    if not isinstance(files, list) or not files or not isinstance(imports, list) or not imports:
        raise PublicationError("native_profile_identity", "Require file/import inventories")
    names: set[str] = set()
    for item in files:
        entry = _object(item).fields
        if set(entry) != {"path", "size", "sha256"}:
            raise PublicationError("native_profile_identity", "Invalid SDK member fields")
        member = Member(_text(entry["path"]), _integer(entry["size"]), _text(entry["sha256"]))
        if member.path in names:
            raise PublicationError("native_profile_identity", "Duplicate SDK member")
        names.add(member.path)
    modules = tuple(_text(name) for name in imports)
    if "__init__.py" not in names or "blake" not in modules or len(modules) != len(set(modules)):
        raise PublicationError("native_profile_identity", "Incomplete SDK inventory")


def verify_host_profile(stage: Path, commit: str, inputs: tuple[Member, ...]) -> None:
    """Refuse malformed or contradictory closed host/request/stage evidence."""
    for name in ("installed-sdk.json", "native-request.json"):
        selected = tuple(member for member in inputs if member.path == name)
        if len(selected) != 1:
            raise PublicationError("native_profile_membership", name)
        checked_member(stage, selected[0])
    identity = _load(stage / "installed-sdk.json")
    request = _load(stage / "native-request.json")
    plan = _load(stage / "native-stage.json")
    _identity(identity, commit)
    _selection(request, commit)
    _selection(plan, commit)
    if _object(plan.fields.get("sdk_identity")) != identity:
        raise PublicationError("native_profile_identity", "Stage and host receipt differ")
    if plan.fields.get("request_sha256") != file_hash(stage / "native-request.json"):
        raise PublicationError("native_profile_request", "Stage/request digest differs")
