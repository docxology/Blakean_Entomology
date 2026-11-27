"""Stage an admitted published edition for a standalone Template reader build."""

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
from typing import TypedDict, cast
from zipfile import ZipFile

IMAGE = re.compile(
    r"^!\[(?P<alt>.+)\]\(\.\./figures/(?P<file>[^/)]+)\)\{#(?P<label>fig:[^ }]+)", re.M
)
NUMBER = re.compile(
    r"(?<![A-Za-z0-9_@.-])-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?%?(?!(?:[A-Za-z0-9_-]|\.\d))"
)


class Asset(TypedDict):
    sha256: str
    bytes: int


class Release(TypedDict):
    release_tag: str
    assets: dict[str, Asset]


class Cover(TypedDict):
    image: str


class Paper(TypedDict):
    title: str
    subtitle: str
    version: str
    cover: Cover


class Configuration(TypedDict):
    paper: Paper


class Arguments(argparse.Namespace):
    archive: Path = Path()
    archive_sha256: str = ""


def stage(root: Path, archive: Path, digest: str) -> None:
    """Check the public ZIP and stage only the paper inputs in a fresh output tree."""
    release = cast(Release, json.loads((root / "research/publication-20261103.json").read_bytes()))
    filename = "Blakean_Entomology-1.0.0-rendering-inputs.zip"
    record = release["assets"][filename]
    with archive.open("rb") as stream:
        actual = hashlib.file_digest(stream, "sha256").hexdigest()
    if actual != digest or actual != record["sha256"] or archive.stat().st_size != record["bytes"]:
        raise ValueError("Archive does not match the caller pin and public release receipt")

    output = root / "output"
    if output.exists():
        raise FileExistsError(output)
    with ZipFile(archive) as package:
        manifest_name = "BUNDLE-MANIFEST.json"
        manifest = cast("dict[str, str]", json.loads(package.read(manifest_name)))
        if sorted(package.namelist()) != sorted([*manifest, manifest_name]):
            raise ValueError("ZIP members differ from manifest")
        for member, expected in manifest.items():
            if hashlib.sha256(package.read(member)).hexdigest() != expected:
                raise ValueError(f"ZIP member differs from manifest: {member}")

        manuscript = output / "manuscript"
        figures = output / "figures"
        data = output / "data"
        manuscript.mkdir(parents=True)
        figures.mkdir()
        data.mkdir()
        parts = ("00_frontmatter.md", "10_article.md", "preamble.md", "references.bib")
        for name in parts:
            _ = (manuscript / name).write_bytes(package.read(f"paper/manuscript/{name}"))

        config = cast(Configuration, json.loads(package.read("paper/manuscript/config.yaml")))
        config["paper"].update(
            title="Blakean Entomology",
            subtitle="Small Lives, Uncertain Bodies, and the Work of Attention",
            version=release["release_tag"].removeprefix("v"),
        )
        _ = (manuscript / "config.yaml").write_text(
            "# Generated manuscript ordering\n" + json.dumps(config, indent=2) + "\n",
            encoding="utf-8",
        )

        registry: list[dict[str, str]] = []
        for name in parts[:2]:
            text = (manuscript / name).read_text(encoding="utf-8")
            for match in IMAGE.finditer(text):
                image = match["file"]
                _ = (figures / image).write_bytes(package.read(f"paper/output/figures/{image}"))
                registry.append(
                    {"label": match["label"], "filename": image, "alt_text": match["alt"]}
                )
        cover = Path(config["paper"]["cover"]["image"]).name
        _ = (figures / cover).write_bytes(package.read(f"paper/output/figures/{cover}"))
        _ = (figures / "figure_registry.json").write_text(
            json.dumps({"schema_version": 1, "figures": registry}, indent=2) + "\n",
            encoding="utf-8",
        )

    # The retained values are evidence for publication parity, not regenerated results.
    with (data / "retained-reader-values.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(("value", "source"))
        for name in parts[:2]:
            text = (manuscript / name).read_text(encoding="utf-8")
            values = sorted({match[0] for match in NUMBER.finditer(text)})
            writer.writerows((value, name) for value in values)
    print(f"Verified {len(manifest)} bundle members.")
    print(f"Staged {len(registry)} figures plus the cover.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--archive", type=Path, required=True)
    _ = parser.add_argument("--archive-sha256", required=True)
    args = parser.parse_args(namespace=Arguments())
    stage(Path(__file__).resolve().parents[1], args.archive, args.archive_sha256)
