"""The Workbench profile of Open Knowledge Format v0.2.

These schemas use the same bounded JSON Schema subset as provider operations.
Unknown document fields remain available for OKF extensions.
"""

from __future__ import annotations

from copy import deepcopy


STATES = ["candidate", "investigated", "verified", "published", "contested", "stale", "superseded"]
TEXT = {"type": "string", "minLength": 1}
IDENTIFIER = {"type": "string", "minLength": 1, "maxLength": 80}
HASH = {"type": "string", "minLength": 64, "maxLength": 64}


def object_schema(properties, required=None, *, extensions=True):
    return {"type": "object", "properties": deepcopy(properties),
            "required": list(properties) if required is None else required,
            "additionalProperties": extensions}


def array_schema(items, minimum=0):
    return {"type": "array", "items": deepcopy(items), "minItems": minimum}


SOURCE = object_schema({"resource": TEXT, "revision": TEXT, "sha256": HASH})
ATTESTATION = object_schema({"by": TEXT, "at": TEXT})
COMMON = {
    "type": TEXT, "id": IDENTIFIER, "version": {"type": "integer", "minimum": 1},
    "owner": TEXT, "governance_state": {"type": "string", "enum": STATES},
    "status": {"type": "string", "enum": ["draft", "stable", "deprecated"]},
    "sources": array_schema(SOURCE, 1), "generated": ATTESTATION,
    "verified": array_schema(ATTESTATION),
}
MEASURE = object_schema({
    "metric": TEXT,
    "operator": {"type": "string", "enum": ["equals", "at_least", "at_most", "less_than", "greater_than"]},
    "value": {"type": "number"}, "unit": TEXT,
})
CRITERION = object_schema({"id": IDENTIFIER, "given": TEXT, "when": TEXT, "then": TEXT,
                           "measure": MEASURE})
DOMAIN_FIELDS = {
    "KnowledgeTopic": {"classification": TEXT, "scope": TEXT, "summary": TEXT,
                       "related": array_schema(TEXT), "open_questions": array_schema(TEXT)},
    "Requirement": {"description": TEXT, "rationale": TEXT,
                    "acceptance_criteria": array_schema(CRITERION, 1)},
    "Architecture": {"scope": TEXT, "components": array_schema(TEXT, 1),
                     "interfaces": array_schema(TEXT), "dependencies": array_schema(TEXT),
                     "decisions": array_schema(TEXT)},
    "Decision": {"context": TEXT, "options": array_schema(TEXT, 2), "decision": TEXT,
                 "rationale": TEXT, "consequences": array_schema(TEXT, 1)},
    "RepositoryProfile": {"repository_id": IDENTIFIER, "purpose": TEXT, "scope": TEXT,
                          "responsibility": TEXT, "components": array_schema(TEXT, 1),
                          "contracts": array_schema(TEXT), "dependencies": array_schema(TEXT),
                          "languages": array_schema(TEXT, 1), "entry_points": array_schema(TEXT),
                          "validation_commands": array_schema(TEXT)},
    "GovernanceFinding": {
        "subject": object_schema({"id": IDENTIFIER, "version": {"type": "integer", "minimum": 1}}),
        "category": TEXT,
        "severity": {"type": "string", "enum": ["info", "warning", "error"]},
        "evidence": array_schema(SOURCE, 1), "proposed_action": TEXT,
        "resolution": {"type": "string", "enum": ["open", "resolved", "deferred"]},
    },
}
HEADINGS = {
    "KnowledgeTopic": ["Scope", "Summary", "Documented knowledge", "Connections",
                       "Evidence limits", "Open questions"],
    "Requirement": ["Description", "Rationale", "Acceptance criteria"],
    "Architecture": ["Scope", "Components", "Interfaces", "Dependencies", "Decisions"],
    "Decision": ["Context", "Options", "Decision", "Rationale", "Consequences"],
    "RepositoryProfile": ["Purpose", "Scope", "Responsibility", "Components", "Contracts",
                          "Dependencies", "Languages", "Entry points", "Validation commands"],
    "GovernanceFinding": ["Subject", "Evidence", "Proposed action", "Resolution"],
}
DOCUMENT_SCHEMAS = {}
for kind, fields in DOMAIN_FIELDS.items():
    properties = {**COMMON, **fields, "type": {"type": "string", "enum": [kind]}}
    DOCUMENT_SCHEMAS[kind] = {"title": f"Workbench {kind} (OKF v0.2)", **object_schema(properties)}

RAW_RECORD = object_schema({
    "id": IDENTIFIER, "resource": TEXT, "revision": TEXT, "sha256": HASH,
    "ingested_at": TEXT,
    "classification": {"type": "string", "enum": ["business", "architecture", "decision",
                       "implementation", "deployment", "verification", "unknown", "mixed"]},
    "snapshot": TEXT,
}, ["id", "resource", "revision", "sha256", "ingested_at", "classification"])
RAW_MANIFEST_SCHEMA = object_schema({"schema_version": {"type": "integer", "enum": [1]},
                                     "sources": array_schema(RAW_RECORD)}, extensions=False)
AUDIT_EVENT_SCHEMA = object_schema({
    "id": IDENTIFIER, "item_id": IDENTIFIER, "item_version": {"type": "integer", "minimum": 1},
    "actor": TEXT, "at": TEXT,
    "action": {"type": "string", "enum": ["transition", "approval"]},
    "from_state": {"type": "string", "enum": ["untracked", *STATES]},
    "to_state": {"type": "string", "enum": STATES},
    "content_sha256": HASH, "reason": TEXT, "evidence": array_schema(SOURCE, 1),
})

SCHEMA_FILES = {
    "knowledge-topic.schema.json": DOCUMENT_SCHEMAS["KnowledgeTopic"],
    "requirement.schema.json": DOCUMENT_SCHEMAS["Requirement"],
    "architecture.schema.json": DOCUMENT_SCHEMAS["Architecture"],
    "decision.schema.json": DOCUMENT_SCHEMAS["Decision"],
    "repository-profile.schema.json": DOCUMENT_SCHEMAS["RepositoryProfile"],
    "governance-finding.schema.json": DOCUMENT_SCHEMAS["GovernanceFinding"],
    "raw-manifest.schema.json": RAW_MANIFEST_SCHEMA,
    "audit-event.schema.json": AUDIT_EVENT_SCHEMA,
}
