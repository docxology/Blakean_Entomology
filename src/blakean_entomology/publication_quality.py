"""Actual PDF metadata and extracted-text admission for native publication."""

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .publication_transport_models import PublicationError


@dataclass(frozen=True, slots=True)
class PDFMetadata:
    title: str
    pages: int


def parse_pdfinfo(text: str) -> PDFMetadata:
    """Parse required semantic fields from actual Poppler output."""
    fields: dict[str, str] = {}
    for line in text.splitlines():
        key, separator, value = line.partition(":")
        if separator:
            fields[key.strip()] = value.strip()
    title = fields.get("Title", "")
    pages = fields.get("Pages", "")
    if not title or not pages.isdecimal() or int(pages) < 1:
        raise PublicationError("pdf_metadata_fields", "Require title and a positive page count")
    return PDFMetadata(title=title, pages=int(pages))


def require_title(metadata: PDFMetadata, expected: str) -> None:
    """A rendered title must equal the admitted resolved title."""
    if metadata.title != expected:
        raise PublicationError("pdf_title", f"Expected {expected!r}, observed {metadata.title!r}")


def inspect_pdf(pdf: Path, expected: str, output: Path) -> PDFMetadata:
    """Run actual metadata/text readers and retain raw outputs before admission."""
    output.mkdir()
    commands = (
        ("pdfinfo.txt", "pdfinfo", (str(pdf),)),
        ("pdftext.txt", "pdftotext", ("-layout", str(pdf), "-")),
    )
    for name, tool, arguments in commands:
        executable = shutil.which(tool)
        if executable is None:
            raise PublicationError("native_output_tool", tool)
        result = subprocess.run(
            [executable, *arguments],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            check=False,
        )
        with (output / name).open("xb") as stream:
            _ = stream.write(result.stdout)
        with (output / (name + ".stderr")).open("xb") as stream:
            _ = stream.write(result.stderr)
        if result.returncode:
            raise PublicationError("native_output_reader", result.stderr.decode(errors="replace"))
    metadata = parse_pdfinfo((output / "pdfinfo.txt").read_text())
    require_title(metadata, expected)
    return metadata
