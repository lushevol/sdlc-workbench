"""Build scoped CES contract derivatives from retained sources; never call CES."""

from collections import defaultdict
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

import yaml


ROOT = Path(__file__).resolve().parents[3]
LIBRARY = ROOT / ".agents/skills/ces-domain-capability"
REVIEW = Path(__file__).with_name("ces-standard-source-review-20261123.json")
maps = defaultdict(dict)


def token(value, category):
    if value == "":
        return value
    entries = maps[category]
    if value not in entries:
        entries[value] = f"{category}-{len(entries) + 1:03d}"
    return entries[value]


def sanitize(value, field=""):
    if isinstance(value, dict):
        return {token(key, "group") if field in ("data_policies", "data_profiles") else key:
                sanitize(item, key) for key, item in value.items()}
    if isinstance(value, list):
        return [sanitize(item, field) for item in value]
    if isinstance(value, str):
        category = {
            "app_name": "application", "appName": "application", "itam_id": "itam",
            "user_id": "account", "user_ids": "account", "entitlement_name": "entitlement",
            "entitlementName": "entitlement", "feature": "feature", "featureName": "feature",
            "action": "action", "actionName": "action", "policy_owner": "owner",
            "data_profile_owner": "owner",
        }.get(field, "value")
        return token(value, category)
    return value


def write_json(relative, value):
    (LIBRARY / relative).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def observed_schema(value):
    if isinstance(value, list):
        return [observed_schema(item) for item in value]
    if not isinstance(value, dict):
        return value
    # Inspector requirements must not become claims of service-wide requiredness.
    return {key: observed_schema(item) for key, item in value.items()
            if key not in ("required", "minLength", "maxItems", "$id", "$schema")}


def build():
    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    source_keys = ("inventory", "http_sources", "assigned_role_fixture", "functional_profile_user_sources",
                   "canonical_candidate_references", "authentication_evidence", "limits")
    register = {key: deepcopy(review[key]) for key in source_keys}
    register["task_source_register"] = str(REVIEW.relative_to(ROOT))
    for source in register["http_sources"]:
        source.pop("path")
        source["source_lookup"] = {"inventory_path": review["inventory"]["path"],
                                   "inventory_sha256": review["inventory"]["sha256"],
                                   "locator": source["inventory_locator"]}
    register["standalone_limits"] = [
        "Workspace paths identify retained originals; they can be unavailable in standalone copies.",
        "Source hashes identify inspected bytes, not current deployment or business approval.",
        "Canonical references remain candidate/draft where recorded; no publication is implied.",
    ]
    write_json("Knowledge/sources.json", register)
    pairs = []
    for source in review["http_sources"]:
        raw = (ROOT / source["path"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == source["sha256"]
        example = yaml.safe_load(raw)["examples"][0]
        body = json.loads(example["response"]["body"]["data"])
        url = urlsplit(example["request"]["url"])
        parts = url.path.split("/")
        # /fmces/v1/entitlement/app/{itam}/{app}: indexes include the leading empty part.
        params = {"itam_id": token(parts[5], "itam"), "application": token(parts[6], "application")}
        effective = source["id"].startswith("effective-user")
        if effective:
            params["user_id"] = token(parts[8], "account")
        indexes = list(range(len(body)))
        if not effective:
            selectors = [lambda row: bool(row["user_ids"]) and bool(row["role_entitlements"]),
                         lambda row: not row["role_entitlements"], lambda row: not row["user_ids"]]
            indexes = sorted({next(i for i, row in enumerate(body) if predicate(row)) for predicate in selectors})
        selected = deepcopy([body[i] for i in indexes])
        nested_projections = []
        if not effective:
            for row_index, row in zip(indexes, selected):
                for field in ("user_ids", "role_entitlements"):
                    if len(row[field]) > 2:
                        nested_projections.append({"source_row_index": row_index, "field": field,
                                                   "original_length": len(row[field]), "selected_range": [0, 2]})
                        row[field] = row[field][:2]
        pair = {
            "id": source["id"],
            "operationId": "getEffectiveUser" if effective else "getApplicationCatalog",
            "applicability": {"environment": "UAT", "http_date": source["response"]["http_date"]},
            "request": {"method": example["request"]["method"], "origin": source["request"]["origin"],
                        "route_template": source["request"]["route_template"], "path_parameters": params,
                        "query_parameters": {}, "headers": {"Authorization": "Bearer <redacted>"}},
            "response": {"status": example["response"]["status"],
                         "headers": {"content-type": source["response"]["content_type"],
                                     "date": source["response"]["http_date"]},
                         "body": sanitize(selected), "body_complete": effective,
                         "original_record_count": len(body), "selected_record_indexes": indexes,
                         "nested_array_projections": nested_projections},
            "evidence": {"classification": "sanitized-observation", "source_id": source["id"],
                         "source_lookup": {"inventory_path": review["inventory"]["path"],
                                           "inventory_sha256": review["inventory"]["sha256"],
                                           "locator": source["inventory_locator"]},
                         "source_sha256": source["sha256"],
                         "source_revision": source["revision"], "request_locator": "/examples/0/request",
                         "response_locator": "/examples/0/response", "body_locator": "/examples/0/response/body/data",
                         "sanitization": "Stable typed aliases replace string values and dynamic group keys; empty strings/nulls remain.",
                         "selection_limit": "Catalog rows and large nested arrays are sampled; never infer absent assignments or grants from these subsets.",
                         "derivation": str(Path(__file__).relative_to(ROOT))},
        }
        write_json(f"Contracts/examples/{source['id']}-uat-pair.json", pair)
        pairs.append(pair)

    fixture = review["assigned_role_fixture"]
    raw = (ROOT / fixture["path"]).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == fixture["sha256"]
    write_json("Contracts/examples/assigned-role-body-fixture.json", {
        "id": "assigned-role-sdk-body", "operationId": "getAssignedRoles", "request": None,
        "response": {"status": None, "headers": None, "body": sanitize(json.loads(raw))},
        "evidence": {"classification": "sanitized-supplied-body-fixture", "source_path": fixture["path"],
                     "source_sha256": fixture["sha256"], "source_revision": fixture["revision"],
                     "locator": "/", "capture_date": None, "environment": None,
                     "limit": "No captured request, status, headers, or account identity accompanies this SDK body."},
    })

    schemas = {}
    for view, name in (("catalog", "CatalogObservation"), ("effective-user", "EffectiveUserObservation"),
                       ("assigned-role", "AssignedRoleObservation")):
        local = json.loads((LIBRARY / f"Contracts/schemas/{view}-response.schema.json").read_text())
        schema = observed_schema(local)
        schema["description"] = "Observed field shapes only. Requiredness, bounds, defaults and full service behavior remain unconfirmed."
        schema["x-local-inspection-schema"] = f"schemas/{view}-response.schema.json"
        schemas[name] = schema

    role_fields = schemas["AssignedRoleObservation"]["items"]["properties"]
    role_fields["appUID"]["type"] = "integer"
    role_fields["itamId"]["type"] = "null"
    for side in ("features", "actions"):
        fields = role_fields["featureActionDtos"]["items"]["properties"][side]["properties"]
        application = next(branch for branch in fields["applicationDto"]["anyOf"] if branch["type"] == "object")
        application["properties"]["appUID"]["type"] = "integer"
        fields["applicationDto"] = application

    paths = {}
    operations = (("getApplicationCatalog", "/fmces/v1/entitlement/app/{itam_id}/{application}", "CatalogObservation"),
                  ("getEffectiveUser", "/fmces/v1/entitlement/app/{itam_id}/{application}/user/{user_id}", "EffectiveUserObservation"),
                  ("getAssignedRoles", "/fmces/v1/entitlement/user/{user_id}", "AssignedRoleObservation"))
    for operation_id, path, schema_name in operations:
        names = [part[1:-1] for part in path.split("/") if part.startswith("{")]
        response = {"description": "Observed UAT 200 JSON bodies; schemas model captured shapes, not service-wide requiredness.",
                    "content": {"application/json": {"schema": {"$ref": f"#/components/schemas/{schema_name}"}}}}
        responses = {"200": response, "default": {"description": "No HTTP failure body or status contract was retained."}}
        if operation_id == "getAssignedRoles":
            responses = {"default": {"description": "SDK body fixture only. Its HTTP status and response media type were not retained.",
                                     "x-local-json-body-schema": {"$ref": f"#/components/schemas/{schema_name}"}}}
        paths[path] = {"get": {
            "operationId": operation_id, "summary": operation_id,
            "description": "Read-only source-derived subset. Confirm environment, permissions, completeness and current API revision before use.",
            "parameters": [{"name": name, "in": "path", "required": True,
                            "schema": {"type": "string"}, "description": "Bind to the exact source request; no default is supplied."}
                           for name in names],
            "responses": responses,
            "x-observed-client-authentication": "Bearer header; scopes, token requirements and unauthenticated behavior remain unknown.",
            "x-paired-cases": [f"examples/{p['id']}-uat-pair.json" for p in pairs if p["operationId"] == operation_id],
            "x-evidence-register": "../Knowledge/sources.json",
        }}
    contract = {
        "openapi": "3.1.0", "info": {"title": "CES inspected interface subset", "version": "capture-2026-11-03",
            "description": "Source-derived technical reference. HTTP captures and the SDK body fixture have distinct evidence classes. No service-wide guarantee is inferred."},
        "servers": [{"url": "https://fmcesuat.gdc.standardchartered.com", "description": "Observed UAT origin; select active task configuration explicitly."}],
        "paths": paths, "components": {"schemas": schemas, "securitySchemes": {
            "observedBearer": {"type": "http", "scheme": "bearer",
                "description": "Observed client configuration, not a complete authentication or permission contract."}}},
        "x-unresolved": ["Service-required fields, nullability outside captured values, defaults, enums and limits",
                         "Error contracts, authorization scopes and unauthenticated behavior", "Pagination and collection completeness",
                         "Assigned-role HTTP request/response pair", "function_entitlement wire location and empty representation"],
    }
    (LIBRARY / "Contracts/openapi.yaml").write_text(yaml.safe_dump(contract, sort_keys=False, allow_unicode=True), encoding="utf-8")


if __name__ == "__main__":
    build()
