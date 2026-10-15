#!/usr/bin/env python3
"""Compatibility entry point for ratan_harness.graph.service_dependencies_graph_mcp."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from ratan_harness.graph import service_dependencies_graph_mcp as _engine

if __name__ == "__main__":
    raise SystemExit(_engine.main())
else:
    sys.modules[__name__] = _engine
    globals().update(vars(_engine))
