"""Apply shared Blake methods and bind every result to its inputs."""

import csv
import hashlib
import io
import json
from collections import Counter
from importlib.resources import files
from pathlib import Path
from typing import Final

from blake.applications import load_bundle
from blake.studies import StudyHit, StudyRow, StudySpec, StudySummary, scan_passages, summarize
from pydantic import TypeAdapter
from typing_extensions import TypedDict

from . import __version__
from .models import (
    Artifact,
    CorpusPin,
    Decision,
    EvidenceError,
    ReviewDecision,
    ReviewSummary,
    RunReceipt,
    is_animal_decision,
)


class ReviewQueueRow(TypedDict):
    hit_id: str
    term_id: str
    source_plane: str
    text_role: str
    passage_id: str
    title: str
    locator: str
    source_url: str
    expression: str
    context: str
    decision: str
    reviewer: str
    rationale: str
    verification_locator: str


QUEUE_ADAPTER: Final = TypeAdapter(ReviewQueueRow)


def queue_row(hit: StudyHit) -> ReviewQueueRow:
    """Project known hit fields while preserving blank, unreviewed decisions."""
    return ReviewQueueRow(
        hit_id=hit.hit_id,
        term_id=hit.term_id,
        source_plane=hit.source_plane,
        text_role=hit.text_role,
        passage_id=hit.passage_id,
        title=hit.title,
        locator=hit.locator,
        source_url=hit.source_url,
        expression=hit.expression,
        context=hit.context,
        decision="",
        reviewer="",
        rationale="",
        verification_locator="",
    )


def queue_identity(row: ReviewQueueRow) -> tuple[str, ...]:
    """Select every immutable evidence field from a review queue row."""
    return (
        row["hit_id"],
        row["term_id"],
        row["source_plane"],
        row["text_role"],
        row["passage_id"],
        row["title"],
        row["locator"],
        row["source_url"],
        row["expression"],
        row["context"],
    )


def csv_decisions(
    raw: bytes, hits: tuple[StudyHit, ...], run_sha256: str
) -> tuple[ReviewDecision, ...]:
    """Admit annotations only after CSV rows match the pinned candidate evidence."""
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline=""), strict=True)
    try:
        if tuple(reader.fieldnames or ()) != tuple(ReviewQueueRow.__annotations__):
            raise EvidenceError("csv_header", "Use the unchanged review-queue column header")
        by_id = {hit.hit_id: hit for hit in hits}
        seen: set[str] = set()
        decisions: list[ReviewDecision] = []
        for row_number, raw_row in enumerate(reader, start=2):
            if None in raw_row or any(value is None for value in raw_row.values()):
                raise EvidenceError("csv_row_width", str(row_number))
            row = QUEUE_ADAPTER.validate_python(raw_row, strict=True)
            identity = row["hit_id"]
            if identity not in by_id or identity in seen:
                raise EvidenceError("unknown_or_duplicate_hit", identity)
            seen.add(identity)
            if queue_identity(row) != queue_identity(queue_row(by_id[identity])):
                raise EvidenceError("csv_candidate_changed", identity)
            if not row["decision"].strip():
                if any(
                    row[field].strip()
                    for field in ("reviewer", "rationale", "verification_locator")
                ):
                    raise EvidenceError("partial_csv_annotation", identity)
                continue
            decisions.append(
                ReviewDecision.model_validate(
                    {
                        "run_sha256": run_sha256,
                        "hit_id": identity,
                        "decision": row["decision"],
                        "reviewer": row["reviewer"],
                        "rationale": row["rationale"],
                        "verification_locator": row["verification_locator"],
                    }
                )
            )
    except csv.Error as exc:
        raise EvidenceError("csv_format", str(exc)) from exc
    return tuple(decisions)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def application_code_sha256() -> str:
    """Bind analysis, review rules, CLI custody and version as one producer."""
    package = files("blakean_entomology")
    bindings = {
        name: digest(package.joinpath(name).read_bytes())
        for name in ("__init__.py", "core.py", "models.py", "cli.py")
    }
    return digest(json.dumps(bindings, sort_keys=True, separators=(",", ":")).encode())


def vocabulary(path: Path | None = None) -> StudySpec:
    raw = (
        path.read_bytes()
        if path
        else files("blakean_entomology").joinpath("resources/vocabulary.json").read_bytes()
    )
    return StudySpec.model_validate_json(raw)


def safe_directory(path: Path) -> None:
    if any(part.is_symlink() for part in (path, *path.parents)):
        raise EvidenceError("symlink_directory", str(path))


def reserve(path: Path) -> None:
    safe_directory(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.mkdir()  # Exclusive reservation; a failed run is retained for inspection.


def write_new(path: Path, raw: bytes) -> Artifact:
    safe_directory(path.parent)
    with path.open("xb") as handle:
        _ = handle.write(raw)
    return Artifact(name=path.name, size=len(raw), sha256=digest(raw))


def json_bytes(model: StudySummary | RunReceipt | ReviewSummary) -> bytes:
    return (model.model_dump_json(indent=2) + "\n").encode()


def analyze(bundle: Path, pin: CorpusPin, spec: StudySpec, output: Path) -> RunReceipt:
    """Scan all source units and write an immutable private review workspace."""
    snapshot = load_bundle(bundle, pin.bundle_manifest_sha256)
    identity = snapshot.manifest
    if (
        identity.captured_manifest_sha256 != pin.captured_manifest_sha256
        or identity.projection_manifest_sha256 != pin.projection_manifest_sha256
        or identity.index_sha256 != pin.index_sha256
    ):
        raise EvidenceError("corpus_pin_mismatch", str(bundle))
    source = bundle.resolve()
    target = output.resolve()
    if source.is_relative_to(target) or target.is_relative_to(source):
        raise EvidenceError("overlapping_output", str(output))
    result = scan_passages(snapshot.passages, spec)
    summary = summarize(result)
    reserve(output)
    artifacts: list[Artifact] = []
    artifacts.append(write_new(output / "summary.json", json_bytes(summary)))
    hit_bytes = "".join(hit.model_dump_json() + "\n" for hit in result.hits).encode()
    artifacts.append(write_new(output / "hits.jsonl", hit_bytes))
    count_buffer = io.StringIO(newline="")
    count_fields = list(StudyRow.model_fields)
    writer = csv.DictWriter(count_buffer, fieldnames=count_fields)
    writer.writeheader()
    writer.writerows(row.model_dump() for row in summary.rows)
    artifacts.append(write_new(output / "counts.csv", count_buffer.getvalue().encode()))
    queue = io.StringIO(newline="")
    queue_fields = list(ReviewQueueRow.__annotations__)
    queue_writer = csv.DictWriter(queue, fieldnames=queue_fields)
    queue_writer.writeheader()
    for hit in result.hits:
        queue_writer.writerow(queue_row(hit))
    artifacts.append(write_new(output / "review-queue.csv", queue.getvalue().encode()))
    artifacts.append(write_new(output / "report.md", report(summary, spec).encode()))
    receipt = RunReceipt(
        application_version=__version__,
        application_code_sha256=application_code_sha256(),
        corpus_pin=pin,
        spec_sha256=summary.spec_sha256,
        methods_sha256=summary.methods_sha256,
        normalization=summary.normalization,
        files=tuple(artifacts),
    )
    _ = write_new(output / "run.json", json_bytes(receipt))
    return receipt


def report(summary: StudySummary, spec: StudySpec) -> str:
    labels = {term.term_id: ", ".join(term.forms) for term in spec.terms}
    counts: Counter[str] = Counter()
    for row in summary.rows:
        counts[row.term_id] += row.occurrences
    lines = [
        "# Blakean Entomology: private candidate concordance",
        "",
        (
            f"Source units scanned: {summary.scanned_passages:,}. "
            + f"Search categories: {len(spec.terms)}."
        ),
        (
            f"Category-span candidates: {summary.total_occurrences:,}; Blake-primary candidates: "
            + f"{summary.blake_primary_occurrences:,}. Contextual animal decisions: not yet made."
        ),
        "",
        (
            "Counts retain source-copy repetition, homographs and category overlap. XML includes "
            + "editorial descriptions and markup. "
            + "These are retrieval totals, not animal or species totals."
        ),
        "",
        "| Category | Explicit forms | Candidates, all planes |",
        "|---|---|---:|",
    ]
    lines.extend(
        f"| {term.term_id} | {labels[term.term_id]} | {counts[term.term_id]} |"
        for term in spec.terms
    )
    lines += [
        "",
        (
            "See counts.csv for all role/plane cells including zeros, summary.json for "
            + "denominators, hits.jsonl for complete source-bound spans, and review-queue.csv for "
            + "unreviewed contexts. A blank decision is unreviewed, "
            + "never a negative animal finding."
        ),
        "",
        f"Vocabulary SHA256: {summary.spec_sha256}",
        f"Methods SHA256: {summary.methods_sha256}",
        "",
    ]
    return "\n".join(lines)


def load_run(directory: Path) -> tuple[RunReceipt, StudySummary, tuple[StudyHit, ...]]:
    """Reject missing, modified or incomplete output before contextual review."""
    safe_directory(directory)
    receipt_path = directory / "run.json"
    if receipt_path.is_symlink():
        raise EvidenceError("symlink_receipt", str(receipt_path))
    receipt = RunReceipt.model_validate_json(receipt_path.read_bytes())
    names = [artifact.name for artifact in receipt.files]
    if len(set(names)) != len(names) or set(names) != {
        "summary.json",
        "hits.jsonl",
        "counts.csv",
        "review-queue.csv",
        "report.md",
    }:
        raise EvidenceError("artifact_membership", str(directory))
    for artifact in receipt.files:
        path = directory / artifact.name
        if path.is_symlink():
            raise EvidenceError("symlink_artifact", artifact.name)
        raw = path.read_bytes()
        if len(raw) != artifact.size or digest(raw) != artifact.sha256:
            raise EvidenceError("artifact_checksum", artifact.name)
    summary = StudySummary.model_validate_json((directory / "summary.json").read_bytes())
    with (directory / "hits.jsonl").open() as handle:
        hits = tuple(StudyHit.model_validate_json(line) for line in handle if line.strip())
    if (
        summary.spec_sha256 != receipt.spec_sha256
        or summary.methods_sha256 != receipt.methods_sha256
        or summary.normalization != receipt.normalization
        or summary.total_occurrences != len(hits)
        or len({hit.hit_id for hit in hits}) != len(hits)
    ):
        raise EvidenceError("result_membership", str(directory))
    return receipt, summary, hits


def review(directory: Path, decisions_path: Path, expected_run_sha256: str) -> ReviewSummary:
    """Admit explicitly authored decisions against one exact candidate run."""
    if digest((directory / "run.json").read_bytes()) != expected_run_sha256:
        raise EvidenceError("review_run_pin", str(directory))
    _receipt, _summary, hits = load_run(directory)
    raw = decisions_path.read_bytes()
    if decisions_path.suffix.casefold() == ".csv":
        decisions = csv_decisions(raw, hits, expected_run_sha256)
    else:
        decisions = tuple(
            ReviewDecision.model_validate_json(line) for line in raw.splitlines() if line.strip()
        )
    by_id = {hit.hit_id: hit for hit in hits}
    seen: set[str] = set()
    counts: Counter[Decision] = Counter()
    primary_animal = 0
    exploratory_animal = 0
    for decision in decisions:
        if decision.run_sha256 != expected_run_sha256:
            raise EvidenceError("decision_run_pin", decision.hit_id)
        if decision.hit_id not in by_id or decision.hit_id in seen:
            raise EvidenceError("unknown_or_duplicate_hit", decision.hit_id)
        seen.add(decision.hit_id)
        counts[decision.decision] += 1
        if is_animal_decision(decision.decision):
            if by_id[decision.hit_id].blake_primary:
                primary_animal += 1
            else:
                exploratory_animal += 1
    return ReviewSummary(
        application_version=__version__,
        application_code_sha256=application_code_sha256(),
        run_sha256=expected_run_sha256,
        decisions_sha256=digest(raw),
        candidate_hits=len(hits),
        reviewed_hits=len(decisions),
        unreviewed_hits=len(hits) - len(decisions),
        decisions={choice: counts[choice] for choice in Decision},
        primary_animal_hits=primary_animal,
        exploratory_animal_hits=exploratory_animal,
    )
