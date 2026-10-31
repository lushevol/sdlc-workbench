"""Prepare and manage an isolated, source-bound local runtime-log experiment."""
from __future__ import annotations

import argparse
import datetime
import difflib
import hashlib
import io
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
RUNTIME = ROOT / ".workbench/runtime-log-pilot-20261031"
MFE = ROOT / "repos/ui/mfe-base"
ROOT_REPO = ROOT / "repos/ui/mfe-root-config"
REVISIONS = {
    "candidate": "66c6411ade58e4d134e381c2baee8ad3f76a8dbf",
    "baseline": "f025513f696476a9cc8162681410cbd21e029bcb",
}
PORTS = {"bff": 8291, "candidate_mfe": 8342, "candidate_root": 8343,
         "baseline_mfe": 8352, "baseline_root": 8353}
REC = '(window as any).__recordRuntime?.'


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(value):
    return hashlib.sha256(value).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def archive(repo, revision, destination):
    data = subprocess.check_output(["git", "-C", str(repo), "archive", revision])
    destination.mkdir(parents=True, exist_ok=False)
    with tarfile.open(fileobj=io.BytesIO(data)) as stream:
        stream.extractall(destination, filter="data")
    (destination / "node_modules").symlink_to(repo / "node_modules", target_is_directory=True)
    return sha(data)


def edits_for(side):
    edits = []

    def add(file, label, before, after):
        edits.append({"file": file, "id": label, "before": before, "after": after})

    timeout = "src/components/Timeout/common/useController.ts"
    home = "src/pages/Home/common/useController.ts"
    service = "src/hooks/service/index.ts"
    response = "src/hooks/service/util/succes.response.handler.ts"
    add(home, "expiry-scheduled",
        "      const difftime = 1000 * aOrb(store?.expiredIn, 0) - new Date().getTime();",
        "      const difftime = 1000 * aOrb(store?.expiredIn, 0) - new Date().getTime();\n"
        f'      {REC}("home.expiry.scheduled", {{ delayMs: difftime }});')
    add(home, "expiry-fired", "      timerPopup.current = setTimeout(() => {\n        setShowTimeout(true);",
        f'      timerPopup.current = setTimeout(() => {{\n        {REC}("home.expiry.fired", {{}});\n        setShowTimeout(true);')
    add(service, "service-start", "export const relogin = () => {",
        f'export const relogin = () => {{\n  {REC}("renewal.service.start", {{}});')
    add("src/hooks/service/util/success.request.handler.ts", "request",
        "  return request;",
        '  if (request.url?.includes("/api/auth/")) {\n'
        f'    {REC}("auth.request", {{ path: request.url.split("?")[0], tokenPresent: !!store.token, refreshPresent: !!store.refreshToken }});\n'
        "  }\n  return request;")
    add(response, "response-received", "export const successHandler = (response: AxiosResponse): any => {",
        'export const successHandler = (response: AxiosResponse): any => {\n'
        '  if (response.config?.url?.includes("/api/auth/")) {\n'
        f'    {REC}("auth.response.received", {{ path: response.config.url.split("?")[0], status: response.status, accessPresent: !!(response.headers?.["single-ui-authorization"] ?? response.headers?.["Single-UI-Authorization"]), refreshPresent: !!(response.headers?.["single-ui-refresh"] ?? response.headers?.["Single-UI-Refresh"]) }});\n'
        '  }')
    add("src/hooks/service/util/error.response.handler.ts", "response-error",
        "export const errorHandler = (error: AxiosError): unknown => {",
        'export const errorHandler = (error: AxiosError): unknown => {\n'
        '  if (error.config?.url?.includes("/api/auth/")) {\n'
        f'    {REC}("auth.response.error", {{ path: error.config.url.split("?")[0], status: error.response?.status ?? null, canceled: error.code === "ERR_CANCELED" }});\n'
        '  }')
    add("src/hooks/reducer/index.ts", "state-transition", "  return store;",
        '  if (["SET_TOKEN", "SET_REFRESH_TOKEN", "SET_EXPIRED_TOKEN", "CLEAR", "SET_IS_ON_LOGOUT"].includes(action.type)) {\n'
        f'    {REC}("session.state_transition", {{ action: action.type, tokenPresent: !!store.token, refreshPresent: !!store.refreshToken, tokenChanged: state.token !== store.token, refreshChanged: state.refreshToken !== store.refreshToken, isOnLogout: !!store.isOnLogout }});\n'
        '  }\n  return store;')
    add(timeout, "extend-requested", "  const extend = async () => {",
        f'  const extend = async () => {{\n    {REC}("timeout.extend.requested", {{ tokenPresent: !!store.token, refreshPresent: !!store.refreshToken }});')
    add(timeout, "logout-requested", "  const continuLogout = async () => {",
        f'  const continuLogout = async () => {{\n    {REC}("timeout.logout.requested", {{}});')
    if side == "candidate":
        add(timeout, "extend-accepted", "    renewalPending.current = true;",
            f'    renewalPending.current = true;\n    {REC}("timeout.extend.accepted", {{}});')
        add(timeout, "renewal-discarded",
            "        logoutStarted.current\n      )\n        return;\n      ModalEvent(\"close\", { name: \"session control\", ...analyticsData });",
            '        logoutStarted.current\n      ) {\n'
            f'        {REC}("timeout.renewal.discarded", {{ mounted: mounted.current, epochMatches: sessionEpoch === currentSessionEpoch(), logoutStarted: logoutStarted.current }});\n'
            '        return;\n      }\n'
            f'      {REC}("timeout.renewal.success", {{}});\n'
            '      ModalEvent("close", { name: "session control", ...analyticsData });')
        add(timeout, "renewal-failed", "    } catch {\n      // The service reports the failure.",
            f'    }} catch {{\n      {REC}("timeout.renewal.failed", {{}});\n      // The service reports the failure.')
        add(timeout, "renewal-settled", "        renewalPending.current = false;",
            f'        {REC}("timeout.renewal.settled", {{}});\n        renewalPending.current = false;')
        add(timeout, "close-requested", "      props.setOpen(false);",
            f'      {REC}("timeout.prompt.close_requested", {{ reason: "renewal" }});\n      props.setOpen(false);')
        add(timeout, "logout-accepted", "    logoutStarted.current = true;",
            f'    logoutStarted.current = true;\n    {REC}("timeout.logout.accepted", {{}});')
        add(service, "service-settled", "      if (signal.relogin === controller) signal.relogin = undefined;",
            f'      {REC}("renewal.service.settled", {{}});\n      if (signal.relogin === controller) signal.relogin = undefined;')
        add(response, "stale-discarded", '    throw new CanceledError(\n      "Discarded an ended session response",',
            f'    {REC}("auth.response.discarded", {{ aborted: !!response.config?.signal?.aborted }});\n    throw new CanceledError(\n      "Discarded an ended session response",')
        add("src/utils/sessionEpoch.ts", "session-invalidated", "  epoch += 1;",
            f'  epoch += 1;\n  {REC}("session.invalidated", {{}});')
    else:
        add(timeout, "extend-accepted", '    setLoading(true);\n    ButtonEvent("click", { name: "extend", ...analyticsData });',
            f'    {REC}("timeout.extend.accepted", {{}});\n    setLoading(true);\n    ButtonEvent("click", {{ name: "extend", ...analyticsData }});')
        add(timeout, "renewal-returned", "    await relogin();\n    clearAllTimeout();",
            f'    await relogin();\n    {REC}("timeout.renewal.returned", {{ returnedValueDoesNotProveSuccess: true }});\n    clearAllTimeout();')
        add(timeout, "close-requested", "    await relogin();\n    " + REC + '("timeout.renewal.returned", { returnedValueDoesNotProveSuccess: true });\n    clearAllTimeout();\n    props.setOpen(false);',
            "    await relogin();\n    " + REC + '("timeout.renewal.returned", { returnedValueDoesNotProveSuccess: true });\n    clearAllTimeout();\n    ' + REC + '("timeout.prompt.close_requested", { reason: "renewal" });\n    props.setOpen(false);')
        add(timeout, "logout-accepted", '    dispacthIsOnLogout(true);',
            f'    {REC}("timeout.logout.accepted", {{}});\n    dispacthIsOnLogout(true);')
    return edits


def prepare():
    if RUNTIME.exists() or (OUT / "local-source-binding.json").exists():
        raise SystemExit("Pilot preparation already exists; preserve it and choose a new run identity.")
    RUNTIME.mkdir(parents=True)
    binding = {
        "created_at": now(), "runtime": str(RUNTIME.relative_to(ROOT)), "ports": PORTS,
        "runner": str(Path(__file__).relative_to(ROOT)), "runner_sha256": sha(Path(__file__).read_bytes()),
        "authority": "user-input.md#exact-user-input", "source": {},
        "mfe_dirty_worktree_excluded": git(MFE, "status", "--short"),
        "scope": "Local logging-method experiment; no application checkout edits or UAT evidence.",
        "affected_consumers": ["Home expiry scheduling", "Timeout dialog", "shared authentication service", "response interceptors", "session reducer", "session epoch guards"],
        "qualitative_risk": "Sparse synchronous optional observer calls can affect timing. Branches, promises, timers, requests, and credential values remain unchanged.",
        "limits": ["Archived frontend source plus disclosed logging-only instrumentation.",
                   "Toolkit substitute and existing isolated BFF fixture; no production identity or entitlement service.",
                   "Legacy BFF class layers do not establish current BFF checkout execution.",
                   "Local logs support local development only; remote UAT evidence remains required."]}
    mfe_template = (ROOT / ".workbench/four-checks-e2e-20261027/mfe.webpack.cjs").read_text()
    root_template = (ROOT / ".workbench/four-checks-e2e-20261027/root-fast.webpack.cjs").read_text()
    root_rev = git(ROOT_REPO, "rev-parse", "HEAD")
    root_source = RUNTIME / "root-source"
    root_archive_sha = archive(ROOT_REPO, root_rev, root_source)
    binding["root_source"] = {"revision": root_rev, "archive_sha256": root_archive_sha,
                              "path": str(root_source.relative_to(ROOT)), "status": git(ROOT_REPO, "status", "--short")}
    replacements = {}
    patch_parts = []
    for side, revision in REVISIONS.items():
        folder = RUNTIME / side
        source = folder / "source"
        archive_sha = archive(MFE, revision, source)
        source_hashes = {str(p.relative_to(source)): sha(p.read_bytes()) for p in sorted((source / "src").rglob("*")) if p.is_file()}
        edits = edits_for(side)
        originals = {}
        for edit in edits:
            file = source / edit["file"]
            original = file.read_text()
            originals.setdefault(edit["file"], original)
            count = original.count(edit["before"])
            if count != 1:
                raise RuntimeError(f"Instrumentation anchor mismatch: {side} {edit['file']} {edit['id']} {count}")
            updated = original.replace(edit["before"], edit["after"], 1)
            file.write_text(updated)
            edit.update({"before_file_sha256": sha(original.encode()), "after_file_sha256": sha(updated.encode())})
        for name, before in originals.items():
            patch_parts.extend(difflib.unified_diff(before.splitlines(keepends=True), (source / name).read_text().splitlines(keepends=True), fromfile=f"{side}/original/{name}", tofile=f"{side}/instrumented/{name}"))
        port = PORTS[side + "_mfe"]
        config = mfe_template.replace(str(ROOT / ".workbench/ut-final-cancellation-20261027/source"), str(source))
        config = config.replace("require('webpack')", "require(" + json.dumps(str(source / "node_modules/webpack")) + ")")
        config = config.replace("port: 8142", f"port: {port}")
        root_config = root_template.replace(str(ROOT_REPO), str(root_source)).replace("8143", str(port + 1)).replace("8142", str(port)).replace("8091", str(PORTS["bff"]))
        for kind, content in (("mfe", config), ("root", root_config)):
            (folder / (kind + ".webpack.cjs")).write_text(content)
            (OUT / (side + "-" + kind + ".webpack.cjs")).write_text(content)
        replacements[side] = edits
        binding["source"][side] = {"repository": "mfe-base", "revision": revision, "archive_sha256": archive_sha,
                                  "path": str(source.relative_to(ROOT)), "original_source_hashes": source_hashes,
                                  "instrumented_source_hashes": {name: sha((source / name).read_bytes()) for name in originals},
                                  "config_hashes": {kind: sha((folder / (kind + ".webpack.cjs")).read_bytes()) for kind in ("mfe", "root")}}
    fast = ROOT / ".workbench/session-active-cutoff-fix-20261024/bff-fast/classes"
    old = ROOT / ".workbench/portal-session-real-20261019/local-bff/classes"
    manifest = json.loads((old.parent / "source-build-manifest.json").read_text())
    binding["bff_fixture"] = {"original_source_revision": manifest["source_revision"],
                              "current_checkout_revision_not_executed": git(ROOT / "repos/services/single-ui-bff", "rev-parse", "HEAD"),
                              "class_layers_in_precedence_order": [],
                              "classpath_sha256": sha((old.parent / "classpath.txt").read_bytes()),
                              "effective_lifetimes": "Unknown until issuance observation; source defaults do not establish override class settings."}
    for base in (fast, old):
        files = {str(p.relative_to(base)): sha(p.read_bytes()) for p in sorted(base.rglob("*.class"))}
        if not files:
            raise RuntimeError("Required BFF class layer is empty: " + str(base))
        binding["bff_fixture"]["class_layers_in_precedence_order"].append({"path": str(base.relative_to(ROOT)), "resolved_path": str(base.resolve().relative_to(ROOT)), "classes": files})
    binding["toolkit_substitute_hashes"] = {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in sorted((ROOT / ".workbench/portal-session-real-20261019/local-mfe/toolkit-mock").rglob("*")) if p.is_file()}
    save(OUT / "instrumentation-replacements.json", replacements)
    (OUT / "instrumentation.patch").write_text("".join(patch_parts))
    binding["instrumentation_sha256"] = sha((OUT / "instrumentation-replacements.json").read_bytes())
    binding["instrumentation_patch_sha256"] = sha((OUT / "instrumentation.patch").read_bytes())
    save(OUT / "local-source-binding.json", binding)
    print(json.dumps({"status": "PREPARED", "binding": str((OUT / "local-source-binding.json").relative_to(ROOT)), "instrumentation_edits": {side: len(edits) for side, edits in replacements.items()}}))


def start():
    binding = json.loads((OUT / "local-source-binding.json").read_text())
    process_file = RUNTIME / "processes.json"
    if process_file.exists():
        raise SystemExit("Existing process record must be inspected and stopped before restarting.")
    for port in PORTS.values():
        with socket.socket() as sock:
            if sock.connect_ex(("127.0.0.1", port)) == 0:
                raise SystemExit(f"Required loopback port {port} is occupied; no processes were started.")
    old = ROOT / ".workbench/portal-session-real-20261019/local-bff"
    fast = ROOT / ".workbench/session-active-cutoff-fix-20261024/bff-fast"
    classpath = str(fast / "classes") + ":" + str(old / "classes") + ":" + (old / "classpath.txt").read_text().strip()
    commands = [("bff", fast, ["/opt/homebrew/opt/openjdk@17/bin/java", "-Djava.net.useSystemProxies=false", "-cp", classpath, "local.portalsession.LocalSessionApplication", "--server.port=8291", "--server.address=127.0.0.1"], None)]
    for side in REVISIONS:
        source = ROOT / binding["source"][side]["path"]
        folder = RUNTIME / side
        root_source = ROOT / binding["root_source"]["path"]
        for kind, cwd in (("mfe", source), ("root", root_source)):
            port = PORTS[side + "_" + kind]
            commands.append((side + "-" + kind, cwd, ["node", str(cwd / "node_modules/webpack/bin/webpack.js"), "serve", "--config", str(folder / (kind + ".webpack.cjs"))], port))
    records = []
    for name, cwd, command, port in commands:
        env = os.environ.copy()
        env.update({"NPM_CONFIG_UPDATE_NOTIFIER": "false", "mode": "development", "orgName": "fm", "devtool": "source-map", "isLocal": "true", "publicUrl": "", "importmap": "/importmaplocal.json"})
        if port:
            env["port"] = str(port)
        log = RUNTIME / (name + ".log")
        with log.open("x") as stream:
            process = subprocess.Popen(command, cwd=cwd, env=env, stdout=stream, stderr=subprocess.STDOUT, start_new_session=True)
        records.append({"name": name, "pid": process.pid, "owned": True, "started_at": now(), "argv": command, "cwd": str(cwd), "log": str(log)})
        save(process_file, records)
    print(json.dumps({"status": "STARTED", "processes": [{"name": r["name"], "pid": r["pid"]} for r in records], "readiness": "NOT_ASSERTED"}))


def stop():
    process_file = RUNTIME / "processes.json"
    records = json.loads(process_file.read_text())
    results = []
    for record in records:
        pid = record["pid"]
        result = {"name": record["name"], "pid": pid}
        current = subprocess.run(["ps", "-p", str(pid), "-o", "command="], capture_output=True, text=True).stdout.strip()
        marker = "local.portalsession.LocalSessionApplication" if record["name"] == "bff" else str(RUNTIME)
        port_matches = record["name"] != "bff" or "--server.port=8291" in current
        if not current:
            result["status"] = "ALREADY_EXITED"
        elif marker not in current or not port_matches:
            result["status"] = "IDENTITY_MISMATCH_NOT_SIGNALED"
        else:
            os.killpg(pid, signal.SIGTERM)
            result["status"] = "OWNED_PROCESS_GROUP_SIGTERM_SENT"
        results.append(result)
    save(OUT / "local-cleanup.json", {"completed_at": now(), "results": results})
    print(json.dumps(results))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("prepare", "start", "stop"))
    args = parser.parse_args()
    {"prepare": prepare, "start": start, "stop": stop}[args.operation]()
