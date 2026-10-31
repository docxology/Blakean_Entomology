"""Commands for request-pinned private review batches."""

from pathlib import Path

import click
from blake.methods.models import ResearchError

from .review_planning import (
    PinnedReviewBatch,
    PinnedReviewFile,
    publish_planning_request,
    verify_planning_request,
)


@click.command("plan-review")
@click.option("--request", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--request-sha256", required=True)
@click.option("--output", type=click.Path(path_type=Path), required=True)
def plan_review_command(request: Path, request_sha256: str, output: Path) -> None:
    """Plan blank review work; no candidate receives an authored judgment."""
    try:
        receipt = publish_planning_request(
            PinnedReviewFile(path=request, sha256=request_sha256), output
        )
    except (OSError, ValueError, ResearchError) as error:
        raise click.ClickException(str(error)) from error
    click.echo(receipt.model_dump_json(indent=2))


@click.command("verify-review")
@click.option("--request", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--request-sha256", required=True)
@click.option("--batch", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--batch-sha256", required=True)
def verify_review_command(
    request: Path, request_sha256: str, batch: Path, batch_sha256: str
) -> None:
    """Four explicit options hold the independent request and batch custody pairs."""
    try:
        verified = verify_planning_request(
            PinnedReviewFile(path=request, sha256=request_sha256),
            PinnedReviewBatch(directory=batch, receipt_sha256=batch_sha256),
        )
    except (OSError, ValueError, ResearchError) as error:
        raise click.ClickException(str(error)) from error
    click.echo(verified.plan.model_dump_json(indent=2))


def register_review_planning_commands(group: click.Group) -> None:
    """Attach planning without changing existing study/review commands."""
    group.add_command(plan_review_command)
    group.add_command(verify_review_command)
