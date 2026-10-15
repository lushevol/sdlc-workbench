#!/usr/bin/env python3
"""Render the schema-v2 Service Dependencies Graph as a dependency-free HTML explorer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


from .viewer_model import build_viewer_model


HTML = Path(__file__).with_name("viewer.html").read_text(encoding="utf-8")


def script_json(value: object) -> str:
    """Keep untrusted source text inside a JSON script element."""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("<", r"\u003c")



def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-prefix", default="../")
    args = parser.parse_args(argv)
    graph = json.loads(args.graph.read_text(encoding="utf-8"))
    if graph.get("schema_version") != "2.0.0":
        raise ValueError("render_graph requires schema version 2.0.0")
    values = {
        "__GRAPH__": script_json(graph),
        "__VIEWER__": script_json(build_viewer_model(graph)),
        "__SOURCE_PREFIX__": script_json(args.source_prefix),
    }
    # Substitute once. Source strings can contain template marker text.
    import re
    rendered = re.sub("|".join(map(re.escape, values)), lambda match: values[match.group()], HTML)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(json.dumps({"output": str(args.output.resolve()), "nodes": len(graph["nodes"]), "edges": len(graph["edges"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
