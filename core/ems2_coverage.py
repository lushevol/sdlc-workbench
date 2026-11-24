"""Compare EMS2 PROD baseline content with EMS2 UAT target content.

Supplied-response replay is the default. Numeric environment identifiers are
request locators; entity, role, subject, and action names define comparison keys.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
from urllib.parse import quote
import webbrowser

from .entitlement_coverage import (
    Collector, _bounded_error, _collection, _comparison_context, _configuration, _hash, _now, _write,
)
from .entitlement_reconciliation import (
    ReconciliationError, compare_sets, normalize_ems2_permissions, split_user_ids,
)
from .entitlement_sources import SourceError, load_root_env, read_http_example, read_matrix


def _discovery(config, folder, included):
    matrices = [read_matrix(folder / entity["workbook"]) for entity in included]
    baseline = {user for matrix in matrices for user in matrix["users"]}
    users = baseline | set(split_user_ids(config.get("users", [])))
    baseline.update(split_user_ids(config.get("users", [])))
    names = {entity["name"] for entity in included}
    paths = sorted({path for pattern in config.get("replay", {}).get("examples", [])
                    for path in folder.glob(pattern)})
    for path in paths:
        item = read_http_example(path)
        if item["method"] != "POST" or not isinstance(item["body"], dict):
            continue
        for environment in ("prod", "uat"):
            settings = config[environment]
            expected = settings["base_url"].rstrip("/") + "/" + settings["entitlements_path"].lstrip("/")
            if item["url"] != expected:
                continue
            for raw_user, entities in item["body"].items():
                if not isinstance(entities, list) or not all(isinstance(name, str) for name in entities):
                    raise SourceError("INVALID_DISCOVERY_REQUEST")
                if not names.intersection(entities):
                    continue
                declared = split_user_ids(raw_user)
                if len(declared) != 1:
                    raise ValueError("An EMS2 request key must identify one account")
                users.update(declared)
                if environment == "prod": baseline.update(declared)
    return matrices, sorted(users), sorted(baseline), paths


def _case(user, collectors, config, included):
    record = {"user_id": user, "at": _now(), "status": "UNASSESSED", "errors": []}
    names = {entity["name"]: entity["name"] for entity in included}
    acquired = {}
    for environment in ("prod", "uat"):
        try:
            raw = collectors[environment].get("ems2", config[environment]["entitlements_path"], {user: list(names)})
            normalized = normalize_ems2_permissions(raw, names)["users"]
            if set(normalized) != {user}:
                raise SourceError("ACCOUNT_CONTEXT_MISMATCH")
            acquired[environment] = normalized[user]
        except (SourceError, ReconciliationError, KeyError, ValueError) as error:
            record["errors"].append({"source": environment, **_bounded_error(error)})
    if record["errors"]:
        return record
    for label, key in (("effective", "effective_permissions"), ("assignments", "assignments"),
                       ("profile_grants", "grants")):
        record[label] = compare_sets(acquired["prod"][key], acquired["uat"][key])
    record.update(status="MATCH" if all(record[k]["equal"] for k in ("effective", "assignments", "profile_grants")) else "DIFFERENT",
                  baseline_has_permissions=bool(acquired["prod"]["grants"]),
                  role_evidence="Assignments and role-specific grants derive from entitlementList permission rows only.",
                  data_scope={"status": "UNASSESSED", "reason": "Complete EMS2 field/value and empty-role definitions were not supplied."},
                  exact_full_profile_status="UNASSESSED")
    return record


def _inventories(collectors, config, included):
    checks = []
    for entity in included:
        for kind in ("subjects", "roles"):
            check = {"entity": entity["name"], "kind": kind, "status": "UNASSESSED", "errors": []}
            values = {}
            for environment in ("prod", "uat"):
                try:
                    path = config[environment][kind + "_path"].format(entity_id=quote(str(entity[environment + "_id"]), safe=""))
                    body = collectors[environment].get("ems2", path)
                    names = _collection(body, kind)
                    if any(not name.strip() for name in names): raise SourceError("INVALID_COLLECTION_ITEM")
                    for row in body[kind]:
                        context = row.get("entity")
                        if context is not None:
                            if not isinstance(context, dict): raise SourceError("INVALID_ENTITY_CONTEXT")
                            if context.get("name") is not None and context["name"] != entity["name"]:
                                raise SourceError("ENTITY_CONTEXT_MISMATCH")
                    values[environment] = [[entity["name"], name] for name in names]
                except (SourceError, ReconciliationError, KeyError, ValueError) as error:
                    check["errors"].append({"source": environment, **_bounded_error(error)})
            check.update(values)
            if not check["errors"]:
                check["comparison"] = compare_sets(values["prod"], values["uat"])
                check["status"] = "MATCH" if check["comparison"]["equal"] else "DIFFERENT"
            checks.append(check)
    result = {"inventories": checks}
    for kind in ("subjects", "roles"):
        acquired = [x for x in checks if x["kind"] == kind and x["status"] != "UNASSESSED"]
        comparison = compare_sets([row for x in acquired for row in x["prod"]],
                                  [row for x in acquired for row in x["uat"]])
        missing = [x["entity"] for x in checks if x["kind"] == kind and x["status"] == "UNASSESSED"]
        comparison.update(complete=not missing, assessed_entities=len(acquired),
                          unassessed_entities=missing, assessed_coverage_percent=comparison["coverage_percent"])
        if missing:
            comparison.update(status="UNASSESSED", equal=None, preserved=None, coverage_percent=None)
        result[kind] = comparison
    return result


def _render(result, path):
    """Write both human-readable formats through the shared report contract."""
    from .coverage_reporting import write_report
    write_report(result, path.parent)


def _finish(result, directory):
    users = result["users"]
    population = result["inventory"]["users"]
    baseline = set(result["inventory"]["baseline_users"])
    baseline.update(user["user_id"] for user in users if user.get("baseline_has_permissions"))
    assessed = {user["user_id"] for user in users if user["status"] != "UNASSESSED"}
    matching = sum(user["status"] == "MATCH" and user["user_id"] in baseline for user in users)
    summary = {"discovered_accounts": len(population), "baseline_accounts": len(baseline),
               "compared_accounts": len(assessed), "matching_accounts": sum(x["status"] == "MATCH" for x in users),
               "different_accounts": sum(x["status"] == "DIFFERENT" for x in users),
               "unassessed_accounts": len(population) - len(assessed), "matching_baseline_accounts": matching,
               "assessed_baseline_accounts": len(baseline & assessed),
               "functional_profile_coverage_percent": round(100 * matching / len(baseline), 6) if baseline and set(population) <= assessed else None,
               "full_data_profile_coverage": "UNASSESSED"}
    subjects = result["entitlements"]["subjects"]
    summary["subject_coverage"] = (f"{subjects['matched_count']}/{subjects['baseline_count']} in assessed inventories; "
                                   f"{len(subjects['unassessed_entities'])} entities unassessed")
    grants = [user["profile_grants"] for user in users if user["status"] != "UNASSESSED"]
    summary["role_grant_preservation"] = f"{sum(item['matched_count'] for item in grants)}/{sum(item['baseline_count'] for item in grants)} observed user grants"
    summary["subject_coverage_percent"] = subjects["coverage_percent"]
    summary["role_coverage_percent"] = result["entitlements"]["roles"]["coverage_percent"]
    result["summary"] = summary
    incomplete = bool(result["errors"]) or summary["unassessed_accounts"] > 0 or any(x["status"] == "UNASSESSED" for x in result["entitlements"]["inventories"])
    if result["errors"]: summary["functional_profile_coverage_percent"] = None
    different = summary["different_accounts"] > 0 or any(x["status"] == "DIFFERENT" for x in result["entitlements"]["inventories"])
    result["status"] = "INCOMPLETE" if incomplete else "DIFFERENCES" if different else "FUNCTIONAL_MATCH"
    result["conclusion"] = ("Comparison is incomplete. Keep unavailable accounts and inventories unassessed."
                            if incomplete else "Review missing and additional UAT permissions before declaring equivalent content."
                            if different else "All declared functional comparisons match. Full data-profile equality remains unassessed.")
    if result["mode"] == "replay": result["conclusion"] = "Mock comparison uses supplied API responses only. " + result["conclusion"]
    result["finished_at"] = _now()
    result["writing_review"] = {"standard": "ASD-STE100", "automated_check": "NOT_RUN", "asd_review": "PENDING",
                               "reviewer": None, "reviewed_at": None,
                               "limitations": ["Automated checks do not check the complete approved dictionary or grammar rules."]}
    _write(directory / "result.json", result)
    with (directory / "differences.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream); writer.writerow(["scope", "account_or_entity", "comparison", "kind", "item"])
        for check in result["entitlements"]["inventories"]:
            for error in check["errors"]:
                writer.writerow(["inventory", check["entity"], check["kind"], "unassessed", json.dumps(error)])
            for kind in ("missing", "additional"):
                for item in check.get("comparison", {}).get(kind, []): writer.writerow(["inventory", check["entity"], check["kind"], kind, json.dumps(item)])
        for user in users:
            for error in user["errors"]: writer.writerow(["user", user["user_id"], error["source"], "unassessed", error["code"]])
            for comparison in ("effective", "assignments", "profile_grants"):
                for kind in ("missing", "additional"):
                    for item in user.get(comparison, {}).get(kind, []): writer.writerow(["user", user["user_id"], comparison, kind, json.dumps(item)])
        for user in population:
            if user not in {item["user_id"] for item in users}: writer.writerow(["user", user, "collection", "unassessed", "NOT_FETCHED"])
        for error in result["errors"]: writer.writerow(["acquisition", "", "source", "unassessed", error["code"]])
    _render(result, directory / "report.html")
    return result


def run(config_path, *, mode="replay", output=None, resume=None, user_limit=None):
    if mode not in ("replay", "live") or (user_limit is not None and user_limit < 1):
        raise ValueError("Invalid mode or user limit")
    config_path = Path(config_path).resolve(); folder = config_path.parent
    config, included = _configuration(config_path)
    for entity in included:
        if not all(str(entity.get(key, "")).strip() for key in ("prod_id", "uat_id")):
            raise ValueError("Each included entity needs PROD and UAT request identifiers")
    matrices, population, baseline, paths = _discovery(config, folder, included)
    binding = {"config_sha256": _hash(config_path.read_bytes()), "mode": mode,
               "matrix_sha256": [matrix["sha256"] for matrix in matrices],
               "replay_sha256": {str(path.resolve()): _hash(path.read_bytes()) for path in paths},
               "implementation_sha256": {name: _hash(Path(__file__).with_name(name).read_bytes()) for name in
                                         ("ems2_coverage.py", "entitlement_coverage.py", "entitlement_sources.py", "entitlement_reconciliation.py", "coverage_reporting.py")}}
    directory = Path(resume).resolve() if resume else Path(output).resolve() if output else (
        folder / config["output_dir"] / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "-ems2-" + mode)).resolve()
    if directory.exists() and not resume: raise ValueError("Output already exists; use --resume")
    directory.mkdir(parents=True, exist_ok=True)
    if resume:
        if json.loads((directory / "binding.json").read_text()) != binding: raise ValueError("Resume configuration or source hashes changed")
    else: _write(directory / "binding.json", binding)
    result = {"schema_version": 1, "mode": mode, "started_at": _now(), "scope": config["scope"],
              "direction": {"baseline": "EMS2 PROD", "target": "EMS2 UAT"},
              "evidence_source": "MOCK: supplied API responses" if mode == "replay" else "LIVE: collected API responses",
              "binding": binding,
              "comparison_context": _comparison_context(config, folder, included, matrices, family="EMS2_ENVIRONMENTS"), "excluded": [entity for entity in config["entities"] if not entity.get("included", True)],
              "inventory": {"users": population, "baseline_users": baseline, "matrices": matrices,
                            "source": "Matrix assignments, configured users, and scoped stored EMS2 request keys; no complete account-directory endpoint supplied."},
              "users": [], "errors": [], "entitlements": {"inventories": []},
              "limits": ["PROD is the baseline. Missing and additional compare UAT with PROD.",
                         "Entity, role, subject, and action names define identity. Environment numeric identifiers are request locators only.",
                         "Account discovery is bounded by matrices, configured users, and supplied request keys.",
                         "Assignments derive from permission rows. Empty roles and complete role definitions cannot be reconstructed.",
                         "Complete EMS2 field/value policies are unavailable; full data-profile equality remains unassessed.",
                         "Replay never establishes current live state or an atomic cross-environment snapshot."]}
    existing = {}
    try:
        workspace = (folder / config["workspace_root"]).resolve()
        environment = load_root_env(workspace) if mode == "live" else {}
        collectors = {}
        for name in ("prod", "uat"):
            settings = config[name]
            ca_key = settings.get("ca_env")
            if ca_key and environment.get(ca_key):
                ca = Path(environment[ca_key]).expanduser()
                environment[ca_key] = str(ca if ca.is_absolute() else workspace / ca)
            collectors[name] = Collector({**config, "ems2": settings}, folder, directory, mode, environment)
        result["entitlements"] = _inventories(collectors, config, included)
        checkpoint = directory / "cases.jsonl"
        if resume and checkpoint.exists():
            for line in checkpoint.read_text().splitlines():
                record = json.loads(line); digest = record.pop("record_sha256", None)
                if digest != _hash(record) or record["user_id"] not in population: raise ValueError("Account checkpoint identity changed")
                existing[record["user_id"]] = record
        pending = [user for user in population if user not in existing or existing[user]["status"] == "UNASSESSED"]
        if user_limit is not None:
            pending = pending[:user_limit]
            result["limits"].append("Explicit user limit used; remaining accounts stay unassessed.")
        workers = max(1, int(config.get("workers", 4)))
        with checkpoint.open("a", encoding="utf-8") as stream:
            for start in range(0, len(pending), workers):
                group = pending[start:start + workers]; stop = False
                with ThreadPoolExecutor(max_workers=len(group)) as pool:
                    for future in as_completed([pool.submit(_case, user, collectors, config, included) for user in group]):
                        record = future.result(); existing[record["user_id"]] = record
                        stream.write(json.dumps({**record, "record_sha256": _hash(record)}) + "\n"); stream.flush(); os.fsync(stream.fileno())
                        print(f"Saved EMS2 account {len(existing)}/{len(population)}: {record['status']}", file=sys.stderr, flush=True)
                        if mode == "live" and any(error.get("http_status") in (401, 403) or error["code"] in
                                                 {"NETWORK_ERROR", "TLS_ERROR", "TLS_CONFIGURATION", "MISSING_CREDENTIAL"} for error in record["errors"]): stop = True
                if stop: break
    except (SourceError, ReconciliationError, KeyError, ValueError) as error:
        result["errors"].append(_bounded_error(error))
    result["users"] = [existing[user] for user in sorted(existing)]
    if "subjects" not in result["entitlements"]:
        for kind in ("subjects", "roles"):
            result["entitlements"][kind] = {**compare_sets([], []), "complete": False, "coverage_percent": None, "unassessed_entities": [e["name"] for e in included]}
    _finish(result, directory)
    return result, directory


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--mode", choices=("replay", "live"), default="replay")
    parser.add_argument("--output"); parser.add_argument("--resume")
    parser.add_argument("--user-limit", type=int)
    parser.add_argument("--open", action="store_true", dest="open_report")
    args = parser.parse_args(argv)
    try:
        result, directory = run(args.config, mode=args.mode, output=args.output, resume=args.resume, user_limit=args.user_limit)
    except (SourceError, ValueError, KeyError, OSError) as error:
        print("EMS2 coverage setup failed: " + type(error).__name__ + ". Check configured source files.", file=sys.stderr)
        return 2
    print(json.dumps({"status": result["status"], "mode": result["mode"], "evidence_source": result["evidence_source"],
                      "summary": result["summary"], "report": str(directory / "report.html"),
                      "html_report": str(directory / "report.html"), "markdown_report": str(directory / "report.md")}, indent=2))
    if args.open_report: webbrowser.open((directory / "report.html").as_uri())
    return 0 if result["status"] == "FUNCTIONAL_MATCH" else 2 if result["status"] == "INCOMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
