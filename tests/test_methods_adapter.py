"""Source closure changes must create a new application producer identity."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import blake

import blakean_entomology


def test_delegated_source_changes_producer(tmp_path: Path) -> None:
    # Given independent real source copies, preserving every live source byte.
    public = tmp_path / "public"
    private = tmp_path / "private"
    shutil.copytree(
        Path(blake.__file__).parent, public / "blake", ignore=shutil.ignore_patterns("__pycache__")
    )
    shutil.copytree(
        Path(blakean_entomology.__file__).parent,
        private / "blakean_entomology",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    environment = {**os.environ, "PYTHONPATH": os.pathsep.join((str(public), str(private)))}
    command = [
        sys.executable,
        "-c",
        "from blakean_entomology.core import application_code_sha256; "
        "print(application_code_sha256())",
    ]
    before = subprocess.run(command, env=environment, check=True, capture_output=True, text=True)
    delegated = public / "blake/methods/annotations.py"
    delegated.write_text(delegated.read_text() + "\n# Synthetic producer sensitivity control.\n")
    # When delegated code bytes change in the independent copy.
    after = subprocess.run(command, env=environment, check=True, capture_output=True, text=True)
    # Then the new producer receipt cannot claim the earlier closure identity.
    assert before.stdout.strip() != after.stdout.strip()
    assert len(after.stdout.strip()) == 64
