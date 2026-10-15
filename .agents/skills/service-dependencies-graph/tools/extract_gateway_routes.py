"""Extract static gateway and OpenAPI route declarations.

The declarations describe path translation. They do not prove deployment or
reachability. Callers can use the records to join an incoming ``/api`` path to
an explicitly declared service route without guessing a prefix.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import yaml


def _line(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def extract_open_api_routes(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Read ``open-apis.apis`` entries from one Spring YAML file."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        root = yaml.compose(text)
    except (OSError, yaml.YAMLError) as exc:
        return [], [{"code": "INVALID_OPEN_API_CONFIGURATION", "path": path.as_posix(), "message": str(exc)}]
    routes: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []

    def scalar(node: Any) -> str | None:
        return node.value if isinstance(node, yaml.ScalarNode) else None

    def mapping(node: Any) -> dict[str, Any]:
        if not isinstance(node, yaml.MappingNode):
            return {}
        return {scalar(key) or "": value for key, value in node.value}

    def find_open_apis(node: Any) -> list[Any]:
        if isinstance(node, yaml.MappingNode):
            values = mapping(node)
            if "open-apis" in values:
                candidate = mapping(values["open-apis"]).get("apis")
                if isinstance(candidate, yaml.SequenceNode):
                    return list(candidate.value)
            for _, child in node.value:
                result = find_open_apis(child)
                if result:
                    return result
        elif isinstance(node, yaml.SequenceNode):
            for child in node.value:
                result = find_open_apis(child)
                if result:
                    return result
        return []

    for item in find_open_apis(root):
        values = mapping(item)
        entrypoint = mapping(values.get("entrypoint"))
        endpoint = mapping(values.get("endpoint"))
        method, incoming, service, target = (scalar(entrypoint.get("method")), scalar(entrypoint.get("path")),
                                              scalar(endpoint.get("service")), scalar(endpoint.get("path")))
        if not method or not incoming or not service or not target:
            diagnostics.append({"code": "UNRESOLVED_OPEN_API_ROUTE", "path": path.as_posix(),
                                "line": item.start_mark.line + 1,
                                "message": "Open API route lacks a static method, path, service, or endpoint path"})
            continue
        # The route protocol must be declared by the configuration. A path
        # that contains ``graphql`` is not enough evidence to classify the
        # transport because REST gateways can use the same naming.
        protocol_value = next((scalar(values.get(key)) or scalar(entrypoint.get(key)) or scalar(endpoint.get(key))
                               for key in ("protocol", "transport", "type")
                               if scalar(values.get(key)) or scalar(entrypoint.get(key)) or scalar(endpoint.get(key))), "REST")
        protocol = protocol_value.upper()
        if protocol in {"HTTP", "HTTP/REST"}:
            protocol = "REST"
        if protocol in {"WS", "WSS", "WEBSOCKET"}:
            protocol = "WEBSOCKET"
        elif protocol not in {"REST", "GRAPHQL"}:
            diagnostics.append({"code": "UNRESOLVED_OPEN_API_ROUTE", "path": path.as_posix(),
                                "line": item.start_mark.line + 1,
                                "message": "Open API route uses an unsupported protocol"})
            continue
        if any("${" in value for value in (incoming, service, target)):
            diagnostics.append({"code": "UNRESOLVED_OPEN_API_ROUTE", "path": path.as_posix(),
                                "line": item.start_mark.line + 1,
                                "message": "Open API route uses a dynamic path or service identity"})
            continue
        operation = next((scalar(values.get(key)) or scalar(endpoint.get(key))
                          for key in ("operation", "operation-name", "operationName", "field")
                          if scalar(values.get(key)) or scalar(endpoint.get(key))), None)
        routes.append({
            "method": method.upper(), "path": incoming, "service": service.removeprefix("lb://"),
            "endpoint_path": target, "line": item.start_mark.line + 1,
            "name": scalar(values.get("name")) or "", "protocol": protocol,
            **({"operation": operation} if operation else {}),
            "path_source": path.as_posix(),
        })
    return routes, diagnostics


def extract_nginx_routes(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Extract ``location``/``rewrite``/``proxy_pass`` blocks from nginx text."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return [], [{"code": "INVALID_NGINX_CONFIGURATION", "path": path.as_posix(), "message": str(exc)}]
    lines = text.splitlines()
    routes: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    location_re = re.compile(r"^\s*location\s+(?:(=)\s+)?([^\s{]+)")
    rewrite_re = re.compile(r"^\s*rewrite\s+(\S+)\s+(\S+)(?:\s+\w+)?\s*;")
    proxy_re = re.compile(r"^\s*proxy_pass\s+(\S+)\s*;")
    upstream_re = re.compile(r"^\s*upstream\s+([\w.-]+)\s*\{")
    upstreams: dict[str, str] = {}
    unresolved_upstreams: set[str] = set()
    declared_upstreams: set[str] = set()
    for number, line in enumerate(lines, 1):
        match = upstream_re.match(line)
        if match:
            name = match.group(1)
            duplicate = name in declared_upstreams
            declared_upstreams.add(name)
            # Stay within this upstream block. A later block cannot supply
            # the destination of an empty or incomplete declaration.
            body: list[str] = []
            depth = 1
            for index in range(number - 1, len(lines)):
                fragment = lines[index].split('#', 1)[0]
                if index == number - 1:
                    fragment = fragment[match.end():]
                for character in fragment:
                    if character == '{':
                        depth += 1
                    elif character == '}':
                        depth -= 1
                    if depth == 0:
                        break
                    body.append(character)
                if depth == 0:
                    break
                body.append('\n')
            servers = [item.group(1).strip() for item in re.finditer(r'\bserver\s+([^;{}]+);', ''.join(body))]
            if (depth != 0 or duplicate or len(servers) != 1
                    or any(token in servers[0] for token in ('$', '{', '}'))):
                unresolved_upstreams.add(name)
                upstreams.pop(name, None)
                diagnostics.append({
                    'code': 'UNRESOLVED_NGINX_UPSTREAM', 'path': path.as_posix(), 'line': number,
                    'message': 'Nginx upstream needs one complete static server declaration for a unique provider identity',
                })
            elif name not in unresolved_upstreams:
                upstreams[name] = servers[0]
    index = 0
    while index < len(lines):
        match = location_re.match(lines[index])
        if not match:
            index += 1
            continue
        start = index
        depth = lines[index].count("{") - lines[index].count("}")
        index += 1
        block: list[tuple[int, str]] = []
        while index < len(lines) and depth > 0:
            depth += lines[index].count("{") - lines[index].count("}")
            block.append((index + 1, lines[index]))
            index += 1
        rewrite = next((rewrite_re.match(line) for _, line in block if rewrite_re.match(line)), None)
        proxy = next((proxy_re.match(line) for _, line in block if proxy_re.match(line)), None)
        if not proxy:
            continue
        location = match.group(2)
        target = proxy.group(1)
        host = target.split("//", 1)[1].split("/", 1)[0] if "//" in target else target
        proxy_path = urlsplit(target).path if "://" in target else ""
        routes.append({
            "location": location, "exact": bool(match.group(1)),
            "rewrite_pattern": rewrite.group(1) if rewrite else None,
            "rewrite_target": rewrite.group(2) if rewrite else None,
            "proxy_path": proxy_path or None,
            "upstream": host, "upstream_server": upstreams.get(host),
            "upstream_ambiguous": host in unresolved_upstreams,
            "websocket": any("Upgrade" in line for _, line in block),
            "line": start + 1, "path_source": path.as_posix(),
        })
    return routes, diagnostics
