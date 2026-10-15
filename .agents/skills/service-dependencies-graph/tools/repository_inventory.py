"""Account for local repositories before extraction; do not clone or index."""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from collections import Counter
from pathlib import Path

import yaml

from .source_inventory import EXCLUDED, is_source_directory, is_source_file, iter_source_files

GROUP_DIRECTORIES = {'ui', 'services', 'infra', 'libraries', 'testing', 'data', 'integration', 'deployment',
                     'frontends', 'backends'}


def own_git_revision(repository: Path) -> dict:
    """Read the checkout revision only when this directory owns Git metadata."""
    result = {'ref': None, 'commit': None, 'dirty': None}
    if not (repository / '.git').exists():
        return result
    try:
        top = subprocess.check_output(['git', '-C', str(repository), 'rev-parse', '--show-toplevel'],
                                      text=True, stderr=subprocess.DEVNULL).strip()
        if Path(top).resolve() != repository.resolve():
            return result
        for key, args in (('ref', ['branch', '--show-current']), ('commit', ['rev-parse', 'HEAD'])):
            result[key] = subprocess.check_output(['git', '-C', str(repository), *args],
                                                 text=True, stderr=subprocess.DEVNULL).strip() or None
        result['dirty'] = bool(subprocess.check_output(['git', '-C', str(repository), 'status', '--porcelain'],
                                                      text=True, stderr=subprocess.DEVNULL).strip())
    except (OSError, subprocess.CalledProcessError):
        return {'ref': None, 'commit': None, 'dirty': None}
    return result


def nginx_files(repository: Path) -> list[Path]:
    """Select static nginx configuration without following excluded source paths."""
    files = []
    for path in iter_source_files(repository, suffixes={'.conf', '.j2'}):
        try:
            text = path.read_text(encoding='utf-8', errors='replace')
        except OSError:
            continue
        if path.name == 'nginx.conf' or path.name.endswith('.conf.j2') or ('location ' in text and 'proxy_pass ' in text):
            files.append(path)
    return files


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str) or key in result:
            raise ValueError('Declaration mapping keys must be unique strings.')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def _read_declaration(path: Path) -> dict:
    try:
        with path.open('rb') as stream:
            raw = stream.read(1024 * 1024 + 1)
        if len(raw) > 1024 * 1024:
            raise ValueError('Source declarations must not exceed one MiB.')
        payload = yaml.load(raw.decode('utf-8'), Loader=_UniqueKeyLoader)
        if not isinstance(payload, dict):
            raise ValueError('Source declarations must contain an object.')
        json.dumps(payload, allow_nan=False)
        return payload
    except (OSError, UnicodeError, yaml.YAMLError, TypeError, RecursionError) as error:
        raise ValueError(f'Load a readable source declaration: {path}') from error


def _declaration_path(workspace: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative.strip():
        raise ValueError('Use nonempty registry declaration paths.')
    path = workspace / relative
    if Path(relative).is_absolute() or not path.resolve().is_relative_to(workspace):
        raise ValueError('Registry declarations must stay within the workspace.')
    return path


def _repository_records(workspace: Path) -> list[dict]:
    """Read only repository locations; metadata never grants execution."""
    settings_path = workspace / 'workspace.yaml'
    if not settings_path.exists():
        settings_path = workspace / 'workspace.json'
    if not settings_path.exists():
        return []
    settings = _read_declaration(settings_path)
    if type(settings.get('schema_version')) is not int or settings['schema_version'] != 1:
        raise ValueError('Workspace source settings need schema_version 1.')
    locations = settings.get('registries', {})
    categories = {'repositories', 'services', 'capabilities', 'contracts', 'sources', 'tools'}
    if not isinstance(locations, dict) or locations.keys() - categories:
        raise ValueError('Use registered catalog categories.')
    for relative in locations.values():
        _declaration_path(workspace, relative)
    rows = []
    if 'repositories' in locations:
        catalog = _read_declaration(_declaration_path(workspace, locations['repositories']))
        if (set(catalog) != {'schema_version', 'repositories'} or
                type(catalog.get('schema_version')) is not int or catalog['schema_version'] != 1 or
                not isinstance(catalog.get('repositories'), list)):
            raise ValueError('Repository catalogs need schema_version 1 and a repositories list.')
        identifiers = set()
        text_fields = {'name', 'description', 'location', 'responsibility'}
        list_fields = {'responsibilities', 'source_ids', 'provides_contract_ids', 'consumes_contract_ids'}
        for row in catalog['repositories']:
            identifier = row.get('id') if isinstance(row, dict) else None
            if (not isinstance(identifier, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}', identifier)
                    or identifier in identifiers):
                raise ValueError('Repository IDs must be unique names without path separators.')
            identifiers.add(identifier)
            for field in text_fields & row.keys():
                if not isinstance(row[field], str) or not row[field].strip():
                    raise ValueError('Repository text fields must contain nonempty text.')
            for field in list_fields & row.keys():
                values = row[field]
                if (not isinstance(values, list) or any(not isinstance(value, str) or not value.strip() for value in values)
                        or len(set(values)) != len(values)):
                    raise ValueError('Repository lists must contain unique nonempty strings.')
            if 'primary_type' in row and row['primary_type'] not in (
                    'frontend', 'backend', 'library', 'integration', 'data', 'deployment', 'testing'):
                raise ValueError('Use a supported repository primary_type.')
            if 'ownership' in row:
                ownership = row['ownership']
                if (not isinstance(ownership, dict) or ownership.keys() - {'team', 'contact'} or
                        any(not isinstance(value, str) or not value.strip() for value in ownership.values())):
                    raise ValueError('Repository ownership needs nonempty team or contact text.')
            rows.append(dict(row))
    local_path = workspace / 'workspace.local.yaml'
    if local_path.exists() or local_path.is_symlink():
        local = _read_declaration(_declaration_path(workspace, 'workspace.local.yaml'))
        if (set(local) != {'schema_version', 'repository_paths'} or
                type(local.get('schema_version')) is not int or local['schema_version'] != 1 or
                not isinstance(local.get('repository_paths'), dict)):
            raise ValueError('Local settings need schema_version 1 and repository_paths.')
        repositories = {row['id']: row for row in rows}
        for identifier, location in local['repository_paths'].items():
            if identifier not in repositories:
                raise ValueError('A local path references an unknown repository.')
            if not isinstance(location, str) or not location.strip():
                raise ValueError('Local repository paths must be nonempty strings.')
            try:
                path = Path(location).expanduser()
                path = (path if path.is_absolute() else workspace / path).resolve()
            except (ValueError, OSError, RuntimeError) as error:
                raise ValueError('Use a valid local repository path.') from error
            repositories[identifier]['location'] = str(path)
    return rows


def _catalog_paths(workspace: Path) -> tuple[list[tuple[Path, dict]], list[str]]:
    rows, limits = [], []
    for item in _repository_records(workspace):
        location = item.get('location')
        if not location:
            limits.append(f"Registered repository {item['id']} has no local location.")
            continue
        if '://' in location:
            limits.append(f"Registered repository {item['id']} has no local source mapping.")
            continue
        path = Path(location).expanduser()
        path = Path(os.path.abspath(path if path.is_absolute() else workspace / path))
        if not path.is_relative_to(workspace):
            limits.append(f"Registered repository {item['id']} is outside this workspace; static extraction excludes it.")
            continue
        rows.append((path, item))
    return rows, limits


def inventory(workspace: Path, root: Path) -> dict:
    workspace, root = workspace.resolve(), root.resolve()
    if not root.is_dir() or not root.is_relative_to(workspace):
        raise ValueError('Repository root must be an existing directory inside the workspace')
    declared, paths = {}, set()
    manifest = root / 'manifest.json'
    if manifest.is_file():
        data = json.loads(manifest.read_text(encoding='utf-8'))
        for row in data.get('repositories', []):
            path = Path(os.path.abspath(workspace / row['path']))
            if not path.is_relative_to(root) or path == root or path in declared:
                raise ValueError('Manifest paths must identify unique repositories inside the repository root')
            declared[path] = row
            paths.add(path)
    catalog_paths, registry_limits = _catalog_paths(workspace)
    for path, entry in catalog_paths:
        declared[path] = {**declared.get(path, {}), 'registry_id': entry['id']}
        paths.add(path)
    for child in sorted(root.iterdir()):
        if not child.is_dir() or child.name.startswith('.'):
            continue
        if (child.name in GROUP_DIRECTORIES and not child.is_symlink() and not (child / '.git').exists()
                and not (child / 'package.json').exists() and not (child / 'pom.xml').exists()):
            paths.update(path for path in child.iterdir() if path.is_dir() and not path.name.startswith('.'))
        else:
            paths.add(child)
    rows, names = [], set()
    for repo in sorted(paths, key=lambda path: path.as_posix()):
        name = repo.name
        if name in names:
            raise ValueError(f'Duplicate repository directory name: {name}')
        names.add(name)
        row = {'name': name, 'path': repo.relative_to(workspace).as_posix(), 'declared': repo in declared,
               'status': 'MISSING', 'kind': None, 'source_files': 0, 'source_extensions': {},
               'content_sha256': None, 'source_exclusions': [], 'nested_manifests': [], 'limitations': [],
               **own_git_revision(repo)}
        if declared.get(repo, {}).get('registry_id'):
            row['registry_id'] = declared[repo]['registry_id']
        rows.append(row)
        if not repo.exists():
            row['limitations'].append('Declared repository source is missing.')
            continue
        if repo.is_symlink() or not repo.resolve().is_relative_to(workspace):
            row['status'] = 'UNSUPPORTED'
            row['limitations'].append('Symlink repository roots are not traversed.')
            continue
        has_web = is_source_file(repo, repo / 'package.json')
        has_java = is_source_file(repo, repo / 'pom.xml')
        java_root = repo / 'src/main/java'
        web_sources = (any(not path.is_relative_to(java_root) for path in iter_source_files(
            repo, root=repo / 'src', suffixes={'.js', '.jsx', '.ts', '.tsx'})) if has_web else False)
        java_runtime = has_java and is_source_directory(repo, java_root)
        row['kind'] = ('SPRING' if java_runtime and not web_sources else 'WEB' if has_web
                       else 'SPRING' if has_java else 'INFRA' if nginx_files(repo) else None)
        row['status'] = 'SCANNED' if row['kind'] else 'UNSUPPORTED'
        if row['commit'] is None:
            row['limitations'].append('Source snapshot has no readable independent Git revision.')
        counts, digest, nested = Counter(), hashlib.sha256(), []
        for path in iter_source_files(repo, exclusions=row['source_exclusions']):
            relative = path.relative_to(repo).as_posix()
            counts[path.suffix] += 1
            digest.update(relative.encode() + b'\0' + hashlib.sha256(path.read_bytes()).digest())
            if path.name in {'pom.xml', 'package.json'} and path.parent != repo:
                nested.append(relative)
        row.update(source_files=sum(counts.values()), source_extensions=dict(sorted(counts.items())),
                   content_sha256=digest.hexdigest())
        if nested:
            row['nested_manifests'] = nested
            row['limitations'].append('Nested manifests supply package identities and build dependencies. Runtime extraction uses the root src layout.')
        if has_web and has_java:
            row['limitations'].append(f"Mixed root manifests: runtime extraction selects {row['kind']} source layouts.")
        source_links = [item for item in row['source_exclusions'] if item['reason'].startswith('SYMLINK_')]
        if source_links:
            row['limitations'].append('Source symlinks are excluded. See source_exclusions for each path.')
        templates = [path for path in nginx_files(repo) if path.name.endswith('.j2')] if row['kind'] == 'INFRA' else []
        if templates:
            row['limitations'].append('Nginx templates need environment values. Dynamic template routes remain unresolved.')
        expected = repo / ('src' if row['kind'] == 'WEB' else 'src/main/java')
        if row['kind'] in {'WEB', 'SPRING'} and not is_source_directory(repo, expected):
            row['limitations'].append('Root source layout is unsupported or absent.')
            row['status'] = 'PARTIAL'
        elif row['kind'] and (nested or (has_web and has_java) or source_links or templates):
            row['status'] = 'PARTIAL'
        if not row['kind']:
            row['limitations'].append('No supported root manifest or nginx configuration exists. Only source inventory is available.')
    return {'schema_version': '1.0.0', 'repositories': rows,
            'counts': dict(sorted(Counter(row['status'] for row in rows).items())),
            'excluded_directories': sorted(EXCLUDED), 'registry_limits': registry_limits,
            'repository_root': root.relative_to(workspace).as_posix()}
