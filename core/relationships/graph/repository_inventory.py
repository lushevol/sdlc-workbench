"""Account for local repositories before extraction; do not clone or index."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from collections import Counter
from pathlib import Path

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


def _catalog_paths(workspace: Path) -> tuple[list[tuple[Path, dict]], list[str]]:
    if not any((workspace / filename).exists() for filename in ('workspace.yaml', 'workspace.json')):
        return [], []
    from ai_sdlc_workbench.workspace import load_workspace
    config, _ = load_workspace(workspace)
    rows, limits = [], []
    for item in config['_catalogs'].get('repositories', []):
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
