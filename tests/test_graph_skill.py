"""Discover the canonical dependency skill portability and adapter checks."""

from pathlib import Path
import runpy

_path = Path(__file__).resolve().parents[1] / ".agents/skills/service-dependencies-graph/tests/test_portability.py"
globals().update({key: value for key, value in runpy.run_path(str(_path)).items() if not key.startswith("__")})
