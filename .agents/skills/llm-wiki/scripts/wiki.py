#!/usr/bin/env python3
"""One linked wiki: OpenKB with URL and token, otherwise the ADE wiki agent."""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
from pathlib import Path
import shutil
import shlex
import subprocess
import sys

VERSION = "0.5.0rc2.dev3+gff54396e5"
REVISION = "ff54396e575ee6feb0113b631a34caa082b441cc"
REQUIREMENT = f"openkb @ git+https://github.com/VectifyAI/OpenKB.git@{REVISION}"
ROOT = Path(__file__).resolve().parents[4]
UPSTREAM = Path(__file__).resolve().parents[1] / "upstream"


def configured_credentials(project):
    """Only explicit KB-local/process credentials select the OpenKB model client."""
    values = {}
    local = project / "knowledge/llm-wiki/.env"
    if local.is_file():
        # These two values are single-line literals; never evaluate shell expansion.
        for line in local.read_text(encoding="utf-8").splitlines():
            key, separator, value = line.strip().removeprefix("export ").partition("=")
            if separator and key.strip() in {"OPENAI_API_BASE", "LLM_API_KEY"}:
                value = value.strip()
                if value.startswith(("'", '"')):
                    try:
                        parts = shlex.split(value, comments=True)
                    except ValueError:
                        raise ValueError("Use a complete single-line quoted credential in the wiki .env") from None
                    value = parts[0] if parts else ""
                else:
                    value = value.split(" #", 1)[0].rstrip()
                values[key.strip()] = value
    return tuple(str(values.get(key) or "").strip() or str(os.environ.get(key) or "").strip()
                 for key in ("OPENAI_API_BASE", "LLM_API_KEY"))


def selected_engine(project):
    url, token = configured_credentials(project)
    return "openkb" if url and token else "llm-wiki-agent"


def validate_api_config(config):
    if str(config.get("model", "")).split("/", 1)[0] in {"chatgpt", "github_copilot"}:
        raise ValueError("Choose an API model compatible with the configured URL/token; automatic OAuth is disabled")
    settings = config.get("litellm") or {}
    if any(key in {"api_base", "api_key", "base_url"} or key.endswith("_key") for key in settings):
        raise ValueError("Configure the URL/token through OPENAI_API_BASE and LLM_API_KEY, not LiteLLM credential overrides")


def agent_handoff(project, operation, source="knowledge/candidates", arguments=()):
    print("Selected engine: llm-wiki-agent (both LLM URL and token were not provided).")
    print("Agent handoff only; no model client was called and no wiki pages were changed.")
    print(f"Current ADE agent: follow {UPSTREAM / 'AGENTS.md'} for {operation}.")
    print(f"Use the single active wiki: {project / 'knowledge/llm-wiki/wiki'}")
    if operation == "compile":
        print(f"Read complete canonical records from: {project / source}")
    if arguments:
        print("Requested arguments: " + " ".join(arguments))
    print("Retain the existing page format: summaries/ holds source summaries; sources/ and raw/ are immutable canonical links.")
    print("Maintain concepts, entities, explorations, contradictions, the index and log in this same wiki; do not create a second wiki.")
    print("Do not run upstream scripted ingest/refresh against linked sources. Reconcile provenance only after successful agent maintenance.")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def runtime_python(project):
    return project / ".venv-openkb" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def command_environment():
    return dict(os.environ, LITELLM_LOCAL_MODEL_COST_MAP="true", PYTHONDONTWRITEBYTECODE="1")


def install(project, requested=None, wheelhouse=None, offline=False):
    python = runtime_python(project)
    uv = shutil.which("uv")
    if not python.exists():
        selected = requested or shutil.which("python3.13") or shutil.which("python3.12")
        if not selected and uv:
            found = subprocess.run([uv, "python", "find", "3.13", "--no-python-downloads"],
                                   capture_output=True, text=True, timeout=30)
            if found.returncode == 0:
                selected = found.stdout.strip()
        selected = selected or sys.executable
        subprocess.run([selected, "-m", "venv", str(python.parent.parent)], check=True, timeout=120)
    installed = subprocess.run([str(python), "-c",
                               "from importlib.metadata import version; print(version('openkb'))"],
                              capture_output=True, text=True, timeout=30)
    if installed.returncode or installed.stdout.strip() != VERSION:
        command = ([uv, "pip", "install", "--python", str(python)] if uv else
                   [str(python), "-m", "pip", "install", "--timeout", "30", "--retries", "1"])
        if wheelhouse:
            command += ["--no-index", "--find-links", str(wheelhouse), f"openkb=={VERSION}"]
        else:
            if offline:
                if not uv:
                    raise ValueError("Offline installation without uv requires --wheelhouse PATH")
                command += ["--offline"]
            command += [REQUIREMENT]
        subprocess.run(command, check=True, timeout=600)
    check = [uv, "pip", "check", "--python", str(python)] if uv else [str(python), "-m", "pip", "check"]
    subprocess.run(check, check=True, timeout=60)
    kb = project / "knowledge/llm-wiki"
    state = kb / ".openkb"
    state.mkdir(parents=True, exist_ok=True)
    config = state / "config.yaml"
    if not config.exists():
        config.write_text("model: openai/gpt-4.1\nlanguage: en\npageindex_threshold: 20\ntimeout: 120\nconcurrency: 2\n", encoding="utf-8")
    elif config.read_text(encoding="utf-8") == "model: chatgpt/gpt-5.4\nlanguage: en\npageindex_threshold: 20\ntimeout: 120\nconcurrency: 2\n":
        config.write_text("model: openai/gpt-4.1\nlanguage: en\npageindex_threshold: 20\ntimeout: 120\nconcurrency: 2\n", encoding="utf-8")
    registry = state / "hashes.json"
    if not registry.exists():
        save_json(registry, {})
    manifest = kb / "source-manifest.json"
    if not manifest.exists():
        save_json(manifest, {"engine": "OpenKB", "version": VERSION, "revision": REVISION, "sources": []})
    for directory in ("raw", "wiki/sources", "wiki/summaries", "wiki/concepts", "wiki/entities", "wiki/explorations"):
        (kb / directory).mkdir(parents=True, exist_ok=True)
    subprocess.run([str(python), "-c",
                    "from pathlib import Path; import sys; from openkb.schema import AGENTS_MD, INDEX_SEED; "
                    "p=Path(sys.argv[1]); "
                    "[(p/name).write_text(text, encoding='utf-8') for name,text in "
                    "[('AGENTS.md',AGENTS_MD),('index.md',INDEX_SEED),('log.md','# Operations Log\\n\\n')] "
                    "if not (p/name).exists()]", str(kb / "wiki")], check=True, timeout=60,
                   env=command_environment())
    print(f"OpenKB {VERSION} installed; workspace: {kb}")
    print("Semantic engine: OpenKB only with OPENAI_API_BASE and LLM_API_KEY; otherwise llm-wiki-agent in the ADE.")


def link_source(link, source):
    link.parent.mkdir(parents=True, exist_ok=True)
    if link.is_symlink():
        if link.resolve() == source.resolve():
            return
        raise ValueError(f"Conflicting source link: {link}")
    if link.exists():
        if digest(link) != digest(source):
            raise ValueError(f"Refusing to replace different source content: {link}")
        link.unlink()
    link.symlink_to(os.path.relpath(source, link.parent))


def compile_sources(project, source):
    url, token = configured_credentials(project)
    if not (url and token):
        raise ValueError("OpenKB compilation requires both OPENAI_API_BASE and LLM_API_KEY; use the llm-wiki-agent ADE workflow")
    from dataclasses import replace
    import yaml
    from openkb.agent.compiler import compile_short_doc
    from openkb.cli import _setup_llm_key
    from openkb.config import resolve_effective_config, resolve_concurrency, resolve_credential_bundle
    from openkb.locks import kb_ingest_lock
    from openkb.log import append_log

    kb = project / "knowledge/llm-wiki"
    folder = (project / source).resolve()
    folder.relative_to(project)
    records = {}
    record_metadata = {}
    record_hashes = {}
    for candidate in sorted(folder.rglob("*.md"), key=lambda p: (-len(p.parts), str(p))):
        if candidate.name in {"README.md", "index.md"}:
            continue
        candidate.resolve().relative_to(project)
        content = candidate.read_bytes()
        text = content.decode("utf-8")
        source_hash = hashlib.sha256(content).hexdigest()
        if not text.startswith("---\n"):
            raise ValueError(f"Canonical record lacks metadata: {candidate}")
        metadata = yaml.safe_load(text.partition("\n")[2].split("\n---", 1)[0])
        identifier = metadata.get("id") if isinstance(metadata, dict) else None
        if not isinstance(identifier, str) or not identifier.strip():
            raise ValueError(f"Canonical record lacks an id: {candidate}")
        if identifier in records:
            if record_hashes[identifier] != source_hash:
                raise ValueError(f"Conflicting canonical records for {identifier}")
            continue
        records[identifier] = candidate
        record_metadata[identifier] = metadata
        record_hashes[identifier] = source_hash
    if not records:
        raise ValueError(f"No canonical records in {folder}")
    if len({path.stem for path in records.values()}) != len(records):
        raise ValueError("Canonical filename collision; use unique filenames before compilation")
    config = resolve_effective_config(kb)[0]
    validate_api_config(config)
    _setup_llm_key(kb)
    bundle = replace(resolve_credential_bundle(kb), base_url=url, api_key=token)
    manifest_path = kb / "source-manifest.json"
    registry_path = kb / ".openkb/hashes.json"
    with kb_ingest_lock(kb / ".openkb"):
        manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {"engine": "OpenKB", "sources": []}
        bindings = {record["doc_name"]: record for record in manifest["sources"]}
        registry = json.loads(registry_path.read_text())
        for identifier, original in records.items():
            before = digest(original)
            if before != record_hashes[identifier]:
                raise ValueError(f"Source changed before compilation; rescan it: {original}")
            raw = kb / "raw" / original.name
            full_text = kb / "wiki/sources" / original.name
            link_source(raw, original)
            link_source(full_text, original)
            # Use the native semantic compiler; conversion would duplicate or replace canonical links.
            asyncio.run(compile_short_doc(original.stem, full_text, kb, config["model"],
                                          max_concurrency=resolve_concurrency(config) or 2,
                                          bundle=bundle))
            if digest(original) != before:
                raise ValueError(f"Source changed during compilation; binding not advanced: {original}")
            registry = {key: value for key, value in registry.items() if value.get("doc_name") != original.stem}
            registry[before] = {"name": original.name, "doc_name": original.stem, "type": "md",
                                "path": f"raw/{original.name}", "raw_path": f"raw/{original.name}",
                                "source_path": f"wiki/sources/{original.name}"}
            bindings[original.stem] = {"doc_name": original.stem, "id": identifier,
                                       "origin": original.relative_to(project).as_posix(), "sha256": before,
                                       **{key: record_metadata[identifier][key]
                                          for key in ("version", "status", "governance_state")
                                          if key in record_metadata[identifier]}}
            manifest["sources"] = list(bindings.values())
            save_json(registry_path, registry)
            save_json(manifest_path, manifest)
            append_log(kb / "wiki", "ingest", f"OpenKB semantic compilation: {original.name}")
            print(f"Compiled {original.name}")


def verify(project):
    from importlib.metadata import version
    from openkb.lint import (find_broken_links, check_index_sync, find_orphans,
                             find_missing_entries, find_invalid_frontmatter,
                             find_missing_okf_fields, run_structural_lint)

    if version("openkb") != VERSION:
        raise ValueError(f"Expected OpenKB {VERSION}; run install")
    kb = project / "knowledge/llm-wiki"
    manifest = json.loads((kb / "source-manifest.json").read_text())
    registry = json.loads((kb / ".openkb/hashes.json").read_text())
    for record in manifest["sources"]:
        original = project / record["origin"]
        original.resolve().relative_to(project)
        if digest(original) != record["sha256"]:
            raise ValueError(f"Compiled source binding is stale: {original}; compile it before advancing the hash")
        for relative in (f"raw/{original.name}", f"wiki/sources/{original.name}"):
            link = kb / relative
            if not link.is_symlink() or link.resolve() != original.resolve():
                raise ValueError(f"Expected canonical source link: {link}")
        if registry.get(record["sha256"], {}).get("doc_name") != record["doc_name"]:
            raise ValueError(f"OpenKB registry mismatch: {record['doc_name']}")
    wiki = kb / "wiki"
    errors = (find_broken_links(wiki) + check_index_sync(wiki) + find_orphans(wiki)
              + find_missing_entries(kb / "raw", wiki, kb_dir=kb)
              + find_invalid_frontmatter(wiki) + find_missing_okf_fields(wiki))
    print(run_structural_lint(kb))
    if errors:
        raise ValueError("OpenKB structural findings: " + "; ".join(errors))
    print(f"Verified OpenKB {VERSION}; {len(manifest['sources'])} unchanged linked canonical sources")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    installer = commands.add_parser("install")
    installer.add_argument("--python")
    installer.add_argument("--wheelhouse", type=Path)
    installer.add_argument("--offline", action="store_true")
    commands.add_parser("verify")
    commands.add_parser("graph")
    commands.add_parser("engine", help="Show the selected semantic engine without exposing credentials")
    compiler = commands.add_parser("compile", help="Run the original OpenKB semantic compiler on linked canonical records")
    compiler.add_argument("--source", default="knowledge/candidates")
    native = commands.add_parser("run")
    native.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    project = args.project.resolve()
    if args.command == "install":
        install(project, args.python, args.wheelhouse, args.offline)
        return
    python = runtime_python(project)
    if python.exists() and Path(sys.prefix).resolve() != python.parent.parent.resolve():
        subprocess.run([str(python), str(Path(__file__).resolve()), *sys.argv[1:]],
                       check=True, env=command_environment())
        return
    kb = project / "knowledge/llm-wiki"
    if args.command == "run" and (not args.arguments or args.arguments[0].startswith("-") or
            args.arguments[0] in {"add", "remove", "watch", "init", "recompile", "use", "delete-kb", "chat"}):
        raise ValueError("For linked canonical records use compile; edit/publish sources through Workbench ingestion and governance")
    if args.command == "engine":
        url, token = configured_credentials(project)
        print(json.dumps({"engine": selected_engine(project), "url_configured": bool(url),
                          "token_configured": bool(token), "workspace": str(kb)}))
        return
    semantic = args.command == "compile" or (args.command == "run" and args.arguments
                                               and args.arguments[0] not in {"status", "list", "visualize"})
    if semantic and selected_engine(project) == "llm-wiki-agent":
        operation = "compile" if args.command == "compile" else args.arguments[0]
        agent_handoff(project, operation, getattr(args, "source", "knowledge/candidates"),
                      args.arguments[1:] if args.command == "run" else ())
        return
    if not python.exists():
        raise ValueError("Local OpenKB schema/graph environment missing; run install first")
    if args.command == "verify":
        verify(project)
    elif args.command == "compile":
        compile_sources(project, args.source)
    else:
        arguments = ["visualize", "--no-open"] if args.command == "graph" else args.arguments
        from openkb.cli import cli
        if semantic:
            from openkb.config import resolve_effective_config
            import litellm
            validate_api_config(resolve_effective_config(kb)[0])
            url, token = configured_credentials(project)
            os.environ.update(OPENAI_API_BASE=url, OPENAI_BASE_URL=url, LLM_API_KEY=token)
            litellm.api_base = url
            litellm.api_key = token
        cli.main(args=["--kb-dir", str(kb), *arguments], standalone_mode=False)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(f"OpenKB: {error}", file=sys.stderr)
        sys.exit(1)
