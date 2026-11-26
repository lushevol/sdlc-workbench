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

    service_graph = model['service_graph']
    roots = service_graph['repository_roots']
    summaries = {identifier: {
        **{key: node[key] for key in ('id', 'name', 'type', 'repository', 'dimensions', 'component_kind') if key in node},
        **model['nodes'][identifier], 'detail': detail_locations['nodes'][identifier],
        'search': ' '.join(node.get('source_paths', [])), 'pages': 0,
    } for identifier, node in records['nodes'].items()}
    edge_summaries = {identifier: {
        **{key: edge[key] for key in ('id', 'source', 'target', 'relationship', 'dimension')},
        **model['edges'][identifier], 'detail': detail_locations['edges'][identifier],
        'count': 1, 'edge_ids': [identifier],
    } for identifier, edge in records['edges'].items()}
    node_locations, node_index = pack('node-index', list(summaries.values()))
    edge_locations, edge_index = pack('edge-index', list(edge_summaries.values()))
    service_nodes, service_links = {}, {}
    adjacent, owned_edges = defaultdict(list), defaultdict(list)
    for edge in records['edges'].values():
        owned_edges[records['nodes'][edge['source']].get('repository')].append(edge['id'])
    for link in service_graph['links']:
        key = 'link-' + link['id'].split(':')[-1]
        service_links[link['id']] = {
            **{field: value for field, value in link.items() if field not in {'edge_ids', 'evidence'}},
            'service_link': True, 'key': key,
            'source_pages': (len(link['edge_ids']) + NEIGHBORHOOD_SIZE - 1) // NEIGHBORHOOD_SIZE,
        }
        for offset in range(0, len(link['edge_ids']), NEIGHBORHOOD_SIZE):
            write(key + '-sources-' + str(offset // NEIGHBORHOOD_SIZE),
                  [{'id': identifier, 'chunk': edge_locations[identifier]}
                   for identifier in link['edge_ids'][offset:offset + NEIGHBORHOOD_SIZE]])
        for identifier in (link['source'], link['target']):
            adjacent[identifier].append(link['id'])
    for identifier, metadata in service_graph['nodes'].items():
        node = records['nodes'].get(identifier, {})
        key = hashlib.sha256(identifier.encode()).hexdigest()[:24]
        service_nodes[identifier] = {
            **{field: node[field] for field in ('id', 'name', 'type', 'repository', 'dimensions') if field in node},
            **metadata, 'id': identifier, 'name': metadata.get('label', identifier),
            'detail': detail_locations['nodes'].get(identifier), 'key': key,
            'search': ' '.join(node.get('source_paths', [])),
            'pages': (len(adjacent[identifier]) + NEIGHBORHOOD_SIZE - 1) // NEIGHBORHOOD_SIZE,
            'card_pages': (len(owned_edges[node.get('repository')]) + NEIGHBORHOOD_SIZE - 1) // NEIGHBORHOOD_SIZE
                          if node.get('repository') else 0,
        }
        if node.get('repository'):
            for offset in range(0, len(owned_edges[node['repository']]), NEIGHBORHOOD_SIZE):
                write(key + '-card-' + str(offset // NEIGHBORHOOD_SIZE),
                      [{'id': edge_id, 'chunk': edge_locations[edge_id]}
                       for edge_id in owned_edges[node['repository']][offset:offset + NEIGHBORHOOD_SIZE]])
    service_locations, _ = pack('service-index', list(service_nodes.values()))
    for identifier, link_ids in adjacent.items():
        # Known local peers precede unavailable providers when expanding a hub.
        link_ids.sort(key=lambda link_id: (
            not (service_links[link_id]['source_repository'] and service_links[link_id]['target_repository']), link_id))
        for offset in range(0, len(link_ids), NEIGHBORHOOD_SIZE):
            links = [service_links[link_id] for link_id in link_ids[offset:offset + NEIGHBORHOOD_SIZE]]
            endpoints = sorted({endpoint for link in links for endpoint in (link['source'], link['target'])})
            write(service_nodes[identifier]['key'] + '-' + str(offset // NEIGHBORHOOD_SIZE), {
                'node_refs': [{'id': endpoint, 'chunk': service_locations[endpoint]} for endpoint in endpoints],
                'edges': links,
            })

    trace_keys = {}
    def save_trace(trace):
        key = 'trace-' + hashlib.sha256(trace['id'].encode()).hexdigest()[:24]
        write(key, trace)
        trace_keys[trace['id']] = key
    build_trace_model(graph, trace_sink=save_trace)
    write('trace-index', trace_keys)
    if context:
        write('context', context)
    initial_nodes = [row for row in service_nodes.values() if row.get('repository')]
    initial_ids = {row['id'] for row in initial_nodes}
    overview_links = [row for row in service_links.values()
                      if row['source'] in initial_ids and row['target'] in initial_ids]
    finish()
    return {
        'generated_at': graph['generated_at'], 'repositories': graph['repositories'],
        'roots': roots, 'nodes': initial_nodes,
        'links': overview_links, 'counts': model['counts'],
        'data_dir': folder.name + '/', 'source_prefix': source_prefix,
        'node_index': node_index, 'edge_index': edge_index, 'has_context': bool(context),
        'relationships': sorted({row['relationship'] for row in graph['edges']}),
    }
