---
{
  "type": "KnowledgeTopic",
  "id": "KT-settlement-trade-control-utilities",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-8505398b98d5f3ed15977b7e",
      "resource": "source:ratan-51358/RATAN - 51358/RATAN -Core Function/RATAN-Trade Control  C&A Exception/page.md",
      "revision": "sha256:c1d5374d6d690b605cfa0962e33d6ed19c06e80903fe859e9630791cf22de4b9",
      "sha256": "c1d5374d6d690b605cfa0962e33d6ed19c06e80903fe859e9630791cf22de4b9",
      "snapshot": "knowledge/evidence/sources/sha256/c1d5374d6d690b605cfa0962e33d6ed19c06e80903fe859e9630791cf22de4b9.md"
    },
    {
      "id": "SRC-ce242836905c47208a4b2edf",
      "resource": "source:ratan-51358/RATAN - 51358/RATAN -Core Function/RATAN-Trade Control  FX Replication/page.md",
      "revision": "sha256:2780da890b2c1794723fddb105599400435ee131c917cff877687cb6ee03fc8f",
      "sha256": "2780da890b2c1794723fddb105599400435ee131c917cff877687cb6ee03fc8f",
      "snapshot": "knowledge/evidence/sources/sha256/2780da890b2c1794723fddb105599400435ee131c917cff877687cb6ee03fc8f.md"
    },
    {
      "id": "SRC-331798d3d7455cae6c555f62",
      "resource": "source:ratan-51358/RATAN - 51358/RATAN -Core Function/RATAN-Trade Control  Option Expiry Blotter/page.md",
      "revision": "sha256:10dd09731fbd837022bebe18f107cbd8a7c33dc000239650860410423f825d45",
      "sha256": "10dd09731fbd837022bebe18f107cbd8a7c33dc000239650860410423f825d45",
      "snapshot": "knowledge/evidence/sources/sha256/10dd09731fbd837022bebe18f107cbd8a7c33dc000239650860410423f825d45.md"
    },
    {
      "id": "SRC-8191f91e74330dc48dec54d3",
      "resource": "source:ratan-51358/RATAN - 51358/RATAN -Core Function/RATAN-Trade Control  Trade Validation/page.md",
      "revision": "sha256:2f4fe2c7f6677d661043b2a9b5b5e3f034a894e40d53435ebdd2f93436dbad55",
      "sha256": "2f4fe2c7f6677d661043b2a9b5b5e3f034a894e40d53435ebdd2f93436dbad55",
      "snapshot": "knowledge/evidence/sources/sha256/2f4fe2c7f6677d661043b2a9b5b5e3f034a894e40d53435ebdd2f93436dbad55.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T01:54:24.358660+00:00"
  },
  "verified": [],
  "classification": "settlement",
  "scope": "Four separate Trade Control proposals covering C&A checks, FX replication, option fixing, and trade-rule exceptions.",
  "summary": "The selected pages describe proposed trade-control workflows with distinct scope, dependencies, and unresolved rules.",
  "related": [],
  "open_questions": [
    "Which C&A scope, PV rules, and output workflow were approved?",
    "Does the C&A batch schedule use GMT or UKT for its second batch?",
    "Which exact predicates govern FX replication to Razor?",
    "Which fixing tolerance, source selection, and timezone govern option expiry?",
    "Who reviewed and approved the trade-validation rules and publication status?"
  ],
  "standard": "ASD-STE100",
  "automated_check": "PASSED",
  "asd_review": "PENDING",
  "reviewer": null,
  "reviewed_at": null,
  "limitations": [
    "This isolated candidate has not completed schema validation or human publication review.",
    "The selected pages describe proposals; they do not establish current approval, implementation, or deployment."
  ]
}
---

# Trade-control proposals for C&A, FX replication, option fixing, and trade validation

## Scope

This draft preserves four separate control designs from the selected Trade Control pages.
They do not establish one shared policy or current implementation.

## Summary

The selected pages propose C&A PV review, eligible FX replication, option-fixing comparison, and trade-rule exception handling.
Each workflow has unresolved authority or predicate details.

## Documented knowledge

### WF-EV-058: C&A PV review

The design compares the latest trade version with its prior version using T-1 EOD market data.
Middle Office reviews the resulting PV difference for in-scope cancellations and amendments.
The linked Middle Office policy was not inspected; the June 2026 remediation target is not delivery evidence.
[Selected source, original lines 9–11](../../../../knowledge/evidence/sources/sha256/c1d5374d6d690b605cfa0962e33d6ed19c06e80903fe859e9630791cf22de4b9.md#L9-L11)

### WF-EV-059: C&A phases

MVP1 limits the proposal to SABRE FMRP Blade trades on the China Linear Rates desk.
MVP2 proposes broader FMRP booking-entity coverage and nine additional non-PV C&A checks.
Adoption and effective scope remain unverified.
[Selected source, original lines 13–16](../../../../knowledge/evidence/sources/sha256/c1d5374d6d690b605cfa0962e33d6ed19c06e80903fe859e9630791cf22de4b9.md#L13-L16)

### WF-EV-060: C&A dependencies and schedule

The design sends three daily PV batches for OVV and a separate EOD feed for previous-version trade PV.
The detailed batch table lists SGT, UKT, and UST windows; EOD uses UTC.
A separate MRB description names SGT, GMT, and UST, so the second-batch label conflicts within this page.
RATAN EOD supplies PV through OVV; RATAN ONE joins TDS3 trades and applies seven Middle Office rules.
The page leaves the user interface or report and user actions undecided.
The nine proposed non-PV checks and seven Middle Office rules describe different scopes; do not equate them.
[Selected source, original lines 26–41](../../../../knowledge/evidence/sources/sha256/c1d5374d6d690b605cfa0962e33d6ed19c06e80903fe859e9630791cf22de4b9.md#L26-L41)

### WF-EV-061: FX replication

The proposal filters Rates-desk Murex FX cash trades in real time before sending eligible trades to Razor for settlement.
It says users can inspect and modify rules in the MO Rules blotter.
The selected view does not include the rule predicates or a complete eligibility table.
[Selected source, original lines 9–11](../../../../knowledge/evidence/sources/sha256/2780da890b2c1794723fddb105599400435ee131c917cff877687cb6ee03fc8f.md#L9-L11), [selected line 15](../../../../knowledge/evidence/sources/sha256/2780da890b2c1794723fddb105599400435ee131c917cff877687cb6ee03fc8f.md#L15), [selected line 55](../../../../knowledge/evidence/sources/sha256/2780da890b2c1794723fddb105599400435ee131c917cff877687cb6ee03fc8f.md#L55)

### WF-EV-062: Option expiry and exercise fixing

The proposal checks published fixing indices against manually applied TP rates each day.
The fixing cut determines whether rates come from MDS or Trading Desk Voice Cuts.
Tolerance logic depends on fixing type; the page proposes a blotter for trades expiring Today and a comparison summary for Trade Control.
Tolerance values, source selection details, and the timezone for Today remain unknown.
[Selected source, original lines 9–17](../../../../knowledge/evidence/sources/sha256/10dd09731fbd837022bebe18f107cbd8a7c33dc000239650860410423f825d45.md#L9-L17)

### WF-EV-063: Trade-rule validation

After receiving a trade from TDS3, RATAN builds trade facts and checks predefined rules.
It records violations in the Ratan Exception Platform for Trade Review.
When no rule matches, the workflow closes any prior-version exception.
When a rule matches, it closes the prior-version exception and creates one for the current version.
The result appears in the exception blotter.
The review table is blank; its instruction says to set status to Published after review.
[Selected source, original lines 3–17](../../../../knowledge/evidence/sources/sha256/2f4fe2c7f6677d661043b2a9b5b5e3f034a894e40d53435ebdd2f93436dbad55.md#L3-L17)

## Connections

This trade-rule workflow is distinct from cashflow ID and business-version duplicate checks in the existing cashflow identity candidate.
The selected page does not define a cashflow visibility gate or trade-confirmation policy.

## Evidence limits

The selected views include only the assigned source ranges.
The linked C&A policy, diagrams, full FX rules, fixing configuration, and execution evidence were not inspected.
The C&A schedule labels conflict within the selected page; preserve both until an owner resolves the difference.
Source authority, current approval, implementation, and deployment remain unverified.

## Open questions

Owner: unknown.

- Which C&A scope, rule set, and user output were approved?
- Which timezone applies to the second C&A PV batch: GMT or UKT?
- Which exact eligibility predicates govern FX replication?
- Which fixing thresholds, rate-source selection, and timezone govern option expiry?
- Who reviewed the trade-validation rules, and was the page ever published?
