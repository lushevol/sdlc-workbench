#!/usr/bin/env python3
"""Compatibility entry point for ratan_harness.tracing."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from ratan_harness import tracing as _engine

if __name__ == "__main__":
    raise SystemExit("Import this module through ratan_harness.")
else:
    sys.modules[__name__] = _engine
    globals().update(vars(_engine))
