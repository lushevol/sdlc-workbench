"""Protect supplied architecture evidence without promoting it to extracted facts."""
from contextlib import redirect_stdout
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

load_tool = runpy.run_path(str(Path(__file__).with_name('_support.py')))['load_tool']
context_tool = load_tool('architecture_context')
generation = load_tool('generate_all_graphs')
snapshot = load_tool('snapshot')


def supplied_context(root):
    source = root / 'evidence/architecture-clarification.txt'
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text('The shell loads the tile through supplied routes.\n', encoding='utf-8')
    sources = [{'id': 'source:owner', 'path': source.relative_to(root).as_posix(),
                'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                'revision': 'owner-clarification-2026-10-22', 'kind': 'USER_CLARIFICATION'}]
    layers = [{'id': f'layer:{name}', 'label': name.title(), 'order': index,
               'description': f'Supplied {name} responsibility.', 'source_ids': ['source:owner']}
              for index, name in enumerate(('root', 'shell', 'container', 'tile'), 1)]
    subjects = [{'id': 'subject:shell', 'repository': 'repo:client', 'label': 'Portal shell',
                 'role': 'SHELL', 'layer_id': 'layer:shell', 'status': 'USER_REPORTED',
                 'description': 'The shell loads features.', 'source_ids': ['source:owner']},
                {'id': 'subject:tile', 'repository': None, 'label': 'Remote tile',
                 'role': 'TILE', 'layer_id': 'layer:tile', 'status': 'OUT_OF_SCOPE',
                 'description': 'The tile source is absent.', 'source_ids': ['source:owner']}]
    document = {'schema_version': '1.0.0', 'sources': sources, 'layers': layers, 'subjects': subjects,
                'relationships': [{'id': 'relationship:load', 'source': 'subject:shell', 'target': 'subject:tile',
                                   'kind': 'LOADS_REMOTE_UI', 'description': 'Supplied route and loading responsibility.',
                                   'source_ids': ['source:owner']}],
                'notes': [{'id': 'note:scope', 'subject_ids': ['subject:tile'],
                           'description': 'Runtime routing remains unverified.', 'source_ids': ['source:owner']}]}
    path = root / context_tool.DEFAULT_CONTEXT
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2) + '\n', encoding='utf-8')
    return document, path, source


class ArchitectureContextTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='graph-architecture-context-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def test_invalid_schema_references_duplicates_and_unsafe_sources_are_rejected(self):
        """Given invalid context, when validation runs, then each unsupported input raises ValueError."""
        document, _, _ = supplied_context(self.root)
        bad = []
        def change(name, mutate):
            row = deepcopy(document)
            mutate(row)
            bad.append((name, row))
        change('version', lambda row: row.update(schema_version='9.0.0'))
        change('unsupported field', lambda row: row.update(runtime_verified=True))
        change('duplicate id', lambda row: row['subjects'].append(deepcopy(row['subjects'][0])))
        change('duplicate layer order', lambda row: row['layers'][1].update(order=1))
        change('unknown source', lambda row: row['subjects'][0].update(source_ids=['source:unknown']))
        change('unknown layer', lambda row: row['subjects'][0].update(layer_id='layer:unknown'))
        change('unknown repository', lambda row: row['subjects'][0].update(repository='repo:unknown'))
        change('unknown target', lambda row: row['relationships'][0].update(target='subject:unknown'))
        change('unknown note subject', lambda row: row['notes'][0].update(subject_ids=['subject:unknown']))
        change('traversal', lambda row: row['sources'][0].update(path='../outside.txt'))
        change('absolute source', lambda row: row['sources'][0].update(path='/private/tmp/outside.txt'))
        change('windows source', lambda row: row['sources'][0].update(path='C:\\outside.txt'))
        for name, payload in bad:
            with self.subTest(name=name), self.assertRaises(ValueError):
                context_tool.validate_document(payload, {'repo:client'})

    def test_changed_source_hash_and_symlink_escape_are_rejected(self):
        """Given changed or escaped evidence, when capture runs, then generation rejects its source identity."""
        document, path, source = supplied_context(self.root)
        source.write_bytes(b'Changed clarification')
        with self.assertRaisesRegex(ValueError, 'source hash changed'):
            context_tool.load_context(self.root, path)
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / 'source'
            target.write_bytes(b'External source')
            source.unlink()
            source.symlink_to(target)
            document['sources'][0]['sha256'] = hashlib.sha256(target.read_bytes()).hexdigest()
            path.write_text(json.dumps(document), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'outside the workspace'):
                context_tool.load_context(self.root, path)

    def test_saved_bundle_validates_source_bytes_after_original_workspace_disappears(self):
        """Given captured evidence, when originals disappear, then saved bytes work and tampering raises ValueError."""
        document, path, source = supplied_context(self.root)
        captured = context_tool.load_context(self.root, path)
        candidate = self.root / 'bundle'
        candidate.mkdir()
        context_tool.write_context(captured, candidate, {'repo:client'})
        path.unlink()
        source.unlink()
        saved = context_tool.candidate_context(candidate, {'repo:client'})
        self.assertEqual(saved['document'], document)
        self.assertEqual(context_tool.freshness(saved, self.root)['status'], 'STALE')
        evidence = next((candidate / 'architecture-context-sources').iterdir())
        evidence.write_bytes(b'Changed saved source')
        with self.assertRaisesRegex(ValueError, 'snapshot hash changed'):
            context_tool.candidate_context(candidate, {'repo:client'})

    def test_source_change_during_generation_preserves_published_bundle(self):
        """Given a published bundle, when evidence changes during generation, then publication fails and preserves every byte."""
        _, path, source = supplied_context(self.root)
        self._repository()
        output = self.root / 'generated'
        with redirect_stdout(io.StringIO()):
            generation.main(['--workspace', str(self.root), '--out', str(output)])
        before = {item.relative_to(output): item.read_bytes() for item in output.rglob('*') if item.is_file()}
        original_run = generation.run
        def mutate_after_validation(*parts, **kwargs):
            original_run(*parts, **kwargs)
            if 'validate_graph' in parts:
                source.write_bytes(b'Changed during generation')
        with patch.object(generation, 'run', side_effect=mutate_after_validation), redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(ValueError, 'source hash changed'):
                generation.main(['--workspace', str(self.root), '--out', str(output)])
        self.assertTrue(path.is_file())
        self.assertEqual(before, {item.relative_to(output): item.read_bytes() for item in output.rglob('*') if item.is_file()})

    def _repository(self):
        repository = self.root / 'repos/ui/client'
        (repository / 'src').mkdir(parents=True)
        (repository / 'package.json').write_text('{"name":"@fixture/client"}', encoding='utf-8')
        (repository / 'src/index.ts').write_text("fetch('/orders');\n", encoding='utf-8')

    def test_input_symlink_retarget_makes_freshness_stale(self):
        """Given a captured input alias, when its target changes, then freshness reports that alias as STALE."""
        document, path, _ = supplied_context(self.root)
        first = path.with_name('first.json')
        second = path.with_name('second.json')
        path.rename(first)
        document['notes'][0]['description'] = 'Changed routing explanation.'
        second.write_text(json.dumps(document), encoding='utf-8')
        path.symlink_to(first.name)
        captured = context_tool.load_context(self.root, path)
        self.assertEqual(captured.path, path.relative_to(self.root).as_posix())
        output = self.root / 'bundle'
        output.mkdir()
        context_tool.write_context(captured, output, {'repo:client'})
        saved = context_tool.candidate_context(output, {'repo:client'})
        self.assertEqual(context_tool.freshness(saved, self.root)['status'], 'CURRENT')
        path.unlink()
        path.symlink_to(second.name)
        current = context_tool.freshness(saved, self.root)
        self.assertEqual(current['status'], 'STALE')
        self.assertEqual(current['changed_paths'], [path.relative_to(self.root).as_posix()])
        self.assertNotEqual(captured.fingerprints(), context_tool.load_context(self.root, path).fingerprints())

    def test_copied_skill_build_query_freshness_view_and_tamper_without_canonical_promotion(self):
        """Given a copied skill, when supplied context changes, then facts stay unchanged and freshness detects changed evidence."""
        self._repository()
        skill = self.root / '.agents/skills/service-dependencies-graph'
        shutil.copytree(Path(__file__).resolve().parents[1], skill,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        runner = skill / 'scripts/graph.py'
        def command(*arguments):
            result = subprocess.run([sys.executable, str(runner), '--workspace', str(self.root), *arguments],
                                    cwd=self.root.parent, capture_output=True, text=True, timeout=45)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            return result
        command('build', '--out', 'generated')
        output = self.root / 'generated'
        graph_before = json.loads((output / 'graph.json').read_bytes())
        links_before = load_tool('viewer_model').build_viewer_model(graph_before)['system_links']
        document, path, source = supplied_context(self.root)
        # Text supplied by users must remain inert inside the embedded JSON and rendered HTML.
        document['subjects'][0]['description'] = '</script><script>unsafe()</script>'
        path.write_text(json.dumps(document), encoding='utf-8')
        command('build', '--out', 'generated')
        graph_after = json.loads((output / 'graph.json').read_bytes())
        for key in ('nodes', 'edges', 'evidence'):
            self.assertEqual(graph_before[key], graph_after[key])
        self.assertEqual(links_before, load_tool('viewer_model').build_viewer_model(graph_after)['system_links'])
        self.assertEqual((output / context_tool.APPLIED_CONTEXT).read_bytes(), path.read_bytes())
        manifest = json.loads((output / 'manifest.json').read_bytes())
        self.assertEqual(manifest['architecture_context']['status'], 'USER_REPORTED')
        self.assertIn('architecture-context-sources/0000.source', {row['path'] for row in manifest['artifacts']})
        viewer = (output / 'relationship-viewer.html').read_text(encoding='utf-8')
        self.assertIn('User-reported architecture', viewer)
        self.assertIn('architecture-context-data', viewer)
        self.assertNotIn('</script><script>unsafe()', viewer)
        queried = json.loads(command('query', '--data-dir', 'generated', 'coverage').stdout)
        self.assertEqual(queried['architecture_context']['document'], document)
        self.assertEqual(queried['freshness']['status'], 'CURRENT')
        node = shutil.which('node')
        if node:
            result = subprocess.run([node, str(skill / 'tests/viewer_interactions.cjs'),
                                     str(output / 'relationship-viewer.html'), 'user-context'],
                                    capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        source.write_bytes(b'Clarification changed after the build')
        stale = json.loads(command('query', '--data-dir', 'generated', 'coverage').stdout)
        self.assertEqual(stale['architecture_context']['freshness']['status'], 'STALE')
        self.assertEqual(stale['freshness']['status'], 'STALE')
        self.assertIn(source.relative_to(self.root).as_posix(), stale['freshness']['changed_paths'])
        # Query saved bytes through the copied skill even after the input document changes.
        path.write_bytes(b'{}')
        self.assertEqual(json.loads(command('query', '--data-dir', 'generated', 'coverage').stdout)
                         ['architecture_context']['document'], document)
        (output / 'architecture-context-sources/0000.source').write_bytes(b'Tampered bundle')
        rejected = subprocess.run([sys.executable, str(runner), '--workspace', str(self.root),
                                   'query', '--data-dir', 'generated', 'coverage'],
                                  capture_output=True, text=True, timeout=15)
        self.assertEqual(rejected.returncode, 1)
        self.assertEqual(json.loads(rejected.stdout)['code'], 'INVALID_SNAPSHOT')


if __name__ == '__main__':
    unittest.main()
