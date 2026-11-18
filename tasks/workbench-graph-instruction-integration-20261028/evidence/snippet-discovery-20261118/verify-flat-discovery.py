"""Exercise the complete discovery bundle against an independent flat fixture."""
import hashlib
import json
from pathlib import Path
import runpy
import tempfile
from unittest.mock import patch

root = Path(__file__).resolve().parents[4]
load = runpy.run_path(str(root / '.agents/skills/service-dependencies-graph/tests/_support.py'))['load_tool']
generate = load('generate_all_graphs')
snapshot = load('snapshot')

with tempfile.TemporaryDirectory(prefix='graph-flat-holdout-') as temporary:
    workspace = Path(temporary)

    def write(relative, text):
        path = workspace / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    write('repos/services/deep/custom/worker.odd', '''package worker
import "net/http"
func settle() { gateway.Send(os.Getenv("ORDERS_URL")) }
var payment = "https://external.example/payments?secret=hidden-query"
''')
    write('repos/ui/package.json', '{"name":"@holdout/ui"}')
    write('repos/ui/src/index.ts', 'export const ready = true;')
    write('repos/ui/arbitrary/solace.custom', '''import solace from "solclientjs";
const destination = solace.SolclientFactory.createTopicDestination("orders/created");
session.send(message);
session.subscribe(destination);
''')
    deployment = write('repos/ui/.hidden/deploy.runtime', '''ORDERS_URL=https://orders.example/settle
SOLACE_HOST=smfs://broker.example:55443
SOLACE_VPN=operations
SOLACE_PASSWORD=never-retain-this-value
''')
    write('repos/provider/runtime/endpoints.extensionless', '''router.post("/settle", receive);
const destination = Queue.durableExclusiveQueue("orders.queue");
receiver.receiveAsync(handler);
''')
    write('repos/provider/contracts/orders.proto', '''syntax = "proto3";
service Orders { rpc Settle (Request) returns (Response); }
''')
    write('repos/provider/config/subscription', 'topic=orders/created\nqueue=orders.queue\nvpn=operations\n')
    write('repos/provider/node_modules/ignored/client', 'fetch("https://dependency.example")')
    (workspace / 'repos/provider/binary').write_bytes(b'\x00\x01')
    (workspace / 'repos/provider/large').write_bytes(b'x' * (2 * 1024 * 1024 + 1))
    (workspace / 'repos/provider/link').symlink_to(deployment)
    arguments = ['--workspace', str(workspace), '--repos', 'repos', '--layout', 'flat',
                 '--out', 'generated', '--no-context']
    assert generate.main(arguments) == 0
    output = workspace / 'generated'
    graph = json.loads((output / 'graph.json').read_bytes())
    audit = json.loads((output / 'coverage-declarations.json').read_bytes())
    coverage = snapshot.query(output, 'coverage', {}, workspace)
    assert coverage['freshness']['status'] == 'CURRENT'
    assert {row['name'] for row in coverage['coverage']['repositories']} == {'services', 'ui', 'provider'}
    rows = audit['pattern_candidates']
    assert any(row['family'] == 'CALL_HINT' and row['value'] == 'gateway.Send' for row in rows)
    assert any(row['value'] == 'https://external.example/payments' for row in rows)
    assert any(row['value'] == 'orders/created' for row in rows)
    assert any(row['value'] == 'orders.queue' for row in rows)
    assert any(row['family'] == 'RPC_INTERFACE' for row in rows)
    found = snapshot.query(output, 'patterns', {'service_only': True, 'include_snippets': True,
                                               'query': 'session.send'}, workspace)
    assert found['matching_total'] > 0
    generic = next(row for row in found['matches'] if row['family'] == 'CALL_HINT')
    assert generic['protocol_hints'] == []
    serialized = json.dumps(audit)
    assert 'never-retain-this-value' not in serialized and 'hidden-query' not in serialized
    reasons = audit['discovery_inventory']['summary']['skip_reasons']
    assert {'VENDORED_DEPENDENCY', 'BINARY_FILE', 'SOURCE_SIZE_LIMIT', 'SYMLINK_FILE'} <= set(reasons)
    assert not any(edge['relationship'] == 'REVIEWED_RELATIONSHIP' for edge in graph['edges'])
    assert not any(edge.get('resolution_status') == 'RESOLVED'
                   and graph_node['repository'] in {'repo:services', 'repo:provider'}
                   for edge in graph['edges'] for graph_node in graph['nodes']
                   if graph_node['id'] == edge['target'])
    original = deployment.read_text()
    deployment.write_text(original.replace('orders.example', 'others.example'))
    assert snapshot.query(output, 'coverage', {}, workspace)['freshness']['status'] == 'STALE'
    deployment.write_text(original)
    manifest_before = (output / 'manifest.json').read_bytes()
    original_run = generate.run
    mutated = False

    def change_after_extraction(*parts, **kwargs):
        global mutated
        original_run(*parts, **kwargs)
        if not mutated and 'build_graph' in parts:
            deployment.write_text(original.replace('orders.example', 'others.example'))
            mutated = True

    with patch.object(generate, 'run', side_effect=change_after_extraction):
        try:
            generate.main(arguments)
        except ValueError as error:
            assert 'changed during graph generation' in str(error)
        else:
            raise AssertionError('Changed source was published')
    assert (output / 'manifest.json').read_bytes() == manifest_before

result = {
    'status': 'PASSED', 'fixture': 'independent temporary flat repository parent',
    'repositories': ['services', 'ui', 'provider'],
    'checks': ['custom and hidden text collected', 'external HTTP authority retained',
               'Solace destination, queue, broker and generic publisher candidates available',
               'RPC contracts collected', 'no automatic provider joins', 'credential values redacted',
               'exclusions accounted', 'same-length hidden deployment edit marks snapshot stale',
               'source mutation prevents publication and preserves previous bundle'],
    'fixture_candidate_count': len(rows),
    'fixture_discovery_inventory': audit['discovery_inventory']['summary'],
    'preserved_manifest_sha256': hashlib.sha256(manifest_before).hexdigest(),
    'limits': ['Controlled fixture verifies discovery contracts, not live connectivity or universal semantic recall.'],
}
Path(__file__).with_name('flat-discovery.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
