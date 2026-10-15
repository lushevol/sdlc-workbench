---
standard: ASD-STE100
automated_check: PENDING
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
- Automated checks do not check the complete approved dictionary or grammar rules.
---

# Repository onboarding assessment

Replace placeholders with inspected facts or explicit unknowns.
Set automated status from actual checks; record results and limits below.

- Repository ID: `unknown`
- Checkout root: `REVIEW_REQUIRED`
- Git revision: `unknown`
- Checkout changes: `unknown`
- Assessment mode: `assess | draft | verify`
- Dependency profile: `external-dependencies/1`
- Evidence validation: `not-run | passed | failed`
- Assessment date: `REVIEW_REQUIRED`
- Repository documentation directory: `not-requested | repository-relative directory`

## Purpose and ownership

Describe owned responsibilities, consumed interfaces, non-goals, and unknowns.
Bind each material claim to `repo-onboarding.json`.
Separate observed implementation from approved intent.
Owner: unknown until source evidence identifies the responsible owner.

## Critical dependency summary

Place critical relationships and consequential unknowns here before general readiness.
Derive priority from evidenced workflow consequences; preserve inferred or unknown business impact.
Use local dependency IDs from `repo-onboarding.json` to connect details, claims, and findings.
An observed protocol does not establish observed permissions, activation, or production connectivity.

| Dependency ID and workflow | Failure or permission consequence | Evidence status and limit | Owner | Next action |
| --- | --- | --- | --- | --- |
| REVIEW_REQUIRED | REVIEW_REQUIRED | unknown: REVIEW_REQUIRED | unknown | REVIEW_REQUIRED |

## Deployables and components

| Candidate identity | Responsibility | Entrypoints and source patterns | Claim IDs | Status |
| --- | --- | --- | --- | --- |
| REVIEW_REQUIRED | REVIEW_REQUIRED | REVIEW_REQUIRED | REVIEW_REQUIRED | unknown |

## Provided interfaces and permissions

Record each identified method/path, GraphQL field, RPC method, stream, webhook, or callback operation.
Trace global, route, method, resolver, interceptor, gateway, and deployment controls where available.
Keep network reachability, CORS, CSRF, authentication, and authorization distinct.
Missing authorization evidence means unknown restrictions.

| Dependency ID and operation | Exposure boundary | Authentication and authorization | Enforcement and conditions | Claim IDs and field limits |
| --- | --- | --- | --- | --- |
| REVIEW_REQUIRED | unknown | unknown | unknown | REVIEW_REQUIRED |

## Outbound APIs and call conditions

Trace callers through startup, request, UI action, message, schedule, transaction, retry, manual, or shutdown paths.
Preserve guards, feature flags, profiles, timezones, endpoint substitutions, and unresolved runtime frequency.
For gRPC, include streaming mode, deadlines, interceptors, metadata, transport security, and target resolution.

| Dependency ID and remote operation | Caller and trigger | Timing and conditions | Configuration and failure behavior | Claim IDs and field limits |
| --- | --- | --- | --- | --- |
| REVIEW_REQUIRED | unknown | unknown | unknown | REVIEW_REQUIRED |

## Messaging and managed events

Include Kafka, MQ/JMS, Solace, AMQP, managed event services, and other inspected messaging technologies.
Keep separate broker bindings, namespaces, destinations, subscriptions, and consumer groups distinct.
Record payload/schema references, permissions, delivery behavior, acknowledgements, retries, and dead-letter handling when supported.

| Dependency ID and role | Broker binding and destination | Activation and routing | Delivery, access, and failure behavior | Claim IDs and field limits |
| --- | --- | --- | --- | --- |
| REVIEW_REQUIRED | unknown | unknown | unknown | REVIEW_REQUIRED |

## Databases and data services

Include database engines, caches, search/vector stores, warehouses, and other inspected data services.
Keep migrations, schema declarations, application datasource use, and successful execution separate.

| Dependency ID and datasource | Engine and data objects | Read/write effects and callers | Transactions, access, and failure behavior | Claim IDs and field limits |
| --- | --- | --- | --- | --- |
| REVIEW_REQUIRED | unknown | unknown | unknown | REVIEW_REQUIRED |

## Configuration dependencies

Trace files, imports, nonsecret key names, profiles, arguments, environment references, and external providers to their consumers.
Record defaults, required inputs, override precedence, loading timing, and unresolved substitutions.
Record secret reference mechanisms without copying credentials, secret values, or credential file contents.

| Dependency ID and source | Safe keys and consumers | Profiles, precedence, and loading | Required inputs and unknowns | Claim IDs and field limits |
| --- | --- | --- | --- | --- |
| REVIEW_REQUIRED | unknown | unknown | unknown | REVIEW_REQUIRED |

## Other external dependencies

Include identity, LDAP, trust, storage, network, platform, scheduling, observability, frontend, business providers, and engineering delivery.
Keep runtime, configuration, build, test, deployment, and optional scopes distinct.
For LDAP, inspect bind method, TLS, search/base references, group mapping, and downstream authorization consumers.
Omit directory entries, user identifiers, bind credentials, and sensitive search values.

| Dependency ID and family | Asset or peer and operation | Phase, trigger, and conditions | Access, configuration, and consequence | Claim IDs and field limits |
| --- | --- | --- | --- | --- |
| REVIEW_REQUIRED | unknown | unknown | unknown | REVIEW_REQUIRED |

## Detailed relationship records

Repeat this card for each relationship; use it when summary tables cannot hold the required details.
Follow the skill's evidence contract for exact structured fields.
Bind each attribute to claim IDs and its own evidence status.
Use explicit reasons for unknown, inferred, or conflicting attributes.
Do not transfer certainty between attributes or duplicate the claim citation system.

### Dependency `REVIEW_REQUIRED`

| Detail | Value or explicit unknown | Evidence status | Supporting claim IDs and reason |
| --- | --- | --- | --- |
| Component, peer/asset, protocol, operation/resource, direction | unknown | unknown | REVIEW_REQUIRED |
| Phase, environment/profile, optionality, activation | unknown | unknown | REVIEW_REQUIRED |
| Caller, trigger, timing, guards | unknown | unknown | REVIEW_REQUIRED |
| Interaction pattern and data effects | unknown | unknown | REVIEW_REQUIRED |
| Authentication, authorization, network restrictions, enforcement | unknown | unknown | REVIEW_REQUIRED |
| Configuration sources, safe keys, consumers, defaults, precedence | unknown | unknown | REVIEW_REQUIRED |
| Failure, timeout, retry/backoff, fallback, delivery behavior | unknown | unknown | REVIEW_REQUIRED |
| Criticality, consequence, rationale | unknown | unknown | REVIEW_REQUIRED |
| Owner, unresolved questions, next action | unknown | unknown | REVIEW_REQUIRED |
| Applicable family details | unknown | unknown | REVIEW_REQUIRED |

Split rows when attributes have different evidence states or supporting claims.
Keep family details explicit, including API permissions, outbound activation, messaging bindings, and datasource/configuration relationships.
If no critical relationships are identified, record the inspected scope and evidence limit instead of implying production absence.

## Dependency family coverage

Review every family, including `other`, before completing the assessment.
Use `inspected`, `not-observed`, `unknown`, or `out-of-scope`, with an inspected scope and reason.
`not-observed` means no relationship was found within that scope; it does not establish absence from production.
Keep coverage dispositions separate from relationship attribute evidence statuses.
Replace all placeholders and record exclusions, unavailable inputs, and follow-up actions.

| Family | Disposition | Inspected scope and exclusions | Reason, evidence limits, and next action |
| --- | --- | --- | --- |
| `api` | unknown | REVIEW_REQUIRED | REVIEW_REQUIRED |
| `messaging` | unknown | REVIEW_REQUIRED | REVIEW_REQUIRED |
| `managed-events` | unknown | REVIEW_REQUIRED | REVIEW_REQUIRED |
| `data` | unknown | REVIEW_REQUIRED | REVIEW_REQUIRED |
| `identity` | unknown | REVIEW_REQUIRED | REVIEW_REQUIRED |
| `trust` | unknown | REVIEW_REQUIRED | REVIEW_REQUIRED |
| `configuration` | unknown | REVIEW_REQUIRED | REVIEW_REQUIRED |
| `storage` | unknown | REVIEW_REQUIRED | REVIEW_REQUIRED |
| `network` | unknown | REVIEW_REQUIRED | REVIEW_REQUIRED |
| `platform` | unknown | REVIEW_REQUIRED | REVIEW_REQUIRED |
| `scheduling` | unknown | REVIEW_REQUIRED | REVIEW_REQUIRED |
| `observability` | unknown | REVIEW_REQUIRED | REVIEW_REQUIRED |
| `frontend` | unknown | REVIEW_REQUIRED | REVIEW_REQUIRED |
| `business-provider` | unknown | REVIEW_REQUIRED | REVIEW_REQUIRED |
| `delivery` | unknown | REVIEW_REQUIRED | REVIEW_REQUIRED |
| `other` | unknown | REVIEW_REQUIRED | REVIEW_REQUIRED |

## Readiness

| Dimension | Status | Claim IDs | Gap and required action |
| --- | --- | --- | --- |
| Repository identity | missing | REVIEW_REQUIRED | REVIEW_REQUIRED |
| Purpose and ownership | missing | REVIEW_REQUIRED | REVIEW_REQUIRED |
| Agent instructions | missing | REVIEW_REQUIRED | REVIEW_REQUIRED |
| Build and tests | missing | REVIEW_REQUIRED | REVIEW_REQUIRED |
| Interface contracts | missing | REVIEW_REQUIRED | REVIEW_REQUIRED |
| Functional mapping | missing | REVIEW_REQUIRED | REVIEW_REQUIRED |
| Dependency visibility | missing | REVIEW_REQUIRED | REVIEW_REQUIRED |
| Evidence governance | missing | REVIEW_REQUIRED | REVIEW_REQUIRED |

## Findings

| ID and priority | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| REVIEW_REQUIRED | REVIEW_REQUIRED | REVIEW_REQUIRED | unknown | REVIEW_REQUIRED |

Separate P0 blockers, P1 improvements, and P2 options through the priority column.
Write proposed acceptance criteria as measurable Gherkin scenarios supported by the finding.
Name the condition, action, observable result, and required limit.
Do not invent business thresholds.

## Conflicts and unresolved questions

Record both citations for conflicts.
Name the required decision and its known or unknown owner.

## Proposed changes awaiting review

| File and record ID | Supporting claims | Review state | Review owner | Unknown fields |
| --- | --- | --- | --- | --- |
| REVIEW_REQUIRED | REVIEW_REQUIRED | review_required | unknown | REVIEW_REQUIRED |

List only files actually staged.
Keep review metadata outside canonical catalog envelopes.

## Checks and execution limits

| Check | Actual result | Evidence or reason omitted |
| --- | --- | --- |
| Static inventory | not-run | REVIEW_REQUIRED |
| Evidence helper | not-run | REVIEW_REQUIRED |
| Dependency profile and family coverage | not-run | REVIEW_REQUIRED |
| Isolated catalog validation | not-run | REVIEW_REQUIRED |
| Target build and tests | not-run | REVIEW_REQUIRED |
| Writing checks | not-run | REVIEW_REQUIRED |
| Repository topic links and portable evidence | not-requested | REVIEW_REQUIRED |

Record inventory omissions, revision gaps, unexecuted checks, and unsupported runtime conclusions.
A passing static check does not establish production behavior or business approval.

## Repository topic documents

Include this section only when the user requested documents inside the repository.
List the topic index, portable evidence register, provenance, and source baseline.
Keep the original validated report in external staging.
Record validation before the documentation commit and any later baseline-byte review separately.
Generated documents remain candidates until the required knowledge review occurs.
