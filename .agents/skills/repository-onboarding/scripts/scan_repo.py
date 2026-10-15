#!/usr/bin/env python3
"""Read-only, dependency-free repository inventory for ADE onboarding.

Does not execute repository code, contact the network, or copy source content.
"""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import subprocess
import sys

SKIP_DIRS = {
    ".git", ".svn", ".hg", ".idea", ".vscode", ".next", ".nuxt",
    ".turbo", ".gradle", ".mvn", ".venv", "venv", "node_modules",
    "dist", "build", "target", "coverage", "out", "vendor", "__pycache__",
    ".cache", ".pytest_cache", "tmp", "temp", "logs", ".pnpm-store",
}
SKIP_FILE_PREFIXES = (".env",)
SKIP_FILE_SUFFIXES = (
    ".pem", ".key", ".p12", ".pfx", ".jks", ".keystore", ".crt",
    ".cer", ".der", ".asc", ".log", ".map", ".class", ".jar",
    ".zip", ".tar", ".gz", ".png", ".jpg", ".jpeg", ".gif",
    ".pdf", ".xlsx", ".docx", ".parquet", ".db", ".sqlite",
)
DOC_NAMES = {"readme.md", "agents.md", "claude.md", "contributing.md", "architecture.md"}
MANIFEST_NAMES = {
    "package.json", "pnpm-workspace.yaml", "pnpm-lock.yaml", "yarn.lock",
    "package-lock.json", "pom.xml", "build.gradle", "build.gradle.kts",
    "settings.gradle", "settings.gradle.kts", "gradlew", "mvnw",
    "tsconfig.json", "turbo.json", "rush.json", "nx.json",
}
CONFIG_NAMES = {
    "vite.config.ts", "vite.config.js", "webpack.config.js", "webpack.config.ts",
    "rsbuild.config.ts", "rsbuild.config.js", "systemjs.config.js",
    "import-map.json", "application.yml", "application.yaml", "application.properties",
    "azure-pipelines.yml", "azure-pipelines.yaml", "jenkinsfile",
    "dockerfile", "nginx.conf", "single-spa.config.js",
}
CANDIDATE_EXTENSIONS = {".ts", ".tsx", ".js", ".jsx", ".java", ".kt", ".py"}
ENTRYPOINT_BASENAMES = {
    "main.ts", "main.tsx", "index.ts", "index.tsx", "bootstrap.ts",
    "bootstrap.tsx", "single-spa.ts", "single-spa.tsx", "application.java",
}
MAX_FILES = 80000
MAX_LIST_ITEMS = 250


def within(base: Path, value: Path) -> bool:
    try:
        return os.path.commonpath((str(base), str(value))) == str(base)
    except ValueError:
        return False


def git(repo: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args], text=True, capture_output=True,
            check=False, timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        pass
    return None


def candidates(values: list[str], limit: int = MAX_LIST_ITEMS) -> list[str]:
    return sorted(set(values))[:limit]


def safe_package_metadata(repo: Path) -> dict:
    path = repo / "package.json"
    if not path.is_file() or path.is_symlink() or path.stat().st_size > 1024 * 1024:
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {}
        dependencies = set(data.get("dependencies") or {}) | set(data.get("devDependencies") or {})
        names = [
            "react", "single-spa", "systemjs", "vite", "typescript", "redux",
            "@reduxjs/toolkit", "antd", "@mui/material", "@module-federation/enhanced",
            "@rsbuild/core", "@apollo/client", "graphql", "@tanstack/react-query",
        ]
        return {
            "package_name": data.get("name") if isinstance(data.get("name"), str) else None,
            "script_names": sorted((data.get("scripts") or {}).keys()) if isinstance(data.get("scripts"), dict) else [],
            "stack_signals": [name for name in names if name in dependencies],
        }
    except (OSError, ValueError, UnicodeError):
        return {"warning": "package.json metadata could not be parsed"}


def scan(repo: Path) -> dict:
    found = {k: [] for k in (
        "documentation", "manifests", "configurations", "contract_candidates",
        "test_candidates", "entrypoint_candidates", "functional_folder_candidates",
    )}
    count = 0
    warnings = []
    for current, folders, files in os.walk(repo, topdown=True, followlinks=False):
        here = Path(current)
        folders[:] = sorted(
            d for d in folders
            if d not in SKIP_DIRS and not (here / d).is_symlink()
            and not d.lower().startswith("secret")
        )
        rel_dir = here.relative_to(repo).as_posix()
        if rel_dir.startswith("src/features/") and len(Path(rel_dir).parts) == 3:
            found["functional_folder_candidates"].append(rel_dir)
        if rel_dir.startswith("src/modules/") and len(Path(rel_dir).parts) == 3:
            found["functional_folder_candidates"].append(rel_dir)
        for filename in sorted(files):
            p = here / filename
            if p.is_symlink() or filename.lower().startswith(SKIP_FILE_PREFIXES) or filename.lower().endswith(SKIP_FILE_SUFFIXES):
                continue
            count += 1
            if count > MAX_FILES:
                warnings.append(f"inventory stopped after {MAX_FILES} files; repository is too large for exhaustive static enumeration")
                break
            rel = p.relative_to(repo).as_posix()
            low = filename.lower()
            if low in DOC_NAMES or (rel.startswith("docs/") and low.endswith(".md")):
                found["documentation"].append(rel)
            if low in MANIFEST_NAMES:
                found["manifests"].append(rel)
            if low in CONFIG_NAMES or (rel.startswith(".github/workflows/") and low.endswith((".yml", ".yaml"))):
                found["configurations"].append(rel)
            if (low.endswith((".graphql", ".graphqls", ".proto", ".avsc"))
                or "openapi" in low or "asyncapi" in low or "swagger" in low):
                found["contract_candidates"].append(rel)
            if ("/test/" in "/" + rel or "/tests/" in "/" + rel
                or "/__tests__/" in "/" + rel or low.endswith((".test.ts", ".test.tsx", ".spec.ts", ".spec.tsx", "test.java", "tests.java"))):
                if p.suffix.lower() in CANDIDATE_EXTENSIONS or low.endswith((".feature", ".xml")):
                    found["test_candidates"].append(rel)
            if low in ENTRYPOINT_BASENAMES or (low.endswith("application.java") and "/main/" in "/" + rel):
                if p.suffix.lower() in CANDIDATE_EXTENSIONS:
                    found["entrypoint_candidates"].append(rel)
        if count > MAX_FILES:
            break
    root_git = git(repo, "rev-parse", "--show-toplevel")
    head = git(repo, "rev-parse", "HEAD")
    dirty = git(repo, "status", "--porcelain", "--untracked-files=normal")
    if root_git is None or head is None:
        warnings.append("Git checkout/revision not available; evidence cannot be pinned to a verified commit")
    elif dirty:
        warnings.append("working tree is modified or contains untracked files; source lines may differ from HEAD")
    source_roots = [x for x in ["src/main/java", "src/main/kotlin", "src/main/resources", "src", "app", "packages", "apps"] if (repo / x).is_dir()]
    test_roots = [x for x in ["src/test/java", "src/test/kotlin", "src/test", "tests", "test", "e2e"] if (repo / x).is_dir()]
    pkg = safe_package_metadata(repo)
    stack = pkg.get("stack_signals", []).copy()
    if any(p.endswith("pom.xml") or p.endswith("build.gradle") or p.endswith("build.gradle.kts") for p in found["manifests"]):
        stack.append("jvm-build")
    result = {
        "schema_version": "1.0",
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "repository": {
            "name": repo.name,
            "path": str(repo),
            "revision": head if head and len(head) == 40 else "unknown",
            "git_top_level": root_git or "unknown",
            "working_tree_clean": dirty == "" if dirty is not None else None,
        },
        "inventory_scope": {
            "method": "filename-and-manifest-metadata-only",
            "files_enumerated": min(count, MAX_FILES),
            "skipped_directories": sorted(SKIP_DIRS),
        },
        "source_roots": source_roots,
        "test_roots": test_roots,
        "stack_signals": sorted(set(stack)),
        "package_metadata": pkg,
        **{k: candidates(v) for k, v in found.items()},
        "warnings": warnings,
        "limitations": [
            "Candidate entrypoints, folder names, and contracts are not confirmed business mappings.",
            "No target code was executed; builds, tests, runtime routing and remote dependencies were not verified.",
            "This script does not compute symbol graphs, runtime call graphs or cross-repository ownership.",
        ],
    }
    for key, vals in found.items():
        if len(set(vals)) > MAX_LIST_ITEMS:
            result["warnings"].append(f"{key}: output truncated to {MAX_LIST_ITEMS} paths")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="Target local repository checkout")
    parser.add_argument("--output", required=True, help="JSON inventory path, outside target repository")
    args = parser.parse_args()
    repo = Path(args.repo).expanduser().resolve()
    dest = Path(args.output).expanduser().resolve()
    if not repo.is_dir():
        parser.error(f"repository path not found: {repo}")
    if within(repo, dest):
        parser.error("output must be outside the target repository")
    result = scan(repo)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote inventory: {dest}")
    print(f"Files inspected: {result['inventory_scope']['files_enumerated']}; revision: {result['repository']['revision']}")
    for warning in result["warnings"]:
        print(f"WARNING: {warning}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
