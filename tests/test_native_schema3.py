"""Explicit historical profiles and the new normal-Git production selection."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError
from test_native_sdk import identity, request, stage_fields, write_current_transport

from blakean_entomology.publication_contract import NativeStage
from blakean_entomology.publication_sdk import admit_native_sdk
from blakean_entomology.publication_transport_models import PublicationError

NEW_PIN = "263d7c83abe6f1309a64af3285a683c1b7672269"
SCHEMA2_PIN = "d34876e021a8f2e654b96f1c23f7ec43d8d958c2"


def test_schema3_is_the_exact_new_profile() -> None:
    selected = request(3, NEW_PIN)
    assert selected.schema_version == 3
    current = identity(NEW_PIN).model_copy(update={"version": "0.7.0"})
    stage = NativeStage.model_validate(
        {**stage_fields(), "schema_version": 3, "sdk_commit": NEW_PIN, "sdk_identity": current}
    )
    assert stage.sdk_identity == current


def test_schema2_remains_readable_at_its_original_pin() -> None:
    selected = request(2, SCHEMA2_PIN)
    old = identity(SCHEMA2_PIN).model_copy(update={"version": "0.6.0"})
    stage = NativeStage.model_validate(
        {**stage_fields(), "schema_version": 2, "sdk_commit": SCHEMA2_PIN, "sdk_identity": old}
    )
    assert selected.sdk_commit == stage.sdk_commit == SCHEMA2_PIN
    with pytest.raises(PublicationError, match="native_historical_profile"):
        admit_native_sdk(selected)


@pytest.mark.parametrize("schema,commit", [(2, NEW_PIN), (3, SCHEMA2_PIN), (4, NEW_PIN)])
def test_profiles_cannot_be_relabelled(schema, commit) -> None:
    with pytest.raises(ValidationError, match="native_sdk_profile|literal_error"):
        request(schema, commit)


@pytest.mark.parametrize(
    "schema,commit,version", [(2, SCHEMA2_PIN, "0.7.0"), (3, NEW_PIN, "0.6.0")]
)
def test_stage_refuses_a_crossed_software_version(schema, commit, version) -> None:
    selected = identity(commit).model_copy(update={"version": version})
    with pytest.raises(ValidationError, match="native_sdk_identity"):
        NativeStage.model_validate(
            {
                **stage_fields(),
                "schema_version": schema,
                "sdk_commit": commit,
                "sdk_identity": selected,
            }
        )


@pytest.mark.parametrize(
    "schema,commit,version", [(2, SCHEMA2_PIN, "0.6.0"), (3, NEW_PIN, "0.7.0")]
)
def test_each_receipted_profile_is_readable_in_a_stdlib_only_child(
    tmp_path, schema, commit, version
) -> None:
    from blakean_entomology.publication_wire import read_transport

    pin = write_current_transport(tmp_path, schema=schema, commit=commit, version=version)
    assert read_transport(tmp_path, pin).schema_version == schema
    source = Path(__file__).resolve().parents[1] / "src"
    script = (
        "import sys,json\n"
        f"sys.path.insert(0,{str(source)!r})\n"
        "from pathlib import Path\n"
        "from blakean_entomology.publication_wire import read_transport\n"
        f"p=read_transport(Path({str(tmp_path)!r}),{pin!r})\n"
        "assert not any(n=='blake' or n.startswith('blake.') or n=='pydantic' "
        "or n.startswith('pydantic.') for n in sys.modules)\n"
        "print(json.dumps({'schema':p.schema_version,'pin':p.sdk_commit}))\n"
    )
    result = subprocess.run(
        [sys.executable, "-S", "-B", "-c", script],
        env={k: v for k, v in os.environ.items() if k != "PYTHONPATH"},
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == {"schema": schema, "pin": commit}


@pytest.mark.parametrize("kind", ["request", "stage"])
def test_rebound_schema_drift_is_refused(tmp_path, kind) -> None:
    from test_native_profile import rebind

    from blakean_entomology.publication_wire import read_transport

    _ = write_current_transport(tmp_path)
    path = tmp_path / ("native-request.json" if kind == "request" else "native-stage.json")
    value = json.loads(path.read_text())
    value["schema_version"] = 2
    path.write_text(json.dumps(value))
    if kind == "request":
        stage = tmp_path / "native-stage.json"
        plan = json.loads(stage.read_text())
        import hashlib

        plan["request_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        stage.write_text(json.dumps(plan))
    pin = rebind(tmp_path)
    with pytest.raises(PublicationError, match="native_profile_selection"):
        read_transport(tmp_path, pin)
