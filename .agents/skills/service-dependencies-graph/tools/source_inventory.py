"""Use one source boundary for extraction, census, and content fingerprints."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, Iterator


EXCLUDED = {'.git', '.gitnexus', 'node_modules', 'target', 'build', 'dist', 'coverage',
            '.venv', 'venv', '__pycache__', 'generated', 'test', 'tests', '__tests__', '@types'}
SOURCE_SUFFIXES = {'.java', '.kt', '.ts', '.tsx', '.js', '.jsx', '.py', '.go', '.rs', '.cs',
                   '.xml', '.json', '.yaml', '.yml', '.properties', '.conf', '.j2', '.graphql', '.sql'}


def _absolute(path: Path) -> Path:
    # Normalize relative segments without following a source symlink.
    return Path(os.path.abspath(path))


def _directory_issue(repository: Path, directory: Path) -> str | None:
    if not directory.is_relative_to(repository):
        return 'OUTSIDE_REPOSITORY'
    for path in (directory, *directory.parents):
        if path == repository:
            return 'SYMLINK_DIRECTORY' if path.is_symlink() else None
        if path.is_symlink():
            return 'SYMLINK_DIRECTORY'
        if path.name in EXCLUDED:
            return 'EXCLUDED_DIRECTORY'
        if path.name.startswith('.'):
            return 'HIDDEN_DIRECTORY'
    return 'OUTSIDE_REPOSITORY'


def is_source_file(repository: Path, path: Path) -> bool:
    repository, path = _absolute(repository), _absolute(path)
    return (path.suffix in SOURCE_SUFFIXES and not path.is_symlink()
            and _directory_issue(repository, path.parent) is None and path.is_file())


def is_source_directory(repository: Path, path: Path) -> bool:
    repository, path = _absolute(repository), _absolute(path)
    return _directory_issue(repository, path) is None and path.is_dir()


def iter_source_files(repository: Path, *, root: Path | None = None,
                      suffixes: Iterable[str] | None = None,
                      exclusions: list[dict[str, str]] | None = None) -> Iterator[Path]:
    repository = _absolute(repository)
    root = _absolute(root or repository)
    allowed = SOURCE_SUFFIXES if suffixes is None else SOURCE_SUFFIXES & set(suffixes)

    def exclude(path: Path, reason: str) -> None:
        if exclusions is not None:
            relative = path.relative_to(repository).as_posix() if path.is_relative_to(repository) else str(path)
            exclusions.append({'path': relative, 'reason': reason})

    issue = _directory_issue(repository, root)
    if issue:
        exclude(root, issue)
        return
    for parent, directories, filenames in os.walk(root, followlinks=False):
        parent = Path(parent)
        accepted = []
        for name in sorted(directories):
            path = parent / name
            issue = _directory_issue(repository, path)
            if issue:
                exclude(path, issue)
            else:
                accepted.append(name)
        directories[:] = accepted
        for name in sorted(filenames):
            path = parent / name
            if path.is_symlink():
                exclude(path, 'SYMLINK_FILE')
            elif path.suffix in allowed and path.is_file():
                yield path


def source_directories(repository: Path, *, root: Path) -> set[Path]:
    """Return only directories that contain an included source file."""
    root = _absolute(root)
    directories = set()
    for path in iter_source_files(repository, root=root):
        for parent in path.parents:
            if parent == root:
                break
            directories.add(parent)
    return directories
