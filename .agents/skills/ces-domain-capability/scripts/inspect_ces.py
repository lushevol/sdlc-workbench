"""Preserve the original CES inspector command path."""

from pathlib import Path
import runpy


if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parents[1] / "Workflows/tools/inspect_ces.py"), run_name="__main__")
