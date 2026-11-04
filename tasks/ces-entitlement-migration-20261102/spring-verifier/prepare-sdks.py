#!/usr/bin/env python3
"""Build exact SDK Git objects without changing the owning checkout.

Python 3.10+, Git, Java 17+, and Maven 3.8+ are required. The --check path
performs no acquisition. Build deadlines bound Maven and its child processes.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
import xml.etree.ElementTree as ET

PROJECT = Path(__file__).resolve().parent
REVISIONS = {
    "ems2": "b0aa82005e7f14202f85f5ef583f25e42da9eeb3",
    "ces": "fd9a157e260850b6d9efa10da3223950ea61133a",
}


class PreparationError(Exception):
    """A bounded prerequisite or build step did not complete."""


def positive_seconds(value: str) -> int:
    try:
        seconds = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("Use a whole number of seconds.") from error
    if seconds < 1 or seconds > 86400:
        raise argparse.ArgumentTypeError("Use 1 through 86400 seconds.")
    return seconds


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def command_output(command: list[str], *, env: dict[str, str] | None = None,
                   cwd: Path | None = None) -> str:
    try:
        result = subprocess.run(command, cwd=cwd, env=env, capture_output=True,
                                text=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise PreparationError("Prerequisite command is unavailable or exceeded 15 seconds.") from error
    if result.returncode:
        raise PreparationError("Prerequisite command failed. Check Git, Java, and Maven locally.")
    return result.stdout + result.stderr


def executable(value: str, component: str) -> str:
    resolved = shutil.which(value)
    if not resolved:
        raise PreparationError(f"{component} is unavailable. Install the approved tool and add its executable to PATH.")
    return resolved


def diagnostics(options: argparse.Namespace) -> tuple[dict[str, str], dict]:
    sdk_repo = options.sdk_repo.expanduser().resolve()
    if not sdk_repo.is_dir():
        raise PreparationError("SDK repository is missing. Supply --sdk-repo with the independent SDK checkout path.")
    env = dict(os.environ)
    if options.java_home:
        selected_jdk = options.java_home.expanduser().resolve()
        java_bin = selected_jdk / "bin" / ("java.exe" if os.name == "nt" else "java")
        if not java_bin.is_file():
            raise PreparationError("The selected --java-home lacks bin/java. Select the approved JDK root.")
        env["JAVA_HOME"] = str(selected_jdk)
        env["PATH"] = str(selected_jdk / "bin") + os.pathsep + env.get("PATH", "")
    java = shutil.which("java", path=env.get("PATH"))
    if not java:
        raise PreparationError("Java is unavailable. Install approved JDK 17 and set --java-home or PATH.")
    java_version = command_output([java, "-version"], env=env)
    major = re.search(r'version\s+"(\d+)', java_version)
    if major is None or int(major.group(1)) < 17:
        raise PreparationError("Java 17 or later is required. Select approved JDK 17 with --java-home.")
    git = executable("git", "Git")
    maven = executable(options.maven, "Maven")
    maven_version = command_output([maven, "-version"], env=env)
    version = re.search(r"Apache Maven\s+(\d+)\.(\d+)(?:\.(\d+))?", maven_version)
    if version is None or tuple(map(int, version.groups()[:2])) < (3, 8):
        raise PreparationError("Maven 3.8 or later is required. Select an approved Maven executable with --maven.")
    maven_java = re.search(r"Java version:\s*(\d+)", maven_version)
    if maven_java is None or int(maven_java.group(1)) < 17:
        raise PreparationError("Maven must use Java 17 or later. Set --java-home to the approved JDK root.")
    for name, revision in REVISIONS.items():
        resolved = command_output([git, "-C", str(sdk_repo), "rev-parse", "--verify", revision + "^{commit}"]).strip()
        if resolved != revision:
            raise PreparationError(f"The {name} SDK revision is unavailable. Import the exact reviewed Git commit into this checkout.")
    destination = options.output.expanduser().resolve()
    parent = destination
    while not parent.exists() and parent != parent.parent:
        parent = parent.parent
    if not parent.is_dir() or not os.access(parent, os.W_OK):
        raise PreparationError("The output location is not writable. Select a writable --output directory.")
    if destination.exists() and not destination.is_dir():
        raise PreparationError("The output path is a file. Select a directory with --output.")
    if options.maven_repository:
        cache = options.maven_repository.expanduser().resolve()
        parent_cache = cache
        while not parent_cache.exists() and parent_cache != parent_cache.parent:
            parent_cache = parent_cache.parent
        if not parent_cache.is_dir() or not os.access(parent_cache, os.W_OK):
            raise PreparationError("Maven repository is not writable. Select a writable --maven-repository directory.")
    report = {
        "status": "READY",
        "sdk_repository": str(sdk_repo),
        "java_major": int(major.group(1)),
        "java_version": java_version.splitlines()[0],
        "java": java,
        "maven_version": ".".join(part for part in version.groups() if part is not None),
        "git": git,
        "maven": maven,
        "output": str(destination),
        "revisions": REVISIONS,
        "mode": "OFFLINE" if options.offline else "CONNECTED",
        "deadline_seconds_per_build": options.deadline_seconds,
        "limits": ["Readiness does not establish artifact availability, live access, or passing SDK tests."],
    }
    return env, report


def extract_archive(payload: bytes, destination: Path) -> None:
    """Permit regular files and directories only, with no escaping paths."""
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:") as archive:
        for member in archive.getmembers():
            relative = PurePosixPath(member.name)
            if relative.is_absolute() or ".." in relative.parts or not (member.isdir() or member.isfile()):
                raise PreparationError("SDK archive contains an unsupported or unsafe path.")
            target = destination.joinpath(*relative.parts)
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                stream = archive.extractfile(member)
                if stream is None:
                    raise PreparationError("SDK archive file cannot be read.")
                with stream, target.open("wb") as output:
                    shutil.copyfileobj(stream, output)


def stop_process_tree(process: subprocess.Popen) -> None:
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       timeout=15, check=False)
    else:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    process.wait(timeout=15)


def run_build(command: list[str], source: Path, env: dict[str, str], log: Path,
              deadline: int) -> int:
    launch = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt" else {"start_new_session": True}
    with log.open("wb") as output:
        try:
            process = subprocess.Popen(command, cwd=source, env=env,
                                       stdout=output, stderr=subprocess.STDOUT, **launch)
        except OSError as error:
            raise PreparationError("Cannot launch Maven. Check the executable, JDK, and writable build directory.") from error
        try:
            return process.wait(timeout=deadline)
        except subprocess.TimeoutExpired:
            stop_process_tree(process)
            output.write(f"\nPREPARATION_TIMEOUT: Maven exceeded {deadline} seconds.\n".encode("utf-8"))
            output.flush()
            return 124


def test_counts(source: Path) -> dict[str, int]:
    counts = dict(tests=0, failures=0, errors=0, skipped=0)
    for report in source.glob("**/target/surefire-reports/TEST-*.xml"):
        suite = ET.parse(report).getroot()
        for key in counts:
            counts[key] += int(suite.get(key, "0"))
    return counts


def prepare(options: argparse.Namespace, env: dict[str, str], check: dict) -> dict:
    destination = options.output.expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    for name in REVISIONS:
        if (destination / f"{name}-sdk.jar").exists():
            raise PreparationError("An SDK JAR already exists. Preserve it and select a new --output directory.")
    if (destination / "sdk-manifest.json").exists():
        raise PreparationError("An SDK manifest already exists. Select a new --output directory.")
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    evidence = destination / "build-evidence" / run_id
    evidence.mkdir(parents=True, exist_ok=False)
    manifest = {"schema_version": 1, "created_at": datetime.now(timezone.utc).isoformat(),
                "status": "INCOMPLETE", "inputs": check, "sdks": {},
                "limits": ["SDK unit tests use mock CES responses. No live migration result is established."]}
    manifest_path = evidence / "preparation.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    try:
        with tempfile.TemporaryDirectory(prefix="ems2-ces-sdk-") as temporary:
            for name, revision in REVISIONS.items():
                source = Path(temporary) / name
                source.mkdir()
                archive = subprocess.run([check["git"], "-C", check["sdk_repository"], "archive", revision],
                                         capture_output=True, timeout=30)
                if archive.returncode:
                    raise PreparationError(f"Cannot export the exact {name} revision. Check the supplied Git repository.")
                extract_archive(archive.stdout, source)
                inputs = {str(p.relative_to(source)): sha256(p) for p in source.rglob("*") if p.is_file()}
                command = [check["maven"], "--batch-mode", "-Dstyle.color=never", "-Dformatter.skip=true",
                           "-Dmaven.wagon.http.retryHandler.count=1", "-Daether.transport.http.retryHandler.count=1",
                           "-Daether.connector.connectTimeout=15000", "-Daether.connector.requestTimeout=60000"]
                if options.offline:
                    command.append("--offline")
                if options.maven_repository:
                    command.append("-Dmaven.repo.local=" + str(options.maven_repository.expanduser().resolve()))
                command += ["clean", "package"]
                log = evidence / f"{name}-maven.log"
                entry = {"revision": revision, "command": command, "source_sha256": inputs,
                         "status": "BUILDING", "log": str(log.relative_to(destination))}
                manifest["sdks"][name] = entry
                manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
                code = run_build(command, source, env, log, options.deadline_seconds)
                counts = test_counts(source)
                entry.update(exit_code=code, counts=counts, log_sha256=sha256(log))
                reports = evidence / f"{name}-surefire-reports"
                reports.mkdir()
                for report in source.glob("**/target/surefire-reports/*"):
                    if report.is_file():
                        shutil.copy2(report, reports / report.name)
                manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
                if code:
                    if code == 124:
                        raise PreparationError(f"The {name} SDK build exceeded its deadline. Inspect the retained log and restore missing prerequisites.")
                    raise PreparationError(f"The {name} SDK build failed. Inspect its retained Maven log and restore missing prerequisites.")
                if sum(counts[key] for key in ("failures", "errors", "skipped")) or (name == "ces" and counts["tests"] == 0):
                    raise PreparationError(f"The {name} SDK did not complete every applicable test. No readiness was recorded.")
                changed = [path for path, expected in inputs.items() if not (source / path).exists() or sha256(source / path) != expected]
                if changed:
                    raise PreparationError(f"The {name} build changed source bytes. Retain the log and investigate before using the artifact.")
                jars = [p for p in (source / "single-ui-sdk-starter" / "target").glob("fmoportal-auth-sdk-*.jar")
                        if not p.name.endswith(("-sources.jar", "-javadoc.jar", "-tests.jar"))]
                if len(jars) != 1:
                    raise PreparationError(f"The {name} build did not produce one SDK runtime JAR.")
                final_jar = destination / f"{name}-sdk.jar"
                shutil.copy2(jars[0], final_jar)
                entry.update(status="PASSED", artifact=final_jar.name, sha256=sha256(final_jar),
                             baseline_no_tracked_tests=(name == "ems2" and counts["tests"] == 0))
                manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        manifest["baseline"] = {"revision": REVISIONS["ems2"], "sha256": manifest["sdks"]["ems2"]["sha256"], "file": "ems2-sdk.jar"}
        manifest["candidate"] = {"revision": REVISIONS["ces"], "sha256": manifest["sdks"]["ces"]["sha256"], "file": "ces-sdk.jar"}
        manifest["status"] = "READY"
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        (destination / "sdk-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        return manifest
    except Exception:
        manifest["status"] = "INCOMPLETE"
        for entry in manifest["sdks"].values():
            if entry["status"] == "BUILDING":
                entry["status"] = "INCOMPLETE"
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sdk-repo", required=True, type=Path)
    parser.add_argument("--check", action="store_true", help="Diagnose prerequisites without downloads or builds")
    parser.add_argument("--maven", default="mvn", help="Maven executable name or path")
    parser.add_argument("--java-home", type=Path, help="Approved JDK root")
    parser.add_argument("--maven-repository", type=Path, help="Writable Maven cache; reuse for connected and offline runs")
    parser.add_argument("--offline", action="store_true", help="Never acquire dependencies from remote repositories")
    parser.add_argument("--deadline-seconds", type=positive_seconds, default=600, help="Bound each SDK Maven build, including dependency downloads")
    parser.add_argument("--output", type=Path, default=PROJECT / "lib", help="New SDK artifact directory; default: project lib/")
    options = parser.parse_args()
    try:
        env, check = diagnostics(options)
        if options.check:
            print(json.dumps(check, indent=2))
            return 0
        manifest = prepare(options, env, check)
        print(json.dumps({"status": manifest["status"], "output": check["output"],
                          "sdks": {name: {key: entry[key] for key in ("revision", "artifact", "sha256", "counts")}
                                   for name, entry in manifest["sdks"].items()}}, indent=2))
        return 0
    except (PreparationError, subprocess.TimeoutExpired, ET.ParseError, OSError) as error:
        print("SDK preparation is incomplete: " + str(error), file=sys.stderr)
        print("Recovery: check the approved JDK, Maven, and exact Git revisions; inspect retained local build logs.", file=sys.stderr)
        print("For blocked downloads, prepare a matching Maven cache from approved Maven Central or the company mirror.", file=sys.stderr)
        print("Transfer that cache unchanged, then use --offline --maven-repository PATH with a new --output directory.", file=sys.stderr)
        print("Run this command with --check again before retrying. Credential values belong only in private Maven settings.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
