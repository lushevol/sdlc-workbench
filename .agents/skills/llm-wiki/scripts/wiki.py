#!/usr/bin/env python3
"""One linked wiki: OpenKB with URL and token, otherwise the ADE wiki agent."""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import importlib.util
import json
import os
import posixpath
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import shutil
import shlex
import subprocess
import sys
import tempfile
from datetime import datetime
import uuid
from urllib.parse import unquote, urlsplit

VERSION = "0.5.0rc2.dev3+gff54396e5"
REVISION = "ff54396e575ee6feb0113b631a34caa082b441cc"
REQUIREMENT = f"openkb @ git+https://github.com/VectifyAI/OpenKB.git@{REVISION}"
ROOT = Path(__file__).resolve().parents[4]
UPSTREAM = Path(__file__).resolve().parents[1] / "upstream"
INCREMENTAL_CONTRACT = 1



def knowledge_roots(project):
    """Reuse runtime layout resolution; isolated OpenKB environments need no runtime install."""
    try:
        from ai_sdlc_workbench.knowledge_layout import knowledge_layout
    except ImportError as error:
        if error.name not in {None, "ai_sdlc_workbench", "ai_sdlc_workbench.knowledge_layout"}:
            raise
        # OpenKB and standalone skill runtimes can omit the Workbench package.
        project = Path(project).resolve()
        current, legacy = project / "knowledge/evidence", project / "evidence/knowledge"
        current_marker, legacy_marker = current / "manifest.yaml", legacy / "manifest.yaml"
        current_present = current_marker.exists() or current_marker.is_symlink()
        legacy_present = legacy_marker.exists() or legacy_marker.is_symlink()
        if current_present and legacy_present:
            raise ValueError("Both knowledge manifests exist. Finish or recover the layout migration before continuing.")
        if current_present:
            records = project / "knowledge/records"
            if not records.is_dir():
                raise ValueError("The consolidated knowledge layout requires knowledge/records/. Restore it before continuing.")
            return records, current
        if not legacy_present and any(path.exists() or path.is_symlink() for path in (current, project / "knowledge/records")):
            raise ValueError("The consolidated knowledge layout is incomplete. Restore knowledge/evidence/manifest.yaml before continuing.")
        return project / "knowledge", legacy
    return knowledge_layout(project)


def canonical_folder(project, source=None):
    canonical, _ = knowledge_roots(project)
    if any(path.is_symlink() for path in (canonical, *canonical.parents) if path != project and path.is_relative_to(project)):
        raise ValueError("Canonical knowledge roots must not use symbolic links")
    folder = canonical / "candidates" if source is None else (canonical if source == "knowledge" else project / source)
    folder = folder.resolve()
    folder.relative_to(canonical.resolve())
    return folder


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


def agent_handoff(project, operation, source=None, arguments=()):
    print("Selected engine: llm-wiki-agent (both LLM URL and token were not provided).")
    print("Agent handoff only; no model client was called and no wiki pages were changed.")
    print(f"Current ADE agent: follow {UPSTREAM / 'AGENTS.md'} for {operation}.")
    print(f"Use the single active wiki: {project / 'knowledge/llm-wiki/wiki'}")
    if operation == "compile":
        if "--record" in arguments:
            print("Read only the complete canonical records named by --record below and their affected wiki dependencies.")
        else:
            print(f"Read complete canonical records from: {canonical_folder(project, source)}")
    if arguments:
        print("Requested arguments: " + " ".join(arguments))
    print("Retain the existing page format: summaries/ holds source summaries; sources/ and raw/ are immutable canonical links.")
    print("Maintain concepts, entities, explorations, contradictions, the index and log in this same wiki; do not create a second wiki.")
    print("Do not run upstream scripted ingest/refresh against linked sources. Reconcile provenance only after successful agent maintenance.")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(json_bytes(value))
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def save_plan(project, path, value):
    path = path if path.is_absolute() else project / path
    try:
        relative = path.relative_to(project / ".workbench")
    except ValueError:
        raise ValueError("Plan output must use an unused path below the project's ignored .workbench/") from None
    if ".." in relative.parts or any(parent.is_symlink() for parent in (path, *path.parents) if parent != project):
        raise ValueError("Plan output and its parent directories must not be symlinks")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(json_bytes(value))


def runtime_python(project):
    return project / ".venv-openkb" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def local_yaml_runtime(project):
    """Use an existing local parser runtime, with no installation or discovery IO."""
    if importlib.util.find_spec("yaml") is not None:
        return False
    relative = "Scripts/python.exe" if os.name == "nt" else "bin/python"
    for python in (project / ".venv" / relative, runtime_python(project)):
        if python.is_file() and Path(sys.executable).resolve() != python.resolve():
            subprocess.run([str(python), str(Path(__file__).resolve()), *sys.argv[1:]],
                           check=True, env=command_environment())
            return True
    raise ValueError("PyYAML is unavailable; use the installed Workbench Python or run Workbench setup")


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


def canonical_records(project, source, selected=()):
    """Resolve exact canonical inputs before any engine or credential setup."""
    import yaml
    folder = canonical_folder(project, source)
    wiki = (project / "knowledge/llm-wiki").resolve()
    if folder.is_relative_to(wiki):
        raise ValueError("Derived wiki files are not canonical inputs")
    paths = []
    for relative in selected:
        candidate = project / relative
        if Path(relative).is_absolute() or ".." in Path(relative).parts:
            raise ValueError(f"Use a workspace-relative canonical record: {relative}")
        candidate.resolve().relative_to(folder)
        if not candidate.is_file() or candidate.suffix != ".md":
            raise ValueError(f"Requested canonical record is missing or not Markdown: {relative}")
        paths.append(candidate)
    if not selected:
        paths = list(folder.rglob("*.md"))
    records = {}
    for candidate in sorted(paths, key=lambda p: (-len(p.parts), str(p))):
        if candidate.name in {"README.md", "index.md"}:
            if selected:
                raise ValueError(f"Navigation is not a canonical record: {candidate}")
            continue
        candidate.resolve().relative_to(project)
        if candidate.resolve().is_relative_to(wiki):
            if selected:
                raise ValueError("Derived wiki files are not canonical inputs")
            continue
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
            if records[identifier]["sha256"] != source_hash:
                raise ValueError(f"Conflicting canonical records for {identifier}")
            continue
        records[identifier] = {"path": candidate, "metadata": metadata, "sha256": source_hash}
    if not records and not folder.is_dir():
        raise ValueError(f"No canonical records in {folder}")
    if len({record["path"].stem for record in records.values()}) != len(records):
        raise ValueError("Canonical filename collision; use unique filenames before compilation")
    return records


def binding_bytes(kb):
    return tuple(path.read_bytes() if path.exists() else None
                 for path in (kb / "source-manifest.json", kb / ".openkb/hashes.json"))


def require_binding_bytes(kb, expected):
    if binding_bytes(kb) != expected:
        raise ValueError("Wiki provenance changed concurrently; reconcile without overwriting it")


def wiki_state(kb, with_bytes=False):
    previous = binding_bytes(kb)
    manifest = json.loads(previous[0]) if previous[0] is not None else {"engine": "OpenKB", "sources": []}
    registry = json.loads(previous[1]) if previous[1] is not None else {}
    state = manifest.setdefault("incremental", {"contract": INCREMENTAL_CONTRACT, "completed": {}, "outputs": {}, "attempts": {}})
    if state.get("contract") != INCREMENTAL_CONTRACT:
        raise ValueError("Unsupported incremental wiki contract; reconcile existing receipts")
    for key in ("completed", "outputs", "attempts"):
        state.setdefault(key, {})
    return (manifest, registry, previous) if with_bytes else (manifest, registry)


def recipe_hash(kb, recipe):
    """Caller names nonsecret semantic settings; private configuration stays unread."""
    schema = kb / "wiki/AGENTS.md"
    value = {"contract": INCREMENTAL_CONTRACT, "compiler_revision": REVISION,
             "schema_sha256": digest(schema) if schema.is_file() else None, "recipe": recipe}
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def output_path(kb, relative):
    path = kb / relative
    if Path(relative).is_absolute() or ".." in Path(relative).parts or not relative.startswith("wiki/"):
        raise ValueError(f"Expected a wiki-relative derived output: {relative}")
    path.resolve().relative_to((kb / "wiki").resolve())
    if path.is_symlink() or relative.startswith("wiki/sources/") or path.suffix != ".md" or path.name in {"AGENTS.md", "log.md"}:
        raise ValueError(f"Expected a derived Markdown output, not a canonical alias: {relative}")
    return path


def output_hashes(kb):
    return {path.relative_to(kb).as_posix(): digest(path)
            for path in sorted((kb / "wiki").rglob("*.md"))
            if not path.is_symlink() and "sources" not in path.relative_to(kb / "wiki").parts
            and path.name not in {"AGENTS.md", "log.md"}}


def dependent_outputs(kb, doc_name):
    """Prior citations plus affected saved synthesis; never traverse the global index."""
    summary = f"wiki/summaries/{doc_name}.md"
    result = {summary, "wiki/index.md"}
    pages = output_hashes(kb)
    references = {}
    for relative in pages:
        text = (kb / relative).read_text(encoding="utf-8")
        references[relative] = set(re.findall(r"(?:summaries|sources|concepts|entities|explorations)/[\w.-]+", text))
        if f"summaries/{doc_name}" in references[relative] or f"summaries/{doc_name}.md" in references[relative] or f"sources/{doc_name}.md" in references[relative]:
            result.add(relative)
    # Follow known inbound dependencies, including concepts and saved synthesis.
    # Index navigation must not make every page depend on every source.
    changed = True
    while changed:
        changed = False
        targets = {relative.removeprefix("wiki/").removesuffix(".md") for relative in result if relative != "wiki/index.md"}
        for relative, refs in references.items():
            if relative != "wiki/index.md" and relative not in result and any(ref.removesuffix(".md") in targets for ref in refs):
                result.add(relative)
                changed = True
    return result


def update_plan(project, source=None, selected=(), recipe="default"):
    """Local inventory and receipts only: no OpenKB imports or private settings."""
    if not isinstance(recipe, str) or not recipe.strip():
        raise ValueError("A nonempty, nonsecret processing recipe identity is required")
    project = project.resolve()
    kb = project / "knowledge/llm-wiki"
    source = canonical_folder(project, source).relative_to(project).as_posix()
    records = canonical_records(project, source, selected)
    manifest, registry = wiki_state(kb)
    state = manifest["incremental"]
    bindings = {record["doc_name"]: record for record in manifest["sources"]}
    fingerprint = recipe_hash(kb, recipe)
    items = []
    for identifier, record in records.items():
        original, sha = record["path"], record["sha256"]
        doc_name = original.stem
        binding, completed, attempt = bindings.get(doc_name), state["completed"].get(doc_name), state["attempts"].get(doc_name)
        if binding and binding.get("id") != identifier:
            raise ValueError(f"Canonical filename/ID collision with existing binding: {doc_name}")
        if any(value.get("id") == identifier and value["doc_name"] != doc_name for value in manifest["sources"]):
            raise ValueError(f"Canonical ID already has another filename binding: {identifier}")
        expected = dependent_outputs(kb, doc_name) | set((completed or {}).get("outputs", [])) | set((attempt or {}).get("expected_outputs", []))
        reasons = []
        if binding is None:
            disposition = "bootstrap_review" if any(entry.get("doc_name") == doc_name for entry in registry.values()) else "new"
            reasons.append("source is not in the manifest")
        elif binding.get("id") != identifier or binding.get("origin") != original.relative_to(project).as_posix():
            disposition = "repair_review"
            reasons.append("canonical identity or location changed")
        elif binding.get("sha256") != sha:
            disposition = "changed"
            reasons.append("canonical source bytes changed")
        elif attempt:
            disposition = "retry" if attempt.get("status") == "failed" else "pending_review"
            reasons.append(f"unfinished attempt: {attempt.get('status')}")
        elif not completed:
            disposition = "bootstrap_review"
            reasons.append("legacy binding has no reviewed completion receipt")
        elif completed.get("recipe") != fingerprint:
            disposition = "recipe_changed"
            reasons.append("processing recipe or schema changed")
        elif completed.get("sha256") != sha or completed.get("id") != identifier:
            disposition = "repair_review"
            reasons.append("completion identity does not match the canonical input")
        else:
            disposition = "unchanged"
        if attempt and attempt.get("sha256") == sha and disposition != "repair_review":
            disposition = "recipe_changed" if attempt.get("recipe") != fingerprint else ("retry" if attempt.get("status") == "failed" else "pending_review")
            reasons.append(f"unfinished attempt: {attempt.get('status')}")
        if binding and binding.get("sha256") == sha:
            valid_registry = registry.get(sha, {}).get("doc_name") == doc_name
            aliases = all((kb / relative).is_symlink() and (kb / relative).resolve() == original.resolve()
                          and not os.path.isabs(os.readlink(kb / relative))
                          for relative in (f"raw/{original.name}", f"wiki/sources/{original.name}"))
            if not valid_registry or not aliases:
                disposition = "repair_review"
                reasons.append("registry or relative canonical aliases need repair")
        if completed and disposition == "unchanged":
            if not expected.issubset(set(completed["outputs"])):
                disposition = "repair_review"
                reasons.append("derived dependency scope changed")
            for relative in completed["outputs"]:
                path = output_path(kb, relative)
                receipt = state["outputs"].get(relative, {})
                if not path.is_file() or receipt.get("sha256") != digest(path) or identifier not in receipt.get("sources", []):
                    disposition = "repair_review"
                    reasons.append(f"missing or changed reviewed output: {relative}")
        items.append({"id": identifier, "path": original.relative_to(project).as_posix(), "doc_name": doc_name,
                      "sha256": sha, "disposition": disposition, "reasons": reasons, "expected_outputs": sorted(expected),
                      "relocated": bool(binding and binding.get("origin") != original.relative_to(project).as_posix())})
    if not selected:
        folder = (project / source).resolve()
        for binding in manifest["sources"]:
            original = project / binding["origin"]
            if original.resolve().is_relative_to(folder) and not original.is_file():
                items.append({"id": binding.get("id"), "path": binding["origin"], "doc_name": binding["doc_name"],
                              "disposition": "missing", "reasons": ["bound canonical source is missing; history is retained"],
                              "expected_outputs": sorted(dependent_outputs(kb, binding["doc_name"]))})
    counts = {value: sum(item["disposition"] == value for item in items) for value in sorted({item["disposition"] for item in items})}
    return {"recipe": recipe, "recipe_sha256": fingerprint, "source": source, "counts": counts, "records": items}


def compile_queue(plan, force=False):
    if force and any(item.get("relocated") for item in plan["records"]):
        raise ValueError("Canonical relocation requires reviewed binding completion, not forced compilation")
    return [item for item in plan["records"] if item["disposition"] in {"new", "changed", "recipe_changed", "retry"}
            or (force and item["disposition"] != "missing")]


def write_binding_pair(project, manifest, registry, expected, check=None):
    """Retain paired before-images; recover only bytes owned by this attempt."""
    kb = project / "knowledge/llm-wiki"
    paths = (kb / "source-manifest.json", kb / ".openkb/hashes.json")
    values = (manifest, registry)
    require_binding_bytes(kb, expected)
    previous = expected
    recovery = project / ".workbench/wiki" / uuid.uuid4().hex
    recovery.mkdir(parents=True)
    after = [json_bytes(value) for value in values]
    for name, content in zip(("source-manifest.before.json", "hashes.before.json"), previous):
        if content is not None:
            (recovery / name).write_bytes(content)
    receipt = {"status": "pending", "paths": [path.relative_to(project).as_posix() for path in paths],
               "before": [hashlib.sha256(value).hexdigest() if value is not None else None for value in previous],
               "after": [hashlib.sha256(value).hexdigest() for value in after]}
    save_json(recovery / "recovery.json", receipt)
    try:
        current = list(previous)
        for index, (path, value) in enumerate(zip(paths, values)):
            require_binding_bytes(kb, tuple(current))
            save_json(path, value)
            current[index] = after[index]
        require_binding_bytes(kb, tuple(after))
        if check:
            check()
    except BaseException:
        if all((path.read_bytes() if path.exists() else None) in (before, intended)
               for path, before, intended in zip(paths, previous, after)):
            for path, before in zip(paths, previous):
                if before is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_bytes(before)
            receipt["status"] = "restored"
        else:
            receipt["status"] = "reconciliation_required"
        save_json(recovery / "recovery.json", receipt)
        raise
    receipt["status"] = "written"
    save_json(recovery / "recovery.json", receipt)
    return tuple(after)


def compile_sources(project, source, selected=(), recipe="default", force=False):
    plan = update_plan(project, source, selected, recipe)
    if not compile_queue(plan, force):
        print(json.dumps(plan, indent=2))
        return plan
    url, token = configured_credentials(project)
    if not (url and token):
        raise ValueError("OpenKB compilation requires both OPENAI_API_BASE and LLM_API_KEY; use the llm-wiki-agent ADE workflow")
    from dataclasses import replace
    from openkb.agent.compiler import compile_short_doc
    from openkb.cli import _setup_llm_key
    from openkb.config import resolve_effective_config, resolve_concurrency, resolve_credential_bundle
    from openkb.locks import kb_ingest_lock
    from openkb.log import append_log

    kb = project / "knowledge/llm-wiki"
    manifest_path = kb / "source-manifest.json"
    with kb_ingest_lock(kb / ".openkb"):
        plan = update_plan(project, source, selected, recipe)
        queued = compile_queue(plan, force)
        if not queued:
            print(json.dumps(plan, indent=2))
            return plan
        config = resolve_effective_config(kb)[0]
        validate_api_config(config)
        _setup_llm_key(kb)
        bundle = replace(resolve_credential_bundle(kb), base_url=url, api_key=token)
        manifest, registry, expected_pair = wiki_state(kb, with_bytes=True)
        bindings = {record["doc_name"]: record for record in manifest["sources"]}
        for item in queued:
            original = project / item["path"]
            before = digest(original)
            if before != item["sha256"]:
                raise ValueError(f"Source changed before compilation; rescan it: {original}")
            raw = kb / "raw" / original.name
            full_text = kb / "wiki/sources" / original.name
            link_source(raw, original)
            link_source(full_text, original)
            output_before = output_hashes(kb)
            attempt = {"status": "running", "sha256": before, "recipe": plan["recipe_sha256"],
                       "previous_sha256": bindings.get(original.stem, {}).get("sha256"),
                       "expected_outputs": item["expected_outputs"],
                       "output_before": {path: sha for path, sha in output_before.items() if path in item["expected_outputs"]}}
            manifest["incremental"]["attempts"][original.stem] = attempt
            require_binding_bytes(kb, expected_pair)
            save_json(manifest_path, manifest)
            expected_pair = (json_bytes(manifest), expected_pair[1])
            try:
                asyncio.run(compile_short_doc(original.stem, full_text, kb, config["model"],
                                              max_concurrency=resolve_concurrency(config) or 2, bundle=bundle))
                if digest(original) != before:
                    raise ValueError(f"Source changed during compilation; binding not advanced: {original}")
            except BaseException as error:
                attempt["status"] = "failed"
                attempt["failure_type"] = type(error).__name__
                attempt["expected_outputs"] = sorted(set(attempt["expected_outputs"]) | dependent_outputs(kb, original.stem)
                                                     | {path for path, sha in output_hashes(kb).items() if output_before.get(path) != sha})
                require_binding_bytes(kb, expected_pair)
                save_json(manifest_path, manifest)
                raise
            metadata = canonical_records(project, source, [item["path"]])[item["id"]]["metadata"]
            registry = {key: value for key, value in registry.items() if value.get("doc_name") != original.stem}
            registry[before] = {"name": original.name, "doc_name": original.stem, "type": "md",
                                "path": f"raw/{original.name}", "raw_path": f"raw/{original.name}",
                                "source_path": f"wiki/sources/{original.name}"}
            bindings[original.stem] = {"doc_name": original.stem, "id": item["id"],
                                       "origin": original.relative_to(project).as_posix(), "sha256": before,
                                       **{key: metadata[key]
                                          for key in ("version", "status", "governance_state")
                                          if key in metadata}}
            manifest["sources"] = list(bindings.values())
            after = output_hashes(kb)
            attempt["status"] = "pending_review"
            attempt["expected_outputs"] = sorted(set(attempt["expected_outputs"]) | dependent_outputs(kb, original.stem)
                                                 | {path for path in set(output_before) | set(after) if output_before.get(path) != after.get(path)})
            def check_source():
                if digest(original) != before:
                    raise ValueError(f"Source changed before binding completion: {original}")
            expected_pair = write_binding_pair(project, manifest, registry, expected_pair, check_source)
            append_log(kb / "wiki", "ingest", f"OpenKB semantic compilation: {original.name}")
            print(f"Compiled {original.name}; explicit output review is pending")
        return update_plan(project, source, selected, recipe)




def markdown_destinations(text):
    """Return destination spans, preserving labels, titles, and all other bytes for proof."""
    spans, code_ranges = [], []
    frontmatter = re.match(r"\A---\r?\n.*?\r?\n---(?:\r?\n|\Z)", text, re.S)
    if frontmatter:
        code_ranges.append((0, frontmatter.end()))
    fence, start, offset = None, None, 0
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        if fence is not None:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                code_ranges.append((start, offset + len(line)))
                fence = None
        elif marker:
            fence, start = marker[1], offset
        elif line.startswith(("    ", "\t")):
            code_ranges.append((offset, offset + len(line)))
        offset += len(line)
    if fence is not None:
        code_ranges.append((start, len(text)))
    for pattern in (r"(?<!`)(`+)(?!`)(.*?)(?<!`)\1(?!`)", r"<(pre|code)\b[^>]*>.*?</\1\s*>"):
        code_ranges.extend((match.start(), match.end()) for match in re.finditer(pattern, text, re.S | re.I))
    patterns = (r"!?\[[^\]\n]*\]\(\s*(<[^>\n]*>|(?:\\.|[^()\n]|\([^()\n]*\))*)\)",
                r"^ {0,3}\[[^\]\n]+\]:[ \t]*(<[^>\n]*>|[^\n]+)")
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.M):
            if any(match.start() < end and match.end() > start for start, end in code_ranges):
                continue
            raw, start = match.group(1), match.start(1)
            if raw.startswith("<") and ">" in raw:
                spans.append((start + 1, start + raw.index(">")))
            else:
                target = re.sub(r"\s+(['\"]).*\1\s*$", "", raw).rstrip()
                if target:
                    spans.append((start, start + len(target)))
    return sorted(set(spans))


def prove_locator_change(project, revision, before_path, after_path, before_sha, after_sha, locations):
    """Prove a Git-bound migration changed only local Markdown link destinations."""
    if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}", revision):
        raise ValueError("Locator proof requires an exact baseline Git revision")
    raw = subprocess.run(["git", "-C", str(project), "show", f"{revision}:{before_path}"],
                         capture_output=True, check=True).stdout
    current = (project / after_path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != before_sha or hashlib.sha256(current).hexdigest() != after_sha:
        raise ValueError("Locator proof baseline or current bytes do not match the receipt")
    old_text, new_text = raw.decode("utf-8"), current.decode("utf-8")
    old_spans, new_spans = markdown_destinations(old_text), markdown_destinations(new_text)
    def masked(text, spans):
        for start, end in reversed(spans):
            text = text[:start] + "<LOCATOR>" + text[end:]
        return text
    if len(old_spans) != len(new_spans) or masked(old_text, old_spans) != masked(new_text, new_spans):
        raise ValueError("Locator proof rejected changes outside Markdown destinations")
    for (old_start, old_end), (new_start, new_end) in zip(old_spans, new_spans):
        old, new = old_text[old_start:old_end], new_text[new_start:new_end]
        old_url, new_url = urlsplit(old), urlsplit(new)
        if old_url.scheme or old_url.netloc or not old_url.path or old_url.path.startswith("/"):
            if old != new:
                raise ValueError("Locator proof cannot change external or fragment-only destinations")
            continue
        if (new_url.scheme or new_url.netloc or (old_url.query, old_url.fragment) != (new_url.query, new_url.fragment)):
            raise ValueError("Locator proof cannot change destination type, query, or fragment")
        def local_target(origin, destination):
            decoded = unquote(destination)
            if (PurePosixPath(decoded).is_absolute() or PureWindowsPath(decoded).drive
                    or "\\" in decoded):
                raise ValueError("Locator proof requires workspace-relative local destinations without backslashes")
            # Baseline identity is lexical: current aliases may already point at a new origin.
            relative = posixpath.normpath(posixpath.join(str(PurePosixPath(origin).parent), decoded))
            if relative == ".." or relative.startswith("../"):
                raise ValueError("Locator proof local destinations must stay inside the workspace")
            return relative
        previous = local_target(before_path, old_url.path)
        target = local_target(after_path, new_url.path)
        if target != locations.get(previous, previous):
            raise ValueError(f"Locator proof target does not match the migration map: {old}")
        # The current target must also remain confined after following live symlinks.
        (project / target).resolve().relative_to(project)
    return after_sha


def relocate_sources(project, receipt):
    """Move canonical origins and aliases without advancing semantic hashes or completion."""
    from openkb.locks import kb_ingest_lock

    if not isinstance(receipt.get("reason"), str) or not receipt["reason"].strip():
        raise ValueError("Canonical relocation requires its recorded reason")
    sources = receipt.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("Canonical relocation requires nonempty source mappings")
    outputs = receipt.get("outputs", [])
    if not isinstance(outputs, list) or any(not isinstance(output, dict)
            or any(not isinstance(output.get(key), str) or not output[key] for key in ("path", "before_sha256", "sha256"))
            for output in outputs):
        raise ValueError("Output relocation mappings require path, before_sha256, and current sha256")
    project = project.resolve()
    kb = project / "knowledge/llm-wiki"
    with kb_ingest_lock(kb / ".openkb"):
        manifest, registry, expected_pair = wiki_state(kb, with_bytes=True)
        bindings = {record["id"]: record for record in manifest["sources"]}
        planned, seen, aliases = [], set(), {}
        outputs_before = output_hashes(kb)
        proof_revision = receipt.get("baseline_revision")
        locations, map_path, map_sha = {}, None, None
        if proof_revision is not None:
            relative = receipt.get("locator_map")
            if not isinstance(relative, str) or Path(relative).is_absolute() or ".." in Path(relative).parts:
                raise ValueError("Locator proof requires a workspace-relative migration map")
            map_path = project / relative
            map_path.resolve().relative_to(project)
            map_sha = digest(map_path)
            mapping = json.loads(map_path.read_text(encoding="utf-8"))
            if mapping.get("source_revision") != proof_revision or not isinstance(mapping.get("entries"), list):
                raise ValueError("Locator proof baseline and migration map disagree")
            for row in mapping["entries"]:
                if not isinstance(row, dict) or not all(isinstance(row.get(key), str) for key in ("old", "new")):
                    raise ValueError("Migration map entries require old and new workspace paths")
                if row["old"] in locations and locations[row["old"]] != row["new"]:
                    raise ValueError("Migration map has conflicting destinations")
                locations[row["old"]] = row["new"]
        for source in sources:
            if not isinstance(source, dict) or not all(isinstance(source.get(key), str) and source[key]
                                                     for key in ("id", "from", "to", "sha256")):
                raise ValueError("Relocation mappings require id, from, to, and current target sha256")
            if source["id"] in seen:
                raise ValueError("Relocation mappings require unique canonical IDs")
            seen.add(source["id"])
            for value in (source["from"], source["to"]):
                if Path(value).is_absolute() or ".." in Path(value).parts:
                    raise ValueError("Relocation paths must be workspace-relative without traversal")
            canonical = canonical_records(project, "knowledge", [source["to"]])
            record = canonical.get(source["id"])
            binding = bindings.get(source["id"])
            if record is None or binding is None or record["sha256"] != source["sha256"]:
                raise ValueError("Relocation target identity or current bytes do not match the receipt")
            original = record["path"]
            if (binding["origin"] not in {source["from"], source["to"]}
                    or original.stem != binding["doc_name"] or Path(source["from"]).name != original.name):
                raise ValueError("Relocation conflicts with the existing canonical origin or filename")
            for relative in (f"raw/{original.name}", f"wiki/sources/{original.name}"):
                link = kb / relative
                if (not link.is_symlink() or os.path.isabs(os.readlink(link))
                        or link.resolve() not in {(project / source["from"]).resolve(), original.resolve()}):
                    raise ValueError(f"Relocation requires the existing relative canonical alias: {relative}")
                aliases[link] = (os.readlink(link), os.path.relpath(original, link.parent))
            if proof_revision is not None:
                before_sha = source.get("before_sha256")
                if locations.get(source["from"]) != source["to"]:
                    raise ValueError("Canonical relocation is absent from the migration map")
                prove_locator_change(project, proof_revision, source["from"], source["to"],
                                     before_sha, source["sha256"], locations)
                if binding.get("sha256") not in {before_sha, source["sha256"]}:
                    raise ValueError("Locator proof cannot advance a preexisting stale source binding")
                entry = registry.get(binding["sha256"])
                if not entry or entry.get("doc_name") != binding["doc_name"]:
                    raise ValueError("Locator proof requires the matching observed source registry entry")
                if source["sha256"] in registry and registry[source["sha256"]].get("doc_name") != binding["doc_name"]:
                    raise ValueError("Locator proof conflicts with another source hash registry entry")
                registry.pop(binding["sha256"])
                registry[source["sha256"]] = entry
                binding["sha256"] = source["sha256"]
            binding["origin"] = source["to"]
            completed = manifest["incremental"]["completed"].get(binding["doc_name"])
            if completed is not None:
                if completed.get("origin") not in {source["from"], source["to"]}:
                    raise ValueError("Relocation conflicts with an existing completion origin")
                completed["origin"] = source["to"]
                if proof_revision is not None and completed.get("sha256") in {source.get("before_sha256"), source["sha256"]}:
                    completed["sha256"] = source["sha256"]
            planned.append(source)
        for output in outputs:
            if proof_revision is None:
                raise ValueError("Output hash rebinding requires exact locator proof")
            path = output_path(kb, output["path"])
            relative = path.relative_to(project).as_posix()
            prove_locator_change(project, proof_revision, relative, relative,
                                 output.get("before_sha256"), output.get("sha256"), locations)
            observed = manifest["incremental"]["outputs"].get(output["path"])
            if observed is not None:
                if observed.get("sha256") not in {output.get("before_sha256"), output.get("sha256")}:
                    raise ValueError("Locator proof cannot advance a preexisting stale output binding")
                observed["sha256"] = output["sha256"]

        def check_targets():
            for source in planned:
                if digest(project / source["to"]) != source["sha256"]:
                    raise ValueError("Canonical target changed during relocation")
            if output_hashes(kb) != outputs_before:
                raise ValueError("Derived output bytes changed during relocation")
            if map_path is not None and digest(map_path) != map_sha:
                raise ValueError("Migration map changed during locator proof")

        def replace_alias(link, target):
            temporary = link.with_name(f".{link.name}.{uuid.uuid4().hex}.link")
            try:
                temporary.symlink_to(target)
                os.replace(temporary, link)
            finally:
                temporary.unlink(missing_ok=True)

        check_targets()
        require_binding_bytes(kb, expected_pair)
        try:
            for link, (before, after) in aliases.items():
                if os.readlink(link) != before:
                    raise ValueError("Canonical aliases changed concurrently")
                replace_alias(link, after)
            def check_after_write():
                check_targets()
                if any(not link.is_symlink() or os.readlink(link) != after
                       for link, (_, after) in aliases.items()):
                    raise ValueError("Canonical aliases changed during relocation")
            write_binding_pair(project, manifest, registry, expected_pair, check_after_write)
        except BaseException:
            for link, (before, after) in aliases.items():
                if link.is_symlink() and os.readlink(link) == after:
                    replace_alias(link, before)
            raise
    disposition = "proven locator hashes rebound" if proof_revision is not None else "observed hashes preserved"
    print(f"Relocated {len(planned)} canonical origins; {disposition}; semantic completion was preserved")
    return {"relocated": sorted(seen), "semantic_completion": "UNCHANGED"}


def review_sources(project, receipt):
    """Record supplied semantic review, never manufacture it from observed hashes."""
    from openkb.locks import kb_ingest_lock

    for field in ("reviewed_by", "reviewed_at", "review_note", "recipe", "engine"):
        if not isinstance(receipt.get(field), str) or not receipt[field].strip():
            raise ValueError(f"Review receipt requires truthful {field}")
    if receipt["engine"] not in {"openkb", "llm-wiki-agent"}:
        raise ValueError("Review receipt engine must name the actual semantic mode")
    try:
        timestamp = datetime.fromisoformat(receipt["reviewed_at"].replace("Z", "+00:00"))
        if timestamp.utcoffset() is None:
            raise ValueError("timezone missing")
    except ValueError:
        raise ValueError("Review receipt requires an ISO reviewed_at with timezone") from None
    sources = receipt.get("sources")
    outputs = receipt.get("outputs")
    if not isinstance(sources, list) or not sources or not isinstance(outputs, list):
        raise ValueError("Review receipt requires nonempty sources and reviewed outputs")
    selected = [record["path"] for record in sources]
    if len(set(selected)) != len(selected):
        raise ValueError("Duplicate reviewed source")
    kb = project / "knowledge/llm-wiki"
    with kb_ingest_lock(kb / ".openkb"):
        plan = update_plan(project, "knowledge", selected, receipt["recipe"])
        planned = {record["path"]: record for record in plan["records"]}
        manifest, registry, expected_pair = wiki_state(kb, with_bytes=True)
        state = manifest["incremental"]
        bindings = {record["doc_name"]: record for record in manifest["sources"]}
        reviewed = {}
        for output in outputs:
            relative = output["path"]
            path = output_path(kb, relative)
            if relative in reviewed or not isinstance(output.get("note"), str) or not output["note"].strip():
                raise ValueError(f"Output requires one explicit semantic review note: {relative}")
            sha = digest(path) if path.is_file() else None
            if output.get("sha256") != sha or (sha is None and output.get("disposition") != "removed"):
                raise ValueError(f"Reviewed output is missing or changed: {relative}")
            if not isinstance(output.get("sources"), list):
                raise ValueError(f"Output review must name the source IDs it preserves: {relative}")
            reviewed[relative] = output
        new_completions = {}
        for source in sources:
            item = planned[source["path"]]
            doc_name = item["doc_name"]
            original = project / item["path"]
            if source.get("sha256") != item["sha256"]:
                raise ValueError(f"Reviewed source is stale: {item['path']}")
            existing = bindings.get(doc_name)
            attempt = state["attempts"].get(doc_name, {})
            summary = f"wiki/summaries/{doc_name}.md"
            previous_sha = attempt.get("previous_sha256") if attempt else (existing or {}).get("sha256")
            previous_summary = attempt.get("output_before", {}).get(summary) if attempt else state["outputs"].get(summary, {}).get("sha256")
            if previous_sha and previous_sha != item["sha256"] and summary in reviewed and previous_summary == reviewed[summary]["sha256"] and not source.get("unchanged_reason", "").strip():
                raise ValueError(f"Changed source with unchanged summary requires a supported unchanged_reason: {doc_name}")
            if existing and existing.get("id") != item["id"]:
                raise ValueError(f"Canonical identity changed; reconcile it before wiki review: {doc_name}")
            if existing and existing.get("origin") != item["path"] and not source.get("relocation_reason"):
                raise ValueError(f"Canonical relocation requires its review reason: {doc_name}")
            withdrawn = source.get("withdrawn_outputs", [])
            if not isinstance(withdrawn, list) or any(not value.get("reason", "").strip() for value in withdrawn):
                raise ValueError(f"Withdrawn dependent claims require reviewed reasons: {doc_name}")
            removed = {value["path"] for value in withdrawn}
            wanted = set(source.get("outputs", []))
            for relative in wanted | removed:
                output_path(kb, relative)
            if f"wiki/summaries/{doc_name}.md" not in wanted or "wiki/index.md" not in wanted:
                raise ValueError(f"Review must include the source summary and index: {doc_name}")
            required = set(item["expected_outputs"])
            if required - wanted - removed or wanted & removed:
                raise ValueError(f"Review omitted former or current dependent outputs: {doc_name}")
            if not wanted.issubset(reviewed) or not removed.issubset(reviewed):
                raise ValueError(f"Review must bind all maintained and withdrawn outputs: {doc_name}")
            if any(reviewed[relative]["sha256"] is None for relative in wanted):
                raise ValueError(f"Expected reviewed output is missing: {doc_name}")
            if removed and not source.get("withdrawal_review_note", "").strip():
                raise ValueError(f"Withdrawn claims require a semantic disposition: {doc_name}")
            # A changed derived page can lose implementation or test facts while
            # the canonical policy correction remains valid.  Require the
            # reviewer to account for every changed output explicitly so that
            # policy editing cannot silently erase system evidence.
            previous_outputs = attempt.get("output_before", {}) if attempt else {}
            current_outputs = {relative: reviewed[relative]["sha256"]
                               for relative in set(wanted) | removed}
            changed_outputs = {relative for relative, sha in current_outputs.items()
                               if previous_outputs.get(relative) != sha}
            if changed_outputs:
                claim_review = source.get("claim_review")
                if not isinstance(claim_review, dict):
                    raise ValueError(f"Changed outputs require an explicit claim review: {doc_name}")
                declared = claim_review.get("changed_outputs")
                if not isinstance(declared, list) or any(not isinstance(value, dict) for value in declared):
                    raise ValueError(f"Claim review must enumerate every changed output: {doc_name}")
                declared_paths = [value.get("path") for value in declared]
                if (len(set(declared_paths)) != len(declared_paths) or
                        set(declared_paths) != changed_outputs or
                        any(not isinstance(value, str) or not value.strip() for value in declared_paths)):
                    raise ValueError(f"Claim review must enumerate every changed output: {doc_name}")
                if not isinstance(claim_review.get("review_note"), str) or not claim_review["review_note"].strip():
                    raise ValueError(f"Claim review requires a review note: {doc_name}")
                for changed in declared:
                    change_type = changed.get("change_type")
                    if change_type not in {"additive", "replacement", "removal", "mixed"}:
                        raise ValueError(f"Changed outputs need a reviewed change type: {doc_name}")
                    removed_claims = changed.get("removed_claims")
                    if not isinstance(removed_claims, list):
                        raise ValueError(f"Changed outputs require removed_claims, even when empty: {doc_name}")
                    if change_type in {"replacement", "removal", "mixed"} and not removed_claims:
                        raise ValueError(f"Replacement, removal, or mixed changes require removed claims: {doc_name}")
                    for claim in removed_claims:
                        if not isinstance(claim, dict):
                            raise ValueError(f"Each removed claim needs a classification: {doc_name}")
                        if not isinstance(claim.get("claim"), str) or not claim["claim"].strip():
                            raise ValueError(f"Removed claims need their prior text or meaning: {doc_name}")
                        if claim.get("claim_type") not in {"intent", "implementation", "test", "execution", "deployment", "approval", "unknown"}:
                            raise ValueError(f"Removed claims need a supported classification: {doc_name}")
                        if claim.get("disposition") not in {"preserved", "superseded", "withdrawn"}:
                            raise ValueError(f"Removed claims need a reviewed disposition: {doc_name}")
                        evidence = claim.get("evidence")
                        if (not isinstance(evidence, list) or not evidence or
                                any(not isinstance(value, str) or not value.strip() for value in evidence)):
                            raise ValueError(f"Removed claims need supporting evidence: {doc_name}")
            completion = {"id": item["id"], "origin": item["path"], "sha256": item["sha256"],
                          "recipe": plan["recipe_sha256"], "outputs": sorted(wanted),
                          "withdrawn_outputs": withdrawn, "reviewed_by": receipt["reviewed_by"],
                          "reviewed_at": receipt["reviewed_at"], "review_note": receipt["review_note"],
                          "engine": receipt["engine"]}
            if changed_outputs:
                completion["claim_review"] = claim_review
            new_completions[doc_name] = completion
            if source.get("unchanged_reason"):
                new_completions[doc_name]["unchanged_reason"] = source["unchanged_reason"]
            metadata = canonical_records(project, "knowledge", [item["path"]])[item["id"]]["metadata"]
            for relative in (f"raw/{original.name}", f"wiki/sources/{original.name}"):
                link = kb / relative
                if not link.is_symlink() or link.resolve() != original.resolve() or os.path.isabs(os.readlink(link)):
                    raise ValueError(f"Review requires an existing relative canonical alias: {relative}")
            if item["sha256"] in registry and registry[item["sha256"]].get("doc_name") != doc_name:
                raise ValueError(f"Source hash registry collision: {doc_name}")
            registry = {sha: entry for sha, entry in registry.items() if entry.get("doc_name") != doc_name}
            registry[item["sha256"]] = {"name": original.name, "doc_name": doc_name, "type": "md",
                                        "path": f"raw/{original.name}", "raw_path": f"raw/{original.name}",
                                        "source_path": f"wiki/sources/{original.name}"}
            bindings[doc_name] = {"id": item["id"], "doc_name": doc_name, "origin": item["path"], "sha256": item["sha256"],
                                  **{key: metadata[key] for key in ("version", "status", "governance_state") if key in metadata}}
        # A shared-page review must explicitly preserve every existing owner's
        # claims; updating its global output hash must not silently bless a loss.
        completions = {**state["completed"], **new_completions}
        for relative, output in reviewed.items():
            owners = {value["id"] for value in completions.values() if relative in value["outputs"]}
            if not owners.issubset(set(output["sources"])) or (owners and output["sha256"] is None):
                raise ValueError(f"Shared output review omitted preserved source claims: {relative}")
            for owner in owners:
                completion = next(value for value in completions.values() if value["id"] == owner)
                if digest(project / completion["origin"]) != completion["sha256"]:
                    raise ValueError(f"Shared output owner source changed: {owner}")
            state["outputs"][relative] = {**output, "reviewed_by": receipt["reviewed_by"], "reviewed_at": receipt["reviewed_at"]}
        state["completed"].update(new_completions)
        for doc_name in new_completions:
            state["attempts"].pop(doc_name, None)
        manifest["sources"] = list(bindings.values())

        def check_reviewed_bytes():
            for source in sources:
                if digest(project / source["path"]) != source["sha256"]:
                    raise ValueError(f"Source changed during review: {source['path']}")
            for relative, output in reviewed.items():
                path = output_path(kb, relative)
                if (digest(path) if path.is_file() else None) != output["sha256"]:
                    raise ValueError(f"Output changed during review: {relative}")

        check_reviewed_bytes()
        check_structure(kb)
        def verify_after_write():
            check_reviewed_bytes()
            verify(project)
        write_binding_pair(project, manifest, registry, expected_pair, verify_after_write)
        print(f"Recorded reviewed completion for {len(new_completions)} canonical sources")
        return {"completed": sorted(new_completions), "reviewed_outputs": sorted(reviewed), "recipe_sha256": plan["recipe_sha256"]}


def check_structure(kb):
    from openkb.lint import (find_broken_links, check_index_sync, find_orphans,
                             find_missing_entries, find_invalid_frontmatter,
                             find_missing_okf_fields, run_structural_lint)
    wiki = kb / "wiki"
    errors = (find_broken_links(wiki) + check_index_sync(wiki) + find_orphans(wiki)
              + find_missing_entries(kb / "raw", wiki, kb_dir=kb)
              + find_invalid_frontmatter(wiki) + find_missing_okf_fields(wiki))
    print(run_structural_lint(kb))
    if errors:
        raise ValueError("OpenKB structural findings: " + "; ".join(errors))


def verify(project):
    from importlib.metadata import version

    if version("openkb") != VERSION:
        raise ValueError(f"Expected OpenKB {VERSION}; run install")
    kb = project / "knowledge/llm-wiki"
    canonical = canonical_folder(project, "knowledge")
    manifest = json.loads((kb / "source-manifest.json").read_text())
    registry = json.loads((kb / ".openkb/hashes.json").read_text())
    for record in manifest["sources"]:
        original = project / record["origin"]
        original.resolve().relative_to(canonical.resolve())
        if digest(original) != record["sha256"]:
            raise ValueError(f"Compiled source binding is stale: {original}; compile it before advancing the hash")
        for relative in (f"raw/{original.name}", f"wiki/sources/{original.name}"):
            link = kb / relative
            if not link.is_symlink() or link.resolve() != original.resolve():
                raise ValueError(f"Expected canonical source link: {link}")
        if registry.get(record["sha256"], {}).get("doc_name") != record["doc_name"]:
            raise ValueError(f"OpenKB registry mismatch: {record['doc_name']}")
    check_structure(kb)
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
    compiler.add_argument("--source", help="Canonical folder; defaults to the active layout candidates directory")
    compiler.add_argument("--record", action="append", default=[], help="Exact workspace-relative canonical record; repeat as needed")
    compiler.add_argument("--recipe", default="default", help="Nonsecret identity of semantic settings and governing policy")
    compiler.add_argument("--force", action="store_true", help="Intentionally recompile selected inputs, including legacy bindings")
    planner = commands.add_parser("plan", help="Plan incremental wiki work locally without an engine or credentials")
    planner.add_argument("--source", help="Canonical folder; defaults to the active layout candidates directory")
    planner.add_argument("--record", action="append", default=[])
    planner.add_argument("--recipe", default="default")
    planner.add_argument("--output", type=Path, help="Save the complete plan and print compact counts and queued paths")
    reviewer = commands.add_parser("review", help="Finalize an actual source/output semantic review receipt")
    reviewer.add_argument("--receipt", type=Path, required=True)
    relocator = commands.add_parser("relocate", help="Move canonical origins/aliases while preserving observed hashes and pending work")
    relocator.add_argument("--receipt", type=Path, required=True)
    native = commands.add_parser("run")
    native.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    project = args.project.resolve()
    if args.command == "install":
        install(project, args.python, args.wheelhouse, args.offline)
        return
    if args.command in {"plan", "compile"} and local_yaml_runtime(project):
        return
    if args.command == "plan":
        result = update_plan(project, args.source, args.record, args.recipe)
        if args.output:
            save_plan(project, args.output, result)
            print(json.dumps({"counts": result["counts"], "queued": [record["path"] for record in result["records"]
                                                                  if record["disposition"] != "unchanged"],
                              "plan": str(args.output)}))
        else:
            print(json.dumps(result, indent=2))
        return
    if args.command == "compile":
        plan = update_plan(project, args.source, args.record, args.recipe)
        queued = compile_queue(plan, args.force)
        if not queued:
            print(json.dumps(plan, indent=2))
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
        arguments = args.arguments[1:] if args.command == "run" else ["--recipe", args.recipe]
        if args.command == "compile":
            for item in queued:
                arguments.extend(["--record", item["path"]])
            if args.force:
                arguments.append("--force")
        agent_handoff(project, operation, getattr(args, "source", None),
                      arguments)
        return
    if not python.exists():
        raise ValueError("Local OpenKB schema/graph environment missing; run install first")
    if args.command == "verify":
        verify(project)
    elif args.command == "compile":
        compile_sources(project, args.source, args.record, args.recipe, args.force)
    elif args.command == "review":
        review_sources(project, json.loads(args.receipt.read_text(encoding="utf-8")))
    elif args.command == "relocate":
        relocate_sources(project, json.loads(args.receipt.read_text(encoding="utf-8")))
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
