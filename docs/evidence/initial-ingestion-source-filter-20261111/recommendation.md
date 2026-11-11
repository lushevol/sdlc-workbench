# Source selection before first knowledge ingestion

Date: 11 November 2026, Asia/Singapore.
Scope: proposed source selection for intended business-system behavior.
Reference: [exact user input](user-input.md#exact-user-input).

**Select source sections that explain intended behavior, its meaning, or necessary system responsibilities.**
Keep exceptions, conditions, and conflicting intent with each selected rule.
This document proposes a manual review method. It does not establish an implemented automatic filter.

## Topics to keep

These topic groups are recommendations within the existing knowledge boundary.
Use only groups that answer the project's actual questions.

| Topic | Content to select |
| --- | --- |
| Purpose and scope | Users, supported capabilities, business outcomes, and explicit exclusions. |
| Domain concepts and data | Terms, entities, identity meanings, relationships, states, and data lifecycle rules. |
| User and system workflows | Actors, triggers, preconditions, steps, outputs, alternative paths, and state transitions. |
| Business rules | Eligibility, validation, calculations, precedence, limits, and decision rules. |
| Security behavior | Authentication, permissions, sessions, tenant isolation, and denial behavior. |
| Contracts and integration | Requests, responses, events, defaults, errors, compatibility, and external system obligations. |
| Target architecture | Intended component responsibilities, trust boundaries, dependencies, and ownership of rules. |
| Failure and recovery | Retry, timeout, rollback, duplicate handling, recovery, and continuity requirements. |
| Quality constraints and decisions | Measurable performance, availability, audit, retention, accessibility, and behavior-relevant design rationale. |

Target architecture qualifies when it explains intended responsibilities and has a current consumer.
Generic framework descriptions do not qualify merely because the system uses that framework.
Historical proposals can support candidate intent. Their age or presence does not establish current applicability.

## Selection method

1. Define the system boundary and the questions the first ingestion must answer.
2. Inventory source paths, titles, dates, owners, revisions, and hashes. Identify duplicates and missing attachments.
3. Read each document's sections. Use filenames and keywords only to locate possible material.
4. Ask whether each section defines intended behavior, necessary domain meaning, or intended responsibilities.
5. Read the surrounding conditions, exceptions, tables, diagrams, and linked definitions before selecting a claim.
6. Record relevance separately from authority, intent status, and applicability. Investigate material conflicts before treating a rule as settled.
7. Derive connected candidate records from selected evidence. Keep the original sources and exact locators available.

For behavior claims, capture the actor, trigger, conditions, required result, and exceptions when the source supplies them.
Do not invent missing values to complete that description.
For definitions and architecture, capture the meaning or responsibility and the behavior it supports.
Keep system rules found inside operational procedures. Defer unrelated staffing, scheduling, and tool instructions.

## Selection decisions

These are proposed review labels. They are not new runtime fields or publication states.

| Decision | Use |
| --- | --- |
| KEEP | The relevant content describes intended behavior or necessary context. Preserve its actual intent status. |
| KEEP SECTIONS | The document mixes qualifying content with unrelated material. Select exact sections with necessary context. |
| EVIDENCE ONLY | The content describes implementation, deployment, incidents, measurements, or execution outcomes. |
| HOLD | Missing context, conflicting rules, or unclear applicability prevents a reliable interpretation. Record the reason and next evidence. |
| EXCLUDE FROM BATCH | The content is unrelated, duplicated, empty, or general tool instruction without relevant system semantics. |

Exclusion from this batch does not authorize deleting original documents or protected evidence.
Unknown authority does not erase relevant content. Preserve it as uncertain candidate material when its meaning remains clear.
Source selection does not approve the rule or publish knowledge.

Keep one selection index with these columns:

`source ID | revision/hash | section/locator | topic/question | decision | reason | intent status | applicability | authority | unresolved context`

Reference each retained payload once. Reuse its identity across all supported topics.

## Boundary examples

These examples illustrate selection. They are not claims about the project's actual policy.

| Source content | Decision and reason |
| --- | --- |
| A requirement defines when users lose access. | KEEP: it defines intended security behavior. |
| A release guide mixes configuration validation with staffing schedules. | KEEP SECTIONS: retain validation rules and their conditions. |
| A test report records observed latency. | EVIDENCE ONLY: a measurement cannot define the performance requirement. |
| A draft design proposes a recovery timeout. | KEEP as proposed intent, or HOLD if missing context prevents interpretation. |
| A tutorial lists framework installation commands. | EXCLUDE FROM BATCH unless a section supplies a relevant system contract. |

## Evidence and confidence

| Claim | Evidence | Class and confidence | Limit |
| --- | --- | --- | --- |
| Knowledge retains intent, workflows, contracts, and intended architecture. | [Knowledge standards](../../../knowledge/README.md#knowledge-standards) | Documented rule; high. The source states the permitted content. | This does not classify each raw document. |
| Actual implementation and observations remain separate from intent. | [Intent boundary](../../../knowledge/README.md#intended-behavior-and-independent-gaps) | Documented rule; high. The source states the separation. | Actual behavior needs its own evidence. |
| Selection must answer project questions and preserve source context. | [Scope](../../../.agents/skills/ingest-knowledge/references/workflow.md#1-define-the-scope) and [evidence reading](../../../.agents/skills/ingest-knowledge/references/workflow.md#3-read-and-trace-the-evidence) | Documented procedure; high. The workflow requires both checks. | Topic groups and decision labels above are recommendations. |

Inspected workspace HEAD: `86f686b9d01f8faedf805ee67df28dfb631ddbea`.
The following hashes identify the inspected guide bytes.

| Source | SHA-256 |
| --- | --- |
| `knowledge/README.md` | `abf81e780245f54d6e026c0e96e2b47a83004d3039539af05dd5d093ae423329` |
| `.agents/skills/ingest-knowledge/references/workflow.md` | `0340e6d98af51e6b486eedf9567256d9d97336e5f4db53e96074ac5c0916629f` |

No raw-document collection was supplied for full classification in this request.
No source registration, knowledge publication, semantic ingestion, or automatic filtering ran.
Authority and applicability remain source-specific review questions.

## Validation

Documentation checks: PASSED. Five local links and anchors resolve. Both source hashes match.
Diff checks found no whitespace errors.
ASD-STE100 review: PENDING. No complete dictionary or grammar certification was performed.
Runtime tests: NOT_RUN. This stage changes only this recommendation and its user-input reference.
