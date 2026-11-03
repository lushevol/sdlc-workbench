"""Protect knowledge navigation, provenance, and architecture isolation.

The shipped JavaScript executes in the existing minimal DOM harness.
These tests assert UI outcomes without an added browser dependency.
"""
from contextlib import redirect_stdout
from copy import deepcopy
import importlib.util
import io
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
load_tool = runpy.run_path(str(HERE / '_support.py'))['load_tool']
_spec = importlib.util.spec_from_file_location('_knowledge_viewer_fixture', HERE / 'test_graph_viewer.py')
_fixture_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_fixture_module)
graph_fixture = _fixture_module.graph_fixture


def knowledge_fixture():
    graph = graph_fixture()
    graph['knowledge'] = {'schema_version': '1.0.0', 'inputs': [{'path': 'knowledge/topic with space.md', 'sha256': 'a' * 64}],
                          'counts': {}, 'limitations': ['Declared links do not prove semantic support.']}
    for index in range(28):
        identifier = 'knowledge:record:' + str(index).zfill(2)
        graph['nodes'].append({'id': identifier, 'type': 'KNOWLEDGE_RECORD', 'name': 'Topic ' + str(index).zfill(2),
                               'repository': None, 'dimensions': ['KNOWLEDGE'], 'source_paths': ['knowledge/topic with space.md'],
                               'evidence': ['ev:knowledge'], 'assertion_status': 'CONFIRMED',
                               'properties': {'projection': 'knowledge', 'record_id': 'KT-' + str(index), 'version': 2,
                                              'record_type': 'KnowledgeTopic', 'owner': None, 'content_sha256': 'b' * 64,
                                              'governance_state': 'published' if index == 1 else 'candidate',
                                              'evidence_class': 'DOCUMENTED_INTENT'}})
    for index in range(36):
        identifier = 'knowledge:source:' + str(index).zfill(2)
        graph['nodes'].append({'id': identifier, 'type': 'SOURCE_REVISION', 'name': 'Source ' + str(index),
                               'repository': None, 'dimensions': ['KNOWLEDGE'], 'source_paths': [], 'evidence': ['ev:knowledge'],
                               'assertion_status': 'CONFIRMED', 'properties': {'projection': 'knowledge',
                               'revision': 'source-revision', 'sha256': 'c' * 64, 'snapshot_status': 'MATCH',
                               'snapshot': 'evidence/knowledge/source with space.md'}})
        graph['edges'].append({'id': 'knowledge:edge:' + str(index), 'source': 'knowledge:record:00', 'target': identifier,
                               'relationship': 'CITES_SOURCE', 'dimension': 'KNOWLEDGE', 'assertion_status': 'CONFIRMED',
                               'evidence': ['ev:knowledge'], 'properties': {'projection': 'knowledge', 'grade': 'UNRESOLVED',
                               'limitations': ['Claim support was not reviewed.']}})
    graph['edges'].append({'id': 'knowledge:related', 'source': 'knowledge:record:01', 'target': 'knowledge:record:00',
                           'relationship': 'RELATED_TO', 'dimension': 'KNOWLEDGE', 'evidence': ['ev:knowledge'],
                           'assertion_status': 'CONFIRMED', 'properties': {'projection': 'knowledge'}})
    graph['evidence'].append({'id': 'ev:knowledge', 'path': 'knowledge/topic with space.md', 'line': 4,
                              'declaration': 'Knowledge metadata declaration', 'extractor': 'knowledge-projection',
                              'repository': None})
    return graph


class KnowledgeViewerTests(unittest.TestCase):
    def run_viewer(self, graph, assertions):
        node = shutil.which('node')
        self.assertIsNotNone(node, 'Node.js is required for the shipped viewer interaction checks.')
        harness = (HERE / 'viewer_interactions.cjs').read_text(encoding='utf-8').split('if (process.argv[3] === "investigated")')[0]
        harness = harness.replace('    return null;', '''    if (selector === '[data-knowledge-node]' && this.dataset.knowledgeNode) return this;
    if (selector === '[data-knowledge-edge]' && this.dataset.knowledgeEdge) return this;
    return null;''')
        with tempfile.TemporaryDirectory(prefix='knowledge-viewer-') as temporary:
            root = Path(temporary)
            source, output, script = root / 'graph.json', root / 'viewer.html', root / 'check.cjs'
            source.write_text(json.dumps(graph), encoding='utf-8')
            with redirect_stdout(io.StringIO()):
                load_tool('render_graph').main([str(source), '--output', str(output)])
            script.write_text(harness + '\n' + assertions, encoding='utf-8')
            result = subprocess.run([node, str(script), str(output)], capture_output=True, text=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_knowledge_projection_never_changes_architecture_navigation(self):
        """Given knowledge declarations, architecture counts and trace metadata retain their original meaning."""
        base, extended = graph_fixture(), knowledge_fixture()
        before = deepcopy(extended)
        build = load_tool('viewer_model').build_viewer_model
        self.assertEqual(build(base), build(extended))
        self.assertEqual(extended, before)

    def test_focus_filters_and_pagination_retain_every_record_and_link(self):
        """Given more than one page, every declared ID remains reachable and candidates remain candidates."""
        self.run_viewer(knowledge_fixture(), r'''
assert.equal(elements.get('knowledge-workspace').hidden, false);
assert.equal(elements.get('viewer-workspace').hidden, true);
assert.match(elements.get('knowledge-records').innerHTML, /candidate/);
assert.match(elements.get('knowledge-detail').innerHTML, /bbbbbbbbbbbb/);
assert.match(elements.get('knowledge-detail').innerHTML, /Unknown/);
const seenRecords = new Set();
do {
  for (const match of elements.get('knowledge-records').innerHTML.matchAll(/data-knowledge-node="([^"]+)"/g)) seenRecords.add(match[1]);
  if(elements.get('knowledge-record-next').disabled)break;
  elements.get('knowledge-record-next').fire('click');
} while(true);
assert.equal(seenRecords.size, 28);
const seenEdges = new Set();
do {
  for (const match of elements.get('knowledge-edges').innerHTML.matchAll(/data-knowledge-edge="([^"]+)"/g)) seenEdges.add(match[1]);
  if(elements.get('knowledge-edge-next').disabled)break;
  elements.get('knowledge-edge-next').fire('click');
} while(true);
assert.equal(seenEdges.size, 37);
const graphEdges = new Set();
do {
  for(const edge of evaluate('knowledgeIncidentEdges().slice(knowledgeGraphPage*knowledgeNeighborPageSize,(knowledgeGraphPage+1)*knowledgeNeighborPageSize)')) graphEdges.add(edge.id);
  if(elements.get('knowledge-graph-next').disabled)break;
  elements.get('knowledge-graph-next').fire('click');
} while(true);
assert.deepEqual([...seenEdges].sort(), [...graphEdges].sort());
set('knowledge-state', 'published');
assert.equal(evaluate('knowledgeFilteredNodes().length'),1);
assert.equal(evaluate('knowledgeFocus'),'knowledge:record:01');
assert.equal(evaluate('knowledgeIncidentEdges().length'),0);
set('knowledge-state','all');
set('knowledge-search','KT-27','input');
assert.equal(evaluate('knowledgeFocus'),'knowledge:record:27');
assert.match(elements.get('knowledge-records').innerHTML,/Topic 27/);
elements.get('architecture-tab').fire('click');
assert.equal(elements.get('viewer-workspace').hidden,false);
assert.equal(elements.get('knowledge-workspace').hidden,true);
assert(!evaluate('matchingNodes.map(node=>node.id)').some(id=>id.startsWith('knowledge:')));
console.log('Knowledge pagination, review filtering, focus, and architecture isolation passed.');
''')

    def test_untrusted_titles_and_sources_cannot_create_active_markup_or_unsafe_links(self):
        """Given hostile source text, rendered labels escape markup and source links reject unsafe schemes."""
        graph = knowledge_fixture()
        record = next(node for node in graph['nodes'] if node['id'] == 'knowledge:record:00')
        record['name'] = '<img src=x onerror="alert(1)"> __GRAPH__'
        record['source_paths'] += ['javascript:alert(1)', '../private/file.md', '//host/path']
        graph['knowledge']['limitations'] += ['</script><script>unsafe()</script>']
        self.run_viewer(graph, r'''
vm.runInContext("knowledgeFocusNode('knowledge:record:00')",context);
assert(!elements.get('knowledge-detail').innerHTML.includes('<img'));
assert.match(elements.get('knowledge-detail').innerHTML,/&lt;img/);
assert(!elements.get('knowledge-detail').innerHTML.includes('href="javascript:'));
assert(!elements.get('knowledge-detail').innerHTML.includes('href="../private'));
assert.match(elements.get('knowledge-detail').innerHTML,/knowledge\/topic%20with%20space.md/);
assert.equal(evaluate("knowledgeHref('javascript:alert(1)')"),null);
assert.equal(evaluate("knowledgeHref('data:text/html,unsafe')"),null);
assert.equal(evaluate("knowledgeHref('//untrusted/path')"),null);
assert.equal(evaluate("knowledgeHref('../private/file')"),null);
assert.equal(evaluate("knowledgeHref('https://example.com/source')"),'https://example.com/source');
vm.runInContext("knowledgeSelection={kind:'edge',id:'knowledge:edge:0'};renderKnowledgeDetail()",context);
assert.match(elements.get('knowledge-detail').innerHTML,/Semantic assessment<\/strong>UNRESOLVED/);
assert.match(elements.get('knowledge-detail').innerHTML,/Declaration status<\/strong>CONFIRMED/);
assert.match(elements.get('knowledge-detail').innerHTML,/does not prove semantic support/);
assert.match(elements.get('knowledge-limits').innerHTML,/&lt;\/script&gt;/);
vm.runInContext("knowledgeFocusNode('knowledge:source:00')",context);
assert.match(elements.get('knowledge-detail').innerHTML,/source%20with%20space.md/);
assert.match(elements.get('knowledge-detail').innerHTML,/Snapshot integrity<\/strong>MATCH/);
assert.match(elements.get('knowledge-detail').innerHTML,/Backlinks · 1/);
console.log('Knowledge escaping, safe sources, evidence grades, and source backlinks passed.');
''')

    def test_empty_and_legacy_snapshots_remain_navigable(self):
        """Given no knowledge records, the empty projection explains itself and legacy architecture still opens."""
        graph = graph_fixture()
        self.run_viewer(graph, r'''
assert.equal(elements.get('explorer-tabs').hidden,true);
assert.equal(elements.get('viewer-workspace').hidden,false);
console.log('Legacy snapshot remains architecture-first.');
''')
        graph['knowledge'] = {'schema_version':'1.0.0','inputs':[],'counts':{},'limitations':[]}
        self.run_viewer(graph, r'''
assert.equal(elements.get('explorer-tabs').hidden,false);
assert.equal(elements.get('knowledge-workspace').hidden,false);
assert.match(elements.get('knowledge-focus-title').textContent,/No knowledge records/);
assert.equal(elements.get('knowledge-record-next').disabled,true);
assert.match(elements.get('knowledge-diagram').innerHTML,/no knowledge records/);
console.log('Empty knowledge projection stays usable.');
''')


if __name__ == '__main__':
    unittest.main()
