#!/usr/bin/env python3
"""Machine-readable, direct-REST Rundeck commands for an AI agent."""
import argparse
import getpass
import json
import os
import re
import sys
from pathlib import Path

from client import RundeckClient, RundeckError, AuthenticationError
from policy import Policy, PolicyError
from sanitize import scrub, scrub_text

ROOT = Path(__file__).resolve().parents[3]


def load_dotenv(path):
    """Minimal parser for non-secret simple KEY=VALUE lines; env vars take priority."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if re.fullmatch(r"[A-Z][A-Z0-9_]*", key) and key != "RUNDECK_PASSWORD":
            os.environ.setdefault(key, value)


def parser():
    p = argparse.ArgumentParser(description="Rundeck 5.10 REST-only AI connector")
    p.add_argument("--policy", help="Alternative policy.json location")
    subs = p.add_subparsers(dest="command", required=True)
    subs.add_parser("health", help="Show server and API version")
    projects = subs.add_parser("projects", help="List visible projects")
    projects.add_argument("--limit", type=int, default=30)
    jobs = subs.add_parser("jobs", help="List/inspect job metadata or definitions")
    js = jobs.add_subparsers(dest="operation", required=True)
    jl = js.add_parser("list")
    jl.add_argument("--project", required=True)
    jl.add_argument("--limit", type=int, default=30)
    show = js.add_parser("show")
    show.add_argument("--id", required=True)
    definition = js.add_parser("definition")
    definition.add_argument("--id", required=True)
    run = js.add_parser("run")
    run.add_argument("--id", required=True)
    run.add_argument("--option", action="append", default=[], metavar="KEY=VALUE")
    ex = subs.add_parser("executions", help="Find executions and logs")
    xs = ex.add_subparsers(dest="operation", required=True)
    xl = xs.add_parser("list")
    xl.add_argument("--project", required=True)
    xl.add_argument("--status", choices=["running", "succeeded", "failed", "aborted"])
    xl.add_argument("--recent", help="Examples: 24h, 7d, 2w")
    xl.add_argument("--limit", type=int, default=20)
    for op in ("show", "logs"):
        xp = xs.add_parser(op)
        xp.add_argument("--id", required=True)
        if op == "logs":
            xp.add_argument("--lines", type=int, default=100)
    return p


def bounded(value, maximum):
    if not 1 <= value <= maximum:
        raise ValueError(f"Count must be between 1 and {maximum}")
    return value


def emit(value):
    print(json.dumps(scrub(value), indent=2, ensure_ascii=False))


def job_summary(job):
    return {k: job.get(k) for k in
            ("id", "name", "group", "project", "description", "href", "permalink",
             "scheduled", "scheduleEnabled", "enabled", "averageDuration") if k in job}


def execution_summary(ex):
    keys = ("id", "status", "project", "date-started", "date-ended",
            "href", "permalink", "description", "successfulNodes", "failedNodes")
    result = {k: ex[k] for k in keys if k in ex}
    job = ex.get("job")
    if isinstance(job, dict):
        result["job"] = {k: job[k] for k in ("id", "name", "group", "project") if k in job}
    return result


def filter_projects(items, policy, limit):
    return [p for p in items if not policy.config.get("allowed_projects")
            or p.get("name") in policy.config["allowed_projects"]][:limit]


def parse_job_options(raw):
    result = {}
    for entry in raw:
        if "=" not in entry:
            raise ValueError("Job options require KEY=VALUE")
        key, value = entry.split("=", 1)
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,63}", key):
            raise ValueError("Invalid option name")
        if key in result:
            raise ValueError("Duplicate job option")
        if re.search(r"(?i)(pass|token|secret|credential|api.?key)", key):
            raise ValueError("Secret-like option names are forbidden; use Rundeck secure options")
        if len(value) > 1000:
            raise ValueError("Option value is too long")
        result[key] = value
    return result


def require_human_approval(job_id, project, job_name, options):
    if not sys.stdin.isatty():
        raise PolicyError("Execution requires a human-controlled interactive terminal")
    print(f"\nACTION: Execute Rundeck job {job_id}", file=sys.stderr)
    print(f"Project: {project} | Job: {scrub_text(job_name, 100)}", file=sys.stderr)
    print("Options: " + (", ".join(sorted(options)) or "none") + " (values hidden)", file=sys.stderr)
    print("Review the exact option values outside the AI chat before approval.", file=sys.stderr)
    confirm = input(f"Type 'RUN {job_id}' to authorize this execution: ")
    if confirm != f"RUN {job_id}":
        raise PolicyError("Local human confirmation was not provided")


def run_command(args, client, policy):
    if args.command == "health":
        result = client.system_info()
        system = result.get("system", {}) if isinstance(result, dict) else {}
        emit({"rundeck": system.get("rundeck", {}), "api_version_requested": client.api_version})
    elif args.command == "projects":
        limit = bounded(args.limit, policy.max_items())
        result = client.projects()
        if not isinstance(result, list):
            raise RundeckError("Unexpected projects response")
        visible = filter_projects(result, policy, limit)
        emit({"projects": [{k: p[k] for k in ("name", "label", "description") if k in p} for p in visible],
              "returned": len(visible)})
    elif args.command == "jobs":
        if args.operation == "list":
            policy.check_project(args.project)
            limit = bounded(args.limit, policy.max_items())
            jobs = client.jobs(args.project)
            if not isinstance(jobs, list):
                raise RundeckError("Unexpected jobs response")
            emit({"project": args.project, "jobs": [job_summary(j) for j in jobs[:limit]],
                  "returned": min(len(jobs), limit)})
        elif args.operation in ("show", "definition"):
            client._job_id(args.id)
            if args.operation == "definition":
                policy.check_definition()
            meta = client.job_info(args.id)
            project = meta.get("project")
            policy.check_project(project)
            emit(job_summary(meta) if args.operation == "show" else client.job_definition(args.id))
        elif args.operation == "run":
            client._job_id(args.id)
            options = parse_job_options(args.option)
            # Deny before even sending a read request when execution is globally off.
            if policy.config.get("enable_job_execution") is not True:
                raise PolicyError("Job execution is disabled in policy.json")
            # No execution without job metadata, local allowlist and direct confirmation.
            meta = client.job_info(args.id)
            project = meta.get("project")
            policy.check_execution(project, args.id, options)
            require_human_approval(args.id, project, meta.get("name", ""), options)
            output = client.run_job(args.id, options)
            # Only return execution metadata, never submitted option values.
            emit({"submitted": True, "job_id": args.id, "project": project,
                  "execution": execution_summary(output) if isinstance(output, dict) else {}})
    elif args.command == "executions":
        if args.operation == "list":
            policy.check_project(args.project)
            limit = bounded(args.limit, policy.max_items())
            result = client.executions(args.project, args.status, args.recent, limit)
            if not isinstance(result, dict):
                raise RundeckError("Unexpected executions response")
            emit({"project": args.project, "executions": [execution_summary(ex)
                  for ex in result.get("executions", [])[:limit]],
                  "paging": result.get("paging")})
        elif args.operation in ("show", "logs"):
            client._execution_id(args.id)
            # Determine project from execution before retrieving sensitive details.
            meta = client.execution(args.id)
            policy.check_project(meta.get("project"))
            if args.operation == "show":
                emit(execution_summary(meta))
            else:
                lines = bounded(args.lines, policy.max_log_lines())
                result = client.logs(args.id, lines)
                if not isinstance(result, dict):
                    raise RundeckError("Unexpected output response")
                emit({"execution_id": args.id, "project": meta.get("project"),
                      "offset": result.get("offset"), "dataoffset": result.get("dataoffset"),
                      "completed": result.get("completed"), "hasFailed": result.get("hasFailed"),
                      "entries": result.get("entries", [])[:lines]})


def main(argv=None):
    load_dotenv(ROOT / ".env")
    args = parser().parse_args(argv)
    try:
        policy = Policy.load(args.policy)
        url = os.environ.get("RUNDECK_URL", "")
        user = os.environ.get("RUNDECK_USER", "")
        client = RundeckClient(url, user, os.environ.get("RUNDECK_API_VERSION", "46"),
                               os.environ.get("RUNDECK_TIMEOUT_SECONDS", "20"),
                               policy.max_response_bytes())
        # Password never appears on CLI arguments or in a config file. A parent process
        # may inject RUNDECK_PASSWORD via an approved secrets provider.
        password = os.environ.get("RUNDECK_PASSWORD")
        if not password:
            if not sys.stdin.isatty():
                raise AuthenticationError("No interactive terminal: supply password from an approved runtime secrets provider")
            password = getpass.getpass("Rundeck password: ")
        client.login(password)
        del password
        run_command(args, client, policy)
        return 0
    except (ValueError, PolicyError, AuthenticationError, RundeckError) as exc:
        # Avoid echoing exception bodies that could contain credentials.
        print(json.dumps({"ok": False, "error": scrub_text(str(exc), 180)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
