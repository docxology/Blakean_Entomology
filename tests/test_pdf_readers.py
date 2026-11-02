"""Exercise the actual Poppler metadata/text boundary on real PDF bytes."""

import pytest
from PIL import Image

from blakean_entomology.publication_quality import inspect_pdf
from blakean_entomology.publication_transport_models import PublicationError


def fixture_pdf(path) -> None:
    with Image.new("RGB", (40, 60), "white") as image:
        image.save(path, "PDF", title="An actual fixture")


def test_actual_pdf_metadata_and_text_readers(tmp_path) -> None:
    pdf = tmp_path / "fixture.pdf"
    fixture_pdf(pdf)
    receipt = tmp_path / "inspection"
    result = inspect_pdf(pdf, "An actual fixture", receipt)
    assert result.title == "An actual fixture"
    assert result.pages == 1
    assert (receipt / "pdfinfo.txt").stat().st_size > 0
    assert (receipt / "pdftext.txt").is_file()


def test_actual_pdf_title_refusal_retains_reader_evidence(tmp_path) -> None:
    pdf = tmp_path / "fixture.pdf"
    fixture_pdf(pdf)
    receipt = tmp_path / "inspection"
    with pytest.raises(PublicationError, match="pdf_title"):
        inspect_pdf(pdf, "Wrong title", receipt)
    assert (receipt / "pdfinfo.txt").is_file()
    assert (receipt / "pdftext.txt").is_file()


def test_actual_reader_rejects_a_corrupt_pdf(tmp_path) -> None:
    pdf = tmp_path / "invalid.pdf"
    pdf.write_bytes(b"not a PDF")
    receipt = tmp_path / "inspection"
    with pytest.raises(PublicationError, match="native_output_reader"):
        inspect_pdf(pdf, "No substituted title", receipt)
    assert (receipt / "pdfinfo.txt.stderr").read_bytes()
