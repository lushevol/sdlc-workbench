#!/usr/bin/env python3
"""Run bounded offline checks against real BFF sources and cached Java jars.

No source substitution, dependency acquisition, or application startup occurs.
The isolated checks do not replace the owning Maven build or complete suite.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


RUNNER = r'''
import org.junit.platform.engine.discovery.DiscoverySelectors;
import org.junit.platform.launcher.Launcher;
import org.junit.platform.launcher.LauncherDiscoveryRequest;
import org.junit.platform.launcher.TestExecutionListener;
import org.junit.platform.launcher.TestIdentifier;
import org.junit.platform.launcher.core.LauncherDiscoveryRequestBuilder;
import org.junit.platform.launcher.core.LauncherFactory;
import org.junit.platform.launcher.listeners.SummaryGeneratingListener;
import org.junit.platform.launcher.listeners.TestExecutionSummary;
import org.junit.platform.engine.TestExecutionResult;
import org.junit.platform.engine.support.descriptor.MethodSource;

public final class BffEntityFieldLauncher {
    public static void main(String[] args) {
        LauncherDiscoveryRequestBuilder builder = LauncherDiscoveryRequestBuilder.request();
        for (String name : args) builder.selectors(DiscoverySelectors.selectClass(name));
        LauncherDiscoveryRequest request = builder.build();
        SummaryGeneratingListener summary = new SummaryGeneratingListener();
        Launcher launcher = LauncherFactory.create();
        launcher.registerTestExecutionListeners(summary, new TestExecutionListener() {
            @Override public void executionFinished(TestIdentifier id, TestExecutionResult result) {
                if (!id.isTest()) return;
                String source = id.getSource().map(Object::toString).orElse("");
                String className = "";
                String methodName = "";
                if (id.getSource().orElse(null) instanceof MethodSource method) {
                    className = method.getClassName();
                    methodName = method.getMethodName();
                }
                System.out.println("CASE\t" + result.getStatus() + "\t" + className
                    + "\t" + methodName + "\t" + id.getDisplayName().replace('\t', ' '));
                result.getThrowable().ifPresent(error -> error.printStackTrace(System.out));
            }
        });
        launcher.execute(request);
        TestExecutionSummary result = summary.getSummary();
        System.out.println("COUNTS\t" + result.getTestsFoundCount() + "\t" + result.getTestsStartedCount()
            + "\t" + result.getTestsSucceededCount() + "\t" + result.getTestsFailedCount()
            + "\t" + result.getTestsSkippedCount() + "\t" + result.getTestsAbortedCount()
            + "\t" + result.getContainersFailedCount());
        for (TestExecutionSummary.Failure failure : result.getFailures()) {
            System.out.println("FAILURE\t" + failure.getTestIdentifier().getDisplayName());
            failure.getException().printStackTrace(System.out);
        }
        if (result.getTestsFoundCount() == 0 || result.getTestsFailedCount() != 0
            || result.getTestsAbortedCount() != 0 || result.getTestsSkippedCount() != 0
            || result.getContainersFailedCount() != 0) System.exit(1);
    }
}
'''


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--cache", type=Path, default=Path.home() / ".m2/repository")
    parser.add_argument("--java-home", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mapper-only", action="store_true",
                        help="Do not repeat a service compilation already blocked by missing private dependencies.")
    args = parser.parse_args()
    repo = args.repo.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    coordinates = [
        ("org/projectlombok/lombok", "1.18.34", "lombok"),
        ("com/fasterxml/jackson/core/jackson-annotations", "2.17.2", "jackson-annotations"),
        ("com/fasterxml/jackson/core/jackson-core", "2.17.2", "jackson-core"),
        ("com/fasterxml/jackson/core/jackson-databind", "2.17.2", "jackson-databind"),
        ("org/slf4j/slf4j-api", "2.0.16", "slf4j-api"),
        *[("org/springframework/" + name, "6.1.13", name) for name in
          ["spring-core", "spring-context", "spring-beans", "spring-jcl", "spring-test", "spring-web", "spring-expression", "spring-aop"]],
        ("org/springframework/boot/spring-boot", "3.3.4", "spring-boot"),
        ("org/springframework/retry/spring-retry", "2.0.11", "spring-retry"),
        ("jakarta/persistence/jakarta.persistence-api", "3.1.0", "jakarta.persistence-api"),
        ("jakarta/annotation/jakarta.annotation-api", "2.1.1", "jakarta.annotation-api"),
        ("org/apache/tomcat/embed/tomcat-embed-core", "10.1.39", "tomcat-embed-core"),
        ("org/apache/commons/commons-lang3", "3.14.0", "commons-lang3"),
        ("commons-lang/commons-lang", "2.6", "commons-lang"),
        ("com/auth0/java-jwt", "4.3.0", "java-jwt"),
        ("org/jasypt/jasypt", "1.9.3", "jasypt"),
        *[("org/junit/jupiter/" + name, "5.10.3", name) for name in
          ["junit-jupiter-api", "junit-jupiter-engine", "junit-jupiter-params"]],
        *[("org/junit/platform/" + name, "1.10.3", name) for name in
          ["junit-platform-commons", "junit-platform-engine", "junit-platform-launcher"]],
        ("org/apiguardian/apiguardian-api", "1.1.2", "apiguardian-api"),
        ("org/opentest4j/opentest4j", "1.3.0", "opentest4j"),
        ("org/mockito/mockito-core", "5.11.0", "mockito-core"),
        ("org/mockito/mockito-junit-jupiter", "5.11.0", "mockito-junit-jupiter"),
        ("net/bytebuddy/byte-buddy", "1.14.19", "byte-buddy"),
        ("net/bytebuddy/byte-buddy-agent", "1.14.19", "byte-buddy-agent"),
        ("org/objenesis/objenesis", "3.3", "objenesis"),
        ("io/micrometer/micrometer-observation", "1.13.4", "micrometer-observation"),
        ("io/micrometer/micrometer-commons", "1.13.4", "micrometer-commons"),
    ]
    jars = [args.cache / path / version / f"{name}-{version}.jar"
            for path, version, name in coordinates]
    missing = [str(path) for path in jars if not path.is_file()]
    if missing:
        (output / "result.json").write_text(json.dumps({"status": "BLOCKED", "missing": missing}, indent=2) + "\n")
        print(json.dumps({"status": "BLOCKED", "missing": missing}))
        return 2
    classpath = os.pathsep.join(map(str, jars))
    main_source = repo / "src/main/java"
    test_source = repo / "src/test/java"
    javac = args.java_home / "bin/javac"
    java = args.java_home / "bin/java"
    prefix = "com.scb.sso.singleuibff.service.v2.authorization."
    test_names = ["AuthorizationResultMapperTest", "Ems3ApplicationNameAuthorizationTest", "TileAuthorizationServiceImplTest"]
    steps = []
    source_paths: set[Path] = set()

    def run(label: str, command: list[str], timeout: int = 60) -> dict:
        try:
            process = subprocess.run(command, cwd=repo, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, text=True, timeout=timeout)
            text = process.stdout
            code = process.returncode
        except subprocess.TimeoutExpired as error:
            text = (error.stdout or b"").decode() if isinstance(error.stdout, bytes) else error.stdout or ""
            code = None
        for raw in re.findall(r"\[parsing started (?:DirectoryFileObject|SimpleFileObject)\[([^\]]+)\]", text):
            path = Path(raw)
            if not path.is_file() and ":" in raw:
                base, relative = raw.split(":", 1)
                path = Path(base) / relative
            if path.is_file() and path.is_relative_to(repo):
                source_paths.add(path)
        # Omit verbose class-loading noise; retain parsed sources, diagnostics, and test outcomes.
        retained = "\n".join(line for line in text.splitlines() if not line.startswith(
            ("[loading ", "[checking ", "[wrote ", "[search path for ", "[total ", "Round ", "Processor ")))
        log = output / f"{label}.log"
        log.write_text(retained + "\n")
        record = {"step": label, "command": command, "exit_code": code,
                  "status": "PASSED" if code == 0 else "FAILED" if code is not None else "TIMEOUT",
                  "deadline_seconds": timeout, "log": log.name, "log_sha256": digest(log)}
        steps.append(record)
        return {**record, "text": text}

    with tempfile.TemporaryDirectory(prefix="bff-entity-fields-") as directory:
        temporary = Path(directory)
        classes = temporary / "classes"
        classes.mkdir()
        launcher = temporary / "BffEntityFieldLauncher.java"
        launcher.write_text(RUNNER)
        compiler = [str(javac), "--release", "17", "-verbose", "-implicit:class",
                    "-cp", classpath, "-processorpath", str(jars[0]),
                    "-sourcepath", str(main_source) + os.pathsep + str(test_source), "-d", str(classes)]
        mapper_sources = [main_source / "com/scb/sso/singleuibff" / relative for relative in [
            "dto/config/EntitlementSource.java", "dto/ems2/v2/Action.java",
            "dto/ems2/v2/Entity.java", "dto/ems2/v2/Ems2Result.java",
            "dto/ems2/v2/Subject.java", "service/v2/filter/ems3/dto/Ems3DataEntitlementDto.java",
            "service/v2/authorization/AuthorizationResultMapper.java",
        ]]
        # Lombok does not transform implicitly discovered dependencies. Compile the
        # complete mapper production closure explicitly before compiling its test.
        production_compile = run("mapper-production-compile", compiler + [str(path) for path in mapper_sources])
        mapper_file = test_source / Path((prefix + test_names[0]).replace(".", "/") + ".java")
        test_compiler = [str(javac), "--release", "17", "-verbose", "-proc:none",
                         "-cp", str(classes) + os.pathsep + classpath,
                         "-sourcepath", str(test_source), "-d", str(classes)]
        compile_result = run("mapper-test-compile", test_compiler + [str(mapper_file), str(launcher)]) if production_compile["exit_code"] == 0 else production_compile
        cases = []
        counts = None
        if compile_result["exit_code"] == 0:
            execution = run("mapper-tests", [str(java), "-cp", str(classes) + os.pathsep + classpath,
                                             "BffEntityFieldLauncher", prefix + test_names[0]])
            for line in execution["text"].splitlines():
                if line.startswith("CASE\t"):
                    _, status, class_name, method_name, display = line.split("\t", 4)
                    cases.append({"class": class_name, "method": method_name,
                                  "display": display, "status": status})
                elif line.startswith("COUNTS\t"):
                    values = list(map(int, line.split("\t")[1:]))
                    counts = dict(zip(["found", "started", "passed", "failed", "skipped", "aborted", "failed_containers"], values))
        service_files = [test_source / Path((prefix + name).replace(".", "/") + ".java") for name in test_names[1:]]
        service_compile = ({"status": "BLOCKED", "exit_code": None}
                           if args.mapper_only else run("service-compile", compiler + [str(path) for path in service_files]))
        service_execution = None
        if service_compile["exit_code"] == 0:
            service_execution = run("service-tests", [str(java), "-cp", str(classes) + os.pathsep + classpath,
                                                      "BffEntityFieldLauncher", *[prefix + name for name in test_names[1:]]])

    result = {
        "started_at": started, "finished_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip(),
        "java_home": str(args.java_home), "java_version": subprocess.check_output([str(java), "-version"], stderr=subprocess.STDOUT, text=True).strip(),
        "requested_test_classes": [prefix + name for name in test_names],
        "mapper": {"counts": counts, "cases": cases},
        "service": {"compilation": service_compile["status"], "execution": "NOT_RUN" if service_execution is None else service_execution["status"]},
        "steps": steps,
        "sources": [{"path": str(path.relative_to(repo)), "sha256": digest(path)} for path in sorted(source_paths)],
        "cached_dependencies": [{"path": str(path), "sha256": digest(path)} for path in jars],
        "limits": [
            "Offline isolated checks use unchanged actual source files and real cached dependencies. No application or starter classes are fabricated.",
            "Dependency versions are explicit. Spring isolation uses 6.1.13, the Boot 3.3.4 baseline, rather than all explicit BFF overrides.",
            "The custom JUnit launcher is a test runner only. It does not replace application source.",
            "These checks do not replace the owning Maven build, complete applicable suite, or live integration evidence.",
        ],
    }
    result["status"] = "PASSED_WITH_LIMITS" if counts and counts["passed"] == counts["found"] and not any(counts[k] for k in ["failed", "skipped", "aborted", "failed_containers"]) else "FAILED"
    if service_compile["exit_code"] != 0:
        result["limits"].append("Service test compilation is blocked by the retained compiler diagnostics. No service test was executed.")
    (output / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "mapper_counts": counts, "service": result["service"], "output": str(output)}))
    return 0 if result["status"] == "PASSED_WITH_LIMITS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
