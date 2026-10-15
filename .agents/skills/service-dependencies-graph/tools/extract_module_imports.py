"""Join value imports to exact in-scope npm package declarations."""

from __future__ import annotations

import hashlib

from tree_sitter import Language, Parser
import tree_sitter_typescript

from .source_inventory import iter_source_files


def extract(graph, packages) -> None:
    namespaces = {name.removeprefix('npm:').split('/')[0] for name in packages if name.startswith('npm:@')}
    for repository in graph.repositories:
        if repository['kind'] != 'WEB' or not repository['visible']:
            continue
        root = graph.repo_roots[repository['id']]
        owner = 'application:' + repository['name']
        for path in iter_source_files(root, root=root / 'src', suffixes={'.ts', '.tsx', '.js', '.jsx'}):
            if path.name.endswith(('.test.ts', '.test.tsx', '.spec.ts', '.spec.tsx',
                                   '.test.js', '.test.jsx', '.spec.js', '.spec.jsx', '.d.ts')):
                continue
            encoded = path.read_bytes()
            language = (tree_sitter_typescript.language_tsx() if path.suffix in {'.tsx', '.jsx'}
                        else tree_sitter_typescript.language_typescript())
            tree = Parser(Language(language)).parse(encoded)
            source_path = path.relative_to(graph.workspace).as_posix()
            for node in tree.root_node.named_children:
                if node.type != 'import_statement':
                    continue
                source = node.child_by_field_name('source')
                if source is None:
                    continue
                raw = encoded[source.start_byte:source.end_byte].decode('utf-8', errors='replace')
                if len(raw) < 2 or '\\' in raw:
                    continue
                module = raw[1:-1]
                providers = packages.get('npm:' + module, {})
                candidates = {key: value for key, value in providers.items() if key != owner}
                if not candidates and (providers or module.split('/')[0] not in namespaces):
                    continue
                declaration = encoded[node.start_byte:node.end_byte].decode('utf-8', errors='replace')
                if node.has_error:
                    graph.diagnostic('UNSUPPORTED_MODULE_IMPORT', 'Module import has a source parse error',
                                     repository['id'], source_path)
                    continue
                # Tree-sitter exposes the type keyword and per-specifier type modifiers.
                if any(child.type == 'type' for child in node.children):
                    continue
                clause = next((child for child in node.named_children if child.type == 'import_clause'), None)
                if clause is not None:
                    bindings = list(clause.named_children)
                    if len(bindings) == 1 and bindings[0].type == 'named_imports':
                        specifiers = bindings[0].named_children
                        if specifiers and all(any(child.type == 'type' for child in item.children) for item in specifiers):
                            continue
                evidence = graph.add_evidence(repository['id'], source_path, node.start_point.row + 1,
                                              declaration, 'es-module-import')
                properties = {'module': module, 'dependency_kind': 'MODULE'}
                if len(candidates) == 1:
                    target, provider_evidence = next(iter(candidates.items()))
                    graph.add_edge(owner, target, 'IMPORTS_MODULE', 'RUNTIME', {evidence} | provider_evidence,
                                   resolution_status='RESOLVED', properties={**properties,
                                   'resolution_rule': 'exact-npm-module-import'})
                else:
                    boundary = 'external-module:' + hashlib.sha256(module.encode()).hexdigest()[:24]
                    graph.add_node(boundary, 'EXTERNAL_SYSTEM', module, None, dimensions=('RUNTIME',),
                                   component_kind=None, functional_role='Names an imported module without a unique provider',
                                   business_meaning='The module provider remains unresolved', source_paths=(),
                                   evidence=(evidence,), properties=properties)
                    graph.add_edge(owner, boundary, 'IMPORTS_MODULE', 'RUNTIME', (evidence,),
                                   resolution_status='AMBIGUOUS' if candidates else 'UNRESOLVED',
                                   properties={**properties, **({'candidate_providers': sorted(candidates)} if candidates else {})})
                    graph.diagnostic('AMBIGUOUS_MODULE_PROVIDER' if candidates else 'UNRESOLVED_MODULE_PROVIDER',
                                     'Multiple repositories publish ' + module if candidates else 'No exact in-scope package publishes ' + module,
                                     repository['id'], source_path)
