"""Discover canonical skill regressions from the standalone checkout."""
from pathlib import Path
import runpy

_path = Path(__file__).resolve().parents[1] / ".agents/skills/service-dependencies-graph/tests/test_web_structure.py"
globals().update({key: value for key, value in runpy.run_path(str(_path)).items() if not key.startswith("__")})
