#!/usr/bin/env python3
"""Run the actual routing mapper's JUnit tests with cached dependencies only."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--java-home", type=Path, required=True)
    parser.add_argument("--cache", type=Path, default=Path.home() / ".m2/repository")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--replace", action="store_true",
                        help="Refresh a mutable candidate result in place; never use for a retained baseline.")
    parser.add_argument("--admin-only", action="store_true",
                        help="Run the existing drawer utility suite without the new routing mapper tests.")
    args = parser.parse_args()
    repo = args.repo.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=args.replace)
    helper = Path(__file__).parent.parent / "frontend-entitlement-impact-20261105/verify_bff_entity_fields.py"
    spec = importlib.util.spec_from_file_location("bff_existing_launcher", helper)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    coordinates = [
        ("org/projectlombok/lombok", "1.18.34", "lombok"),
        ("org/slf4j/slf4j-api", "2.0.16", "slf4j-api"),
        *[("org/springframework/" + name, "6.1.13", name)
          for name in ("spring-core", "spring-context", "spring-beans", "spring-jcl")],
        ("org/springframework/boot/spring-boot", "3.3.4", "spring-boot"),
        ("jakarta/persistence/jakarta.persistence-api", "3.1.0", "jakarta.persistence-api"),
        ("org/hibernate/orm/hibernate-core", "6.5.3.Final", "hibernate-core"),
        ("org/apache/tomcat/embed/tomcat-embed-core", "10.1.39", "tomcat-embed-core"),
        ("org/apache/commons/commons-lang3", "3.14.0", "commons-lang3"),
        ("commons-lang/commons-lang", "2.6", "commons-lang"),
        ("com/auth0/java-jwt", "4.3.0", "java-jwt"),
        *[("com/fasterxml/jackson/core/" + name, "2.17.2", name)
          for name in ("jackson-annotations", "jackson-core", "jackson-databind")],
        *[("org/junit/jupiter/" + name, "5.10.3", name)
          for name in ("junit-jupiter-api", "junit-jupiter-engine", "junit-jupiter-params")],
        *[("org/junit/platform/" + name, "1.10.3", name)
          for name in ("junit-platform-commons", "junit-platform-engine", "junit-platform-launcher")],
        ("org/apiguardian/apiguardian-api", "1.1.2", "apiguardian-api"),
        ("org/opentest4j/opentest4j", "1.3.0", "opentest4j"),
    ]
    jars = [args.cache / path / version / f"{name}-{version}.jar" for path, version, name in coordinates]
    missing = [str(path) for path in jars if not path.is_file()]
    if missing:
        result = {"status": "BLOCKED", "missing": missing}
        (output / "result.json").write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result))
        return 2
    classpath = os.pathsep.join(map(str, jars))
    source = repo / "src/main/java/com/scb/sso/singleuibff/util/EntitlementRouting.java"
    test = repo / "src/test/java/com/scb/sso/singleuibff/util/EntitlementRoutingTest.java"
    tests = [repo / "src/test/java/com/scb/sso/singleuibff/util/AdminModuleUtilTest.java"]
    if not args.admin_only:
        tests.insert(0, test)
    sources = tests + ([source] if source.exists() else []) + [
        repo / "src/main/java/com/scb/sso/singleuibff" / name for name in (
            "dto/config/EntitlementSource.java", "dto/ems2/v2/Action.java",
            "dto/ems2/v2/Subject.java", "dto/ems2/v2/Entity.java", "dto/ems2/v2/Ems2Result.java",
            "dto/response/ResponseOfAuthenticate.java", "dto/request/RequestOfApplicationTile.java",
            "dto/request/RequestOfApplicationCategory.java", "dto/request/RequestOfImportMap.java",
            "config/EMS2ConfigProperties.java", "config/JWTConfigProperties.java",
            "entity/ApplicationCategory.java", "entity/ApplicationTile.java", "entity/ImportMap.java",
            "entity/ApplicationSession.java", "exceptions/JwtException.java", "exceptions/RecordNotCreatedException.java",
            "util/Constant.java", "util/TileEntitlementConfig.java", "util/JwtTokenUtil.java", "util/AdminModuleUtil.java",
            "service/v1/SessionService.java", "service/v2/authorization/TileAuthorizationResult.java",
            "service/v2/filter/ems3/dto/Drawer.java", "service/v2/filter/ems3/util/Constant.java")]
    steps = []
    cases = []
    counts = None

    def run(label: str, command: list[str]) -> subprocess.CompletedProcess:
        process = subprocess.run(command, cwd=repo, text=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, timeout=60)
        log = output / f"{label}.log"
        log.write_text(process.stdout)
        steps.append({"name": label, "exit_code": process.returncode, "deadline_seconds": 60,
                      "command": command, "log": log.name, "sha256": digest(log)})
        return process

    with tempfile.TemporaryDirectory(prefix="bff-routing-") as temporary:
        directory = Path(temporary)
        launcher = directory / "BffEntityFieldLauncher.java"
        launcher.write_text(module.RUNNER)
        classes = directory / "classes"
        classes.mkdir()
        compilation = run("compile", [str(args.java_home / "bin/javac"), "--release", "17",
            "-cp", classpath, "-processorpath", str(jars[0]), "-d", str(classes),
            *map(str, sources), str(launcher)])
        if compilation.returncode == 0:
            execution = run("tests", [str(args.java_home / "bin/java"), "-cp",
                str(classes) + os.pathsep + classpath, "BffEntityFieldLauncher",
                *["com.scb.sso.singleuibff.util." + path.stem for path in tests]])
            for line in execution.stdout.splitlines():
                if line.startswith("CASE\t"):
                    _, status, class_name, method_name, display = line.split("\t", 4)
                    cases.append({"status": status, "class": class_name, "method": method_name, "display": display})
                elif line.startswith("COUNTS\t"):
                    counts = dict(zip(("found", "started", "passed", "failed", "skipped", "aborted", "failed_containers"),
                                      map(int, line.split("\t")[1:])))
    passed = counts is not None and counts["found"] > 0 and counts["passed"] == counts["found"] and not any(
        counts[key] for key in ("failed", "skipped", "aborted", "failed_containers"))
    result = {
        "recorded_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "status": "PASSED" if passed else "FAILED",
        "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip(),
        "production_mapper_present": source.exists(),
        "requested_test_classes": [path.stem for path in tests],
        "sources": [{"path": str(path.relative_to(repo)), "sha256": digest(path)} for path in sources],
        "runner": {"path": str(Path(__file__)), "sha256": digest(Path(__file__)),
                   "reused_launcher": str(helper), "launcher_sha256": digest(helper)},
        "dependencies": [{"path": str(path), "sha256": digest(path)} for path in jars],
        "steps": steps, "counts": counts, "cases": cases,
        "limits": ["Actual selected mapper, DTO, drawer utility, and JUnit tests, compiled with cached real jars and Java 17.",
                   "No fabricated application classes, enterprise calls, or dependency acquisition.",
                   "Spring isolation uses cached 6.1.13 rather than every BFF explicit override.",
                   "This focused execution excludes Spring controller integration and the complete Maven suite."]}
    (output / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "counts": counts, "output": str(output)}))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
