"""Write bounded local-script chunks without embedding canonical evidence in HTML."""
from __future__ import annotations

from collections import defaultdict
import hashlib
import base64
import gzip
import json
import tempfile
from pathlib import Path

from .viewer_model import build_viewer_model
from .viewer_traces import build_trace_model

CHUNK_BYTES = 192 * 1024
NEIGHBORHOOD_SIZE = 12


def script_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('<', r'\u003c')


def write_bundle(graph: dict, output: Path, context: dict | None, source_prefix: str) -> dict:
    """Each canonical record is stored once; summaries support progressive navigation."""
    folder = output.with_suffix('.data')
    if folder.is_symlink():
        raise ValueError('Viewer data must not be a symbolic link')
    folder.mkdir(parents=True, exist_ok=True)
    model = build_viewer_model(graph, include_traces=False)
    records = {kind: {row['id']: row for row in graph.get(kind, [])}
               for kind in ('nodes', 'edges', 'evidence')}

    # Spool bounded navigation records into deterministic buckets. This avoids thousands of tiny files.
    spool = tempfile.TemporaryDirectory(prefix='.viewer-data-', dir=folder)
    spool_path = Path(spool.name)

    def write(key, value):
        hashed = 2166136261
        for char in key:
            hashed = ((hashed ^ ord(char)) * 16777619) & 0xffffffff
        bucket = f'bucket-{hashed % 512:03x}'
        with (spool_path / bucket).open('a', encoding='utf-8') as stream:
            stream.write(script_json(key) + ':' + script_json(value) + '\n')
        return key

    def finish():
        for path in sorted(spool_path.iterdir()):
            payload = ('{' + ','.join(path.read_text(encoding='utf-8').rstrip('\n').split('\n')) + '}').encode('utf-8')
            encoded = base64.b64encode(gzip.compress(payload, mtime=0)).decode()
            target = folder / (path.name + '.js')
            if target.is_symlink():
                raise ValueError('Viewer data cannot overwrite symbolic links')
            target.write_text('window.serviceGraphChunk(' + script_json(path.name) + ',' + script_json(encoded) + ');\n', encoding='utf-8')
        spool.cleanup()

    def pack(prefix, values):
        locations, pages, batch, size = {}, [], [], 0
        def flush():
            if not batch:
                return
            key = prefix + '-' + str(len(pages))
            write(key, batch)
            pages.append(key)
            for row in batch:
                locations[row['id']] = key
        for row in values:
            length = len(script_json(row).encode('utf-8'))
            if batch and size + length > CHUNK_BYTES:
                flush()
                batch.clear()
                size = 0
            batch.append(row)
            size += length
        flush()
        return locations, pages

    evidence_locations, _ = pack('evidence', records['evidence'].values())
    detail_locations = {}
    for kind in ('nodes', 'edges'):
        values = ({**row, 'evidence_chunks': sorted({evidence_locations[ref]
                   for ref in row.get('evidence', []) if ref in evidence_locations})}
                  for row in records[kind].values())
        detail_locations[kind], _ = pack(kind, values)

    owned, adjacent = defaultdict(list), defaultdict(list)
    for node in records['nodes'].values():
        owned[node.get('repository')].append(node['id'])
    for edge in records['edges'].values():
        for identifier in {edge['source'], edge['target']}:
            adjacent[identifier].append(edge['id'])
    roots = dict(model['repository_roots'])
    for repo in graph['repositories']:
        if repo['id'] not in roots:
            roots[repo['id']] = 'viewer-repository:' + repo['id']
    repository_by_root = {identifier: rid for rid, identifier in roots.items()}
    neighborhood_edges = {}
    for identifier in records['nodes']:
        rid = repository_by_root.get(identifier)
        neighborhood_edges[identifier] = (sorted({edge for node_id in owned[rid] for edge in adjacent[node_id]})
                                           if rid else sorted(adjacent[identifier]))
    for rid, identifier in roots.items():
        neighborhood_edges.setdefault(identifier, sorted({edge for node_id in owned[rid] for edge in adjacent[node_id]}))

    def node_summary(identifier):
        node = records['nodes'].get(identifier)
        if not node:
            rid = repository_by_root[identifier]
            repo = next(row for row in graph['repositories'] if row['id'] == rid)
            node = {'id': identifier, 'name': repo['name'], 'repository': rid,
                    'type': 'SOURCE_INVENTORY', 'dimensions': ['RUNTIME']}
        result = {key: node[key] for key in ('id', 'name', 'type', 'repository', 'dimensions', 'component_kind') if key in node}
        result.update(model['nodes'].get(identifier, {'lane': 'source', 'family': 'other', 'dependency_scope': 'PRODUCTION'}))
        result['detail'] = detail_locations['nodes'].get(identifier)
        result['key'] = hashlib.sha256(identifier.encode()).hexdigest()[:24]
        entries = len(neighborhood_edges[identifier])
        if identifier in repository_by_root:
            entries += len(owned[repository_by_root[identifier]])
        result['search'] = ' '.join(node.get('source_paths', []))
        result['pages'] = (entries + NEIGHBORHOOD_SIZE - 1) // NEIGHBORHOOD_SIZE
        return result

    summaries = {identifier: node_summary(identifier) for identifier in neighborhood_edges}
    edge_summaries = {identifier: {
        **{key: edge[key] for key in ('id', 'source', 'target', 'relationship', 'dimension')},
        **model['edges'][identifier], 'detail': detail_locations['edges'][identifier],
        'count': 1, 'edge_ids': [identifier],
    } for identifier, edge in records['edges'].items()}
    entries_by_node = {}
    labels = {'api': 'APIs', 'data': 'Data and messages', 'shared': 'Shared code',
              'configuration': 'Configuration', 'package': 'Packages',
              'structure': 'Components and ownership', 'other': 'Other declarations'}
    for identifier, edge_ids in neighborhood_edges.items():
        entries_by_node[identifier] = [{'edge': edge_summaries[edge_id]} for edge_id in edge_ids]
    for rid, root in roots.items():
        groups = []
        for family, label in labels.items():
            edge_ids = [edge_id for edge_id in neighborhood_edges[root]
                        if edge_summaries[edge_id]['family'] == family]
            node_ids = [node_id for node_id in owned[rid]
                        if model['nodes'][node_id]['family'] == family and node_id != root]
            if not edge_ids and not node_ids:
                continue
            identifier = 'viewer-group:' + rid + ':' + family
            entries = [{'edge': edge_summaries[edge_id]} for edge_id in edge_ids]
            entries += [{'node': node_id} for node_id in node_ids]
            summaries[identifier] = {
                'id': identifier, 'name': label, 'label': label, 'type': 'DEPENDENCY_GROUP',
                'repository': rid, 'family': family, 'lane': 'service', 'group': rid,
                'dependency_scope': summaries[root]['dependency_scope'],
                'key': hashlib.sha256(identifier.encode()).hexdigest()[:24],
                'pages': (len(entries) + NEIGHBORHOOD_SIZE - 1) // NEIGHBORHOOD_SIZE,
                'count': len(edge_ids), 'parent': root,
            }
            entries_by_node[identifier] = entries
            navigation = {'id': 'viewer-navigation:' + identifier, 'source': root, 'target': identifier,
                          'family': family, 'status': 'declared', 'label': 'Contains navigation group',
                          'dependency_scope': summaries[root]['dependency_scope'], 'navigation': True}
            groups.append({'edge': navigation})
        entries_by_node[root] = groups
        summaries[root]['pages'] = (len(groups) + NEIGHBORHOOD_SIZE - 1) // NEIGHBORHOOD_SIZE
    node_locations, node_index = pack('node-index', [summaries[identifier] for identifier in records['nodes']])
    edge_locations, edge_index = pack('edge-index', list(edge_summaries.values()))

    def neighborhood(page):
        ids = {row['node'] for row in page if 'node' in row}
        ids.update(endpoint for row in page if 'edge' in row
                   for endpoint in (row['edge']['source'], row['edge']['target']))
        return {
            'nodes': [summaries[node_id] for node_id in sorted(ids) if node_id not in node_locations],
            'node_refs': [{'id': node_id, 'chunk': node_locations[node_id]}
                          for node_id in sorted(ids) if node_id in node_locations],
            'edges': [row['edge'] for row in page if 'edge' in row and row['edge'].get('navigation')],
            'edge_refs': [{'id': row['edge']['id'], 'chunk': edge_locations[row['edge']['id']]}
                          for row in page if 'edge' in row and not row['edge'].get('navigation')],
        }

    for identifier, entries in entries_by_node.items():
        for offset in range(0, len(entries), NEIGHBORHOOD_SIZE):
            page = entries[offset:offset + NEIGHBORHOOD_SIZE]
            write(summaries[identifier]['key'] + '-' + str(offset // NEIGHBORHOOD_SIZE), neighborhood(page))

    trace_keys = {}
    def save_trace(trace):
        key = 'trace-' + hashlib.sha256(trace['id'].encode()).hexdigest()[:24]
        write(key, trace)
        trace_keys[trace['id']] = key
    build_trace_model(graph, trace_sink=save_trace)
    write('trace-index', trace_keys)
    if context:
        write('context', context)
    overview_links = []
    for link in model['system_links']:
        if link['source_repository'] and link['target_repository'] and link['source_repository'] != link['target_repository']:
            key = 'link-' + link['id'].split(':')[-1]
            for offset in range(0, len(link['edge_ids']), NEIGHBORHOOD_SIZE):
                identifiers = link['edge_ids'][offset:offset + NEIGHBORHOOD_SIZE]
                write(key + '-' + str(offset // NEIGHBORHOOD_SIZE),
                      neighborhood([{'edge': edge_summaries[edge_id]} for edge_id in identifiers]))
            overview_links.append({**{key: value for key, value in link.items() if key not in {'edge_ids', 'evidence'}},
                                   'key': key, 'pages': (len(link['edge_ids']) + NEIGHBORHOOD_SIZE - 1) // NEIGHBORHOOD_SIZE,
                                   'source': roots[link['source_repository']], 'target': roots[link['target_repository']]})
    finish()
    return {
        'generated_at': graph['generated_at'], 'repositories': graph['repositories'],
        'roots': roots, 'nodes': [summaries[identifier] for identifier in roots.values()],
        'links': overview_links, 'counts': model['counts'],
        'data_dir': folder.name + '/', 'source_prefix': source_prefix,
        'node_index': node_index, 'edge_index': edge_index, 'has_context': bool(context),
        'relationships': sorted({row['relationship'] for row in graph['edges']}),
    }
