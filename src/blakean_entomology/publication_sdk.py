"""Application policy over Blake's reusable installed Git provenance verifier."""

from blake.methods.common import EvidenceError
from blake.methods.installed import InstalledGitPackage, verify_installed_git

from .publication_contract import NativeRequest
from .publication_transport_models import PublicationError


def admit_native_sdk(request: NativeRequest) -> InstalledGitPackage:
    """Refuse historical production and actual/declared SDK drift before writes."""
    if request.schema_version != 2:
        raise PublicationError(
            "native_historical_profile",
            "Retain the original producer; create a schema-2 request for new staging",
        )
    try:
        return verify_installed_git("blake", request.sdk_commit)
    except EvidenceError as error:
        raise PublicationError("native_sdk_" + error.code, error.detail) from error
