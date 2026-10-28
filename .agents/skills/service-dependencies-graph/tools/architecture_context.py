"""Capture architecture seeds and evidence-backed investigation decisions."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator


DEFAULT_CONTEXT = 'relationships/service-dependencies/architecture-context.json'
APPLIED_CONTEXT = 'architecture-context.json'
PROVENANCE = 'architecture-context-provenance.json'
LIMITATIONS = [
    'USER_REPORTED architecture describes supplied intent. It does not verify runtime behavior or deployment.',
    'SOURCE_REVIEW evidence can explain agreement, conflicts, and limits. It does not promote supplied claims to source facts.',
    'Architecture annotations do not change canonical graph nodes, edges, or resolved repository links.',
    'Unbound subjects and OUT_OF_SCOPE subjects do not establish a discovered repository or provider.',
]
INVESTIGATION_LIMITATIONS = [
    'Initial instructions guide investigation. They do not establish source facts or runtime behavior.',
    'Investigation decisions retain source ranges, hashes, rationale, and explicit uncertainty within the canonical graph.',
    'SUPPORTED denotes reviewed static evidence. It does not establish deployment or passing execution.',
    'Unbound and OUT_OF_SCOPE subjects remain explicit boundaries, not discovered providers.',
]


def _object(properties, required=None):
    return {'type': 'object', 'properties': properties,
            'required': list(properties) if required is None else required, 'additionalProperties': False}


TEXT = {'type': 'string', 'minLength': 1, 'maxLength': 10000}
ID = {'type': 'string', 'pattern': r'^[A-Za-z][A-Za-z0-9_.:-]{0,127}$'}
REFS = {'type': 'array', 'items': ID, 'minItems': 1, 'maxItems': 128, 'uniqueItems': True}
SOURCE = _object({'id': ID, 'path': TEXT, 'sha256': {'type': 'string', 'pattern': r'^[0-9a-f]{64}$'},
                  'revision': TEXT, 'kind': {'enum': ['USER_CLARIFICATION', 'SOURCE_REVIEW']}})
LAYER = _object({'id': ID, 'label': TEXT, 'order': {'type': 'integer', 'minimum': 1, 'maximum': 1000},
                 'description': TEXT, 'source_ids': REFS})
SUBJECT = _object({'id': ID, 'repository': {'type': ['string', 'null'], 'pattern': r'^repo:.+'},
                   'label': TEXT, 'role': TEXT, 'layer_id': {'anyOf': [ID, {'type': 'null'}]},
                   'status': {'enum': ['USER_REPORTED', 'OUT_OF_SCOPE']},
                   'description': TEXT, 'source_ids': REFS})
SUBJECT['properties']['node_id'] = TEXT
RELATIONSHIP = _object({'id': ID, 'source': ID, 'target': ID, 'kind': TEXT,
                        'description': TEXT, 'source_ids': REFS})
NOTE = _object({'id': ID, 'subject_ids': {'type': 'array', 'items': ID, 'maxItems': 512, 'uniqueItems': True},
                'description': TEXT, 'source_ids': REFS})
SOURCE_REF = _object({'source_id': ID, 'line': {'type': 'integer', 'minimum': 1},
                      'end_line': {'type': 'integer', 'minimum': 1}})
INVESTIGATION = _object({
    'id': ID, 'relationship_id': ID,
    'status': {'enum': ['SUPPORTED', 'INFERRED', 'CONFLICTED', 'UNVERIFIED', 'OUT_OF_SCOPE']},
    'family': {'enum': ['api', 'data', 'shared', 'configuration', 'structure']},
    'rationale': TEXT,
    'source_refs': {'type': 'array', 'items': SOURCE_REF, 'maxItems': 128},
    'canonical_edge_ids': {'type': 'array', 'items': TEXT, 'maxItems': 128, 'uniqueItems': True},
})


def _array(items, maximum=512):
    return {'type': 'array', 'items': items, 'maxItems': maximum}


SCHEMA = _object({'schema_version': {'enum': ['1.0.0', '1.1.0']}, 'sources': {**_array(SOURCE, 128), 'minItems': 1},
                  'layers': _array(LAYER, 128), 'subjects': _array(SUBJECT),
                  'relationships': _array(RELATIONSHIP, 2048), 'notes': _array(NOTE)})
SCHEMA['properties']['investigations'] = _array(INVESTIGATION, 2048)
SCHEMA['allOf'] = [{
    'if': {'properties': {'schema_version': {'const': '1.1.0'}}},
    'then': {'required': ['investigations']},
    'else': {'not': {'required': ['investigations']}},
}]


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def relative_path(value: str) -> str:
    """Reject traversal and link ambiguity before resolving a workspace path."""
    path = PurePosixPath(value)
    if (not value or '\x00' in value or '\\' in value or ':' in value or
            path.is_absolute() or any(part in ('', '.', '..') for part in value.split('/'))):
        raise ValueError('Architecture context paths must be safe workspace-relative paths')
    return value


def workspace_file(workspace: Path, relative: str) -> Path:
    path = (workspace / relative_path(relative)).resolve()
    if not path.is_relative_to(workspace.resolve()) or not path.is_file():
        raise ValueError('Architecture context source is missing or outside the workspace: ' + relative)
    return path


def validate_document(document: dict, repository_ids: set[str] | None = None) -> None:
    errors = sorted(Draft202012Validator(SCHEMA).iter_errors(document), key=lambda error: str(error.path))
    if errors:
        raise ValueError('Invalid architecture context: ' + errors[0].message)
    identifiers = []
    for name in ('sources', 'layers', 'subjects', 'relationships', 'notes', 'investigations'):
        identifiers.extend(row['id'] for row in document.get(name, []))
    if len(identifiers) != len(set(identifiers)):
        raise ValueError('Architecture context IDs must be unique')
    source_ids = {row['id'] for row in document['sources']}
    layer_ids = {row['id'] for row in document['layers']}
    subject_ids = {row['id'] for row in document['subjects']}
    orders = [row['order'] for row in document['layers']]
    if len(orders) != len(set(orders)):
        raise ValueError('Architecture context layer orders must be unique')
    for source in document['sources']:
        relative_path(source['path'])
    for name in ('layers', 'subjects', 'relationships', 'notes'):
        for row in document[name]:
            if not set(row['source_ids']) <= source_ids:
                raise ValueError('Architecture context contains an unknown source reference: ' + row['id'])
    for row in document['subjects']:
        if row['layer_id'] is not None and row['layer_id'] not in layer_ids:
            raise ValueError('Architecture context contains an unknown layer reference: ' + row['id'])
        if repository_ids is not None and row['repository'] is not None and row['repository'] not in repository_ids:
            raise ValueError('Architecture context contains an unknown repository reference: ' + row['repository'])
    for row in document['relationships']:
        if row['source'] not in subject_ids or row['target'] not in subject_ids:
            raise ValueError('Architecture context contains an unknown subject reference: ' + row['id'])
    for row in document['notes']:
        if not set(row['subject_ids']) <= subject_ids:
            raise ValueError('Architecture context contains an unknown note subject reference: ' + row['id'])
    if document['schema_version'] == '1.1.0':
        relationships = {row['id'] for row in document['relationships']}
        reviewed = [row['relationship_id'] for row in document['investigations']]
        if len(reviewed) != len(set(reviewed)) or set(reviewed) != relationships:
            raise ValueError('Each architecture relationship requires exactly one investigation')
        sources = {row['id']: row for row in document['sources']}
        for row in document['investigations']:
            for ref in row['source_refs']:
                if ref['source_id'] not in sources:
                    raise ValueError('Investigation contains an unknown source reference: ' + row['id'])
                if ref['end_line'] < ref['line']:
                    raise ValueError('Investigation contains an invalid source range: ' + row['id'])
            if row['status'] == 'SUPPORTED' and not any(
                    sources[ref['source_id']]['kind'] == 'SOURCE_REVIEW' for ref in row['source_refs']):
                raise ValueError('SUPPORTED investigation requires SOURCE_REVIEW evidence: ' + row['id'])


def validate_source_ranges(document: dict, sources: dict[str, bytes]) -> None:
    for row in document.get('investigations', []):
        for ref in row['source_refs']:
            count = len(sources[ref['source_id']].splitlines())
            if ref['end_line'] > count:
                raise ValueError('Investigation source range exceeds captured bytes: ' + row['id'])


@dataclass
class ContextInput:
    document: dict
    path: str
    content: bytes
    sources: dict[str, bytes]

    def fingerprints(self) -> dict[str, str]:
        return {self.path: sha256(self.content), **{row['path']: row['sha256'] for row in self.document['sources']}}


def load_context(workspace: Path, path: Path, required=False) -> ContextInput | None:
    """Capture exact input and cited evidence bytes before generation."""
    workspace = workspace.resolve()
    supplied = path if path.is_absolute() else workspace / path
    try:
        relative = supplied.relative_to(workspace).as_posix()
    except ValueError:
        # Accept a filesystem alias for the workspace root without resolving input aliases inside it.
        roots = [parent for parent in supplied.parents if parent.resolve() == workspace]
        if not roots:
            raise ValueError('Architecture context must be inside the workspace') from None
        relative = supplied.relative_to(roots[0]).as_posix()
    relative_path(relative)
    resolved = supplied.resolve()
    if not resolved.is_relative_to(workspace):
        raise ValueError('Architecture context must be inside the workspace')
    if not supplied.exists() and not required:
        return None
    content = workspace_file(workspace, relative).read_bytes()
    document = json.loads(content)
    validate_document(document)
    sources = {}
    for row in document['sources']:
        source = workspace_file(workspace, row['path']).read_bytes()
        if sha256(source) != row['sha256']:
            raise ValueError('Architecture context source hash changed: ' + row['path'])
        sources[row['id']] = source
    validate_source_ranges(document, sources)
    return ContextInput(document, relative, content, sources)


def write_context(captured: ContextInput, candidate: Path, repository_ids: set[str]) -> None:
    validate_document(captured.document, repository_ids)
    (candidate / APPLIED_CONTEXT).write_bytes(captured.content)
    source_rows = []
    for index, row in enumerate(captured.document['sources']):
        relative = f'architecture-context-sources/{index:04d}.source'
        target = candidate / relative
        target.parent.mkdir(exist_ok=True)
        target.write_bytes(captured.sources[row['id']])
        source_rows.append({**row, 'snapshot_path': relative})
    integrated = captured.document['schema_version'] == '1.1.0'
    provenance = {'schema_version': captured.document['schema_version'], 'status': 'INVESTIGATED' if integrated else 'USER_REPORTED',
                  'input_path': captured.path, 'input_sha256': sha256(captured.content),
                  'sources': source_rows, 'limitations': INVESTIGATION_LIMITATIONS if integrated else LIMITATIONS}
    (candidate / PROVENANCE).write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def read_bundle_context(artifacts: dict[str, bytes], repository_ids: set[str]) -> dict | None:
    """Validate captured bytes without requiring the original workspace."""
    if not {APPLIED_CONTEXT, PROVENANCE} & artifacts.keys():
        return None
    if not {APPLIED_CONTEXT, PROVENANCE} <= artifacts.keys():
        raise ValueError('Architecture context bundle lacks its applied input or provenance')
    document = json.loads(artifacts[APPLIED_CONTEXT])
    validate_document(document, repository_ids)
    provenance = json.loads(artifacts[PROVENANCE])
    integrated = document['schema_version'] == '1.1.0'
    expected_status = 'INVESTIGATED' if integrated else 'USER_REPORTED'
    if (not isinstance(provenance, dict) or provenance.get('schema_version') != document['schema_version'] or
            provenance.get('status') != expected_status or provenance.get('input_sha256') != sha256(artifacts[APPLIED_CONTEXT]) or
            not isinstance(provenance.get('sources'), list) or
            provenance.get('limitations') != (INVESTIGATION_LIMITATIONS if integrated else LIMITATIONS)):
        raise ValueError('Invalid architecture context provenance')
    relative_path(provenance['input_path'])
    expected = document['sources']
    rows = provenance['sources']
    if len(expected) != len(rows):
        raise ValueError('Architecture context source provenance does not match applied input')
    paths = set()
    for source, saved in zip(expected, rows):
        if not isinstance(saved, dict) or {key: value for key, value in saved.items() if key != 'snapshot_path'} != source:
            raise ValueError('Architecture context source provenance does not match applied input')
        path = relative_path(saved['snapshot_path'])
        if not path.startswith('architecture-context-sources/') or path in paths:
            raise ValueError('Invalid architecture context source snapshot path')
        paths.add(path)
        if path not in artifacts or sha256(artifacts[path]) != source['sha256']:
            raise ValueError('Architecture context source snapshot hash changed: ' + source['id'])
    validate_source_ranges(document, {row['id']: artifacts[saved['snapshot_path']]
                                     for row, saved in zip(expected, rows)})
    return {'status': expected_status, 'document': document, 'provenance': provenance}


def candidate_context(candidate: Path, repository_ids: set[str]) -> dict | None:
    names = [APPLIED_CONTEXT, PROVENANCE]
    names.extend(path.relative_to(candidate).as_posix() for path in (candidate / 'architecture-context-sources').glob('*'))
    artifacts = {name: (candidate / name).read_bytes() for name in names if (candidate / name).is_file()}
    return read_bundle_context(artifacts, repository_ids)


def freshness(context: dict, workspace: Path) -> dict:
    """Compare live input and source bytes separately from canonical-source freshness."""
    provenance = context['provenance']
    expected = {provenance['input_path']: provenance['input_sha256']}
    expected.update({row['path']: row['sha256'] for row in provenance['sources']})
    changed = []
    for relative, checksum in expected.items():
        try:
            if sha256(workspace_file(workspace, relative).read_bytes()) == checksum:
                continue
        except (OSError, ValueError):
            pass
        changed.append(relative)
    return {'status': 'STALE' if changed else 'CURRENT', 'changed_paths': sorted(changed)}
