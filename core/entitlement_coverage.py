"""Run scoped EMS2-to-CES reconciliation from project-owned configuration.

This optional helper supports the inspected collection and matrix contracts only.
It does not infer data-policy equivalence or a complete EMS2 account directory.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import threading
from urllib.parse import quote
import webbrowser

from .entitlement_reconciliation import (
    ReconciliationError, compare_sets, normalize_ces_catalog,
    normalize_ces_user, normalize_ems2_permissions,
)
from .entitlement_sources import (
    JsonHttpClient, SourceError, _redacted_url, load_root_env, read_http_example, read_matrix,
)


def _now():
    return datetime.now(timezone.utc).isoformat()


def _hash(value):
    data = value if isinstance(value, bytes) else json.dumps(value, sort_keys=True).encode()
    return hashlib.sha256(data).hexdigest()


def _write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def _clean(value):
    if isinstance(value, dict):
        return {k: ("[REDACTED]" if k.lower() in {
            "authorization", "password", "access_token", "refresh_token", "secret"
        } else _clean(v)) for k, v in value.items()}
    if isinstance(value, list):
        return [_clean(v) for v in value]
    return value


def _bounded_error(error):
    return {"code": getattr(error, "code", type(error).__name__),
            "http_status": getattr(error, "status", None)}


def _platform_only_roles(catalogs, excluded_features):
    result = set()
    for app, catalog in catalogs.items():
        for role in catalog["entitlements"]:
            grants = [g for g in catalog["grants"] if g[:2] == [app, role]]
            if grants and all((g[0], g[2]) in excluded_features for g in grants):
                result.add((app, role))
    return result


class Collector:
    def __init__(self, config, config_dir, run_dir, mode, env):
        self.config, self.config_dir, self.run_dir, self.mode = config, config_dir, run_dir, mode
        self.client = (JsonHttpClient(env, timeout=config.get("timeout_seconds", 15),
                                     retries=config.get("retries", 1),
                                     allow_http=config.get("allow_local_http", False))
                       if mode == "live" else None)
        self.examples = {}
        self.example_items = []
        self.env = env
        self.cache = {}
        self.lock = threading.Lock()
        if mode == "replay":
            for pattern in config.get("replay", {}).get("examples", []):
                for path in sorted(config_dir.glob(pattern)):
                    item = read_http_example(path)
                    if not isinstance(item.get("response_status"), int) or not 200 <= item["response_status"] < 300:
                        continue
                    if item.get("example_request_url") and item["example_request_url"] != item["url"]:
                        continue
                    key = self._key(item["method"], item["url"], item["body"])
                    self.examples[key] = (item["response"], str(path), _hash(path.read_bytes()))
                    self.example_items.append(item)

    @staticmethod
    def _key(method, url, body):
        return _hash([method, url, body])

    def get(self, service, path, body=None):
        settings = self.config[service]
        url = settings["base_url"].rstrip("/") + "/" + path.lstrip("/")
        method = "POST" if body is not None else "GET"
        key = self._key(method, url, body)
        capture = self.run_dir / "responses" / (key + ".json")
        with self.lock:
            if key in self.cache:
                return self.cache[key]
        if capture.exists():
            stored = json.loads(capture.read_text())
            if stored["request_key"] != key:
                raise ValueError("Capture request identity mismatch")
            response = stored["data"]
            if stored.get("data_sha256") != _hash(response):
                raise ValueError("Capture content hash mismatch")
        elif self.mode == "replay":
            # A recorded multi-entity POST can answer a strict subset of those entities.
            # Preserve the recorded count check before selecting the requested scope.
            if key not in self.examples and service == "ems2" and isinstance(body, dict):
                for item in self.example_items:
                    if item["method"] != method or item["url"] != url or not isinstance(item["body"], dict): continue
                    if set(item["body"]) != set(body): continue
                    if not all(set(body[u]).issubset(item["body"][u]) for u in body): continue
                    response = json.loads(json.dumps(item["response"]))
                    if not isinstance(response, dict): continue
                    for user, entities in body.items():
                        row = response.get(user, {})
                        if not isinstance(row.get("entitlements"), list) or row.get("count") != len(row["entitlements"]):
                            raise SourceError("INCOMPLETE_REPLAY_COLLECTION")
                        row["entitlements"] = [g for g in row["entitlements"] if g.get("subject", {}).get("entity", {}).get("name") in entities]
                        row["count"] = len(row["entitlements"])
                    self.examples[key] = (response, "scoped recorded POST", _hash(item["response"]))
                    break
            if key not in self.examples:
                raise SourceError("REPLAY_NOT_CAPTURED")
            response, source, source_hash = self.examples[key]
            if response is None:
                raise SourceError("REPLAY_RESPONSE_MISSING")
            _write(capture, {"request_key": key, "mode": self.mode, "source": source,
                             "source_sha256": source_hash, "at": _now(), "data": _clean(response),
                             "data_sha256": _hash(_clean(response))})
        else:
            token_env = settings.get("token_env")
            if settings.get("token_optional") and not self.env.get(token_env): token_env = None
            result = self.client.request(method, url, body=body,
                                         token_env=token_env,
                                         ca_env=settings.get("ca_env"))
            response = result["data"]
            _write(capture, {"request_key": key, "mode": self.mode,
                             "at": result["at"], "status": result["status"],
                             "url": result["url"], "sha256": result["sha256"],
                             "data": _clean(response), "data_sha256": _hash(_clean(response))})
        with self.lock:
            self.cache[key] = response
        return response


def _collection(body, key):
    if not isinstance(body, dict) or not isinstance(body.get(key), list):
        raise SourceError("INVALID_COLLECTION")
    if isinstance(body.get("count"), bool) or not isinstance(body.get("count"), int) or body["count"] != len(body[key]):
        raise SourceError("INCOMPLETE_COLLECTION")
    if any(not isinstance(x, dict) or not isinstance(x.get("name"), str) for x in body[key]):
        raise SourceError("INVALID_COLLECTION_ITEM")
    return [x["name"] for x in body[key]]


def _configuration(path):
    config = json.loads(path.read_text(encoding="utf-8"))
    if config.get("schema_version") != 1:
        raise ValueError("Unsupported configuration version")
    included = [e for e in config["entities"] if e.get("included", True)]
    if not included or len({e["name"] for e in included}) != len(included):
        raise ValueError("Entity scope must be nonempty and unique")
    forbidden = {"token", "password", "authorization", "headers", "secret"}
    def check(value):
        if isinstance(value, dict):
            if forbidden.intersection(k.lower() for k in value):
                raise ValueError("Use environment references for private credentials")
            for child in value.values(): check(child)
        elif isinstance(value, list):
            for child in value: check(child)
    check(config)
    return config, included


def _comparison_context(config, folder, included, matrices, *, family):
    """Retain only non-credential routing, mapping, and matrix provenance."""
    environments = (("ems2", "ces") if family == "EMS2_TO_CES" else ("prod", "uat"))
    allowed_routes = ("base_url", "entitlements_path", "subjects_path", "roles_path", "catalog_path", "user_path")
    sources = {}
    for label, key in zip(("baseline", "target"), environments):
        sources[label] = {"system": "CES" if key == "ces" else "EMS2"}
        sources[label].update({name: _redacted_url(value) for name in allowed_routes
                              if isinstance((value := config[key].get(name)), str)})
    entity_keys = ("name", "id", "app", "prod_id", "uat_id", "workbook")
    provenance = []
    for entity, matrix in zip(included, matrices):
        provenance.append({"entity": entity["name"], "path": str((folder / entity["workbook"]).resolve()),
                           "configured_path": entity["workbook"], "sha256": matrix.get("sha256"),
                           "app": matrix.get("app"), "itam_id": matrix.get("itam_id"),
                           **{label: len(matrix[key]) if key in matrix else None for label, key in
                              (("profile_count", "profiles"), ("grant_count", "grants"),
                               ("subject_count", "features"), ("account_count", "users"),
                               ("assignment_count", "assignments"))},
                           "sheets": {"profiles": "Entitlement", "grants": "EntitlementFeatureAction",
                                      "assignments": "UserEntitlement", "subjects": "Feature"}})
    return {"family": family, "sources": sources,
            "entities": [{**{key: entity[key] for key in entity_keys if key in entity}, "included": True}
                         for entity in included],
            "matrices": provenance,
            "mappings": {"entity_app": {entity["name"]: entity.get("app", entity["name"]) for entity in included},
                         **{kind: config.get(kind + "_mapping", {}) for kind in ("role", "subject", "action")}},
            "identity_rule": ("EMS2 role/entity/subject/action map to CES entitlement/app/feature/action."
                              if family == "EMS2_TO_CES" else
                              "Entity, role, subject, and action names define identity; numeric IDs locate requests.")}


def _baseline(config_dir, included):
    matrices = [read_matrix(config_dir / e["workbook"]) for e in included]
    grants, profiles, assignments, features, users = set(), set(), set(), set(), set()
    for entity, matrix in zip(included, matrices):
        if matrix["app"] != entity["app"]:
            raise ValueError("Matrix application differs from configured mapping")
        grants.update(map(tuple, matrix["grants"]))
        profiles.update(map(tuple, matrix["profiles"]))
        assignments.update(map(tuple, matrix["assignments"]))
        features.update((matrix["app"], f) for f in matrix["features"])
        users.update(matrix["users"])
    return {"matrices": matrices, "grants": sorted(grants), "profiles": sorted(profiles),
            "assignments": sorted(assignments), "features": sorted(features), "users": sorted(users)}


def _case(user, collector, config, included, baseline, catalogs):
    record = {"user_id": user, "at": _now(), "status": "UNASSESSED", "errors": []}
    entity_apps = {e["name"]: e["app"] for e in included}
    features = set(map(tuple, baseline["features"]))
    excluded = {(e["app"], e["feature"]) for e in config.get("excluded_features", [])}
    old = None
    try:
        raw = collector.get("ems2", config["ems2"]["entitlements_path"], {user: list(entity_apps)})
        old = normalize_ems2_permissions(raw, entity_apps,
                                        role_mapping=config.get("role_mapping"),
                                        subject_mapping=config.get("subject_mapping"),
                                        action_mapping=config.get("action_mapping"))["users"][user]
    except (SourceError, ReconciliationError, KeyError, ValueError) as error:
        record["errors"].append({"source": "ems2", **_bounded_error(error)})
    targets = []
    for app in sorted(set(entity_apps.values())):
        try:
            path = config["ces"]["user_path"].format(app=quote(app, safe=""), user=quote(user, safe=""))
            body = collector.get("ces", path)
            normalized = normalize_ces_user(body, app, expected_user=user)["users"]
            target = normalized.get(user, {"assignments": [], "effective_permissions": [],
                                            "data_scope": {}, "account_absent": True})
            targets.append(target)
        except (SourceError, ReconciliationError, KeyError, ValueError) as error:
            record["errors"].append({"source": "ces", "app": app, **_bounded_error(error)})
    if old is None or record["errors"]:
        return record
    scoped = sorted({tuple(g) for t in targets for g in t["effective_permissions"] if tuple(g[:2]) not in excluded})
    outside = sorted({tuple(g) for t in targets for g in t["effective_permissions"] if tuple(g[:2]) in excluded})
    expected_roles = {tuple(a) for a in old["assignments"]}
    matrix_roles = {tuple(a[1:]) for a in baseline["assignments"] if a[0] == user}
    actual_roles = {tuple(a) for t in targets for a in t["assignments"]}
    relevant_roles = actual_roles - _platform_only_roles(catalogs, excluded)
    effective = compare_sets(old["effective_permissions"], scoped)
    assignments = compare_sets(expected_roles, relevant_roles)
    catalog_grants = {tuple(g) for c in catalogs.values() for g in c["grants"]
                      if (g[0], g[1]) in actual_roles and tuple([g[0], g[2]]) not in excluded}
    provenance = compare_sets(old["grants"], catalog_grants)
    catalog_roles = {tuple(a[1:]) for c in catalogs.values() for a in c["assignments"]
                     if a[0] == user and tuple(a[1:]) in relevant_roles}
    membership = compare_sets(catalog_roles, relevant_roles)
    # Per-role reconstruction from catalog membership is declared separately from effective API assertions.
    complete = all(x["equal"] for x in (effective, assignments, provenance))
    record.update(status="MATCH" if complete else "DIFFERENT", effective=effective,
                  assignments=assignments, profile_grants=provenance,
                  matrix_assignment_comparison=compare_sets(matrix_roles, expected_roles),
                  catalog_membership={"status": "CONSISTENT" if membership["equal"] else "UNASSESSED",
                                      "comparison": membership,
                                      "limit": "Direct catalog versus effective role membership; inheritance semantics are unconfirmed."},
                  outside_scope_permissions=[list(x) for x in outside],
                  outside_baseline_roles=[list(x) for x in sorted(actual_roles - relevant_roles)],
                  baseline_has_permissions=bool(old["effective_permissions"]),
                  role_evidence="EMS2 permission rows; matrix assignments reported separately; CES catalog plus effective role names",
                  data_scope={"status": "UNASSESSED", "reason": "No complete comparable EMS2 field/value definition supplied",
                              "ces": [_clean(t.get("data_scope", {})) for t in targets]},
                  exact_full_profile_status="UNASSESSED")
    return record


def _render(result, path):
    """Write both human-readable formats through the shared report contract."""
    from .coverage_reporting import write_report
    write_report(result, path.parent)


def _finish(result, run_dir):
    users = result["users"]
    baseline_users = set(result["inventory"]["baseline_users"])
    baseline_users.update(x["user_id"] for x in users if x.get("baseline_has_permissions"))
    summary = {"discovered_accounts": len(result["inventory"]["users"]),
               "compared_accounts": sum(x["status"] != "UNASSESSED" for x in users),
               "matching_accounts": sum(x["status"] == "MATCH" for x in users),
               "different_accounts": sum(x["status"] == "DIFFERENT" for x in users),
               "unassessed_accounts": len(result["inventory"]["users"]) - sum(x["status"] != "UNASSESSED" for x in users)}
    summary["baseline_accounts"] = len(baseline_users)
    summary["matching_baseline_accounts"] = sum(x["status"] == "MATCH" and x["user_id"] in baseline_users for x in users)
    assessed_baseline = {x["user_id"] for x in users if x["status"] != "UNASSESSED"}
    baseline_complete = baseline_users.issubset(assessed_baseline)
    lower_bound = round(100 * summary["matching_baseline_accounts"] / len(baseline_users), 2) if baseline_users else None
    summary["functional_profile_coverage_percent"] = lower_bound if baseline_complete else None
    summary["verified_functional_match_lower_bound_percent"] = lower_bound
    summary["full_data_profile_coverage"] = "UNASSESSED"
    for label, key in (("subject_coverage", "subjects"), ("role_grant_preservation", "profile_grants")):
        comparison = result["entitlements"].get(key, {})
        summary[label] = f"{comparison.get('matched_count', 0)}/{comparison.get('baseline_count', 'unknown')}"
    result["summary"] = summary
    defs = result["entitlements"]
    inventories = defs.get("live_inventories", [])
    has_errors = bool(result.get("errors")) or summary["unassessed_accounts"] > 0 or any(x.get("status") == "UNASSESSED" for x in inventories) or bool(defs.get("matrix_limits")) or any(x.get("catalog_membership", {}).get("status") == "UNASSESSED" for x in users)
    has_differences = summary["different_accounts"] > 0 or any(x.get("missing_count", 0) or x.get("additional_count", 0) for x in defs.values() if isinstance(x, dict)) or any(not x.get("comparison", {}).get("equal", True) for x in inventories)
    result["status"] = "INCOMPLETE" if has_errors else "DIFFERENCES" if has_differences else "FUNCTIONAL_MATCH"
    result["conclusion"] = ("Collection is incomplete. Keep unavailable accounts in the denominator and resolve source access or missing captures."
                            if has_errors else "Review the reported differences before declaring equivalent permissions."
                            if has_differences else "All assessed functional comparisons match within the configured scope. Full data-profile equality is unassessed.")
    if result["mode"] == "replay":
        result["conclusion"] = ("Mock comparison uses supplied API responses only. " +
                                ("Missing captures remain unassessed; complete migration coverage cannot be calculated."
                                 if has_errors else "Review the reported differences before declaring equivalent captured permissions."
                                 if has_differences else "All captured functional comparisons match within the configured scope."))
    if any(e.get("code") in ("TLS_ERROR", "TLS_CONFIGURATION") for e in result.get("errors", [])):
        result["conclusion"] = "TLS validation blocked collection. Configure CES_COVERAGE_CA_FILE with the approved CA chain, then rerun."
    result["finished_at"] = _now()
    result["writing_review"] = {"standard": "ASD-STE100", "automated_check": "NOT_RUN", "asd_review": "PENDING",
                               "reviewer": None, "reviewed_at": None,
                               "limitations": ["Automated checks do not check the complete approved dictionary or grammar rules."]}
    _write(run_dir / "result.json", result)
    with (run_dir / "differences.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream); writer.writerow(["scope", "account", "comparison", "kind", "item"])
        for name, comparison in defs.items():
            if isinstance(comparison, dict):
                for kind in ("missing", "additional"):
                    for item in comparison.get(kind, []): writer.writerow(["entitlements", "", name, kind, json.dumps(item)])
        for user in users:
            for error in user.get("errors", []): writer.writerow(["user", user["user_id"], error["source"], "unassessed", error["code"]])
            for name in ("effective", "assignments", "profile_grants"):
                for kind in ("missing", "additional"):
                    for item in user.get(name, {}).get(kind, []): writer.writerow(["user", user["user_id"], name, kind, json.dumps(item)])
            for name, comparison in (("catalog_membership", user.get("catalog_membership", {}).get("comparison", {})),
                                     ("matrix_assignment_comparison", user.get("matrix_assignment_comparison", {}))):
                for kind in ("missing", "additional"):
                    for item in comparison.get(kind, []): writer.writerow(["source_consistency", user["user_id"], name, kind, json.dumps(item)])
        completed_ids = {u["user_id"] for u in users}
        for user_id in result["inventory"]["users"]:
            if user_id not in completed_ids: writer.writerow(["user", user_id, "collection", "unassessed", "NOT_FETCHED"])
        for error in result.get("errors", []): writer.writerow(["acquisition", "", "source", "unassessed", error["code"]])
        for inventory in defs.get("live_inventories", []):
            if inventory.get("status") == "UNASSESSED":
                writer.writerow(["inventory", inventory["entity"], inventory["kind"], "unassessed", inventory["error"]["code"]])
            for kind in ("missing", "additional"):
                for item in inventory.get("comparison", {}).get(kind, []): writer.writerow(["inventory", inventory["entity"], inventory["kind"], kind, json.dumps(item)])
    _render(result, run_dir / "report.html")
    return result


def run(config_path, *, mode="replay", output=None, resume=None, user_limit=None):
    if mode not in ("live", "replay"):
        raise ValueError("Unsupported coverage mode")
    config_path = Path(config_path).resolve(); config_dir = config_path.parent
    config, included = _configuration(config_path)
    baseline = _baseline(config_dir, included)
    binding = {"config_sha256": _hash(config_path.read_bytes()),
               "matrix_sha256": sorted(m["sha256"] for m in baseline["matrices"]), "mode": mode}
    binding["implementation_sha256"] = {p.name: _hash(p.read_bytes()) for p in (
        Path(__file__), Path(__file__).with_name("entitlement_sources.py"), Path(__file__).with_name("entitlement_reconciliation.py"),
        Path(__file__).with_name("coverage_reporting.py"))}
    if mode == "replay":
        binding["replay_sha256"] = {str(p.resolve()): _hash(p.read_bytes()) for pattern in config.get("replay", {}).get("examples", []) for p in sorted(config_dir.glob(pattern))}
    run_dir = Path(resume).resolve() if resume else Path(output).resolve() if output else \
        (config_dir / config["output_dir"] / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + mode)).resolve()
    if run_dir.exists() and not resume:
        raise ValueError("Output directory already exists; use --resume to continue it")
    run_dir.mkdir(parents=True, exist_ok=True)
    if resume:
        if json.loads((run_dir / "binding.json").read_text()) != binding:
            raise ValueError("Resume configuration or source hashes changed")
    else: _write(run_dir / "binding.json", binding)
    workspace = (config_dir / config["workspace_root"]).resolve()
    environment = load_root_env(workspace) if mode == "live" else {}
    for service in ("ems2", "ces"):
        ca_key = config[service].get("ca_env")
        if ca_key and environment.get(ca_key):
            ca_path = Path(environment[ca_key]).expanduser()
            environment[ca_key] = str(ca_path if ca_path.is_absolute() else workspace / ca_path)
    collector = Collector(config, config_dir, run_dir, mode, environment)
    result = {"schema_version": 1, "mode": mode, "started_at": _now(), "scope": config["scope"],
              "evidence_source": "MOCK: supplied API responses" if mode == "replay" else "LIVE: collected API responses",
              "binding": binding, "direction": {"baseline": "EMS2", "target": "CES"},
              "comparison_context": _comparison_context(config, config_dir, included, baseline["matrices"], family="EMS2_TO_CES"),
              "excluded": [e for e in config["entities"] if not e.get("included", True)],
              "excluded_features": config.get("excluded_features", []),
              "inventory": {"baseline_users": baseline["users"], "users": baseline["users"],
                            "source": "Matrix assignments plus CES catalog user_ids; no complete EMS2 directory endpoint supplied"},
              "entitlements": {}, "users": [], "errors": [],
              "limits": ["EMS2 production and CES UAT only; FMO exception is outside the production denominator.",
                         "Matrix definitions are supplied conversion inputs. Live inventories can expose incomplete matrix definitions.",
                         "Effective CES responses do not attribute each grant to a role. Catalog reconstruction is separate evidence.",
                         "Data-policy/profile field-value equivalence is unassessed without a complete EMS2 definition.",
                         "Replay uses stored responses and never establishes current live state.",
                         "Recorded capture times do not establish an atomic cross-system synchronization snapshot."]}
    catalogs = {}
    try:
        for app in sorted({e["app"] for e in included}):
            raw = collector.get("ces", config["ces"]["catalog_path"].format(app=quote(app, safe="")))
            catalogs[app] = normalize_ces_catalog(raw, app)
        all_users = set(baseline["users"]) | {u for c in catalogs.values() for u in c["users"]}
        result["inventory"].update(users=sorted(all_users), catalog_users=sorted({u for c in catalogs.values() for u in c["users"]}))
        excluded_features = {(e["app"], e["feature"]) for e in config.get("excluded_features", [])}
        live_grants = [g for c in catalogs.values() for g in c["grants"] if tuple([g[0], g[2]]) not in excluded_features]
        result["entitlements"]["profile_grants"] = compare_sets(baseline["grants"], live_grants)
        platform_roles = _platform_only_roles(catalogs, excluded_features)
        result["entitlements"]["profile_names"] = compare_sets(baseline["profiles"], [[app, name] for app, c in catalogs.items() for name in c["entitlements"] if (app, name) not in platform_roles or [app, name] in baseline["profiles"]])
        result["entitlements"]["subjects"] = compare_sets(baseline["features"], [[g[0], g[2]] for g in live_grants])
        result["entitlements"]["matrix_limits"] = [m["missing_profile_definitions"] for m in baseline["matrices"] if m["missing_profile_definitions"]]
        result["entitlements"]["live_inventories"] = []
        for entity in included:
            for kind in ("subjects", "roles"):
                try:
                    path = config["ems2"][kind + "_path"].format(entity_id=quote(entity["id"], safe=""))
                    names = _collection(collector.get("ems2", path), kind)
                    mapping = config.get("subject_mapping" if kind == "subjects" else "role_mapping", {}).get(entity["name"], {})
                    names = [mapping.get(n, n) for n in names]
                    expected = baseline["matrices"][included.index(entity)]["features" if kind == "subjects" else "profiles"]
                    expected_names = [p[1] for p in expected] if kind == "roles" else expected
                    comparison = compare_sets([[n] for n in names], [[n] for n in expected_names])
                    result["entitlements"]["live_inventories"].append({"entity": entity["name"], "kind": kind, "comparison": comparison})
                except (SourceError, ValueError) as error:
                    result["entitlements"]["live_inventories"].append({"entity": entity["name"], "kind": kind, "status": "UNASSESSED", "error": _bounded_error(error)})
        existing = {}
        checkpoint = run_dir / "cases.jsonl"
        if resume and checkpoint.exists():
            for line in checkpoint.read_text().splitlines():
                item = json.loads(line)
                digest = item.pop("record_sha256", None)
                if digest != _hash(item): raise ValueError("Account checkpoint hash mismatch")
                existing[item["user_id"]] = item
        result["users"] = list(existing.values())
        pending = [u for u in result["inventory"]["users"] if u not in existing or existing[u]["status"] == "UNASSESSED"]
        if user_limit is not None:
            pending = pending[:user_limit]
            result["limits"].append("Explicit account limit used. Remaining accounts stay unassessed in the full denominator.")
        # Probe one real account before scheduling the full population. Global access failures stop collection.
        stop = False
        with checkpoint.open("a", encoding="utf-8") as stream:
            def save(record):
                stored = {**record, "record_sha256": _hash(record)}
                stream.write(json.dumps(stored, ensure_ascii=False) + "\n"); stream.flush(); os.fsync(stream.fileno())
                existing[record["user_id"]] = record
                print(f"Saved account {len(existing)}/{len(result['inventory']['users'])}: {record['status']}", flush=True)
            for start in range(0, len(pending), max(1, int(config.get("workers", 4)))):
                group = pending[start:start + max(1, int(config.get("workers", 4)))]
                with ThreadPoolExecutor(max_workers=len(group)) as pool:
                    futures = [pool.submit(_case, user, collector, config, included, baseline, catalogs) for user in group]
                    for future in as_completed(futures):
                        record = future.result(); save(record)
                        if mode == "live" and record["errors"] and any(e.get("http_status") in (401, 403) or e["code"] in {"NETWORK_ERROR", "TLS_ERROR", "TLS_CONFIGURATION", "MISSING_CREDENTIAL"} for e in record["errors"]): stop = True
                if stop: break
        result["users"] = [existing[u] for u in sorted(existing)]
    except (SourceError, ReconciliationError, ValueError) as error:
        result["errors"].append(_bounded_error(error))
    _finish(result, run_dir)
    return result, run_dir


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--mode", choices=("live", "replay"), default="replay",
                        help="Use supplied response mocks by default; live collection requires an explicit selection")
    parser.add_argument("--output")
    parser.add_argument("--resume")
    parser.add_argument("--user-limit", type=int, help="Bound a diagnostic run; omitted accounts remain unassessed")
    parser.add_argument("--open", action="store_true", dest="open_report")
    args = parser.parse_args(argv)
    if args.user_limit is not None and args.user_limit < 1: parser.error("--user-limit must be positive")
    try:
        result, directory = run(args.config, mode=args.mode, output=args.output, resume=args.resume, user_limit=args.user_limit)
    except (ValueError, OSError, KeyError, SourceError) as error:
        print("Coverage setup failed: " + type(error).__name__ + ". Check configuration, input files, and environment.", file=sys.stderr)
        return 2
    print(json.dumps({"status": result["status"], "mode": result["mode"], "evidence_source": result["evidence_source"],
                      "summary": result["summary"], "report": str(directory / "report.html"),
                      "html_report": str(directory / "report.html"), "markdown_report": str(directory / "report.md")}, indent=2))
    if args.open_report: webbrowser.open((directory / "report.html").as_uri())
    return 0 if result["status"] == "FUNCTIONAL_MATCH" else 2 if result["status"] == "INCOMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
