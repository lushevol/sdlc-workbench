"""Inspect retained CES JSON without exposing entitlement or account values."""

import argparse
import json
from pathlib import Path
import re
import sys


MAX_BYTES = 16 * 1024 * 1024
DATA_FIELDS = {"data_policies": dict, "data_profiles": dict, "data_entitlements": list}


class EvidenceError(ValueError):
    pass


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        # Argument errors can include a filename or account value.
        self.exit(2, "Invalid CES inspector arguments. Use --help for usage.\n")


def unique(values, field):
    entries = set(values)
    if len(entries) != len(values):
        raise EvidenceError(f"{field} contains duplicate entries.")
    return entries


def json_object(pairs):
    unique([key for key, _ in pairs], "JSON object")
    return dict(pairs)


def reject_constant(_):
    raise EvidenceError("Use finite JSON numbers.")


def read_json(filename):
    path = Path(filename)
    try:
        if not path.is_file():
            raise EvidenceError("Select a regular local JSON file.")
        with path.open("rb") as stream:
            raw = stream.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise EvidenceError("CES evidence exceeds the 16 MiB input limit.")
        body = json.loads(raw, object_pairs_hook=json_object, parse_constant=reject_constant)
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError):
        raise EvidenceError("Read a valid local CES JSON response body.") from None
    return body


def read_rows(filename):
    return require_type(read_json(filename), list, "CES response body")


def require_type(value, kind, field):
    if not isinstance(value, kind):
        label = "array" if kind is list else "object"
        raise EvidenceError(f"{field} requires an explicit JSON {label}.")
    return value


def name(value, field):
    if not isinstance(value, str) or not value.strip():
        raise EvidenceError(f"{field} requires a nonempty string.")
    return value.strip()


def identity(value):
    value = name(value, "CES account identity")
    if re.search(r"[,;|\s]", value):
        raise EvidenceError("CES account identity must select one account.")
    return value


def permissions(value):
    grants = []
    for permission in require_type(value, list, "role_entitlements"):
        permission = require_type(permission, dict, "CES permission")
        grants.append((name(permission.get("feature"), "feature"), name(permission.get("action"), "action")))
    return unique(grants, "role_entitlements")


def catalog_records(rows, app):
    name(app, "CES application")
    catalog, ids = {}, []
    for item in rows:
        row = require_type(item, dict, "CES catalog record")
        role = name(row.get("entitlement_name"), "entitlement_name")
        if role in catalog:
            raise EvidenceError("CES catalog contains duplicate entitlement names.")
        if "entitlement_id" in row:
            if type(row["entitlement_id"]) is not int:
                raise EvidenceError("entitlement_id requires an integer.")
            ids.append(row["entitlement_id"])
        members = require_type(row.get("user_ids"), list, "user_ids")
        member_ids = unique([identity(member) for member in members], "user_ids")
        catalog[role] = (member_ids, permissions(row.get("role_entitlements")))
    unique(ids, "catalog entitlement IDs")
    return catalog


def catalog_summary(rows, app):
    catalog = catalog_records(rows, app)
    accounts = set().union(*(members for members, _ in catalog.values()))
    return {"status": "CATALOG_PRESENT" if rows else "CATALOG_EMPTY",
            "application_scope": "CALLER_DECLARED", "entitlement_count": len(rows),
            "account_count": len(accounts),
            "assignment_count": sum(len(members) for members, _ in catalog.values()),
            "role_grant_count": sum(len(grants) for _, grants in catalog.values())}


def effective_row(rows, app, user, itam_id=None):
    app = name(app, "CES application")
    user = identity(user)
    if not rows:
        return None
    if len(rows) != 1:
        raise EvidenceError("CES effective-user response must contain at most one record.")
    row = require_type(rows[0], dict, "CES effective-user record")
    context = require_type(row.get("user_data"), dict, "user_data")
    if name(context.get("app_name"), "app_name") != app or identity(context.get("user_id")) != user:
        raise EvidenceError("CES response differs from the requested application or account.")
    if itam_id is not None and name(context.get("itam_id"), "itam_id") != name(itam_id, "expected ITAM ID"):
        raise EvidenceError("CES response differs from the requested ITAM ID.")
    return row


def effective_record(rows, app, user, itam_id=None):
    row = effective_row(rows, app, user, itam_id)
    if row is None:
        return None
    entitlements = require_type(row.get("entitlements"), dict, "entitlements")
    names = require_type(entitlements.get("entitlement_name"), list, "entitlement_name")
    assignments = unique([name(value, "CES assigned entitlement") for value in names], "entitlement_name")
    grants = permissions(entitlements.get("role_entitlements"))
    data = {}
    for key, kind in DATA_FIELDS.items():
        if key in entitlements:
            section = require_type(entitlements[key], kind, key)
            data[key] = json.dumps(section, sort_keys=True, allow_nan=False)
    return assignments, grants, data


def user_summary(record, requested=None):
    if record is None:
        result = {"status": "RECORD_ABSENT"}
        if requested is not None:
            result["requested_grant"] = "UNASSESSED"
        return result
    assignments, grants, data = record
    result = {"status": "PRESENT", "assignment_count": len(assignments),
              "effective_grant_count": len(grants), "role_grant_attribution": "UNAVAILABLE",
              "data_sections_present": sorted(data)}
    if requested is not None:
        result["requested_grant"] = "PRESENT" if requested in grants else "ABSENT"
    return result


def selected_grant(feature, action):
    if feature is None and action is None:
        return None
    if feature is None or action is None:
        raise EvidenceError("Supply --feature and --action together.")
    return name(feature, "feature"), name(action, "action")


def assigned_grant_side(value, field, app, app_uid):
    side = require_type(value, dict, "CES assigned-role grant")
    nested = side.get("applicationDto")
    if nested is not None:
        nested = require_type(nested, dict, "applicationDto")
        nested_uid = nested.get("appUID")
        if nested_uid is not None and type(nested_uid) is not int:
            raise EvidenceError("Grant application UID requires an integer.")
        if name(nested.get("appName"), "grant application name") != app or (
            app_uid is not None and nested_uid != app_uid
        ):
            raise EvidenceError("Grant application contradicts its assigned role.")
    return name(side.get(field), field)


def assigned_role_records(rows, app, app_id=None, app_uid=None):
    app = name(app, "CES application")
    if app_id is not None:
        app_id = name(app_id, "CES application ID")
    assignments = {}
    selected_ids, selected_uids = set(), set()
    matched_app_name = False
    for item in rows:
        row = require_type(item, dict, "CES assigned-role record")
        if name(row.get("appName"), "appName") != app:
            continue
        matched_app_name = True
        row_id = name(row.get("appId"), "appId")
        if app_id is not None and row_id != app_id:
            continue
        row_uid = row.get("appUID")
        if row_uid is not None and type(row_uid) is not int:
            raise EvidenceError("appUID requires an integer.")
        if app_uid is not None and row_uid != app_uid:
            continue
        selected_ids.add(row_id)
        if row_uid is not None:
            selected_uids.add(row_uid)
        if len(selected_ids) > 1 or len(selected_uids) > 1:
            raise EvidenceError("The selected application name matches conflicting CES application identities.")
        role = name(row.get("entitlementName"), "entitlementName")
        if role in assignments:
            raise EvidenceError("CES assigned-role response contains duplicate entitlement names.")
        grants = []
        for item in require_type(row.get("featureActionDtos"), list, "featureActionDtos"):
            pair = require_type(item, dict, "CES assigned-role grant")
            feature = assigned_grant_side(pair.get("features"), "featureName", app, row_uid)
            action = assigned_grant_side(pair.get("actions"), "actionName", app, row_uid)
            grants.append((feature, action))
        assignments[role] = unique(grants, "CES assigned-role grant list")
    if matched_app_name and not assignments:
        raise EvidenceError("No matching application row has the requested CES application identity.")
    return assignments


def assigned_role_summary(rows, app, app_id=None, app_uid=None, entitlement=None, requested=None):
    if entitlement is not None:
        entitlement = name(entitlement, "CES assigned entitlement")
    assignments = assigned_role_records(rows, app, app_id, app_uid)
    result = {
        "status": "ASSIGNMENTS_PRESENT" if assignments else "NO_ASSIGNMENTS",
        "account_scope": "CALLER_DECLARED",
        "assignment_count": len(assignments),
        "assignments_without_grants": sum(not grants for grants in assignments.values()),
        "role_grant_count": sum(len(grants) for grants in assignments.values()),
    }
    if entitlement is not None:
        result["requested_entitlement"] = "PRESENT" if entitlement in assignments else "ABSENT"
    if requested is not None:
        grants = assignments.values() if entitlement is None else [assignments.get(entitlement, set())]
        result["requested_grant"] = "PRESENT" if any(requested in pairs for pairs in grants) else "ABSENT"
    return result


def delta(before, after):
    return {"added": len(after - before), "removed": len(before - after)}


def compare(before, after):
    if before is None or after is None:
        return {"status": "UNASSESSED", "before": user_summary(before)["status"],
                "after": user_summary(after)["status"]}
    old_assignments, old_grants, old_data = before
    new_assignments, new_grants, new_data = after
    return {
        "status": "COMPARED",
        "assignments": delta(old_assignments, new_assignments),
        "effective_grants": delta(old_grants, new_grants),
        "role_grant_attribution": "UNAVAILABLE",
        "data_sections_changed": sorted(key for key in old_data.keys() | new_data.keys()
                                        if old_data.get(key) != new_data.get(key)),
    }


def compare_views(left, right):
    if right is None:
        return {"status": "UNASSESSED"}
    return {"status": "MATCH" if left == right else "DIFFERENT", **delta(left, right)}


def profile_value(row, pointer, expected):
    if expected is not None and not isinstance(expected, str):
        raise EvidenceError("Expected profile must be a JSON string or null.")
    if not pointer.startswith("/") or re.search(r"~(?![01])", pointer):
        raise EvidenceError("Supply a JSON Pointer relative to the effective-user record.")
    missing = object()
    value = row if row is not None else missing
    for token in pointer.split("/")[1:]:
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(value, dict):
            value = value.get(token, missing)
        elif isinstance(value, list) and re.fullmatch(r"0|[1-9][0-9]*", token) and len(token) <= len(str(len(value))):
            index = int(token)
            value = value[index] if index < len(value) else missing
        else:
            value = missing
        if value is missing:
            return {"status": "UNASSESSED", "reason": "RECORD_ABSENT" if row is None else "VALUE_ABSENT"}
    return {"status": "MATCH" if value == expected else "DIFFERENT"}


def reconcile(catalog, assigned_roles, effective, user):
    user = identity(user)
    catalog_roles = {role: grants for role, (members, grants) in catalog.items() if user in members}
    catalog_names = set(catalog_roles)
    assigned_names = set(assigned_roles)
    catalog_role_grants = {(role, *pair) for role, pairs in catalog_roles.items() for pair in pairs}
    assigned_role_grants = {(role, *pair) for role, pairs in assigned_roles.items() for pair in pairs}
    assigned_union = set().union(*assigned_roles.values())
    effective_names, effective_grants = effective[:2] if effective is not None else (None, None)
    return {
        "status": "COMPARED" if effective is not None else "UNASSESSED",
        "catalog_account_scope": "CALLER_DECLARED",
        "assigned_role_account_scope": "CALLER_DECLARED",
        "effective_user_status": "PRESENT" if effective is not None else "RECORD_ABSENT",
        "comparisons": {
            "catalog_vs_assigned_role_assignments": compare_views(catalog_names, assigned_names),
            "catalog_vs_effective_assignments": compare_views(catalog_names, effective_names),
            "assigned_role_vs_effective_assignments": compare_views(assigned_names, effective_names),
            "catalog_vs_assigned_role_grants": compare_views(catalog_role_grants, assigned_role_grants),
            "assigned_role_union_vs_effective_grants": compare_views(assigned_union, effective_grants),
        },
    }


def main(argv=None):
    parser = ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("catalog", "user", "compare", "assigned-role", "reconcile", "profile"):
        subparser = commands.add_parser(command)
        if command == "compare":
            subparser.add_argument("before")
            subparser.add_argument("after")
        elif command == "reconcile":
            subparser.add_argument("catalog")
            subparser.add_argument("role_details")
            subparser.add_argument("effective")
        else:
            subparser.add_argument("file")
        subparser.add_argument("--app", required=True)
        if command in ("user", "compare", "reconcile", "profile"):
            subparser.add_argument("--user", required=True)
        if command in ("reconcile", "profile"):
            subparser.add_argument("--itam-id")
        if command == "profile":
            subparser.add_argument("--pointer", required=True)
            subparser.add_argument("--expected", required=True)
        if command in ("user", "assigned-role"):
            subparser.add_argument("--feature")
            subparser.add_argument("--action")
        if command in ("assigned-role", "reconcile"):
            subparser.add_argument("--app-id")
            subparser.add_argument("--app-uid", type=int)
        if command == "assigned-role":
            subparser.add_argument("--entitlement")
    args = parser.parse_args(argv)
    try:
        if args.command == "catalog":
            result = catalog_summary(read_rows(args.file), args.app)
        elif args.command == "user":
            requested = selected_grant(args.feature, args.action)
            result = user_summary(effective_record(read_rows(args.file), args.app, args.user), requested)
        elif args.command == "assigned-role":
            requested = selected_grant(args.feature, args.action)
            result = assigned_role_summary(read_rows(args.file), args.app, args.app_id, args.app_uid,
                                           args.entitlement, requested)
        elif args.command == "reconcile":
            catalog = catalog_records(read_rows(args.catalog), args.app)
            assigned_roles = assigned_role_records(read_rows(args.role_details), args.app, args.app_id, args.app_uid)
            effective = effective_record(read_rows(args.effective), args.app, args.user, args.itam_id)
            result = reconcile(catalog, assigned_roles, effective, args.user)
        elif args.command == "profile":
            row = effective_row(read_rows(args.file), args.app, args.user, args.itam_id)
            result = profile_value(row, args.pointer, read_json(args.expected))
        else:
            before = effective_record(read_rows(args.before), args.app, args.user)
            after = effective_record(read_rows(args.after), args.app, args.user)
            result = compare(before, after)
    except EvidenceError as error:
        print(str(error), file=sys.stderr)
        return 2
    except (ValueError, RecursionError):
        print("CES evidence contains an unsupported JSON value.", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
