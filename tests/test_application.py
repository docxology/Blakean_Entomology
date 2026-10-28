"""Behavioral controls for application custody and contextual decisions."""

import csv
import io
import json
import tarfile
from collections import Counter
from pathlib import Path

import pytest
from blake.applications import (
    ApplicationBundleManifest,
    ApplicationFile,
    ApplicationProducer,
    PassageBinding,
)
from blake.recovery import recover_corpus
from blake.studies import StudySpec, StudyTerm
from blake.text_search.models import Passage
from blake.text_search.recovered import build_recovered_search
from click.testing import CliRunner

from blakean_entomology.cli import main
from blakean_entomology.core import analyze, digest, load_run, review, vocabulary
from blakean_entomology.models import CorpusPin, EvidenceError, ReviewDecision, RunReceipt


@pytest.fixture
def inputs(tmp_path: Path) -> tuple[Path, CorpusPin, StudySpec, Path]:
    passages = tuple(
        Passage(
            passage_id=identity,
            work_id="synthetic",
            author_id="william-blake-1757-1827" if role == "primary" else "mixed-edition",
            title="Synthetic control, not a Blake quotation",
            edition_id=identity,
            edition="Test edition",
            locator="test section",
            locator_kind="section",
            source_url="https://example.org/control",
            rights="Synthetic test fixture",
            text_role=role,
            source_plane=plane,
            source_sha256="a" * 64,
            text=text,
        )
        for identity, role, plane, text in (
            ("p1", "primary", "reading", 'An Emmet saw a bee;\n"the worm" can fly.'),
            ("p2", "primary", "reading", 'An Emmet saw a bee;\n"the worm" can fly.'),
            ("e1", "editorial", "erdman", "A Mite in the hand; flies fly."),
        )
    )
    raw = ("".join(p.model_dump_json() + "\n" for p in passages)).encode()
    manifest = ApplicationBundleManifest(
        captured_manifest_sha256="b" * 64,
        projection_manifest_sha256="c" * 64,
        index_sha256="d" * 64,
        archive_commit="recorded-test-identity",
        normalization="nfkc-casefold-source-spans-v2",
        producer=ApplicationProducer(
            blake_version="0.2.0",
            python="3.11",
            exporter_sha256="e" * 64,
            projection_producer_sha256="f" * 64,
        ),
        passages_file=ApplicationFile(size=len(raw), sha256=digest(raw)),
        passages=len(passages),
        passage_ids=tuple(p.passage_id for p in passages),
        passage_bindings=tuple(
            PassageBinding(
                passage_id=p.passage_id,
                text_sha256=digest(p.text.encode()),
                source_sha256="a" * 64,
            )
            for p in passages
        ),
        passages_by_role=dict(Counter(p.text_role for p in passages)),
        passages_by_plane=dict(Counter(p.source_plane for p in passages)),
        passages_by_author=dict(Counter(p.author_id for p in passages)),
    )
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    (bundle / "passages.jsonl").write_bytes(raw)
    manifest_raw = (manifest.model_dump_json(indent=2) + "\n").encode()
    (bundle / "manifest.json").write_bytes(manifest_raw)
    pin = CorpusPin(
        bundle_manifest_sha256=digest(manifest_raw),
        captured_manifest_sha256="b" * 64,
        projection_manifest_sha256="c" * 64,
        index_sha256="d" * 64,
    )
    spec = StudySpec(
        study_id="synthetic-invertebrate-control",
        title="Test",
        terms=tuple(
            StudyTerm(term_id=name, forms=forms, group="test")
            for name, forms in (
                ("ant", ("ant", "emmet")),
                ("bee", ("bee",)),
                ("worm", ("worm",)),
                ("fly", ("fly", "flies")),
                ("mite", ("mite",)),
                ("spider", ("spider",)),
            )
        ),
    )
    return bundle, pin, spec, tmp_path / "run"


@pytest.fixture
def recovered_source(tmp_path: Path) -> Path:
    """Capture small real source files through the shared offline recovery API."""
    commit = "a" * 40
    source = tmp_path / "source"
    sources = source / "recovery/sources"
    sources.mkdir(parents=True)
    with tarfile.open(sources / f"blakearchive-{commit}.tar.gz", "w:gz") as archive:
        entries = {
            "works/__contents__.xml": b"<collection/>",
            "works/mhh.a.xml": (
                b'<bad work="Marriage"><phystext><l>An Emmet and a bee.</l></phystext></bad>'
            ),
        }
        for name, raw in entries.items():
            info = tarfile.TarInfo(f"data-{commit}/{name}")
            info.size = len(raw)
            archive.addfile(info, io.BytesIO(raw))
    erdman = sources / "erdman"
    erdman.mkdir()
    (erdman / "pages.json").write_text(
        json.dumps([{"id": 1, "page_id": "1", "contents": "<div>A fly.</div>"}])
    )
    recover_corpus(source, commit=commit, offline=True, images=False)
    build_recovered_search(source)
    return source


def rebind_artifacts(directory: Path) -> None:
    """Update receipts so semantic corruption reaches independent membership checks."""
    receipt = RunReceipt.model_validate_json((directory / "run.json").read_bytes())
    artifacts = tuple(
        artifact.model_copy(
            update={
                "size": (directory / artifact.name).stat().st_size,
                "sha256": digest((directory / artifact.name).read_bytes()),
            }
        )
        for artifact in receipt.files
    )
    (directory / "run.json").write_text(
        receipt.model_copy(update={"files": artifacts}).model_dump_json()
    )


def read_queue(directory: Path) -> tuple[list[str], list[dict[str, str]]]:
    with (directory / "review-queue.csv").open(newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or ()), list(reader)


def write_queue(path: Path, columns: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        writer.writerows([row.get(column, "") for column in columns] for row in rows)


def test_candidates_keep_verbs_money_and_duplicate_editions(inputs) -> None:
    bundle, pin, spec, output = inputs
    analyze(bundle, pin, spec, output)
    _receipt, summary, hits = load_run(output)
    assert summary.total_occurrences == 11
    assert summary.blake_primary_occurrences == 8
    assert len(hits) == 11
    assert {hit.expression for hit in hits if hit.term_id == "mite"} == {"Mite"}
    assert sum(row.occurrences for row in summary.rows if row.term_id == "spider") == 0
    assert len(summary.rows) == 54
    with (output / "review-queue.csv").open() as handle:
        queue = tuple(csv.DictReader(handle))
    assert len(queue) == 11
    assert all(not row["decision"] for row in queue)


def test_occupied_output_preserves_prior_receipt(inputs) -> None:
    bundle, pin, spec, output = inputs
    analyze(bundle, pin, spec, output)
    before = (output / "run.json").read_bytes()
    with pytest.raises(FileExistsError):
        analyze(bundle, pin, spec, output)
    assert (output / "run.json").read_bytes() == before


def test_changed_bundle_is_rejected_before_output(inputs) -> None:
    bundle, pin, spec, output = inputs
    with (bundle / "passages.jsonl").open("ab") as handle:
        handle.write(b"changed")
    with pytest.raises(ValueError, match="passages_checksum"):
        analyze(bundle, pin, spec, output)
    assert not output.exists()


def test_changed_source_identity_is_rejected(inputs) -> None:
    bundle, pin, spec, output = inputs
    other = pin.model_copy(update={"index_sha256": "0" * 64})
    with pytest.raises(EvidenceError, match="corpus_pin_mismatch"):
        analyze(bundle, other, spec, output)


@pytest.mark.parametrize("filename", ["hits.jsonl", "summary.json", "counts.csv"])
def test_changed_output_cannot_enter_review(inputs, filename: str) -> None:
    bundle, pin, spec, output = inputs
    analyze(bundle, pin, spec, output)
    with (output / filename).open("ab") as handle:
        handle.write(b"corruption")
    with pytest.raises(EvidenceError, match="artifact_checksum"):
        load_run(output)


def test_missing_completion_marker_cannot_enter_review(inputs) -> None:
    bundle, pin, spec, output = inputs
    analyze(bundle, pin, spec, output)
    (output / "run.json").rename(output / "retained-incomplete.json")
    with pytest.raises(FileNotFoundError):
        load_run(output)


def test_explicit_review_keeps_remaining_candidates_unreviewed(inputs, tmp_path: Path) -> None:
    bundle, pin, spec, output = inputs
    analyze(bundle, pin, spec, output)
    _receipt, _summary, hits = load_run(output)
    monetary = next(hit for hit in hits if hit.term_id == "mite")
    run_sha = digest((output / "run.json").read_bytes())
    decision = ReviewDecision(
        run_sha256=run_sha,
        hit_id=monetary.hit_id,
        decision="non_animal",
        reviewer="test reviewer",
        rationale="Synthetic monetary sense control",
    )
    decisions = tmp_path / "decisions.jsonl"
    decisions.write_text(decision.model_dump_json() + "\n")
    summary = review(output, decisions, run_sha)
    assert summary.reviewed_hits == 1
    assert summary.unreviewed_hits == 10
    assert summary.primary_animal_hits == 0
    assert summary.exploratory_animal_hits == 0


@pytest.mark.parametrize("mutation", ["unknown", "duplicate", "run"])
def test_wrong_decisions_cannot_change_animal_total(inputs, tmp_path: Path, mutation: str) -> None:
    bundle, pin, spec, output = inputs
    analyze(bundle, pin, spec, output)
    _receipt, _summary, hits = load_run(output)
    run_sha = digest((output / "run.json").read_bytes())
    decision = dict(
        run_sha256=run_sha,
        hit_id=hits[0].hit_id,
        decision="animal_literal",
        reviewer="test",
        rationale="Synthetic explicit animal",
        verification_locator="test section",
    )
    rows = [decision]
    match mutation:
        case "unknown":
            decision["hit_id"] = "unknown"
        case "duplicate":
            rows.append(decision.copy())
        case "run":
            decision["run_sha256"] = "0" * 64
    decisions = tmp_path / "decisions.jsonl"
    decisions.write_text("".join(json.dumps(row) + "\n" for row in rows))
    with pytest.raises(EvidenceError):
        review(output, decisions, run_sha)


def test_animal_decision_requires_verification_locator() -> None:
    with pytest.raises(ValueError, match="animal_locator_required"):
        ReviewDecision(
            run_sha256="0" * 64,
            hit_id="hit",
            decision="animal_literal",
            reviewer="reviewer",
            rationale="animal",
        )


def test_cli_analyze_and_verify_use_real_bundle(inputs, tmp_path: Path) -> None:
    bundle, pin, spec, output = inputs
    pin_file = tmp_path / "pin.json"
    pin_file.write_text(pin.model_dump_json())
    spec_file = tmp_path / "spec.json"
    spec_file.write_text(spec.model_dump_json())
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "analyze",
            "--bundle",
            str(bundle),
            "--pin",
            str(pin_file),
            "--vocabulary",
            str(spec_file),
            "--output",
            str(output),
        ],
    )
    assert result.exit_code == 0, result.output
    checked = runner.invoke(main, ["verify-run", str(output)])
    assert checked.exit_code == 0, checked.output
    assert json.loads(result.output)["corpus_pin"]["bundle_manifest_sha256"] == (
        pin.bundle_manifest_sha256
    )


def test_packaged_vocabulary_matches_editable_registry() -> None:
    registry = Path(__file__).resolve().parents[1] / "research/vocabulary.json"
    assert vocabulary().model_dump() == vocabulary(registry).model_dump()
    assert len(vocabulary().terms) >= 100


def test_summary_never_contains_provider_context(inputs) -> None:
    bundle, pin, spec, output = inputs
    analyze(bundle, pin, spec, output)
    raw = (output / "summary.json").read_bytes()
    assert b"An Emmet saw" not in raw
    assert b"expression" not in raw
    assert b"context" not in raw


def test_symlink_output_is_refused(inputs, tmp_path: Path) -> None:
    bundle, pin, spec, _output = inputs
    real = tmp_path / "real"
    real.mkdir()
    link = tmp_path / "link"
    link.symlink_to(real, target_is_directory=True)
    with pytest.raises(EvidenceError, match="symlink_directory"):
        analyze(bundle, pin, spec, link / "output")


@pytest.mark.parametrize("relationship", ["same", "child", "ancestor"])
def test_output_cannot_overlap_the_source_bundle(inputs, relationship: str) -> None:
    # Given a source snapshot and output roots that would contain its evidence.
    bundle, pin, spec, _output = inputs
    outputs = {"same": bundle, "child": bundle / "run", "ancestor": bundle.parent}

    # When analysis is asked to write into an overlapping root.
    with pytest.raises(EvidenceError, match="overlapping_output"):
        analyze(bundle, pin, spec, outputs[relationship])


@pytest.mark.parametrize("name", ["run.json", "hits.jsonl"])
def test_symlinked_run_files_are_refused(inputs, tmp_path: Path, name: str) -> None:
    # Given valid output replaced by a symlink to byte-identical retained evidence.
    bundle, pin, spec, output = inputs
    _ = analyze(bundle, pin, spec, output)
    retained = tmp_path / (name + ".retained")
    (output / name).rename(retained)
    (output / name).symlink_to(retained)

    # When the run is opened, then identical bytes cannot bypass regular-file custody.
    with pytest.raises(EvidenceError, match="symlink_receipt|symlink_artifact"):
        load_run(output)


@pytest.mark.parametrize("mutation", ["duplicate", "omitted"])
def test_incomplete_or_duplicate_artifact_membership_is_refused(inputs, mutation: str) -> None:
    # Given a receipt that no longer names exactly one of every required artifact.
    bundle, pin, spec, output = inputs
    receipt = analyze(bundle, pin, spec, output)
    files = list(receipt.files)
    if mutation == "duplicate":
        files.append(files[0])
    else:
        files.pop()
    (output / "run.json").write_text(
        receipt.model_copy(update={"files": tuple(files)}).model_dump_json()
    )

    # When opened, then file checksums cannot substitute for complete membership.
    with pytest.raises(EvidenceError, match="artifact_membership"):
        load_run(output)


@pytest.mark.parametrize("mutation", ["spec", "methods", "normalization", "count", "duplicate-hit"])
def test_rehashed_inconsistent_outputs_are_refused(inputs, mutation: str) -> None:
    # Given altered output with freshly recomputed file receipts.
    bundle, pin, spec, output = inputs
    _ = analyze(bundle, pin, spec, output)
    if mutation == "duplicate-hit":
        rows = (output / "hits.jsonl").read_text().splitlines()
        rows[1] = rows[0]
        (output / "hits.jsonl").write_text("\n".join(rows) + "\n")
    else:
        summary = json.loads((output / "summary.json").read_bytes())
        changes = {
            "spec": ("spec_sha256", "0" * 64),
            "methods": ("methods_sha256", "0" * 64),
            "normalization": ("normalization", "different-method"),
            "count": ("total_occurrences", 999),
        }
        field, value = changes[mutation]
        summary[field] = value
        (output / "summary.json").write_text(json.dumps(summary))
    rebind_artifacts(output)

    # When opened, then cross-artifact identities and occurrence membership must agree.
    with pytest.raises(EvidenceError, match="result_membership"):
        load_run(output)


def test_animal_review_counts_primary_and_exploratory_without_promoting_authorship(
    inputs, tmp_path: Path
) -> None:
    # Given a primary bee candidate and an editorial plural-fly candidate.
    bundle, pin, spec, output = inputs
    _ = analyze(bundle, pin, spec, output)
    _receipt, _summary, hits = load_run(output)
    selected = (
        next(hit for hit in hits if hit.term_id == "bee" and hit.blake_primary),
        next(hit for hit in hits if hit.expression == "flies" and not hit.blake_primary),
    )
    run_sha = digest((output / "run.json").read_bytes())
    decisions = tmp_path / "animal-decisions.jsonl"
    decisions.write_text(
        "".join(
            ReviewDecision(
                run_sha256=run_sha,
                hit_id=hit.hit_id,
                decision="animal_literal",
                reviewer="synthetic-control-reviewer",
                rationale="The synthetic context explicitly names the animal.",
                verification_locator=hit.locator,
            ).model_dump_json()
            + "\n"
            for hit in selected
        )
    )

    # When independently bound decisions are admitted.
    summary = review(output, decisions, run_sha)

    # Then review counts remain separated by the inherited source boundary.
    assert (summary.primary_animal_hits, summary.exploratory_animal_hits) == (1, 1)
    assert (summary.reviewed_hits, summary.unreviewed_hits) == (2, 9)
    assert selected[1].text_role == "editorial"


def test_review_requires_the_exact_run_bytes_before_loading_decisions(
    inputs, tmp_path: Path
) -> None:
    # Given a valid run and a deliberately incorrect externally supplied identity.
    bundle, pin, spec, output = inputs
    _ = analyze(bundle, pin, spec, output)
    decisions = tmp_path / "decisions.jsonl"
    decisions.write_text("")

    # When review is attempted, then it cannot silently select another run.
    with pytest.raises(EvidenceError, match="review_run_pin"):
        review(output, decisions, "0" * 64)


@pytest.mark.parametrize("field", ["reviewer", "rationale"])
def test_whitespace_review_credit_or_rationale_is_refused(field: str) -> None:
    # Given a syntactically nonempty but meaningless review field.
    record = {
        "run_sha256": "0" * 64,
        "hit_id": "synthetic-hit",
        "decision": "uncertain",
        "reviewer": "reviewer",
        "rationale": "context undecided",
    }
    record[field] = "   "

    # When parsed, then empty credit cannot masquerade as authored review.
    with pytest.raises(ValueError, match="reviewer_and_rationale_required"):
        ReviewDecision.model_validate(record)


def test_cli_import_uses_real_recovered_sources_and_preserves_a_portable_pin(
    recovered_source: Path, tmp_path: Path
) -> None:
    # Given a real offline recovery and its independently built search projection.
    destination = tmp_path / "imported"
    pin_file = tmp_path / "pins/corpus.json"

    # When the application CLI imports it through the public Blake interface.
    result = CliRunner().invoke(
        main,
        [
            "import-corpus",
            "--source",
            str(recovered_source),
            "--destination",
            str(destination),
            "--pin-output",
            str(pin_file),
        ],
    )

    # Then the portable import and written pin agree with the actual manifest bytes.
    assert result.exit_code == 0, result.output
    pin = CorpusPin.model_validate_json(pin_file.read_bytes())
    assert pin.bundle_manifest_sha256 == digest((destination / "manifest.json").read_bytes())
    assert json.loads(result.output)["bundle_manifest_sha256"] == pin.bundle_manifest_sha256


@pytest.mark.parametrize("existing", ["regular", "dangling-symlink", "ancestor-symlink"])
def test_cli_import_guards_pin_custody_before_export(tmp_path: Path, existing: str) -> None:
    # Given a source root and an occupied or aliased requested pin slot.
    source = tmp_path / "source"
    source.mkdir()
    destination = tmp_path / "imported"
    pin_file = tmp_path / "pin.json"
    if existing == "regular":
        pin_file.write_text("preserve me")
    elif existing == "dangling-symlink":
        pin_file.symlink_to(tmp_path / "absent")
    else:
        target = tmp_path / "target"
        target.mkdir()
        link = tmp_path / "alias"
        link.symlink_to(target, target_is_directory=True)
        pin_file = link / "pin.json"

    # When import is attempted, then it refuses before exporting any corpus bytes.
    result = CliRunner().invoke(
        main,
        [
            "import-corpus",
            "--source",
            str(source),
            "--destination",
            str(destination),
            "--pin-output",
            str(pin_file),
        ],
    )
    assert result.exit_code != 0
    assert "Error:" in result.output
    assert not destination.exists()
    if existing == "regular":
        assert pin_file.read_text() == "preserve me"


def test_cli_import_reports_missing_recovery_without_fabricating_a_pin(tmp_path: Path) -> None:
    # Given an existing directory without captured recovery evidence.
    source = tmp_path / "source"
    source.mkdir()
    destination = tmp_path / "imported"
    pin_file = tmp_path / "pin.json"

    # When import runs, then the real missing-file failure is surfaced.
    result = CliRunner().invoke(
        main,
        [
            "import-corpus",
            "--source",
            str(source),
            "--destination",
            str(destination),
            "--pin-output",
            str(pin_file),
        ],
    )
    assert result.exit_code != 0
    assert "Error:" in result.output
    assert not pin_file.exists()


@pytest.mark.parametrize("root", ["source", "destination"])
def test_cli_pin_cannot_write_into_the_source_or_exported_bundle(tmp_path: Path, root: str) -> None:
    # Given a pin path inside either read-only source custody or the immutable bundle.
    source = tmp_path / "source"
    source.mkdir()
    destination = tmp_path / "imported"
    pin_root = source if root == "source" else destination
    pin_file = pin_root / "pins/corpus.json"

    # When importing, then the pin root is refused before any source or bundle write.
    result = CliRunner().invoke(
        main,
        [
            "import-corpus",
            "--source",
            str(source),
            "--destination",
            str(destination),
            "--pin-output",
            str(pin_file),
        ],
    )
    assert result.exit_code != 0
    assert "overlapping_pin" in result.output
    assert list(source.iterdir()) == []
    assert not destination.exists()


def test_cli_analyze_reports_a_wrong_corpus_identity(inputs, tmp_path: Path) -> None:
    # Given a correctly encoded pin naming a different source index.
    bundle, pin, spec, output = inputs
    pin_file = tmp_path / "pin.json"
    pin_file.write_text(pin.model_copy(update={"index_sha256": "0" * 64}).model_dump_json())
    spec_file = tmp_path / "spec.json"
    spec_file.write_text(spec.model_dump_json())

    # When the real analyze command is invoked, then it fails before output admission.
    result = CliRunner().invoke(
        main,
        [
            "analyze",
            "--bundle",
            str(bundle),
            "--pin",
            str(pin_file),
            "--vocabulary",
            str(spec_file),
            "--output",
            str(output),
        ],
    )
    assert result.exit_code != 0
    assert "corpus_pin_mismatch" in result.output
    assert not output.exists()


def test_cli_verify_reports_corrupt_output(inputs) -> None:
    # Given a valid run whose candidate ledger was subsequently altered.
    bundle, pin, spec, output = inputs
    _ = analyze(bundle, pin, spec, output)
    with (output / "hits.jsonl").open("ab") as handle:
        _ = handle.write(b"corrupt")

    # When verification runs, then the command reports the failed checksum.
    result = CliRunner().invoke(main, ["verify-run", str(output)])
    assert result.exit_code != 0
    assert "artifact_checksum" in result.output


def test_cli_review_writes_a_separate_bound_summary_and_refuses_overwrite(
    inputs, tmp_path: Path
) -> None:
    # Given a complete run and an explicitly empty reviewed subset.
    bundle, pin, spec, output = inputs
    _ = analyze(bundle, pin, spec, output)
    run_sha = digest((output / "run.json").read_bytes())
    decisions = tmp_path / "decisions.jsonl"
    decisions.write_text("")
    review_output = tmp_path / "review.json"
    args = [
        "review",
        "--run",
        str(output),
        "--run-sha256",
        run_sha,
        "--decisions",
        str(decisions),
        "--output",
        str(review_output),
    ]
    runner = CliRunner()

    # When reviewed and repeated, then the first immutable summary survives.
    first = runner.invoke(main, args)
    assert first.exit_code == 0, first.output
    before = review_output.read_bytes()
    second = runner.invoke(main, args)
    assert second.exit_code != 0
    assert review_output.read_bytes() == before
    assert json.loads(before)["unreviewed_hits"] == 11


def test_unedited_csv_queue_preserves_all_candidates_as_unreviewed(inputs, tmp_path: Path) -> None:
    # Given an untouched copy outside the hash-bound run directory.
    bundle, pin, spec, output = inputs
    _ = analyze(bundle, pin, spec, output)
    before = (output / "review-queue.csv").read_bytes()
    edited = tmp_path / "review.csv"
    edited.write_bytes(before)
    run_sha = digest((output / "run.json").read_bytes())

    # When that CSV passes through the same review command contract.
    summary = review(output, edited, run_sha)

    # Then genuinely blank annotations remain unreviewed and original evidence is unchanged.
    assert (summary.reviewed_hits, summary.unreviewed_hits) == (0, 11)
    assert summary.decisions_sha256 == digest(before)
    assert (output / "review-queue.csv").read_bytes() == before


@pytest.mark.parametrize("complete", [False, True])
def test_csv_review_roundtrip_admits_complete_and_partial_annotations(
    inputs, tmp_path: Path, complete: bool
) -> None:
    # Given a copied queue with either two or all eleven explicitly annotated rows.
    bundle, pin, spec, output = inputs
    _ = analyze(bundle, pin, spec, output)
    columns, rows = read_queue(output)
    assert any("\n" in row["context"] and '"' in row["context"] for row in rows)
    assert any("," in row["title"] for row in rows)
    selected = rows if complete else rows[:2]
    for row in selected:
        row.update(decision="uncertain", reviewer="CSV reviewer", rationale="Context unresolved")
    edited = tmp_path / "annotated.csv"
    write_queue(edited, columns, rows)
    run_sha = digest((output / "run.json").read_bytes())
    summary_path = tmp_path / "csv-summary.json"

    # When the real CLI reviews the edited file using the externally supplied run pin.
    result = CliRunner().invoke(
        main,
        [
            "review",
            "--run",
            str(output),
            "--run-sha256",
            run_sha,
            "--decisions",
            str(edited),
            "--output",
            str(summary_path),
        ],
    )

    # Then only annotated rows count as reviewed and the decision source is hash-bound.
    assert result.exit_code == 0, result.output
    summary = json.loads(summary_path.read_bytes())
    expected = 11 if complete else 2
    assert (summary["reviewed_hits"], summary["unreviewed_hits"]) == (expected, 11 - expected)
    assert summary["decisions"]["uncertain"] == expected
    assert summary["decisions_sha256"] == digest(edited.read_bytes())


def test_csv_review_accepts_a_deliberately_selected_subset_with_a_utf8_bom(
    inputs, tmp_path: Path
) -> None:
    # Given one selected row from the exported queue, encoded by a spreadsheet with a BOM.
    bundle, pin, spec, output = inputs
    _ = analyze(bundle, pin, spec, output)
    columns, rows = read_queue(output)
    rows = [next(row for row in rows if row["term_id"] == "bee")]
    rows[0].update(
        decision="animal_literal",
        reviewer="CSV reviewer",
        rationale="Synthetic animal reference",
        verification_locator=rows[0]["locator"],
    )
    edited = tmp_path / "selected.CSV"
    write_queue(edited, columns, rows)
    edited.write_bytes(b"\xef\xbb\xbf" + edited.read_bytes())
    run_sha = digest((output / "run.json").read_bytes())

    # When the selected subset is reviewed.
    summary = review(output, edited, run_sha)

    # Then omitted candidates remain unreviewed, with no inferred negative decisions.
    assert (summary.reviewed_hits, summary.unreviewed_hits) == (1, 10)
    assert summary.primary_animal_hits == 1


@pytest.mark.parametrize(
    "field",
    [
        "hit_id",
        "term_id",
        "source_plane",
        "text_role",
        "passage_id",
        "title",
        "locator",
        "source_url",
        "expression",
        "context",
    ],
)
def test_csv_refuses_every_changed_immutable_field_even_when_unreviewed(
    inputs, tmp_path: Path, field: str
) -> None:
    # Given a queue copy with one altered evidence field and no annotation.
    bundle, pin, spec, output = inputs
    _ = analyze(bundle, pin, spec, output)
    columns, rows = read_queue(output)
    rows[0][field] += "-altered"
    edited = tmp_path / "changed.csv"
    write_queue(edited, columns, rows)
    run_sha = digest((output / "run.json").read_bytes())

    # When reviewed, then blank decisions cannot bypass source identity checks.
    with pytest.raises(EvidenceError, match="csv_candidate_changed|unknown_or_duplicate_hit"):
        review(output, edited, run_sha)


@pytest.mark.parametrize("mutation", ["duplicate", "unknown"])
def test_csv_refuses_duplicate_and_unknown_unreviewed_rows(
    inputs, tmp_path: Path, mutation: str
) -> None:
    # Given an unreviewed queue copy with an ambiguous or unknown candidate identity.
    bundle, pin, spec, output = inputs
    _ = analyze(bundle, pin, spec, output)
    columns, rows = read_queue(output)
    if mutation == "duplicate":
        rows.append(rows[0].copy())
    else:
        rows[0]["hit_id"] = "unknown-candidate"
    edited = tmp_path / "wrong-identity.csv"
    write_queue(edited, columns, rows)
    run_sha = digest((output / "run.json").read_bytes())

    # When reviewed, then identity validation precedes skipping unreviewed rows.
    with pytest.raises(EvidenceError, match="unknown_or_duplicate_hit"):
        review(output, edited, run_sha)


@pytest.mark.parametrize("mutation", ["missing", "extra", "duplicate", "reordered"])
def test_csv_requires_the_exact_exported_header(inputs, tmp_path: Path, mutation: str) -> None:
    # Given a CSV whose columns no longer identify the exported queue schema.
    bundle, pin, spec, output = inputs
    _ = analyze(bundle, pin, spec, output)
    columns, rows = read_queue(output)
    if mutation == "missing":
        columns.pop()
    elif mutation == "extra":
        columns.append("extra")
    elif mutation == "duplicate":
        columns.append(columns[0])
    else:
        columns.reverse()
    edited = tmp_path / "wrong-header.csv"
    write_queue(edited, columns, rows)
    run_sha = digest((output / "run.json").read_bytes())

    # When reviewed, then partial or ambiguous schemas cannot enter the review ledger.
    with pytest.raises(EvidenceError, match="csv_header"):
        review(output, edited, run_sha)


@pytest.mark.parametrize("mutation", ["short", "long"])
def test_csv_requires_each_row_to_match_the_header_width(
    inputs, tmp_path: Path, mutation: str
) -> None:
    # Given an exact header followed by a structurally incomplete or overfull row.
    bundle, pin, spec, output = inputs
    _ = analyze(bundle, pin, spec, output)
    columns, rows = read_queue(output)
    values = [rows[0][column] for column in columns]
    values = values[:-1] if mutation == "short" else [*values, "unexpected"]
    edited = tmp_path / "wrong-width.csv"
    with edited.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        writer.writerow(values)
    run_sha = digest((output / "run.json").read_bytes())

    # When reviewed, then DictReader's missing/extra-column placeholders are rejected.
    with pytest.raises(EvidenceError, match="csv_row_width"):
        review(output, edited, run_sha)


@pytest.mark.parametrize("field", ["reviewer", "rationale", "verification_locator"])
def test_csv_refuses_partial_annotations_without_a_decision(
    inputs, tmp_path: Path, field: str
) -> None:
    # Given a reviewer entry without an explicit contextual classification.
    bundle, pin, spec, output = inputs
    _ = analyze(bundle, pin, spec, output)
    columns, rows = read_queue(output)
    rows[0][field] = "partially completed"
    edited = tmp_path / "partial.csv"
    write_queue(edited, columns, rows)
    run_sha = digest((output / "run.json").read_bytes())

    # When reviewed, then partial annotation is not silently discarded as unreviewed.
    with pytest.raises(EvidenceError, match="partial_csv_annotation"):
        review(output, edited, run_sha)


def test_csv_animal_annotation_still_requires_a_verification_locator(
    inputs, tmp_path: Path
) -> None:
    # Given an otherwise complete animal decision without its required locator.
    bundle, pin, spec, output = inputs
    _ = analyze(bundle, pin, spec, output)
    columns, rows = read_queue(output)
    rows[0].update(decision="animal_figurative", reviewer="reviewer", rationale="Animal metaphor")
    edited = tmp_path / "missing-locator.csv"
    write_queue(edited, columns, rows)
    run_sha = digest((output / "run.json").read_bytes())

    # When parsed from CSV, then the existing contextual-review boundary still applies.
    with pytest.raises(ValueError, match="animal_locator_required"):
        review(output, edited, run_sha)


@pytest.mark.parametrize("field", ["decision", "reviewer", "rationale"])
def test_csv_annotation_uses_the_existing_decision_validation(
    inputs, tmp_path: Path, field: str
) -> None:
    # Given a completed annotation with one invalid decision or missing required field.
    bundle, pin, spec, output = inputs
    _ = analyze(bundle, pin, spec, output)
    columns, rows = read_queue(output)
    rows[0].update(decision="uncertain", reviewer="reviewer", rationale="Context undecided")
    rows[0][field] = "not-a-decision" if field == "decision" else ""
    edited = tmp_path / "invalid-annotation.csv"
    write_queue(edited, columns, rows)
    run_sha = digest((output / "run.json").read_bytes())

    # When parsed from CSV, then the shared review contract rejects the invalid annotation.
    with pytest.raises(ValueError):
        review(output, edited, run_sha)


def test_csv_parser_reports_malformed_quoted_input(inputs, tmp_path: Path) -> None:
    # Given a valid schema followed by an unterminated quoted cell.
    bundle, pin, spec, output = inputs
    _ = analyze(bundle, pin, spec, output)
    columns, _rows = read_queue(output)
    edited = tmp_path / "malformed.csv"
    with edited.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        _ = handle.write('"unterminated')
    run_sha = digest((output / "run.json").read_bytes())

    # When reviewed, then malformed quoting is surfaced as a CSV boundary error.
    with pytest.raises(EvidenceError, match="csv_format"):
        review(output, edited, run_sha)


def test_editing_the_original_queue_invalidates_the_run_before_csv_review(
    inputs, tmp_path: Path
) -> None:
    # Given annotation performed inside the immutable original output directory.
    bundle, pin, spec, output = inputs
    _ = analyze(bundle, pin, spec, output)
    run_sha = digest((output / "run.json").read_bytes())
    columns, rows = read_queue(output)
    rows[0].update(decision="uncertain", reviewer="reviewer", rationale="Needs context")
    write_queue(output / "review-queue.csv", columns, rows)

    # When reviewed, then original artifact checks fail before parsing any decisions.
    with pytest.raises(EvidenceError, match="artifact_checksum"):
        review(output, output / "review-queue.csv", run_sha)
