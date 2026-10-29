# /// script
# requires-python = ">=3.11"
# dependencies = ["click>=8.1", "matplotlib>=3.7", "pydantic==2.11.9"]
# ///
# Run with the existing external E interpreter and the contract's source PYTHONPATH.
"""Publication schematics from verified private taxonomy and atlas receipts."""

from pathlib import Path
from typing import Literal

import click
from blake.methods.models import Digest, EvidenceError, FileReceipt, FrozenModel, ResearchError
from blake.methods.runs import digest, read_regular, reserve, write_new
from blake.methods.storage import publish_bytes
from reference_plotting import atlas_figure, image_bytes, primary_cohort, tree_figure

from blakean_entomology.atlas_models import AtlasReceipt
from blakean_entomology.core import vocabulary
from blakean_entomology.taxonomy import load_reference
from blakean_entomology.workflows import require_private_output


class FigureReceipt(FrozenModel):
    schema_version: Literal[1] = 1
    atlas_sha256: Digest
    reference_sha256: Digest
    generator_sha256: Digest
    presentation_sha256: Digest
    count_unit: Literal["category-source-span candidates"] = "category-source-span candidates"
    files: tuple[FileReceipt, ...]
    tree_caption: str
    atlas_caption: str


def build_figures(
    atlas_path: Path,
    atlas_sha256: str,
    reference_path: Path,
    sources: Path,
    reference_sha256: str,
    output: Path,
) -> FigureReceipt:
    """Reject changed inputs, cross-bound sources and unsafe or occupied outputs."""
    require_private_output(output, atlas_path)
    require_private_output(output, sources)
    require_private_output(output, reference_path)
    raw = read_regular(atlas_path)
    if digest(raw) != atlas_sha256:
        raise EvidenceError("atlas_pin", str(atlas_path))
    atlas = AtlasReceipt.model_validate_json(raw)
    if atlas.reference_sha256 != reference_sha256:
        raise EvidenceError("atlas_reference_binding", str(reference_path))
    reference = load_reference(reference_path, sources, reference_sha256, vocabulary())
    if atlas.vocabulary_sha256 != reference.vocabulary_sha256:
        raise EvidenceError("atlas_vocabulary_binding", str(atlas_path))
    primary = primary_cohort(atlas)
    tree_caption = (
        f"Selected NCBI reference classification with conditional lexical associations. "
        f"The {primary.source_units} primary reading units supply {atlas.primary_candidates:,} "
        f"category-source-span candidates across all {atlas.category_count} categories. "
        "Displayed counts name individual categories and are never allocated or summed to taxa. "
        "Solid branches compress unshown classification ancestors; spacing is schematic. "
        "Teal dashed links are conditional animal senses; amber dotted links are ambiguous. "
        "Worm spans several lineages; Polypus and other historical forms retain "
        "unresolved alternatives. This is not a sequence-inferred phylogeny, identification, "
        "complete animal tree or monophyly claim."
    )
    atlas_caption = (
        f"Source-role corpus atlas: {atlas.scanned_units:,} captured units, "
        f"{atlas.candidates:,} overlapping category-span candidates; "
        f"{primary.source_units} primary reading units in {primary.work_groups} work groups. "
        "A prints raw counts with log(1+n) colour; B shows within-work matched-unit fractions, "
        "with equal-work and pooled coverage at right. Work groups with zero matches remain. "
        f"Exact whole-text grouping leaves {primary.exact_text_units} primary units. "
        "No contextual decisions transfer to this atlas; corpus images remain unreviewed."
    )
    figures = (tree_figure(reference, atlas), atlas_figure(atlas))
    payloads = tuple(
        (name + "." + kind, image_bytes(fig, kind))
        for name, fig in zip(("invertebrate-reference", "corpus-atlas"), figures, strict=True)
        for kind in ("png", "svg")
    )
    _ = load_reference(reference_path, sources, reference_sha256, vocabulary())
    if read_regular(atlas_path) != raw:
        raise EvidenceError("atlas_changed", str(atlas_path))
    reserve(output)
    artifacts = tuple(publish_bytes(output / name, payload) for name, payload in payloads)
    captions = f"Reference schematic. {tree_caption}\n\nCorpus atlas. {atlas_caption}\n"
    artifacts += (publish_bytes(output / "captions.md", captions.encode()),)
    receipt = FigureReceipt(
        atlas_sha256=atlas_sha256,
        reference_sha256=reference_sha256,
        generator_sha256=digest(Path(__file__).read_bytes()),
        presentation_sha256=digest(Path(__file__).with_name("reference_plotting.py").read_bytes()),
        files=artifacts,
        tree_caption=tree_caption,
        atlas_caption=atlas_caption,
    )
    _ = write_new(output / "figures.json", (receipt.model_dump_json(indent=2) + "\n").encode())
    return receipt


@click.command()
@click.option("--atlas", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--atlas-sha256", required=True)
@click.option("--reference", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--sources", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--reference-sha256", required=True)
@click.option("--output", type=click.Path(path_type=Path), required=True)
def main(
    atlas: Path,
    atlas_sha256: str,
    reference: Path,
    sources: Path,
    reference_sha256: str,
    output: Path,
) -> None:
    """Publish private aggregate PNG/SVG figures from two explicitly pinned inputs."""
    try:
        _ = build_figures(atlas, atlas_sha256, reference, sources, reference_sha256, output)
    except (OSError, ValueError, ResearchError) as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(str(output / "figures.json"))


if __name__ == "__main__":
    main()
