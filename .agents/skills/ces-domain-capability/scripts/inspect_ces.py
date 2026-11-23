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


def read_rows(filename):
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
    return require_type(body, list, "CES response body")


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


def catalog_summary(rows, app):
    name(app, "CES application")
    names, ids, accounts = [], [], set()
    assignment_count = grant_count = 0
    for item in rows:
        row = require_type(item, dict, "CES catalog record")
        names.append(name(row.get("entitlement_name"), "entitlement_name"))
        if "entitlement_id" in row:
            if type(row["entitlement_id"]) is not int:
                raise EvidenceError("entitlement_id requires an integer.")
            ids.append(row["entitlement_id"])
        members = require_type(row.get("user_ids"), list, "user_ids")
        member_ids = unique([identity(member) for member in members], "user_ids")
        accounts.update(member_ids)
        assignment_count += len(member_ids)
        grant_count += len(permissions(row.get("role_entitlements")))
    unique(names, "catalog entitlement names")
    unique(ids, "catalog entitlement IDs")
    return {"status": "CATALOG_PRESENT" if rows else "CATALOG_EMPTY",
            "application_scope": "CALLER_DECLARED", "entitlement_count": len(rows),
            "account_count": len(accounts), "assignment_count": assignment_count,
            "role_grant_count": grant_count}


def effective_record(rows, app, user):
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


def main(argv=None):
    parser = ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("catalog", "user", "compare"):
        subparser = commands.add_parser(command)
        if command == "compare":
            subparser.add_argument("before")
            subparser.add_argument("after")
        else:
            subparser.add_argument("file")
        subparser.add_argument("--app", required=True)
        if command != "catalog":
            subparser.add_argument("--user", required=True)
        if command == "user":
            subparser.add_argument("--feature")
            subparser.add_argument("--action")
    args = parser.parse_args(argv)
    try:
        if args.command == "catalog":
            result = catalog_summary(read_rows(args.file), args.app)
        elif args.command == "user":
            requested = None
            if args.feature is not None or args.action is not None:
                if args.feature is None or args.action is None:
                    raise EvidenceError("Supply --feature and --action together.")
                requested = (name(args.feature, "feature"), name(args.action, "action"))
            result = user_summary(effective_record(read_rows(args.file), args.app, args.user), requested)
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
