"""Project admission and staging for the real docxology/template writers."""

import configparser
import csv
import hashlib
import json
import re
from pathlib import Path
from typing import ClassVar

from blake.methods.runs import reserve
from pydantic import BaseModel, ConfigDict

from . import __version__
from .publication_contract import NativeRequest, NativeStage
from .publication_custody import checked_member, output_member, template_sources
from .publication_data import load_abstract_data, pinned_bytes
from .publication_frontmatter import frontmatter_markdown, publish_frontmatter
from .publication_wire import Member, PublicationError
from .workflows import require_private_output


class PreparedArticle(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)
    atlas_sha256: str
    casebook_sha256: str
    manuscript_sha256: str
    bibliography_sha256: str
    files: tuple[Member, ...]


def prepare_native_stage(request: NativeRequest, output: Path, template: Path) -> NativeStage:
    """Admit current source and prior exact data before reserving a new stage."""
    root = Path.cwd()
    require_private_output(output, request.prepared.path)
    raw = pinned_bytes(request.prepared)
    prepared = PreparedArticle.model_validate_json(raw)
    directory = request.prepared.path.parent
    for item in prepared.files:
        checked_member(directory, item)
    payloads = {item.path: (directory / item.path).read_bytes() for item in prepared.files}
    template_map = template_sources(template, request.template_commit)
    current = root / "docs/manuscript"
    if (
        prepared.atlas_sha256 != request.atlas.sha256
        or prepared.casebook_sha256 != request.casebook.sha256
        or prepared.manuscript_sha256
        != hashlib.sha256((current / "blakean-entomology.md").read_bytes()).hexdigest()
        or prepared.bibliography_sha256
        != hashlib.sha256((current / "references.bib").read_bytes()).hexdigest()
    ):
        raise PublicationError("prepared_source_binding", str(directory))
    config = pinned_bytes(request.config)
    preamble = pinned_bytes(request.preamble)
    stylesheet = pinned_bytes(request.web_css)
    data = load_abstract_data(request)
    font = template / "infrastructure/rendering/assets/fonts/liberation/LiberationSans-Regular.ttf"
    if not font.is_file() or font.is_symlink():
        raise PublicationError("template_font", str(font))
    reserve(output)
    manuscripts = output / "manuscript"
    figures = output / "output/figures"
    manuscripts.mkdir()
    figures.mkdir(parents=True)
    web = output / "output/web"
    web.mkdir()
    _ = (web / "web.css").write_bytes(stylesheet)
    for name, payload in payloads.items():
        if name.startswith("assets/"):
            _ = (figures / Path(name).name).write_bytes(payload)
    data_sha = publish_frontmatter(data, figures, (request.cover.path, font))
    body = payloads["blakean-entomology.md"].decode().replace("(assets/", "(../figures/")
    _ = (manuscripts / "10_article.md").write_text(body)
    frontmatter = frontmatter_markdown(data)
    _ = (manuscripts / "00_frontmatter.md").write_text(frontmatter)
    _ = (manuscripts / "references.bib").write_bytes(payloads["references.bib"])
    _ = (manuscripts / "config.yaml").write_bytes(config)
    _ = (manuscripts / "preamble.md").write_bytes(preamble)
    title = re.search(r'^title:\s*"([^"]+)"\s*$', body, re.MULTILINE)
    if title is None:
        raise PublicationError("paper_title", "Require the authored quoted YAML title")
    variables = {
        "PAPER_TITLE": title.group(1).split(": ", 1)[0],
        "PAPER_SUBTITLE": title.group(1).partition(": ")[2],
        "PAPER_VERSION": __version__,
    }
    with (output / "manuscript_variables.csv").open("x", newline="") as stream:
        csv.writer(stream).writerows(variables.items())
    registry: list[dict[str, str]] = []
    for match in re.finditer(
        r"!\[((?:[^\[\]]|\[[^\[\]]*\])*)\]\(([^)]+)\)\{#(fig:[\w-]+)[^}]*\}",
        frontmatter + "\n" + body,
    ):
        registry.append(
            {"label": match.group(3), "filename": Path(match.group(2)).name, "alt": match.group(1)}
        )
    _ = (figures / "figure_registry.json").write_text(
        json.dumps({"figures": registry}, indent=2) + "\n"
    )
    sources = tuple(
        output_member(p, root)
        for base in (root / "src", root / "tools")
        for p in sorted(base.rglob("*.py"))
    )
    canonical_request = request.model_dump_json().encode()
    _ = (output / "native-request.json").write_bytes(canonical_request)
    inputs = tuple(
        output_member(p, output)
        for base in (manuscripts, figures)
        for p in sorted(base.iterdir())
        if p.is_file()
    ) + (
        output_member(output / "manuscript_variables.csv", output),
        output_member(output / "native-request.json", output),
        output_member(web / "web.css", output),
    )
    record = NativeStage(
        request_sha256=hashlib.sha256(canonical_request).hexdigest(),
        template_sources=template_map,
        source_order=("00_frontmatter.md", "10_article.md"),
        inputs=inputs,
        sources=sources,
        frontmatter_data_sha256=data_sha,
    )
    _ = (output / "native-stage.json").write_text(record.model_dump_json(indent=2) + "\n")
    with (output / "native-wire.csv").open("x", newline="") as stream:
        writer = csv.writer(stream)
        for role, records in (("input", inputs), ("source", sources)):
            for entry in records:
                writer.writerow((role, entry.path, entry.size, entry.sha256))
        for name, sha in template_map.items():
            writer.writerow(("template", name, (template / name).stat().st_size, sha))
    transport = configparser.ConfigParser(interpolation=None)
    transport["native"] = {
        "template_commit": request.template_commit,
        "sdk_commit": request.sdk_commit,
        "source_date_epoch": str(record.source_date_epoch),
        "source_order": ",".join(record.source_order),
        "wire_sha256": hashlib.sha256((output / "native-wire.csv").read_bytes()).hexdigest(),
        "stage_sha256": hashlib.sha256((output / "native-stage.json").read_bytes()).hexdigest(),
    }
    with (output / "native-transport.ini").open("x") as stream:
        transport.write(stream)
    # Re-admit every caller-held source, including the original museum recto.
    for item in (
        request.prepared,
        request.atlas,
        request.composition,
        request.casebook,
        request.cover,
        request.cover_provenance,
        request.config,
        request.preamble,
        request.web_css,
    ):
        _ = pinned_bytes(item)
    return record
