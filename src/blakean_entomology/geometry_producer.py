"""Bind the actual domain geometry and shared arithmetic source closure."""

from blake.methods.producer import SourceBinding, source_hashes

from .producer import APPLICATION_SOURCES, SHARED_SOURCES

GEOMETRY_SOURCES = (
    "composition.py",
    "geometry_models.py",
    "geometry_inputs.py",
    "geometry.py",
    "geometry_io.py",
    "geometry_run.py",
    "geometry_producer.py",
    "geometry_cli.py",
)


def geometry_producers(*, figures: bool) -> dict[str, str]:
    """Optional figure source enters only the producer that actually uses it."""
    drawing = (
        ("geometry_figures.py", "geometry_review_figure.py", "geometry_plotting.py")
        if figures
        else ()
    )
    return source_hashes(
        (
            SourceBinding("blakean_entomology", APPLICATION_SOURCES + GEOMETRY_SOURCES + drawing),
            SourceBinding(
                "blake",
                SHARED_SOURCES
                + (
                    "methods/composition.py",
                    "methods/installed.py",
                    "methods/installed_models.py",
                    "methods/installed_records.py",
                ),
            ),
        )
    )
