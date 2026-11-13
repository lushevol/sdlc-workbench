"""Keep explicit legacy fixtures independent of the current initialization layout."""

from pathlib import Path

from ai_sdlc_workbench.workspace import initialize_workspace


def initialize_legacy_workspace(root: Path) -> Path:
    root = initialize_workspace(root)
    evidence = root / "knowledge/evidence"
    if evidence.exists():
        (root / "evidence").mkdir(exist_ok=True)
        evidence.rename(root / "evidence/knowledge")
        records = root / "knowledge/records"
        for child in records.iterdir():
            child.rename(root / "knowledge" / child.name)
        records.rmdir()
    return root
