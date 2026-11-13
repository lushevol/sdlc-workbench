"""Project local knowledge declarations without granting truth or publication."""
from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re

import yaml


SCHEMA_VERSION = '1.0.0'
MAX_DECLARATION_BYTES = 4 * 1024 * 1024
MAX_INPUTS = 20000
_HASH = re.compile(r'[a-f0-9]{64}\Z')
_TYPES = {'KnowledgeTopic', 'Requirement', 'Architecture', 'Decision', 'RepositoryProfile', 'GovernanceFinding'}
_STATES = {'candidate', 'investigated', 'verified', 'published', 'contested', 'stale', 'superseded'}
_CATALOGS = ('repositories', 'services', 'capabilities', 'contracts', 'sources', 'tools')
LIMITATIONS = [
    'Projected links retain declarations. They do not establish semantic truth, business conformance, or human approval.',
    'Candidate, historical, contested, stale, and superseded records keep their declared states.',
    'Source hashes identify retained bytes. They do not establish live-source freshness, deployment, or runtime execution.',
    'Related IDs are navigation references. They do not establish implementation or assertion coverage.',
    'Historical missing locators remain unresolved. No relocation or version equivalence is inferred.',
]



def _knowledge_roots(project):
    """Reuse runtime layout resolution; standalone graph environments need no runtime install."""
    try:
        from ai_sdlc_workbench.knowledge_layout import knowledge_layout
    except ImportError as error:
        if error.name not in {None, "ai_sdlc_workbench", "ai_sdlc_workbench.knowledge_layout"}:
            raise
        # Standalone graph runtimes can omit the Workbench package.
        project = Path(project).resolve()
        current, legacy = project / "knowledge/evidence", project / "evidence/knowledge"
        current_marker, legacy_marker = current / "manifest.yaml", legacy / "manifest.yaml"
        current_present = current_marker.exists() or current_marker.is_symlink()
        legacy_present = legacy_marker.exists() or legacy_marker.is_symlink()
        if current_present and legacy_present:
            raise ValueError("Both knowledge manifests exist. Finish or recover the layout migration before continuing.")
        if current_present:
            records = project / "knowledge/records"
            if not records.is_dir():
                raise ValueError("The consolidated knowledge layout requires knowledge/records/. Restore it before continuing.")
            return records, current
        if not legacy_present and any(path.exists() or path.is_symlink() for path in (current, project / "knowledge/records")):
            raise ValueError("The consolidated knowledge layout is incomplete. Restore knowledge/evidence/manifest.yaml before continuing.")
        return project / "knowledge", legacy
    return knowledge_layout(project)

def _identity(kind, *parts):
    raw = json.dumps(parts, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)
    return 'knowledge:' + kind + ':' + hashlib.sha256(raw.encode()).hexdigest()[:24]


def _record_hash(value):
    raw = json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(raw.encode()).hexdigest()


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if not isinstance(key, str) or key in result:
            raise ValueError('Knowledge input keys must be unique strings.')
        result[key] = value
    return result


class _Loader(yaml.SafeLoader):
    pass


def _mapping(loader, node, deep=False):
    return _pairs(loader.construct_pairs(node, deep=deep))


_Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def _safe(root, value, *, required=False):
    if not isinstance(value, str) or not value or '\x00' in value or '\\' in value:
        raise ValueError('Knowledge input paths must be nonempty workspace-relative paths.')
    relative = PurePosixPath(value)
    if relative.is_absolute() or PureWindowsPath(value).drive or '..' in relative.parts:
        raise ValueError('Knowledge input paths must stay within the workspace.')
    path = root / value
    for part in (path, *path.parents):
        if part == root.parent:
            break
        if part.is_symlink():
            raise ValueError('Knowledge inputs must not use symbolic links: ' + value)
    if not path.resolve().is_relative_to(root):
        raise ValueError('Knowledge input paths must stay within the workspace.')
    if required and not path.is_file():
        raise ValueError('A declared knowledge input is unavailable: ' + value)
    return path


def _bytes(path):
    with path.open('rb') as stream:
        raw = stream.read(MAX_DECLARATION_BYTES + 1)
    if len(raw) > MAX_DECLARATION_BYTES:
        raise ValueError('A knowledge declaration exceeds the four MiB limit.')
    return raw


def _decode(path):
    try:
        text = _bytes(path).decode('utf-8')
        value = (json.loads(text, object_pairs_hook=_pairs,
                            parse_constant=lambda _: (_ for _ in ()).throw(ValueError('Use finite JSON values.')))
                 if path.suffix.lower() == '.json' else yaml.load(text, Loader=_Loader))
        json.dumps(value, allow_nan=False)
        if not isinstance(value, dict):
            raise ValueError('Knowledge declarations must contain objects.')
        return value
    except (UnicodeError, yaml.YAMLError, TypeError, RecursionError) as error:
        raise ValueError('Load valid UTF-8 knowledge declarations: ' + path.name) from error


def _digest(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(65536), b''):
            digest.update(block)
    return digest.hexdigest()


def _walk(root, relative, suffixes):
    base = _safe(root, relative)
    if not base.exists():
        return []
    if not base.is_dir():
        raise ValueError('Knowledge input roots must be directories: ' + relative)
    result = []
    for directory, directories, files in os.walk(base, followlinks=False):
        if relative == 'knowledge' and Path(directory) == base:
            # The compiled wiki owns its schema, state, and canonical-source links.
            directories[:] = [name for name in directories if name.casefold() != 'llm-wiki']
            files = [name for name in files if name.casefold() != 'llm-wiki']
        for name in sorted(directories + files):
            path = Path(directory) / name
            _safe(root, path.relative_to(root).as_posix())
        for name in sorted(files):
            path = Path(directory) / name
            if path.suffix.lower() in suffixes:
                result.append(path)
                if len(result) > MAX_INPUTS:
                    raise ValueError('The knowledge input inventory exceeds its bound.')
    return sorted(result)


def _catalog_locations(root):
    settings = {}
    configs = []
    for name in ('workspace.yaml', 'workspace.json'):
        path = _safe(root, name)
        if path.exists():
            settings = _decode(path)
            configs.append(path)
            break
    locations = settings.get('registries', {})
    if not isinstance(locations, dict) or set(locations) - set(_CATALOGS):
        raise ValueError('Knowledge projection needs supported registry declarations.')
    paths = {}
    for category in _CATALOGS:
        path = _safe(root, locations.get(category, 'registry/' + category + '.yaml'))
        if path.exists():
            paths[category] = path
    local = _safe(root, 'workspace.local.yaml')
    if local.exists():
        configs.append(local)
    return paths, configs


def _manifest(root):
    _, evidence = _knowledge_roots(root)
    path = _safe(root, (evidence / 'manifest.yaml').relative_to(root).as_posix())
    if not path.exists():
        return path, []
    value = _decode(path)
    if value.get('schema_version') != 1 or not isinstance(value.get('sources'), list):
        raise ValueError('Use source manifest schema version 1 with a sources list.')
    seen = set()
    for row in value['sources']:
        _source_key(row)
        if not isinstance(row.get('id'), str) or not row['id']:
            raise ValueError('Manifest sources need stable IDs.')
        key = (row['resource'], row['revision'])
        if key in seen:
            raise ValueError('Source resource/revision pairs must be unique.')
        seen.add(key)
        if row.get('snapshot') is not None:
            _safe(root, row['snapshot'])
    return path, value['sources']


def _source_key(row):
    if not isinstance(row, dict) or any(not isinstance(row.get(key), str) or not row[key]
                                         for key in ('resource', 'revision', 'sha256')):
        raise ValueError('Source citations need resource, revision, and SHA-256.')
    if not _HASH.fullmatch(row['sha256']):
        raise ValueError('Source citations need lowercase SHA-256 values.')
    return row['resource'], row['revision'], row['sha256']


def input_fingerprints(workspace):
    """Return sorted local inputs. Missing historical targets are not invented."""
    root = Path(workspace).resolve()
    paths = set()
    canonical, evidence = _knowledge_roots(root)
    for relative, suffixes in ((canonical.relative_to(root).as_posix(), {'.md'}),
                               ((evidence / 'findings').relative_to(root).as_posix(), {'.md'}),
                               ((evidence / 'audit').relative_to(root).as_posix(), {'.yaml', '.yml'}),
                               ('relationships/requirement-code/baselines', {'.json'})):
        paths.update(_walk(root, relative, suffixes))
    catalogs, configs = _catalog_locations(root)
    paths.update(catalogs.values())
    paths.update(configs)
    manifest, sources = _manifest(root)
    if manifest.is_file():
        paths.add(manifest)
    for source in sources:
        if source.get('snapshot'):
            path = _safe(root, source['snapshot'])
            if path.is_file():
                paths.add(path)
    # Baseline-referenced retained files can live outside the source manifest.
    for path in list(paths):
        if path.parent == root / 'relationships/requirement-code/baselines':
            value = _decode(path)
            for row in _rows(value, 'artifacts', path):
                target = _safe(root, row.get('path'))
                if target.is_file():
                    paths.add(target)
    if len(paths) > MAX_INPUTS:
        raise ValueError('The knowledge input inventory exceeds its bound.')
    return [{'path': path.relative_to(root).as_posix(), 'sha256': _digest(path)}
            for path in sorted(paths, key=lambda item: item.relative_to(root).as_posix())]


def _rows(value, key, path):
    rows = value.get(key, [])
    if not isinstance(rows, list) or len(rows) > MAX_INPUTS or any(not isinstance(row, dict) for row in rows):
        raise ValueError('Use object lists for ' + key + ' in ' + path.name)
    seen = set()
    for row in rows:
        if not isinstance(row.get('id'), str) or not row['id'] or row['id'] in seen:
            raise ValueError('Use unique record IDs for ' + key + ' in ' + path.name)
        seen.add(row['id'])
    return rows


def _baseline(value, file, root):
    """Validate the projected fields without interpreting baseline business claims."""
    if type(value.get('schema_version')) is not int or value['schema_version'] != 1 or not isinstance(value.get('baseline_id'), str) or not value['baseline_id']:
        raise ValueError('Behavior baselines need schema version 1 and an ID.')
    for row in _rows(value, 'artifacts', file):
        _safe(root, row.get('path'))
        if row.get('kind') not in {'INTENT', 'CODE', 'TEST', 'EXECUTION'} or not _HASH.fullmatch(str(row.get('sha256', ''))):
            raise ValueError('Baseline artifacts need a supported kind and SHA-256.')
        if 'source_path' in row:
            _safe(root, row['source_path'])
        if 'revision' in row and not re.fullmatch(r'[a-f0-9]{40}|[a-f0-9]{64}', str(row['revision'])):
            raise ValueError('Baseline source revisions must identify exact commits.')
    for row in _rows(value, 'behaviors', file):
        intent = row.get('intent')
        if type(row.get('version')) is not int or row['version'] < 1 or not isinstance(intent, dict):
            raise ValueError('Behavior records need a positive version and intent locator.')
        if not isinstance(intent.get('artifact_id'), str) or not _HASH.fullmatch(str(intent.get('record_sha256', ''))):
            raise ValueError('Behavior intent locators need an artifact identity and metadata SHA-256.')
        _line_range(intent)
    for row in _rows(value, 'links', file):
        if row.get('relationship') not in {'IMPLEMENTED_BY', 'ASSERTED_BY'} or row.get('grade') not in {'CONFIRMED', 'LIKELY', 'POSSIBLE', 'UNRESOLVED'}:
            raise ValueError('Baseline links need supported relationship and grade values.')
        for field in ('behavior_record_sha256', 'artifact_record_sha256'):
            if not _HASH.fullmatch(str(row.get(field, ''))):
                raise ValueError('Baseline links need exact endpoint metadata SHA-256 values.')
        if any(not isinstance(row.get(field), str) or not row[field] for field in ('behavior_id', 'artifact_id')):
            raise ValueError('Baseline links need endpoint identities.')
        _line_range(row)
    for row in _rows(value, 'executions', file):
        if not isinstance(row.get('artifact_id'), str) or not _HASH.fullmatch(str(row.get('artifact_record_sha256', ''))):
            raise ValueError('Execution declarations need exact result artifact identity and metadata SHA-256.')
        codes, bindings = row.get('code_artifact_ids', []), row.get('assertion_bindings', [])
        if not isinstance(codes, list) or any(not isinstance(code, str) for code in codes):
            raise ValueError('Execution code references must contain ID strings.')
        if not isinstance(bindings, list) or any(not isinstance(binding, dict) or not isinstance(binding.get('link_id'), str)
                                                or not _HASH.fullmatch(str(binding.get('link_record_sha256', ''))) for binding in bindings):
            raise ValueError('Execution assertion bindings need exact link identities and metadata SHA-256 values.')
    _rows(value, 'findings', file)


def _line_range(row):
    if (type(row.get('start_line')) is not int or type(row.get('end_line')) is not int
            or not 1 <= row['start_line'] <= row['end_line']):
        raise ValueError('Behavior locators require valid positive line ranges.')


def _frontmatter(path):
    text = _bytes(path).decode('utf-8')
    if path.name in {'README.md', 'index.md'}:
        return None
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)', text, re.DOTALL)
    if not match:
        raise ValueError('Knowledge records require YAML frontmatter: ' + path.name)
    value = yaml.load(match.group(1), Loader=_Loader)
    if (not isinstance(value, dict) or value.get('type') not in _TYPES or
            not isinstance(value.get('id'), str) or not value['id'] or
            type(value.get('version')) is not int or value['version'] < 1 or
            value.get('governance_state') not in _STATES or
            not isinstance(value.get('owner'), str) or not value['owner'] or
            not isinstance(value.get('sources'), list)):
        raise ValueError('Knowledge records need valid type, identity, version, lifecycle, owner, and sources: ' + path.name)
    for source in value['sources']:
        _source_key(source)
    if not isinstance(value.get('related', []), list) or any(not isinstance(item, str) or not item for item in value.get('related', [])):
        raise ValueError('Related references must be nonempty ID strings.')
    return value


class _Projection:
    def __init__(self, graph, inputs):
        self.graph, self.root, self.inputs = graph, Path(graph.workspace).resolve(), inputs
        self.hashes = {row['path']: row['sha256'] for row in inputs}
        self.by_id, self.records, self.sources, self.catalogs = defaultdict(list), {}, {}, {}
        self.record_paths, self.catalog_paths = {}, {}
        self.criteria = {}

    def evidence(self, path, label, *, line=1):
        return self.graph.add_evidence(None, path, line, label, 'knowledge-projection')

    def node(self, kind, identity, path, properties, *, name=None, evidence=None):
        node_id = _identity(kind.lower(), *identity)
        properties = {'projection': 'knowledge', **properties}
        self.graph.add_node(node_id, kind, name or str(properties.get('record_id', kind)), None,
                            dimensions=('KNOWLEDGE',), component_kind=None,
                            functional_role='Retained knowledge declaration',
                            business_meaning='Declared ' + kind.lower().replace('_', ' ') + '; review evidence and limits.',
                            source_paths=[path], evidence=[evidence or self.evidence(path, kind + ' metadata')],
                            properties=properties)
        return node_id

    def edge(self, left, right, relationship, path, **properties):
        return self.graph.add_edge(left, right, relationship, 'KNOWLEDGE',
                                   [self.evidence(path, relationship + ' declaration')],
                                   properties={'projection': 'knowledge', 'evidence_class': 'DECLARED_METADATA', **properties})

    def unresolved(self, owner, reference, path, reason, *, relationship='HAS_UNRESOLVED_REFERENCE', **properties):
        node = self.node('UNRESOLVED_REFERENCE', (owner, reference, reason), path,
                         {'record_id': reference, 'evidence_class': 'UNKNOWN', 'reason': reason, **properties})
        self.graph.diagnostic('KNOWLEDGE_REFERENCE_UNRESOLVED', reason + ': ' + reference, path=path)
        self.edge(owner, node, relationship, path, resolution_status='UNRESOLVED')
        return node

    def reference(self, owner, reference, path, relationship='RELATED_TO', *, version=None, digest=None):
        candidates = self.by_id.get(reference, [])
        if version is not None:
            candidates = [node for node in candidates if self.graph.nodes[node]['properties'].get('version') == version]
        if digest is not None:
            candidates = [node for node in candidates if self.graph.nodes[node]['properties'].get('content_sha256') == digest]
        if len(candidates) == 1:
            self.edge(owner, candidates[0], relationship, path)
            return candidates[0]
        return self.unresolved(owner, reference, path, 'Ambiguous reference' if candidates else 'Missing exact reference',
                               relationship=relationship, requested_version=version, requested_sha256=digest)

    def load_sources(self):
        manifest, rows = _manifest(self.root)
        path = manifest.relative_to(self.root).as_posix()
        for row in rows:
            key = _source_key(row)
            snapshot = row.get('snapshot')
            status = ('MATCH' if self.hashes.get(snapshot) == row['sha256'] else
                      'MISMATCH' if snapshot in self.hashes else 'MISSING' if snapshot else 'NOT_RETAINED')
            node = self.node('SOURCE_REVISION', key, path,
                             {'record_id': row['id'], 'revision': row['revision'], 'sha256': row['sha256'],
                              'resource': row['resource'], 'classification': row.get('classification', 'unknown'),
                              'evidence_class': 'DECLARED_METADATA', 'snapshot': snapshot,
                              'snapshot_status': status, 'applicability': row.get('applicability', 'unknown')})
            self.sources[key] = node
            self.by_id[row['id']].append(node)
            if status in {'MISMATCH', 'MISSING'}:
                self.unresolved(node, snapshot, path, 'Retained snapshot ' + status.lower(), expected_sha256=row['sha256'])

    def citations(self, node, sources, path):
        for source in sources:
            key = _source_key(source)
            target = self.sources.get(key)
            if target:
                self.edge(node, target, 'CITES_SOURCE', path, source_revision=source['revision'], source_sha256=source['sha256'])
            else:
                self.unresolved(node, source['resource'], path, 'Source citation is absent from the manifest',
                                relationship='CITES_SOURCE', source_revision=source['revision'], source_sha256=source['sha256'])

    def load_records(self):
        identities = set()
        canonical, evidence = _knowledge_roots(self.root)
        for folder in (canonical.relative_to(self.root).as_posix(),
                       (evidence / 'findings').relative_to(self.root).as_posix()):
            for file in _walk(self.root, folder, {'.md'}):
                meta = _frontmatter(file)
                if meta is None:
                    continue
                key = (meta['id'], meta['version'])
                if key in identities:
                    raise ValueError('Knowledge ID/version pairs must be unique.')
                identities.add(key)
                path = file.relative_to(self.root).as_posix()
                props = {key: deepcopy(meta[key]) for key in ('id', 'version', 'owner', 'governance_state', 'status') if key in meta}
                props['record_id'] = props.pop('id')
                props.update(record_type=meta['type'], content_sha256=self.hashes[path], evidence_class='DOCUMENTED_INTENT')
                kind = 'FINDING' if meta['type'] == 'GovernanceFinding' else 'KNOWLEDGE_RECORD'
                if kind == 'FINDING':
                    props.update(evidence_class='DECLARED_METADATA', resolution=meta.get('resolution', 'unknown'))
                title = meta.get('title')
                node = self.node(kind, (meta['id'], meta['version'], self.hashes[path]), path, props,
                                 name=title if isinstance(title, str) and title.strip() else meta['id'])
                self.by_id[meta['id']].append(node)
                self.records[node], self.record_paths[node] = meta, path
                self.citations(node, meta['sources'], path)
                for criterion in _rows(meta, 'acceptance_criteria', file):
                    if any(not isinstance(criterion.get(key), str) or not criterion[key] for key in ('given', 'when', 'then')):
                        raise ValueError('Acceptance criteria require Given, When, and Then text.')
                    ac = self.node('ACCEPTANCE_CRITERION', (node, criterion['id'], _record_hash(criterion)), path,
                                   {**props, 'record_id': criterion['id'], 'parent_record_id': meta['id'],
                                    'record_sha256': _record_hash(criterion)})
                    self.edge(node, ac, 'HAS_CRITERION', path)
                    self.criteria[(node, criterion['id'])] = ac
        for node, meta in self.records.items():
            path = self.record_paths[node]
            for reference in meta.get('related', []):
                self.reference(node, reference, path)
            if meta.get('repository_id'):
                self.reference(node, meta['repository_id'], path, 'DESCRIBES_REPOSITORY')
            if meta['type'] == 'GovernanceFinding':
                subject = meta.get('subject', {})
                self.reference(node, subject.get('id', 'unknown'), path, 'CONCERNS', version=subject.get('version'))
                self.citations(node, meta.get('evidence', []), path)

    def load_catalogs(self):
        paths, configs = _catalog_locations(self.root)
        rows_by_category = {}
        for category, file in paths.items():
            if category == 'tools':
                continue  # Execution tool configuration is fingerprinted, never copied.
            value = _decode(file)
            if value.get('schema_version') != 1:
                raise ValueError('Knowledge catalogs require schema version 1.')
            rows = _rows(value, category, file)
            rows_by_category[category] = rows
            path = file.relative_to(self.root).as_posix()
            for row in rows:
                node = self.node('CATALOG_ENTITY', (category, row['id'], _record_hash(row)), path,
                                 {'record_id': row['id'], 'catalog': category, 'content_sha256': _record_hash(row),
                                  'evidence_class': 'DECLARED_METADATA'}, name=row.get('name', row['id']))
                self.catalogs[(category, row['id'])] = node
                self.catalog_paths[node] = path
                self.by_id[row['id']].append(node)
        relations = {'repository_ids': ('repositories', 'ASSOCIATED_WITH_REPOSITORY'),
                     'repository_id': ('repositories', 'ASSOCIATED_WITH_REPOSITORY'),
                     'deployment_repository_ids': ('repositories', 'DEPLOYMENT_DECLARED_IN'),
                     'service_ids': ('services', 'ASSOCIATED_WITH_SERVICE'),
                     'source_ids': ('sources', 'DECLARES_SOURCE'),
                     'provides_contract_ids': ('contracts', 'PROVIDES_CONTRACT'),
                     'consumes_contract_ids': ('contracts', 'CONSUMES_CONTRACT')}
        for category, rows in rows_by_category.items():
            for row in rows:
                node = self.catalogs[(category, row['id'])]
                path = self.catalog_paths[node]
                for field, (target_category, relationship) in relations.items():
                    references = row.get(field, [])
                    references = [references] if isinstance(references, str) else references
                    if not isinstance(references, list) or any(not isinstance(ref, str) for ref in references):
                        raise ValueError('Catalog references must contain ID strings.')
                    for reference in references:
                        target = self.catalogs.get((target_category, reference))
                        if target:
                            self.edge(node, target, relationship, path)
                        else:
                            self.unresolved(node, reference, path, 'Missing catalog reference', relationship=relationship)
        local = next((file for file in configs if file.name == 'workspace.local.yaml'), None)
        overrides = _decode(local).get('repository_paths', {}) if local else {}
        if not isinstance(overrides, dict):
            raise ValueError('Repository path overrides must be an object.')
        for row in rows_by_category.get('repositories', []):
            node = self.catalogs[('repositories', row['id'])]
            path = self.catalog_paths[node]
            location = overrides.get(row['id'], row.get('location'))
            if not location or not isinstance(location, str) or '://' in location:
                self.unresolved(node, row['id'], path, 'No usable local repository location')
                continue
            declared = Path(location).expanduser()
            declared = declared if declared.is_absolute() else self.root / declared
            matches = [repo['id'] for repo in self.graph.repositories
                       if (self.root / repo['path']).resolve() == declared.resolve()]
            roots = [item['id'] for item in self.graph.nodes.values()
                     if item.get('repository') in matches and item['type'] in {'APPLICATION', 'SERVICE'}]
            if len(matches) != 1 or not roots:
                self.unresolved(node, row['id'], path, 'Repository graph identity is absent or ambiguous')
                continue
            for target in sorted(roots):
                self.edge(node, target, 'SAME_REPOSITORY_AS', path, graph_repository_id=matches[0], binding='EXACT_LOCAL_PATH')

    def load_audits(self):
        _, evidence = _knowledge_roots(self.root)
        for file in _walk(self.root, (evidence / 'audit').relative_to(self.root).as_posix(), {'.yaml', '.yml'}):
            event = _decode(file)
            for field in ('id', 'item_id', 'content_sha256', 'action', 'from_state', 'to_state'):
                if not isinstance(event.get(field), str) or not event[field]:
                    raise ValueError('Audit events need complete identity and state fields.')
            if type(event.get('item_version')) is not int or event['item_version'] < 1 or not _HASH.fullmatch(event['content_sha256']):
                raise ValueError('Audit targets need a valid version and final file SHA-256.')
            path = file.relative_to(self.root).as_posix()
            props = {key: deepcopy(event[key]) for key in ('item_id', 'item_version', 'content_sha256', 'action', 'from_state', 'to_state', 'actor', 'at') if key in event}
            props.update(record_id=event['id'], evidence_class='DECLARED_METADATA')
            node = self.node('AUDIT_EVENT', (event['id'], self.hashes[path]), path, props)
            self.reference(node, event['item_id'], path, 'RECORDS_EVENT_FOR',
                           version=event['item_version'], digest=event['content_sha256'])
            self.citations(node, event.get('evidence', []), path)

    def load_baselines(self):
        for file in _walk(self.root, 'relationships/requirement-code/baselines', {'.json'}):
            value = _decode(file)
            _baseline(value, file, self.root)
            path = file.relative_to(self.root).as_posix()
            baseline = value['baseline_id']
            artifacts, behaviors, links, canonical = {}, {}, {}, {}
            for row in _rows(value, 'artifacts', file):
                target = _safe(self.root, row.get('path'))
                if not isinstance(row.get('sha256'), str) or not _HASH.fullmatch(row['sha256']):
                    raise ValueError('Baseline artifacts need a SHA-256.')
                kind = {'INTENT': 'KNOWLEDGE_RECORD', 'CODE': 'CODE_ARTIFACT', 'TEST': 'TEST_ASSERTION', 'EXECUTION': 'EXECUTION'}.get(row.get('kind'))
                if kind is None:
                    raise ValueError('Unsupported baseline artifact kind.')
                status = 'MATCH' if self.hashes.get(row['path']) == row['sha256'] else 'MISMATCH' if target.is_file() else 'MISSING'
                props = {key: deepcopy(row[key]) for key in ('repository_id', 'revision', 'source_path', 'sha256') if key in row}
                props.update(record_id=row['id'], baseline_id=baseline, artifact_kind=row['kind'],
                             retained_path=row['path'], retained_status=status, record_sha256=_record_hash(row),
                             evidence_class='INSPECTED_IMPLEMENTATION' if row['kind'] == 'CODE' else 'DECLARED_METADATA')
                node = self.node(kind, (baseline, row['id'], _record_hash(row)), path, props)
                artifacts[row['id']] = (node, row)
                if status != 'MATCH':
                    self.unresolved(node, row['path'], path, 'Baseline retained artifact ' + status.lower(), expected_sha256=row['sha256'])
                elif row['kind'] == 'INTENT':
                    matches = [key for key, record_path in self.record_paths.items()
                               if record_path == row['path'] and self.hashes[record_path] == row['sha256']]
                    if len(matches) == 1:
                        canonical[row['id']] = matches[0]
                        self.edge(node, matches[0], 'SAME_RECORD_AS', path, binding='EXACT_FILE_HASH')
                        parent = self.graph.nodes[matches[0]]['properties']
                        self.graph.nodes[node]['properties'].update({key: parent[key] for key in ('governance_state', 'owner', 'version') if key in parent})
            for row in _rows(value, 'behaviors', file):
                if type(row.get('version')) is not int or row['version'] < 1:
                    raise ValueError('Behavior versions must be positive integers.')
                props = {key: deepcopy(row[key]) for key in ('version', 'criterion_id', 'state') if key in row}
                props.update(record_id=row['id'], baseline_id=baseline, record_sha256=_record_hash(row), evidence_class='DOCUMENTED_INTENT')
                node = self.node('BEHAVIOR', (baseline, row['id'], _record_hash(row)), path, props)
                behaviors[row['id']] = (node, row)
                intent = row.get('intent', {})
                target = artifacts.get(intent.get('artifact_id'))
                self.baseline_reference(node, target, intent.get('record_sha256'), path, 'DECLARES_INTENT',
                                        start_line=intent.get('start_line'), end_line=intent.get('end_line'))
                if target:
                    parent = self.graph.nodes[target[0]]['properties']
                    self.graph.nodes[node]['properties'].update({key: parent[key] for key in ('governance_state', 'owner') if key in parent})
                    canonical_record = canonical.get(intent.get('artifact_id'))
                    criterion = self.criteria.get((canonical_record, row.get('criterion_id')))
                    if criterion and intent.get('record_sha256') == _record_hash(target[1]):
                        self.edge(node, criterion, 'DECLARES_CRITERION', path, binding='EXACT_INTENT_RECORD')
            for row in _rows(value, 'links', file):
                if row.get('relationship') not in {'IMPLEMENTED_BY', 'ASSERTED_BY'} or row.get('grade') not in {'CONFIRMED', 'LIKELY', 'POSSIBLE', 'UNRESOLVED'}:
                    raise ValueError('Baseline links need supported relationship and grade values.')
                left, right = behaviors.get(row.get('behavior_id')), artifacts.get(row.get('artifact_id'))
                if not left or not right:
                    owner = left[0] if left else right[0] if right else self.node('UNRESOLVED_REFERENCE', (baseline, row['id']), path,
                                                                              {'record_id': row['id'], 'evidence_class': 'UNKNOWN'})
                    self.unresolved(owner, row['id'], path, 'Baseline link endpoint is missing')
                    continue
                props = {key: deepcopy(row[key]) for key in ('id', 'grade', 'start_line', 'end_line', 'behavior_record_sha256', 'artifact_record_sha256', 'limitations') if key in row}
                props.update(baseline_id=baseline, record_sha256=_record_hash(row),
                             binding_status='MATCH' if row.get('behavior_record_sha256') == _record_hash(left[1]) and row.get('artifact_record_sha256') == _record_hash(right[1]) else 'MISMATCH')
                if row['relationship'] == 'ASSERTED_BY':
                    if not isinstance(row.get('assertion'), str) or not row['assertion']:
                        raise ValueError('Assertion links need explicit assertion text.')
                    props['assertion_sha256'] = hashlib.sha256(row['assertion'].encode()).hexdigest()
                    inherited = {key: self.graph.nodes[left[0]]['properties'][key]
                                 for key in ('governance_state', 'owner') if key in self.graph.nodes[left[0]]['properties']}
                    assertion = self.node('TEST_ASSERTION', (baseline, row['id'], _record_hash(row)), path,
                                          {**inherited, 'record_id': row['id'], 'baseline_id': baseline,
                                           'record_sha256': _record_hash(row), 'assertion_sha256': props['assertion_sha256'],
                                           'assertion_kind': 'DECLARED_ASSERTION', 'grade': row['grade'],
                                           'evidence_class': 'DECLARED_METADATA'})
                    self.edge(assertion, right[0], 'LOCATED_IN', path,
                              start_line=row.get('start_line'), end_line=row.get('end_line'))
                    target_node = assertion
                else:
                    target_node = right[0]
                edge = self.edge(left[0], target_node, row['relationship'], path, **props)
                links[row['id']] = (edge, row, target_node)
                if props['binding_status'] != 'MATCH':
                    self.unresolved(left[0], row['id'], path, 'Baseline endpoint metadata hash changed')
            for row in _rows(value, 'executions', file):
                props = {key: deepcopy(row[key]) for key in ('mode', 'level', 'environment', 'limitations') if key in row}
                props.update(record_id=row['id'], baseline_id=baseline, record_sha256=_record_hash(row),
                             evidence_class='DECLARED_METADATA', outcome='UNKNOWN', business_verification='NOT_VERIFIED')
                node = self.node('EXECUTION', (baseline, row['id'], _record_hash(row)), path, props)
                artifact = artifacts.get(row.get('artifact_id'))
                self.baseline_reference(node, artifact, row.get('artifact_record_sha256'), path, 'RETAINS_RESULT')
                if artifact and self.graph.nodes[artifact[0]]['properties']['retained_status'] == 'MATCH':
                    result_path = _safe(self.root, artifact[1]['path'])
                    if result_path.suffix == '.json':
                        result = _decode(result_path)
                        outcome = result.get('status', 'UNKNOWN')
                        self.graph.nodes[node]['properties']['outcome'] = outcome if outcome in {'PASSED', 'FAILED', 'PARTIAL', 'BLOCKED'} else 'UNKNOWN'
                for code in row.get('code_artifact_ids', []):
                    if code in artifacts:
                        self.edge(node, artifacts[code][0], 'DECLARES_EXECUTED_CODE', path)
                    else:
                        self.unresolved(node, str(code), path, 'Execution code artifact is missing')
                for binding in row.get('assertion_bindings', []):
                    link = links.get(binding.get('link_id'))
                    if link:
                        self.edge(node, link[2], 'DECLARES_ASSERTION_BINDING', path,
                                  link_id=binding['link_id'],
                                  binding_status='MATCH' if binding.get('link_record_sha256') == _record_hash(link[1]) else 'MISMATCH')
                    else:
                        self.unresolved(node, str(binding.get('link_id')), path, 'Execution assertion link is missing')
            for row in _rows(value, 'findings', file):
                node = self.node('FINDING', (baseline, row['id'], _record_hash(row)), path,
                                 {'record_id': row['id'], 'baseline_id': baseline, 'evidence_class': 'DECLARED_METADATA',
                                  'record_sha256': _record_hash(row),
                                  'owner': row.get('owner', 'unknown'), 'category': row.get('kind', 'unknown')})
                behavior = behaviors.get(row.get('behavior_id'))
                if behavior:
                    self.edge(node, behavior[0], 'CONCERNS', path)

    def baseline_reference(self, owner, target, expected_hash, path, relationship, **properties):
        if target:
            self.edge(owner, target[0], relationship, path,
                      binding_status='MATCH' if expected_hash == _record_hash(target[1]) else 'MISMATCH',
                      expected_record_sha256=expected_hash, **properties)
        else:
            self.unresolved(owner, relationship, path, 'Baseline reference target is missing', relationship=relationship)

    def run(self):
        self.load_sources()
        self.load_catalogs()
        self.load_records()
        self.load_audits()
        self.load_baselines()
        counts = Counter(node['type'] for node in self.graph.nodes.values() if node.get('properties', {}).get('projection') == 'knowledge')
        self.graph.knowledge = {'schema_version': SCHEMA_VERSION, 'inputs': self.inputs,
                                'counts': {'nodes': sum(counts.values()), 'edges': sum(edge.get('dimension') == 'KNOWLEDGE' for edge in self.graph.edges.values()),
                                           **dict(sorted(counts.items())), 'input_files': len(self.inputs)},
                                'limitations': list(LIMITATIONS)}


def apply_knowledge(graph, census=None):
    """Append an atomic deterministic projection. Never edit canonical records."""
    inputs = input_fingerprints(graph.workspace)
    candidate = deepcopy(graph)
    previous = {key for key, node in candidate.nodes.items()
                if node.get('properties', {}).get('projection') == 'knowledge'}
    candidate.nodes = {key: node for key, node in candidate.nodes.items() if key not in previous}
    candidate.edges = {key: edge for key, edge in candidate.edges.items()
                       if edge.get('properties', {}).get('projection') != 'knowledge'
                       and edge['source'] not in previous and edge['target'] not in previous}
    candidate.evidence = {key: row for key, row in candidate.evidence.items()
                          if row.get('extractor') != 'knowledge-projection'}
    candidate.diagnostics = {key: row for key, row in candidate.diagnostics.items()
                            if not row.get('code', '').startswith('KNOWLEDGE_')}
    _Projection(candidate, inputs).run()
    if input_fingerprints(graph.workspace) != inputs:
        raise ValueError('Knowledge inputs changed during projection.')
    for field in ('nodes', 'edges', 'evidence', 'diagnostics', 'knowledge'):
        setattr(graph, field, getattr(candidate, field))
