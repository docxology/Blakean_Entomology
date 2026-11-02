"""Thin command for an explicit new original-codepoint analysis epoch."""

from pathlib import Path

import click

from .geometry_run import publish_geometry


@click.command(name="geometry")
@click.option("--request", "request_path", type=click.Path(path_type=Path), required=True)
@click.option("--request-sha256", required=True, help="Caller-held request byte digest.")
@click.option("--bundle", type=click.Path(path_type=Path), required=True)
@click.option("--run", type=click.Path(path_type=Path), required=True)
@click.option("--decisions", type=click.Path(path_type=Path), required=True)
@click.option("--windows", type=click.Path(path_type=Path), required=True)
@click.option("--vocabulary", type=click.Path(path_type=Path), required=True)
@click.option("--output", type=click.Path(path_type=Path), required=True)
@click.option("--figures/--no-figures", default=False)
def geometry(
    request_path: Path,
    request_sha256: str,
    bundle: Path,
    run: Path,
    decisions: Path,
    windows: Path,
    vocabulary: Path,
    output: Path,
    *,
    figures: bool,
) -> None:
    """Measure matched support and documented reading without adding decisions."""
    try:
        report = publish_geometry(
            request_path,
            request_sha256,
            bundle,
            run,
            decisions,
            windows,
            vocabulary,
            output,
            figures=figures,
        )
    except (OSError, ValueError, ImportError) as error:
        raise click.ClickException(f"geometry_failed: {error}") from error
    click.echo(
        f"Measured {report.candidate_hits} candidates in {len(report.sources)} units; "
        + f"{report.reviewed_hits} reviewed, {report.unreviewed_hits} unreviewed."
    )


if __name__ == "__main__":
    geometry()
