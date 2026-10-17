h1. TDA Automation — Business Checks Reference

This document lists the *business/governance checks* automated by the TDA tooling ({{AutoTDAScript.py}} collects the evidence; the {{dtp-tda-report}} Copilot skill applies the rules below and produces the checkpoint report), for review and feedback by the TDA team.

Each check below states: *what is verified*, *what evidence is used*, and *how it is scored* (CRITICAL = blocks the release, MODERATE = risk to flag and follow up, MINOR/Info = noted for awareness only, LOOKS GOOD = no issue found).

{info:title=Scope of this automation}
This is a point-in-time automated check of what's recorded in ADO/Confluence/SonarQube/Genie/ServiceNow at the moment the collector is run — it does not replace manual TDA judgement, but is intended to remove the manual effort of chasing this evidence across five different systems.
{info}

h2. 1. Release Governance

||Business Check||What "good" looks like||Severity if failed||
|Release Work Item is in a valid lifecycle state|State is {{Prepared Release Candidate}}, {{Ready For Approval}}, or {{Released}}|*CRITICAL* if any other state|
|Release is linked to a parent Application|An Application work item is set as the parent of the Release WI|*CRITICAL* if missing — mandatory platform governance requirement|
|Release WI is not an undisclosed clone|If the release was cloned from another, this is called out for review|Flagged for review (not auto-blocked) if cloned flag is set without explanation|
|PO / TSO / TSUO sign-off recorded|Approval fields show "Yes"|Informational only — the release pipeline itself already enforces this before a Release WI can reach this stage, so it is never treated as a blocker here|
|AIG (Application Impact Guide) + Rollback plan linked|Link present on the Release WI|Informational only — the document may exist on the pipeline's Extension tab without being linked here|
|Implementation Plan documented|{{Implementation Plan}} field populated on the Change Manifest|*MODERATE* if empty|
|Backout Plan documented|{{Backout Plan}} field populated on the Change Manifest|*MODERATE* if empty|
|Release status aligned with ServiceNow change record|E.g. Release {{Prepared Release Candidate}} ↔ CHG {{Scheduled/Assess/Implement}}; Release {{Released}} ↔ CHG {{Closed/Review/Implement}}|Informational only — a mismatch is noted for the release manager, never a blocker|

h2. 2. Application-Level Approvals

||Business Check||What "good" looks like||Severity if failed||
|Application architecture / ASRM / NFR / TEM / Test Strategy approvals are current|Expiry date is in the future|*CRITICAL* if already expired; *MINOR/Info* if expiring within 90 days but not yet expired|

h2. 3. ServiceNow Change Management

||Business Check||What "good" looks like||Severity if failed||
|CHG record exists and is retrievable|Change record found in ServiceNow for the CHG number on the Release WI|Flagged if no data returned — checked for CHG number accuracy / connectivity, not an automatic blocker|
|CHG state is consistent with release progress|See "Release status aligned with ServiceNow" above|Informational only|

{note:title=Streams without ServiceNow}
Some streams do not use a ServiceNow change process — this check is skipped entirely for those streams by design, not treated as a gap.
{note}

h2. 4. Performance Testing (PT) Governance

||Business Check||What "good" looks like||Severity if failed||
|Every release has PT evidence *or* a documented reason PT wasn't needed|Either (a) a PT Plan *and* PT Report, or (b) a PT Impact Assessment (PTIA) — as a Confluence page or a written justification on the Release WI|*CRITICAL* if neither exists|
|Not both — only one route should be used|Only PT docs *or* PTIA is present, not both|*MODERATE* if both are present (indicates process confusion)|
|PT Plan / PT Report are approved|Confluence page is accessible and has recorded approver(s)|*CRITICAL* if the page is inaccessible; *MODERATE* if accessible but has no recorded approver|
|Written PTIA justification is credible, not a placeholder|Explains a specific, credible reason (e.g. component/architecture scope)|*MODERATE* if generic/boilerplate (e.g. "N/A", "Not required") — asks the release manager to confirm it's accurate for this release|

h2. 5. Post-Implementation Testing (PIT) Governance

||Business Check||What "good" looks like||Severity if failed||
|PIT plan is documented somewhere|A Confluence/SC Wiki PIT page (via the stream's standard PIT URL *or* a link found in the Release WI's {{Review Comments}} field) *or* the Release WI's {{PITPlan}} Change Manifest field is populated|*CRITICAL* if none of the three exists|
|PIT Confluence page is approved (when used)|Page accessible and has recorded approver(s)|*MODERATE* if accessible but empty of approvers and the release is already {{Released}}; informational only if still pre-release|

{note:title=Text-only PIT plans}
When the PIT plan is only recorded as text on the Release WI rather than a Confluence page, this is accepted as satisfying the requirement — the tooling notes that execution/approval ownership for that route stays with the application/release team, since it can't independently verify a text field's approval status.
{note}

h2. 6. Manual Test Execution Evidence — CRITICAL Gate

For *every* manual test case executed as part of the release:

||Business Check||What "good" looks like||Severity if failed||
|Test execution records exist at all|Test Results data present in ADO for the release|*CRITICAL* if completely absent — impossible to confirm any manual testing occurred|
|Every test case outcome is Passed|No Failed / Blocked / Not Run outcomes|*CRITICAL* on any non-Passed outcome|
|Every test step within a test case is Passed|All steps marked Passed|*CRITICAL* if any step isn't|
|Evidence is attached|A file (screenshot/doc/PDF/etc.) or a URL/ADO-link is present on the test case or one of its steps|*CRITICAL* if no evidence exists anywhere on the test case|

{warning:title=Hard gate}
A release cannot be considered tested without both a Passed outcome *and* attached evidence for every manual test case.
{warning}

h2. 7. Automated Regression Testing (Genie / ADO-native)

||Business Check||What "good" looks like||Severity if failed||
|Regression failure rate|0% failures|*CRITICAL* if failure rate > 5%; *MODERATE* if 1–5%; *MINOR* if under 1% but non-zero|
|Failed regression scenarios are manually re-tested|A test case documenting manual re-verification of each automated failure exists, is Passed, and has evidence attached|*CRITICAL* if no such re-test case exists, or it exists but isn't Passed/evidenced|

{note}
Regression results may come from Genie, or — for streams that don't use Genie — from automated results published directly to ADO. Both are checked against the identical thresholds above. If a stream has temporarily disabled its regression data collection, this is reported as "not evaluated" rather than a gap, since it's a known/deliberate exception.
{note}

h2. 8. Requirements Traceability (Story → Test Coverage)

||Business Check||What "good" looks like||Severity if failed||
|Every story has at least one form of test coverage|Covered by *any one* of: ADO manual System / Integration / Acceptance test case, or Genie/automation System or Integration Testing evidence|*MODERATE* only if a story has *none* of these five — having just 1 of the 5 is sufficient, it is not a gap|
|Story completeness — Application ID recorded|{{Custom.ApplicationID}} populated on the story|*MODERATE* if missing|
|Story completeness — Story Type recorded|{{Custom.StoryType}} populated on the story|*MODERATE* if missing|
|Automated test coverage exists where expected|If a release declares "Automated Testing = Yes" in scope, at least some stories should show automation evidence (from ADO or Genie)|*MODERATE* if the release claims automated testing in scope but no stories show any automation evidence|

{note}
Automation status is also reported as an informational trend — e.g. how many stories have Genie-tool automation vs. ADO-tagged automation — since these two data points commonly diverge and that divergence alone is not treated as a defect.
{note}

h2. 9. Story Closure Review

||Business Check||What "good" looks like||Severity if failed||
|Story's last comment doesn't indicate unresolved work|Comment is empty, or clearly indicates successful closure (e.g. "Verified", "Validated", "Testing completed")|*MODERATE* if the comment contains language suggesting something is pending/blocked/failing (e.g. "not working", "pending", "waiting", "MQ issues", "raised a bug") — listed individually for release-manager review|
|Story state matches expected release-lifecycle stage|E.g. stories in {{Done}} once the release is {{Released}} is expected, not a problem|Informational only|

h2. 10. Code Quality Gates (SonarQube)

||Business Check||What "good" looks like||Severity if failed||
|Overall test coverage|≥ 40%|*CRITICAL* if below 40%|
|New-code coverage|≥ 40%|*CRITICAL* if below 40%|
|Correct Quality Gate profile assigned|Project uses the bank-standard {{ESDLC-Sonarway-managed}} gate|*CRITICAL* if a different/custom gate is assigned|
|Unit tests all passing|No Failed unit test outcomes|*CRITICAL* if any fail (requires Dev Lead approval to proceed if accepted)|
|No unclassified ("Others") unit tests|All unit tests are properly categorised|*CRITICAL* if "Others"-category tests exist|
|Configured code exclusions|Reported for awareness (which files/patterns are excluded from Sonar analysis, coverage, duplication, or test detection)|Informational only — never a gate on its own, but visibility helps the team confirm exclusions are intentional and not hiding untested code|

h2. 11. Cross-Document Consistency

Guards against approvals/documents that were copy-pasted from a previous release or the wrong stream and never updated.

||Business Check||What "good" looks like||Severity if failed||
|PT Plan / PT Report / PTIA / PIT page titles reference the correct release version and stream|Page titles match the canonical version extracted from the Release WI title|Flagged for review if a mismatch is found (e.g. a PT report still titled for last release's version)|
|ServiceNow change description matches the release|Description references the same release/stream|Flagged for review if it doesn't|

h2. What this automation does *not* decide

* It does not overrule human TDA sign-off — it surfaces evidence and applies the rules above consistently, but the final PASS / CONDITIONAL / BLOCKED verdict is meant to inform, not replace, TDA team judgement.
* Checks explicitly marked *informational/MINOR* above are never allowed to escalate into a release blocker by the automation, regardless of context — by design, to avoid false blockers on things that are already enforced elsewhere (e.g. pipeline-level approval gates) or are genuinely just FYI items.

h2. Feedback wanted from the TDA team

* Are the CRITICAL / MODERATE / MINOR thresholds above (5%/1% regression failure rate, 40% coverage, 90-day approval expiry window, 85% story description/AC similarity, etc.) set at the right level for our release governance standard?
* Are there business checks currently done manually during TDA sign-off that are *not* reflected in this list and should be added?
* Are there checks above that should be reclassified (e.g. a MODERATE that should be CRITICAL, or vice versa)?

