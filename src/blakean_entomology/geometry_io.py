"""Caller-pinned geometry inputs and text-free tabular export."""

import csv
import io
import json
from dataclasses import dataclass
from pathlib import Path

from blake.methods.runs import digest, read_regular
from blake.studies import StudyHit, StudySpec
from blake.text_search.models import Passage
from pydantic import TypeAdapter

from .core import load_run
from .geometry_models import DocumentedWindow, GeometryReport, GeometryRequest
from .models import EvidenceError, ReviewDecision
from .workflows import load_pinned_bundle


@dataclass(frozen=True, slots=True)
class GeometryInputs:
    request: GeometryRequest
    input_hashes: dict[str, str]
    passages: tuple[Passage, ...]
    hits: tuple[StudyHit, ...]
    decisions: tuple[ReviewDecision, ...]
    windows: tuple[DocumentedWindow, ...]
    spec: StudySpec


def read_geometry_inputs(
    request_path: Path,
    expected_request_sha256: str,
    bundle: Path,
    run: Path,
    decisions: Path,
    windows: Path,
    vocabulary: Path,
) -> GeometryInputs:
    """Verify the old run fully; a geometry epoch does not rerun its matcher."""
    raw_request = read_regular(request_path)
    if digest(raw_request) != expected_request_sha256:
        raise EvidenceError("geometry_request_pin", str(request_path))
    request = GeometryRequest.model_validate_json(raw_request)
    paths = {"decisions": decisions, "windows": windows, "vocabulary": vocabulary}
    payloads = {name: read_regular(path) for name, path in paths.items()}
    hashes = {name: digest(raw) for name, raw in payloads.items()}
    if any(
        hashes[name] != expected
        for name, expected in (
            ("decisions", request.decisions_sha256),
            ("windows", request.windows_sha256),
            ("vocabulary", request.vocabulary_sha256),
        )
    ):
        raise EvidenceError("geometry_input_pin", "Request input bytes differ")
    snapshot = load_pinned_bundle(bundle, request.corpus_pin)
    receipt, summary, hits = load_run(run, request.run_sha256)
    if receipt.corpus_pin != request.corpus_pin or summary.scanned_passages != len(
        snapshot.passages
    ):
        raise EvidenceError("geometry_run_identity", "Run and source inventory differ")
    # Historical models retain their own coercion contract. New geometry also
    # admits every original raw hit under strict scalar rules, before using it.
    for line in read_regular(run / "hits.jsonl").splitlines():
        if line.strip():
            _ = StudyHit.model_validate_json(line, strict=True)
    spec = StudySpec.model_validate_json(payloads["vocabulary"], strict=True)
    canonical = json.dumps(
        spec.model_dump(mode="json"), sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode()
    if digest(canonical) != receipt.spec_sha256:
        raise EvidenceError("geometry_vocabulary_identity", "Vocabulary differs from original run")
    judgments = tuple(
        ReviewDecision.model_validate_json(line, strict=True)
        for line in payloads["decisions"].splitlines()
        if line.strip()
    )
    reading = TypeAdapter(tuple[DocumentedWindow, ...]).validate_json(
        payloads["windows"], strict=True
    )
    return GeometryInputs(
        request=request,
        passages=snapshot.passages,
        hits=hits,
        decisions=judgments,
        windows=reading,
        spec=spec,
        input_hashes={
            **hashes,
            "request": expected_request_sha256,
            "run": request.run_sha256,
            "bundle": request.corpus_pin.bundle_manifest_sha256,
        },
    )


def source_geometry_csv(report: GeometryReport) -> bytes:
    """Expose all source denominators; unknown reading windows remain explicit."""
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(
        (
            "passage_id",
            "work_id",
            "role",
            "plane",
            "author_id",
            "text_sha256",
            "codepoints",
            "candidates",
            "summed_codepoints",
            "union_codepoints",
            "overlap_codepoints",
            "excess_codepoints",
            "overlapping_pairs",
            "source_components",
            "reviewed_hits",
            "reviewed_union_codepoints",
            "unreviewed_union_codepoints",
            "documented_window_events",
            "documented_window_codepoints",
            "reviewed_without_documented_window",
        )
    )
    for source in report.sources:
        measure = source.measure
        writer.writerow(
            (
                source.passage_id,
                source.work_id,
                source.role,
                source.plane,
                source.author_id,
                source.text_sha256,
                source.codepoints,
                measure.records,
                measure.summed_codepoints,
                measure.union_codepoints,
                measure.overlap_codepoints,
                measure.excess_codepoints,
                measure.overlapping_pairs,
                measure.source_components,
                source.reviewed_hits,
                source.reviewed_union_codepoints,
                source.unreviewed_union_codepoints,
                source.documented_window_events,
                "unavailable"
                if source.documented_window_codepoints is None
                else source.documented_window_codepoints,
                source.reviewed_without_documented_window,
            )
        )
    return stream.getvalue().encode()
