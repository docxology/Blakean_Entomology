# /// script
# requires-python = ">=3.11"
# dependencies = ["click>=8.1", "pydantic==2.11.9", "matplotlib>=3.7"]
# ///
# ─── How to run ───
# In the admitted project and locked external application environment:
# uv run python tools/render_manuscript.py --help
# Supply the independently pinned request, template checkout, compatible external
# template Python and a NEW private analysis_output destination.
# ──────────────────
"""Admit source-derived front matter and call the actual docxology/template writers."""

import hashlib
import os
import subprocess
from pathlib import Path

import click

from blakean_entomology.publication import prepare_native_stage
from blakean_entomology.publication_contract import NativeRequest, PinnedInput
from blakean_entomology.publication_data import pinned_bytes
from blakean_entomology.publication_wire import PublicationError


@click.command()
@click.option("--request", type=click.Path(path_type=Path, exists=True), required=True)
@click.option("--request-sha256", required=True)
@click.option("--template-root", type=click.Path(path_type=Path, exists=True), required=True)
@click.option("--template-python", type=click.Path(path_type=Path, exists=True), required=True)
@click.option("--output", type=click.Path(path_type=Path), required=True)
@click.option(
    "--prepare-only", is_flag=True, help="Close a fresh stage without invoking native writers."
)
def main(
    request: Path,
    request_sha256: str,
    template_root: Path,
    template_python: Path,
    output: Path,
    prepare_only: bool,
) -> None:
    """Publish only to an unoccupied private epoch; keep every failed attempt."""
    invocation = PinnedInput(path=request, sha256=request_sha256)
    specification = NativeRequest.model_validate_json(pinned_bytes(invocation))
    _ = prepare_native_stage(specification, output, template_root)
    if prepare_only:
        click.echo(str(output / "native-stage.json"))
        return
    environment = dict(os.environ)
    _ = environment.pop("VIRTUAL_ENV", None)
    _ = environment.pop("PYTHONPATH", None)
    worker = Path(__file__).with_name("native_template_worker.py")
    with (output / "native-render.stdout").open("xb") as stdout:
        with (output / "native-render.stderr").open("xb") as stderr:
            transport_sha = hashlib.sha256(
                (output / "native-transport.ini").read_bytes()
            ).hexdigest()
            command = [
                str(template_python),
                "-B",
                str(worker),
                str(template_root),
                str(output),
                transport_sha,
            ]
            process = subprocess.Popen(
                command, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, env=environment
            )
            _ = (output / "native-worker.pid").write_text(str(process.pid) + "\n")
            status = process.wait()
    if status != 0:
        raise PublicationError("template_render_failed", str(output / "native-render.stderr"))
    click.echo(str(output / "native-render-receipt.json"))


if __name__ == "__main__":
    main()
