#!/usr/bin/env python3
"""Workbench launcher for a complete, unmodified llm-wiki-agent snapshot."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from datetime import date
from urllib.parse import unquote, urlsplit

SKILL = Path(__file__).resolve().parents[1]
UPSTREAM = SKILL / "upstream"
LOCK = SKILL / "upstream-lock.json"
TOOLS = ("ingest", "query", "lint", "health", "heal", "refresh", "build_graph",
         "file_to_md", "pdf2md")
LINK = re.compile(r"(?<!!)\[([^\]\n]+)\]\(([^)\s]+)\)")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_lock():
    return json.loads(LOCK.read_text(encoding="utf-8"))


def verify_source(root, complete=True):
    files = load_lock()["files"]
    expected = {p: h for p, h in files.items()
                if complete or p.split("/")[0] not in {"wiki", "raw", "graph"}}
    bad = [p for p, h in expected.items()
           if not (root / p).is_file() or digest(root / p) != h]
    if complete:
        actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
        bad.extend(sorted(actual - set(expected)))
    if bad:
        raise ValueError(f"Upstream integrity mismatch in {root}: {', '.join(bad)}")
    return len(expected)


def prepare(project):
    verify_source(UPSTREAM)
    runtime = project / "knowledge/llm-wiki"
    for name, expected_hash in load_lock()["files"].items():
        target = runtime / name
        is_data = name.split("/")[0] in {"wiki", "raw", "graph"}
        if target.exists():
            if not is_data and digest(target) != expected_hash:
                raise ValueError(f"Runtime source was edited: {target}; preserve your edit before reinstalling")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(UPSTREAM / name, target)
    return runtime


def env_python(project):
    return project / ".venv-llm-wiki" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def compatible(executable):
    result = subprocess.run([str(executable), "-c",
                             "import sys; print('.'.join(map(str, sys.version_info[:2])))"],
                            capture_output=True, text=True, timeout=15)
    return result.returncode == 0 and (3, 11) <= tuple(map(int, result.stdout.strip().split('.'))) < (3, 14)


def select_python(requested):
    if requested:
        candidates = [requested]
    else:
        candidates = [shutil.which(f"python3.{v}") for v in (13, 12, 11)] + [sys.executable]
        if shutil.which("uv"):
            found = subprocess.run(["uv", "python", "find", "3.13", "--no-python-downloads"],
                                   capture_output=True, text=True, timeout=30)
            if found.returncode == 0:
                candidates.insert(0, found.stdout.strip())
    for candidate in filter(None, candidates):
        if compatible(candidate):
            return str(candidate)
    raise ValueError("Use install --python PATH with Python 3.11-3.13 (upstream NetworkX requires >=3.11)")


def install(project, requested):
    runtime = prepare(project)
    python = env_python(project)
    uv = shutil.which("uv")
    if not python.exists():
        selected = select_python(requested)
        command = ([uv, "venv", "--python", selected, str(python.parent.parent)] if uv else
                   [selected, "-m", "venv", str(python.parent.parent)])
        subprocess.run(command, check=True, timeout=120)
    if not compatible(python):
        raise ValueError(f"{python} must use Python 3.11-3.13")
    if uv:
        command = [uv, "pip", "install", "--python", str(python), "-r", str(UPSTREAM / "requirements.txt"),
                   "-r", str(UPSTREAM / "pyproject.toml")]
    else:
        dependencies = json.loads(subprocess.check_output(
            [str(python), "-c", "import json,tomllib,sys; print(json.dumps(tomllib.load(open(sys.argv[1],'rb'))['project']['dependencies']))",
             str(UPSTREAM / "pyproject.toml")], text=True))
        command = [str(python), "-m", "pip", "install", "--timeout", "30", "--retries", "1",
                   "-r", str(UPSTREAM / "requirements.txt"), *dependencies]
    subprocess.run(command, check=True, timeout=600)
    check = [uv, "pip", "check", "--python", str(python)] if uv else [str(python), "-m", "pip", "check"]
    subprocess.run(check, check=True, timeout=60)
    subprocess.run([str(python), "-c", "import litellm,networkx,markitdown,tqdm; print('All upstream dependency groups import successfully')"],
                   check=True, timeout=60)
    print(f"Installed upstream {load_lock()['revision']}\nRuntime: {runtime}\nPython: {python}")


def page_target(relative):
    parts = relative.parts
    if relative.as_posix() == "overview/index.md":
        return Path("overview.md")
    kind = parts[0] if parts[0] in {"sources", "entities", "concepts", "syntheses"} else "syntheses"
    stem = "-".join(parts[:-1] if relative.name == "index.md" else (*parts[:-1], relative.stem))
    slug = re.sub(r"[^a-z0-9-]+", "-", stem.lower()).strip("-") or "knowledge-map"
    return Path(kind) / f"wb-{slug}.md"


def candidate_page_target(relative):
    stem = "-".join((*relative.parts[:-1], relative.stem))
    slug = re.sub(r"[^a-z0-9-]+", "-", stem.lower()).strip("-") or "knowledge-record"
    return Path("sources") / f"wb-candidate-{slug}.md"


def strip_frontmatter(content):
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end >= 0:
            return content[end + len("\n---"):].lstrip("\n")
    return content


def frontmatter_value(content, key):
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", content, re.MULTILINE)
    return match.group(1).strip().strip("\"'") if match else ""


def export(project, source_path=None):
    runtime = prepare(project)
    source = (project / (source_path or Path("knowledge/candidates"))).resolve()
    source_rel = source.relative_to(project)
    is_candidate_export = source_rel == Path("knowledge/candidates")
    pages = sorted(p for p in source.rglob("*.md")
                   if p.name not in {"README.md", "index.md"})
    if not pages:
        raise ValueError(f"No wiki pages to export from {source}")
    mapping = {p.resolve(): runtime / "wiki" /
               (candidate_page_target(p.relative_to(source)) if is_candidate_export
                else page_target(p.relative_to(source))) for p in pages}
    if len(set(mapping.values())) != len(mapping):
        raise ValueError("Wiki export filename collision")
    manifest_path = runtime / "export-manifest.json"
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    managed = previous.get("managed", {})
    for name, expected in managed.items():
        target = runtime / name
        if target.exists() and digest(target) != expected:
            raise ValueError(f"Export-managed page was edited: {target}; reconcile it before export")

    outputs, raw_links, entries, records = {}, {}, [], {}
    today = date.today().isoformat()
    for original, target in mapping.items():
        content = original.read_text(encoding="utf-8")
        relative = original.relative_to(project).as_posix()
        title_match = re.search(r"^# (.+)$", content, re.MULTILINE)
        title = title_match.group(1) if title_match else original.stem

        def replace(match):
            label, href = match.groups()
            url = urlsplit(href)
            if url.scheme or url.netloc or not url.path:
                return match.group(0)
            linked = (original.parent / unquote(url.path)).resolve()
            if linked in mapping:
                return f"{label} ([[{mapping[linked].stem}]])"
            if linked.is_file() and linked.is_relative_to(project):
                name = linked.relative_to(project).as_posix()
                records[name] = digest(linked)
            rebased = os.path.relpath(linked, target.parent).replace(os.sep, "/")
            return f"[{label}]({rebased}{'#' + url.fragment if url.fragment else ''})"

        body = LINK.sub(replace, strip_frontmatter(content) if is_candidate_export else content)
        raw = Path("raw/workbench") / source_rel / original.relative_to(source)
        kind = "source" if is_candidate_export else {"sources": "source", "entities": "entity", "concepts": "concept"}.get(target.parent.name, "synthesis")
        status = "candidate-derived" if is_candidate_export else "derived-not-approved"
        candidate_fields = ""
        if is_candidate_export:
            candidate_fields = (f"candidate_id: {frontmatter_value(content, 'id')}\n"
                                f"candidate_version: {frontmatter_value(content, 'version')}\n"
                                f"candidate_governance_state: {frontmatter_value(content, 'governance_state')}\n"
                                f"candidate_status: {frontmatter_value(content, 'status')}\n"
                                f"candidate_classification: {frontmatter_value(content, 'classification')}\n")
        header = (f"---\ntitle: {json.dumps(title, ensure_ascii=False)}\ntype: {kind}\n"
                  "tags: []\nsources: []\n"
                  f"source_file: {raw.as_posix()}\nsource: {raw.as_posix()}\n"
                  f"source_hash: {digest(original)[:16]}\nlast_updated: {today}\n"
                  f"{candidate_fields}"
                  f"workbench_origin: {relative}\nworkbench_sha256: {digest(original)}\n"
                  f"workbench_status: {status}\n---\n\n")
        outputs[target] = header + body
        raw_links[runtime / raw] = original
        entries.append({"origin": relative, "sha256": digest(original),
                        "page": target.relative_to(runtime).as_posix(), "raw": raw.as_posix(), "title": title})

    for target, content in outputs.items():
        name = target.relative_to(runtime).as_posix()
        # The shipped overview is an editable scaffold in the operational copy only.
        scaffold = name == "wiki/overview.md" and digest(target) == load_lock()["files"].get(name) if target.exists() else False
        if target.exists() and name not in managed and not scaffold and target.read_text(encoding="utf-8") != content:
            raise ValueError(f"Export would overwrite an unmanaged page: {target}")
    for target in raw_links:
        name = target.relative_to(runtime).as_posix()
        if name in managed and target.exists() and digest(target) != managed[name]:
            raise ValueError(f"Raw source link target was edited: {target}; reconcile it before export")
    managed_targets = set(outputs) | set(raw_links)
    for name in set(managed) - {p.relative_to(runtime).as_posix() for p in managed_targets}:
        (runtime / name).unlink(missing_ok=True)
    for target, content in outputs.items():
        write(target, content)
    for target, original in raw_links.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.unlink(missing_ok=True)
        target.symlink_to(os.path.relpath(original, target.parent))

    if is_candidate_export:
        overview = runtime / "wiki/overview.md"
        overview_lines = [
            "---", 'title: "Candidate knowledge overview"', "type: synthesis",
            "tags: []", "sources: []", f"last_updated: {today}",
            "workbench_status: candidate-derived", "---", "",
            "# Candidate knowledge overview", "",
            "This native wiki is generated from `knowledge/candidates/`.",
            "Every source page remains candidate or draft knowledge pending confirmation.",
            "", "## Candidate records", "",
        ]
        overview_lines.extend(f"- [[{target.stem}]]" for target in sorted(mapping.values()))
        write(overview, "\n".join(overview_lines) + "\n")

    index = runtime / "wiki/index.md"
    # Reconcile the catalog with every native page, including independently ingested pages.
    index_pages = sorted(p for p in (runtime / "wiki").rglob("*.md")
                         if p.name not in {"index.md", "log.md", "lint-report.md"})
    write(index, "# Wiki Index\n\nDerived knowledge; lifecycle and canonical authority remain with the cited records.\n\n" +
          "\n".join(f"- [{p.stem}]({p.relative_to(runtime / 'wiki').as_posix()})" for p in index_pages) + "\n")
    log = runtime / "wiki/log.md"
    existing_log = log.read_text(encoding="utf-8")
    previous_references = previous.get("referenced_files", previous.get("canonical_records", {}))
    if previous.get("pages") != entries or previous_references != records:
        for entry in entries:
            if entry["page"].startswith("wiki/sources/"):
                existing_log += f"\n## [{today}] ingest | {entry['title']}\n\nWorkbench export of `{entry['origin']}`; existing derived content, no LLM invocation.\n"
        if is_candidate_export:
            existing_log += f"\n## [{today}] export | Candidate knowledge base\n\nGenerated from `{source_rel.as_posix()}`; candidate records remain unconfirmed.\n"
        write(log, existing_log)
    manifest = {"upstream_revision": load_lock()["revision"], "pages": entries,
                "source_class": "candidate" if is_candidate_export else "workbench",
                "referenced_files": records,
                "managed": {p.relative_to(runtime).as_posix(): digest(p) for p in managed_targets}}
    write(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(f"Exported {len(entries)} native pages; {len(records)} referenced files; originals unchanged")


def run_tool(project, tool, args):
    runtime = prepare(project)
    python = env_python(project)
    if not python.exists():
        raise ValueError("Run wiki.py install first")
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", LITELLM_LOCAL_MODEL_COST_MAP="True")
    return subprocess.run([str(python), str(runtime / "tools" / f"{tool}.py"), *args],
                          cwd=runtime, env=environment).returncode


def verify(project):
    count = verify_source(UPSTREAM)
    runtime = project / "knowledge/llm-wiki"
    if runtime.exists():
        verify_source(runtime, complete=False)
    manifest = runtime / "export-manifest.json"
    if manifest.exists():
        exported = json.loads(manifest.read_text())
        if exported.get("upstream_revision") != load_lock()["revision"]:
            raise ValueError("Export was generated by a different upstream revision; run export")
        for name, expected in exported["managed"].items():
            if not (runtime / name).is_file() or digest(runtime / name) != expected:
                raise ValueError(f"Export page changed: {name}; reconcile before refreshing")
        references = exported.get("referenced_files", exported.get("canonical_records", {}))
        inputs = {p["origin"]: p["sha256"] for p in exported["pages"]} | references
        for name, expected in inputs.items():
            if not (project / name).is_file() or digest(project / name) != expected:
                raise ValueError(f"Wiki export is stale: {name}; run export")
    graph = runtime / "graph/graph.json"
    if graph.exists():
        data = json.loads(graph.read_text())
        nodes = {n["id"] for n in data["nodes"]}
        if not nodes or not data["edges"]:
            raise ValueError("Native graph is empty")
        if any(e["from"] not in nodes or e["to"] not in nodes for e in data["edges"]):
            raise ValueError("Native graph contains dangling endpoints")
        if manifest.exists():
            expected_nodes = {p["page"][5:-3] for p in exported["pages"]}
            if not expected_nodes <= nodes:
                raise ValueError(f"Native graph is missing exported pages: {expected_nodes - nodes}")
        print(f"Native graph: {len(nodes)} nodes, {len(data['edges'])} edges")
    print(f"Verified {count} pristine upstream files at {load_lock()['revision']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=SKILL.parents[2], help="Workbench project root")
    sub = parser.add_subparsers(dest="command", required=True)
    setup = sub.add_parser("install", help="Install both original dependency groups and prepare native workspace")
    setup.add_argument("--python", help="Python 3.11-3.13 interpreter")
    export_command = sub.add_parser("export", help="Export a Workbench source tree into native upstream format")
    export_command.add_argument("--source", type=Path, default=Path("knowledge/candidates"),
                                help="Source tree; defaults to knowledge/candidates")
    sub.add_parser("verify", help="Verify pristine source, export freshness and native graph coverage")
    graph = sub.add_parser("graph", help="Run ORIGINAL tools/build_graph.py; all options pass through")
    graph.add_argument("args", nargs=argparse.REMAINDER)
    run = sub.add_parser("run", help="Run any original upstream tool; relative paths use native workspace")
    run.add_argument("tool", choices=TOOLS)
    run.add_argument("args", nargs=argparse.REMAINDER)
    args, extra = parser.parse_known_args()
    project = args.project.resolve()
    os.environ.setdefault("UV_CACHE_DIR", str(project / ".workbench/llm-wiki/uv-cache"))
    os.environ.setdefault("UV_HTTP_TIMEOUT", "30")
    os.environ.setdefault("UV_HTTP_RETRIES", "1")
    if args.command not in {"graph", "run"} and extra:
        parser.error("unrecognized arguments: " + " ".join(extra))
    try:
        if args.command == "install":
            install(project, args.python)
        elif args.command == "export":
            export(project, args.source)
        elif args.command == "verify":
            verify(project)
        else:
            return run_tool(project, "build_graph" if args.command == "graph" else args.tool, extra + args.args)
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
