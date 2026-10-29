"""Portable, typed, text-free composition epochs; historical receipts stay intact.

Size policy (# noqa: SIZE_OK): user-owned workflow contains its typed receipt
boundary and source custody.
"""

from __future__ import annotations

import csv
import io
import json
import sys
from collections.abc import Sequence
from importlib import metadata, resources
from pathlib import Path
from typing import Final, Literal

from blake.methods.compatibility import bundle_to_projection
from blake.methods.models import (
    Artifact,
    Digest,
    EvidenceError,
    FrozenModel,
    Plane,
    Role,
)
from blake.methods.producer import SourceBinding, source_hashes
from blake.methods.profiles import RetrievalProfile, RuntimeProfile, runtime_profile
from blake.methods.proximity import ProximityGrid, ProximityStudy, build_proximity_study
from blake.methods.runs import (
    digest,
    read_regular,
    reserve,
    safe_directory,
    verify_artifacts,
    write_new,
)
from blake.methods.search_models import SearchRequest
from blake.studies import StudySpec
from pydantic import Field

from .atlas import atlas_from_passages
from .atlas_models import AtlasReceipt, ReviewEpoch
from .composition import (
    CHANNELS,
    LITERAL_PAIRS,
    WIDTHS,
    composition_audit,
    inventory_from_atlas,
)
from .models import CorpusPin
from .sensitivity import analyze_sensitivity
from .workflows import ProximityReceipt, SensitivityReceipt, load_pinned_bundle

EXPORTS: Final = frozenset(
    {
        "composition.json",
        "composition-categories.csv",
        "omission-effects.csv",
        "name-work-matrix.csv",
        "source-channels.csv",
        "category-source-channels.csv",
        "literal-relationships.json",
        "literal-pairs.csv",
        "literal-pair-work.csv",
    }
)


class CompositionInputs(FrozenModel):
    """Explicit paths and trusted atlas digest; no machine or epoch path inference."""

    atlas: Path
    atlas_sha256: Digest
    sensitivity: Path
    bundle: Path
    pin: Path
    vocabulary: Path
    proximity: Path


class InputBinding(FrozenModel):
    path: str
    sha256: Digest
    size: int = Field(ge=0)


class SourceCensus(FrozenModel):
    captured_units: int
    all_category_candidates: int
    primary_candidates: int
    categories: int
    explicit_forms: int
    primary_units: int
    primary_work_groups: int
    nfkc_tokens: int
    exact_text_units: int
    literal_tokens: int


class SourceOrigin(FrozenModel):
    """Actual imported package bytes; installed distribution metadata is separate."""

    sdk_root: str
    application_root: str
    sdk_distribution_version: str
    sdk_distribution_direct_url: str | None
    code_sha256: Digest
    code: dict[str, str]


class ProducerEpochs(FrozenModel):
    historical_atlas_application: Digest
    historical_atlas_methods: Digest
    historical_sensitivity_application: Digest
    historical_proximity_application: Digest
    current_atlas_application: Digest
    current_atlas_methods: Digest
    comparison: Literal["identical numerical payloads, profiles and denominators"] = (
        "identical numerical payloads, profiles and denominators"
    )


class CompositionRun(FrozenModel):
    schema_version: Literal[1] = 1
    epoch: Literal["composition-expansion-v1"] = "composition-expansion-v1"
    status: Literal["source-candidate"] = "source-candidate"
    atlas_sha256: Digest
    inputs: tuple[InputBinding, ...]
    files: tuple[Artifact, ...]
    source_origin: SourceOrigin
    producer_epochs: ProducerEpochs
    python: str
    prefix: str
    base_prefix: str
    nfkc_profile: RuntimeProfile
    literal_profile: RuntimeProfile
    source_census: SourceCensus
    history: ReviewEpoch | None
    interpretation: str = (
        "Finite category-source-span inventory; copies, nested categories and unreviewed senses "
        "retained. Equal composition averages only positive-mass group profiles; zero groups stay "
        "in coverage exports. Literal pairs use separate complete original-word envelopes. "
        "No new animal decisions, image claims, independent-work or complete-oeuvre claims. "
        "Source qualification does not establish installation of these new bytes."
    )


class MatrixRow(FrozenModel):
    work_id: str
    category: str
    candidates: int
    matched_units: int
    eligible_source_units: int
    nfkc_tokens: int
    rate_per_10000_tokens: float | None
    within_work_name_category_share: float | None


class ChannelRow(FrozenModel):
    role: str
    plane: str
    author_id: str
    channel: str
    categories: int
    observed_categories: int
    source_units: int
    nfkc_tokens: int
    category_candidates: int
    exact_text_category_candidates: int


class CategoryChannelRow(FrozenModel):
    role: str
    plane: str
    author_id: str
    category: str
    registry_group: str
    channel: str
    candidates: int
    matched_units: int
    source_units: int
    nfkc_tokens: int
    exact_text_candidates: int


class PairRow(FrozenModel):
    pair: str
    window_words: int | Literal["whole_unit"]
    matched_units: int
    eligible_units: int
    matched_work_groups: int
    eligible_work_groups: int
    literal_tokens: int


class PairWorkRow(FrozenModel):
    pair: str
    window_words: int | Literal["whole_unit"]
    work_id: str
    matched_units: int
    eligible_units: int
    literal_tokens: int


def encode(value: FrozenModel) -> bytes:
    """Serialize a validated receipt; NaN and unknown fields cannot enter via raw JSON."""
    return (value.model_dump_json(indent=2) + "\n").encode()


def table(rows: Sequence[FrozenModel]) -> bytes:
    """Export a nonempty typed row sequence without discarding zero or undefined cells."""
    if not rows:
        raise EvidenceError("composition_table", "Require explicit rows")
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(type(rows[0]).model_fields))
    writer.writeheader()
    writer.writerows(row.model_dump() for row in rows)
    return buffer.getvalue().encode()


def verify_destination(output: Path, output_root: Path, sources: tuple[Path, ...]) -> None:
    """Reject occupied, linked, escaping or input-overlapping outputs before publication."""
    safe_directory(output)
    safe_directory(output_root)
    target, root = output.absolute(), output_root.absolute()
    if (
        ".." in output.parts
        or ".." in output_root.parts
        or not target.is_relative_to(root)
        or target == root
    ):
        raise EvidenceError(
            "composition_output", "Require a new child of explicit private output root"
        )
    if output.exists():
        raise FileExistsError(str(output))
    if any(
        target.is_relative_to(p.absolute()) or p.absolute().is_relative_to(target) for p in sources
    ):
        raise EvidenceError("composition_overlap", str(output))


def fingerprint(paths: tuple[Path, ...]) -> tuple[InputBinding, ...]:
    """Bind actual regular-file bytes, before computation and immediately before publication."""
    return tuple(
        InputBinding(path=str(p.absolute()), sha256=digest(raw), size=len(raw))
        for p in paths
        for raw in (read_regular(p),)
    )


def source_origin() -> SourceOrigin:
    """Fingerprint conservative imported source closure, including the new generic module."""
    bindings = tuple(
        SourceBinding(
            package,
            tuple(
                sorted(p.name for p in resources.files(package).iterdir() if p.name.endswith(".py"))
            ),
        )
        for package in ("blake.methods", "blake.text_search", "blakean_entomology")
    )
    bindings += (
        SourceBinding("blake", ("__init__.py", "applications.py", "studies.py", "version.py")),
    )
    code = source_hashes(bindings)
    raw = json.dumps(code, sort_keys=True, separators=(",", ":")).encode()
    return SourceOrigin(
        sdk_root=str(resources.files("blake")),
        application_root=str(resources.files("blakean_entomology")),
        sdk_distribution_version=metadata.version("blake"),
        sdk_distribution_direct_url=metadata.distribution("blake").read_text("direct_url.json"),
        code_sha256=digest(raw),
        code=code,
    )


def make_payloads(
    atlas: AtlasReceipt, spec: StudySpec, proximity: ProximityStudy
) -> dict[str, bytes]:
    """Construct nine text-free products using domain selection and public composition."""
    cohort = next(
        c
        for c in atlas.cohorts
        if (c.role, c.plane, c.author_id) == ("primary", "reading", "william-blake-1757-1827")
    )
    inventory = inventory_from_atlas(spec, cohort.works)
    audit = composition_audit(inventory, cohort.categories)
    matrix = tuple(
        MatrixRow(
            work_id=w.group_id,
            category=category,
            candidates=w.counts[i],
            matched_units=w.matched_units[i],
            eligible_source_units=w.source_units,
            nfkc_tokens=w.tokens,
            rate_per_10000_tokens=10000 * w.counts[i] / w.tokens if w.tokens else None,
            within_work_name_category_share=w.counts[i] / sum(w.counts) if sum(w.counts) else None,
        )
        for w in inventory.groups
        for i, category in enumerate(inventory.categories)
    )
    channels: list[ChannelRow] = []
    categories: list[CategoryChannelRow] = []
    for c in atlas.cohorts:
        query = {q.query_id: q for q in c.categories}
        if set(query) != {t.term_id for t in spec.terms}:
            raise EvidenceError("composition_categories", "Complete registry summaries required")
        for channel in sorted(set(CHANNELS.values())):
            ids = tuple(t.term_id for t in spec.terms if CHANNELS[t.group] == channel)
            channels.append(
                ChannelRow(
                    role=c.role,
                    plane=c.plane,
                    author_id=c.author_id,
                    channel=channel,
                    categories=len(ids),
                    observed_categories=sum(query[q].copy_retaining.occurrences > 0 for q in ids),
                    source_units=c.source_units,
                    nfkc_tokens=c.tokens,
                    category_candidates=sum(query[q].copy_retaining.occurrences for q in ids),
                    exact_text_category_candidates=sum(
                        query[q].exact_text.occurrences for q in ids
                    ),
                )
            )
        for t in spec.terms:
            q = query[t.term_id]
            categories.append(
                CategoryChannelRow(
                    role=c.role,
                    plane=c.plane,
                    author_id=c.author_id,
                    category=t.term_id,
                    registry_group=t.group,
                    channel=CHANNELS[t.group],
                    candidates=q.copy_retaining.occurrences,
                    matched_units=q.copy_retaining.matched_units,
                    source_units=c.source_units,
                    nfkc_tokens=c.tokens,
                    exact_text_candidates=q.exact_text.occurrences,
                )
            )
    pairs = tuple(
        PairRow(
            pair="+".join(r.request.terms),
            window_words=r.request.window_words
            if r.request.window_words is not None
            else "whole_unit",
            matched_units=r.matched_source_units,
            eligible_units=r.eligible_source_units,
            matched_work_groups=r.matched_source_families,
            eligible_work_groups=r.eligible_source_families,
            literal_tokens=r.eligible_word_tokens,
        )
        for r in proximity.rows
    )
    pairworks = tuple(
        PairWorkRow(
            pair="+".join(r.request.terms),
            window_words=r.request.window_words
            if r.request.window_words is not None
            else "whole_unit",
            work_id=f.work_id,
            matched_units=f.matched_units,
            eligible_units=f.source_units,
            literal_tokens=f.word_tokens,
        )
        for r in proximity.rows
        for f in r.facets
    )
    return {
        "composition.json": encode(audit),
        "composition-categories.csv": table(audit.categories),
        "omission-effects.csv": table(audit.omissions),
        "name-work-matrix.csv": table(matrix),
        "source-channels.csv": table(channels),
        "category-source-channels.csv": table(categories),
        "literal-relationships.json": encode(proximity),
        "literal-pairs.csv": table(pairs),
        "literal-pair-work.csv": table(pairworks),
    }


def generate(inputs: CompositionInputs, output: Path, output_root: Path) -> CompositionRun:
    """Verify source bytes and recompute current SDK numbers without rebasing old producers."""
    paths = (
        inputs.atlas,
        inputs.pin,
        inputs.vocabulary,
        inputs.sensitivity,
        inputs.proximity,
        inputs.bundle / "manifest.json",
        inputs.bundle / "passages.jsonl",
    )
    verify_destination(output, output_root, (*paths, inputs.bundle))
    before = fingerprint(paths)
    origin = source_origin()
    raw_atlas = read_regular(inputs.atlas)
    if digest(raw_atlas) != inputs.atlas_sha256:
        raise EvidenceError("composition_atlas_pin", "atlas SHA-256 mismatch")
    atlas = AtlasReceipt.model_validate_json(raw_atlas)
    pin = CorpusPin.model_validate_json(read_regular(inputs.pin))
    spec = StudySpec.model_validate_json(read_regular(inputs.vocabulary))
    sensitivity = SensitivityReceipt.model_validate_json(read_regular(inputs.sensitivity))
    old_proximity = ProximityReceipt.model_validate_json(read_regular(inputs.proximity))
    nfkc = runtime_profile(RetrievalProfile.NFKC_TOKENS_V2)
    literal = runtime_profile(RetrievalProfile.LITERAL_CASEFOLD_V1)
    registry = json.dumps(
        spec.model_dump(mode="json"), sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode()
    projection = old_proximity.binding.projection_pin
    if (
        pin != atlas.corpus_pin
        or pin != sensitivity.corpus_pin
        or digest(registry) != atlas.vocabulary_sha256
        or sensitivity.spec_sha256 != atlas.vocabulary_sha256
        or atlas.profile != nfkc
        or sensitivity.profile != nfkc
        or old_proximity.profile != literal
        or old_proximity.binding.bundle_manifest_sha256 != pin.bundle_manifest_sha256
        or any(
            getattr(projection, f) != getattr(pin, f)
            for f in ("captured_manifest_sha256", "projection_manifest_sha256", "index_sha256")
        )
    ):
        raise EvidenceError("composition_binding", "Pin, registry or retrieval profile mismatch")
    snapshot = load_pinned_bundle(inputs.bundle, pin)
    # Recompute the entire atlas on actual bytes; ignore only named producer/history fields.
    current = atlas_from_passages(snapshot.passages, spec, pin, atlas.reference_sha256)
    excluded = {
        "application_code_sha256",
        "methods_sha256",
        "historical_review",
        "historical_review_summary_sha256",
    }
    if current.model_dump(exclude=excluded) != atlas.model_dump(exclude=excluded):
        raise EvidenceError("composition_atlas_replay", "Actual source atlas numbers differ")
    statistics = analyze_sensitivity(snapshot.passages, spec)
    if statistics != sensitivity.statistics:
        raise EvidenceError(
            "composition_inventory_replay", "Actual source counts/profile/denominators differ"
        )
    projection_passages = bundle_to_projection(snapshot.passages)
    old_replay = build_proximity_study(projection_passages, projection, old_proximity.study.grid)
    if old_replay != old_proximity.study:
        raise EvidenceError("composition_proximity_replay", "Historical proximity numbers differ")
    primary = tuple(
        p
        for p in snapshot.passages
        if (p.text_role, p.source_plane, p.author_id)
        == ("primary", "reading", "william-blake-1757-1827")
    )
    grid = ProximityGrid(
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
            for pair in LITERAL_PAIRS
            for width in WIDTHS
        )
    )
    proximity = build_proximity_study(bundle_to_projection(primary), projection, grid)
    payloads = make_payloads(atlas, spec, proximity)
    cohort = next(
        c
        for c in atlas.cohorts
        if (c.role, c.plane, c.author_id) == ("primary", "reading", "william-blake-1757-1827")
    )
    run = CompositionRun(
        atlas_sha256=inputs.atlas_sha256,
        inputs=before,
        files=tuple(Artifact(name=n, size=len(b), sha256=digest(b)) for n, b in payloads.items()),
        source_origin=origin,
        producer_epochs=ProducerEpochs(
            historical_atlas_application=atlas.application_code_sha256,
            historical_atlas_methods=atlas.methods_sha256,
            historical_sensitivity_application=sensitivity.application_code_sha256,
            historical_proximity_application=old_proximity.application_code_sha256,
            current_atlas_application=current.application_code_sha256,
            current_atlas_methods=current.methods_sha256,
        ),
        python=sys.version,
        prefix=sys.prefix,
        base_prefix=sys.base_prefix,
        nfkc_profile=nfkc,
        literal_profile=literal,
        source_census=SourceCensus(
            captured_units=atlas.scanned_units,
            all_category_candidates=atlas.candidates,
            primary_candidates=atlas.primary_candidates,
            categories=atlas.category_count,
            explicit_forms=atlas.explicit_form_count,
            primary_units=len(primary),
            primary_work_groups=cohort.work_groups,
            nfkc_tokens=cohort.tokens,
            exact_text_units=cohort.exact_text_units,
            literal_tokens=proximity.rows[0].eligible_word_tokens,
        ),
        history=atlas.historical_review,
    )
    _ = load_pinned_bundle(inputs.bundle, pin)
    if fingerprint(paths) != before or source_origin() != origin:
        raise EvidenceError(
            "composition_changed", "Source bytes/producer changed during computation"
        )
    reserve(output)
    for name, raw in payloads.items():
        _ = write_new(output / name, raw)
    _ = verify_artifacts(output, run.files, EXPORTS)
    if fingerprint(paths) != before or source_origin() != origin:
        raise EvidenceError(
            "composition_changed", "Source bytes/producer changed during publication"
        )
    _ = write_new(output / "run.json", encode(run))
    return run
