"""Separate NFKC category sensitivity from literal invertebrate proximity."""

from collections import Counter
from pathlib import Path
from typing import Final

from blake.applications import ApplicationBundle, load_bundle
from blake.methods.models import (
    Digest,
    EvidenceError,
    FrozenModel,
    Plane,
    ProjectionCorpusPin,
    Role,
)
from blake.methods.profiles import RetrievalProfile, runtime_profile
from blake.methods.proximity import ProximityGrid, ProximityStudy, build_proximity_study
from blake.methods.runs import digest
from blake.methods.schema_conversion import bundle_to_projection
from blake.methods.search_models import SearchRequest
from blake.methods.statistics import analyze_inventory
from blake.methods.statistics_models import CountedStatistics, SourceUnit
from blake.studies import StudySpec, scan_passages
from blake.text_search.models import Passage
from blake.text_search.normalize import tokenize

PAIRS: Final = (("worm", "fly"), ("bee", "flower"), ("spider", "web"), ("emmet", "grass"))
WIDTHS: Final = (8, 16, 32, 64, None)


class ProximityBinding(FrozenModel):
    """Bind portable input bytes and the explicit projection provenance separately."""

    bundle_manifest_sha256: Digest
    projection_pin: ProjectionCorpusPin


def analyze_sensitivity(passages: tuple[Passage, ...], spec: StudySpec) -> CountedStatistics:
    """Recompute category spans and denominators on Blake-primary reading sources.

    Every eligible unit remains in the inventory, including zero-token texts and
    categories with zero matches. Category overlap is retained as separate counts.
    No precomputed study result is accepted across this boundary.
    """
    study = scan_passages(passages, spec)
    counts = Counter((hit.passage_id, hit.term_id) for hit in study.hits)
    query_ids = tuple(term.term_id for term in spec.terms)
    units = tuple(
        SourceUnit(
            passage_id=passage.passage_id,
            work_id=passage.work_id,
            title=passage.title,
            edition_id=passage.edition_id,
            copy_id=passage.copy_id,
            text_sha256=digest(passage.text.encode()),
            tokens=len(tokenize(passage.text).terms),
            occurrences={query: counts[(passage.passage_id, query)] for query in query_ids},
        )
        for passage in passages
        if passage.text_role == "primary"
        and passage.source_plane == "reading"
        and passage.author_id == "william-blake-1757-1827"
    )
    return analyze_inventory(units, query_ids, runtime_profile(RetrievalProfile.NFKC_TOKENS_V2))


def default_proximity_grid() -> ProximityGrid:
    """Declare private lexical pairs independently from the NFKC study vocabulary."""
    return ProximityGrid(
        requests=tuple(
            SearchRequest(
                terms=pair,
                mode="all",
                window_words=width,
                role=Role.PRIMARY,
                plane=Plane.READING,
                whole_words=True,
                limit=1,
                context_chars=0,
            )
            for pair in PAIRS
            for width in WIDTHS
        )
    )


def literal_proximity_from_bundle(
    bundle: Path, binding: ProximityBinding, grid: ProximityGrid | None = None
) -> ProximityStudy:
    """Verify portable bytes before explicit conversion to literal-search inputs."""
    snapshot = load_proximity_bundle(bundle, binding)
    pin = binding.projection_pin
    return build_proximity_study(
        bundle_to_projection(snapshot.passages),
        pin,
        default_proximity_grid() if grid is None else grid,
    )


def load_proximity_bundle(bundle: Path, binding: ProximityBinding) -> ApplicationBundle:
    """Require exact portable bytes and their three projection corpus identities."""
    snapshot = load_bundle(bundle, binding.bundle_manifest_sha256)
    manifest = snapshot.manifest
    pin = binding.projection_pin
    if (
        manifest.captured_manifest_sha256 != pin.captured_manifest_sha256
        or manifest.projection_manifest_sha256 != pin.projection_manifest_sha256
        or manifest.index_sha256 != pin.index_sha256
    ):
        raise EvidenceError("corpus_pin_mismatch", str(bundle))
    return snapshot
