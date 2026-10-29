"""Explicit source closure for the shared-method application epoch."""

from typing import Final

from blake.methods.producer import SourceBinding, source_binding_sha256

APPLICATION_SOURCES: Final = (
    "__init__.py",
    "core.py",
    "models.py",
    "cli.py",
    "producer.py",
    "sensitivity.py",
    "workflows.py",
    "taxonomy_models.py",
    "taxonomy.py",
    "atlas_models.py",
    "atlas.py",
    "casebook.py",
)
SHARED_SOURCES: Final = (
    "__init__.py",
    "version.py",
    "studies.py",
    "applications.py",
    "text_search/__init__.py",
    "text_search/models.py",
    "text_search/normalize.py",
    "text_search/index.py",
    "text_search/vocabulary.py",
    "methods/__init__.py",
    "methods/annotations.py",
    "methods/runs.py",
    "methods/producer.py",
    "methods/storage.py",
    "methods/models.py",
    "methods/hierarchy.py",
    "methods/common.py",
    "methods/bundle_models.py",
    "methods/projection_models.py",
    "methods/profiles.py",
    "methods/statistics.py",
    "methods/statistics_core.py",
    "methods/statistics_models.py",
    "methods/proximity.py",
    "methods/search.py",
    "methods/search_models.py",
    "methods/compatibility.py",
    "methods/concordance.py",
    "methods/corpus.py",
    "methods/workspace.py",
    "methods/resources/corpus-search.html",
    "methods/resources/corpus-search.css",
    "methods/resources/corpus-search.js",
)


def application_code_sha256() -> str:
    """Bind application policy, delegated methods and offline workspace resources."""
    return source_binding_sha256(
        (
            SourceBinding("blakean_entomology", APPLICATION_SOURCES),
            SourceBinding("blake", SHARED_SOURCES),
        )
    )
