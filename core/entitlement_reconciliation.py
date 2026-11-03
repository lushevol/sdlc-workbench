"""Normalize supported permission contracts and compare their declared content.

This module performs no network or file access. Application and name mappings
belong to the calling project's configuration. Names remain case-sensitive.
"""

from __future__ import annotations

import json
import math
import re
from collections.abc import Iterable, Mapping
from typing import Any


class ReconciliationError(ValueError):
    """A permission response cannot support a complete comparison."""


def _name(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ReconciliationError(f"{field} must contain a nonempty name")
    return value.strip()


def _object(value: Any, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ReconciliationError(f"{field} must be an object")
    return value


def _array(value: Any, field: str) -> list[Any]:
    if not isinstance(value, list):
        raise ReconciliationError(f"{field} must be an explicit array")
    return value


def _records(values: Iterable[tuple[str, ...]]) -> list[list[str]]:
    return [list(value) for value in sorted(set(values))]


def _map_name(
    name: str, entity: str, mapping: Mapping[str, Mapping[str, str]] | None, field: str
) -> str:
    if mapping is None:
        return name
    scope = mapping.get(entity, {})
    if not isinstance(scope, Mapping):
        raise ReconciliationError(f"{field} mapping scope must be an object")
    return _name(scope.get(name, name), f"mapped {field}")


def split_user_ids(value: Any) -> list[str]:
    """Expand scalar, delimited-cell, or JSON-array identities without a limit.

    Numeric spreadsheet identifiers are accepted only when they are integral.
    Leading zeroes in string identities are retained. Delimiters are commas,
    semicolons, pipes, and whitespace; identity values must not contain them.
    """
    if value is None:
        return []
    if isinstance(value, bool):
        raise ReconciliationError("A boolean is not an account identifier")
    if isinstance(value, int):
        return [str(value)]
    if isinstance(value, float):
        if not math.isfinite(value) or not value.is_integer():
            raise ReconciliationError("A numeric account identifier must be integral")
        return [str(int(value))]
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return []
        if text.startswith("["):
            try:
                parsed = json.loads(text)
            except (TypeError, ValueError) as exc:
                raise ReconciliationError("An account array cell must contain valid JSON") from exc
            if not isinstance(parsed, list):
                raise ReconciliationError("An account array cell must contain a JSON array")
            return split_user_ids(parsed)
        return sorted(set(part for part in re.split(r"[,;|\s]+", text) if part))
    if isinstance(value, (list, tuple, set, frozenset)):
        return sorted({item for group in value for item in split_user_ids(group)})
    raise ReconciliationError("Account identifiers must be scalars or arrays")


def normalize_ems2_permissions(
    body: Any,
    entity_app_mapping: Mapping[str, str],
    *,
    role_mapping: Mapping[str, Mapping[str, str]] | None = None,
    subject_mapping: Mapping[str, Mapping[str, str]] | None = None,
    action_mapping: Mapping[str, Mapping[str, str]] | None = None,
) -> dict[str, Any]:
    """Normalize an EMS2 entitlementList object into mapped user permission sets.

    EMS2 counts must match the received rows. Every row needs consistent entity
    context for its role, subject, and action. Unknown entities are errors.
    Assignments here are derived from permission rows; empty roles cannot be
    recovered from this endpoint alone.
    """
    response = _object(body, "EMS2 response")
    users: dict[str, Any] = {}
    for raw_user, raw_result in response.items():
        user_ids = split_user_ids(raw_user)
        if len(user_ids) != 1:
            raise ReconciliationError("An EMS2 response key must identify one account")
        user = user_ids[0]
        result = _object(raw_result, "EMS2 account result")
        rows = _array(result.get("entitlements"), "EMS2 entitlements")
        count = result.get("count")
        if isinstance(count, bool) or not isinstance(count, int) or count != len(rows):
            raise ReconciliationError("EMS2 count is missing or does not match the received entitlement rows")
        grants: set[tuple[str, str, str, str]] = set()
        entities: set[str] = set()
        for raw_row in rows:
            row = _object(raw_row, "EMS2 entitlement row")
            subject = _object(row.get("subject"), "EMS2 subject")
            role = _object(row.get("role"), "EMS2 role")
            action = _object(row.get("action"), "EMS2 action")
            contexts = [
                _name(_object(part.get("entity"), "EMS2 entity").get("name"), "EMS2 entity name")
                for part in (subject, role, action)
            ]
            if len(set(contexts)) != 1:
                raise ReconciliationError("EMS2 permission row has conflicting entity contexts")
            entity = contexts[0]
            if entity not in entity_app_mapping:
                raise ReconciliationError("EMS2 response contains an entity without an application mapping")
            app = _name(entity_app_mapping[entity], "mapped CES application")
            mapped_role = _map_name(_name(role.get("name"), "EMS2 role name"), entity, role_mapping, "role")
            feature = _map_name(
                _name(subject.get("name"), "EMS2 subject name"), entity, subject_mapping, "subject"
            )
            mapped_action = _map_name(
                _name(action.get("name"), "EMS2 action name"), entity, action_mapping, "action"
            )
            grants.add((app, mapped_role, feature, mapped_action))
            entities.add(entity)
        normalized = {
            "grants": _records(grants),
            "assignments": _records((app, role) for app, role, _, _ in grants),
            "effective_permissions": _records((app, feature, action) for app, _, feature, action in grants),
            "source_entities": sorted(entities),
            "assignment_source": "PERMISSION_ROWS_ONLY",
            "data_scope_assessment": "UNASSESSED",
        }
        if user in users:
            raise ReconciliationError("EMS2 response contains duplicate normalized account identifiers")
        users[user] = normalized
    return {"users": users}


def normalize_ces_catalog(body: Any, app: str) -> dict[str, Any]:
    """Normalize a CES application entitlement catalog, including membership.

    Catalog membership is retained separately from effective-user responses.
    The caller must establish that the entire application catalog was received.
    """
    app = _name(app, "CES application")
    rows = _array(body, "CES application catalog")
    grants: set[tuple[str, str, str, str]] = set()
    assignments: set[tuple[str, str, str]] = set()
    entitlements: set[str] = set()
    users: set[str] = set()
    for raw_row in rows:
        row = _object(raw_row, "CES entitlement")
        entitlement = _name(row.get("entitlement_name"), "CES entitlement name")
        if entitlement in entitlements:
            raise ReconciliationError("CES catalog contains duplicate entitlement names within one application")
        entitlements.add(entitlement)
        permissions = _array(row.get("role_entitlements"), "CES role_entitlements")
        if "user_ids" not in row or row["user_ids"] is None:
            raise ReconciliationError("CES catalog is missing its user_ids membership field")
        members = split_user_ids(row["user_ids"])
        users.update(members)
        assignments.update((user, app, entitlement) for user in members)
        for raw_permission in permissions:
            permission = _object(raw_permission, "CES catalog permission")
            feature = _name(permission.get("feature"), "CES feature")
            action = _name(permission.get("action"), "CES action")
            grants.add((app, entitlement, feature, action))
    return {
        "app": app,
        "grants": _records(grants),
        "assignments": _records(assignments),
        "users": sorted(users),
        "entitlements": sorted(entitlements),
        "membership_source": "APPLICATION_CATALOG",
    }


def normalize_ces_user(body: Any, app: str, *, expected_user: str | None = None) -> dict[str, Any]:
    """Normalize CES effective-user grants without inventing role attribution.

    An explicit empty response means no returned user record. A different user
    or application context, omitted fields, and ambiguous duplicate records are
    errors. Data sections are preserved but receive no equivalence claim.
    """
    app = _name(app, "CES application")
    if expected_user is not None:
        expected_ids = split_user_ids(expected_user)
        if len(expected_ids) != 1:
            raise ReconciliationError("Expected CES account must identify one account")
        expected_user = expected_ids[0]
    rows = _array(body, "CES effective-user response")
    users: dict[str, Any] = {}
    for raw_row in rows:
        row = _object(raw_row, "CES effective-user record")
        context = _object(row.get("user_data"), "CES user_data")
        actual_app = _name(context.get("app_name"), "CES user application")
        identities = split_user_ids(context.get("user_id"))
        if len(identities) != 1:
            raise ReconciliationError("CES user_data must identify one account")
        user = identities[0]
        if actual_app != app or (expected_user is not None and user != expected_user):
            raise ReconciliationError("CES effective response does not match the requested account and application")
        if user in users:
            raise ReconciliationError("CES effective response contains duplicate account records")
        entitlements = _object(row.get("entitlements"), "CES entitlements")
        names = _array(entitlements.get("entitlement_name"), "CES entitlement_name")
        assignments = {(app, _name(name, "CES assigned entitlement")) for name in names}
        permissions = _array(entitlements.get("role_entitlements"), "CES effective role_entitlements")
        effective: set[tuple[str, str, str]] = set()
        for raw_permission in permissions:
            permission = _object(raw_permission, "CES effective permission")
            effective.add((app, _name(permission.get("feature"), "CES feature"),
                           _name(permission.get("action"), "CES action")))
        users[user] = {
            "assignments": _records(assignments),
            "effective_permissions": _records(effective),
            "data_scope": {
                key: entitlements[key]
                for key in ("data_policies", "data_profiles", "data_entitlements")
                if key in entitlements
            },
            "role_provenance": "UNAVAILABLE",
            "data_scope_assessment": "UNASSESSED",
        }
    return {"app": app, "users": users}


def compare_sets(baseline: Any, candidate: Any) -> dict[str, Any]:
    """Compare explicit sets of scoped string records and retain all outcomes.

    Empty or unavailable denominators never produce a 100 percent result.
    Matched rows remain available for audit while the differences contain only
    missing and additional rows. Preserved content and exact equality differ.
    """
    def validate(rows: Any) -> set[tuple[str, ...]]:
        if not isinstance(rows, (list, tuple, set, frozenset)):
            raise ReconciliationError("Compared records must be explicit collections")
        values: set[tuple[str, ...]] = set()
        width: int | None = None
        for row in rows:
            if not isinstance(row, (list, tuple)) or not row:
                raise ReconciliationError("Each compared record must be a nonempty sequence of names")
            record = tuple(_name(part, "comparison name") for part in row)
            if width is not None and len(record) != width:
                raise ReconciliationError("Compared records have inconsistent identity dimensions")
            width = len(record)
            values.add(record)
        return values

    old = validate(baseline)
    new = validate(candidate)
    if old and new and len(next(iter(old))) != len(next(iter(new))):
        raise ReconciliationError("Baseline and candidate use different identity dimensions")
    matched = old & new
    missing = old - new
    additional = new - old
    return {
        "status": "EMPTY" if not old and not new else "DIFFERENT" if missing or additional else "PASS",
        "baseline_count": len(old),
        "candidate_count": len(new),
        "matched_count": len(matched),
        "missing_count": len(missing),
        "additional_count": len(additional),
        "coverage_percent": round(100 * len(matched) / len(old), 6) if old else None,
        "preserved": not missing,
        "equal": old == new,
        "matched": _records(matched),
        "missing": _records(missing),
        "additional": _records(additional),
        "differences": {"missing": _records(missing), "additional": _records(additional)},
    }
