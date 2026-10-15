"""Use one source boundary for extraction, census, and content fingerprints."""
from __future__ import annotations

import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable, Iterator


EXCLUDED = {'.git', '.gitnexus', 'node_modules', 'target', 'build', 'dist', 'coverage',
            '.venv', 'venv', '__pycache__', 'generated', 'test', 'tests', '__tests__', '@types'}
SOURCE_SUFFIXES = {'.java', '.kt', '.ts', '.tsx', '.js', '.jsx', '.py', '.go', '.rs', '.cs',
                   '.xml', '.json', '.yaml', '.yml', '.properties', '.conf', '.j2', '.graphql', '.sql',
                   '.robot', '.resource'}


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


def discover_maven_modules(repository: Path) -> dict:
    """Read declared module roots without invoking Maven or selecting profiles."""
    repository = _absolute(repository)
    pending, visited, modules, diagnostics = [repository], set(), [], []
    while pending:
        module = pending.pop(0)
        if module in visited:
            continue
        visited.add(module)
        relative = module.relative_to(repository).as_posix() if module.is_relative_to(repository) else str(module)
        if not is_source_file(repository, module / 'pom.xml'):
            diagnostics.append({'code': 'UNAVAILABLE_MAVEN_MODULE', 'path': relative,
                                'message': 'Declared module has no included readable pom.xml'})
            continue
        try:
            document = ET.fromstring((module / 'pom.xml').read_bytes())
        except (OSError, ET.ParseError):
            diagnostics.append({'code': 'MAVEN_MODULE_PARSE_ERROR', 'path': relative + '/pom.xml',
                                'message': 'Cannot parse declared Maven module'})
            continue
        modules.append(module)
        declared_roots = document.findall('./{*}build/{*}sourceDirectory') + document.findall('./{*}build/{*}resources/{*}resource/{*}directory')
        for declaration in declared_roots:
            value = (declaration.text or '').strip()
            candidate = _absolute(module / value)
            if not value or '${' in value or not is_source_directory(repository, candidate):
                diagnostics.append({'code': 'UNRESOLVED_MAVEN_SOURCE_ROOT', 'path': relative + '/pom.xml',
                                    'message': 'Custom source root is dynamic, excluded, missing, or outside its repository'})
        for declaration in document.findall('./{*}modules/{*}module'):
            value = (declaration.text or '').strip()
            child = _absolute(module / value)
            if (not value or '${' in value or not child.is_relative_to(repository)
                    or not is_source_directory(repository, child)):
                diagnostics.append({'code': 'UNRESOLVED_MAVEN_MODULE', 'path': relative + '/pom.xml',
                                    'message': 'Module path is dynamic, excluded, missing, or outside its repository'})
            elif child in visited:
                diagnostics.append({'code': 'DUPLICATE_MAVEN_MODULE', 'path': relative + '/pom.xml',
                                    'message': 'Module cycle or duplicate declaration was not traversed twice'})
            elif child not in pending:
                pending.append(child)
        for profile in document.findall('./{*}profiles/{*}profile'):
            if profile.findall('./{*}modules/{*}module'):
                diagnostics.append({'code': 'PROFILE_MAVEN_MODULES', 'path': relative + '/pom.xml',
                                    'message': 'Profile module activation is unknown; profile-only modules are not selected'})
    return {'modules': modules, 'diagnostics': diagnostics}


def maven_modules(repository: Path) -> list[Path]:
    return discover_maven_modules(repository)['modules']


def _maven_roots(repository: Path, kind: str) -> list[Path]:
    roots = []
    modules = maven_modules(repository) if is_source_file(repository, repository / 'pom.xml') else [repository]
    for module in modules:
        candidates = [module / ('src/main/java' if kind == 'java' else 'src/main/resources')]
        try:
            document = ET.fromstring((module / 'pom.xml').read_bytes())
            if kind == 'java':
                custom = document.find('./{*}build/{*}sourceDirectory')
                if custom is not None:
                    candidates = [module / custom.text.strip()] if custom.text and '${' not in custom.text else []
            else:
                configured = document.findall('./{*}build/{*}resources/{*}resource/{*}directory')
                if configured:
                    candidates = [module / item.text.strip() for item in configured if item.text and '${' not in item.text]
        except (OSError, ET.ParseError):
            pass
        for path in candidates:
            path = _absolute(path)
            if is_source_directory(repository, path) and path not in roots:
                roots.append(path)
    return roots


def java_source_roots(repository: Path) -> list[Path]:
    return _maven_roots(repository, 'java')


def resource_source_roots(repository: Path) -> list[Path]:
    return _maven_roots(repository, 'resources')
