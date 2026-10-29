"""Private Matplotlib presentation of verified invertebrate reference and atlas data."""

import io
import math
from typing import Final

import matplotlib
from blake.methods.hierarchy import layout_evidence_tree
from matplotlib.figure import Figure

from blakean_entomology.atlas_models import AtlasReceipt, CoverageCohort
from blakean_entomology.taxonomy import reference_tree
from blakean_entomology.taxonomy_models import TaxonomyReference

matplotlib.use("Agg")

TREE_IDS: Final = (
    33208,
    6040,
    6073,
    6231,
    6340,
    6157,
    6447,
    6448,
    6544,
    6605,
    6656,
    6893,
    7540,
    7553,
    6681,
    6675,
    50557,
    7147,
    7041,
    7088,
    7399,
    36668,
    3042114,
)
ASSOCIATIONS: Final = {
    6040: ("sponge",),
    6073: ("polypus",),
    6231: (),
    6340: (),
    6157: (),
    6448: ("snail", "slug"),
    6544: ("mussel",),
    6605: ("polypus",),
    6893: ("spider",),
    7540: ("centipede",),
    7553: ("millipede",),
    6681: ("crab",),
    6675: ("barnacle",),
    7147: ("fly",),
    7041: ("beetle",),
    7088: ("caterpillar",),
    36668: ("ant",),
    3042114: ("bee",),
}
TERMS: Final = (
    "worm",
    "fly",
    "ant",
    "bee",
    "spider",
    "polypus",
    "snail",
    "mussel",
    "wing",
    "shell",
)


def primary_cohort(atlas: AtlasReceipt) -> CoverageCohort:
    """Use the author's primary reading population, never all-plane pooled counts."""
    return next(
        c
        for c in atlas.cohorts
        if (c.role, c.plane, c.author_id) == ("primary", "reading", "william-blake-1757-1827")
    )


def tree_figure(reference: TaxonomyReference, atlas: AtlasReceipt) -> Figure:
    """Draw compressed reference edges and separate, conditional lexical leads."""
    tree = reference_tree(reference, TREE_IDS)
    positions = {p.node_id: p for p in layout_evidence_tree(tree)}
    leaves = {n.node_id for n in tree.nodes} - {n.parent_id for n in tree.nodes}
    primary = primary_cohort(atlas)
    counts = {q.query_id: q.copy_retaining.occurrences for q in primary.categories}
    statuses = {m.term_id: m.status.value for m in reference.mappings}
    figure = Figure(figsize=(7.1, 9.4), layout="constrained")
    axis = figure.add_subplot()
    for node in tree.nodes:
        p = positions[node.node_id]
        if node.parent_id is not None:
            parent = positions[node.parent_id]
            _ = axis.plot(
                [parent.depth, parent.depth, p.depth],
                [parent.row, p.row, p.row],
                color="#34495e",
                linewidth=1.05,
            )
        _ = axis.plot(p.depth, p.row, "o", color="#34495e", markersize=3)
        _ = axis.text(
            p.depth + 0.06,
            p.row - 0.13,
            node.label,
            fontsize=9.2,
            va="bottom",
            color="#182c3d",
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.4},
        )
        if node.node_id in leaves:
            terms = ASSOCIATIONS.get(int(node.node_id), ())
            label = "; ".join(
                f"{'ant/emmet' if t == 'ant' else t}"
                + ("?" if statuses[t] == "ambiguous_mapping" else "")
                + f" {counts[t]}"
                for t in terms
            )
            if not terms:
                label = "worm? — no allocation"
            ambiguous = not terms or any(statuses[t] == "ambiguous_mapping" for t in terms)
            color = "#a65715" if ambiguous else "#187686"
            _ = axis.plot(
                [p.depth + 0.05, 4.75],
                [p.row, p.row],
                color=color,
                linestyle=":" if ambiguous else "--",
                linewidth=0.9,
                alpha=0.7,
            )
            _ = axis.text(4.85, p.row, label, fontsize=9.7, va="center", color=color)
    _ = axis.set_xlim(-0.3, 7.25)
    _ = axis.set_ylim(max(p.row for p in positions.values()) + 0.8, -1.5)
    _ = axis.text(0, -1, "A  Selected NCBI lineages", fontsize=11, weight="bold")
    _ = axis.text(4.85, -1, "Conditional words · candidates", fontsize=10, weight="bold")
    axis.set_axis_off()
    _ = figure.suptitle(
        "Invertebrate reference, uncertain literary bodies", fontsize=14, weight="bold"
    )
    _ = figure.supxlabel(
        f"Primary reading: {primary.source_units} units, {primary.tokens:,} NFKC tokens.\n"
        f"worm: {counts['worm']} candidates; polyphyletic label, alternatives not exhaustive.\n"
        "Solid: compressed classification. Dashed teal: conditional animal sense.\n"
        "Dotted amber: ambiguous association. Numbers count lexical categories, not animals.\n"
        "Polypus appears twice as alternatives; its count must not be summed.\n"
        "No branch lengths, time, inferred sequence tree, or proof of monophyly.\n"
        "Selected branches only; 'invertebrates' is not a clade. NCBI capture: 28 Oct 2026.",
        fontsize=9,
    )
    return figure


def atlas_figure(atlas: AtlasReceipt) -> Figure:
    """Expose source-role counts and equal-work coverage alongside retained copies."""
    primary = primary_cohort(atlas)
    cohorts = atlas.cohorts
    raw = [
        [
            sum(q.copy_retaining.occurrences for q in c.categories if q.query_id == t)
            for c in cohorts
        ]
        for t in TERMS
    ]
    works = sorted(primary.works, key=lambda w: w.key)
    coverage = [
        [next(q.measure.coverage_fraction for q in w.queries if q.query_id == t) for w in works]
        for t in TERMS
    ]
    figure = Figure(figsize=(7.1, 9.4), layout="constrained")
    counts = figure.add_subplot(2, 1, 1)
    _ = counts.imshow(
        [[math.log1p(n) for n in row] for row in raw], aspect="auto", cmap="Blues", vmin=0
    )
    _ = counts.set_xticks(
        range(len(cohorts)),
        [f"{c.plane}\n{c.role}\n{c.source_units} units" for c in cohorts],
        fontsize=9,
    )
    _ = counts.set_yticks(range(len(TERMS)), TERMS, fontsize=10)
    for i, row in enumerate(raw):
        for j, n in enumerate(row):
            _ = counts.text(
                j,
                i,
                str(n),
                ha="center",
                va="center",
                fontsize=10,
                color="white" if math.log1p(n) > 4.8 else "#152536",
            )
    _ = counts.set_title(
        "A  Category-span candidates by source role/plane\n(colour = log(1 + count))",
        loc="left",
        fontsize=11,
    )
    axis = figure.add_subplot(2, 1, 2)
    _ = axis.imshow(coverage, aspect="auto", cmap="Blues", vmin=0, vmax=1)
    _ = axis.set_yticks(range(len(TERMS)), TERMS, fontsize=10)
    _ = axis.set_xticks(
        range(len(works)), [w.key[0] for w in works], rotation=70, ha="right", fontsize=8
    )
    queries = {q.query_id: q for q in primary.categories}
    for i, term in enumerate(TERMS):
        q = queries[term]
        _ = axis.text(
            len(works) + 0.2,
            i,
            f"{100 * q.work_balanced_coverage_fraction:.1f}% / "
            + f"{100 * (q.copy_retaining.coverage_fraction or 0):.1f}%",
            va="center",
            fontsize=9,
        )
    _ = axis.text(len(works) + 0.2, -1, "Equal work / pooled", fontsize=9, weight="bold")
    _ = axis.set_title(
        "B  Primary reading: matched-unit fraction in each work group",
        loc="left",
        fontsize=11,
    )
    _ = axis.set_xlim(-0.5, len(works) + 6)
    _ = figure.suptitle(
        f"Corpus atlas | {atlas.scanned_units:,} units · {atlas.category_count} categories · "
        + f"{atlas.explicit_form_count} forms",
        fontsize=13,
        weight="bold",
    )
    historical = atlas.historical_review
    old = (
        f"Historical decisions: {historical.reviewed_hits}/{historical.candidate_hits:,}; "
        + f"{historical.unreviewed_hits:,} unreviewed on their old pin. "
        if historical
        else "No historical review supplied. "
    )
    _ = figure.supxlabel(
        f"B: {primary.source_units} primary units, {primary.work_groups} recorded groups, "
        + f"{primary.tokens:,} NFKC tokens. White = 0, dark blue = 1.\n"
        + f"Exact whole-text grouping: {primary.exact_text_units} primary units; "
        + "embedded repeated poems remain.\n"
        + old
        + "New atlas decisions: 0.\n"
        + "Copies, category overlap and non-animal senses retained.\n"
        + "Blank review is not absence. Corpus images unreviewed.",
        fontsize=9,
    )
    return figure


def image_bytes(figure: Figure, kind: str) -> bytes:
    """Keep raster and vector presentations bound to the same in-memory figure."""
    with io.BytesIO() as buffer:
        figure.savefig(
            buffer,
            format=kind,
            dpi=240,
            facecolor="white",
            metadata={"Creator": "Blakean Entomology"} if kind == "svg" else None,
        )
        return buffer.getvalue()
