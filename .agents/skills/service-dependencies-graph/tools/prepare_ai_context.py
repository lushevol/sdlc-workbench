#!/usr/bin/env python3
"""Compatibility entry point for ratan_harness.graph.prepare_ai_context."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from ratan_harness.graph import prepare_ai_context as _engine

if __name__ == "__main__":
    raise SystemExit(_engine.main())
else:
    sys.modules[__name__] = _engine
    globals().update(vars(_engine))
