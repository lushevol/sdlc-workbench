#!/usr/bin/env python3
"""Read-only, dependency-free repository inventory for AI SDLC Workbench.

Does not execute repository code, contact the network, or copy source content.
"""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
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
    "pyproject.toml", "setup.py", "setup.cfg", "requirements.txt", "pipfile",
    "pipfile.lock", "poetry.lock", "uv.lock",
}
CONFIG_NAMES = {
    "vite.config.ts", "vite.config.js", "webpack.config.js", "webpack.config.ts",
    "rsbuild.config.ts", "rsbuild.config.js", "systemjs.config.js",
    "import-map.json", "application.yml", "application.yaml", "application.properties",
    "azure-pipelines.yml", "azure-pipelines.yaml", "jenkinsfile",
    "dockerfile", "nginx.conf", "single-spa.config.js",
    "chart.yaml", "chart.yml", "chart.lock", "kustomization.yaml", "kustomization.yml", "kustomization",
    "compose.yaml", "compose.yml", "docker-compose.yaml", "docker-compose.yml",
    "pulumi.yaml", "pulumi.yml", "web.config", "app.config", "ldap.conf", "krb5.conf",
    "rabbitmq.conf", "rabbitmq.config", "advanced.config", "server.properties",
    "kafka.properties", "consumer.properties", "producer.properties", "solace.properties", "mq.properties",
    "jdbc.properties", "datasource.properties", "persistence.xml", "hibernate.cfg.xml", "mybatis-config.xml",
    "flyway.conf", "liquibase.properties", "vault.hcl", "consul.hcl", "envoy.yaml",
    "cassandra.yaml", "redis.conf", "mongod.conf", "logback.xml", "logback-spring.xml",
    "log4j2.xml", "log4j2.properties", "otel-collector.yaml", "prometheus.yml",
}
CONFIG_EXTENSIONS = {".yaml", ".yml", ".json", ".toml", ".xml", ".conf", ".properties", ".ini"}
CONFIG_DIRECTORIES = {
    "config", "configuration", "configurations", "helm", "chart", "charts", "kustomize",
    "k8s", "kubernetes", "deploy", "deployment", "deployments", "manifests",
}
MIGRATION_EXTENSIONS = {".sql", ".cql", ".xml", ".yaml", ".yml", ".json", ".java", ".kt", ".js", ".ts", ".py", ".cs"}
MIGRATION_DIRECTORIES = {"migration", "migrations", "changelog", "changelogs", "liquibase"}
CANDIDATE_EXTENSIONS = {".ts", ".tsx", ".js", ".jsx", ".java", ".kt", ".py"}
ENTRYPOINT_BASENAMES = {
    "main.ts", "main.tsx", "index.ts", "index.tsx", "bootstrap.ts",
    "bootstrap.tsx", "single-spa.ts", "single-spa.tsx", "application.java",
    "main.py", "__main__.py", "cli.py",
}
MAX_FILES = 80000
MAX_LIST_ITEMS = 250
COMMIT_ID = re.compile(r"(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})\Z")


def within(base: Path, value: Path) -> bool:
    try:
        return os.path.commonpath((str(base), str(value))) == str(base)
    except ValueError:
        return False


def git(repo: Path, *args: str) -> str | None:
    try:
        # A repository's fsmonitor setting can execute a hook during status.
        # Optional index refreshes must not write to an assessed checkout.
        environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        environment["GIT_OPTIONAL_LOCKS"] = "0"
        result = subprocess.run(
            ["git", "--no-optional-locks", "-c", "core.fsmonitor=false", "-C", str(repo), *args],
            text=True, capture_output=True, check=False, timeout=5, env=environment,
        )
        if result.returncode == 0:
            return result.stdout if "-z" in args else result.stdout.strip()
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        pass
    return None


def candidates(values: list[str], limit: int = MAX_LIST_ITEMS) -> list[str]:
    return sorted(set(values))[:limit]


def configuration_candidate(relative: str) -> bool:
    """Select configuration filenames without opening their contents."""
    path = Path(relative.lower())
    name = path.name
    if name in CONFIG_NAMES:
        return True
    if relative.startswith(".github/workflows/") and path.suffix in {".yml", ".yaml"}:
        return True
    if re.fullmatch(r"(?:application|bootstrap)(?:[-.].+)?\.(?:properties|ya?ml)", name):
        return True
    if name.startswith(("dockerfile.", "docker-compose.", "docker-compose-", "compose.", "compose-")):
        return name.startswith("dockerfile.") or path.suffix in {".yml", ".yaml"}
    if name.endswith((".tf", ".tf.json", ".tfvars", ".tfvars.json")) or name == ".terraform.lock.hcl":
        return True
    if re.fullmatch(r"(?:values|pulumi)(?:[-.].+)?\.ya?ml", name):
        return True
    if re.fullmatch(r"appsettings(?:\..+)?\.json", name):
        return True
    if re.fullmatch(r"(?:next|nuxt|svelte|astro|vitest|playwright)\.config\.[cm]?[jt]s", name):
        return True
    return path.suffix in CONFIG_EXTENSIONS and bool(set(path.parts[:-1]) & CONFIG_DIRECTORIES)


def migration_candidate(relative: str) -> bool:
    """Select migration candidates without implying an active database connection."""
    path = Path(relative.lower())
    if path.suffix not in MIGRATION_EXTENSIONS:
        return False
    return (bool(set(path.parts[:-1]) & MIGRATION_DIRECTORIES)
            or re.fullmatch(r"(?:v[^_]+__|r__).+\.(?:sql|cql|java|kt)", path.name) is not None
            or path.name.startswith(("db.changelog", "changelog.", "changelog-")))


def safe_package_metadata(repo: Path) -> dict:
    path = repo / "package.json"
    if not path.is_file() or path.is_symlink() or path.stat().st_size > 1024 * 1024:
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {}
        dependencies = set()
        for key in ("dependencies", "devDependencies"):
            value = data.get(key, {})
            if not isinstance(value, dict):
                return {"warning": f"package.json {key} must be an object"}
            dependencies.update(value)
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
    root_git = git(repo, "rev-parse", "--show-toplevel")
    if root_git is not None and Path(root_git).resolve() != repo:
        raise ValueError("--repo must identify the Git checkout root, not a subdirectory")
    listed = git(repo, "ls-files", "--cached", "--others", "--exclude-standard", "-z") if root_git is not None else None
    selected_paths = set(listed.split("\x00")) - {""} if listed is not None else None
    selected_directories = set()
    for path in selected_paths or ():
        parts = path.rstrip("/").split("/")
        selected_directories.update("/".join(parts[:n]) for n in range(1, len(parts)))
    found = {k: [] for k in (
        "documentation", "manifests", "configurations", "contract_candidates",
        "migration_candidates", "test_candidates", "entrypoint_candidates", "functional_folder_candidates",
    )}
    count = 0
    warnings = []
    omitted_directories = []
    omitted_files = 0
    visited_directories = set()
    if selected_paths is None:
        warnings.append("Git file selection unavailable; filename fallback cannot exclude all ignored files")
    for current, folders, files in os.walk(repo, topdown=True, followlinks=False):
        here = Path(current)
        rel_dir = here.relative_to(repo).as_posix()
        visited_directories.add(rel_dir)
        admitted = []
        for directory in sorted(folders):
            child = here / directory
            relative = child.relative_to(repo).as_posix()
            reason = None
            if directory in SKIP_DIRS or directory.lower().startswith("secret"):
                reason = "excluded directory category"
            elif child.is_symlink():
                reason = "symlink directory"
            elif (child / ".git").exists():
                reason = "nested Git checkout"
            elif selected_paths is not None and relative not in selected_directories:
                reason = "no files selected by Git"
            if reason is not None:
                omitted_directories.append({"path": relative, "reason": reason})
            else:
                admitted.append(directory)
        folders[:] = admitted
        if rel_dir.startswith("src/features/") and len(Path(rel_dir).parts) == 3:
            found["functional_folder_candidates"].append(rel_dir)
        if rel_dir.startswith("src/modules/") and len(Path(rel_dir).parts) == 3:
            found["functional_folder_candidates"].append(rel_dir)
        for filename in sorted(files):
            p = here / filename
            rel = p.relative_to(repo).as_posix()
            if selected_paths is not None and rel not in selected_paths:
                omitted_files += 1
                continue
            if p.is_symlink() or filename.lower().startswith(SKIP_FILE_PREFIXES) or filename.lower().endswith(SKIP_FILE_SUFFIXES):
                omitted_files += 1
                continue
            count += 1
            if count > MAX_FILES:
                warnings.append(f"inventory stopped after {MAX_FILES} files; repository is too large for exhaustive static enumeration")
                break
            low = filename.lower()
            if low in DOC_NAMES or (rel.startswith("docs/") and low.endswith(".md")):
                found["documentation"].append(rel)
            if low in MANIFEST_NAMES:
                found["manifests"].append(rel)
            if configuration_candidate(rel):
                found["configurations"].append(rel)
            if (low.endswith((".graphql", ".graphqls", ".proto", ".avsc", ".avdl", ".wsdl", ".xsd"))
                or "openapi" in low or "asyncapi" in low or "swagger" in low):
                found["contract_candidates"].append(rel)
            if migration_candidate(rel):
                found["migration_candidates"].append(rel)
            if ("/test/" in "/" + rel or "/tests/" in "/" + rel
                or "/__tests__/" in "/" + rel or low.endswith((".test.ts", ".test.tsx", ".spec.ts", ".spec.tsx", "test.java", "tests.java"))):
                if p.suffix.lower() in CANDIDATE_EXTENSIONS or low.endswith((".feature", ".xml")):
                    found["test_candidates"].append(rel)
            if low in ENTRYPOINT_BASENAMES or (low.endswith("application.java") and "/main/" in "/" + rel):
                if p.suffix.lower() in CANDIDATE_EXTENSIONS:
                    found["entrypoint_candidates"].append(rel)
        if count > MAX_FILES:
            break
    head = git(repo, "rev-parse", "HEAD")
    dirty = git(repo, "status", "--porcelain", "--untracked-files=normal")
    if root_git is None or head is None:
        warnings.append("Git checkout/revision not available; evidence cannot be pinned to a verified commit")
    elif dirty:
        warnings.append("working tree is modified or contains untracked files; source lines may differ from HEAD")
    source_roots = [x for x in ["src/main/java", "src/main/kotlin", "src/main/resources", "src", "app", "packages", "apps", "core"] if x in visited_directories]
    test_roots = [x for x in ["src/test/java", "src/test/kotlin", "src/test", "tests", "test", "e2e"] if x in visited_directories]
    pkg = safe_package_metadata(repo) if selected_paths is None or "package.json" in selected_paths else {}
    stack = pkg.get("stack_signals", []).copy()
    if any(p.endswith("pom.xml") or p.endswith("build.gradle") or p.endswith("build.gradle.kts") for p in found["manifests"]):
        stack.append("jvm-build")
    if any(Path(path).name in {"pyproject.toml", "setup.py", "setup.cfg"} for path in found["manifests"]):
        stack.append("python-build")
    result = {
        "schema_version": "1.0",
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "repository": {
            "name": repo.name,
            "path": str(repo),
            "revision": head if head and COMMIT_ID.fullmatch(head) else "unknown",
            "git_top_level": root_git or "unknown",
            "working_tree_clean": dirty == "" if dirty is not None else None,
        },
        "inventory_scope": {
            "method": "filename-and-manifest-metadata-only",
            "file_selection": "tracked-and-untracked-nonignored-files" if selected_paths is not None else "filesystem-fallback",
            "files_enumerated": min(count, MAX_FILES),
            "enumeration_truncated": count > MAX_FILES,
            "file_limit": MAX_FILES,
            "list_limit": MAX_LIST_ITEMS,
            "category_counts": {
                key: {"matched": len(set(values)), "reported": min(len(set(values)), MAX_LIST_ITEMS),
                      "truncated": len(set(values)) > MAX_LIST_ITEMS}
                for key, values in found.items()
            },
            "skipped_directories": sorted(SKIP_DIRS),
            "omitted_files_in_visited_directories": omitted_files,
            "omitted_directory_count": len(omitted_directories),
            "omitted_directories": omitted_directories[:MAX_LIST_ITEMS],
        },
        "source_roots": source_roots,
        "test_roots": test_roots,
        "stack_signals": sorted(set(stack)),
        "package_metadata": pkg,
        **{k: candidates(v, MAX_LIST_ITEMS) for k, v in found.items()},
        "warnings": warnings,
        "limitations": [
            "Candidate entrypoints, folder names, and contracts are not confirmed business mappings.",
            "Configuration and migration filenames do not establish active dependencies or complete dependency coverage.",
            "No target code was executed; builds, tests, runtime routing and remote dependencies were not verified.",
            "This script does not compute symbol graphs, runtime call graphs or cross-repository ownership.",
            "Ignored files and independent nested Git checkouts are excluded when Git file selection is available.",
        ],
    }
    for key, vals in found.items():
        if len(set(vals)) > MAX_LIST_ITEMS:
            result["warnings"].append(f"{key}: output truncated to {MAX_LIST_ITEMS} paths")
    if len(omitted_directories) > MAX_LIST_ITEMS:
        result["warnings"].append(f"omitted_directories: output truncated to {MAX_LIST_ITEMS} paths")
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
    try:
        result = scan(repo)
    except ValueError as exc:
        parser.error(str(exc))
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote inventory: {dest}")
    print(f"Files inspected: {result['inventory_scope']['files_enumerated']}; revision: {result['repository']['revision']}")
    for warning in result["warnings"]:
        print(f"WARNING: {warning}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
