"""Keep measured source accountability separate from semantic quality."""
from pathlib import Path
import hashlib
import json
import runpy
import tempfile
import unittest

load_tool = runpy.run_path(str(Path(__file__).with_name('_support.py')))['load_tool']
audit = load_tool('coverage_audit')
builder = load_tool('build_graph')
inventory = load_tool('repository_inventory').inventory
validator = load_tool('validate_graph')
snapshot = load_tool('snapshot')

class CoverageAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repos/service'
        self.repo.mkdir(parents=True)
        (self.repo / 'pom.xml').write_text('<project/>')

    def write(self, path, value):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(value)

    def test_source_gaps_errors_and_unknown_semantic_denominators_are_explicit(self):
        self.write('src/main/java/Broken.java', 'class Broken {')
        self.write('other/Missed.java', 'class Missed {}')
        graph = builder.Graph(self.root)
        rid = graph.add_repository(self.repo, 'SPRING', True)
        result = audit.build_audit(graph.document(), inventory(self.root, self.root / 'repos'), self.root, [])
        measures = result['repositories'][rid]
        self.assertEqual(measures['source_inventory']['rate'], 1)
        self.assertEqual(measures['source_gaps'], 1)
        self.assertEqual(measures['parse_coverage']['numerator'], 1)
        self.assertEqual(measures['parse_coverage']['denominator'], 2)
        self.assertEqual(measures['semantic_extraction_recall'], 'UNKNOWN')
        self.assertEqual(measures['reviewed_precision'], 'UNKNOWN')
        self.assertTrue(any(row['parse_status'] == 'ERROR' for row in result['files']))

    def test_markers_reconcile_locations_without_claiming_semantic_review(self):
        self.write('src/main/java/Order.java', '@Entity class Order { @Column String name; }')
        graph = builder.Graph(self.root)
        rid = graph.add_repository(self.repo, 'SPRING', True)
        ev = graph.add_evidence(rid, 'repos/service/src/main/java/Order.java', 1, 'Entity mapping', 'orm-entity')
        census = inventory(self.root, self.root / 'repos')
        rows = [{'repository': rid, 'family': 'ORM_ENTITY', 'path': 'repos/service/src/main/java/Order.java',
                 'line': 1, 'disposition': 'EXTRACTED', 'evidence': [ev]}]
        result = audit.build_audit(graph.document(), census, self.root, rows)
        markers = {row['family']: row for row in result['source_candidates']}
        self.assertEqual(markers['ORM_ENTITY']['accountability'], 'RECORDED')
        self.assertEqual(markers['ORM_ENTITY']['evidence'], [ev])
        self.assertEqual(markers['ORM_COLUMN']['accountability'], 'GAP')
        self.assertEqual(markers['ORM_ENTITY']['review_status'], 'PENDING')
        self.assertEqual(result['repositories'][rid]['marker_accountability']['rate'], .5)

    def test_new_projection_requires_detail_but_legacy_projection_remains_valid(self):
        graph = builder.Graph(self.root)
        graph.add_repository(self.repo, 'SPRING', True)
        document = graph.document()
        projection = builder.dependencies(graph)
        self.assertEqual(validator.validate_dependencies(projection, document), [])
        for groups in projection['repositories'].values():
            for key in ('configuration_keys', 'entities', 'columns', 'internal_dependencies', 'api_calls', 'orm_mappings'):
                groups.pop(key)
        self.assertTrue(validator.validate_dependencies(projection, document))
        document['generator']['version'] = '2.0.0'
        self.assertEqual(validator.validate_dependencies(projection, document), [])

    def test_build_retains_audit_and_snapshot_coverage_query_summary(self):
        self.write('src/main/java/Ready.java', 'class Ready {}')
        out = self.root / 'generated'
        builder.main(['--workspace', str(self.root), '--out', str(out)])
        result = json.loads((out / 'analysis-coverage.json').read_text())
        self.assertEqual(result['declaration_audit'], 'coverage-declarations.json')
        self.assertEqual(result['repositories'][0]['measures']['source_inventory']['rate'], 1)
        detail = json.loads((out / 'coverage-declarations.json').read_text())
        self.assertTrue(detail['files'])
        self.assertTrue(any(row['family'] == 'java_source_file' for row in detail['declarations']))

    def test_same_line_declarations_retain_all_evidence_and_sql_limits(self):
        self.write('src/main/java/Query.java', 'class Query {}')
        graph = builder.Graph(self.root)
        rid = graph.add_repository(self.repo, 'SPRING', True)
        path = 'repos/service/src/main/java/Query.java'
        ids = {graph.add_evidence(rid, path, 1, declaration, 'sql-column-reference')
               for declaration in ('References orders.id', 'References orders.total')}
        rows = [{'path': 'src/main/java/Query.java', 'line': 1, 'family': 'SQL',
                 'declaration': declaration, 'disposition': 'EXTRACTED',
                 'limitations': ['UNSUPPORTED_COMPLEX_SQL']}
                for declaration in ('Query one', 'Query two')]
        builder.retain_ledger(graph, self.repo, rid, rows)
        result = audit.build_audit(graph.document(), inventory(self.root, self.root / 'repos'),
                                   self.root, graph.declaration_ledger)
        canonical = [row for row in result['declarations'] if row['family'] == 'sql-column-reference']
        self.assertEqual({ev for row in canonical for ev in row['evidence']}, ids)
        declarations = [row for row in result['declarations'] if row['family'] == 'SQL']
        self.assertEqual(len(declarations), 2)
        self.assertTrue(all(row['limitations'] == ['UNSUPPORTED_COMPLEX_SQL'] for row in declarations))

    def test_scope_changes_change_extraction_fingerprints_without_source_changes(self):
        fingerprints = load_tool('repository_inventory').extraction_fingerprints
        original = {'repositories': [{'path': 'repos/service', 'content_sha256': 'unchanged',
                                     'kind': 'TESTING', 'primary_type': 'testing'}]}
        changed = json.loads(json.dumps(original))
        changed['repositories'][0].update(kind=None, primary_type='backend')
        self.assertNotEqual(fingerprints(original), fingerprints(changed))

    def test_manifest_requires_declared_audit_but_accepts_legacy_without_pointer(self):
        out = self.root / 'snapshot'
        out.mkdir()
        def bundle(pointer):
            payloads = {'graph.json': {}, 'analysis-coverage.json': pointer,
                        'repository-relationships.json': {}, 'services.json': {}}
            rows = []
            for name, value in payloads.items():
                content = json.dumps(value).encode()
                (out / name).write_bytes(content)
                rows.append({'path': name, 'sha256': hashlib.sha256(content).hexdigest()})
            (out / 'manifest.json').write_text(json.dumps({'generated_at': '2026-10-15T00:00:00Z',
                'canonical_graph': 'graph.json', 'graph_sha256': rows[0]['sha256'], 'artifacts': rows}))
        bundle({'declaration_audit': 'coverage-declarations.json'})
        with self.assertRaises(snapshot.SnapshotError):
            snapshot._bundle(out)
        bundle({})
        self.assertEqual(len(snapshot._bundle(out)[1]), 4)

if __name__ == '__main__':
    unittest.main()
