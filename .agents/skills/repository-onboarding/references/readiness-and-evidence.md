# Readiness and evidence contract

## Readiness dimensions

Use `ready`, `partial`, `missing`, or `not-applicable` for each dimension.
Give a rationale, supporting claim IDs, evidence limits, and any required action.

| Dimension | Ready when |
| --- | --- |
| Repository identity | The checkout root and exact Git revision are available. |
| Purpose and ownership | Source corroborates repository responsibility and known ownership; non-goals and ownership gaps remain explicit. |
| Agent instructions | Applicable guidance supports navigation, constraints, and permitted verification commands. |
| Build and tests | Authorized execution and inspected assertions support reproducibility within a stated environment. |
| Interface contracts | Relevant provided and consumed interfaces have versioned source evidence. |
| Functional mapping | Inspected source connects business functions to components, entrypoints, and tests. |
| Dependency visibility | The dependency profile records critical relationships, permissions, activation, configuration, impact, coverage, and evidence limits. |
| Evidence governance | Claims retain exact citations, conflicts, revision limits, and review status. |

Documented commands without retained execution support at most `partial` build readiness.
A missing Git revision prevents the exact-evidence gate from passing.
For a non-code asset, explain each `not-applicable` choice.
Do not mark missing evidence as inapplicable merely to improve readiness.

Classify P0 blockers by their effect on the requested workflow.
Examples include unreadable source, unknown implementation ownership, or missing verification commands for code changes.
P1 improvements address consequential mapping or contract gaps.
P2 options need a demonstrated benefit before implementation.

Give every finding evidence, a consequence, an owner, and a next action.
Mark unknown owners explicitly.
Write measurable Gherkin scenarios for proposed acceptance criteria.

## Structured report

`repo-onboarding.json` is a skill-local staging report.
It is not a Workbench catalog or governed knowledge record.
Its `schema_version` remains the string `"1.0"`.
Canonical catalogs instead use integer `schema_version: 1`.
The following example shows the legacy envelope.
New assessments also select the external dependency profile defined below.

```json
{
  "schema_version": "1.0",
  "repository": {
    "id": "<confirmed repository ID or unknown>",
    "path": "<absolute local checkout root>",
    "revision": "<full 40-character or 64-character commit ID or unknown>"
  },
  "claims": [
    {
      "id": "CMP-001",
      "category": "component",
      "statement": "The inspected controller delegates the request to a service method.",
      "status": "observed",
      "evidence": [
        {"path": "<actual repository-relative source path>", "start_line": 12, "end_line": 18, "kind": "source"}
      ]
    },
    {
      "id": "DEP-002",
      "category": "external-dependency",
      "statement": "The configured listener might consume the declared topic.",
      "status": "inferred",
      "reason": "Configuration declares a topic, but no retained runtime observation establishes consumption.",
      "evidence": [
        {"path": "<actual configuration path>", "start_line": 20, "end_line": 24, "kind": "configuration"}
      ]
    },
    {
      "id": "GAP-003",
      "category": "verification",
      "statement": "Production consumption remains unknown.",
      "status": "unknown",
      "reason": "No applicable runtime observation or retained integration execution was available.",
      "evidence": []
    }
  ],
  "output_review": {
    "standard": "ASD-STE100",
    "automated_check": "PENDING",
    "asd_review": "PENDING",
    "reviewer": null,
    "reviewed_at": null,
    "limitations": [
      "Automated checks do not check the complete approved dictionary or grammar rules."
    ]
  }
}
```

Replace illustrative statements, paths, ranges, and revision before use.
Set `automated_check` from checks actually performed and record each check result in the assessment.
The evidence helper does not validate ASD metadata or semantic accuracy.
Only a complete writing review can set `asd_review: PASSED`.

## Claim and evidence rules

- `observed`: direct evidence supports a narrow source observation.
  This status establishes neither knowledge approval nor passing business execution.
- `inferred`: evidence supports a possible interpretation; include a nonempty string `reason`.
- `conflicting`: cite at least two disagreeing sources and explain the conflict in `reason`.
- `unknown`: supply a nonempty string `reason` instead of guessing.

Claims need unique nonempty IDs, categories, and statements.
Observed and inferred claims need evidence.
Allowed evidence kinds are `source`, `test`, `contract`, `configuration`, `documentation`, and `runtime-artifact`.
Paths use POSIX separators and identify regular files inside the checkout.
Use inclusive line ranges beginning at 1.
Symlinks and paths outside the checkout cannot supply this helper's evidence.

The helper checks that HEAD matches the report revision.
It checks each cited file's bytes against the committed Git blob.
Ignored, untracked, and changed evidence files fail validation.
Unrelated checkout changes can remain when all cited bytes match the declared commit.

Git checkout transformations, including automatic CRLF conversion, can prevent a byte match.
Record that limit and inspect committed bytes without running repository filters.
An unknown revision cannot pass exact evidence validation.
Record that limit while preserving the assessment.

Runtime observations outside the repository need their own retained identity and review in `assessment.md`.
The helper accepts only files within the repository.
A source citation to a test does not prove that its assertions passed.
A runtime artifact's presence does not authenticate its reported result.

## External dependency profile

Read [the dependency investigation guide](external-dependencies.md) before filling this profile.
Keep `schema_version: "1.0"` and add `dependency_profile: "external-dependencies/1"`.
Add `external_dependencies` and `dependency_coverage` arrays to the existing envelope.
Legacy reports remain valid without these three keys.
They do not pass the stronger dependency profile gate.
The helper rejects extension keys without the supported profile.

### Relationship records

Each dependency record requires the following fields.
Record separate relationships when direction, phase, operation, broker, or environment changes materially.
Do not merge identities solely because configured names match.

| Field | Contract |
| --- | --- |
| `id` | Unique nonempty local dependency ID. This ID creates no canonical service identity. |
| `family` | One family key from the coverage table below. |
| `direction` | `inbound`, `outbound`, `bidirectional`, or `local`, relative to the inspected component. |
| `phase` | `runtime`, `build`, `test`, `deployment`, or `configuration`. |
| `attributes` | Object containing every required attribute below. Additional attributes use the same evidence contract. |
| `review` | Object with nonempty `owner` and `next_action` strings. Use `unknown` for an unresolved owner. |

Every required attribute uses its own value, evidence status, and claim references.
Use a narrow value that its cited claims actually support.
An observed protocol cannot establish observed permission, invocation, or deployment.

| Required attribute | Required investigation content |
| --- | --- |
| `component` | Local deployable, module, job, or source boundary. |
| `peer` | Remote system or local asset; preserve unresolved identity and configuration bindings. |
| `protocol` | Transport, client mechanism, or format. |
| `operation` | Provided operation, remote call, publish/consume action, query, or resource interaction. |
| `environment` | Inspected profile, namespace, deployment scope, and unresolved environment inputs. |
| `activation` | Required or optional relationship, activation phase, profiles, flags, and defaults. |
| `trigger` | Caller and initiating request, event, startup, schedule, manual action, or shutdown. |
| `conditions` | Guards, conditional beans, transaction stages, feature checks, and other execution conditions. |
| `timing` | Schedule, sequence, frequency, deadlines, and unknown timezone or runtime timing. |
| `interaction` | Synchronous/asynchronous, request/reply, stream, and relevant data effects. |
| `authentication` | Identity mechanism and enforcement points. |
| `authorization` | Roles, scopes, entitlements, tenant/resource checks, ACLs, grants, and enforcement points. |
| `network_access` | Source-declared exposure, ingress, gateway, transport security, and network restrictions. |
| `configuration` | Paths, nonsecret keys, consumers, defaults, overrides, and external bindings. |
| `resilience` | Timeouts, retries, backoff, fallback, circuit breakers, delivery handling, and failure propagation. |
| `impact` | Affected workflow and evidenced consequences of failure or permission changes. |
| `criticality` | Qualitative priority, rationale, confidence, and business impact limits. |
| `family_details` | Applicable family-specific details from the investigation guide. |

The following JSON shows one attribute, not a complete dependency record.
Use the same structure for each required and additional attribute.

```json
{
  "authorization": {
    "value": null,
    "status": "unknown",
    "claim_ids": [],
    "reason": "The inspected files do not establish authorization enforcement."
  }
}
```

`value` must be a nonempty string for `observed`, `inferred`, and `conflicting` attributes.
An `unknown` attribute must use `value: null` and explain its missing evidence.
`claim_ids` must be an array of unique nonempty strings referencing existing claims.
An unknown attribute can have zero claim references.
Keep citations inside claims; inline dependency or coverage evidence is rejected.

| Attribute status | Required support |
| --- | --- |
| `observed` | At least one observed claim with evidence; no conflicting supporting claim. |
| `inferred` | At least one observed or inferred claim with evidence, plus an inference reason. |
| `conflicting` | A conflicting claim, or two distinct evidence-bearing observed/inferred claims with two distinct citations; include a conflict reason. |
| `unknown` | A nonempty reason and null value; optional claim references preserve relevant investigation context. |

Different evidence kinds for one path and line range do not create two distinct citations.
The helper checks support status and citation structure.
It cannot decide whether citations support the stated field or actually disagree.
Read the cited source and preserve contrary evidence during assessment.
Do not use a broad supporting claim to hide a field-specific uncertainty.

### Coverage records

Include exactly one coverage record for every family key below.
These coverage dispositions differ from claim and attribute evidence statuses.

| Family key | Family-specific details required when applicable |
| --- | --- |
| `api` | Operation, exposure boundary, contract/payload, version, permission enforcement, and caller activation. |
| `messaging` | Broker binding, destination, role, routing, group/subscription, payload/schema, delivery, acknowledgement, replay, and ACLs. |
| `managed-events` | Event service, resource binding, producer/consumer role, filtering, delivery, retry, and dead-letter controls. |
| `data` | Engine/client, datasource binding, objects, reads/writes, transactions, migrations, pools, failover, and permissions. |
| `identity` | Directory/provider binding, bind/token flow, transport, search/group mapping, and downstream authorization consumers. |
| `trust` | Secret/key/certificate reference, trust source, consumer, retrieval/rotation conditions, and access controls. |
| `configuration` | File/key/source, consumer, profile, precedence, required/default behavior, injection, and unresolved substitutions. |
| `storage` | Filesystem/object/transfer binding, paths or resource keys, read/write/watch actions, retention, and permissions. |
| `network` | Name resolution, discovery, proxy/gateway/mesh routing, activation, and network policy. |
| `platform` | Cloud/platform API or sidecar, resource, SDK operation, execution identity, and activation. |
| `scheduling` | Scheduler/workflow binding, job, cron/timezone, initiating event, lock/coordination, and failure handling. |
| `observability` | Telemetry/audit/control endpoint, sink/agent binding, activation, delivery, and effect of sink failure. |
| `frontend` | Remote module/CDN/desktop/browser binding, loading or interaction trigger, trust boundary, and failure handling. |
| `business-provider` | Provider function, operation/feed/notification, protocol, initiating workflow, and availability consequence. |
| `delivery` | Package/artifact/toolchain/native binary/build/test/deployment input, resolution source, phase, and reproducibility limits. |
| `other` | Explicit kind, local and external boundaries, operation, conditions, and reason no existing family fits. |

Each record requires `family`, `status`, `scope`, `reason`, and `dependency_ids`.
`scope` contains one or more nonempty inspected or excluded path descriptions.
`reason` explains the disposition and evidence limits as a nonempty string.
`dependency_ids` contains unique existing IDs from that family.
Every dependency must appear in its family's coverage record.

| Coverage status | Meaning and structural rule |
| --- | --- |
| `inspected` | The reviewed family has at least one recorded relationship. |
| `not-observed` | No relationship was found within the inspected scope; the dependency ID list must be empty. |
| `unknown` | Available scope cannot establish sufficient coverage; zero or more relationships can remain recorded. |
| `out-of-scope` | The stated boundary excludes this family; the dependency ID list must be empty. |

`not-observed` does not establish absence from production.
Report unavailable deployment settings and dynamic routing beside the affected relationships.
An empty dependency array needs justified coverage records for every family.
The helper checks structure and references, not completeness of discovery.
Put critical unknowns and unsupported permission conclusions in the assessment summary and findings.

## Findings and proposal review

For each proposal, record its file, record ID, supporting claims, review state, and known or unknown review owner.
Keep unconfirmed identifiers and fields in this review table rather than inventing catalog values.
Distinguish documented intent from source implementation and runtime observations.
Keep unresolved questions visible through later ingestion and governance review.
