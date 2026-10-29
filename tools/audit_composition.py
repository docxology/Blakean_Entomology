# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
# Run with existing project dependencies (no sync):
# uv run --no-sync python tools/audit_composition.py --help
"""Portable CLI for a fresh source-bound composition epoch; no installs or downloads."""

import sys

from blakean_entomology.cli import main

if __name__ == "__main__":
    main(["composition-audit", *sys.argv[1:]])
