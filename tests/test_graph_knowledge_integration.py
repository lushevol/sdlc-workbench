"""Discover the canonical knowledge graph skill regression tests."""

from pathlib import Path
import runpy

_path = Path(__file__).resolve().parents[1] / ".agents/skills/service-dependencies-graph/tests/test_knowledge_integration.py"
globals().update({key: value for key, value in runpy.run_path(str(_path)).items() if not key.startswith("__")})
