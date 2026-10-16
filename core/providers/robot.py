"""Run registered Robot suites and retain native execution evidence."""

from __future__ import annotations

import os
import hashlib
from pathlib import Path, PureWindowsPath
import re
import signal
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

from ..models import Context, Operation, Resource
from .common import BuiltinProvider, ProviderError, configured_path, object_schema, string_schema, timeout


class RobotTestingProvider(BuiltinProvider):
    id = "testing.robot"
    resource_kind = "testing"
    operations = {
        "list": Operation("list", "List registered Robot suites.", object_schema()),
        "run": Operation("run", "Execute a registered Robot suite and retain its results.", object_schema({
            "suite": string_schema(maximum=256), "dry_run": {"type": "boolean", "default": False}},
            ("suite",)), mutating=True),
    }

    def _configuration(self, resource: Resource, context: Context) -> tuple[Path, str, dict[str, Path], list[Path]]:
        if set(resource.config) - {"path", "python", "suites", "variable_files"}:
            raise ProviderError("INVALID_CONFIGURATION", "The Robot resource contains an unsupported setting.")
        root = configured_path(resource, context)
        if not root.is_dir():
            raise ProviderError("RESOURCE_UNAVAILABLE", "The Robot repository directory is unavailable.")
        python = resource.config.get("python")
        if not isinstance(python, str) or not 1 <= len(python) <= 4096 or "\x00" in python:
            raise ProviderError("INVALID_CONFIGURATION", "Configure the Robot Python executable path.")
        if python != "{python}" and not Path(python).is_absolute():
            if PureWindowsPath(python).drive or "\\" in python or ".." in Path(python).parts:
                raise ProviderError("INVALID_CONFIGURATION", "Use an absolute or repository-relative Python executable path.")
        suites = resource.config.get("suites")
        if not isinstance(suites, dict) or not 1 <= len(suites) <= 256:
            raise ProviderError("INVALID_CONFIGURATION", "Configure named Robot suite paths.")
        selected = {}
        for name, relative in suites.items():
            if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,255}", name):
                raise ProviderError("INVALID_CONFIGURATION", "A registered Robot suite name is invalid.")
            if (not isinstance(relative, str) or not 1 <= len(relative) <= 4096 or "\x00" in relative
                    or "\\" in relative or Path(relative).is_absolute() or PureWindowsPath(relative).drive
                    or ".." in Path(relative).parts):
                raise ProviderError("INVALID_CONFIGURATION", "Robot suite paths must stay inside the repository.")
            path = (root / relative).resolve()
            if not path.is_relative_to(root):
                raise ProviderError("INVALID_CONFIGURATION", "A Robot suite path leaves the repository.")
            if not path.is_dir() and not (path.is_file() and path.suffix.lower() in {".robot", ".rbt"}):
                raise ProviderError("RESOURCE_UNAVAILABLE", "A registered Robot suite file or directory is unavailable.")
            if path.is_dir() and any(not child.resolve().is_relative_to(root) for child in path.rglob("*")
                                     if child.is_symlink()):
                raise ProviderError("INVALID_CONFIGURATION", "A Robot suite directory contains an escaping symbolic link.")
            selected[name] = path
        declarations = resource.config.get("variable_files", [])
        if not isinstance(declarations, list) or len(declarations) > 32:
            raise ProviderError("INVALID_CONFIGURATION", "Robot variable_files must be a list of at most 32 YAML paths.")
        variable_files = []
        for value in declarations:
            if not isinstance(value, str) or not 1 <= len(value) <= 4096 or "\x00" in value:
                raise ProviderError("INVALID_CONFIGURATION", "A Robot variable file path is invalid.")
            path = Path(value)
            if not path.is_absolute():
                if PureWindowsPath(value).drive or "\\" in value or ".." in path.parts:
                    raise ProviderError("INVALID_CONFIGURATION", "Use absolute or repository-relative Robot variable file paths.")
                path = root / path
            if path.suffix.lower() not in {".yaml", ".yml"} or path.is_symlink() or not path.is_file():
                raise ProviderError("INVALID_CONFIGURATION", "Robot variable files must be regular YAML files.")
            path = path.resolve()
            if path in variable_files:
                raise ProviderError("INVALID_CONFIGURATION", "Robot variable file paths must be unique.")
            variable_files.append(path)
        return root, python, selected, variable_files

    @staticmethod
    def _taskkill_path() -> str:
        """Use the Windows system directory instead of searching PATH."""
        import ctypes
        import ntpath

        directory = ctypes.create_unicode_buffer(32768)
        length = ctypes.windll.kernel32.GetSystemDirectoryW(directory, len(directory))
        if not 0 < length < len(directory) or not ntpath.isabs(directory.value):
            raise OSError("The Windows system directory is unavailable.")
        return ntpath.join(directory.value, "taskkill.exe")

    @classmethod
    def _terminate(cls, process, *, windows: bool) -> str | None:
        if windows:
            try:
                cleanup = subprocess.run([cls._taskkill_path(), "/PID", str(process.pid), "/T", "/F"],
                                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                         stderr=subprocess.DEVNULL, timeout=5, shell=False)
                if cleanup.returncode == 0:
                    return None
            except (OSError, AttributeError, subprocess.TimeoutExpired):
                pass
            limitation = "Windows child process termination was not confirmed."
        else:
            try:
                os.killpg(process.pid, signal.SIGKILL)
                return None
            except ProcessLookupError:
                return None
            except OSError:
                limitation = "Child process group termination was not confirmed."
        try:
            process.kill()
        except OSError:
            pass
        return limitation

    @staticmethod
    def _source(root: Path) -> dict:
        source = {"revision": None, "dirty": None}
        marker = root / ".git"
        if not (marker.is_file() or marker.is_dir()):
            return source
        environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        environment.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0")
        base = ["git", "--no-optional-locks", "-c", "core.fsmonitor=false", "-C", str(root)]
        try:
            with tempfile.TemporaryFile() as output:
                revision = subprocess.run(base + ["rev-parse", "--verify", "HEAD"], stdin=subprocess.DEVNULL,
                                          stdout=output, stderr=subprocess.DEVNULL, env=environment, timeout=5)
                output.seek(0)
                value = output.read(66).decode("ascii", errors="replace").strip()
            if revision.returncode == 0 and re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", value):
                source["revision"] = value
            with tempfile.TemporaryFile() as output:
                status = subprocess.run(base + ["status", "--porcelain=v1", "--untracked-files=normal"],
                                        stdin=subprocess.DEVNULL, stdout=output, stderr=subprocess.DEVNULL,
                                        env=environment, timeout=5)
                output.seek(0)
                if status.returncode == 0:
                    source["dirty"] = bool(output.read(1))
        except (OSError, subprocess.TimeoutExpired):
            pass
        return source

    @staticmethod
    def _suite_sources(root: Path, selected: Path) -> list[dict]:
        paths = sorted(selected.rglob("*")) if selected.is_dir() else [selected]
        sources = []
        for path in paths:
            if not path.is_file() or path.suffix.lower() not in {".robot", ".resource", ".rbt"}:
                continue
            if not path.resolve().is_relative_to(root):
                raise ProviderError("INVALID_CONFIGURATION", "A Robot source path leaves the repository.")
            digest, size = hashlib.sha256(), 0
            with path.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    digest.update(chunk)
                    size += len(chunk)
            sources.append({"path": path.relative_to(root).as_posix(), "sha256": digest.hexdigest(), "size_bytes": size})
        return sources

    @staticmethod
    def _results(path: Path) -> dict:
        if not path.is_file() or path.is_symlink():
            raise ProviderError("MISSING_ROBOT_OUTPUT", "Robot did not produce a regular output.xml file.")
        if path.stat().st_size > 64 * 1024 * 1024:
            raise ProviderError("INVALID_ROBOT_OUTPUT", "Robot output.xml exceeds the 64 MiB limit.")
        try:
            robot = ET.parse(path).getroot()
        except (ET.ParseError, OSError, ValueError):
            raise ProviderError("INVALID_ROBOT_OUTPUT", "Robot output.xml is malformed.") from None
        if robot.tag != "robot" or not robot.findall("suite"):
            raise ProviderError("INVALID_ROBOT_OUTPUT", "Robot output.xml has no Robot suite results.")
        tests = []
        counters = {"PASS": 0, "FAIL": 0, "SKIP": 0, "total": 0}
        suite_failed = False

        def visit(suite, parents):
            nonlocal suite_failed
            names = [*parents, suite.get("name", "")]
            suite_status = suite.find("status")
            if suite_status is None or suite_status.get("status") not in {"PASS", "FAIL", "SKIP"}:
                raise ProviderError("INVALID_ROBOT_OUTPUT", "A Robot suite result has no supported status.")
            suite_failed = suite_failed or suite_status.get("status") == "FAIL"
            for test in suite.findall("test"):
                status = test.find("status")
                if status is None or status.get("status") not in {"PASS", "FAIL", "SKIP"}:
                    raise ProviderError("INVALID_ROBOT_OUTPUT", "A Robot test result has no supported status.")
                value = status.get("status")
                tests.append({"id": test.get("id"), "name": test.get("name", ""),
                              "suite": ".".join(names), "status": value})
                counters[value] += 1
                counters["total"] += 1
            for child in suite.findall("suite"):
                visit(child, names)

        for suite in robot.findall("suite"):
            visit(suite, [])
        if not tests:
            raise ProviderError("INVALID_ROBOT_OUTPUT", "Robot output.xml contains no test results.")
        return {"tests": tests, "counts": counters, "suite_failed": suite_failed}

    def _invoke(self, operation: str, resource: Resource, arguments: dict, context: Context) -> dict:
        root, python, suites, variable_files = self._configuration(resource, context)
        if operation == "list":
            return {"status": "SUCCEEDED", "suites": sorted(suites)}
        suite = arguments["suite"]
        if suite not in suites:
            raise ProviderError("UNKNOWN_SUITE", "The Robot resource does not register this suite.")
        dry_run = arguments.get("dry_run", False)
        if type(dry_run) is not bool:
            raise ProviderError("INVALID_ARGUMENT", "dry_run must be a boolean.")
        interpreter = Path(sys.executable) if python == "{python}" else Path(python)
        if not interpreter.is_absolute():
            interpreter = root / interpreter
        if not interpreter.is_file():
            raise ProviderError("RESOURCE_UNAVAILABLE", "The configured Robot Python executable is unavailable.")
        seconds = timeout(context)
        directory = context.run_dir / "robot"
        directory.mkdir(parents=True, exist_ok=True)
        stdout_path, stderr_path = context.run_dir / "stdout.txt", context.run_dir / "stderr.txt"
        command = [str(interpreter), "-m", "robot", "--outputdir", str(directory)]
        if dry_run:
            command.append("--dryrun")
        for path in variable_files:
            command.extend(["--variablefile", str(path)])
        command.append(str(suites[suite]))
        result = {"status": "FAILED", "suite": suite, "suite_path": str(suites[suite]),
                  "environment": resource.environment, "dry_run": dry_run,
                  "execution_mode": "dry-run" if dry_run else "execution", "behavior_verified": False,
                  "source": self._source(root), "suite_sources": self._suite_sources(root, suites[suite]),
                  "command": command, "cwd": str(root),
                  "timeout_seconds": seconds, "stdout_path": str(stdout_path), "stderr_path": str(stderr_path),
                  "output_path": str(directory / "output.xml"), "log_path": str(directory / "log.html"),
                  "report_path": str(directory / "report.html"),
                  "limitations": ["Execution results do not establish approved business behavior.",
                                  "Source identity describes the files before execution.",
                                  "Suite imports and private inputs outside the selected sources are not captured."]}
        if dry_run:
            result["limitations"].append("Dry run checks suite structure and keyword resolution without executing test assertions.")
        if result["source"]["revision"] is None or result["source"]["dirty"] is None:
            result["limitations"].append("The repository revision or working tree state is unknown.")
        if result["source"]["dirty"]:
            result["limitations"].append("HEAD does not identify uncommitted working tree bytes.")
        if variable_files:
            result["limitations"].append("Private variable file contents are not captured.")
        environment = {key: value for key, value in os.environ.items() if key not in {"ROBOT_OPTIONS", "REBOT_OPTIONS"}}
        timed_out = False
        cleanup_limit = None
        with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
            process = subprocess.Popen(command, cwd=root, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
                                       env=environment, shell=False, start_new_session=os.name == "posix")
            try:
                process.wait(timeout=seconds)
            except subprocess.TimeoutExpired:
                timed_out = True
                cleanup_limit = self._terminate(process, windows=os.name == "nt")
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    cleanup_limit = "The Robot process did not confirm termination within five seconds."
        result.update(exit_code=process.returncode, stdout_bytes=stdout_path.stat().st_size,
                      stderr_bytes=stderr_path.stat().st_size)
        try:
            parsed = self._results(directory / "output.xml")
            result.update(parsed)
            if parsed["counts"]["SKIP"]:
                result["limitations"].append("Skipped tests supply no assertion execution evidence.")
            if process.returncode == 0 and not parsed["counts"]["FAIL"] and not parsed["suite_failed"]:
                result["status"] = "SUCCEEDED"
        except ProviderError as error:
            result.update(code=error.code, message=error.message)
        if timed_out:
            result["status"] = "TIMEOUT"
        if cleanup_limit:
            result["cleanup_status"] = "UNKNOWN"
            result["limitations"].append(cleanup_limit)
        return result
