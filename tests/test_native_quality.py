"""Fail-capable parsing of the rendered PDF's semantic metadata."""

import pytest

from blakean_entomology.publication_quality import PDFMetadata, parse_pdfinfo, require_title
from blakean_entomology.publication_wire import PublicationError


def test_actual_metadata_fields_are_parsed() -> None:
    # Given Poppler's line-oriented semantic fields.
    raw = "Title: Fixture\nPages: 4\nPage size: 612 x 792 pts\n"
    # When the boundary parses it.
    observed = parse_pdfinfo(raw)
    # Then only the required typed values are admitted.
    assert observed == PDFMetadata(title="Fixture", pages=4)


@pytest.mark.parametrize(
    "raw",
    (
        "Pages: 4\n",
        "Title: Fixture\n",
        "Title: Fixture\nPages: zero\n",
        "Title: Fixture\nPages: 0\n",
    ),
)
def test_missing_or_malformed_metadata_is_refused(raw) -> None:
    # Given absent or malformed actual-output fields.
    # When the metadata boundary parses them.
    with pytest.raises(PublicationError):
        _ = parse_pdfinfo(raw)
    # Then no implicit title or page-count fallback is produced.


def test_placeholder_title_does_not_match_admitted_title() -> None:
    # Given the concrete failure reproduced by native03.
    observed = PDFMetadata(title="{{PAPER_TITLE}}", pages=40)
    # When compared with the admitted resolved title.
    with pytest.raises(PublicationError):
        require_title(observed, "Fixture")
    # Then available variable keys cannot stand in for resolved output bytes.


def test_resolved_title_is_admitted() -> None:
    # Given exact semantic output metadata.
    observed = PDFMetadata(title="Fixture", pages=4)
    # When checked against the same admitted title.
    require_title(observed, "Fixture")
    # Then the actual equality contract passes.
