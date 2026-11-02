"""Immutable SDK selections for readable historical and current native records."""

from typing import Final

TEMPLATE_COMMIT: Final = "efce6d6f5b3c4e8e2bbf92d8250855a0a9389ae8"
SDK_COMMIT: Final = "45171a099a6a658c52ab689501de646a28485653"
SCHEMA2_SDK_COMMIT: Final = "d34876e021a8f2e654b96f1c23f7ec43d8d958c2"
CURRENT_SDK_COMMIT: Final = "263d7c83abe6f1309a64af3285a683c1b7672269"
CURRENT_SCHEMA: Final = 3


def sdk_version(schema: int, commit: str) -> str | None:
    """Require an exact schema/pin pair; booleans and future schemas are refused."""
    if type(schema) is not int:
        return None
    return {
        (1, SDK_COMMIT): "0.5.0",
        (2, SCHEMA2_SDK_COMMIT): "0.6.0",
        (3, CURRENT_SDK_COMMIT): "0.7.0",
    }.get((schema, commit))


def sdk_profile(schema: int, commit: str) -> bool:
    """Historical bytes stay readable; new staging has one current profile."""
    return sdk_version(schema, commit) is not None
