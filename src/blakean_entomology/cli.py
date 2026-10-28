"""Commands for reproducible candidate retrieval and explicit evidence review."""

import sqlite3
from pathlib import Path

import click
from blake.applications import export_recovered
from pydantic import ValidationError

from . import __version__
from .core import (
    analyze,
    digest,
    json_bytes,
    load_run,
    review,
    safe_directory,
    vocabulary,
    write_new,
)
from .models import CorpusPin, EvidenceError


@click.group()
@click.version_option(__version__)
def main() -> None:
    """Study invertebrates using the shared, pinned Blake corpus and methods."""


@main.command("import-corpus")
@click.option("--source", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--destination", type=click.Path(path_type=Path), required=True)
@click.option("--pin-output", type=click.Path(path_type=Path), required=True)
def import_corpus(source: Path, destination: Path, pin_output: Path) -> None:
    """Export a new independent private snapshot and write its trusted pin."""
    try:
        if pin_output.exists() or pin_output.is_symlink():
            raise EvidenceError("occupied_pin", str(pin_output))
        safe_directory(pin_output)
        pin_path = pin_output.resolve()
        if any(pin_path.is_relative_to(root.resolve()) for root in (source, destination)):
            raise EvidenceError("overlapping_pin", str(pin_output))
        pin_output.parent.mkdir(parents=True, exist_ok=True)
        manifest = export_recovered(source, destination)
        pin = CorpusPin(
            bundle_manifest_sha256=digest((destination / "manifest.json").read_bytes()),
            captured_manifest_sha256=manifest.captured_manifest_sha256,
            projection_manifest_sha256=manifest.projection_manifest_sha256,
            index_sha256=manifest.index_sha256,
        )
        with pin_output.open("x") as handle:
            _ = handle.write(pin.model_dump_json(indent=2) + "\n")
    except (OSError, ValueError, sqlite3.Error) as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(pin.model_dump_json(indent=2))


@main.command("analyze")
@click.option("--bundle", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--pin", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--vocabulary", "spec_path", type=click.Path(exists=True, path_type=Path))
@click.option("--output", type=click.Path(path_type=Path), required=True)
def analyze_command(bundle: Path, pin: Path, spec_path: Path | None, output: Path) -> None:
    """Retrieve all candidates, complete count tables and a private review queue."""
    try:
        receipt = analyze(
            bundle, CorpusPin.model_validate_json(pin.read_bytes()), vocabulary(spec_path), output
        )
    except (OSError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(receipt.model_dump_json(indent=2))


@main.command("verify-run")
@click.argument("directory", type=click.Path(exists=True, path_type=Path))
def verify_run(directory: Path) -> None:
    """Verify all retained outputs and report their pinned identities."""
    try:
        _receipt, summary, _hits = load_run(directory)
    except (OSError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(summary.model_dump_json(indent=2))
    click.echo(f"run_sha256={digest((directory / 'run.json').read_bytes())}")


@main.command("review")
@click.option("--run", "directory", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--run-sha256", required=True)
@click.option("--decisions", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--output", type=click.Path(path_type=Path), required=True)
def review_command(directory: Path, run_sha256: str, decisions: Path, output: Path) -> None:
    """Validate annotated queue CSV or JSONL and write an immutable review summary."""
    try:
        summary = review(directory, decisions, run_sha256)
        _ = write_new(output, json_bytes(summary))
    except (OSError, ValueError, ValidationError) as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(summary.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
