"""Keep broad text discovery independent from typed source extraction layouts."""
import hashlib
import json
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch

load_tool = runpy.run_path(str(Path(__file__).with_name('_support.py')))['load_tool']
discovery = load_tool('discovery_sources')
repository_inventory = load_tool('repository_inventory')
audit = load_tool('coverage_audit')
builder = load_tool('build_graph')


class DiscoverySourceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='graph-discovery-')
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.repo = self.workspace / 'repos/client'
        self.repo.mkdir(parents=True)

    def write(self, relative, text='fetch("https://external.example/api/orders");\n'):
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def test_text_inventory_includes_hidden_extensionless_tests_and_custom_generated_clients(self):
        paths = {'Dockerfile', '.github/workflows/deploy', '.settings/runtime.custom',
                 'tests/nested/client.odd', 'test/connection', 'generated/clients/service.custom',
                 'deep/arbitrary/layout/deployment/interfaces/no-extension', 'build/clients/custom',
                 'dist/handwritten/client', 'vendor/source/client', 'services/configuration'}
        for relative in paths:
            self.write(relative)
        result = discovery.discovery_inventory(self.repo)
        self.assertEqual({row['path'] for row in result['files'] if row['status'] == 'SCANNED'}, paths)
        self.assertEqual(result['summary']['scanned_files'], len(paths))
        self.assertEqual(result['summary']['skipped_entries'], 0)
        self.assertTrue(all(row['sha256'] == hashlib.sha256((self.repo / row['path']).read_bytes()).hexdigest()
                            for row in result['files']))
        self.assertEqual(result, discovery.discovery_inventory(self.repo))

    def test_binary_large_symlink_metadata_and_dependency_subtrees_have_explicit_reasons(self):
        (self.repo / 'image.bin').write_bytes(b'\x89PNG\x00\x01binary')
        (self.repo / 'large.custom').write_bytes(b'x' * (discovery.MAX_TEXT_BYTES + 1))
        self.write('.git/objects/metadata')
        self.write('node_modules/third-party/index.js')
        self.write('.venv/lib/python/library.py')
        self.write('__pycache__/cache.pyc')
        self.write('pom.xml', '<project/>')
        self.write('target/classes/generated.txt')
        source = self.write('source.custom')
        (self.repo / 'link-file').symlink_to(source)
        (self.repo / 'link-directory').symlink_to(self.repo / 'node_modules', target_is_directory=True)
        rows = {row['path']: row for row in discovery.discovery_inventory(self.repo)['files']}
        self.assertEqual({key: rows[key]['reason'] for key in rows if rows[key]['status'] == 'SKIPPED'}, {
            'image.bin': 'BINARY_FILE', 'large.custom': 'SOURCE_SIZE_LIMIT', '.git': 'GIT_METADATA',
            'node_modules': 'VENDORED_DEPENDENCY', '.venv': 'VENDORED_DEPENDENCY',
            '__pycache__': 'BUILD_ARTIFACT', 'target': 'BUILD_ARTIFACT',
            'link-file': 'SYMLINK_FILE', 'link-directory': 'SYMLINK_DIRECTORY'})
        self.assertTrue(rows['image.bin']['sha256'])
        self.assertFalse(any(path.startswith('.git/') or path.startswith('node_modules/') for path in rows))

    def test_common_unicode_and_legacy_text_encodings_are_scanned(self):
        content = 'url="https://external.example/api/orders"\n'
        (self.repo / 'unicode.custom').write_bytes(content.encode('utf-16'))
        (self.repo / 'legacy.custom').write_bytes(('caf\xe9\n' + content).encode('latin-1'))
        result = discovery.discovery_inventory(self.repo)
        self.assertEqual({row['status'] for row in result['files']}, {'SCANNED'})
        self.assertEqual(discovery.read_discovery_text(self.repo / 'unicode.custom'), content)

    def test_unreadable_files_keep_relative_identity_and_stat_fingerprint(self):
        path = self.write('restricted.custom')
        original_open = Path.open
        def guarded_open(current, *args, **kwargs):
            if current == path:
                raise PermissionError('external machine path must not leak')
            return original_open(current, *args, **kwargs)
        with patch.object(Path, 'open', guarded_open):
            first = discovery.discovery_inventory(self.repo)
            second = discovery.discovery_inventory(self.repo)
        self.assertEqual(first, second)
        row, = first['files']
        self.assertEqual((row['path'], row['reason']), ('restricted.custom', 'UNREADABLE_SOURCE'))
        self.assertIn('mtime_ns', row)
        self.assertNotIn(str(self.repo), json.dumps(first))
        self.assertNotIn('external machine path', json.dumps(first))

    def test_same_length_edits_outside_typed_boundary_change_extraction_fingerprints(self):
        self.write('package.json', '{"name":"@fixture/client"}')
        self.write('src/index.ts', 'export const ready = true;')
        files = [self.write('Dockerfile', 'FROM first\n'),
                 self.write('.github/workflows/deploy', 'uses: first\n'),
                 self.write('tests/configuration.unknown', 'host=first\n')]
        current = repository_inventory.inventory(self.workspace, self.workspace / 'repos')
        for path in files:
            with self.subTest(path=path):
                before = current
                path.write_text(path.read_text().replace('first', 'other'))
                current = repository_inventory.inventory(self.workspace, self.workspace / 'repos')
                self.assertEqual(before['repositories'][0]['content_sha256'], current['repositories'][0]['content_sha256'])
                self.assertNotEqual(repository_inventory.extraction_fingerprints(before), repository_inventory.extraction_fingerprints(current))
                self.assertEqual(repository_inventory.extraction_fingerprints(before, include_discovery=False),
                                 repository_inventory.extraction_fingerprints(current, include_discovery=False))

    def test_flat_roots_preserve_group_named_repositories_with_arbitrary_nested_files(self):
        for name in ('ui', 'services', 'deployment'):
            path = self.workspace / 'repos' / name / 'arbitrary/nested/runtime.custom'
            path.parent.mkdir(parents=True)
            path.write_text('endpoint=unknown')
        result = repository_inventory.inventory(self.workspace, self.workspace / 'repos', layout='flat')
        self.assertEqual({row['path'] for row in result['repositories']},
                         {'repos/client', 'repos/ui', 'repos/services', 'repos/deployment'})
        self.assertEqual(result['repository_layout'], 'flat')
        self.assertTrue(all(row['discovery_sha256'] for row in result['repositories']))
        with self.assertRaisesRegex(ValueError, 'layout'):
            repository_inventory.inventory(self.workspace, self.workspace / 'repos', layout='invalid')

    def test_audit_keeps_broad_discovery_separate_from_typed_inventory(self):
        self.write('package.json', '{"name":"@fixture/client"}')
        self.write('src/index.ts', 'export const ready = true;')
        self.write('.github/workflows/deploy')
        self.write('tests/custom/generated-client.extensionless')
        census = repository_inventory.inventory(self.workspace, self.workspace / 'repos')
        result = audit.build_audit(builder.Graph(self.workspace).document(), census, self.workspace, [])
        typed_paths = {row['path'] for row in result['files']}
        broad_paths = {row['path'] for row in result['discovery_inventory']['files']}
        self.assertNotIn('repos/client/.github/workflows/deploy', typed_paths)
        self.assertIn('repos/client/.github/workflows/deploy', broad_paths)
        self.assertIn('repos/client/tests/custom/generated-client.extensionless', broad_paths)
        self.assertEqual(result['discovery_inventory']['summary']['scanned_files'], 4)
        self.assertEqual(result['repositories']['repo:client']['discovery_inventory']['content_sha256'],
                         census['repositories'][0]['discovery_sha256'])

    def test_audit_rejects_temporary_source_revision_even_after_restoration(self):
        original = 'CALL_URL=https://alpha.example/orders\n'
        changed = 'CALL_URL=https://bravo.example/orders\n'
        source = self.write('custom/extensionless', original)
        census = repository_inventory.inventory(self.workspace, self.workspace / 'repos')
        scan_repository = audit.scan_repository

        def capture_changed_revision(*arguments):
            source.write_text(changed)
            try:
                return scan_repository(*arguments)
            finally:
                source.write_text(original)

        with patch.object(audit, 'scan_repository', side_effect=capture_changed_revision):
            with self.assertRaisesRegex(ValueError, 'DISCOVERY_SOURCE_CHANGED: repos/client'):
                audit.build_audit(builder.Graph(self.workspace).document(), census, self.workspace, [])
        self.assertEqual(source.read_text(), original)
        current = repository_inventory.inventory(self.workspace, self.workspace / 'repos')
        self.assertEqual(repository_inventory.extraction_fingerprints(census),
                         repository_inventory.extraction_fingerprints(current))


if __name__ == '__main__':
    unittest.main()
