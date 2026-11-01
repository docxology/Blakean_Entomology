"""Real-file native custody and measured graphical publication, without mocks."""

import configparser
import csv
import hashlib
from pathlib import Path

import pytest
from test_taxonomy import STAGE

from blakean_entomology.publication_contract import PinnedInput
from blakean_entomology.publication_custody import checked_member, output_member
from blakean_entomology.publication_data import (
    pinned_bytes,
)
from blakean_entomology.publication_transport_models import Member, PublicationError
from blakean_entomology.publication_wire import read_transport


@pytest.mark.parametrize("failure", ("hash", "missing", "symlink"))
def test_pinned_source_refuses_real_file_changes(tmp_path, failure) -> None:
    # Given a trusted source digest.
    path = tmp_path / "input"
    path.write_bytes(b"original")
    pin = PinnedInput(path=path, sha256=hashlib.sha256(b"original").hexdigest())
    match failure:
        case "hash":
            path.write_bytes(b"changed")
        case "missing":
            pin = pin.model_copy(update={"path": tmp_path / "absent"})
        case "symlink":
            link = tmp_path / "link"
            link.symlink_to(path)
            pin = pin.model_copy(update={"path": link})
    # When the source boundary is read.
    with pytest.raises(PublicationError):
        _ = pinned_bytes(pin)
    # Then the invocation source remains explicit; no replacement is written.
    assert path.exists()


@pytest.mark.parametrize(
    "name", ("../escape", "/absolute", "", "a/../../escape", ".", "./a", "a//b", "a\\b", "a/./b")
)
def test_relative_member_refuses_escape(name) -> None:
    # Given an unsafe relative-path request.
    # When constructing the native transport member.
    with pytest.raises(PublicationError):
        _ = Member(name, 1, "a" * 64)
    # Then the boundary rejects it before any file operation.


def test_actual_member_control_rejects_changed_bytes(tmp_path) -> None:
    # Given a closed actual file receipt.
    path = tmp_path / "member"
    path.write_bytes(b"retained")
    record = output_member(path, tmp_path)
    checked_member(tmp_path, record)
    path.write_bytes(b"mutated")
    # When the same receipt is re-admitted.
    with pytest.raises(PublicationError):
        checked_member(tmp_path, record)
    # Then the stale receipt cannot qualify the changed source.


def write_transport(root: Path, row: tuple[str, ...]) -> str:
    """Create actual native transport files without a fabricated runtime."""
    with (root / "native-wire.csv").open("w", newline="") as stream:
        csv.writer(stream).writerow(row)
    (root / "native-stage.json").write_text("{}")
    (root / "manuscript_variables.csv").write_text("PAPER_TITLE,Fixture\n")
    config = configparser.ConfigParser()
    config["native"] = {
        "template_commit": "efce6d6f5b3c4e8e2bbf92d8250855a0a9389ae8",
        "sdk_commit": "45171a099a6a658c52ab689501de646a28485653",
        "source_date_epoch": "1793318400",
        "source_order": "00_frontmatter.md,10_article.md",
        "wire_sha256": hashlib.sha256((root / "native-wire.csv").read_bytes()).hexdigest(),
        "stage_sha256": hashlib.sha256((root / "native-stage.json").read_bytes()).hexdigest(),
    }
    with (root / "native-transport.ini").open("w") as stream:
        config.write(stream)
    return hashlib.sha256((root / "native-transport.ini").read_bytes()).hexdigest()


def test_native_transport_preserves_exact_source_and_input_roles(tmp_path) -> None:
    # Given a hash-bound stdlib transport carrying a concrete input member.
    expected = write_transport(tmp_path, ("input", "source.md", "4", "a" * 64))
    # When the separate-runtime boundary parses it.
    plan = read_transport(tmp_path, expected)
    # Then source-role and numerical metadata survive without loose JSON coercion.
    assert plan.inputs == (Member("source.md", 4, "a" * 64),)
    assert plan.source_order == ("00_frontmatter.md", "10_article.md")
    assert plan.sdk_commit == "45171a099a6a658c52ab689501de646a28485653"


@pytest.mark.parametrize("failure", ("pin", "wire", "stage", "row", "variables"))
def test_native_transport_refuses_changed_or_malformed_closure(tmp_path, failure) -> None:
    # Given actual transport files and their original independent hash.
    row = ("input", "source.md", "4", "a" * 64)
    if failure == "row":
        row = ("input", "source.md")
    expected = write_transport(tmp_path, row)
    if failure == "pin":
        expected = "0" * 64
    elif failure == "wire":
        (tmp_path / "native-wire.csv").write_text("mutated")
    elif failure == "stage":
        (tmp_path / "native-stage.json").write_text("mutated")
    elif failure == "variables":
        (tmp_path / "manuscript_variables.csv").write_text("malformed\n")
    # When the native boundary admits the changed closure.
    with pytest.raises(PublicationError):
        _ = read_transport(tmp_path, expected)
    # Then the caller-held pin and explicit structure are enforced.


def test_native_cli_refusal_preserves_typed_error_through_click(tmp_path) -> None:
    # Given an actual source file and a deliberately wrong caller-held pin.
    import subprocess
    import sys

    request = tmp_path / "request.json"
    request.write_text("{}")
    output = tmp_path / "analysis_output/rejected"
    command = [
        sys.executable,
        str(STAGE / "tools/render_manuscript.py"),
        "--request",
        str(request),
        "--request-sha256",
        "0" * 64,
        "--template-root",
        str(tmp_path),
        "--template-python",
        sys.executable,
        "--output",
        str(output),
    ]
    # When the real CLI rejects the source before reserving output.
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    # Then Click can propagate the typed refusal without masking it with a traceback mutation error.
    assert result.returncode != 0
    assert "source_pin" in result.stderr
    assert "TypeError:" not in result.stderr
    assert not output.exists()


@pytest.mark.parametrize(
    ("field", "replacement"),
    (
        ("sdk_commit", "0" * 40),
        ("template_commit", "0" * 40),
        ("source_order", "../outside.md"),
        ("schema_version", "broken"),
        ("source_date_epoch", "0"),
    ),
)
def test_native_transport_refuses_declared_pin_and_order_changes(
    tmp_path, field, replacement
) -> None:
    # Given a structurally valid transport whose declared selection was changed.
    _ = write_transport(tmp_path, ("input", "source.md", "4", "a" * 64))
    path = tmp_path / "native-transport.ini"
    config = configparser.ConfigParser(interpolation=None)
    config.read_string(path.read_text())
    config["native"][field] = replacement
    with path.open("w") as stream:
        config.write(stream)
    expected = hashlib.sha256(path.read_bytes()).hexdigest()
    # When even the changed transport's own correct hash is supplied.
    with pytest.raises(PublicationError):
        _ = read_transport(tmp_path, expected)
    # Then the framework/SDK selection and source order remain a closed contract.
