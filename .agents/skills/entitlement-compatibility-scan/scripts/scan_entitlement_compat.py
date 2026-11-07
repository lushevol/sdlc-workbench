#!/usr/bin/env python3
"""Find high-recall EMS2/CES compatibility candidates without executing target code."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SKIP_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "target",
    ".next",
    "coverage",
    ".turbo",
    "vendor",
}

PATTERNS = [
    ("identity-cardinality", r"\b(roleList|roleName|roleId|role)\b|getUser\(\)\s*\.\s*role"),
    ("legacy-projection", r"X_RATANONE|user\.entitlements|entitlementsToken|dataEntitlementRoles|roleName"),
    ("action-parity", r"hasPermission\s*\(|F_Input_Delete_Modify|ACCESS_[A-Z_]+|subject\s*:\s*action"),
    ("ownership", r"\b(assignee|assigneeList|moduleOwner|owner|creator)\b|saved.?view|saved.?filter"),
    ("tile-routing", r"EMS2|EMS3|CES|entitlementRouting|applicationId|applicationName|tileId|tile_id"),
    ("data-scope", r"data[_-]profiles?|data[_-]policies?|dataEntitlementRoles|authorization.?limit|PSS_RO"),
    ("admin-token", r"FMO\s+PORTAL\s+ADMIN|role_entitlements|importmap|category|empty|undefined|throw"),
    ("lifecycle-cache", r"module.?level|useMemo|useCallback|const\s+\w+\s*=\s*hasPermission|cached|cache"),
    ("configuration-alias", r"feature.?flag|entitlements?\s*[:=]|subject.?alias|blank.?feature"),
    ("verification", r"roleList|roleName|X_RATANONE|entitlement|CES|EMS3|EMS2"),
]

TEXT_SUFFIXES = {
    ".c",
    ".cc",
    ".cpp",
    ".cs",
    ".go",
    ".java",
    ".js",
    ".jsx",
    ".json",
    ".kt",
    ".md",
    ".py",
    ".rb",
    ".ts",
    ".tsx",
    ".yml",
    ".yaml",
    ".xml",
}


def files_under(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        yield path


def git_state(root: Path):
    git_dir = root / ".git"
    if git_dir.exists():
        head = "available"
        try:
            import subprocess

            head = subprocess.check_output(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        except Exception:
            pass
        return {"git": True, "revision": head}
    return {"git": False, "revision": None}


def scan(root: Path):
    compiled = [(category, re.compile(pattern, re.IGNORECASE)) for category, pattern in PATTERNS]
    findings = []
    file_count = 0
    for path in files_under(root):
        file_count += 1
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        relative = str(path.relative_to(root))
        is_test_file = bool(re.search(r"(^|[./])[^/]+\.(test|spec)\.[^.]+$", relative, re.I))
        for line_number, line in enumerate(lines, 1):
            for category, pattern in compiled:
                if category == "verification" and not is_test_file:
                    continue
                match = pattern.search(line)
                if match:
                    findings.append(
                        {
                            "category": category,
                            "file": relative,
                            "line": line_number,
                            "text": line.strip()[:240],
                            "test_file": is_test_file,
                        }
                    )
    return {
        "repository": str(root),
        "state": git_state(root),
        "inventory": {"files": file_count, "excluded_directories": sorted(SKIP_DIRS)},
        "findings": findings,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repositories", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = {
        "tool": "entitlement-compatibility-scan",
        "version": 1,
        "repositories": [scan(repo.resolve()) for repo in args.repositories],
        "limits": [
            "Static high-recall matches do not prove reachability or incompatibility.",
            "Generated, dependency, and build directories are excluded.",
            "No live API, deployment, or runtime behavior is checked.",
        ],
    }
    rendered = json.dumps(payload, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
