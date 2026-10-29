"""Apply shared Blake methods and bind every result to its inputs."""

import csv
import io
from collections import Counter
from importlib.resources import files
from pathlib import Path

from blake.applications import load_bundle
from blake.methods.annotations import (
    ReviewQueueRow,
    count_decisions,
    queue_row,
    validate_decision_membership,
)
from blake.methods.annotations import csv_decisions as parse_csv_decisions
from blake.methods.runs import (
    digest as digest,
)
from blake.methods.runs import (
    read_regular,
    require_run_pin,
    reserve,
    verify_artifacts,
)
from blake.methods.runs import safe_directory as safe_directory
from blake.methods.runs import (
    write_new as write_new,
)
from blake.studies import StudyHit, StudyRow, StudySpec, StudySummary, scan_passages, summarize

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
from .producer import application_code_sha256 as application_code_sha256


def csv_decisions(
    raw: bytes, hits: tuple[StudyHit, ...], run_sha256: str
) -> tuple[ReviewDecision, ...]:
    """Apply private decision policy after shared immutable candidate checks."""
    return tuple(
        ReviewDecision.model_validate(item.model_dump())
        for item in parse_csv_decisions(raw, hits, run_sha256)
    )


def vocabulary(path: Path | None = None) -> StudySpec:
    raw = (
        path.read_bytes()
        if path
        else files("blakean_entomology").joinpath("resources/vocabulary.json").read_bytes()
    )
    return StudySpec.model_validate_json(raw)


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


def load_run(
    directory: Path, expected_run_sha256: str | None = None
) -> tuple[RunReceipt, StudySummary, tuple[StudyHit, ...]]:
    """Reject missing, modified or incomplete output before contextual review."""
    raw_receipt = (
        read_regular(directory / "run.json", "receipt")
        if expected_run_sha256 is None
        else require_run_pin(directory, expected_run_sha256)
    )
    receipt = RunReceipt.model_validate_json(raw_receipt)
    payloads = verify_artifacts(
        directory,
        receipt.files,
        {
            "summary.json",
            "hits.jsonl",
            "counts.csv",
            "review-queue.csv",
            "report.md",
        },
    )
    summary = StudySummary.model_validate_json(payloads["summary.json"])
    hits = tuple(
        StudyHit.model_validate_json(line)
        for line in payloads["hits.jsonl"].splitlines()
        if line.strip()
    )
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
    _receipt, _summary, hits = load_run(directory, expected_run_sha256)
    raw = decisions_path.read_bytes()
    if decisions_path.suffix.casefold() == ".csv":
        decisions = csv_decisions(raw, hits, expected_run_sha256)
    else:
        decisions = tuple(
            ReviewDecision.model_validate_json(line) for line in raw.splitlines() if line.strip()
        )
    by_id = {hit.hit_id: hit for hit in hits}
    validate_decision_membership(decisions, hits, expected_run_sha256)
    totals = count_decisions(decisions, len(hits), tuple(choice.value for choice in Decision))
    primary_animal = 0
    exploratory_animal = 0
    for decision in decisions:
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
        candidate_hits=totals.candidate_hits,
        reviewed_hits=totals.reviewed_hits,
        unreviewed_hits=totals.unreviewed_hits,
        decisions={choice: totals.decisions[choice.value] for choice in Decision},
        primary_animal_hits=primary_animal,
        exploratory_animal_hits=exploratory_animal,
    )
