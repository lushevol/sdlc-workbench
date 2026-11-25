#!/usr/bin/env python3
"""Render the schema-v2 graph as a small HTML entry point with local lazy data."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
from pathlib import Path
import re

from .architecture_context import candidate_context
from .viewer_bundle import script_json, write_bundle

HTML = Path(__file__).with_name('viewer.html').read_text(encoding='utf-8')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('graph', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--source-prefix', default='../')
    args = parser.parse_args(argv)
    graph = json.loads(args.graph.read_text(encoding='utf-8'))
    if graph.get('schema_version') != '2.0.0':
        raise ValueError('render_graph requires schema version 2.0.0')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.is_symlink():
        raise ValueError('Viewer HTML must not be a symbolic link')
    context = candidate_context(args.graph.parent, {row['id'] for row in graph['repositories']})
    if context:
        for source in context['provenance']['sources']:
            source['snapshot_path'] = os.path.relpath(
                args.graph.parent.resolve() / source['snapshot_path'], args.output.parent.resolve()).replace(os.sep, '/')
    data = args.output.with_suffix('.data')
    backup = data.with_name(data.name + '.previous')
    if data.is_symlink() or backup.exists() or backup.is_symlink():
        raise ValueError('Viewer data path or previous backup needs review')
    if data.exists() and (not data.is_dir() or any(
            not re.fullmatch(r'bucket-[0-9a-f]{3}\.js', path.name) or not path.is_file() or path.is_symlink()
            for path in data.iterdir())):
        raise ValueError('Viewer data directory must be empty or contain generated data buckets')
    with tempfile.TemporaryDirectory(prefix='.viewer-render-', dir=args.output.parent) as temporary:
        staged_html = Path(temporary) / args.output.name
        bootstrap = write_bundle(graph, staged_html, context, args.source_prefix)
        values = {'__BOOTSTRAP__': script_json(bootstrap)}
        rendered = re.sub('|'.join(map(re.escape, values)), lambda match: values[match.group()], HTML)
        staged_html.write_text(rendered, encoding='utf-8')
        if data.exists():
            data.replace(backup)
        try:
            staged_html.with_suffix('.data').replace(data)
            staged_html.replace(args.output)
        except Exception:
            if data.exists():
                shutil.rmtree(data)
            if backup.exists():
                backup.replace(data)
            raise
        if backup.exists():
            shutil.rmtree(backup)
    print(json.dumps({'output': str(args.output.resolve()), 'nodes': len(graph['nodes']),
                      'edges': len(graph['edges']), 'html_bytes': args.output.stat().st_size,
                      'data_dir': bootstrap['data_dir']}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
