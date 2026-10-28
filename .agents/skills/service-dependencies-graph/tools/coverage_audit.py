"""Keep source discovery, extraction dispositions, and semantic review separate."""
from __future__ import annotations

import ast
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import warnings

from tree_sitter import Language, Parser
import tree_sitter_java
import tree_sitter_typescript

from .source_inventory import iter_source_files, java_source_roots
from .extract_pattern_candidates import scan_repository


def _rate(numerator, denominator):
    return {'numerator': numerator, 'denominator': denominator,
            'rate': round(numerator / denominator, 6) if denominator else 'N/A'}


def _walk(node):
    yield node
    for child in node.named_children:
        yield from _walk(child)


def build_audit(document: dict, census: dict, workspace: Path, ledger: list[dict]) -> dict:
    files, candidates = [], []
    pattern_candidates = []
    pattern_skipped = []
    pattern_scanned = 0
    for repository in census['repositories']:
        repo = workspace / repository['path']
        if not repo.is_dir():
            continue
        patterns = scan_repository(workspace, 'repo:' + repository['name'], repo)
        pattern_scanned += patterns['scanned_files']
        pattern_skipped.extend(patterns['skipped_files'])
        pattern_candidates.extend(patterns['candidates'])
        roots = java_source_roots(repo) if repository['kind'] == 'SPRING' else []
        for path in iter_source_files(repo):
            relative = path.relative_to(workspace).as_posix()
            raw = path.read_bytes()
            record = {'repository': 'repo:' + repository['name'], 'path': relative,
                      'sha256': hashlib.sha256(raw).hexdigest(), 'disposition': 'INVENTORIED',
                      'parse_status': 'NOT_APPLICABLE', 'semantic_review': 'PENDING'}
            language = None
            if path.suffix == '.java':
                language = tree_sitter_java.language()
                included = any(path.is_relative_to(root) for root in roots)
                record['disposition'] = 'PARSED_SOURCE' if included else 'GAP'
                if not included:
                    record['reason'] = 'Java file is outside supported declared source roots'
            elif path.suffix in {'.ts', '.tsx', '.js', '.jsx'} and repository['kind'] == 'WEB':
                language = (tree_sitter_typescript.language_tsx() if path.suffix in {'.tsx', '.jsx'}
                            else tree_sitter_typescript.language_typescript())
                record['disposition'] = 'PARSED_SOURCE'
            elif repository['kind'] is None:
                record.update(disposition='GAP', reason='Repository stack has inventory-only coverage')
            elif path.suffix == '.py' and repository['kind'] == 'TESTING':
                record['disposition'] = 'PARSED_SOURCE'
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter('ignore', SyntaxWarning)
                        ast.parse(raw)
                    record['parse_status'] = 'PARSED'
                except (SyntaxError, ValueError):
                    record.update(parse_status='ERROR', reason='Python source parse failed')
            if language is not None:
                tree = Parser(Language(language)).parse(raw)
                record['parse_status'] = 'ERROR' if tree.root_node.has_error else 'PARSED'
                if tree.root_node.has_error:
                    record['reason'] = 'Source parse contains errors; retained declarations can be partial'
                if path.suffix == '.java' and record['disposition'] == 'PARSED_SOURCE':
                    # Independent broad markers are audit candidates. They do
                    # not assert receiver identity, semantic recall, or intent.
                    for node in _walk(tree.root_node):
                        family = None
                        if node.type in {'annotation', 'marker_annotation'}:
                            name = node.child_by_field_name('name')
                            annotation = raw[name.start_byte:name.end_byte].decode('utf-8') if name else ''
                            family = {'Column': 'ORM_COLUMN', 'Entity': 'ORM_ENTITY',
                                      'ConfigurationProperties': 'configuration_class'}.get(annotation.rsplit('.', 1)[-1])
                        if family:
                            candidates.append({'repository': record['repository'], 'path': relative,
                                               'line': node.start_point.row + 1, 'family': family,
                                               'review_status': 'PENDING', 'basis': 'independent-source-marker'})
            files.append(record)
    retained = []
    seen = set()
    for row in ledger:
        identity = row.get('declaration_id') or hashlib.sha256(json.dumps(row, sort_keys=True).encode()).hexdigest()
        key = ('ledger', identity)
        if key in seen:
            continue
        seen.add(key)
        retained.append({**row, 'declaration_id': identity, 'semantic_review': 'PENDING'})
    # Preserve canonical declarations from legacy extractors as dispositions.
    for row in document['evidence']:
        key = ('canonical_evidence', row['id'])
        if key in seen:
            continue
        seen.add(key)
        retained.append({'repository': row['repository'], 'family': row['extractor'], 'path': row['path'],
                         'line': row['line'], 'disposition': 'EXTRACTED', 'evidence': [row['id']],
                         'semantic_review': 'PENDING'})
    families = defaultdict(Counter)
    for row in retained:
        row['owner'] = 'UNKNOWN'
        row['next_action'] = ('Review source semantics and canonical evidence' if row['disposition'] == 'EXTRACTED'
                              else 'Inspect source and resolve the recorded extraction limit')
        families[row['family']][row['disposition']] += 1
    # A marker is a separate audit candidate. Location matches establish only
    # accountability, never correctness of the represented declaration.
    for row in candidates:
        matches = [item for item in retained if all(item.get(key) == row[key]
                   for key in ('repository', 'path', 'line', 'family'))]
        row['accountability'] = 'RECORDED' if matches else 'GAP'
        row['dispositions'] = sorted({item['disposition'] for item in matches})
        row['evidence'] = sorted({ev for item in matches for ev in item.get('evidence', [])})
    pattern_families = defaultdict(Counter)
    canonical_extractors = defaultdict(set)
    for item in document['evidence']:
        canonical_extractors[(item.get('repository'), item.get('path'), item.get('line'))].add(item.get('extractor'))
    family_extractors = {
        'HTTP_ENDPOINT': {'web-rest', 'java-http-client', 'spring-rest', 'nginx-route', 'web-graphql', 'web-graphql-operation',
                          'web-rtk-api-base-query', 'web-websocket'},
        'CONFIG_READ': {'java-configuration', 'configuration-source', 'reads-config'},
        'MESSAGE_CHANNEL': {'java-kafka-client', 'java-kafka-helper', 'camel-route'},
        'DATABASE_TABLE': {'java-database-client', 'orm-entity', 'orm-column', 'sql-column-reference'},
        'MODULE_IMPORT': {'web-module-import', 'web-source-import', 'web-graphql-document-import', 'npm-dependency', 'maven-dependency',
                          'systemjs-import', 'systemjs-import-map'},
        'GATEWAY_ROUTE': {'nginx-route', 'nginx-template', 'spring-open-api-route'},
        'GRAPHQL_SCHEMA': {'graphql-schema', 'web-graphql-document'},
    }
    for row in pattern_candidates:
        extractors = canonical_extractors.get((row['repository'], row['path'], row['line']), set())
        expected = family_extractors.get(row['family'], set())
        row['accountability'] = 'RECORDED' if extractors & expected else 'REVIEW_REQUIRED'
        row['matched_extractors'] = sorted(extractors & expected)
        pattern_families[row['family']][row['accountability']] += 1
    by_repo = {}
    for repo in census['repositories']:
        rid = 'repo:' + repo['name']
        selected = [r for r in files if r['repository'] == rid]
        parsable = [r for r in selected if r['parse_status'] != 'NOT_APPLICABLE']
        markers = [r for r in candidates if r['repository'] == rid]
        by_repo[rid] = {
            'source_inventory': _rate(len(selected), repo['source_files']),
            'parse_coverage': _rate(sum(r['parse_status'] == 'PARSED' for r in parsable), len(parsable)),
            'source_gaps': sum(r['disposition'] == 'GAP' for r in selected),
            'independent_marker_candidates': dict(sorted(Counter(r['family'] for r in markers).items())),
            'marker_accountability': _rate(sum(r['accountability'] == 'RECORDED' for r in markers), len(markers)),
            'semantic_extraction_recall': 'UNKNOWN', 'reviewed_precision': 'UNKNOWN',
            'reason': 'Independent marker candidates still require semantic source review',
        }
        selected_patterns = [row for row in pattern_candidates if row['repository'] == rid]
        by_repo[rid]['pattern_candidates'] = dict(sorted(Counter(row['family'] for row in selected_patterns).items()))
        by_repo[rid]['pattern_accountability'] = dict(sorted(Counter(row['accountability'] for row in selected_patterns).items()))
    return {'schema_version': '1.0.0', 'generated_at': document['generated_at'],
            'canonical_graph': 'graph.json', 'files': sorted(files, key=lambda r: r['path']),
            'declarations': sorted(retained, key=lambda r: (str(r.get('repository')), r['path'], r['line'], r['family'])),
            'source_candidates': candidates, 'pattern_candidates': pattern_candidates,
            'pattern_summary': {'scanned_files': pattern_scanned,
                                'skipped_files': sorted(pattern_skipped, key=lambda row: row['path']),
                                'families': {key: dict(sorted(value.items())) for key, value in sorted(pattern_families.items())}},
            'repositories': by_repo,
            'families': {key: dict(sorted(value.items())) for key, value in sorted(families.items())},
            'limitations': ['Source markers and evidence counts do not establish semantic coverage.',
                           'Semantic rates remain UNKNOWN until an independent source review supplies denominators.',
                           'A gap disposition does not count as successful extraction.',
                           'Pattern candidates use high-recall search and require source review before canonical promotion.',
                           'Static declarations do not establish production execution.']}
