"""Resolve the two supported knowledge layouts without merging authority."""

from pathlib import Path

from .models import WorkbenchError


def knowledge_layout(root: Path) -> tuple[Path, Path]:
    """Return absolute canonical-record and evidence roots for one active layout."""
    root = Path(root).expanduser().resolve()
    records, evidence = root / "knowledge/records", root / "knowledge/evidence"
    legacy = root / "evidence/knowledge"
    current_marker, legacy_marker = evidence / "manifest.yaml", legacy / "manifest.yaml"
    current = current_marker.exists() or current_marker.is_symlink()
    previous = legacy_marker.exists() or legacy_marker.is_symlink()
    if current and previous:
        raise WorkbenchError("Both knowledge manifests exist. Finish or recover the layout migration before continuing.")
    if current:
        if not records.is_dir():
            raise WorkbenchError("The consolidated knowledge layout requires knowledge/records/. Restore it before continuing.")
        return records, evidence
    if not previous and any(path.exists() or path.is_symlink() for path in (records, evidence)):
        raise WorkbenchError("The consolidated knowledge layout is incomplete. Restore knowledge/evidence/manifest.yaml before continuing.")
    return root / "knowledge", legacy
