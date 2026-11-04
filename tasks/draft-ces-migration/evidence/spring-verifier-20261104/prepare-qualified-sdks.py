"""Prepare exact SDKs offline using all compile/test goals and the JAR goal.

This controlled fallback does not execute formatter, flatten, or source archive
lifecycle plugins. It never changes SDK source or suppresses SDK test cases.
"""
from pathlib import Path
import datetime
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile

EVIDENCE = Path(__file__).resolve().parent
ROOT = EVIDENCE.parents[3]
PROJECT = ROOT / "tasks/draft-ces-migration/spring-verifier"
REPO = ROOT / "repos/libraries/single-ui-sdk-starter"
CACHE = Path("/private/tmp/sdk-coverage-20261104-yiiye_1q/repository")
LIB = PROJECT / "lib"
RUN = EVIDENCE / "qualified-sdk-preparation"
JAVA = "/opt/homebrew/opt/openjdk@17"
SPEC = importlib.util.spec_from_file_location("sdk_prepare", PROJECT / "prepare-sdks.py")
HELPER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HELPER)
LIMITS = [
    "Offline qualified module goals compile unchanged source, execute every declared test, and create runtime JARs.",
    "Formatter, flatten, source archive, and unrelated reactor lifecycle steps were not executed.",
    "The ordinary clean package helper failed before compilation because exact formatter dependencies were absent.",
    "The original baseline declares no tracked test cases; its zero-test result is explicit.",
    "Candidate tests use controlled responses. No live company endpoint or deployed consumer was verified.",
]


def save(document):
    (RUN / "preparation.json").write_text(json.dumps(document, indent=2) + "\n")


def main():
    RUN.mkdir(exist_ok=False)
    LIB.mkdir(exist_ok=True)
    for target in [LIB / "ems2-sdk.jar", LIB / "ces-sdk.jar", LIB / "sdk-manifest.json"]:
        if target.exists():
            raise RuntimeError("Existing artifact must not be overwritten: " + str(target))
    failed = LIB / "build-evidence/20261104T033959Z"
    if failed.is_dir():
        shutil.copytree(failed, RUN / "ordinary-helper-failure")
    env = dict(os.environ)
    env["JAVA_HOME"] = JAVA
    env["PATH"] = JAVA + "/bin" + os.pathsep + env.get("PATH", "")
    manifest = {"schema_version": 1, "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "status": "INCOMPLETE", "mode": "OFFLINE_QUALIFIED_MODULE_GOALS", "sdks": {}, "limits": LIMITS}
    save(manifest)
    with tempfile.TemporaryDirectory(prefix="qualified-sdk-", dir="/private/tmp") as temporary:
        temporary = Path(temporary)
        settings = temporary / "settings.xml"
        settings.write_text('<settings xmlns="http://maven.apache.org/SETTINGS/1.2.0"/>\n')
        for name, revision in HELPER.REVISIONS.items():
            source = temporary / name
            source.mkdir()
            payload = subprocess.check_output(["git", "-C", str(REPO), "archive", revision], timeout=30)
            HELPER.extract_archive(payload, source)
            inputs = {str(p.relative_to(source)): HELPER.sha256(p) for p in sorted(source.rglob("*")) if p.is_file()}
            command = ["/opt/homebrew/bin/mvn", "-B", "-o", "-s", str(settings), "-Dstyle.color=never",
                       "-Dmaven.repo.local=" + str(CACHE), "-Dformatter.skip=true", "-pl", "single-ui-sdk-starter",
                       "org.apache.maven.plugins:maven-resources-plugin:3.3.1:resources",
                       "org.apache.maven.plugins:maven-compiler-plugin:3.8.0:compile",
                       "org.apache.maven.plugins:maven-resources-plugin:3.3.1:testResources",
                       "org.apache.maven.plugins:maven-compiler-plugin:3.8.0:testCompile",
                       "org.apache.maven.plugins:maven-surefire-plugin:3.5.5:test",
                       "org.apache.maven.plugins:maven-jar-plugin:3.4.2:jar"]
            log = RUN / (name + "-maven.log")
            entry = {"revision": revision, "command": command, "source_sha256": inputs,
                     "status": "BUILDING", "deadline_seconds": 180, "log": log.name}
            manifest["sdks"][name] = entry
            save(manifest)
            code = HELPER.run_build(command, source, env, log, 180)
            counts = HELPER.test_counts(source)
            changed = [path for path, digest in inputs.items() if not (source / path).is_file() or HELPER.sha256(source / path) != digest]
            entry.update(exit_code=code, counts=counts, source_changes=changed, log_sha256=HELPER.sha256(log))
            reports = RUN / (name + "-surefire-reports")
            reports.mkdir()
            for report in source.glob("**/target/surefire-reports/*"):
                if report.is_file():
                    shutil.copy2(report, reports / report.name)
            save(manifest)
            if code or changed or any(counts[key] for key in ("failures", "errors", "skipped")) or (name == "ces" and not counts["tests"]):
                entry["status"] = "INCOMPLETE_OR_FAILED"
                save(manifest)
                raise RuntimeError("Exact SDK preparation did not pass: " + name)
            artifacts = [path for path in (source / "single-ui-sdk-starter/target").glob("fmoportal-auth-sdk-*.jar")
                         if not path.name.endswith(("-sources.jar", "-javadoc.jar", "-tests.jar"))]
            if len(artifacts) != 1:
                raise RuntimeError("Expected one runtime JAR: " + name)
            target = LIB / (name + "-sdk.jar")
            shutil.copy2(artifacts[0], target)
            entry.update(status="PASSED_CONTROLLED_SCOPE", artifact=target.name, sha256=HELPER.sha256(target))
            save(manifest)
    manifest.update(status="READY_CONTROLLED_SCOPE",
                    baseline={"revision": HELPER.REVISIONS["ems2"], "sha256": manifest["sdks"]["ems2"]["sha256"], "file": "ems2-sdk.jar"},
                    candidate={"revision": HELPER.REVISIONS["ces"], "sha256": manifest["sdks"]["ces"]["sha256"], "file": "ces-sdk.jar"})
    save(manifest)
    (LIB / "sdk-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"status": manifest["status"], "counts": {name: row["counts"] for name, row in manifest["sdks"].items()},
                      "baseline": manifest["baseline"], "candidate": manifest["candidate"]}, indent=2))


if __name__ == "__main__":
    main()
