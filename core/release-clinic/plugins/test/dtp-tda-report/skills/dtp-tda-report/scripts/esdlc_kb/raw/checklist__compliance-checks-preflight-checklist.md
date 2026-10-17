# Release Compliance Controls — Pre-Flight Checklist (App Team Reference)

**Purpose:** This checklist lists every compliance control enforced during the release pipeline, what is actually being checked, and what your team can verify **before** triggering the pipeline — so failures can be caught and fixed up front instead of being discovered (and re-discovered) by repeatedly running the pipeline.

**How to use this document:** Work through the checklist for the stage you're about to run (CI Build → PRE_TEST → PRE_RELEASE → Release Approval → PRE_PRODUCTION). Each row tells you the work item/field/system involved, the condition that must be true, and the severity if it isn't. Items marked **Hard Stop** will fail the pipeline; items marked **Warning** are reported but do not block.

---

## 1. Pipeline Flow at a Glance

| # | Stage | Mandatory | What Happens |
|---|---|---|---|
| 1 | CI Build | Yes | Secrets scan, commit-to-work-item linkage, static/dependency/container security scans, branch naming validation |
| 2 | QA Deploy + PRE_TEST Compliance Check | Yes | Validates the release is ready to enter QA testing |
| 3 | **Pre-Release Approval (human gate)** | Yes | Pipeline pauses for a Test Manager to confirm testing activities are complete |
| 4 | PRE_RELEASE Compliance Check | Yes | Re-validates PRE_TEST items plus test-summary, SIA/security, cloud/CSDM, and change-request checks |
| 5 | Security Vulnerability Build Breaker | Yes | Fails if open, unaccepted critical/high vulnerabilities remain |
| 6 | Change Request created in ServiceNow | Yes | Auto-creates the SNOW Change Request from the Release Work Item |
| 7 | **Release Approval (human gate)** | Yes | Pipeline pauses for PO / TSO / TSUO / Security Champion sign-off |
| 8 | CCH Approval *(conditional)* | If in scope | Waits (up to 30 days) for Cloud Change Hub approval in the Cloud Onboarding Portal |
| 9 | Artefact checksum, fetch, and promotion | Yes | Confirms artefact integrity and promotes it from non-prod to prod Artifactory |
| 10 | PRE_PRODUCTION Compliance Check | Yes | Final governance gate before production deployment |
| 11 | Production Deployment | Yes | Your application pipeline's own deployment steps |

> **What is a "human gate"?** Steps 3 and 7 pause the pipeline until a member of the relevant ADO Environment's approver group clicks **Approve** in the ADO web UI. Step 3 confirms *"all testing activities completed"*; step 7 confirms *"all approval activities completed for Release."*

---

## 2. CI Build Checklist

Runs on every commit/PR, before the CD pipeline starts.

| # | Control | Pass Condition | Severity | What to Check Beforehand |
|---|---|---|---|---|
| 1 | Secrets scanning | No secrets detected in the commit | Hard Stop | Run a local secrets scan before pushing; never commit credentials, tokens, or keys |
| 2 | Commit → Work Item linkage | Every commit message references a valid ADO Work Item ID | Hard Stop | Ensure every commit is linked to a Work Item (Story/Bug/Task) before pushing |
| 3 | Static code analysis (SAST) | Passes your project's SonarQube quality gate | Reported (gate depends on your quality gate config) | Run SonarQube locally/in a feature branch first if your quality gate is strict |
| 4 | SonarQube report | — | Informational only | No action required — review the published report |
| 5 | Nexus IQ dependency scan | No new critical/high open-source vulnerabilities | Non-blocking (auto-creates ADO Work Items for findings) | Review and remediate before they accumulate; check `package-lock.json`/`pom.xml`/`go.sum`/`requirements.txt` dependencies |
| 6 | SBOM analysis | — | Informational only | Review published SBOM report |
| 7 | Aqua DTA container image scan *(Docker builds only)* | No critical findings in the container image | Reported | Scan your image locally before pushing if you maintain your own Dockerfile |
| 8 | MAST mobile security scan *(conditional — mobile apps)* | — | Reported | Applies only if `enableMastScan` is turned on for your pipeline |
| 9 | NowSecure mobile scan *(conditional — mobile apps)* | — | Reported | Applies only if NowSecure is configured for your pipeline |
| 10 | ECR branch scan *(conditional)* | — | Reported | Applies only on Emergency Change Release (ECR) branches |
| 11 | Security Vulnerability Advisory check | No unaccepted vulnerabilities on protected branches (`develop`, `hotfix/*`, `release/*`, `main`, `master`, `catalyst/main`, `catalyst/release/*`) | Advisory by default; Hard Stop only if your pipeline sets "block if vulnerable" | Triage and accept/remediate open vulnerabilities before merging to a protected branch |
| 12 | Early Feedback *(optional)* | Runs PRE_TEST + PRE_RELEASE checks in preview/warning mode | Non-blocking — informational preview | Use this to get an early read on PRE_TEST/PRE_RELEASE compliance without waiting for the real gate |
| 13 | Qualys scan *(API projects only)* | — | Reported | Applies only if your service exposes an API endpoint scanned by Qualys |
| 14 | **Branch naming validation** | Branch name matches the required pattern (see below) | **Hard Stop — pipeline exits immediately, no further stages run** | Rename any non-compliant branch **before** triggering the pipeline |

### 2.1 Branch Naming Validation — Detail

**Rules:**
- Validation is **case-sensitive**.
- Required branch names and prefixes must be **lowercase exactly as shown** below.
- For prefix-based branches, mixed case is allowed **after** the valid lowercase prefix (e.g. `release/Fix-For-ABC-123` is fine).

| Branch Pattern | Match Type | Deployment Scope |
|---|---|---|
| `release/` | Prefix | Production |
| `hotfix/` | Prefix | Production |
| `hotfix/ecr/` | Prefix | Production |
| `main` | Exact | Production |
| `master` | Exact | Production |
| `catalyst/main` | Exact | Production |
| `catalyst/release/` | Prefix | Production |
| `develop` | Exact | Dev only |
| `feature/` | Prefix | Dev only |
| `catalyst/feature/` | Prefix | Dev only |

**Commonly blocked mistakes:** `Release/...`, `RELEASE/...`, `Hotfix/...`, `HotFix/...`, `Main`, `Master`, `Develop`, `Feature/...`, `Catalyst/Main`, `Catalyst/Release/...` — all fail because of incorrect casing.

**✅ Pre-flight action:** Check your active branch name is lowercase-exact (for `main`/`master`/`develop`/`catalyst/main`) or lowercase-prefixed (for `release/`, `hotfix/`, `hotfix/ecr/`, `feature/`, `catalyst/release/`, `catalyst/feature/`) **before** triggering the pipeline. No YAML changes are needed on your side — this is enforced automatically.

---

## 3. PRE_TEST Compliance Checklist

**When:** At the QA stage gate, before QA testing begins.
**Mode:** Hard Stop for "Must Meet" items; Warning for others.

### 3.1 Pre-Stage Guards (checked first, before anything else below)

| # | Control | Pass Condition | Severity |
|---|---|---|---|
| G1 | Change Type populated | If the Release Work Item is in `Prepare for Release Candidate` state, the `Change Type` field must not be empty | Hard Stop |
| G2 | Story / Prod Bug state valid | Every Story/Production Bug linked to the Release must be in a state valid for PRE_TEST (see Appendix B) | Hard Stop |
| G3 | No unexpected work item types linked | Only expected work item types should be linked to the Release Work Item | Warning |

### 3.2 Expiry Date Checks (Application Work Item)

| # | Control | App Work Item Field | Pass Condition | Severity |
|---|---|---|---|---|
| 1 | Application Architecture expiry | `Application Architecture Approval Expiry Date` | Must not be expired relative to the Planned Release Date | Hard Stop |
| 2 | NFR expiry | `NFR Approval Expiry Date` | Must not be expired relative to the Planned Release Date | Hard Stop |
| 3 | Test Strategy expiry | `Test Strategy Approval Expiry Date` | Must not be expired relative to the Planned Release Date | Hard Stop |

**✅ Pre-flight action:** Open the Application Work Item and confirm all three expiry dates are populated and in the future. If any artefact approval has lapsed, get it re-approved by the relevant reviewer (Domain Architect/TSO for Architecture, Product Owner for NFR, TSO/PO for Test Strategy) before triggering the pipeline — approval renewals can take up to ~50 minutes to reflect after the reviewer sets the new approval date, so don't leave this to the last minute.

### 3.3 Functional Checks

| # | Control | Work Item | Pass Condition | Severity | What to Check Beforehand |
|---|---|---|---|---|---|
| 4 | Solution Intent (SI) linkage & approval | Solution Intent WI | Every in-scope Epic/Feature/Story must trace to a linked Solution Intent that is `Approved` (not expired); the requirement's creation date must be **after** the SI's approval date | Hard Stop | Confirm every Story/Feature/Epic in scope has a linked, currently-Approved Solution Intent created before the requirement itself |
| 5 | Functional Requirements — Story Prioritization | User Story WI | All in-scope Stories must be `Prioritized` (or later) — not `Open`/`Cancelled` — and prioritized by an authorised Product Owner | Hard Stop | Ensure Stories are prioritized by the correct Product Owner (App-level, Component-level, or Service PO) before the release enters PRE_TEST |
| 6 | Feature / Epic state validation | Feature / Epic WI | No Story linked to the Release may trace to a Feature or Epic in `Completed` or `Rejected` state | Hard Stop (Warning on ECR branches) | Check the Feature/Epic chain above every linked Story isn't already closed out |
| 7 | Release Work Item state | Release WI | Must be `New`, `Security Questionnaire Completed`, `Security Control Triggered`, or `Prepare for Release Candidate` | Hard Stop | Confirm the Release WI is in one of these states before running the pipeline |
| 8 | ITR plan and test report | Application WI | IT Resilience capacity/restore/recovery plans and test reports must be current, based on your ITR selection in the Solution Intent | Hard Stop | Verify ITR plan/report dates on the Application WI are populated and current |
| 9 | Cloud Release ID / CCH scope | Release WI | Cloud Release ID must be valid to determine CCH scope | Hard Stop | Confirm the Cloud Release ID field is populated correctly |
| 10 | Planned release date not past | Release WI | `Planned Release Date` must be in the future at pipeline run time | Hard Stop | Double-check the planned release date before running the pipeline |
| 11 | Unclosed Deviation — warning | Deviation WI | Any unclosed Deviation with remediation due within 3 months | Warning | Review open Deviations for your Application Service and plan remediation |
| 12 | Unclosed Deviation — hard stop | Deviation WI | Any unclosed Deviation with a **past** remediation due date | Hard Stop | Close or extend any overdue Deviation before running the pipeline |
| 13 | Data Quality | Story / Solution Intent WI | Validates data quality linkage across stories via Solution Intent | Warning | Review data-quality flags on the Solution Intent if applicable |
| 14 | API controls *(API deployments only)* | Release WI | Additional governance checks for API-based deployments | Hard Stop | Applies only if your pipeline is flagged as an API repository deployment |

---

## 4. PRE_RELEASE Compliance Checklist

**When:** After QA/SIT testing completes.
**Mode:** Hard Stop for "Must Meet" items; Warning for others. Re-validates PRE_TEST items in addition to the checks below. For COTS applications, an extra Code Review/Unit Testing expiry check applies.

### 4.1 Expiry Date Checks

| # | Control | App Work Item Field | Pass Condition | Severity |
|---|---|---|---|---|
| 1 | Test Environment Management (TEM) expiry | `TEM Approval Expiry Date` | Should be current | Warning only |
| 2 | Pre-Deployment Verification (ASRM) expiry | `ASRM Approval Expiry Date` | Must be current | Hard Stop |
| 3 | Code Review & Unit Testing expiry *(COTS applications only)* | `Code Review and Unit Testing TSO Approval Expiry Date` | Must be current | Hard Stop |

### 4.2 SIA / Security Controls

| # | Control | Pass Condition | Severity |
|---|---|---|---|
| 4a | SIA ID present and correctly formatted *(ServiceNow SIA path)* | `SIA ID` field populated and matches expected format | Hard Stop |
| 4b | SIA record exists in ServiceNow | A matching SIA record must exist | Hard Stop |
| 4c | Application ID matches | The system referenced in the SIA must match your Application's Business Application ID | Hard Stop |
| 4d | SIA validation status | Must be `Compliant`, `Compliant - Self Assessed`, or `Non-Compliant Assessed & Risk Accepted` | Hard Stop |
| 4e | SIA stage is Closed | SIA record stage must equal `Closed` | Hard Stop |
| 4f | No unexpected Security Control work items *(ADO path)* | Every linked Security Control WI must be expected/applicable | Hard Stop |
| 4g | One Security Control work item per applicable control | Exactly one WI per applicable control (not zero, not multiple) | Hard Stop |
| 4h | Security Control WI in a compliant state | State must be compliant (or an accepted non-compliant state) | Hard Stop / Warning |
| 4i | S-BIA rating consistency | Must match across Application WI, Release WI, and Security Control WIs | Warning |

**✅ Pre-flight action:** Confirm your SIA (or Security Control work items, whichever path applies to your project) are complete, correctly linked, and in a compliant state before requesting the PRE_RELEASE run. This is skipped for cloud-platform pipelines and ECR branches.

### 4.3 Test Summary

| # | Control | Pass Condition | Severity |
|---|---|---|---|
| 5a | Test types in scope selected | At least one value chosen in `Test Types in Scope` | Hard Stop |
| 5b | Rationale for not doing Performance Testing | Required if PT is excluded from scope | Hard Stop |
| 5c | Rationale for excluding test types | Required if System/Integration/Acceptance/Regression testing is excluded | Hard Stop |
| 5d | Every requirement has test coverage | Every linked requirement (Story/Bug) has at least one test case | Hard Stop |
| 5e | Every test case has been run | No test case left with zero executions | Hard Stop |
| 5f | No open Critical/High defects | Zero open Critical or High severity defects | Hard Stop |
| 5g | Test case coverage per in-scope test type | At least one test case per in-scope non-regression test type | Hard Stop |
| 5h | Regression test cases exist | At least one regression test case, if Regression is in scope | Hard Stop |
| 5i | PT mandatory fields populated | PT Plan link, PT Report link, "Attached Release Controls Doc", PT Performed On — all populated | Hard Stop |
| 5j | PT document links reachable | PT Plan/Report links must resolve | Hard Stop |
| 5k | "Attached Release Controls Document" = Yes | Field must equal `"Yes"` | Hard Stop |
| 5l | PT Performed On date valid | Must be before Planned Release Date **and** within the last 365 days | Hard Stop |
| 5m | Evidence attached to passed test cases | Screenshot/attachment required per passed test case (comment-only is rejected unless explicitly permitted) | Hard Stop |
| 5n | Comment-only evidence *(deprecation notice)* | — | Warning |
| 5o | Failed or Blocked test cases | Any test case left Failed/Blocked | Warning |
| 5p | Open Medium/Low defects | Any open Medium/Low severity defect | Warning |
| 5q | Excluded test types | Informational confirmation | Warning |
| 5r | UVT test cases linked *(Catalyst projects only)* | At least one UVT test case linked | Warning |

**✅ Pre-flight action:** Before requesting PRE_RELEASE, confirm: every requirement has linked, executed test cases; there are no open Critical/High defects; and — if Performance Testing is in scope — the PT Plan/Report links, the "Attached Release Controls Document" flag, and the "PT Performed On" date (within the last 12 months and before your planned release date) are all correctly set.

### 4.4 Other PRE_RELEASE Checks

| # | Control | Work Item / Source | Pass Condition | Severity |
|---|---|---|---|---|
| 6 | Cloud Type / Install Type vs ServiceNow CSDM | Application WI vs ServiceNow | Must match | Hard Stop |
| 7 | Cloud Onboarding ID vs LEAP | Application WI vs LEAP | Must align | Hard Stop |
| 8 | Rollback plan availability | Release WI | Rollback plan must be confirmed available (or explicitly not available, per your pipeline input) | Hard Stop |
| 9 | SNOW Change Request | Release WI + ServiceNow | CR must exist and be in a valid state | Hard Stop |
| 10 | Artefact validation | Release WI / Artifactory | Artefact info must validate against Artifactory | Hard Stop |
| 11 | Planned release date not past | Release WI | Must not have already passed | Hard Stop |
| 12 | Story / Prod Bug state = Ready for Release | User Story / Bug WI | All must be in `Ready for Release` | Hard Stop |
| 13 | Release Work Item state | Release WI | Must be `Prepare for Release Candidate` | Hard Stop |
| 14 | Release WI auto-moved to Ready for Approval | Release WI | Automatic on success — no action needed | — |
| 15 | Security Vulnerability Build Breaker | ServiceNow + ADO | No open/unresolved vulnerabilities | Hard Stop |

---

## 5. Release Approval Checklist (PO / TSO / TSUO / Security Champion)

**When:** After PRE_RELEASE compliance passes, before artefact promotion and production deployment.

| # | Control | Pass Condition | Notes |
|---|---|---|---|
| 1a | Assurance Review status | Must be `Compliant` or `N/A`. `Non-Compliant` requires a pre-recorded Assurance Exception (fails hard if missing); `Non-Compliant Blocked`/`In Progress` always fails | Hard Stop |
| 1b | Security Champion (DRS) sign-off *(conditional)* | `Security Validation Status` must be `Compliant` or `Non-Compliant Assessed & risk Accepted` | Skipped for cloud-platform pipelines, ECR branches, and Day 2 Operations |
| 1c | PO Approval *(non-ECR, non-Day2)* | `PO Approval = Yes`, recorded by a member of your Application's PO group | Skipped for ECR branches and Day 2 Operations |
| 1d | TSO Approval *(non-ECR, non-Day2)* | `TSO Approval = Yes`, recorded by a member of your Application's TSO group | Skipped for ECR branches and Day 2 Operations |
| 1e | TSUO Approval | `TSUO Approval = Yes`, recorded by a member of your Application's PSS-review group | **Always required** — never skipped |
| 2 | CCH approval *(conditional)* | Must be approved in the Cloud Onboarding Portal if in scope | Pipeline waits up to 30 days |
| 3 | Artefact checksum integrity | Build artefact checksum must match the JFrog build provenance record | Hard Stop |
| 4 | Artefact fetch | Artefact metadata retrieved successfully from Artifactory | Hard Stop |
| 5 | Artefact promotion | Artefact promoted from non-prod to prod Artifactory | Hard Stop |

**✅ Pre-flight action:** Line up PO, TSO, TSUO, and (if applicable) Security Champion approvals **before** the pipeline reaches this gate — it will sit waiting for these sign-offs, and TSUO approval in particular is never skipped regardless of branch type or release type.

---

## 6. PRE_PRODUCTION Compliance Checklist

**When:** After Release Approval and artefact promotion, immediately before production deployment.
**Note:** This stage does not re-run test-summary or Artifactory checks — it's a pure governance/approvals gate.

### 6.1 Pre-Stage Guards

| # | Control | Pass Condition | Severity |
|---|---|---|---|
| G1 | Change Type populated | Same check as PRE_TEST — must not be empty if Release WI is in `Prepare for Release Candidate` | Hard Stop |
| G2 | Story / Prod Bug state = Ready for Release | Same check repeated from PRE_RELEASE | Hard Stop |

### 6.2 Checks

| # | Control | Work Item / Source | Pass Condition | Severity |
|---|---|---|---|---|
| 1 | Security Assessment Validity Date | Release WI | Must not be in the past | Hard Stop |
| 2 | SNOW Change Request approved/scheduled | Release WI + ServiceNow | CR must be approved/scheduled | Hard Stop |
| 3 | Snapshot / tamper check | Release WI | The Release WI must not have been altered since the PRE_RELEASE compliance report was generated | Hard Stop |
| 4 | Assurance review + Release WI state | Release WI | PO/PSS review complete; Release WI must be `Approved` | Hard Stop |
| 5 | Requirements linkage vs test summary | Story/Bug WI + Test Summary | Requirements linked to the Release must exactly match those in the PRE_RELEASE test summary — no additions/removals since then | Hard Stop |

**✅ Pre-flight action:** Do not add or remove Story/Bug links to the Release Work Item after PRE_RELEASE passes — doing so will fail this check and require re-running the pipeline from PRE_RELEASE.

---

## Appendix A — Valid Release Work Item States per Stage

| Stage | Valid States |
|---|---|
| PRE_TEST | `New`, `Security Questionnaire Completed`, `Security Control Triggered`, `Prepare for Release Candidate` |
| PRE_RELEASE | `Prepare for Release Candidate` |
| PRE_PRODUCTION | `Approved` |

## Appendix B — Valid Story / Bug States per Stage

| Stage | Valid States |
|---|---|
| PRE_TEST | `Prioritized`, `In Analysis`, `Ready for Development`, `In Development`, `On Hold`, `Dev Done`, `In Test`, `Ready for Release` |
| PRE_RELEASE | `Ready for Release` only |
| PRE_PRODUCTION | `Ready for Release` only |

## Appendix C — Application Artefact Expiry Fields Reference

These fields live on the **Application Work Item** and follow the same pattern: an approval date set by the relevant reviewer, and a rolling expiry date recalculated automatically 12 months from that approval (unless noted).

| Stage Checked | Control | App WI Field | Must Meet |
|---|---|---|---|
| PRE_TEST | Application Architecture | `Application Architecture Approval Expiry Date` | Yes |
| PRE_TEST | NFR | `NFR Approval Expiry Date` | Yes |
| PRE_TEST | Test Strategy | `Test Strategy Approval Expiry Date` | Yes |
| PRE_RELEASE | Test Environment Management (TEM) | `TEM Approval Expiry Date` | No (warning only) |
| PRE_RELEASE | Pre-Deployment Verification (ASRM) | `ASRM Approval Expiry Date` | Yes |
| PRE_RELEASE (COTS only) | Code Review and Unit Testing | `Code Review and Unit Testing TSO Approval Expiry Date` | Yes |

> **Tip:** Keep these approval dates refreshed well ahead of your planned release date. Automatic recalculation of the expiry date after a new approval is set can take up to ~50 minutes — don't set the approval the same moment you plan to trigger the pipeline.

## Appendix D — Control Reference Names (as they appear in compliance reports)

| Control | Stage(s) |
|---|---|
| Solution Intent | PRE_TEST |
| Functional Requirement | PRE_TEST |
| Application Architecture | PRE_TEST (expiry) |
| Test Strategy | PRE_TEST (expiry) |
| NFR | PRE_TEST (expiry) |
| Data Quality | PRE_TEST |
| AWG Feature | PRE_TEST (Catalyst only) |
| ITR Capacity Plan | PRE_TEST |
| ITR Restore Plan | PRE_TEST |
| ITR Recovery Plan | PRE_TEST |
| ITR Recovery Test | PRE_TEST |
| ITR Restore Test | PRE_TEST |
| ITR Data Restore Test | PRE_TEST |
| ITR Availability Test | PRE_TEST |
| Test Environment Management | PRE_RELEASE (expiry, warning) |
| Pre Deployment Verification - ASRM | PRE_RELEASE (expiry) |
| Code Review and Unit Testing | PRE_RELEASE (COTS only) |
| SIA | PRE_RELEASE |
| Test Summary | PRE_RELEASE |
| Pre Deployment Verification - Rollback | PRE_RELEASE |
| Catalyst Test Strategy | PRE_RELEASE (Catalyst only) |

## Appendix E — External Systems Your Records Need to Be Valid In

| System | What It's Used For |
|---|---|
| ServiceNow (SNOW) | CSDM (Cloud/Install Type), Change Requests, SIA records |
| LEAP — Cloud Onboarding Portal | Cloud Onboarding ID validation, CCH approvals |
| Genie | Test automation results, test summary reports |
| JFrog Artifactory | Build artefact storage, checksum/provenance verification, promotion |
| ADO Security Groups | PO / TSO / TSUO / Domain Architect approval-authority checks |

---

**Questions about a specific control or a failure message you don't understand?** Reach out to the **ADO Support team** (`ADO_Support@exchange.standardchartered.com`) with the Release ID and the exact control name from the compliance report (Appendix D) rather than re-running the pipeline speculatively.
