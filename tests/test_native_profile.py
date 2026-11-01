"""Adversarial hash-closed SDK/request/stage semantics, separate from host imports."""

import configparser
import csv
import hashlib
import json

import pytest
from test_native_sdk import write_current_transport

from blakean_entomology.publication_transport_models import PublicationError
from blakean_entomology.publication_wire import read_transport


def rebind(root) -> str:
    wire = root / "native-wire.csv"
    with wire.open(newline="") as stream:
        rows = list(csv.reader(stream))
    for row in rows:
        payload = (root / row[1]).read_bytes()
        row[2:] = [str(len(payload)), hashlib.sha256(payload).hexdigest()]
    with wire.open("w", newline="") as stream:
        csv.writer(stream).writerows(rows)
    config = configparser.ConfigParser(interpolation=None)
    config.read(root / "native-transport.ini")
    for name, key in (
        ("native-wire.csv", "wire_sha256"),
        ("native-stage.json", "stage_sha256"),
        ("installed-sdk.json", "sdk_identity_sha256"),
    ):
        config["native"][key] = hashlib.sha256((root / name).read_bytes()).hexdigest()
    config["native"]["sdk_identity_size"] = str((root / "installed-sdk.json").stat().st_size)
    with (root / "native-transport.ini").open("w") as stream:
        config.write(stream)
    return hashlib.sha256((root / "native-transport.ini").read_bytes()).hexdigest()


@pytest.mark.parametrize(
    "mutation",
    [
        "non_json",
        "root_array",
        "duplicate_json",
        "sdk_commit",
        "sdk_package",
        "sdk_fields",
        "sdk_empty_files",
        "sdk_bad_member",
        "sdk_duplicate_member",
        "sdk_bad_size",
        "sdk_bad_digest",
        "sdk_relative_root",
        "sdk_empty_imports",
        "sdk_no_root_import",
        "sdk_duplicate_import",
        "stage_commit",
        "stage_schema",
        "stage_identity",
        "stage_request_hash",
        "request_commit",
        "missing_request",
        "empty_text",
        "wrong_object",
    ],
)
def test_rebound_but_invalid_profile_refuses(tmp_path, mutation) -> None:
    # Given valid real files, deliberately rebind their changed bytes as a producer bug could.
    _ = write_current_transport(tmp_path)
    sdk = tmp_path / "installed-sdk.json"
    stage = tmp_path / "native-stage.json"
    request = tmp_path / "native-request.json"
    data = json.loads(sdk.read_text())
    plan = json.loads(stage.read_text())
    specification = json.loads(request.read_text())
    if mutation in {"non_json", "root_array", "duplicate_json"}:
        sdk.write_text(
            {
                "non_json": "broken",
                "root_array": "[]",
                "duplicate_json": '{"commit":"a","commit":"b"}',
            }[mutation]
        )
    elif mutation.startswith("sdk_") or mutation in {"empty_text", "wrong_object"}:
        if mutation == "sdk_commit":
            data["commit"] = "f" * 40
        elif mutation == "sdk_package":
            data["package"] = "another"
        elif mutation == "sdk_fields":
            data["extra"] = "unexpected"
        elif mutation == "sdk_empty_files":
            data["files"] = []
        elif mutation == "sdk_bad_member":
            data["files"][0]["extra"] = "unexpected"
        elif mutation == "sdk_duplicate_member":
            data["files"].append(data["files"][0])
        elif mutation == "sdk_bad_size":
            data["files"][0]["size"] = True
        elif mutation == "sdk_bad_digest":
            data["record_sha256"] = "not-a-digest"
        elif mutation == "sdk_relative_root":
            data["package_root"] = "relative"
        elif mutation == "sdk_empty_imports":
            data["imported_modules"] = []
        elif mutation == "sdk_no_root_import":
            data["imported_modules"] = ["blake.child"]
        elif mutation == "sdk_duplicate_import":
            data["imported_modules"] = ["blake", "blake"]
        elif mutation == "empty_text":
            data["version"] = ""
        elif mutation == "wrong_object":
            data["files"] = [1]
        sdk.write_text(json.dumps(data))
        plan["sdk_identity"] = data
        stage.write_text(json.dumps(plan))
    elif mutation == "request_commit":
        specification["sdk_commit"] = "f" * 40
        request.write_text(json.dumps(specification))
        plan["request_sha256"] = hashlib.sha256(request.read_bytes()).hexdigest()
        stage.write_text(json.dumps(plan))
    elif mutation == "missing_request":
        with (tmp_path / "native-wire.csv").open("w", newline="") as stream:
            csv.writer(stream).writerow(
                (
                    "input",
                    "installed-sdk.json",
                    sdk.stat().st_size,
                    hashlib.sha256(sdk.read_bytes()).hexdigest(),
                )
            )
    else:
        if mutation == "stage_commit":
            plan["sdk_commit"] = "f" * 40
        elif mutation == "stage_schema":
            plan["schema_version"] = True
        elif mutation == "stage_identity":
            plan["sdk_identity"]["version"] = "different"
        elif mutation == "stage_request_hash":
            plan["request_sha256"] = "0" * 64
        stage.write_text(json.dumps(plan))
    pin = rebind(tmp_path)
    # When supplied with the correctly rebound outer pin.
    with pytest.raises(PublicationError):
        read_transport(tmp_path, pin)
    # Then closure alone cannot promote contradictory host metadata to admission.
