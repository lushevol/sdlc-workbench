# Illustrative invoice portal

Source ID: `SAMPLE-SRC-001`.
Revision label: `sample-v1`.
Source owner: unknown.
Authority: illustrative only.

This fictional context connects the catalog samples.
It defines no actual business requirement, approval, implementation, or execution result.
All names, identifiers, rules, and limits apply only to these examples.
Real artifacts require real sources and responsible owners.

## Product and identities

Customers use a portal to view their invoices.
Customer A owns invoice INV-001.
Customer B has no permission to view INV-001.
Customer A and customer B are authenticated for the sample access scenarios.

The illustrative repository ID is SAMPLE-REPO-001.
The illustrative service ID is SAMPLE-SVC-001.
The illustrative capability ID is SAMPLE-CAP-001.
The illustrative interface ID is SAMPLE-CONTRACT-001.

These IDs identify separate resources.
They establish no deployed relationship.

## Proposed behavior

Rule SAMPLE-RULE-001 permits an authenticated customer to view an owned invoice.
Rule SAMPLE-RULE-002 denies access when the customer lacks permission.
Rule SAMPLE-RULE-003 returns no invoice content after denied access.

Requirement SAMPLE-REQ-001 covers permitted access.
Criterion SAMPLE-AC-001 expects exactly one invoice with identifier INV-001.
Requirement SAMPLE-REQ-002 covers denied access.
Criterion SAMPLE-AC-002 expects zero invoices and the message "Access denied".

Requirement SAMPLE-NFR-001 covers response time.
Its proposed target is a 95th percentile of 500 milliseconds or less.
The illustrative load is 20 concurrent customers for 10 minutes after a two-minute warmup.
The timing interval starts when the service receives a request.
The timing interval ends when the service completes its response.
The measurement includes successful authorized invoice requests only.

These numbers are sample inputs. They require business review before real use.

## Proposed design

Architecture SAMPLE-ARCH-001 proposes a portal, an invoice service, and an invoice store.
The portal requests GET /invoices/{invoice_id} from the service.
The service checks identity and invoice access before returning invoice content.
The sample interface proposes HTTP 200 for permitted access and HTTP 403 for denied access.
These status codes are illustrative design choices.
The store remains a proposed internal dependency.

Decision SAMPLE-ADR-001 proposes a service access check for each invoice request.
The decision remains a draft.

## Verification and release

Test SAMPLE-TEST-001 will check SAMPLE-AC-001.
Test SAMPLE-TEST-002 will check SAMPLE-AC-002.
No test has executed.
No repository revision, deployment identity, log, or runtime observation is available.
All execution results remain NOT_RUN or null.

Release SAMPLE-REL-001 remains proposed.
No deployment, rollback, acceptance, or publication has occurred.

## Unknowns

| Question | Owner | Required next action |
| --- | --- | --- |
| Who owns invoice access policy? | unknown | Identify the business owner and obtain the policy source. |
| Can staff view customer invoices? | unknown | Obtain a reviewed rule before adding staff scenarios. |
| Which repository implements the service? | unknown | Inspect the registered repository at an exact revision. |
| Which retention period applies? | unknown | Obtain the applicable retention decision. |
| Which production objectives apply? | unknown | Obtain approved service objectives and measurement conditions. |

## Sample interpretation

Treat sample requirements and designs as proposed intent.
Treat hypothetical defects and incidents as writing examples.
Keep those examples separate from actual observations.
Use null for missing evidence and unknown for a missing owner.
Never infer approval, execution success, or production readiness from this context.
