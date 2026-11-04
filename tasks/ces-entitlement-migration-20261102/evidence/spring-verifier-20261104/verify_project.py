"""Retain the complete build and actual-JAR replay predicates for this task."""
from pathlib import Path
import datetime
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET

EVIDENCE = Path(__file__).resolve().parent
PROJECT = EVIDENCE.parents[1] / "spring-verifier"
JAVA_HOME = Path("/opt/homebrew/opt/openjdk@17")
CACHE = Path("/private/tmp/sdk-coverage-20261104-yiiye_1q/repository")
SETTINGS = CACHE.parent / "settings.xml"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def source_hashes():
    return {str(p.relative_to(PROJECT)): digest(p) for p in PROJECT.rglob("*")
            if p.is_file() and not {"target", "lib", "reports", "__pycache__"}.intersection(p.relative_to(PROJECT).parts)}


def execute(command, directory, env, deadline):
    directory.mkdir()
    inputs = {"startedAt": now(), "command": command, "cwd": str(PROJECT),
              "sourceHashes": source_hashes(), "javaHome": str(JAVA_HOME),
              "runnerSha256": digest(Path(__file__)),
              "limits": ["Controlled local execution with synthetic HTTP responses; no company endpoint access."]}
    save(directory / "inputs.json", inputs)
    with (directory / "command.log").open("wb") as stream:
        try:
            code = subprocess.run(command, cwd=PROJECT, env=env, stdout=stream,
                                  stderr=subprocess.STDOUT, timeout=deadline).returncode
        except subprocess.TimeoutExpired:
            code = 124
    return inputs, code


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-label", default="03")
    options = parser.parse_args()
    env = dict(os.environ)
    env["JAVA_HOME"] = str(JAVA_HOME)
    env["PATH"] = str(JAVA_HOME / "bin") + os.pathsep + env["PATH"]
    build = EVIDENCE / ("full-build-" + options.run_label)
    command = ["/opt/homebrew/bin/mvn", "-B", "-o", "-s", str(SETTINGS),
               "-Dmaven.repo.local=" + str(CACHE), "clean", "verify"]
    inputs, code = execute(command, build, env, 240)
    counts = dict(tests=0, failures=0, errors=0, skipped=0)
    (build / "surefire-reports").mkdir()
    for path in (PROJECT / "target/surefire-reports").glob("*"):
        if not path.is_file():
            continue
        shutil.copy2(path, build / "surefire-reports" / path.name)
        if path.name.startswith("TEST-") and path.suffix == ".xml":
            suite = ET.parse(path).getroot()
            for key in counts:
                counts[key] += int(suite.get(key, "0"))
    jar = PROJECT / "target/ems2-ces-spring-verifier-1.0.0.jar"
    passed = code == 0 and counts["tests"] > 0 and not sum(counts[k] for k in ("failures", "errors", "skipped"))
    unchanged = inputs["sourceHashes"] == source_hashes()
    result = {"finishedAt": now(), "exitCode": code, "counts": counts,
              "status": "PASSED" if passed and unchanged else "FAILED", "sourceBytesUnchanged": unchanged,
              "jarSha256": digest(jar) if jar.exists() else None}
    save(build / "result.json", result)
    print(json.dumps(result), flush=True)
    if not passed or not unchanged:
        return 1
    replay = EVIDENCE / ("actual-sdk-replays-" + options.run_label)
    replay.mkdir()
    save(replay / "sdk-manifest.json", json.loads((PROJECT / "lib/sdk-manifest.json").read_text()))
    manifest = json.loads((PROJECT / "lib/sdk-manifest.json").read_text())
    manifest["baseline"]["sha256"] = "0" * 64
    save(replay / "wrong-hash-manifest.json", manifest)
    cases = [("match", [], 0, "SCOPED_SDK_PARITY_PASS"),
             ("missing", ["--verification.replay.variant=missing"], 1, "DIFFERENCES"),
             ("extra", ["--verification.replay.variant=extra"], 1, "DIFFERENCES"),
             ("failure", ["--verification.replay.variant=failure"], 2, "INCOMPLETE"),
             ("empty", ["--verification.replay.variant=empty"], 0, "SCOPED_SDK_PARITY_PASS"),
             ("incomplete-population", ["--verification.population-complete=false"], 2, "INCOMPLETE"),
             ("malformed", ["--verification.replay.variant=malformed"], 2, "INCOMPLETE"),
             ("wrong-artifact", ["--verification.manifest=" + str(replay / "wrong-hash-manifest.json")], 2, "INCOMPLETE")]
    inventory = []
    for name, args, expected_exit, expected_status in cases:
        directory = replay / name
        reports = directory / "output"
        command = [str(PROJECT / "run.command"), "--verification.output=" + str(reports), *args]
        inputs, code = execute(command, directory, env, 90)
        report_files = list(reports.glob("*/report.json"))
        assertions = {"oneReport": len(report_files) == 1, "expectedExit": code == expected_exit,
                      "sourceBytesUnchanged": inputs["sourceHashes"] == source_hashes()}
        report = json.loads(report_files[0].read_text()) if len(report_files) == 1 else {}
        assertions.update(expectedStatus=report.get("status") == expected_status,
                          completeMigrationNotClaimed=report.get("migrationVerified") is False,
                          threeAccountsRetained=len(report.get("accounts", [])) == 3)
        accounts = report.get("accounts", [])
        if name in ("match", "empty"):
            assertions["allMatch"] = all(a.get("status") == "MATCH" for a in accounts)
            assertions["scopedAccountParity100"] = report.get("metrics", {}).get("sdkParityPercent") == 100
        if name == "match" and accounts:
            baseline = accounts[0].get("baseline", {}).get("permissions", {})
            assertions["emptyRolePreserved"] = baseline.get("LEGACY_APP:EMPTY") == {}
            assertions["duplicatesPreserved"] = baseline.get("LEGACY_APP:READER", {}).get("TRADE") == ["view", "view", "export"]
            assertions["threeEntityScopes"] = report.get("entities") == ["LEGACY_APP", "LEGACY_DATA", "LEGACY_SYSTEM"]
        if name in ("missing", "extra"):
            bob = next((a for a in accounts if a.get("userId") == "bob"), {})
            kind = "MISSING_PERMISSION" if name == "missing" else "ADDITIONAL_PERMISSION"
            assertions["exactDifference"] = any(d.get("kind") == kind for d in bob.get("comparison", {}).get("differences", []))
            if name == "extra":
                assertions["extraPreventsFalse100Pass"] = bob.get("comparison", {}).get("metrics", {}).get("roleScopedPermissions", {}).get("coveragePercent") == 100
        if name == "failure":
            bob = next((a for a in accounts if a.get("userId") == "bob"), {})
            assertions["httpFailureUnassessed"] = bob.get("status") == "UNASSESSED" and "HTTP_503" in bob.get("candidate", {}).get("errors", [])
        if name == "empty":
            assertions["zeroPermissionDenominatorsStayNull"] = all(a.get("comparison", {}).get("metrics", {}).get("roleScopedPermissions", {}).get("coveragePercent") is None for a in accounts)
        if name == "incomplete-population":
            assertions["noParityPercentage"] = report.get("metrics", {}).get("sdkParityPercent") is None
        if name == "malformed":
            assertions["dtoErrorsCannotBecomeEmptyParity"] = all(a.get("status") == "UNASSESSED" and "SDK_RESPONSE_DESERIALIZATION_FAILURE" in a.get("candidate", {}).get("errors", []) for a in accounts)
        if name == "wrong-artifact":
            assertions["wrongArtifactsUnassessed"] = all(a.get("status") == "UNASSESSED" and "ARTIFACT_SHA256_MISMATCH" in a.get("baseline", {}).get("errors", []) for a in accounts)
        if report_files:
            text = report_files[0].read_text()
            assertions["syntheticTokenNotRetained"] = "synthetic-service-token" not in text
        result = {"case": name, "finishedAt": now(), "exitCode": code, "actualStatus": report.get("status"),
                  "status": "PASSED" if all(assertions.values()) else "FAILED", "assertions": assertions,
                  "artifactHashes": {str(p.relative_to(directory)): digest(p) for p in directory.rglob("*") if p.is_file()}}
        save(directory / "result.json", result)
        inventory.append({"case": name, "status": result["status"], "result": name + "/result.json"})
        save(replay / "progress.json", {"completedAt": now(), "cases": inventory})
        print(json.dumps({"case": name, "status": result["status"], "assertions": assertions}), flush=True)
    result = {"finishedAt": now(), "status": "PASSED" if all(c["status"] == "PASSED" for c in inventory) else "FAILED",
              "cases": inventory, "sourceHashes": source_hashes(), "verifierJarSha256": digest(jar),
              "limits": ["Synthetic HTTP services, actual exact SDK artifacts; no company credentials or endpoints.",
                         "Scoped SDK permission maps only; enterprise migration remains unverified."]}
    save(replay / "result.json", result)
    return 0 if result["status"] == "PASSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
