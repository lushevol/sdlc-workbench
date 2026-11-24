"""Read supplied migration matrices without changing their bytes."""
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import openpyxl

TASK = Path(__file__).resolve().parents[2]
FILES = TASK / "ces migration"
OUT = Path(__file__).with_name("matrix-inventory.json")


def clean(value):
    return str(value).strip() if value is not None else None


def rows(sheet, start=2):
    return [(number, list(row)) for number, row in
            enumerate(sheet.iter_rows(min_row=start, values_only=True), start)
            if any(v is not None for v in row)]


inventory = []
all_users = set()
all_pairs = set()
all_status_users = set()
all_user_types = defaultdict(set)
for path in sorted(FILES.glob("*.xlsx")):
    workbook = openpyxl.load_workbook(path, data_only=True, read_only=False)
    formula_workbook = openpyxl.load_workbook(path, data_only=False, read_only=True)
    application = rows(workbook["Application"])[0][1]
    assignments = rows(workbook["UserEntitlement"], 3)
    status_rows = rows(workbook["User Active Status"], 3)
    entitlement_rows = rows(workbook["Entitlement"])
    efa_rows = rows(workbook["EntitlementFeatureAction"])
    feature_rows = rows(workbook["Feature"])
    users = {clean(r[0]) for _, r in assignments if r[0] is not None}
    user_pairs = [(clean(r[0]), clean(r[1])) for _, r in assignments]
    all_users.update(users)
    for _, row in assignments:
        all_user_types[clean(row[0])].add(clean(row[5]))
    all_pairs.update((path.name, *pair) for pair in user_pairs)
    profiles = {clean(r[0]) for _, r in entitlement_rows}
    referenced_profiles = {clean(r[0]) for _, r in efa_rows}
    assigned_profiles = {clean(r[1]) for _, r in assignments}
    status_users = {clean(r[0]) for _, r in status_rows if r[0] is not None}
    all_status_users.update(status_users)
    unassigned_status_rows = [r for _, r in status_rows if clean(r[0]) not in users]
    efa_keys = [tuple(clean(v) for v in r[:4]) for _, r in efa_rows]
    links = defaultdict(set)
    for _, r in efa_rows:
        links[clean(r[0])].add((clean(r[1]), clean(r[2]), clean(r[3])))
    effective = defaultdict(set)
    for _, row in assignments:
        effective[clean(row[0])].update(links.get(clean(row[1]), set()))
    counts = Counter(user_pairs)
    account_types = Counter(clean(r[5]) for _, r in assignments)
    prod = Counter(clean(r[7]) for _, r in assignments)
    nonprod = Counter(clean(r[14]) for _, r in assignments)
    formulas = {s.title: sum(c.data_type == "f" for row in s for c in row)
                for s in formula_workbook}
    missing_rows = [number for number, r in assignments if clean(r[1]) not in links]
    record = {
        "file": str(path.relative_to(TASK)),
        "sha256": sha256(path.read_bytes()).hexdigest(),
        "filename_environment": "uat" if "_uat" in path.name else "prod",
        "properties": {"created": str(workbook.properties.created),
                       "modified": str(workbook.properties.modified),
                       "timezone": "not recorded; not a verified source capture time"},
        "application": {"itam_id": application[0], "itam_name": application[1],
                        "name": application[2], "locator": "Application!A2:C2"},
        "sheets": [{"name": s.title, "max_row": s.max_row,
                    "max_column": s.max_column,
                    "nonempty_data_rows": len(rows(s, 3 if s.title in
                         ("UserEntitlement", "User Active Status") else 2)),
                    "formula_count": formulas[s.title],
                    "hidden_rows": [i for i, d in s.row_dimensions.items() if d.hidden],
                    "hidden_columns": [i for i, d in s.column_dimensions.items() if d.hidden],
                    "auto_filter": s.auto_filter.ref,
                    "comment_count": sum(c.comment is not None for row in s for c in row)}
                   for s in workbook],
        "catalog": {
            "feature_count": len(feature_rows),
            "feature_names": [clean(r[0]) for _, r in feature_rows],
            "feature_locator": f"Feature!A2:D{workbook['Feature'].max_row}",
            "action_count": len(rows(workbook["Action"])),
            "entitlement_count": len(profiles),
            "entitlement_names": sorted(profiles),
            "entitlement_locator": f"Entitlement!A2:F{workbook['Entitlement'].max_row}",
            "efa_rows": len(efa_rows), "efa_unique_keys": len(set(efa_keys)),
            "efa_duplicate_rows": len(efa_keys) - len(set(efa_keys)),
            "efa_locator": f"EntitlementFeatureAction!A2:E{workbook['EntitlementFeatureAction'].max_row}",
            "profiles_without_efa": sorted(profiles - referenced_profiles),
            "efa_profiles_not_in_catalog": sorted(referenced_profiles - profiles),
            "efa_unique_features": sorted({clean(r[2]) for _, r in efa_rows}),
            "efa_unique_feature_action_count": len({(clean(r[2]), clean(r[3])) for _, r in efa_rows}),
            "profiles_without_assignment": sorted(profiles - assigned_profiles),
        },
        "assignments": {
            "row_count": len(assignments), "unique_users": len(users),
            "unique_user_entitlement_pairs": len(set(user_pairs)),
            "duplicate_assignment_rows": sum(n - 1 for n in counts.values()),
            "assigned_profile_count": len(assigned_profiles),
            "assigned_profile_names": sorted(assigned_profiles),
            "assigned_profiles_not_in_catalog": sorted(assigned_profiles - profiles),
            "assigned_profiles_without_efa": sorted(assigned_profiles - referenced_profiles),
            "rows_whose_profile_has_no_efa": missing_rows,
            "missing_profile_assignment_locators": [f"UserEntitlement!A{n}:G{n}" for n in missing_rows],
            "users_with_empty_derived_feature_action_set": sum(not v for v in effective.values()),
            "unique_user_feature_action_tuples": sum(len(v) for v in effective.values()),
            "account_type_assignment_counts": dict(account_types),
            "prod_present_in_assignment_counts": dict(prod),
            "prod_directory_absent_assignment_rows": sum(clean(r[7]) in (None, "None") for _, r in assignments),
            "nonprod_present_in_assignment_counts": dict(nonprod),
            "locator": f"UserEntitlement!A3:G{workbook['UserEntitlement'].max_row}",
            "environment_headers": "UserEntitlement!H1:U2",
            "identity_columns": {"A": "USERNAME", "B": "ENTITLEMENTNAME",
                "N": "Prod PSID", "U": "Non-Prod PSID"},
        },
        "directory_status": {
            "row_count": len(status_rows), "unique_users": len(status_users),
            "users_without_assignment": len(status_users - users),
            "assignment_users_without_status": len(users - status_users),
            "unassigned_prod_directory_present_counts": dict(Counter(clean(r[2]) for r in unassigned_status_rows)),
            "unassigned_nonprod_directory_present_counts": dict(Counter(clean(r[9]) for r in unassigned_status_rows)),
            "locator": f"'User Active Status'!A3:P{workbook['User Active Status'].max_row}",
            "limit": "Directory presence/status is not CES provisioning or permission evidence."
        },
        "limits": [
            "No source-system capture identifier or verified synchronized time is recorded.",
            "These are CES-shaped conversion matrices, not complete EMS2 and CES execution snapshots.",
            "EntitlementFeatureAction joins to UserEntitlement by entitlement and application.",
            "Do not treat directory display names or email differences as permission differences.",
            "Profile names do not establish data-policy field/value content."
        ]
    }
    inventory.append(record)

output = {"analysis_date": "2026-11-03", "mode": "read-only local source inspection",
          "source_count": len(inventory), "matrices": inventory,
          "cross_matrix_unique_assignment_users": len(all_users),
          "cross_matrix_unique_directory_status_users": len(all_status_users),
          "directory_status_users_without_any_assignment": len(all_status_users - all_users),
          "cross_matrix_unique_users_by_account_type": dict(Counter(next(iter(types)) for types in all_user_types.values() if len(types) == 1)),
          "account_type_conflict_user_count": sum(len(types) > 1 for types in all_user_types.values()),
          "cross_matrix_unique_entity_user_entitlement_pairs": len(all_pairs),
          "parity_status": "NOT_MEASURED; no complete paired EMS2 PROD and CES UAT snapshots"}
OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"saved": str(OUT), "unique_users": len(all_users),
                  "summaries": [{"file": m["file"], "catalog": m["catalog"],
                                 "assignments": m["assignments"], "directory_status": m["directory_status"]}
                                for m in inventory]}, ensure_ascii=False))
