"""Commands for reproducible candidate retrieval and explicit evidence review."""

import sqlite3
from pathlib import Path

import click
from blake.applications import export_recovered
from blake.methods.models import ResearchError
from blake.methods.proximity import ProximityGrid
from blake.methods.runs import read_regular
from pydantic import ValidationError

from . import __version__
from .atlas import atlas_workflow
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
from .geometry_cli import geometry
from .models import CorpusPin, EvidenceError
from .review_planning_cli import register_review_planning_commands
from .sensitivity import ProximityBinding
from .taxonomy import load_reference, reference_tree
from .workflows import proximity_workflow, sensitivity_workflow, workspace_workflow


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


@main.command("sensitivity")
@click.option("--bundle", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--pin", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--vocabulary", "spec_path", type=click.Path(exists=True, path_type=Path))
@click.option("--output", type=click.Path(path_type=Path), required=True)
def sensitivity_command(bundle: Path, pin: Path, spec_path: Path | None, output: Path) -> None:
    """Write NFKC category sensitivity for Blake-primary reading units."""
    try:
        receipt = sensitivity_workflow(
            bundle,
            CorpusPin.model_validate_json(read_regular(pin, "pin")),
            vocabulary(spec_path),
            output,
        )
    except (OSError, ValueError, ResearchError) as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(receipt.model_dump_json(indent=2))


@main.command("proximity-study")
@click.option("--bundle", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--binding", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--grid", type=click.Path(exists=True, path_type=Path))
@click.option("--output", type=click.Path(path_type=Path), required=True)
def proximity_command(bundle: Path, binding: Path, grid: Path | None, output: Path) -> None:
    """Write literal ALL proximity with an explicit portable/projection binding."""
    try:
        receipt = proximity_workflow(
            bundle,
            ProximityBinding.model_validate_json(read_regular(binding, "pin")),
            output,
            ProximityGrid.model_validate_json(read_regular(grid, "grid")) if grid else None,
        )
    except (OSError, ValueError, ResearchError) as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(receipt.model_dump_json(indent=2))


@main.command("build-search-workspace")
@click.option("--bundle", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--binding", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--output", type=click.Path(path_type=Path), required=True)
def workspace_command(bundle: Path, binding: Path, output: Path) -> None:
    """Build a private offline literal search workspace under analysis_output."""
    try:
        index = workspace_workflow(
            bundle,
            ProximityBinding.model_validate_json(read_regular(binding, "pin")),
            output,
        )
    except (OSError, ValueError, ResearchError) as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(str(index))


@main.command("verify-reference")
@click.option("--reference", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--sources", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--reference-sha256", required=True)
@click.option("--vocabulary", "spec_path", type=click.Path(exists=True, path_type=Path))
def verify_reference_command(
    reference: Path, sources: Path, reference_sha256: str, spec_path: Path | None
) -> None:
    """Verify captured NCBI lineages and all conditional lexical associations."""
    try:
        model = load_reference(reference, sources, reference_sha256, vocabulary(spec_path))
        tree = reference_tree(model)
    except (OSError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(tree.model_dump_json(indent=2))


@main.command("corpus-atlas")
@click.option("--bundle", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--pin", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--vocabulary", "spec_path", type=click.Path(exists=True, path_type=Path))
@click.option("--reference", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--sources", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--reference-sha256", required=True)
@click.option("--historical-summary", type=click.Path(exists=True, path_type=Path))
@click.option("--output", type=click.Path(path_type=Path), required=True)
def atlas_command(
    bundle: Path,
    pin: Path,
    spec_path: Path | None,
    reference: Path,
    sources: Path,
    reference_sha256: str,
    historical_summary: Path | None,
    output: Path,
) -> None:
    """Audit every declared form and role/plane; preserve distinct review epochs."""
    try:
        receipt = atlas_workflow(
            bundle,
            CorpusPin.model_validate_json(read_regular(pin)),
            vocabulary(spec_path),
            reference,
            sources,
            reference_sha256,
            output,
            historical_summary,
        )
    except (OSError, ValueError, ResearchError) as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(
        f"{receipt.scanned_units} source units; {receipt.candidates} category-span candidates; "
        + f"{receipt.current_epoch_authored_decisions} new decisions. {output}"
    )


@main.command("composition-audit")
@click.option("--atlas", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--atlas-sha256", required=True)
@click.option("--sensitivity", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--bundle", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--pin", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--vocabulary", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--proximity", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--output", type=click.Path(path_type=Path), required=True)
def composition_command(
    atlas: Path,
    atlas_sha256: str,
    sensitivity: Path,
    bundle: Path,
    pin: Path,
    vocabulary: Path,
    proximity: Path,
    output: Path,
) -> None:
    """Recompute bound inputs and write nine text-free composition exports."""
    from .composition_workflow import CompositionInputs, generate

    try:
        receipt = generate(
            CompositionInputs(
                atlas=atlas,
                atlas_sha256=atlas_sha256,
                sensitivity=sensitivity,
                bundle=bundle,
                pin=pin,
                vocabulary=vocabulary,
                proximity=proximity,
            ),
            output,
            Path.cwd() / "analysis_output",
        )
    except (OSError, ValueError, ResearchError) as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(f"{len(receipt.files)} text-free exports; source candidate. {output}")


register_review_planning_commands(main)
main.add_command(geometry)


if __name__ == "__main__":
    main()
