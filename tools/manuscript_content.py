"""Hydrate declared manuscript tokens and export bounded casebook text."""

import re
from typing import Final

from blake.methods.models import EvidenceError

from blakean_entomology.atlas_models import AtlasReceipt
from blakean_entomology.casebook import Casebook
from tools.build_reference_figures import FigureReceipt
from tools.manuscript_assets import AdditionalAssets
from tools.reference_plotting import primary_cohort

TOKEN: Final = re.compile(r"\{\{([A-Z_]+)\}\}")


def hydrate_article(
    text: str,
    atlas: AtlasReceipt,
    figures: FigureReceipt,
    casebook: Casebook,
    taxon_count: int,
    additional: AdditionalAssets | None = None,
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
    if additional is not None:
        values.update((key, value) for key, value in additional.replacements.items())
    missing = set(TOKEN.findall(text)) - set(values)
    if missing:
        raise EvidenceError("manuscript_token", ", ".join(sorted(missing)))
    hydrated = TOKEN.sub(lambda m: values[m.group(1)], text)
    prose = re.sub(r"\$\$[\s\S]*?\$\$|\$[^$\n]*\$", "", hydrated)
    if "{{" in hydrated or "}}" in prose:
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
