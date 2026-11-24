"""Resolve exact ADO build artifacts and retain only typed learning evidence."""

from __future__ import annotations

import hashlib
import json
import os
import re
from urllib.parse import urlsplit

from .assurance import _read, local_path
from .doctor import _environment
from .hook_install import _atomic
from .models import Context, WorkbenchError
from .providers.connectors import ConnectorMcpProvider


_READS = ("report_builds", "report_build_artifacts")
_RECEIPTS = ".workbench/learning/ado-observations"
_SCOPE = {"system", "instance", "project", "repository", "pipeline", "branch"}
_SECRET_KEY = re.compile(r"password|passwd|pass_code|secret|token|cookie|auth|api_?key|private_?key|(?:^|_)pat$", re.I)
_SECRET_VALUE = re.compile(r"^(?:gh[pousr]_|github_pat_|glpat-|xox[baprs]-|sk[-_]|AKIA|ASIA|eyJ\w*\.)", re.I)


def _capture_enabled():
    return os.environ.get("WORKBENCH_LEARNING_CAPTURE", "1").casefold() not in {"0", "false", "off"}


def _matches(value, pattern):
    return isinstance(value, str) and re.fullmatch(pattern, value) is not None


def _build_id(value):
    return type(value) is int and 0 < value <= 2147483647


def _artifact_name(value):
    return _matches(value, r"[A-Za-z0-9][A-Za-z0-9._-]{0,47}") and not _SECRET_VALUE.search(value)


def _branch(value):
    return (_matches(value, r"refs/(?:heads|tags)/[A-Za-z0-9][A-Za-z0-9._/-]{0,159}")
            and all(part not in {"", ".", ".."} for part in value.split("/")))


def _endpoint(value):
    try:
        parts = urlsplit(value)
        if (parts.scheme == "https" and parts.hostname and parts.username is None
                and parts.password is None and not parts.query and not parts.fragment):
            port = "" if parts.port in {None, 443} else f":{parts.port}"
            return f"https://{parts.hostname.lower()}{port}{parts.path.rstrip('/')}"
    except (TypeError, ValueError):
        pass
    raise WorkbenchError("Configure a credential-free HTTPS Azure DevOps organization URL.")


def _contains_secret(value, environment):
    return any(secret and _SECRET_KEY.search(name) and
               (secret == value or (len(secret) >= 8 and secret in value))
               for name, secret in environment.items())


def artifact_scope(workbench, *, resource_id, project, pipeline_id, repository_id, source_ref):
    """Identify an exact selector scope without reading the remote service."""
    scope, _, _ = _selector_context(workbench, resource_id, project, pipeline_id, repository_id, source_ref)
    return scope


def _selector_context(workbench, resource_id, project, pipeline_id, repository_id, source_ref):
    resource = workbench.resources.get(resource_id)
    if (resource is None or resource.provider != "connector.mcp"
            or resource.config.get("connector") != "ado" or "call" not in resource.allowed_operations):
        raise WorkbenchError("Select a registered Azure DevOps connector with call access.")
    grants = resource.config.get("allowed_tools", [])
    if not isinstance(grants, list) or any(tool not in grants for tool in _READS):
        raise WorkbenchError("Both exact artifact read tools must be granted in the selected connector.")
    if (not _matches(project, r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}")
            or not _matches(repository_id, r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}")
            or not _build_id(pipeline_id) or not _branch(source_ref)):
        raise WorkbenchError("Supply a project ID, repository ID, positive pipeline ID, and full Git branch or tag ref.")
    environment, status = _environment(workbench.root)
    if status["status"] != "READY":
        raise WorkbenchError("Read the selected workspace's connector configuration.")
    if any(_contains_secret(value, environment) for value in (project, repository_id, source_ref)):
        raise WorkbenchError("Artifact selectors contain a credential.")
    endpoint = _endpoint(environment.get("AZURE_DEVOPS_ORG_URL", ""))
    instance = "ado-" + hashlib.sha256(endpoint.encode()).hexdigest()
    scope = {"system": "ado", "instance": instance, "project": project.lower(),
             "repository": repository_id.lower(), "pipeline": str(pipeline_id), "branch": source_ref}
    return scope, endpoint, environment


def _read_result(provider, resource, context, tool, arguments):
    # Connector results can include signed artifact URLs. Project them in memory
    # so the ordinary action recorder never receives the raw payload.
    result = provider.invoke("call", resource, {"tool": tool, "arguments": arguments}, context)
    if result.get("status") != "SUCCEEDED":
        raise WorkbenchError(f"The granted Azure DevOps read failed ({tool}).")
    payload = _object(result.get("result")).get("structuredContent", {})
    data = payload.get("data") if isinstance(payload, dict) else None
    values = data.get("value") if isinstance(data, dict) else data
    if (not isinstance(values, list) or not all(isinstance(value, dict) for value in values)
            or (isinstance(data, dict) and data.get("count") is not None and data["count"] != len(values))):
        raise WorkbenchError("Azure DevOps did not return a complete metadata collection.")
    headers = _object(payload.get("headers"))
    if headers.get("x-ms-continuationtoken") or headers.get("x-ms-continuation-token"):
        raise WorkbenchError("Azure DevOps returned an incomplete metadata page.")
    return values


def _receipt(root, observation):
    raw = (json.dumps(observation, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    relative = f"{_RECEIPTS}/{digest}.json"
    return local_path(root, relative), raw, {"path": relative, "sha256": digest, "locator": "/"}


def resolve_artifact(workbench, *, resource_id, project, pipeline_id, build_id, repository_id,
                     source_ref, source_commit, artifact_name=None, expected_scope=None, require_unique=False):
    """Check exact build metadata and resolve one published artifact by name."""
    scope, endpoint, environment = _selector_context(workbench, resource_id, project, pipeline_id,
                                                       repository_id, source_ref)
    if expected_scope is not None and scope != expected_scope:
        raise WorkbenchError("The configured artifact scope changed during resolution. Recheck the selected connector.")
    if (not _build_id(build_id) or not _matches(source_commit, r"[0-9a-fA-F]{40}")
            or _contains_secret(source_commit, environment)):
        raise WorkbenchError("Supply an exact completed build ID and commit SHA.")
    source_commit = source_commit.lower()
    if artifact_name is not None and (not _artifact_name(artifact_name)
                                      or _contains_secret(artifact_name, environment)):
        raise WorkbenchError("Supply a bounded artifact name without sensitive data.")
    resource = workbench.resources[resource_id]
    context = Context(workbench.root, workbench.root, workbench.config.get("timeout_seconds", 30))
    provider = ConnectorMcpProvider()
    builds = _read_result(provider, resource, context, _READS[0], {"project": project, "ids": [build_id]})
    if len(builds) != 1:
        raise WorkbenchError("Azure DevOps did not return exactly one selected build.")
    build = builds[0]
    project_data = _object(build.get("project"))
    repository_data = _object(build.get("repository"))
    expected = ("completed", "succeeded", source_ref, source_commit, pipeline_id,
                scope["repository"], scope["project"], build_id)
    actual = (str(build.get("status", "")).lower(), str(build.get("result", "")).lower(),
              build.get("sourceBranch"), str(build.get("sourceVersion", "")).lower(),
              _object(build.get("definition")).get("id"),
              str(repository_data.get("id", "")).lower(), str(project_data.get("id", "")).lower(), build.get("id"))
    build_url = build.get("url")
    if (actual != expected or not _build_id(actual[4]) or not _build_id(actual[7])
            or not isinstance(build_url, str) or not build_url.startswith(endpoint + "/")):
        raise WorkbenchError("The returned build differs from the requested organization, project, pipeline, repository, ref, commit, or success status.")
    artifacts = _read_result(provider, resource, context, _READS[1], {"project": project, "buildId": build_id})
    base = {"scope": scope, "build_id": build_id, "source_commit": source_commit,
            "integrity": "METADATA_ONLY"}
    if artifact_name is None or (require_unique and (
            len(artifacts) != 1 or artifacts[0].get("name") != artifact_name)):
        names = sorted({name for artifact in artifacts if _artifact_name(name := artifact.get("name"))
                        and not _contains_secret(name, environment)})
        return {"status": "SELECTION_REQUIRED", **base, "available_names": names}
    matches = [artifact for artifact in artifacts if artifact.get("name") == artifact_name]
    if len(matches) != 1 or not _build_id(matches[0].get("id")):
        raise WorkbenchError("Azure DevOps did not return one exact artifact identity for the selected build and name.")
    resolution = {"status": "RESOLVED", **base, "artifact_name": artifact_name, "artifact_id": matches[0]["id"]}
    if _capture_enabled():
        observation = {"schema_version": 1, "source": "ado-connector", "artifact_count": len(artifacts),
                       **{key: resolution[key] for key in ("scope", "build_id", "source_commit",
                                                            "artifact_name", "artifact_id")}}
        try:
            path, raw, reference = _receipt(workbench.root, observation)
            if not path.exists():
                _atomic(path, raw)
            if _read(path) != raw:
                raise WorkbenchError("The artifact observation differs from its content address.")
            resolution["evidence"] = reference
        except (OSError, WorkbenchError):
            resolution["learning_capture"] = "FAILED"
    return resolution


def _object(value):
    return value if isinstance(value, dict) else {}


def verify_artifact_rule(scope, key, value, observations, *, root=None):
    """Verify a name against separate commits and builds under one exact scope."""
    if (key != "artifact-name" or not _artifact_name(value) or not isinstance(scope, dict)
            or set(scope) != _SCOPE or not isinstance(observations, list)
            or scope["system"] != "ado" or not _branch(scope["branch"])
            or not _matches(scope["project"], r"[a-z0-9][a-z0-9._-]{0,79}")
            or not _matches(scope["repository"], r"[a-z0-9][a-z0-9._-]{0,79}")
            or not _matches(scope["pipeline"], r"[1-9][0-9]{0,9}")):
        return False
    fixture = scope["instance"] == "fixture"
    if not fixture and (root is None or not _matches(scope["instance"], r"ado-[0-9a-f]{64}")):
        return False
    source = "fixture" if fixture else "ado-connector"
    builds, commits = set(), set()
    for observation in observations:
        if (not isinstance(observation, dict) or set(observation) !=
                {"schema_version", "source", "scope", "build_id", "source_commit", "artifact_name",
                 "artifact_id", "artifact_count"}
                or type(observation["schema_version"]) is not int or observation["schema_version"] != 1
                or observation["source"] != source or observation["scope"] != scope
                or type(observation["artifact_count"]) is not int or observation["artifact_count"] != 1
                or observation["artifact_name"] != value or not _build_id(observation["build_id"])
                or not _build_id(observation["artifact_id"])
                or not _matches(observation["source_commit"], r"[0-9a-f]{40}")):
            return False
        if not fixture:
            try:
                path, raw, _ = _receipt(root, observation)
                if _read(path) != raw:
                    return False
            except (OSError, WorkbenchError):
                return False
        builds.add(observation["build_id"])
        commits.add(observation["source_commit"])
    return len(builds) >= 2 and len(commits) >= 2
