# /// script
# requires-python = ">=3.11"
# dependencies = ["click>=8.1", "pydantic==2.11.9"]
# ///
# Run with the existing external E interpreter and the source PYTHONPATH.
"""Prepare verified Markdown and assets; native PDF rendering belongs to root."""

import re
import sys
from pathlib import Path

# Source tools are executable scripts; admit their source directory
# for both direct execution and namespace imports without installing tool modules.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import click
from blake.methods.models import EvidenceError, FileReceipt, ResearchError
from blake.methods.runs import digest, read_regular, reserve, write_new
from blake.methods.storage import publish_bytes, verify_file

from blakean_entomology.atlas_models import AtlasReceipt
from blakean_entomology.casebook import load_casebook
from blakean_entomology.core import vocabulary
from blakean_entomology.taxonomy import load_reference
from blakean_entomology.workflows import require_private_output
from tools.build_reference_figures import FigureReceipt
from tools.geometry_asset_contract import verify_geometry_assets
from tools.manuscript_assets import AdditionalInput, PreparationReceipt
from tools.manuscript_content import casebook_markdown, hydrate_article


def prepare(
    manuscript: Path,
    bibliography: Path,
    atlas_path: Path,
    atlas_sha256: str,
    figure_directory: Path,
    figures_sha256: str,
    casebook_path: Path,
    casebook_sha256: str,
    reference: Path,
    sources: Path,
    reference_sha256: str,
    output: Path,
    additional: AdditionalInput | None = None,
) -> PreparationReceipt:
    """Close source/data/figure bindings before writing a new render input epoch."""
    inputs = (
        manuscript,
        bibliography,
        atlas_path,
        figure_directory,
        casebook_path,
        reference,
        sources,
    )
    for source in inputs:
        require_private_output(output, source)
    extension = additional.load(atlas_sha256) if additional is not None else None
    if additional is not None:
        require_private_output(output, additional.directory)
    atlas_raw = read_regular(atlas_path)
    figure_raw = read_regular(figure_directory / "figures.json")
    if digest(atlas_raw) != atlas_sha256 or digest(figure_raw) != figures_sha256:
        raise EvidenceError("manuscript_input_pin", "Atlas or figure receipt changed")
    atlas = AtlasReceipt.model_validate_json(atlas_raw)
    if extension is not None and extension.geometry_binding is not None and additional is not None:
        captions = verify_geometry_assets(additional.directory, extension.geometry_binding, atlas)
        if any(extension.replacements.get(k) != v for k, v in captions.items()):
            raise EvidenceError("geometry_asset_caption_binding", "Figure captions differ")
    figures = FigureReceipt.model_validate_json(figure_raw)
    if (
        figures.atlas_sha256 != atlas_sha256
        or figures.reference_sha256 != reference_sha256
        or atlas.reference_sha256 != reference_sha256
    ):
        raise EvidenceError("manuscript_binding", "Reference/data/figures differ")
    expected_assets = {
        "invertebrate-reference.png",
        "invertebrate-reference.svg",
        "corpus-atlas.png",
        "corpus-atlas.svg",
        "captions.md",
    }
    if {f.path for f in figures.files} != expected_assets or len(figures.files) != 5:
        raise EvidenceError("figure_artifact_membership", str(figure_directory))
    payloads = {
        f.path: verify_file(figure_directory, f.path, f.size, f.sha256).read_bytes()
        for f in figures.files
    }
    book = load_casebook(casebook_path, sources, casebook_sha256)
    model = load_reference(reference, sources, reference_sha256, vocabulary())
    manuscript_raw = read_regular(manuscript)
    bibliography_raw = read_regular(bibliography)
    hydrated = hydrate_article(
        manuscript_raw.decode(), atlas, figures, book, len(model.taxa), extension
    )
    citations = {
        m.group(1) for m in re.finditer(r"@([a-z][a-z0-9:_-]+)", hydrated) if ":" not in m.group(1)
    }
    keys = set(re.findall(r"@\w+\{([^,]+),", bibliography_raw.decode()))
    if len(re.findall(r"@\w+\{([^,]+),", bibliography_raw.decode())) != len(keys):
        raise EvidenceError("manuscript_duplicate_citation_key", str(bibliography))
    if not citations.issubset(keys):
        raise EvidenceError("manuscript_citation", str(sorted(citations - keys)))
    links = re.findall(r"!\[(?:[^\[\]]|\[[^\[\]]*\])*\]\(([^\)]+)\)", hydrated)
    expected = {"retrieval-sensitivity.png", "invertebrate-reference.png", "corpus-atlas.png"}
    if extension is not None:
        expected.update(extension.image_paths)
        for entry in extension.files:
            payloads[entry.path] = read_regular(
                verify_file(
                    figure_directory if additional is None else additional.directory,
                    entry.path,
                    entry.size,
                    entry.sha256,
                )
            )
    expected = {"assets/" + name for name in expected}
    if set(links) != expected or len(links) != len(expected) or hydrated.count("![") != len(links):
        raise EvidenceError("manuscript_figure_membership", str(links))
    prior_figure = read_regular(manuscript.parent / "assets/retrieval-sensitivity.png")
    render_inputs = {
        "blakean-entomology.md": hydrated.encode(),
        "references.bib": bibliography_raw,
        "contextual-casebook.md": casebook_markdown(book).encode(),
        "assets/retrieval-sensitivity.png": prior_figure,
    }
    render_inputs.update(
        ("assets/" + name, payload)
        for name, payload in payloads.items()
        if name.endswith((".png", ".svg")) or extension is not None
    )
    if additional is not None:
        render_inputs["additional-assets.json"] = read_regular(
            additional.directory / "additional-assets.json"
        )
    snapshots = [
        (p, read_regular(p))
        for p in (
            manuscript,
            bibliography,
            atlas_path,
            figure_directory / "figures.json",
            casebook_path,
            reference,
            manuscript.parent / "assets/retrieval-sensitivity.png",
            Path(__file__),
            Path(__file__).with_name("manuscript_assets.py"),
            Path(__file__).with_name("manuscript_content.py"),
            Path(__file__).with_name("geometry_asset_contract.py"),
            Path(__file__).with_name("reference_plotting.py"),
            Path(__file__).with_name("build_reference_figures.py"),
        )
    ]
    artifacts: list[FileReceipt] = []
    reserve(output)
    for name, payload in render_inputs.items():
        published = publish_bytes(output / name, payload)
        artifacts.append(FileReceipt(path=name, size=published.size, sha256=published.sha256))
    for path, raw in snapshots:
        if read_regular(path) != raw:
            raise EvidenceError("manuscript_source_changed", str(path))
    for member in figures.files:
        _ = verify_file(figure_directory, member.path, member.size, member.sha256)
    _ = load_casebook(casebook_path, sources, casebook_sha256)
    _ = load_reference(reference, sources, reference_sha256, vocabulary())
    if additional is not None:
        _ = additional.load(atlas_sha256)
    receipt = PreparationReceipt(
        atlas_sha256=atlas_sha256,
        figures_sha256=figures_sha256,
        casebook_sha256=casebook_sha256,
        reference_sha256=reference_sha256,
        manuscript_sha256=digest(manuscript_raw),
        bibliography_sha256=digest(bibliography_raw),
        generator_sha256=digest(Path(__file__).read_bytes()),
        presentation_sha256=digest(Path(__file__).with_name("reference_plotting.py").read_bytes()),
        figure_tool_sha256=digest(
            Path(__file__).with_name("build_reference_figures.py").read_bytes()
        ),
        files=tuple(artifacts),
        additional_assets_sha256=additional.sha256 if additional is not None else None,
        additional_assets=extension,
        helper_sources=tuple(
            FileReceipt(path=name, size=len(raw), sha256=digest(raw))
            for name in (
                "manuscript_assets.py",
                "manuscript_content.py",
                "geometry_asset_contract.py",
            )
            for raw in (read_regular(Path(__file__).with_name(name)),)
        ),
    )
    _ = write_new(output / "preparation.json", (receipt.model_dump_json(indent=2) + "\n").encode())
    return receipt


@click.command()
@click.option("--manuscript", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--bibliography", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--atlas", "atlas_path", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--atlas-sha256", required=True)
@click.option(
    "--figures", "figure_directory", type=click.Path(exists=True, path_type=Path), required=True
)
@click.option("--figures-sha256", required=True)
@click.option(
    "--casebook", "casebook_path", type=click.Path(exists=True, path_type=Path), required=True
)
@click.option("--casebook-sha256", required=True)
@click.option("--reference", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--sources", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--reference-sha256", required=True)
@click.option("--output", type=click.Path(path_type=Path), required=True)
@click.option("--additional-assets", type=click.Path(exists=True, path_type=Path))
@click.option("--additional-assets-sha256")
def main(
    manuscript: Path,
    bibliography: Path,
    atlas_path: Path,
    atlas_sha256: str,
    figure_directory: Path,
    figures_sha256: str,
    casebook_path: Path,
    casebook_sha256: str,
    reference: Path,
    sources: Path,
    reference_sha256: str,
    output: Path,
    additional_assets: Path | None,
    additional_assets_sha256: str | None,
) -> None:
    """Generate a source-bound Markdown input; do not invoke a native renderer."""
    try:
        if (additional_assets is None) != (additional_assets_sha256 is None):
            raise EvidenceError("additional_asset_options", "Supply directory and SHA together")
        extra = (
            AdditionalInput(additional_assets, additional_assets_sha256)
            if additional_assets is not None and additional_assets_sha256 is not None
            else None
        )
        _ = prepare(
            manuscript,
            bibliography,
            atlas_path,
            atlas_sha256,
            figure_directory,
            figures_sha256,
            casebook_path,
            casebook_sha256,
            reference,
            sources,
            reference_sha256,
            output,
            extra,
        )
    except (OSError, ValueError, ResearchError) as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(str(output / "preparation.json"))


if __name__ == "__main__":
    main()
