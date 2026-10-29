# /// script
# requires-python = ">=3.11"
# dependencies = ["click>=8.1", "pydantic==2.11.9"]
# ///
# Run with the existing external E interpreter and the source PYTHONPATH.
"""Prepare verified Markdown and assets; native PDF rendering belongs to root."""

import re
from pathlib import Path
from typing import Final, Literal

import click
from blake.methods.models import Digest, EvidenceError, FileReceipt, FrozenModel, ResearchError
from blake.methods.runs import digest, read_regular, reserve, write_new
from blake.methods.storage import publish_bytes, verify_file
from build_reference_figures import FigureReceipt
from reference_plotting import primary_cohort

from blakean_entomology.atlas_models import AtlasReceipt
from blakean_entomology.casebook import Casebook, load_casebook
from blakean_entomology.core import vocabulary
from blakean_entomology.taxonomy import load_reference
from blakean_entomology.workflows import require_private_output

TOKEN: Final = re.compile(r"\{\{([A-Z_]+)\}\}")


class PreparationReceipt(FrozenModel):
    schema_version: Literal[1] = 1
    atlas_sha256: Digest
    figures_sha256: Digest
    casebook_sha256: Digest
    reference_sha256: Digest
    manuscript_sha256: Digest
    bibliography_sha256: Digest
    generator_sha256: Digest
    presentation_sha256: Digest
    figure_tool_sha256: Digest
    files: tuple[FileReceipt, ...]
    qualification: Literal["prepared Markdown only; no native PDF or independent acceptance"] = (
        "prepared Markdown only; no native PDF or independent acceptance"
    )


def hydrate_article(
    text: str, atlas: AtlasReceipt, figures: FigureReceipt, casebook: Casebook, taxon_count: int
) -> str:
    """Resolve all declared new count/caption tokens; reject undeclared tokens."""
    primary = primary_cohort(atlas)
    old = atlas.historical_review
    if old is None:
        raise EvidenceError(
            "manuscript_historical_review", "Supply the original historical summary"
        )
    values = {
        "REFERENCE_TAXA": str(taxon_count),
        "ATLAS_CATEGORIES": str(atlas.category_count),
        "ATLAS_FORMS": str(atlas.explicit_form_count),
        "ATLAS_UNITS": f"{atlas.scanned_units:,}",
        "ATLAS_CANDIDATES": f"{atlas.candidates:,}",
        "ATLAS_PRIMARY_CANDIDATES": f"{atlas.primary_candidates:,}",
        "ATLAS_PRIMARY_UNITS": str(primary.source_units),
        "ZERO_NORMALIZED_FORMS": str(sum(f.equivalent_form_candidates == 0 for f in atlas.forms)),
        "ZERO_SURFACE_FORMS": str(sum(f.exact_surface_candidates == 0 for f in atlas.forms)),
        "ALIAS_GROUPS": str(len(atlas.normalized_alias_groups)),
        "ATLAS_DISTINCT_SPANS": f"{atlas.distinct_source_spans:,}",
        "OVERLAP_PAIRS": f"{atlas.overlapping_candidate_pairs:,}",
        "PRIMARY_EXACT_UNITS": str(primary.exact_text_units),
        "CASEBOOK_CASES": str(len(casebook.cases)),
        "COMPLETE_POEMS": str(
            sum(s.credit == "complete_poem_transcription" for s in casebook.selections)
        ),
        "HISTORICAL_REVIEWED": str(old.reviewed_hits),
        "HISTORICAL_UNREVIEWED": f"{old.unreviewed_hits:,}",
        "REFERENCE_CAPTION": figures.tree_caption,
        "ATLAS_CAPTION": figures.atlas_caption,
    }
    missing = set(TOKEN.findall(text)) - set(values)
    if missing:
        raise EvidenceError("manuscript_token", ", ".join(sorted(missing)))
    hydrated = TOKEN.sub(lambda m: values[m.group(1)], text)
    if "{{" in hydrated or "}}" in hydrated:
        raise EvidenceError("manuscript_token_syntax", "Unresolved or malformed token")
    return hydrated


def casebook_markdown(book: Casebook) -> str:
    """Export authored interpretations and exact reading ceilings without source bodies."""
    selections = {s.selection_id: s for s in book.selections}
    lines = [
        "# Contextual casebook",
        "",
        "Bounded textual readings; no new candidate decisions or image identifications.",
        "",
    ]
    for case in book.cases:
        lines += [
            f"## {case.title}",
            "",
            case.interpretation,
            "",
            "Alternative: " + case.rival_reading,
            "",
            "Biological limit: " + case.taxonomic_limit,
            "",
        ]
        for identity in case.selections:
            selection = selections[identity]
            lines += [
                f"- {selection.locator}. Credit: `{selection.credit}`. "
                + f"Selected-text SHA-256: `{selection.selected_text_sha256}`. {selection.limit}"
            ]
        lines += [""]
    return "\n".join(lines)


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
    atlas_raw = read_regular(atlas_path)
    figure_raw = read_regular(figure_directory / "figures.json")
    if digest(atlas_raw) != atlas_sha256 or digest(figure_raw) != figures_sha256:
        raise EvidenceError("manuscript_input_pin", "Atlas or figure receipt changed")
    atlas = AtlasReceipt.model_validate_json(atlas_raw)
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
    hydrated = hydrate_article(manuscript_raw.decode(), atlas, figures, book, len(model.taxa))
    citations = set(re.findall(r"@([a-z][a-z0-9-]+)", hydrated))
    keys = set(re.findall(r"@\w+\{([^,]+),", bibliography_raw.decode()))
    if not citations.issubset(keys):
        raise EvidenceError("manuscript_citation", str(sorted(citations - keys)))
    links = re.findall(r"!\[[^\]]*\]\(assets/([^\)]+)\)", hydrated)
    expected = {"retrieval-sensitivity.png", "invertebrate-reference.png", "corpus-atlas.png"}
    if set(links) != expected or len(links) != len(expected):
        raise EvidenceError("manuscript_figure_membership", str(links))
    prior_figure = read_regular(manuscript.parent / "assets/retrieval-sensitivity.png")
    reserve(output)
    render_inputs = {
        "blakean-entomology.md": hydrated.encode(),
        "references.bib": bibliography_raw,
        "contextual-casebook.md": casebook_markdown(book).encode(),
        "assets/retrieval-sensitivity.png": prior_figure,
    }
    render_inputs.update(
        ("assets/" + name, payload)
        for name, payload in payloads.items()
        if name.endswith((".png", ".svg"))
    )
    artifacts: list[FileReceipt] = []
    for name, payload in render_inputs.items():
        published = publish_bytes(output / name, payload)
        artifacts.append(FileReceipt(path=name, size=published.size, sha256=published.sha256))
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
) -> None:
    """Generate a source-bound Markdown input; do not invoke a native renderer."""
    try:
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
        )
    except (OSError, ValueError, ResearchError) as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(str(output / "preparation.json"))


if __name__ == "__main__":
    main()
