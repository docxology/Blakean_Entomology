"""Current host SDK admission and archival native-profile controls."""

import configparser
import csv
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from blake.methods.installed_models import InstalledFile, InstalledGitPackage
from pydantic import ValidationError

from blakean_entomology.publication import prepare_native_stage
from blakean_entomology.publication_contract import NativeRequest, NativeStage, PinnedInput
from blakean_entomology.publication_sdk import admit_native_sdk
from blakean_entomology.publication_transport_models import PublicationError
from blakean_entomology.publication_wire import (
    CURRENT_SDK_COMMIT,
    SDK_COMMIT,
    TEMPLATE_COMMIT,
    read_transport,
)

ROOT = Path(__file__).resolve().parents[1]


def request(schema: int = 3, commit: str = CURRENT_SDK_COMMIT) -> NativeRequest:
    pin = PinnedInput(path=Path("absent-input"), sha256="a" * 64)
    return NativeRequest.model_validate(
        {
            "schema_version": schema,
            "sdk_commit": commit,
            **{
                name: pin
                for name in (
                    "prepared",
                    "atlas",
                    "composition",
                    "casebook",
                    "cover",
                    "cover_provenance",
                    "config",
                    "preamble",
                    "web_css",
                )
            },
        }
    )


def identity(commit: str = CURRENT_SDK_COMMIT) -> InstalledGitPackage:
    """Synthetic model fixture only; actual installed evidence is checked separately."""
    return InstalledGitPackage(
        distribution="blake",
        package="blake",
        version="0.7.0",
        commit=commit,
        package_root=Path("/fixture"),
        direct_url_sha256="a" * 64,
        metadata_sha256="b" * 64,
        record_sha256="c" * 64,
        files=(InstalledFile(path="__init__.py", size=0, sha256="a" * 64),),
        imported_modules=("blake",),
    )


def stage_fields() -> dict[str, str | dict[str, str] | tuple[str, ...]]:
    return {
        "template_sources": {},
        "source_order": ("00_frontmatter.md", "10_article.md"),
        "request_sha256": "a" * 64,
        "inputs": (),
        "sources": (),
        "frontmatter_data_sha256": "b" * 64,
    }


def test_historical_contract_remains_readable_but_cannot_start_new_production(tmp_path) -> None:
    archived = request(1, SDK_COMMIT)
    retained = NativeStage.model_validate(
        {**stage_fields(), "schema_version": 1, "sdk_commit": SDK_COMMIT}
    )
    assert retained.sdk_identity is None
    output = tmp_path / "analysis_output/new"
    # Historical production refuses before reading even an absent input or writing output.
    with pytest.raises(PublicationError, match="native_historical_profile"):
        prepare_native_stage(archived, output, tmp_path)
    assert not output.exists()


@pytest.mark.parametrize(
    "schema,commit", [(1, CURRENT_SDK_COMMIT), (2, SDK_COMMIT), (2, "0" * 40), (2, "main")]
)
def test_request_refuses_crossed_or_unselected_profiles(schema, commit) -> None:
    with pytest.raises(ValidationError, match="native_sdk_profile"):
        request(schema, commit)


def test_current_stage_carries_selected_pin_and_host_identity() -> None:
    current = NativeStage.model_validate({**stage_fields(), "sdk_identity": identity()})
    assert current.schema_version == 3
    assert current.sdk_commit == current.sdk_identity.commit == CURRENT_SDK_COMMIT


@pytest.mark.parametrize("change", ["absent", "wrong_pin", "wrong_package", "historical"])
def test_stage_refuses_missing_or_crossed_host_identity(change) -> None:
    raw = {**stage_fields(), "sdk_identity": identity().model_dump()}
    if change == "absent":
        raw["sdk_identity"] = None
    elif change == "wrong_pin":
        raw["sdk_identity"]["commit"] = "f" * 40
    elif change == "wrong_package":
        raw["sdk_identity"]["package"] = "another"
    else:
        raw.update(schema_version=1, sdk_commit=SDK_COMMIT)
    with pytest.raises(ValidationError, match="native_sdk_identity"):
        NativeStage.model_validate(raw)


def write_current_transport(
    root: Path,
    *,
    schema: int = 3,
    commit: str = CURRENT_SDK_COMMIT,
    version: str = "0.7.0",
) -> str:
    sdk = identity(commit).model_copy(update={"version": version})
    payload = sdk.model_dump_json().encode()
    (root / "installed-sdk.json").write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    request_bytes = request(schema, commit).model_dump_json().encode()
    (root / "native-request.json").write_bytes(request_bytes)
    request_sha = hashlib.sha256(request_bytes).hexdigest()
    with (root / "native-wire.csv").open("w", newline="") as stream:
        csv.writer(stream).writerows(
            (
                ("input", "installed-sdk.json", len(payload), digest),
                ("input", "native-request.json", len(request_bytes), request_sha),
            )
        )
    (root / "native-stage.json").write_text(
        json.dumps(
            {
                "schema_version": schema,
                "sdk_commit": commit,
                "sdk_identity": sdk.model_dump(mode="json"),
                "request_sha256": request_sha,
            }
        )
    )
    (root / "manuscript_variables.csv").write_text("PAPER_TITLE,Fixture\n")
    config = configparser.ConfigParser(interpolation=None)
    config["native"] = {
        "schema_version": str(schema),
        "template_commit": TEMPLATE_COMMIT,
        "sdk_commit": commit,
        "source_date_epoch": "1793318400",
        "source_order": "00_frontmatter.md,10_article.md",
        "wire_sha256": hashlib.sha256((root / "native-wire.csv").read_bytes()).hexdigest(),
        "stage_sha256": hashlib.sha256((root / "native-stage.json").read_bytes()).hexdigest(),
        "sdk_identity_size": str(len(payload)),
        "sdk_identity_sha256": digest,
    }
    with (root / "native-transport.ini").open("w") as stream:
        config.write(stream)
    return hashlib.sha256((root / "native-transport.ini").read_bytes()).hexdigest()


def test_current_transport_retains_closed_host_receipt_without_importing_sdk(tmp_path) -> None:
    pin = write_current_transport(tmp_path)
    plan = read_transport(tmp_path, pin)
    assert plan.sdk_commit == CURRENT_SDK_COMMIT
    assert plan.sdk_identity in plan.inputs


@pytest.mark.parametrize("mutation", ["bytes", "size", "membership", "symlink"])
def test_current_transport_refuses_identity_drift(tmp_path, mutation) -> None:
    pin = write_current_transport(tmp_path)
    path = tmp_path / "installed-sdk.json"
    if mutation == "bytes":
        path.write_bytes(b"x" * path.stat().st_size)
    elif mutation == "symlink":
        target = tmp_path / "outside.json"
        path.rename(target)
        path.symlink_to(target)
    else:
        config = configparser.ConfigParser(interpolation=None)
        config.read(tmp_path / "native-transport.ini")
        if mutation == "size":
            config["native"]["sdk_identity_size"] = "0"
        else:
            (tmp_path / "native-wire.csv").write_text("")
            config["native"]["wire_sha256"] = hashlib.sha256(b"").hexdigest()
        with (tmp_path / "native-transport.ini").open("w") as stream:
            config.write(stream)
        pin = hashlib.sha256((tmp_path / "native-transport.ini").read_bytes()).hexdigest()
    with pytest.raises(PublicationError, match="native_sdk_identity"):
        read_transport(tmp_path, pin)


def test_actual_normal_sdk_is_admitted_at_the_selected_commit() -> None:
    receipt = admit_native_sdk(request())
    assert receipt.commit == CURRENT_SDK_COMMIT
    assert receipt.distribution == receipt.package == "blake"
    assert len(receipt.files) > 100


@pytest.mark.parametrize("failure", ["missing_identity", "malformed_size", "missing_size"])
def test_transport_parser_errors_are_named_refusals(tmp_path, failure) -> None:
    pin = write_current_transport(tmp_path)
    if failure == "missing_identity":
        (tmp_path / "installed-sdk.json").unlink()
    else:
        path = tmp_path / "native-transport.ini"
        config = configparser.ConfigParser(interpolation=None)
        config.read(path)
        if failure == "missing_size":
            del config["native"]["sdk_identity_size"]
        else:
            config["native"]["sdk_identity_size"] = "not-an-integer"
        with path.open("w") as stream:
            config.write(stream)
        pin = hashlib.sha256(path.read_bytes()).hexdigest()
    with pytest.raises(PublicationError):
        read_transport(tmp_path, pin)


def test_shadow_import_refuses_before_output_in_real_child(tmp_path) -> None:
    shadow = tmp_path / "shadow.py"
    shadow.write_text("# real mismatching file\n")
    output = tmp_path / "analysis_output/refused"
    script = (
        "from pathlib import Path\nimport blake\n"
        "from test_native_sdk import request\n"
        "from blakean_entomology.publication import prepare_native_stage\n"
        f"blake.__file__ = {str(shadow)!r}\n"
        f"prepare_native_stage(request(), Path({str(output)!r}), Path('.'))\n"
    )
    environment = dict(
        os.environ, PYTHONPATH=os.pathsep.join((str(ROOT / "tests"), str(ROOT / "src")))
    )
    result = subprocess.run(
        [sys.executable, "-B", "-c", script],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "native_sdk_installed_import" in result.stderr
    assert not output.exists()
