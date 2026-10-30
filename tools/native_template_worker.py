# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
# ─── How to run ───
# Called by render_manuscript.py with the explicitly selected compatible
# template environment, pinned template source and fresh admitted stage.
# ──────────────────
"""Run the actual pinned template hydration, preflight, PDF and web writers."""

import dataclasses
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

# Only the project contracts are shared with this separately selected runtime.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from blakean_entomology.publication_custody import (
    checked_member,
    file_hash,
    output_member,
    template_sources,
)
from blakean_entomology.publication_quality import inspect_pdf
from blakean_entomology.publication_wire import PublicationError, read_transport


def main() -> None:
    """Stdlib-only native bridge; the selected closed template runtime has no Pydantic."""
    if len(sys.argv) not in (4, 5):
        raise PublicationError(
            "native_arguments", "TEMPLATE_ROOT STAGE TRANSPORT_SHA [--preflight-only]"
        )
    if len(sys.argv) == 5 and sys.argv[4] != "--preflight-only":
        raise PublicationError("native_arguments", sys.argv[4])
    template_root = Path(sys.argv[1])
    stage = Path(sys.argv[2])
    preflight_only = "--preflight-only" in sys.argv[4:]
    plan = read_transport(stage, sys.argv[3])
    stage = stage.resolve()
    template_root = template_root.resolve()
    project = Path(__file__).resolve().parents[1]
    for value in (sys.prefix, sys.base_prefix):
        if Path(value).resolve().stat().st_dev != stage.stat().st_dev:
            raise PublicationError("native_runtime_storage", value)
    if tuple(map(int, platform.python_version_tuple()[:2])) < (3, 14):
        raise PublicationError("native_runtime_version", sys.version)
    before = template_sources(template_root, plan.template_commit)
    if before != plan.template_sources:
        raise PublicationError("template_stage_binding", str(template_root))
    for record in plan.inputs:
        checked_member(stage, record)
    for record in plan.sources:
        checked_member(project, record)
    os.environ.update(
        SOURCE_DATE_EPOCH=str(plan.source_date_epoch), FORCE_SOURCE_DATE="1", TZ="UTC"
    )
    for key in ("TEXMFVAR", "TEXMFCONFIG", "TEXMFCACHE", "TEXMFOUTPUT"):
        path = stage / "runtime" / key.lower()
        path.mkdir(parents=True, exist_ok=True)
        os.environ[key] = str(path)
    sys.path.insert(0, str(template_root))
    import infrastructure.rendering
    from infrastructure.core.files.secure_write import atomic_write_text_confined
    from infrastructure.rendering import RenderingConfig
    from infrastructure.rendering._manuscript_source import verify_config_tokens_resolved
    from infrastructure.rendering._pandoc_filters import formalism_filter_args
    from infrastructure.rendering.manuscript_injection import (
        substitute_manuscript_text,
        write_resolved_manuscript_tree,
    )
    from infrastructure.rendering.pdf_renderer import PDFRenderer
    from infrastructure.validation.content.prerender import prevalidate_for_render
    from native_web import EntomologyWebRenderer

    origin = infrastructure.rendering.__file__
    if not Path(origin).resolve().is_relative_to(template_root):
        raise PublicationError("template_import_origin", str(origin))
    variables = plan.variables
    for source in (stage / "manuscript").iterdir():
        if source.suffix in (".md", ".yaml"):
            _, missing = substitute_manuscript_text(source.read_text(), variables)
            if missing:
                raise PublicationError("native_token", ", ".join(missing))
    manuscript = write_resolved_manuscript_tree(stage, variables)
    resolved_config = manuscript / "config.yaml"
    hydrated_config, missing = substitute_manuscript_text(resolved_config.read_text(), variables)
    if missing:
        raise PublicationError("native_config_token", ", ".join(missing))
    atomic_write_text_confined(manuscript, resolved_config, hydrated_config)
    verify_config_tokens_resolved(resolved_config)
    for resolved in manuscript.iterdir():
        if resolved.suffix in (".md", ".yaml"):
            _, remaining = substitute_manuscript_text(resolved.read_text(), {})
            if remaining:
                raise PublicationError("native_resolved_token", ", ".join(remaining))
    sources = [manuscript / name for name in plan.source_order]
    prevalidate_for_render(sources, repo_root=stage, bib_file=manuscript / "references.bib")
    pandoc, crossref = shutil.which("pandoc"), shutil.which("pandoc-crossref")
    if pandoc is None or crossref is None:
        raise PublicationError("native_crossref", "Require actual Pandoc and pandoc-crossref")
    semantic = subprocess.run(
        [
            pandoc,
            *map(str, sources),
            "--from=markdown",
            "--to=html",
            *formalism_filter_args(),
            "--filter",
            crossref,
            "--citeproc",
            "--bibliography",
            str(manuscript / "references.bib"),
            "--output",
            str(stage / "semantic-preflight.html"),
        ],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        check=False,
    )
    _ = (stage / "semantic-preflight.stdout").write_bytes(semantic.stdout)
    _ = (stage / "semantic-preflight.stderr").write_bytes(semantic.stderr)
    if semantic.returncode != 0 or semantic.stderr.strip():
        raise PublicationError("native_semantics", semantic.stderr.decode(errors="replace"))
    if preflight_only:
        print("Actual template validation and native filter preflight passed")
        return
    config = RenderingConfig(
        manuscript_dir=str(manuscript),
        figures_dir=str(stage / "output/figures"),
        output_dir=str(stage / "output"),
        pdf_dir=str(stage / "output/pdf"),
        web_dir=str(stage / "output/web"),
        enable_slides=False,
    )
    pdf = PDFRenderer(config).render_combined(
        sources, manuscript, project_name="blakean_entomology"
    )
    html = EntomologyWebRenderer(config).render_combined(
        sources, manuscript, project_name="blakean_entomology"
    )
    checks = stage / "output-checks"
    observed = inspect_pdf(pdf, variables["PAPER_TITLE"], checks)
    for name, text in (
        ("PDF metadata", (checks / "pdfinfo.txt").read_text()),
        ("PDF text", (checks / "pdftext.txt").read_text()),
        ("HTML", html.read_text()),
    ):
        _, remaining = substitute_manuscript_text(text, {})
        if remaining:
            raise PublicationError("native_output_token", name + ": " + ", ".join(remaining))
    with (checks / "validation.json").open("x") as stream:
        _ = stream.write(
            json.dumps(
                {
                    "title": observed.title,
                    "pages": observed.pages,
                    "resolved_input_and_output_tokens": True,
                },
                indent=2,
            )
            + "\n"
        )
    if template_sources(template_root, plan.template_commit) != before:
        raise PublicationError("template_source_changed", str(template_root))
    for record in plan.sources:
        checked_member(project, record)
    for record in plan.inputs:
        checked_member(stage, record)
    imported = {
        name: file_hash(Path(module.__file__))
        for name, module in sys.modules.items()
        if name.startswith("infrastructure.")
        and module.__file__ is not None
        and Path(module.__file__).is_file()
        and Path(module.__file__).resolve().is_relative_to(template_root)
    }
    receipt = {
        "template_commit": plan.template_commit,
        "template_sources": before,
        "imported_template_sources": imported,
        "template_sources_unchanged": True,
        "runtime_prefix": sys.prefix,
        "runtime_base_prefix": sys.base_prefix,
        "runtime_version": sys.version,
        "writer_calls": [
            "PDFRenderer.render_combined",
            "EntomologyWebRenderer.render_combined (native base with admitted CSS hook)",
        ],
        "semantic_preflight": "template prevalidate_for_render + real formalism/crossref/citeproc",
        "resolved_inputs": [
            dataclasses.asdict(output_member(p, stage))
            for p in sorted(manuscript.iterdir())
            if p.is_file()
        ],
        "output_checks": [
            dataclasses.asdict(output_member(path, stage))
            for path in sorted(checks.iterdir())
            if path.is_file()
        ],
        "outputs": [
            dataclasses.asdict(output_member(p, stage))
            for base in (pdf.parent, html.parent)
            for p in sorted(base.rglob("*"))
            if p.is_file()
        ],
        "pdf": pdf.relative_to(stage).as_posix(),
        "html": html.relative_to(stage).as_posix(),
        "qualification": "actual template writers; physical-page acceptance is separate",
    }
    with (stage / "native-render-receipt.json").open("x") as stream:
        _ = stream.write(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"pdf": str(pdf), "html": str(html), "template_commit": plan.template_commit}))


if __name__ == "__main__":
    main()
