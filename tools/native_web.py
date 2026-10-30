# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
# Called by the pinned native worker in the selected template environment.
"""Source-owned CSS extension of the pinned actual template web writer."""

from pathlib import Path
from typing import override

from infrastructure.rendering._web_assets import embed_css
from infrastructure.rendering.web_renderer import WebRenderer

from blakean_entomology.publication_wire import PublicationError


class EntomologyWebRenderer(WebRenderer):
    """Keep the full native pipeline and add the admitted domain stylesheet."""

    @staticmethod
    @override
    def _embed_css(html_file: Path) -> None:
        stylesheet = html_file.parent / "web.css"
        if stylesheet.is_symlink() or not stylesheet.is_file():
            raise PublicationError("native_web_stylesheet", str(stylesheet))
        WebRenderer._embed_css(html_file)
        embed_css(html_file, stylesheet)
        if stylesheet.read_text() not in html_file.read_text():
            raise PublicationError("native_web_style_projection", str(html_file))
