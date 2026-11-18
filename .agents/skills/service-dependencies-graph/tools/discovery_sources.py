"""Inventory text candidates independently of typed extractor source layouts."""
from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat


MAX_TEXT_BYTES = 2 * 1024 * 1024
_CACHES = {'__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache', '.cache',
           '.next', '.nuxt', '.svelte-kit', '.parcel-cache', '.gradle', '.tox', '.nox'}
_DEPENDENCIES = {'node_modules', '.pnpm-store', '__pypackages__', '.venv'}


def decode_discovery_text(raw: bytes) -> tuple[str, str]:
    """Recognize common text encodings while rejecting binary control bytes."""
    if raw.startswith((b'\xff\xfe\x00\x00', b'\x00\x00\xfe\xff')):
        encoding = 'utf-32'
    elif raw.startswith((b'\xff\xfe', b'\xfe\xff')):
        encoding = 'utf-16'
    else:
        encoding = 'utf-8-sig'
    try:
        text = raw.decode(encoding)
    except UnicodeError:
        encoding = 'latin-1'
        text = raw.decode(encoding)
    if '\x00' in text or any(ord(character) < 32 and character not in '\t\n\r\f\b' for character in text):
        raise ValueError('BINARY_FILE')
    return text, encoding


def read_discovery_text(path: Path) -> str:
    return decode_discovery_text(path.read_bytes())[0]


def _directory_reason(path: Path) -> str | None:
    name = path.name
    if name == '.git':
        return 'GIT_METADATA'
    if name in _DEPENDENCIES or (path / 'pyvenv.cfg').is_file():
        return 'VENDORED_DEPENDENCY'
    if name == 'vendor' and ((path / 'modules.txt').is_file() or (path / 'composer/installed.json').is_file()):
        return 'VENDORED_DEPENDENCY'
    if name in {'cache', 'unplugged'} and path.parent.name == '.yarn':
        return 'VENDORED_DEPENDENCY'
    if name in _CACHES:
        return 'BUILD_ARTIFACT'
    if name == '.terraform' and ((path / 'providers').is_dir() or (path / 'modules').is_dir()):
        return 'VENDORED_DEPENDENCY'
    if name == 'target' and ((path.parent / 'pom.xml').is_file() or (path / 'maven-status').is_dir()):
        return 'BUILD_ARTIFACT'
    if name == 'build' and (any((path.parent / marker).is_file() for marker in ('build.gradle', 'build.gradle.kts'))
                            or (path / 'CMakeCache.txt').is_file()):
        return 'BUILD_ARTIFACT'
    if name == 'coverage' and any((path / marker).is_file() for marker in ('lcov.info', 'coverage-final.json', 'cobertura.xml')):
        return 'BUILD_ARTIFACT'
    return None


def discovery_inventory(root: Path) -> dict:
    """Account for all text files and explicit file or subtree exclusions.

    Generic names such as tests, deployment, generated, vendor, build, and dist
    are traversed unless a specific dependency or output marker identifies them.
    """
    root = Path(os.path.abspath(root))
    rows = []

    def skipped(path, reason, kind, details=None):
        rows.append({'path': path.relative_to(root).as_posix(), 'status': 'SKIPPED',
                     'kind': kind, 'reason': reason, **(details or {})})

    def visit(directory):
        try:
            entries = sorted(directory.iterdir(), key=lambda path: path.name)
        except OSError:
            skipped(directory, 'UNREADABLE_DIRECTORY', 'DIRECTORY')
            return
        for path in entries:
            try:
                metadata = path.lstat()
            except OSError:
                skipped(path, 'UNREADABLE_SOURCE', 'UNKNOWN')
                continue
            if stat.S_ISLNK(metadata.st_mode):
                skipped(path, 'SYMLINK_DIRECTORY' if path.is_dir() else 'SYMLINK_FILE',
                        'DIRECTORY' if path.is_dir() else 'FILE',
                        {'bytes': metadata.st_size, 'mtime_ns': metadata.st_mtime_ns})
                continue
            if stat.S_ISDIR(metadata.st_mode):
                reason = _directory_reason(path)
                if reason:
                    skipped(path, reason, 'DIRECTORY')
                else:
                    visit(path)
                continue
            details = {'bytes': metadata.st_size}
            if not stat.S_ISREG(metadata.st_mode):
                skipped(path, 'NON_REGULAR_FILE', 'FILE', details)
                continue
            if path.name == '.git':
                skipped(path, 'GIT_METADATA', 'FILE')
                continue
            if metadata.st_size > MAX_TEXT_BYTES:
                skipped(path, 'SOURCE_SIZE_LIMIT', 'FILE', {**details, 'mtime_ns': metadata.st_mtime_ns})
                continue
            try:
                with path.open('rb') as source:
                    raw = source.read(MAX_TEXT_BYTES + 1)
            except OSError:
                skipped(path, 'UNREADABLE_SOURCE', 'FILE', {**details, 'mtime_ns': metadata.st_mtime_ns})
                continue
            digest = hashlib.sha256(raw).hexdigest()
            details.update(bytes=len(raw), sha256=digest)
            if len(raw) > MAX_TEXT_BYTES:
                skipped(path, 'SOURCE_SIZE_LIMIT', 'FILE', {'bytes': metadata.st_size, 'mtime_ns': metadata.st_mtime_ns})
                continue
            try:
                _, encoding = decode_discovery_text(raw)
            except ValueError:
                skipped(path, 'BINARY_FILE', 'FILE', details)
                continue
            rows.append({'path': path.relative_to(root).as_posix(), 'status': 'SCANNED',
                         'kind': 'FILE', 'encoding': encoding, **details})

    if root.is_symlink():
        skipped(root, 'SYMLINK_DIRECTORY', 'DIRECTORY')
    else:
        visit(root)
    rows.sort(key=lambda row: row['path'])
    digest = hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    return {'files': rows, 'content_sha256': digest,
            'summary': {'scanned_files': sum(row['status'] == 'SCANNED' for row in rows),
                        'skipped_entries': sum(row['status'] == 'SKIPPED' for row in rows),
                        'skip_reasons': dict(sorted(Counter(row['reason'] for row in rows if row['status'] == 'SKIPPED').items()))}}
