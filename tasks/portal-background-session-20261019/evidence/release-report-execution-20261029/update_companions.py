"""Refresh current execution and coverage documents from the reconciled catalog."""
from pathlib import Path
import json
import re
import subprocess
from render_report import envelope

HERE=Path(__file__).resolve().parent
TASK=HERE.parent.parent
ROOT=TASK.parent.parent
P='evidence/remaining-execution-20261029/'


def main():
    inv=json.loads((TASK/P/'aggregate/final-inventory.json').read_text())
    counts=inv['counts']; full=counts['PASSED']+counts['FAILED']
    rows={r['id']:r for r in inv['rows']}
    core_summary=json.loads((TASK/P/'core-browser/reconciled-summary.json').read_text())
    core_rows={r['id']:r for r in core_summary['results']}
    assert counts.get('NOT_RUN',0)==0
    rel=TASK.relative_to(ROOT)
    old=subprocess.check_output(['git','show','89daa0bec:'+str(rel/'09-renewal-coverage.md')],cwd=ROOT,text=True)
    coverage=old.replace('version: 1\n','version: 2\n',1)
    coverage=coverage.replace('Scope: the [current request](evidence/user-input-20261028-comprehensive-renewal.txt), seven renewal criteria, and 12 changed shell runtime paths.',
        'Scope: the [latest execution request](evidence/user-input-20261029-run-remaining-cases.txt), seven renewal criteria, and 12 changed shell runtime paths.')
    coverage=coverage.replace('New execution inventory: 3 browser cases and 13 controller cases. Fifteen pass; one security case fails.\nThe other 451 expanded instances remain `NOT_RUN`. Existing unit tests are counted separately.',
        f'All 467 expanded instances have [retained dispositions]({P}aggregate/final-inventory.json).\n'
        f'**{full} fully executed: {counts["PASSED"]} pass and {counts["FAILED"]} fail.**\n'
        f'**{counts["PARTIALLY_EXECUTED"]} partially executed; {counts["BLOCKED"]} blocked before complete execution.**\n'
        'The complete current unit suite passes 471/471 tests across 123 suites. Unit tests have a separate denominator.\n'
        'The catalog retains design-time execution annotations. The final inventory supplies current outcomes.')
    coverage=coverage.replace('AC-4 partial; AC-1, AC-2, AC-3 not rerun','AC-4 partial; AC-1, AC-2, AC-3 fail current activity checks')
    coverage=coverage.replace('| Execution NOT_RUN | 37 rows across 11 declared factors |',
        '| 37 rows partially executed; business commit and native transport predicates blocked | 37 rows across 11 declared factors |')
    coverage=coverage.replace('Current modular test assertions.','Current modular test assertions.')
    rewritten=[]
    for line in coverage.splitlines():
        if line.startswith('| [AC-') and 'Defined; inspected selected predicates | NOT_RUN |' in line:
            criterion=int(re.search(r'\[AC-(\d)',line).group(1))
            case=f'RN-A{criterion:03d}'
            # Workspace cases independently reproduce the same three activity predicates.
            workspace=f'RN-W{28+criterion:03d}'
            result=rows[case]['result']; wr=rows[workspace]['result']
            line=line.replace('[activity.cjs](evidence/comprehensive-renewal-20261028/sources/cff93d755ace/activity.cjs#L10-L42)',
                f'[Current browser assertions]({core_rows[case]["assertion_link"]}); '
                f'[current workspace assertion]({P}workspace-transport/run-workspace.mjs#L137); '
                '[retained supplemental activity.cjs](evidence/comprehensive-renewal-20261028/sources/cff93d755ace/activity.cjs#L10-L42)')
            line=line.replace('Defined; inspected selected predicates | NOT_RUN |',
                f'Defined; inspected selected predicates | **FAILED**: [{case} result]({result}); [{workspace} result]({wr}) |')
            line=line.replace('Inspected current modular test assertions. Those browser assertions were not executed against this pinned source in this stage.',
                'Current committed-source browser execution confirms zero renewal in the measured interval. Later session loss was not observed.')
        if line.startswith('| [AC-4]') and 'Defined; inspected selected predicates | PARTIAL |' in line:
            line=line.replace('No finite test proves indefinite operation. Cross-source historical results retain their original bindings.',
                f'Current [RN-L011 result]({rows["RN-L011"]["result"]}) retains its exact outcome and omitted assertions. '
                'Controlled time cannot establish actual provider, native suspension, or indefinite operation.')
        rewritten.append(line)
    coverage='\n'.join(rewritten)+'\n'
    start=coverage.index('Targeted units: **157 / 157')
    end=coverage.index('## Coverage gaps',start)
    coverage=coverage[:start]+f'''Complete current units: **471/471 pass across 123 suites**, with zero failures, skips, todos, or runner errors.
The [complete execution]({P}full-unit-execution.json) binds current candidate bytes and the unchanged declared suite.
The [467-instance inventory]({P}aggregate/final-inventory.json) separates complete passes, failures, partial checks, and blockers.
Fifteen ordering rows pass. All 181 pairwise and risk rows remain partial because authoritative business-operation checks are unavailable.
The [source-bound release report](10-release-confidence.md) remains NO_GO because the inherited logout revocation failure controls its recommendation.

'''+coverage[end:]
    coverage=coverage.replace('Real application data, dirty forms, lazy modules, live WebSockets, STOMP, SSE, and long transfers remain unexecuted.',
        'Synthetic workspaces now exercise dirty fields and module state. Real business data and live transport acceptance remain unavailable.')
    coverage=coverage.replace('Full four-hour current-candidate browser verification remains absent. Component and historical executions have narrower claims.',
        f'Current endurance disposition: [RN-L011]({rows["RN-L011"]["result"]}). Its omitted predicates remain explicit.\n'
        'Native controls, actual provider acceptance, and complete critical consumer journeys remain unverified.')
    coverage=coverage.replace('Facts: the retained executions establish only their asserted fixture outcomes. One security assertion fails.',
        f'Facts: {counts["FAILED"]} expanded cases fail. Passing results establish only their stated fixture predicates.')
    (TASK/'09-renewal-coverage.md').write_text(coverage)
    # Reuse the single current detailed matrices with their exact anchors and links.
    matrix_start=coverage.index('### AC to test case coverage')
    matrix_end=coverage.index('\n## ', matrix_start)
    matrices=coverage[matrix_start:matrix_end]
    assertion_rows=[]
    for identifier in ['RN-A001','RN-A002','RN-A003','RN-M001','RN-M002','RN-M003','RN-L011','RN-Q009','RN-S023','RN-S035','RN-S037']:
        r=rows[identifier]
        assertion_rows.append(f'| [{identifier}]({r["definition"]}) | {r["title"]} | {r["status"]} | [Bound result and assertions]({r["result"]}) |')
    assertions='\n'.join(assertion_rows)
    families=[]
    for name,group in inv['groups'].items():
        c=group['counts']
        families.append(f'| {name} | {c["TOTAL"]} | {c["PASSED"]} | {c["FAILED"]} | {c["PARTIALLY_EXECUTED"]} | {c["BLOCKED"]} |')
    family_table='\n'.join(families)
    execution=envelope('test-execution-report','EXEC-comprehensive-session-renewal',2)+f'''
# Session Refresh: remaining-case execution and evidence limits

> **Critical conclusions: NO_GO remains. Complete unit tests pass, but material security failure remains.**
> Action: correct or disprove applicable [SEC-01](07-security-review-renewal.md#sec-01), then reassess.
> Consequence: copied valid refresh credentials can regain authentication after apparent logout in the isolated controller test.
> Owner: unknown authentication and security owners. Evidence: [replay failure](evidence/comprehensive-renewal-20261028/expired-logout-case.json).
> Target exposure remains unverified. Complete case execution remains blocked where its required environment is unavailable.

| Metric | Current result |
| --- | --- |
| Requested 451 remaining instances | Every instance has a retained result or explicit execution blocker |
| Entire 467-instance catalog | **{full} fully executed: {counts['PASSED']} pass, {counts['FAILED']} fail** |
| Incomplete catalog execution | **{counts['PARTIALLY_EXECUTED']} partial; {counts['BLOCKED']} blocked**; none counted as passing |
| Full current unit suite | **471/471 pass; 123/123 suites**; zero failures, skips, todos, expected failures, or runner errors |
| SDLC coverage | Seven criteria linked; three selected passing outcomes, three activity failures, one partial |

See the [release conclusion and consolidated failure impacts](10-release-confidence.md) and [essential HTML](10-release-confidence.html).

## Run identity and provenance

The [latest instruction](evidence/user-input-20261029-run-remaining-cases.txt) authorizes remaining local execution and report refresh.
The [READY stage]({P}stage-checkpoint.json) preserves scope, authorization, and excluded actions.
No application fixes, production tests, or deployments were performed.
Every case completion was retained before further execution. Interrupted and corrected attempts remain available.

```yaml
execution_id: remaining-execution-20261029
execution_status: COMPLETED_WITH_BLOCKED_CASES
repository_id: mfe-base
repository_revision: 66c6411ade58e4d134e381c2baee8ad3f76a8dbf
test_revision: "Canonical catalog SHA-256 5622dab3b635113ff0137fbf66489f385bbcb11dc4444ec0070f7203d19a7037"
environment_identity: local-immutable-source-with-disclosed-synthetic-peers
command_or_tool_reference: evidence/remaining-execution-20261029/aggregate/final-inventory.json
process_exit_status: "Per-run originals retained; no single suite process covers the expanded catalog."
actual_results:
  catalog_total: 467
  fully_executed: {full}
  passed: {counts['PASSED']}
  failed: {counts['FAILED']}
  partially_executed: {counts['PARTIALLY_EXECUTED']}
  blocked: {counts['BLOCKED']}
  current_unit_passed: 471
  current_unit_failed: 0
  current_unit_suites: 123
retained_execution_refs:
  - evidence/remaining-execution-20261029/aggregate/final-inventory.json
  - evidence/remaining-execution-20261029/full-unit-execution.json
```

Each run retains its start and completion times. The [inventory]({P}aggregate/final-inventory.json) binds original results and definitions.
The [source binding]({P}execution-source-binding.json) identifies immutable frontend bytes and the historical synthetic BFF fixture.
Actual current BFF and SDK logic ran separately in the [security composition]({P}security/server-execution.json).
The browser login fixture does not establish current composed server-byte acceptance.

## Browser environment and suite completeness

The [canonical catalog](06-test-cases.md) contains 467 expanded instances across 40 use cases.
Its hash is recorded above. Earlier 27-case and review inventories keep their historical revisions.
The catalog retains design-time execution annotations. The final inventory supplies current execution status.
Browser: Microsoft Edge 156.0.4314.50, headless Chromium, macOS, isolated contexts.
Controlled clocks accelerate expiry and endurance. Controlled visibility events do not reproduce native OS suspension.
Actual portal DOM, Home, Timeout, reducers, shared Axios, and source transport callbacks execute where bound.
Synthetic peers replace authentication responses, embedded business modules, and transport servers where disclosed.
Security probes execute actual controller, RSA, SDK-filter, and session-service logic with mocked collaborators.
Source hashes bind each assertion boundary. Twenty-six definitions cite dirty Home bytes excluded from execution.
The [inventory]({P}aggregate/final-inventory.json) records that discrepancy and each missing predicate.
No blocked case is promoted to a pass. Characterization passes do not establish accepted security behavior.
Screenshots are retained per browser case. Source-function and jsdom probes have no native browser screenshot.

| Inventory | Total | Pass | Fail | Partial | Blocked |
| --- | ---: | ---: | ---: | ---: | ---: |
{family_table}

## Assertions and outcomes

The following results are selected navigation points. The [full inventory]({P}aggregate/final-inventory.json) includes every case separately.
Each result identifies assertions, expected values, actual values, source bindings, and omitted boundaries.

| Canonical case | Predicate or boundary | Outcome | Assertions and actual result |
| --- | --- | --- | --- |
{assertions}

All failed cases have consequences, severity, owners, and actions in the [release failure table](10-release-confidence.md#all-failed-cases-and-observed-user-impact).
Fixture errors remain distinct from application failures. Later fixture corrections do not erase the original attempts.
The [core reconciliation]({P}core-browser/reconciled-summary.json) identifies selected final outcomes and retained superseded attempts.

## Coverage inventories and summary

Intent: seven version-5 criteria. Change inventory: twelve runtime paths from `f025513f696476a9cc8162681410cbd21e029bcb` to `66c6411ade58e4d134e381c2baee8ad3f76a8dbf`.
Six paths are behavioral; six support maintenance. Complete changed-predicate and required assertion inventories remain unknown.
The [coverage report](09-renewal-coverage.md) distinguishes definitions, assertions, conformance, and execution.
The current unit suite passes without path narrowing or assertion changes. Its [JSON]({P}full-unit-results.json) retains individual test identities.
This report assesses SDLC coverage. Unit line coverage cannot establish behavioral equivalence.

| Metric | Qualified / total | Scope and limit |
| --- | --- | --- |
| Canonical criterion definitions | 7/7 | Definition relationship only |
| Selected direct assertion associations | 7/7 | Complete required assertion coverage remains UNKNOWN/7 |
| Selected matching passing execution | 3/7 | Synthetic manual recovery scope; three activity failures, one partial |
| Bounded implementation matches | 3/7 | One partial, one contradictory, two missing; complete equivalence unknown |
| Changed-path selected assertion reach | 12/12 | Complete changed-predicate coverage UNKNOWN/12 |
| Factor-pair design | 797/797 | Design only; 181 combination rows retain missing business-operation predicates |

{matrices}

## Retained evidence inventory

| Evidence | Locator | Integrity and availability limit |
| --- | --- | --- |
| Final case inventory | [All 467]({P}aggregate/final-inventory.json) | Exact definition blocks, outline rows, results, and source bindings have SHA-256 |
| Complete units | [Execution]({P}full-unit-execution.json), [results]({P}full-unit-results.json) | 471/471 at current candidate; delayed-exit warning retained |
| Security | [Final audit]({P}security/final-audit.json) | Forty-two newly requested cases; mocks and blocked target checks remain explicit |
| Workspace and transport | [Summary]({P}workspace-transport/summary.json) | Synthetic modules, controlled routes, and source mismatch retained |
| Combinations | [Summary]({P}combinations/combination-summary.json) | 283 bounded assertions pass; only fifteen complete ordering cases pass |
| Original prior executions | [Earlier binding](evidence/comprehensive-renewal-20261028/execution-source-binding.json) | Sixteen prior instances remain separate from the 451 newly requested instances |

## Browser evidence bindings

Case directories retain setup/failure/final captures where available. Result JSON binds captures to the executed predicates.
The [workspace loading failure]({P}workspace-transport/RN-Q009/result.json) includes held-response state and loader disappearance.
Its [screenshot]({P}workspace-transport/RN-Q009/attempt-failed.png) supports the visible state, not a data-loss claim.
The [core summary]({P}core-browser/reconciled-summary.json) and [workspace manifest]({P}workspace-transport/evidence-manifest.json) identify retained captures.
Java, jsdom, and source-function cases rely on assertion and request evidence. Native screenshots are not applicable there.

## Verification conclusion

**The requested catalog is fully reconciled, but complete canonical execution remains unavailable for the blocked predicates.**
Passing results verify only their stated conditions. Full units now satisfy the mandatory current-suite condition.
Security failure, current activity gaps, partial consumers, and policy uncertainty prevent complete conformance or acceptance claims.
`TC >= AC = Code Change` remains unestablished. Unsupported additional behavior and full boundary inventories remain unknown.

## Facts, inferences, and unresolved questions

Facts: per-case results retain actual assertions. Failed predicates remain visible. Current full unit execution passes.
Inferences: conditional security and session interruption risks depend on supported callers and matching deployment settings.
Unknowns: actual business writes, transport authorization, native lifecycle behavior, and pending policy remain unresolved.
Use the [single living policy register](05-test-strategy-renewal.md#policy-questions). No business answer is inferred from execution authorization.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| [SEC-01](07-security-review-renewal.md#sec-01) | Logout can leave refresh usable | unknown authentication owner | Correct or disprove applicable failure; retain rejection controls |
| [New security impacts]({P}security/new-failure-impacts.json) | Conditional credential and authorization risks remain | unknown security owner | Trace actual callers and gateway enforcement |
| [All incomplete predicates]({P}aggregate/final-inventory.json) | Complete acceptance is unavailable | unknown test and service owners | Bind missing environments and exact assertions |
| [Current activity and loading failures]({P}workspace-transport/findings.json) | Renewal and visible loading targets fail | unknown application owner | Retain approved backlog scope; decide loading-gap disposition |

## Sources

| Source | Locator | Revision, hash, and authority |
| --- | --- | --- |
| User | [Latest instruction](evidence/user-input-20261029-run-remaining-cases.txt) | 29 October 2026; local test authorization |
| Canonical definitions | [Catalog](06-test-cases.md) | Exact SHA-256 above; policy acceptance remains separate |
| Sources and results | [Final inventory]({P}aggregate/final-inventory.json) | Exact revisions, assertion bindings, and SHA-256 per item |
| Historical baseline and source map | [Original assertion map](evidence/comprehensive-renewal-20261028/assertion-map.json) | Selected relationships, not complete equivalence |
| Final automated checks | [Validation](evidence/release-report-execution-20261029/validation.json) | Structural checks only; full ASD writing review pending |
'''
    (TASK/'08-test-execution-renewal.md').write_text(execution)


if __name__=='__main__':
    main()
