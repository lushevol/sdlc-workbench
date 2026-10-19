"""Check an authorized evidence relocation without changing source material.

The output is created exclusively. Select a new output path for each later run.
This check compares storage and provenance. It does not verify business behavior.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

import yaml


HASH = re.compile(r"[a-f0-9]{64}\Z")
REVISION = re.compile(r"[a-f0-9]{40}\Z")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def local(root, name):
    relative = Path(name)
    if relative.is_absolute() or not name or ".." in relative.parts:
        raise ValueError("Use a confined workspace-relative path.")
    target = root
    for part in relative.parts:
        target /= part
        if target.is_symlink():
            raise ValueError("Use regular paths without symbolic links.")
    if not target.resolve().is_relative_to(root):
        raise ValueError("Use a confined workspace-relative path.")
    return target


def git(root, *arguments):
    return subprocess.check_output(
        ["git", "-C", str(root), *arguments], stderr=subprocess.DEVNULL
    )


def source_key(record):
    return record["id"], record["revision"]


def source_identity(record):
    return record["resource"], record["revision"], record["sha256"]


def check(root, map_path, manifest_path, audit_path, expected):
    findings = []
    counts = {}

    def fail(code, path):
        # Retain locators and codes only. Never retain source content.
        findings.append({"code": code, "path": str(path)})

    def equal_count(name, actual, target):
        counts[name] = actual
        if actual != target:
            fail("unexpected_" + name, map_path.relative_to(root))

    mapping = json.loads(map_path.read_text(encoding="utf-8"))
    task = map_path.parent.parent.parent
    base = mapping["base_revision"]
    if not REVISION.fullmatch(base):
        raise ValueError("Use a complete base Git revision.")
    git(root, "cat-file", "-e", base + "^{commit}")
    moves = mapping["records"]
    equal_count("relocation_entries", len(moves), expected["moves"])
    old_names = [item["old_path"] for item in moves]
    if len(set(old_names)) != len(old_names):
        fail("duplicate_original_locator", map_path.relative_to(root))
    destinations = {}
    methods = Counter()
    for item in moves:
        old = local(root, item["old_path"])
        target = local(root, item["canonical_path"])
        if not target.is_relative_to(task):
            fail("destination_outside_task", item["canonical_path"])
        recorded = item["sha256"]
        if not HASH.fullmatch(recorded):
            fail("invalid_sha256", item["old_path"])
        original = git(root, "show", base + ":" + item["old_path"])
        if digest(original) != recorded or len(original) != item["bytes"]:
            fail("base_bytes_mismatch", item["old_path"])
        if not target.is_file():
            fail("destination_missing", item["canonical_path"])
        else:
            current = target.read_bytes()
            if current != original or digest(current) != recorded:
                fail("destination_bytes_mismatch", item["canonical_path"])
        if old.exists() or old.is_symlink():
            fail("original_locator_remains", item["old_path"])
        prior = destinations.setdefault(item["canonical_path"], recorded)
        if prior != recorded:
            fail("conflicting_canonical_identity", item["canonical_path"])
        methods[item["method"]] += 1
    counts["canonical_destinations"] = len(destinations)
    counts["duplicate_destination_entries"] = len(moves) - len(destinations)
    counts["relocation_methods"] = dict(sorted(methods.items()))

    prior_record = mapping["prior_manifest"]
    prior_path = local(root, prior_record["path"])
    prior_bytes = prior_path.read_bytes()
    if digest(prior_bytes) != prior_record["sha256"]:
        fail("archived_manifest_hash_mismatch", prior_record["path"])
    if prior_bytes != git(root, "show", base + ":knowledge/raw/manifest.yaml"):
        fail("archived_manifest_base_mismatch", prior_record["path"])
    prior = yaml.safe_load(prior_bytes)
    active_path = local(root, "knowledge/raw/manifest.yaml")
    active = yaml.safe_load(active_path.read_bytes())
    previous = prior["sources"]
    current = active["sources"]
    previous_keys = [source_key(item) for item in previous]
    current_keys = [source_key(item) for item in current]
    if current_keys[:len(previous_keys)] != previous_keys:
        fail("manifest_source_order_or_identity_changed", "knowledge/raw/manifest.yaml")
    if len(set(current_keys)) != len(current_keys):
        fail("duplicate_manifest_identity", "knowledge/raw/manifest.yaml")
    current_by_key = {source_key(item): item for item in current}
    changed = {}
    for item in previous:
        actual = current_by_key.get(source_key(item))
        if actual is None:
            fail("manifest_source_missing", item["id"])
            continue
        fields = {key for key in set(item) | set(actual) if item.get(key) != actual.get(key)}
        if fields:
            changed[source_key(item)] = (item, actual)
            if fields != {"snapshot"}:
                fail("manifest_nonlocation_change", item["id"])
            if destinations.get(actual.get("snapshot")) != item["sha256"]:
                fail("manifest_destination_not_mapped", item["id"])
    equal_count("snapshot_only_updates", len(changed), expected["snapshots"])
    appended = current[len(previous):]
    equal_count("appended_source_records", len(appended), expected["appended"])
    updates = mapping["registered_snapshot_updates"]
    if len(updates) != len(changed):
        fail("snapshot_update_inventory_count_mismatch", map_path.relative_to(root))
    inventoried = set()
    for update in updates:
        key = update["source_id"], update["revision"]
        if key in inventoried or key not in changed:
            fail("snapshot_update_inventory_identity_mismatch", update["source_id"])
            continue
        inventoried.add(key)
        earlier, later = changed[key]
        if (update["old_snapshot"] != earlier["snapshot"]
                or update["snapshot"] != later["snapshot"]
                or source_identity(update) != source_identity(earlier)):
            fail("snapshot_update_inventory_mismatch", update["source_id"])
    if inventoried != set(changed):
        fail("snapshot_update_inventory_incomplete", map_path.relative_to(root))
    for item in appended:
        snapshot = local(root, item["snapshot"])
        if not snapshot.is_file() or digest(snapshot.read_bytes()) != item["sha256"]:
            fail("appended_source_hash_mismatch", item["id"])

    base_audits = [name for name in git(
        root, "ls-tree", "-r", "--name-only", base, "knowledge/audit"
    ).decode().splitlines() if Path(name).suffix.lower() in {".yaml", ".yml"}]
    for name in base_audits:
        path = local(root, name)
        if not path.is_file() or path.read_bytes() != git(root, "show", base + ":" + name):
            fail("existing_audit_changed_or_missing", name)
    counts["unchanged_existing_audit_files"] = len(base_audits)
    actual_audits = {p.relative_to(root).as_posix() for p in (root / "knowledge/audit").rglob("*")
                     if p.is_file() and p.suffix.lower() in {".yaml", ".yml"}}
    new_audits = actual_audits - set(base_audits)
    if new_audits != {audit_path.relative_to(root).as_posix()}:
        fail("unexpected_new_audit_files", "knowledge/audit")
    counts["new_audit_files"] = len(new_audits)
    event = yaml.safe_load(audit_path.read_bytes())
    if local(root, event["item_path"]) != map_path:
        fail("audit_target_not_relocation_map", audit_path.relative_to(root))
    if event["content_sha256"] != digest(map_path.read_bytes()):
        fail("audit_target_hash_mismatch", audit_path.relative_to(root))
    triples = {source_identity(item) for item in current}
    for evidence in event["evidence"]:
        if source_identity(evidence) not in triples:
            fail("audit_evidence_identity_missing", audit_path.relative_to(root))
    prior_event_path = local(root, "knowledge/audit/" + event["previous_event_id"] + ".yaml")
    prior_event = yaml.safe_load(prior_event_path.read_bytes())
    if (event["item_id"] != prior_event["item_id"]
            or event["item_version"] <= prior_event["item_version"]
            or event["from_state"] != prior_event["to_state"]
            or datetime.fromisoformat(event["at"]) < datetime.fromisoformat(prior_event["at"])):
        fail("audit_predecessor_mismatch", audit_path.relative_to(root))
    counts["new_audit_evidence_references"] = len(event["evidence"])

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["task_id"] != mapping["task_id"]:
        fail("task_manifest_identity_mismatch", manifest_path.relative_to(root))
    if (manifest_path.parent / manifest["relocation_map"]).resolve() != map_path:
        fail("task_manifest_relocation_reference_mismatch", manifest_path.relative_to(root))
    evidence_ids = set()
    represented = set()
    for item in manifest["records"]:
        if item["evidence_id"] in evidence_ids:
            fail("task_manifest_duplicate_evidence_id", item["evidence_id"])
        evidence_ids.add(item["evidence_id"])
        path = local(root, item["canonical_path"])
        represented.add(item["canonical_path"])
        if not path.is_file():
            fail("task_manifest_destination_missing", item["evidence_id"])
            continue
        data = path.read_bytes()
        if digest(data) != item["sha256"] or len(data) != item["bytes"]:
            fail("task_manifest_hash_or_size_mismatch", item["evidence_id"])
        if item.get("retained_path") and (task / item["retained_path"]).resolve() != path:
            fail("task_manifest_retained_path_mismatch", item["evidence_id"])
    for missing in set(destinations) - represented:
        fail("canonical_destination_not_indexed", missing)
    counts["task_manifest_records"] = len(manifest["records"])

    hashes = {p.relative_to(root).as_posix(): digest(p.read_bytes()) for p in
              (map_path, prior_path, active_path, manifest_path, audit_path, Path(__file__).resolve())}
    status = "FAILED" if findings else "PASSED"
    return {
        "schema_version": 1,
        "operation": "authorized-task-evidence-relocation-check",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "standard": "ASD-STE100",
        "automated_check": status,
        "asd_review": "PENDING",
        "reviewer": None,
        "reviewed_at": None,
        "base_revision": base,
        "counts": counts,
        "findings": findings,
        "input_sha256": hashes,
        "limitations": [
            "Automated checks do not check the complete approved dictionary or grammar rules.",
            "This check verifies storage and provenance. It does not establish source authority or human approval.",
            "This check does not execute portal behavior or verify PROD causation, corrected recovery, or workspace restoration.",
            "Historical embedded locators require the relocation map and retained Git revision.",
            "Existing ingestion baselines describe the earlier layout. This check does not change their retention rules.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument("--map", type=Path, default=Path(__file__).resolve().with_name("relocation-map.json"))
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--audit", type=Path)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().with_name("integrity-check.json"))
    parser.add_argument("--expected-moves", type=int, default=178)
    parser.add_argument("--expected-snapshots", type=int, default=58)
    parser.add_argument("--expected-appended", type=int, default=2)
    args = parser.parse_args()
    root = args.workspace.resolve()
    map_path = args.map.resolve()
    manifest = args.manifest or map_path.parent.parent / "manifest.json"
    audit = args.audit or root / "knowledge/audit/AUD-20261020-RAW-portal-task-relocation-v2.yaml"
    expected = {"moves": args.expected_moves, "snapshots": args.expected_snapshots,
                "appended": args.expected_appended}
    result = check(root, map_path, manifest.resolve(), audit.resolve(), expected)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    print(json.dumps({"status": result["status"], "counts": result["counts"],
                      "findings": result["findings"]}, indent=2))
    return 0 if result["status"] == "PASSED" else 1


if __name__ == "__main__":
    sys.exit(main())
