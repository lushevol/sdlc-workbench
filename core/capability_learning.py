"""An evidence-bound revision journal for scoped Workbench capabilities."""

from __future__ import annotations

from datetime import datetime, timezone
from functools import lru_cache
from hashlib import sha256
from importlib.resources import files
import json
import os
from pathlib import Path
import re

from jsonschema import Draft202012Validator
import yaml

from .assurance import _json, _read, local_path
from .context.catalogs import UniqueKeyLoader
from .hook_install import _atomic
from .models import WorkbenchError
from .workspace import load_workspace


_CAPTURE = ".workbench/learning"
_JOURNAL = "registry/capability-history"
_ADO = "ado-deploy-artifact"
_CES = "ces-entitlement-migration"
_DIGEST = re.compile(r"[0-9a-f]{64}")
_SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
_SENSITIVE = re.compile(
    r"(?ix) (?:\b(?:authorization\s*:|bearer\s+\S|basic\s+[A-Za-z0-9+/=]{8,}|"
    r"cookie\s*[:=]|set-cookie\s*:|"
    r"(?:password|passwd|client[-_ ]?secret|api[-_ ]?key|access[-_ ]?token|"
    r"refresh[-_ ]?token|personal[-_ ]?access[-_ ]?token|pat|secret|token)\s*[:=])|"
    r"-----BEGIN [^-]+PRIVATE KEY-----|https?://\S+@|https?://\S+\?|"
    r"\b(?:gh[pousr]_|github_pat_|sk-(?:proj-)?|AKIA)[A-Za-z0-9_-]{12,}|"
    r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b|"
    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b)"
)


def _now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def _digest(data):
    return sha256(data).hexdigest()


@lru_cache
def _validator(name):
    schema = json.loads(files("ai_sdlc_workbench").joinpath("schemas", f"learning-{name}.schema.json").read_text())
    return Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)


def _validate(name, record):
    if not _validator(name).is_valid(record):
        raise WorkbenchError(f"The record failed the learning {name} schema.")


def _safe_metadata(value, credentials=()):
    if isinstance(value, dict):
        for key, item in value.items():
            _safe_metadata(key, credentials)
            _safe_metadata(item, credentials)
    elif isinstance(value, list):
        for item in value:
            _safe_metadata(item, credentials)
    elif isinstance(value, str) and (_SENSITIVE.search(value) or any(
            credential == value or (len(credential) >= 8 and credential in value) for credential in credentials)):
        raise WorkbenchError("Sensitive-looking metadata was rejected. Submit a minimized evidence reference.")


def _credentials(root):
    from .doctor import _environment

    values, _ = _environment(root)
    return tuple(value for name, value in values.items() if value and
                 re.search(r"password|passwd|credential|secret|token|cookie|api_?key|private_?key|(?:^|_)pat$", name, re.I))


def _identifier(value, pattern, label):
    if not isinstance(value, str) or len(value) > 64 or not pattern.fullmatch(value):
        raise WorkbenchError(f"Supply a valid {label} identifier.")
    return value


def _read_json(path):
    try:
        return _json(_read(path))
    except (OSError, ValueError, UnicodeError, RecursionError):
        raise WorkbenchError("Read a regular file containing strict JSON.") from None


def _evidence(root, item):
    path = local_path(root, item["path"])
    if any(part in {".git", ".ssh", ".sdlc", ".venv", "node_modules", "workspace.local.yaml"}
           or part.startswith(".env") for part in Path(item["path"]).parts):
        raise WorkbenchError("Private configuration, checkout metadata and raw run stores cannot be learning evidence.")
    raw = _read(path)
    if _digest(raw) != item["sha256"]:
        raise WorkbenchError("Discovery evidence changed. Recheck the source and submit its current hash.")
    return raw


def _matches(rule_scope, selection):
    return rule_scope.items() <= selection.items()


def _overlaps(left, right):
    return all(right[key] == left[key] for key in left.keys() & right.keys())


def _tokens(*values):
    return set(re.findall(r"[a-z0-9]+", " ".join(values).casefold()))


def _protected(discovery, capability_id):
    return (discovery["category"] == "business-rule" or capability_id == _CES
            or discovery["scope"].get("system", "").casefold() == "ces")


def _command_switch(name):
    return os.environ.get(name, "1").casefold() not in {"0", "false", "off"}


class CapabilityRegistry:
    def __init__(self, root, *, configuration=None):
        self.root = Path(root).resolve()
        if configuration is None:
            configuration, _ = load_workspace(self.root)
        self.catalogs = configuration["_catalogs"]
        self.base = {item["id"]: item for item in self.catalogs.get("capabilities", [])}

    def _path(self, relative):
        return local_path(self.root, relative)

    def _write_lock(self):
        from .hooks import _file_lock

        return _file_lock(self._path(f"{_CAPTURE}/write.lock"))

    def history(self, capability_id):
        _identifier(capability_id, _SLUG, "capability")
        directory = self._path(f"{_JOURNAL}/{capability_id}")
        history = []
        previous = None
        for path in sorted(directory.glob("*.json")):
            path = self._path(path.relative_to(self.root).as_posix())
            event = _read_json(path)
            if event.get("schema_version") != 1:
                raise WorkbenchError("The capability history has an unsupported event version.")
            capability = event.get("capability")
            _validate("capability", capability)
            _safe_metadata(event)
            checksum = _digest(_bytes(event))
            number = len(history) + 1
            if (capability["id"] != capability_id or capability["revision"] != number
                    or capability.get("previous") != previous
                    or path.name != f"{number:010d}-{checksum}.json"):
                raise WorkbenchError("The capability history has a broken revision chain.")
            history.append({"sha256": checksum, **event})
            previous = checksum
        return history

    def _latest(self, capability_id):
        history = self.history(capability_id)
        return history[-1] if history else None

    def _learned(self):
        directory = self._path(_JOURNAL)
        if not directory.exists():
            return {}
        if not directory.is_dir():
            raise WorkbenchError("The capability history location must be a directory.")
        return {path.name: self._latest(path.name) for path in sorted(directory.iterdir())
                if path.is_dir() and len(path.name) <= 64 and _SLUG.fullmatch(path.name)}

    def available(self, query="", scope=None):
        learned = self._learned()
        results = []
        terms = _tokens(query)
        for capability_id in sorted(self.base.keys() | learned.keys()):
            entry = learned.get(capability_id)
            if entry is None and capability_id not in self.base:
                continue
            item = entry["capability"] if entry else self.base[capability_id]
            if scope is not None and entry and not (
                _matches(item["scope"], scope) and any(_matches(rule["scope"], scope) for rule in item["rules"])
            ):
                continue
            fields = (capability_id, item.get("name", ""), item.get("description", ""), *item.get("skills", []))
            if terms and not terms & _tokens(*fields):
                continue
            result = {"id": capability_id, "name": item.get("name", capability_id),
                      "status": item["status"] if entry else "DECLARED",
                      "revision": item["revision"] if entry else None,
                      "category": item.get("category"), "skills": item.get("skills", [])}
            if location := self.base.get(capability_id, {}).get("location"):
                result["location"] = location
            results.append(result)
        return results

    def use(self, capability_id, scope, revision=None):
        _validate_scope(scope)
        history = self.history(capability_id)
        if revision is not None:
            history = [event for event in history if event["capability"]["revision"] == revision]
        if not history or history[-1]["capability"]["status"] != "ACTIVE":
            if not history and revision is None and capability_id in self.base:
                return {**self.base[capability_id], "status": "DECLARED", "rules": []}
            return {"id": capability_id, "status": "UNAVAILABLE", "rules": []}
        current = history[-1]["capability"]
        if not _matches(current["scope"], scope):
            return {"id": capability_id, "status": "OUT_OF_SCOPE", "rules": []}
        candidates = [rule for rule in current["rules"] if _matches(rule["scope"], scope)]
        selected = []
        for rule in candidates:
            if any(other["key"] == rule["key"] and rule["scope"].items() < other["scope"].items()
                   for other in candidates):
                continue
            if any(other["key"] == rule["key"] and other["value"] != rule["value"] for other in selected):
                raise WorkbenchError("Applicable rules conflict. Review the capability history.")
            selected.append(rule)
        return {**current, "status": "ACTIVE" if selected else "OUT_OF_SCOPE", "rules": selected}

    def _candidate(self, discovery_id):
        _identifier(discovery_id, _DIGEST, "discovery")
        discovery = _read_json(self._path(f"{_CAPTURE}/discoveries/{discovery_id}.json"))
        _validate("discovery", discovery)
        _safe_metadata(discovery, _credentials(self.root))
        if discovery.get("id") != discovery_id or discovery_id != self._discovery_id(discovery):
            raise WorkbenchError("The discovery contents do not match their identity.")
        return discovery

    def _discovery_id(self, record):
        identity = {key: record.get(key) for key in ("category", "scope", "rule", "skill_id")}
        identity["capability_id"] = self._target(record)
        if record.get("operation") in {"CORRECT", "REPLACE", "DEPRECATE", "NO_CHANGE"}:
            identity["operation"] = record["operation"]
        identity["evidence"] = sorted({item["sha256"] for item in record["evidence"]})
        return _digest(_bytes(identity))

    def pending(self, conflicts=False):
        directory = self._path(f"{_CAPTURE}/discoveries")
        result = []
        for path in sorted(directory.glob("*.json")):
            discovery = self._candidate(path.stem)
            change = self.reconcile(discovery)
            if (conflicts and change["status"] == "CONFLICT") or (
                    not conflicts and change["status"] != "NO_CHANGE"):
                result.append({"discovery": discovery, "change": change})
        return result

    def _target(self, discovery):
        system = discovery["scope"].get("system", "").casefold()
        if system == "ces":
            return _CES
        if system == "ado" and discovery["rule"]["key"] == "artifact-name":
            return _ADO
        if discovery.get("capability_id"):
            return discovery["capability_id"]
        raise WorkbenchError("Select a stable capability identity after inspecting related capabilities.")

    def reconcile(self, discovery):
        identifier = self._target(discovery)
        history = self.history(identifier)
        latest = history[-1] if history else None
        current = latest["capability"] if latest else None
        related = {result["id"] for result in self.available(identifier + " " + discovery["title"])}
        related.update(discovery.get("related_capabilities", []))
        related.discard(identifier)
        requested = discovery.get("operation")
        rule = discovery["rule"]
        scope = discovery["scope"]
        if any(event.get("discovery", {}).get("id") == discovery["id"] for event in history):
            operation, status, reason = "NO_CHANGE", "NO_CHANGE", "This discovery already has a promotion record."
        elif not current:
            if requested == "NO_CHANGE":
                operation, status, reason = "NO_CHANGE", "NO_CHANGE", "The checkpoint recorded no change."
            elif requested and requested != ("EXTEND" if identifier in self.base else "CREATE"):
                operation, status, reason = requested, "CONFLICT", "This operation requires an active learned revision."
            else:
                operation = "EXTEND" if identifier in self.base else "CREATE"
                status, reason = "PROPOSED", "Record this distinct scoped claim."
        elif requested == "NO_CHANGE":
            operation, status, reason = "NO_CHANGE", "NO_CHANGE", "The checkpoint recorded no change."
        else:
            operation, status, reason = "EXTEND", "PROPOSED", "Add a scoped claim to the existing capability."
            for existing in current["rules"]:
                old_scope = existing["scope"]
                if (existing["key"] != rule["key"] or not _overlaps(scope, old_scope)
                        or old_scope.items() < scope.items() or scope.items() < old_scope.items()):
                    continue
                if existing["value"] != rule["value"]:
                    operation, status, reason = "CORRECT", "CONFLICT", "Overlapping scopes disagree."
                    break
                if scope == old_scope:
                    operation, status, reason = "NO_CHANGE", "NO_CHANGE", "This claim already has an active rule."
            if requested in {"REPLACE", "DEPRECATE"}:
                operation, status, reason = requested, "PROPOSED", "A workspace authority must review this operation."
            if current["status"] == "DEPRECATED" and requested != "REPLACE":
                operation, status, reason = "REPLACE", "CONFLICT", "This capability is deprecated."
            if current["category"] != discovery["category"]:
                operation, status, reason = "REPLACE", "CONFLICT", "The category differs from the active capability."
        if operation == "CREATE" and status == "PROPOSED":
            for candidate in related:
                if not _SLUG.fullmatch(candidate) or len(candidate) > 64:
                    continue
                version = self._latest(candidate)
                if not version or version["capability"]["status"] != "ACTIVE":
                    continue
                existing = version["capability"]
                if existing["category"] == discovery["category"] and any(
                        old["key"] == rule["key"] and _overlaps(scope, old["scope"]) for old in existing["rules"]):
                    status, reason = "CONFLICT", "An existing related capability owns an overlapping rule."
                    break
        change = {"capability_id": identifier, "operation": operation, "discovery_id": discovery["id"],
                  "discovery_sha256": _digest(_bytes(discovery)),
                  "baseline": latest["sha256"] if latest else None, "status": status, "reason": reason,
                  "related_capabilities": sorted(related)[:32]}
        change["id"] = _digest(_bytes(change))
        _validate("change", change)
        return change

    def _references(self, discovery):
        missing = set(discovery.get("related_contracts", [])) - {
            contract["id"] for contract in self.catalogs.get("contracts", [])}
        if missing:
            raise WorkbenchError("The discovery references a contract outside the catalog.")
        if "task" in discovery and not self._path(discovery["task"]).is_file():
            raise WorkbenchError("The discovery task record is unavailable.")
        if "skill_id" not in discovery:
            return None
        skill = discovery["skill_id"]
        path = self._path(f".agents/skills/{skill}/SKILL.md")
        try:
            document = _read(path).decode()
            parts = document.split("\n---", 1)
            if not document.startswith("---\n") or len(parts) != 2 or not parts[1][3:].strip():
                raise ValueError
            metadata = yaml.load(parts[0][4:], Loader=UniqueKeyLoader)
        except (OSError, ValueError, UnicodeError, yaml.YAMLError):
            raise WorkbenchError("The linked skill needs valid Agent Skills frontmatter.") from None
        if (not isinstance(metadata, dict) or metadata.get("name") != skill
                or not isinstance(metadata.get("description"), str)
                or not 1 <= len(metadata["description"].strip()) <= 1024
                or {"allowed-tools", "hooks", "agent", "context"} & metadata.keys()):
            raise WorkbenchError("The linked skill has invalid identity, description or executable privileges.")
        return _digest(document.encode())

    def checkpoint(self, input_path):
        """Accept an agent's explicit semantic extraction at a meaningful task boundary."""
        if not _command_switch("WORKBENCH_LEARNING_CAPTURE"):
            return {"status": "CAPTURE_DISABLED"}
        return self._record(_read_json(self._path(input_path)))

    def ado_checkpoint(self, paths, task=None):
        """Extract one scoped naming observation from typed resolver evidence."""
        if not _command_switch("WORKBENCH_LEARNING_CAPTURE"):
            return {"status": "CAPTURE_DISABLED"}
        if not 1 <= len(paths) <= 16:
            raise WorkbenchError("Supply one to sixteen artifact observation paths.")
        evidence = []
        first = None
        for path in paths:
            selected = self._path(path)
            if selected.suffix != ".json":
                raise WorkbenchError("Select an artifact observation JSON file.")
            raw = _read(selected)
            if first is None:
                try:
                    first = _json(raw)
                except (ValueError, UnicodeError, RecursionError):
                    raise WorkbenchError("The artifact observation needs strict JSON.") from None
            evidence.append({"path": path, "sha256": _digest(raw), "locator": "/"})
        record = {
            "category": "contract", "title": "Azure DevOps artifact name",
            "summary": "Record a published artifact name for the checked ADO scope.",
            "scope": first.get("scope"), "evidence": evidence,
            "observed_facts": ["The artifact metadata identifies a published name."],
            "verification_status": "OBSERVED",
            "verification_method": "Compare exact projected build and artifact observations.",
            "skill_id": _ADO, "capability_id": _ADO,
            "rule": {"key": "artifact-name", "value": first.get("artifact_name")},
        }
        if task:
            record["task"] = task
        return self._record(record)

    def _record(self, discovery):
        _validate("discovery", discovery)
        _safe_metadata(discovery, _credentials(self.root))
        if {"id", "discovered_at"} & discovery.keys():
            raise WorkbenchError("Discovery identity and time are assigned at capture.")
        self._target(discovery)
        for evidence in discovery["evidence"]:
            _evidence(self.root, evidence)
        discovery["id"] = self._discovery_id(discovery)
        discovery["discovered_at"] = _now()
        with self._write_lock():
            path = self._path(f'{_CAPTURE}/discoveries/{discovery["id"]}.json')
            if path.exists():
                discovery = self._candidate(discovery["id"])
            else:
                _atomic(path, _bytes(discovery))
            change = self.reconcile(discovery)
            assessment = self._assessment(discovery, change)
            decision = {"change": change, "validation": _public_assessment(assessment)}
            decision_id = _digest(_bytes(decision))
            decision_path = self._path(f"{_CAPTURE}/decisions/{decision_id}.json")
            if not decision_path.exists():
                _atomic(decision_path, _bytes({"recorded_at": _now(), **decision}))
            if assessment["status"] == "AUTO_ELIGIBLE" and _command_switch("WORKBENCH_LEARNING_PROMOTION"):
                event = self._promote(discovery, change, assessment)
                return {"status": "PROMOTED", "discovery": discovery, "change": change,
                        "revision": event["capability"]["revision"]}
        return {"status": assessment["status"], "discovery": discovery, "change": change,
                "validation": _public_assessment(assessment)}

    def _assessment(self, discovery, change):
        try:
            skill_digest = self._references(discovery)
            payloads = [_evidence(self.root, item) for item in discovery["evidence"]]
        except (WorkbenchError, OSError):
            return {"status": "INVALID_EVIDENCE", "reason": "Check evidence hashes, task and catalog references."}
        if change["status"] == "NO_CHANGE":
            return {"status": "NO_CHANGE", "reason": change["reason"]}
        if _protected(discovery, change["capability_id"]):
            return {"status": "GOVERNANCE_REQUIRED", "reason": "Use the canonical knowledge governance workflow."}
        details = {"skill_sha256": skill_digest} if skill_digest else {}
        rule = discovery["rule"]
        if change["capability_id"] == _ADO:
            if not (discovery["category"] == "contract" and rule["key"] == "artifact-name"
                    and discovery.get("skill_id") == _ADO):
                return {"status": "INVALID_EVIDENCE", "reason": "Use the typed ADO artifact rule for this capability."}
            if change["operation"] == "DEPRECATE":
                return {"status": "REVIEW_REQUIRED", "reason": "Record a workspace authority's review of deprecation."}
            try:
                observations = [_json(payload) for payload in payloads]
                from .capability_ado import verify_artifact_rule

                if verify_artifact_rule(discovery["scope"], rule["key"], rule["value"], observations, root=self.root):
                    _safe_metadata(observations, _credentials(self.root))
                    details["proofs"] = observations
                    if change["status"] == "CONFLICT":
                        return {"status": "CONFLICT", "reason": change["reason"], **details}
                    if change["operation"] in {"CREATE", "EXTEND"}:
                        return {"status": "AUTO_ELIGIBLE", "reason": "Independent ADO observations agree.",
                                **details}
                    return {"status": "REVIEW_REQUIRED", "reason": "This operation needs explicit review.",
                            **details}
            except (WorkbenchError, OSError, ValueError, UnicodeError, RecursionError):
                pass
            if change["status"] == "CONFLICT":
                return {"status": "CONFLICT", "reason": change["reason"]}
            return {"status": "INVALID_EVIDENCE", "reason": "ADO observations did not independently verify the rule."}
        if change["status"] == "CONFLICT":
            return {"status": "CONFLICT", "reason": change["reason"]}
        return {"status": "REVIEW_REQUIRED", "reason": "Record a workspace authority's independent check and approval.",
                **details}

    def validate(self, discovery_id):
        discovery = self._candidate(discovery_id)
        change = self.reconcile(discovery)
        return {"change": change, **_public_assessment(self._assessment(discovery, change))}

    def _approval(self, path, change, discovery, assessment):
        approval = _read_json(self._path(path))
        required = {"change_id", "authority", "verification", "evidence"}
        if "skill_sha256" in assessment:
            required.add("skill_sha256")
        if (set(approval) != required or approval["change_id"] != change["id"]
                or approval.get("skill_sha256") != assessment.get("skill_sha256")):
            raise WorkbenchError("Approval must bind to the current proposed change digest.")
        _safe_metadata(approval, _credentials(self.root))
        if any(not isinstance(approval[key], str) or not 1 <= len(approval[key].strip()) <= 300
               or not approval[key].isprintable() for key in ("authority", "verification")):
            raise WorkbenchError("Record the authority and independent verification method.")
        validator = _validator("discovery")
        if not validator.evolve(schema={"$defs": validator.schema["$defs"],
                                        "$ref": "#/$defs/evidence"}).is_valid(approval["evidence"]):
            raise WorkbenchError("The approval needs a valid verification evidence reference.")
        if approval["evidence"]["sha256"] in {item["sha256"] for item in discovery["evidence"]}:
            raise WorkbenchError("Use a separate record for the independent verification and approval.")
        _evidence(self.root, approval["evidence"])
        return approval

    def promote(self, discovery_id, approval_path=None):
        with self._write_lock():
            discovery = self._candidate(discovery_id)
            change = self.reconcile(discovery)
            assessment = self._assessment(discovery, change)
            status = assessment["status"]
            if status == "NO_CHANGE":
                return {"status": status, "change": change}
            if status == "AUTO_ELIGIBLE":
                if not _command_switch("WORKBENCH_LEARNING_PROMOTION") and not approval_path:
                    raise WorkbenchError("Automatic promotion is disabled. Supply recorded approval for manual promotion.")
                if approval_path:
                    assessment["approval"] = self._approval(approval_path, change, discovery, assessment)
            elif status in {"REVIEW_REQUIRED", "CONFLICT"} and approval_path:
                if change["operation"] not in {"CREATE", "EXTEND", "CORRECT", "REPLACE", "DEPRECATE"}:
                    raise WorkbenchError("The conflicted operation cannot be promoted.")
                if status == "CONFLICT" and change["reason"] != "Overlapping scopes disagree.":
                    raise WorkbenchError("Resolve the capability identity or operation before promotion.")
                if change["capability_id"] == _ADO and status == "CONFLICT" and not assessment.get("proofs"):
                    raise WorkbenchError("Check two independent ADO observations before correcting the contract.")
                assessment["approval"] = self._approval(approval_path, change, discovery, assessment)
            else:
                raise WorkbenchError(assessment["reason"])
            return self._promote(discovery, change, assessment)

    def _promote(self, discovery, change, assessment):
        identifier = change["capability_id"]
        previous = self._latest(identifier)
        current = previous["capability"] if previous else None
        baseline = previous["sha256"] if previous else None
        if change["baseline"] != baseline:
            raise WorkbenchError("The registry changed. Reconcile again with the current revision.")
        operation = change["operation"]
        if operation in {"CORRECT", "REPLACE", "DEPRECATE"} and not current:
            raise WorkbenchError("The proposed operation needs an active learned revision.")
        scope = discovery["scope"]
        rule = {**discovery["rule"], "scope": scope, "evidence": discovery["evidence"],
                "discovery_id": discovery["id"]}
        rules = list(current["rules"]) if current else []
        if operation == "CORRECT":
            if not any(old["key"] == rule["key"] and old["scope"] == scope for old in rules):
                raise WorkbenchError("An overlapping scope requires a reconciled replacement.")
            rules = [old for old in rules if old["key"] != rule["key"] or old["scope"] != scope]
        if operation == "REPLACE":
            rules = []
        if operation != "DEPRECATE":
            rules.append(rule)
        for old in rules:
            if (old is not rule and old["key"] == rule["key"] and old["value"] != rule["value"]
                    and _overlaps(old["scope"], scope) and not (
                        old["scope"].items() < scope.items() or scope.items() < old["scope"].items())):
                raise WorkbenchError("The proposed revision still contains conflicting scopes.")
        base = self.base.get(identifier, {})
        skills = [*current["skills"]] if current else []
        if discovery.get("skill_id") and discovery["skill_id"] not in skills:
            skills.append(discovery["skill_id"])
        contracts = set(current["contracts"]) if current else set()
        contracts.update(discovery.get("related_contracts", []))
        shared_scope = {key: value for key, value in scope.items() if
                        all(old["scope"].get(key) == value for old in rules)}
        if operation == "DEPRECATE":
            shared_scope = current["scope"]
        capability = {
            "id": identifier, "name": base.get("name", current["name"] if current else discovery["title"]),
            "description": current["description"] if current else discovery["summary"],
            "category": discovery["category"], "owner": scope.get("system", "workbench"),
            "risk": "read-only", "status": "DEPRECATED" if operation == "DEPRECATE" else "ACTIVE",
            "scope": shared_scope, "rules": rules, "skills": skills, "contracts": sorted(contracts),
            "dependencies": [], "preconditions": [], "permissions": [],
            "triggers": ["Read-only artifact resolution"] if identifier == _ADO else [],
            "change_id": change["id"],
        }
        if identifier == _ADO:
            capability["permissions"] = ["Existing ADO read grants"]
            capability["preconditions"] = ["Exact build, source branch and source commit"]
        return self._append(capability, previous, discovery=discovery, change=change, validation=assessment)

    def _append(self, capability, previous, **details):
        capability["revision"] = previous["capability"]["revision"] + 1 if previous else 1
        if previous:
            capability["previous"] = previous["sha256"]
        _validate("capability", capability)
        event = {"schema_version": 1, "recorded_at": _now(), "capability": capability, **details}
        _safe_metadata(event, _credentials(self.root))
        raw = _bytes(event)
        number = capability["revision"]
        path = self._path(f'{_JOURNAL}/{capability["id"]}/{number:010d}-{_digest(raw)}.json')
        _atomic(path, raw)
        return {"sha256": _digest(raw), **event}

    def rollback(self, capability_id, revision):
        with self._write_lock():
            history = self.history(capability_id)
            if not 1 <= revision <= len(history):
                raise WorkbenchError("Select a recorded revision to restore.")
            current, target = history[-1], history[revision - 1]
            if current is target:
                return current
            comparable = {"revision", "previous", "change_id", "rollback_of"}
            restored = {key: value for key, value in target["capability"].items() if key not in comparable}
            if restored == {key: value for key, value in current["capability"].items() if key not in comparable}:
                return current
            restored["rollback_of"] = target["sha256"]
            return self._append(restored, current, validation={"status": "RESTORED", "target": target["sha256"]})


def _public_assessment(assessment):
    return {key: value for key, value in assessment.items() if key != "proofs"}


def _validate_scope(scope):
    validator = _validator("discovery")
    if not validator.evolve(schema={"$defs": validator.schema["$defs"], "$ref": "#/$defs/scope"}).is_valid(scope):
        raise WorkbenchError("Select a valid applicability scope.")
    _safe_metadata(scope)
