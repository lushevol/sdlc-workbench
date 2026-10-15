"""Deterministic identity and contract joins. Never infer hosts from URL suffixes."""
from __future__ import annotations

import json
import hashlib
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit

import yaml
from .source_inventory import is_source_file, iter_source_files
from .extract_module_imports import extract as extract_module_imports


def stable_id(prefix: str, *parts: object) -> str:
    raw = "|".join(str(part) for part in parts)
    return f"{prefix}:{hashlib.sha256(raw.encode()).hexdigest()[:24]}"


def application_id(repo: dict) -> str:
    return ('application:' if repo['kind'] == 'WEB' else 'service:') + repo['name']


def identities(graph):
    """Index exact published coordinates plus declared service/module aliases."""
    aliases = defaultdict(lambda: defaultdict(set))
    packages = defaultdict(lambda: defaultdict(set))
    dependencies = []

    def evidence(repo, path, declaration, extractor, line=1):
        return graph.add_evidence(repo['id'], path.relative_to(graph.workspace).as_posix(), line, declaration, extractor)

    for repo in graph.repositories:
        if not repo['visible']:
            continue
        root = graph.repo_roots[repo['id']]
        owner = application_id(repo)
        if repo['kind'] == 'INFRA':
            aliases[repo['name'].lower()][owner].update(graph.nodes[owner]['evidence'])
            continue
        manifest = root / ('package.json' if repo['kind'] == 'WEB' else 'pom.xml')
        if not is_source_file(root, manifest):
            graph.diagnostic('EXCLUDED_REPOSITORY_MANIFEST', 'Repository manifest is excluded by the scan policy',
                             repo['id'], manifest.relative_to(graph.workspace).as_posix())
            continue
        ev = evidence(repo, manifest, 'Repository identity: ' + repo['name'], 'repository-identity')
        aliases[repo['name'].lower()][owner].add(ev)
        if repo['kind'] == 'WEB':
            manifests = [manifest]
            manifests.extend(path for path in iter_source_files(root, root=root, suffixes={'.json'})
                             if path.name == 'package.json' and path != manifest)
            for package_manifest in manifests:
                try:
                    data = json.loads(package_manifest.read_text())
                except (ValueError, OSError):
                    graph.diagnostic('INVALID_PACKAGE_MANIFEST', 'Cannot parse package.json', repo['id'], package_manifest.relative_to(graph.workspace).as_posix())
                    continue
                name = data.get('name')
                if isinstance(name, str) and name:
                    extractor = 'npm-package' if package_manifest == manifest else 'npm-nested-package'
                    ev = evidence(repo, package_manifest, 'npm package ' + name, extractor)
                    aliases[name][owner].add(ev)
                    packages['npm:' + name][owner].add(ev)
                for scope in ('dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies'):
                    values = data.get(scope, {})
                    if not isinstance(values, dict):
                        continue
                    for dependency_name in sorted(values):
                        ev = evidence(repo, package_manifest, f'{scope}: {dependency_name}', 'npm-dependency')
                        dependencies.append((owner, 'npm:' + dependency_name, scope, ev))
        else:
            try:
                pom = ET.fromstring(manifest.read_text())
            except (ET.ParseError, OSError):
                graph.diagnostic('INVALID_MAVEN_MANIFEST', 'Cannot parse pom.xml', repo['id'])
                continue
            # Local properties and parent group/version only. No remote parent evaluation.
            for node in pom.iter():
                node.tag = node.tag.rsplit('}', 1)[-1]
            props = {node.tag: (node.text or '').strip() for node in pom.findall('./properties/*')}
            group = pom.findtext('groupId') or pom.findtext('parent/groupId') or ''
            artifact = pom.findtext('artifactId') or ''
            props.update({'project.groupId': group, 'pom.groupId': group, 'project.artifactId': artifact})

            def resolve(value):
                for _ in range(10):
                    new = re.sub(r'\$\{([^}]+)\}', lambda m: props.get(m[1], m[0]), value)
                    if new == value:
                        break
                    value = new
                return value

            group, artifact = resolve(group.strip()), resolve(artifact.strip())
            if group and artifact and '${' not in group + artifact:
                coordinate = f'maven:{group}:{artifact}'
                ev = evidence(repo, manifest, coordinate, 'maven-artifact')
                packages[coordinate][owner].add(ev)
                aliases[artifact.lower()][owner].add(ev)
            for dep in pom.findall('./dependencies/dependency'):
                coordinate = 'maven:' + resolve((dep.findtext('groupId') or '').strip()) + ':' + resolve((dep.findtext('artifactId') or '').strip())
                ev = evidence(repo, manifest, coordinate, 'maven-dependency')
                dependencies.append((owner, coordinate, dep.findtext('scope') or 'compile', ev))
            resource = root / 'src/main/resources'
            for path in iter_source_files(root, root=resource, suffixes={'.yml', '.yaml', '.properties'}):
                if path.parent != resource or not path.name.startswith('application'):
                    continue
                values = []
                try:
                    if path.suffix == '.properties':
                        for line, text in enumerate(path.read_text().splitlines(), 1):
                            match = re.match(r'\s*spring\.application\.name\s*[:=]\s*([^#!\s]+)', text)
                            if match:
                                values.append((match[1], line))
                    else:
                        def visit(node, prefix=()):
                            if isinstance(node, yaml.MappingNode):
                                for key, child in node.value:
                                    visit(child, prefix + tuple(key.value.split('.')))
                            elif isinstance(node, yaml.ScalarNode) and prefix == ('spring', 'application', 'name'):
                                values.append((node.value, node.start_mark.line + 1))
                        for document in yaml.compose_all(path.read_text()):
                            visit(document)
                except (yaml.YAMLError, OSError):
                    graph.diagnostic('INVALID_SERVICE_CONFIGURATION', 'Service identity config cannot be parsed', repo['id'], path.relative_to(graph.workspace).as_posix())
                for value, line in values:
                    if re.fullmatch(r'[A-Za-z0-9_.-]+', value):
                        ev = evidence(repo, path, 'spring.application.name=' + value, 'spring-service-identity', line)
                        aliases[value.lower()][owner].add(ev)
    return aliases, packages, dependencies


def resolve(graph):
    aliases, packages, package_uses = identities(graph)
    extract_module_imports(graph, packages)
    providers = {edge['target'] for edge in graph.edges.values() if edge['relationship'] == 'EXPOSES'}

    def segment_match(actual: str, expected: str) -> bool:
        return actual == expected or bool(re.fullmatch(r'\{[A-Za-z_][\w.]*\}', expected))

    def path_match(actual: str, expected: str) -> bool:
        left = (actual.split('?', 1)[0].rstrip('/') or '/').split('/')
        right = (expected.split('?', 1)[0].rstrip('/') or '/').split('/')
        return len(left) == len(right) and all(segment_match(a, b) for a, b in zip(left, right))

    def rewrite_path(route, path: str) -> str | None:
        location = route.get('location', '')
        if route.get('exact'):
            if path != location:
                return None
        elif not path.startswith(location.rstrip('/') + '/') and path != location:
            return None
        pattern, target = route.get('rewrite_pattern'), route.get('rewrite_target')
        if pattern and target:
            try:
                replacement = re.sub(r'\$(\d+)', r'\\g<\1>', target)
                return re.sub(pattern, replacement, path, count=1)
            except re.error:
                return None
        # A URI target replaces the matched location prefix and retains its suffix.
        proxy_path = route.get('proxy_path')
        if proxy_path:
            return proxy_path + path[len(location):]
        return path

    def gateway_matches(edge, method: str, path: str, protocol: str, allowed_repositories=None):
        if protocol == 'WEBSOCKET' and getattr(graph, 'gateway_routes', None):
            matches = []
            nginx_routes = [row for row in graph.gateway_routes if row.get('kind') == 'NGINX'
                            and row.get('websocket') and not row.get('upstream_ambiguous')]
            for nginx in nginx_routes:
                rewritten = rewrite_path(nginx, path)
                if rewritten is None:
                    continue
                for provider_id in sorted(providers):
                    provider = graph.nodes[provider_id]
                    properties = provider.get('properties', {})
                    if properties.get('protocol') != 'WEBSOCKET' or properties.get('provider_kind') != 'CONTROLLER':
                        continue
                    if allowed_repositories is not None and provider.get('repository') not in allowed_repositories:
                        continue
                    provider_path = properties.get('path', '').rstrip('/') or '/'
                    if not path_match(rewritten, provider_path):
                        continue
                    aliases_for_upstream = set()
                    for upstream in (nginx.get('upstream'), nginx.get('upstream_server')):
                        if not upstream:
                            continue
                        aliases_for_upstream.update(
                            graph.nodes[key].get('repository')
                            for key in aliases.get(str(upstream).lower(), {})
                            if key in graph.nodes and graph.nodes[key].get('type') == 'SERVICE'
                        )
                    # A websocket route must identify the provider through a
                    # declared upstream service identity.  An IP-only or
                    # unknown upstream is evidence of an external boundary,
                    # not permission to attach the route to every matching
                    # local endpoint.
                    if not aliases_for_upstream or provider.get('repository') not in aliases_for_upstream:
                        continue
                    evidence = set(provider.get('evidence', [])) | {nginx['evidence']}
                    matches.append((provider_id, evidence, {
                        'incoming_path': path, 'rewritten_path': rewritten,
                        'gateway_location': nginx['location'], 'upstream': nginx['upstream'],
                        'upstream_server': nginx.get('upstream_server'),
                        'endpoint_path': provider_path,
                    }))
            grouped = defaultdict(set)
            details = defaultdict(list)
            for provider_id, evidence, detail in matches:
                grouped[provider_id].update(evidence)
                details[provider_id].append(detail)
            unique_details = []
            seen_details = set()
            for detail in (detail for rows in details.values() for detail in rows):
                identity = tuple(detail.get(key) for key in (
                    'incoming_path', 'rewritten_path', 'gateway_location',
                    'upstream', 'upstream_server', 'endpoint_path'))
                if identity in seen_details:
                    continue
                seen_details.add(identity)
                unique_details.append(detail)
            return dict(grouped), unique_details
        if protocol not in {'REST', 'GRAPHQL'} or not getattr(graph, 'gateway_routes', None):
            return {}, []
        matches = []
        nginx_routes = [row for row in graph.gateway_routes if row.get('kind') == 'NGINX']
        open_routes = [row for row in graph.gateway_routes if row.get('kind') == 'OPEN_API']

        # A static upstream identity and rewritten path can identify a direct
        # controller without an intermediate Spring open-apis declaration.
        for nginx in nginx_routes:
            if protocol != 'REST' or nginx.get('upstream_ambiguous'):
                continue
            rewritten = rewrite_path(nginx, path)
            authority = nginx.get('upstream_server') or nginx.get('upstream', '')
            if rewritten is None or any(token in authority for token in ('$', '{', '}')):
                continue
            try:
                host = urlsplit('//' + authority.split()[0]).hostname
            except (ValueError, IndexError):
                continue
            service_ids = {key: values for key, values in aliases.get(str(host).lower(), {}).items()
                           if graph.nodes[key].get('type') == 'SERVICE'}
            if len(service_ids) != 1:
                continue
            service_id, identity_evidence = next(iter(service_ids.items()))
            repository = graph.nodes[service_id].get('repository')
            if allowed_repositories is not None and repository not in allowed_repositories:
                continue
            for provider_id in sorted(providers):
                provider = graph.nodes[provider_id]
                properties = provider.get('properties', {})
                if (provider.get('repository') != repository or properties.get('protocol') != 'REST'
                        or properties.get('provider_kind') != 'CONTROLLER'
                        or (properties.get('method') not in {'ANY', method} and method != 'ANY')
                        or not path_match(rewritten, properties.get('path', ''))):
                    continue
                refs = set(provider.get('evidence', [])) | set(identity_evidence) | {nginx['evidence']}
                matches.append((provider_id, refs, {
                    'incoming_path': path, 'rewritten_path': rewritten,
                    'gateway_location': nginx['location'], 'upstream': nginx['upstream'],
                    'upstream_server': nginx.get('upstream_server'),
                    'endpoint_path': properties['path'], 'route_kind': 'DIRECT_NGINX',
                }))

        def add_route(route, rewritten, gateway=None):
            if route.get('protocol', 'REST') != protocol:
                return
            if route['method'] not in {'ANY', method} and method != 'ANY':
                return
            if not path_match(rewritten, route['path']):
                return
            service_ids = aliases.get(str(route['service']).lower(), {})
            service_nodes = [key for key in service_ids
                             if key in graph.nodes and graph.nodes[key].get('type') == 'SERVICE']
            # Duplicate aliases cannot establish the routed service identity.
            if len(service_nodes) != 1:
                return
            service_node = service_nodes[0]
            repository = graph.nodes[service_node].get('repository')
            if allowed_repositories is not None and repository not in allowed_repositories:
                return
            route_evidence = {route['evidence']} | set(service_ids[service_node])
            if gateway:
                route_evidence.add(gateway['evidence'])
            detail = {
                'incoming_path': path, 'rewritten_path': rewritten,
                'service': route['service'], 'endpoint_path': route['endpoint_path'],
            }
            if gateway:
                detail.update(gateway_location=gateway['location'], upstream=gateway['upstream'])
            controller_matches = []
            if protocol == 'REST':
                for provider_id in sorted(providers):
                    provider = graph.nodes[provider_id]
                    properties = provider.get('properties', {})
                    if provider.get('repository') != repository:
                        continue
                    if properties.get('protocol') != protocol or properties.get('provider_kind') != 'CONTROLLER':
                        continue
                    if properties.get('method') not in {'ANY', method} and method != 'ANY':
                        continue
                    if path_match(route['endpoint_path'], properties.get('path', '')):
                        controller_matches.append(provider_id)
            if controller_matches:
                for provider_id in controller_matches:
                    matches.append((provider_id, route_evidence | set(graph.nodes[provider_id]['evidence']), detail))
                return
            # A local open-apis route is static transport evidence, not handler
            # implementation evidence. REST callers must also identify this
            # service; a bare relative path cannot invent a missing provider.
            if route.get('repository') != repository or (protocol == 'REST' and allowed_repositories is None):
                return
            operation_id = stable_id('operation:gateway-transport', repository, protocol,
                                     route['method'], route['endpoint_path'])
            graph.add_node(
                operation_id, 'API_OPERATION', protocol + ' ' + route['endpoint_path'], repository,
                dimensions=('RUNTIME',), component_kind=None,
                functional_role='Declares a gateway transport endpoint',
                business_meaning='Declares static routing without handler execution evidence',
                source_paths=[graph.evidence[route['evidence']]['path']], evidence=route_evidence,
                properties={
                    'protocol': protocol, 'method': route['method'], 'path': route['endpoint_path'],
                    'provider_kind': 'GATEWAY_TRANSPORT', 'service_alias': route['service'],
                    'implementation_status': 'UNKNOWN',
                },
            )
            graph.add_edge(service_node, operation_id, 'EXPOSES', 'RUNTIME', route_evidence,
                           properties={'protocol': protocol, 'route_kind': 'OPEN_API'})
            matches.append((operation_id, route_evidence, detail))

        for route in open_routes:
            add_route(route, path)
        for nginx in nginx_routes:
            if nginx.get('upstream_ambiguous'):
                continue
            rewritten = rewrite_path(nginx, path)
            if rewritten is not None:
                for route in open_routes:
                    add_route(route, rewritten, nginx)
        grouped = defaultdict(set)
        details = []
        seen_details = set()
        for provider_id, evidence, detail in matches:
            grouped[provider_id].update(evidence)
            identity = tuple(detail.get(key) for key in (
                'incoming_path', 'rewritten_path', 'gateway_location', 'upstream', 'service', 'endpoint_path'))
            if identity not in seen_details:
                seen_details.add(identity)
                details.append(detail)
        return dict(grouped), details

    def join(edge, candidates, rule):
        candidates = {key: value for key, value in candidates.items()
                      if graph.nodes[key].get('repository') != graph.nodes[edge['source']].get('repository')}
        # Keep the original external boundary as an auditable unresolved
        # declaration. A second edge records the deterministic provider join.
        # This preserves the candidate frontier for callers that need to see
        # what the source declaration originally named.
        edge['resolution_status'] = 'UNRESOLVED'
        if not candidates:
            return
        edge.setdefault('properties', {})['candidate_providers'] = sorted(candidates)
        if len(candidates) > 1:
            edge['resolution_status'] = 'AMBIGUOUS'
            graph.diagnostic('AMBIGUOUS_RUNTIME_BOUNDARY', 'Multiple compatible providers: ' + ', '.join(sorted(candidates)), graph.nodes[edge['source']].get('repository'))
            return
        target = next(iter(candidates))
        resolved_properties = dict(edge.get('properties', {}))
        resolved_properties.pop('candidate_providers', None)
        resolved_properties.update({'resolved_from': edge['target'], 'resolution_rule': rule})
        graph.add_edge(edge['source'], target, edge['relationship'], edge['dimension'],
                       set(edge['evidence']) | set(candidates[target]),
                       assertion_status=edge['assertion_status'], resolution_status='RESOLVED',
                       properties=resolved_properties)

    for owner, coordinate, scope, ev in package_uses:
        candidates = {key: values for key, values in packages.get(coordinate, {}).items() if key != owner}
        if len(candidates) != 1:
            package_id = stable_id('external-package', coordinate)
            graph.add_node(
                package_id, 'EXTERNAL_SYSTEM', coordinate, None, dimensions=('RUNTIME',), component_kind=None,
                functional_role='Declares a package required by the build',
                business_meaning='Declared build dependency with an unresolved package provider',
                source_paths=(), evidence=(ev,),
                properties={'coordinate': coordinate, 'dependency_kind': 'BUILD', 'boundary_kind': 'PACKAGE'},
            )
            graph.add_edge(
                owner, package_id, 'DEPENDS_ON_PACKAGE', 'RUNTIME', (ev,),
                resolution_status='AMBIGUOUS' if candidates else 'UNRESOLVED',
                properties={'coordinate': coordinate, 'scopes': [scope], 'dependency_kind': 'BUILD',
                            **({'candidate_providers': sorted(candidates)} if candidates else {})},
            )
        for target, provider_evidence in sorted(candidates.items()):
            if len(candidates) == 1:
                graph.add_edge(owner, target, 'DEPENDS_ON_PACKAGE', 'RUNTIME', {ev} | provider_evidence,
                               resolution_status='RESOLVED', properties={'coordinate': coordinate, 'scopes': [scope],
                               'resolution_rule': 'exact-published-coordinate', 'dependency_kind': 'BUILD'})
            else:
                graph.diagnostic('AMBIGUOUS_PACKAGE_PROVIDER', 'Multiple repositories publish ' + coordinate, graph.nodes[owner]['repository'])
                break
    # Snapshot avoids mutating the edge collection while iterating.
    for edge in list(graph.edges.values()):
        target = graph.nodes[edge['target']]
        if target.get('repository') is not None:
            continue
        props = target.get('properties', {})
        relation = edge['relationship']
        if relation == 'LOADS_REMOTE':
            join(edge, aliases.get(props.get('module', ''), {}), 'declared-module-identity')
        elif relation == 'CALLS_SERVICE':
            alias = str(props.get('service_alias', '')).lower()
            join(edge, {key: values for key, values in aliases.get(alias, {}).items() if graph.nodes[key]['type'] == 'SERVICE'}, 'declared-service-identity')
        elif relation in {'CALLS_REST', 'CALLS_GRAPHQL', 'SUBSCRIBES_WS'}:
            protocol = props.get('protocol')
            path = props.get('path', '')
            # Absolute URLs need an exact known authority. Never discard an external host.
            host = None
            if path.startswith(('http://', 'https://', 'ws://', 'wss://', '//')):
                parsed = urlsplit(path)
                if parsed.username or parsed.password:
                    continue
                host, path = parsed.hostname, parsed.path
            if not path.startswith('/'):
                continue
            normalized = path.split('?', 1)[0].rstrip('/') or '/'
            candidates = {}
            service_alias = str(props.get('service_alias', '')).lower()
            allowed_repositories = None
            if service_alias:
                service_ids = aliases.get(service_alias, {})
                allowed_repositories = {
                    graph.nodes[key].get('repository') for key in service_ids
                    if key in graph.nodes and graph.nodes[key].get('type') == 'SERVICE'
                }
            if host:
                authority_repositories = {
                    graph.nodes[key].get('repository') for key in aliases.get(host.lower(), {})
                    if key in graph.nodes and graph.nodes[key].get('type') == 'SERVICE'
                }
                allowed_repositories = (authority_repositories if allowed_repositories is None
                                        else allowed_repositories & authority_repositories)
            for provider_id in sorted(providers):
                provider = graph.nodes[provider_id]
                pp = provider.get('properties', {})
                if pp.get('protocol') != protocol or pp.get('provider_kind') != 'CONTROLLER':
                    continue
                if allowed_repositories is not None and provider.get('repository') not in allowed_repositories:
                    continue
                if protocol == 'REST' and not (
                    pp.get('method') == 'ANY'
                    or props.get('method') in {'ANY', pp.get('method')}
                ):
                    continue
                if host and not any(graph.nodes[key].get('repository') == provider['repository'] for key in aliases.get(host.lower(), {})):
                    continue
                provider_path = pp.get('path', '').rstrip('/') or '/'
                # A whole path segment may be a variable; never erase a prefix or expand wildcards.
                left, right = normalized.split('/'), provider_path.split('/')
                if len(left) != len(right):
                    continue
                def variable(segment):
                    return bool(re.fullmatch(r'\{[A-Za-z_][\w.]*\}', segment))
                if all(a == b or (variable(b) and bool(a)) for a, b in zip(left, right)):
                    # Candidate evidence is merged with gateway evidence below.
                    # Keep the value mutable as a set; provider evidence is
                    # serialized as a list in the graph document.
                    candidates[provider_id] = set(provider['evidence'])
            gateway_candidates, gateway_details = gateway_matches(edge, props.get('method', 'ANY'), normalized, protocol, allowed_repositories)
            if gateway_details:
                edge.setdefault('properties', {})['gateway_routes'] = gateway_details
                for provider_id, evidence in gateway_candidates.items():
                    candidates.setdefault(provider_id, set()).update(evidence)
            if candidates:
                rule = ('gateway-websocket-route-and-exposed-operation' if protocol == 'WEBSOCKET' and gateway_candidates
                        else 'gateway-route-and-declared-transport' if any(
                            graph.nodes[key].get('properties', {}).get('provider_kind') == 'GATEWAY_TRANSPORT'
                            for key in gateway_candidates)
                        else 'nginx-upstream-rewrite-and-exposed-operation' if any(
                            detail.get('route_kind') == 'DIRECT_NGINX' for detail in gateway_details)
                        else 'gateway-rewrite-open-api-and-exposed-operation' if gateway_candidates
                        else 'compatible-exposed-operation' if host is None else 'authority-and-exposed-operation')
            else:
                rule = 'gateway-route-without-local-provider' if gateway_details else 'compatible-exposed-operation'
            join(edge, candidates, rule)
