"""Pinned native source and relative artifact admission; no rendering engines."""

import hashlib
import shutil
import subprocess
from pathlib import Path

from .publication_wire import Member, PublicationError


def file_hash(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def checked_member(root: Path, record: Member) -> None:
    path = root / record.path
    if (
        path.is_symlink()
        or not path.is_file()
        or not path.resolve().is_relative_to(root.resolve())
        or path.stat().st_size != record.size
        or file_hash(path) != record.sha256
    ):
        raise PublicationError("native_input_pin", str(path))


def git_read(template: Path, arguments: tuple[str, ...]) -> bytes:
    git = shutil.which("git")
    if git is None:
        raise PublicationError("native_git", "Git is required for pinned-source admission")
    return subprocess.check_output(
        [git, "-c", "core.fsmonitor=false", "-C", str(template), *arguments],
        stdin=subprocess.DEVNULL,
    )


def template_sources(template: Path, expected: str) -> dict[str, str]:
    if git_read(template, ("rev-parse", "HEAD")).decode().strip() != expected:
        raise PublicationError("template_pin", str(template))
    if git_read(template, ("status", "--porcelain", "--untracked-files=no")):
        raise PublicationError("template_dirty", str(template))
    names = (
        git_read(template, ("ls-files", "-z", "infrastructure", "pyproject.toml", "uv.lock"))
        .decode()
        .strip("\0")
        .split("\0")
    )
    if not names or any((template / n).is_symlink() for n in names):
        raise PublicationError("template_source_inventory", str(template))
    return {name: file_hash(template / name) for name in names if (template / name).is_file()}


def output_member(path: Path, root: Path) -> Member:
    return Member(
        path=path.relative_to(root).as_posix(), size=path.stat().st_size, sha256=file_hash(path)
    )
