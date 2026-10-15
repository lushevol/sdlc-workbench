"""Extract static Spring STOMP/WebSocket endpoint declarations.

The extractor joins a ``registerStompEndpoints`` declaration with literal
endpoint defaults in the same repository.  It records only source-backed
paths.  Configuration expressions that cannot be resolved remain diagnostics.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

from .source_inventory import iter_source_files


_STRING = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')
# Permit the common ``properties.getWebSocket().getEndpoints()`` expression
# without evaluating it.  The bounded parenthesis form avoids stopping at the
# first nested call.
_REGISTRATION = re.compile(r"\baddEndpoint\s*\((?P<argument>(?:[^()]|\([^()]*\))*)\)", re.S)
_DEFAULT_ARRAY = re.compile(
    r"\b(?:String\s*\[\]|List\s*<\s*String\s*>|Set\s*<\s*String\s*>)\s+endpoints\s*="
    r"\s*(?:\{(?P<braced>[^}]*)\}|new\s+String\s*\[\]\s*\{(?P<new_array>[^}]*)\})",
    re.S,
)


def _strings(value: str) -> list[str]:
    result: list[str] = []
    for match in _STRING.finditer(value):
        raw = match.group(0)
        try:
            decoded = json.loads(raw) if raw.startswith('"') else bytes(raw[1:-1], "utf-8").decode("unicode_escape")
        except (ValueError, UnicodeDecodeError):
            continue
        if decoded:
            result.append(decoded)
    return result


def _line(source: str, offset: int) -> int:
    return source.count("\n", 0, offset) + 1


def _yaml_endpoint_defaults(path: Path) -> list[tuple[str, int]]:
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
        root = yaml.compose(source)
    except (OSError, yaml.YAMLError):
        return []

    rows: list[tuple[str, int]] = []

    def scalar(node: Any) -> str | None:
        return node.value if isinstance(node, yaml.ScalarNode) else None

    def visit(node: Any, keys: tuple[str, ...] = ()) -> None:
        if isinstance(node, yaml.MappingNode):
            for key, child in node.value:
                name = scalar(key) or ""
                visit(child, keys + tuple(name.replace("_", "-").split(".")))
        elif isinstance(node, yaml.SequenceNode):
            if keys and keys[-1] == "endpoints" and any("web-socket" in key or "websocket" in key for key in keys):
                for child in node.value:
                    value = scalar(child)
                    if value:
                        rows.append((value, child.start_mark.line + 1))
            else:
                for child in node.value:
                    visit(child, keys)

    visit(root)
    return rows


def extract_websocket_endpoints(repo: Path) -> dict[str, list[dict[str, Any]]]:
    """Return literal Spring STOMP endpoint declarations for ``repo``."""
    repo = repo.resolve()
    rows: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    java_files = list(iter_source_files(repo, root=repo / "src/main/java", suffixes={".java"}))
    defaults: list[tuple[str, Path, int]] = []
    for path in java_files:
        source = path.read_text(encoding="utf-8", errors="replace")
        for match in _DEFAULT_ARRAY.finditer(source):
            for endpoint in _strings(match.group("braced") or match.group("new_array") or ""):
                defaults.append((endpoint, path, _line(source, match.start())))

    for path in java_files:
        source = path.read_text(encoding="utf-8", errors="replace")
        if "registerStompEndpoints" not in source or "addEndpoint" not in source:
            continue
        owner = re.search(r"\bclass\s+(\w+)", source)
        controller = owner.group(1) if owner else path.stem
        for match in _REGISTRATION.finditer(source):
            argument = match.group("argument")
            values = _strings(argument)
            related: list[str] = []
            if not values and re.search(r"getEndpoints|\bendpoints\b", argument, re.I):
                values = [value for value, _, _ in defaults]
                related = [candidate.relative_to(repo).as_posix() for _, candidate, _ in defaults]
                values.extend(value for value, _ in _yaml_endpoint_defaults(repo / "src/main/resources/application.yml")
                              if value not in values)
            if not values:
                diagnostics.append({
                    "code": "UNRESOLVED_WEBSOCKET_ENDPOINT",
                    "path": path.relative_to(repo).as_posix(),
                    "message": f"Line {_line(source, match.start())}: STOMP endpoint expression cannot be resolved statically",
                })
                continue
            for value in values:
                endpoint = value if value.startswith("/") else "/" + value
                rows.append({
                    "path": endpoint,
                    "source_path": path.relative_to(repo).as_posix(),
                    "method": "ANY",
                    "line": _line(source, match.start()),
                    "declaration": source[match.start():match.end()].strip()[:500],
                    "provider_kind": "CONTROLLER",
                    "controller": controller,
                    "handler": "registerStompEndpoints",
                    "related_paths": sorted(set(related)),
                })
    unique = {(row["path"], row["line"], row["provider_kind"]): row for row in rows}
    return {"endpoints": [unique[key] for key in sorted(unique)], "diagnostics": diagnostics}
