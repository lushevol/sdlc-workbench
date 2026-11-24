"""Run exact-source logout comparisons with offline jars and per-case evidence checkpoints."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
REPO = ROOT / "repos/services/single-ui-bff"
CACHE = ROOT / ".workbench/current-bff-audit"
JAVA_HOME = Path("/opt/homebrew/opt/openjdk@17/bin")
REVISIONS = {
    "baseline": "19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a",
    "candidate": "134a340472f29d2a4136e07e516690de6a18e323",
}
CANONICAL = {
    "01-intake.md": "1650a20f8a2aba2105b30b8abc4bd2a881f58ee335925a3daa9f6a6c0d0e0948",
    "06-test-cases.md": "5622dab3b635113ff0137fbf66489f385bbcb11dc4444ec0070f7203d19a7037",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n")
    temporary.replace(path)


def timestamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def parsed_inputs(output):
    paths = []
    for kind, value in re.findall(r"\[parsing started (SimpleFileObject|DirectoryFileObject)\[([^\]]+\.java)\]\]", output):
        if kind == "DirectoryFileObject":
            root, relative = value.split(":", 1)
            path = Path(root) / relative
        else:
            path = Path(value)
        if path.is_file():
            paths.append(path)
    return sorted(set(paths))


def main():
    if (OUT / "paired-execution.json").exists():
        raise SystemExit("Existing run retained; choose a new evidence directory for another run")
    for name, expected in CANONICAL.items():
        assert digest(OUT.parents[1] / name) == expected, name
    jars = [Path(p) for p in (CACHE / "classpath.txt").read_text().strip().split(":") if p.endswith(".jar")]
    assert jars and all(p.is_file() for p in jars), "Offline dependency cache is incomplete"
    scratch = Path(tempfile.mkdtemp(prefix="workbench-paired-logout-20261030-", dir="/private/tmp"))
    classpath = str(CACHE / "classes") + ":" + ":".join(map(str, jars))
    record = {
        "started_at": timestamp(),
        "stage": "READY bounded local paired controller experiment",
        "scratch": str(scratch),
        "runner_sha256": digest(Path(__file__)),
        "probe_sha256": digest(OUT / "SecurityLogoutProbe.java"),
        "user_input_sha256": digest(OUT / "user-input.md"),
        "canonical_before": CANONICAL,
        "java_version": subprocess.run([str(JAVA_HOME / "java"), "-version"], capture_output=True, text=True).stderr,
        "dependency_cache_manifest_sha256": digest(CACHE / "source-build-manifest.json"),
        "dependencies": [{"path": str(p), "sha256": digest(p)} for p in jars],
        "cached_application_classes": [
            {"path": str(p.relative_to(CACHE)), "sha256": digest(p)}
            for p in sorted((CACHE / "classes").rglob("*.class"))
        ],
        "configuration": {
            "RSA_bits": 2048, "algorithm": "RSA512", "access_expiration_minutes": 15,
            "refresh_expiration_minutes": 225, "absolute_expiration_minutes": 60,
            "fixture_access_expiry_delta_seconds": {"RN-S001": 600, "RN-S002": -600},
            "clock": "System wall clock; observed timestamps retained; no controlled clock",
            "mockito_maker": "subclass",
        },
        "limits": [
            "Actual controller, RSA JWT verification, and session-service sources are compiled from each pinned export.",
            "Repository persistence uses an in-memory deny set. Entitlements, drawers, and filter collaborators are mocked.",
            "Both revisions use the identical Java probe and assertions; reflection adapts only the renamed entitlement mock API.",
            "Servlet mocks replace HTTP transport. There is no browser, gateway, provider, real database, replica, or protected business service.",
            "Cached public verification dependencies use Spring/Tomcat overrides; private starters are absent. Production runtime equivalence is NOT_ESTABLISHED.",
            "Cached application classes are stale at 834b4155232222347220e47139a502ee43a9cbdf. Executed selected sources and transitively compiled inputs are pinned and hashed.",
            "No business source, production state, credentials, or deployment is changed.",
        ],
        "builds": {}, "cases": [],
        "prior_attempt": "attempt-01-index.json",
    }
    save(OUT / "paired-execution.json", record)
    for label, revision in REVISIONS.items():
        export = scratch / label
        export.mkdir()
        archive = scratch / (label + ".tar")
        with archive.open("wb") as stream:
            subprocess.run(["git", "-C", str(REPO), "archive", revision], stdout=stream, check=True)
        with tarfile.open(archive) as bundle:
            bundle.extractall(export, filter="data")
        source_root = export / "src/main/java"
        package = source_root / "com/scb/sso/singleuibff"
        selected = [package / p for p in (
            "controller/v2/JwtAuthenticationController.java", "util/JwtTokenUtil.java",
            "service/v1/implementation/SessionServiceImplementation.java",
            "service/v2/authorization/TileAuthorizationService.java", "util/AdminModuleUtil.java",
        )]
        result_source = package / "service/v2/authorization/TileAuthorizationResult.java"
        if result_source.exists():
            selected.append(result_source)
        classes = scratch / (label + "-classes")
        classes.mkdir()
        extension = classes / "mockito-extensions/org.mockito.plugins.MockMaker"
        extension.parent.mkdir(parents=True)
        extension.write_text("mock-maker-subclass\n")
        common = [str(JAVA_HOME / "javac"), "--release", "17", "-verbose", "-Xprefer:source",
                   "-sourcepath", str(source_root), "-cp", classpath, "-d", str(classes),
                  ]
        # Discover transitive source inputs, then make all inputs explicit for Lombok processing.
        # Implicit javac source loading does not run annotation processors on those inputs.
        discovery_command = [*common, "-proc:none", "-Xmaxerrs", "1000", *map(str, selected), str(OUT / "SecurityLogoutProbe.java")]
        discovery = subprocess.run(discovery_command, capture_output=True, text=True, timeout=120)
        discovery_log = OUT / (label + "-source-discovery.txt")
        discovery_log.write_text(discovery.stdout + discovery.stderr)
        explicit_sources = parsed_inputs(discovery.stderr)
        command = [*common, *map(str, explicit_sources)]
        compilation = subprocess.run(command, capture_output=True, text=True, timeout=120)
        log = OUT / (label + "-compile.txt")
        log.write_text(compilation.stdout + compilation.stderr)
        parsed_sources = parsed_inputs(compilation.stderr)
        build = {
            "revision": revision, "export": str(export), "archive_sha256": digest(archive),
            "commit_date": subprocess.check_output(["git", "-C", str(REPO), "show", "-s", "--format=%cI", revision], text=True).strip(),
            "command": command, "compile_exit": compilation.returncode,
            "source_discovery": {"command": discovery_command, "exit": discovery.returncode,
                                 "log": discovery_log.name, "sha256": digest(discovery_log),
                                 "purpose": "Source discovery only; generated Lombok members are unavailable with -proc:none"},
            "compile_log": log.name, "compile_log_sha256": digest(log),
            "source_inputs": [{"path": str(p.relative_to(export)) if p.is_relative_to(export) else str(p),
                               "sha256": digest(p)} for p in parsed_sources],
            "selected_sources": [{"path": str(p.relative_to(export)), "sha256": digest(p)} for p in selected],
            "compiled_classes": [{"path": str(p.relative_to(classes)), "sha256": digest(p)} for p in sorted(classes.rglob("*.class"))],
        }
        record["builds"][label] = build
        save(OUT / "paired-execution.json", record)
        if compilation.returncode:
            record["status"] = "BLOCKED_COMPILATION"
            record["finished_at"] = timestamp()
            save(OUT / "paired-execution.json", record)
            print(json.dumps({"status": record["status"], "revision": label, "log": str(log)}))
            return 1
        for case_id in ("RN-S001", "RN-S002"):
            destination = OUT / (label + "-" + case_id + ".json")
            execution = subprocess.run([str(JAVA_HOME / "java"), "-cp", str(classes) + ":" + classpath,
                                        "SecurityLogoutProbe", case_id, revision, str(destination)],
                                       capture_output=True, text=True, timeout=45)
            execution_log = OUT / (label + "-" + case_id + "-output.txt")
            execution_log.write_text(execution.stdout + execution.stderr)
            if destination.exists():
                case = json.loads(destination.read_text())
            else:
                case = {"case_id": case_id, "revision": revision, "status": "ERROR",
                        "reason": "Probe did not create a case result"}
                save(destination, case)
            case.update({"revision_label": label, "result": destination.name, "result_sha256": digest(destination),
                         "execution_exit": execution.returncode, "output": execution_log.name,
                         "output_sha256": digest(execution_log)})
            record["cases"].append(case)
            record["last_case_saved_at"] = timestamp()
            save(OUT / "paired-execution.json", record)
            print(json.dumps({"revision": label, "case_id": case_id, "status": case["status"]}), flush=True)
            if case["status"] == "ERROR":
                record["status"] = "BLOCKED_EXECUTION"
                save(OUT / "paired-execution.json", record)
                return 1
    record["canonical_after"] = {name: digest(OUT.parents[1] / name) for name in CANONICAL}
    assert record["canonical_after"] == CANONICAL
    record["counts"] = {status: sum(c["status"] == status for c in record["cases"]) for status in ("PASSED", "FAILED", "ERROR")}
    record["status"] = "COMPLETED_WITH_ASSERTION_FAILURES" if record["counts"]["FAILED"] else "PASSED"
    record["finished_at"] = timestamp()
    save(OUT / "paired-execution.json", record)
    print(json.dumps({"status": record["status"], "counts": record["counts"]}), flush=True)
    return int(record["counts"]["FAILED"] > 0)


if __name__ == "__main__":
    raise SystemExit(main())
