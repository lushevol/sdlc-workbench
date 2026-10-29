"""Restore the final report view and apply the user-impact priority rule."""
from pathlib import Path
from collections import Counter
import datetime,hashlib,html,json,re,subprocess

HERE=Path(__file__).resolve().parent
TASK=HERE.parent.parent
ROOT=TASK.parent.parent
CLARITY=TASK/'evidence/report-clarity-20261029'
OLD=TASK/'evidence/release-report-execution-20261029'
REQUEST='evidence/user-input-20261029-impact-priority-layout.txt'
PREFIX='evidence/report-impact-priority-20261029/'

def read(p):return json.loads(p.read_text())
def esc(s):return html.escape(str(s),quote=True)
def link(label,url):return f'<a href="{esc(url)}">{esc(label)}</a>'
def baseline(name):return subprocess.check_output(['git','show','531d285d5:'+str(TASK.relative_to(ROOT)/name)],cwd=ROOT,text=True)
def records(a):return a['issues']+a['review_entries']+a['additional_controls']
def priority_text(row):
    if row['new_priority']=='NONE_CLOSED':return 'Closed locally'
    if row['new_priority']=='NOT_A_DEFECT_PRIORITY':return 'Authorization record'
    return row['new_priority']
def potential_severity(row):
    value=re.sub(r';?\s*P[1-4][^.;]*','',row.get('severity','Unknown'))
    value=re.sub(r'\s*/\s*\.', '.',value)
    value=re.sub(r'\.{2,}', '.',value)
    return value.rstrip(' ./;')
def disposition(row):
    return {
      'SECURITY_RELEASE_BLOCKER':'Release hold for assessed source',
      'SCOPED_SESSION_BLOCKER':'Blocking in the reproduced flow; check applicability',
      'SCOPED_SESSION_DISRUPTION':'Targeted session-risk check; verify provider trigger',
    }.get(row['blocking_disposition'],row['blocking_disposition'].replace('_',' ').capitalize())

def main():
    cases=read(HERE/'case-priority-audit.json');audit=read(HERE/'issue-priority-audit.json')
    ac=read(CLARITY/'ac-explanation-audit.json')['criteria']
    assert len(cases['rows'])==285
    assert Counter(r['status'] for r in cases['rows'])=={'FAILED':15,'PARTIALLY_EXECUTED':199,'BLOCKED':71}
    assert cases['summary']['nonblocking_cases']==284
    allrows=records(audit);byid={r['id']:r for r in allrows}
    # Restore the compact previous report layout. Details remain a separate document.
    ac_descriptions={
      'AC-1':'Mouse movement repeatedly resets the five-second timer. No renewal occurs during the test; session interruption was not observed. P4.',
      'AC-2':'No keyboard renewal binding exists. Session interruption was not observed. P4.',
      'AC-3':'No scroll renewal binding exists. Session interruption was not observed. P4.',
      'AC-4':'Four simulated hours passed. Real SSO prompts and protected-service acceptance remain unverified. P3 verification follow-up.',
      'AC-5':'The dialog stays open while renewal is pending.',
      'AC-6':'Successful renewal closes the dialog once and installs access in the controlled local test.',
      'AC-7':'Failed renewal leaves the dialog open with retry enabled.',
    }
    acrows=[]
    for c in ac:
        status={'PASSED':'Passed','FAILED':'Failed','PARTIAL':'Partial'}[c['status']]
        result=link('Proof',c['result_links'][0])
        acrows.append(f'<tr><td>{link(c["id"],c["definition"])} · {status}</td><td>{esc(ac_descriptions[c["id"]])} {result}</td></tr>')
    mainhtml=(HERE/'report-template.html').read_text().replace('@@AC_ROWS@@','\n'.join(acrows))
    mainhtml=mainhtml.replace('@@CASE_PRIORITY_SUMMARY@@','Current triage for these 285 cases: 1 P1 blocker, 273 P3 follow-ups, and 11 P4 backlog cases.')
    mainhtml=mainhtml.replace('<h2>Issues that need attention</h2>','<a id="failed-reasons"></a><h2>Issues that need attention</h2>')
    (TASK/'10-release-confidence.html').write_text(mainhtml)
    # Keep every reason accessible without expanding the final-report landing page.
    details=baseline('10-release-confidence.html')
    details=details.replace('<title>Session Refresh · Results and reasons</title>','<title>Session Refresh · Detailed evidence</title>')
    details=details.replace('<h1>Release is on hold.<br>Here is what failed and what remains unverified.</h1>',
      '<h1>Detailed results and issue priorities.</h1><p><a href="10-release-confidence.html">← Return to the concise release report</a></p>')
    policy=f'<div class="metric-line"><b>Current priority rule:</b> missing proof or minor effects do not create automatic release holds. Higher priority requires concrete disruptive impact or a genuine blocking problem. {link("User instruction",REQUEST)}.</div>'
    details=details.replace('<div class="stats"',policy+'\n<div class="stats"',1)
    case_map={r['id']:r for r in cases['rows']}
    def revise_case(m):
        text=m.group(0);case_id=re.search(r'06-test-cases.md#[^\"]+\">([^<]+)</a>',text).group(1)
        c=case_map[case_id]
        p=f'<p><b>Current priority: {esc(c["new_priority"])}.</b> {esc(c["reason"])} '
        p+=('Release hold for the assessed source.' if c['release_blocking'] else 'No independent release hold.')+'</p>'
        return text.replace('<td><p><b>Reason:</b>','<td>'+p+'<p><b>Reason:</b>',1)
    details,n=re.subn(r'<tr class="case-row"[\s\S]*?</tr>',revise_case,details)
    assert n==285
    for severity in ['<b>Severity:</b>']:
        details=details.replace(severity,'<b>Retained severity assessment:</b>')
    # Historical cards keep outcomes and potential severity. The new table sets current priorities.
    details=details.replace('Severity describes consequence','Potential severity describes consequence')
    case_groups={}
    for c in cases['rows']:case_groups.setdefault(c['group_id'],[]).append(c)
    def revise_group(m):
        text=m.group(0);group=re.search(r'data-group="([^"]+)"',text).group(1)
        priorities=sorted({c['new_priority'] for c in case_groups[group]})
        treatment='Release hold for assessed source.' if any(c['release_blocking'] for c in case_groups[group]) else 'No independent release hold.'
        text=text.replace('<p><b>Why:</b>',f'<p><b>Current priority: {esc(", ".join(priorities))}.</b> {treatment}</p><p><b>Why:</b>',1)
        text=re.sub(r'<p class="note"><b>Retained severity assessment:</b>[\s\S]*?</p>',
            '<p class="note">Potential severity remains separate from priority. Use the current issue register for release treatment.</p>',text)
        return text
    details=re.sub(r'<article class="reason-card">[\s\S]*?</article>',revise_group,details)
    issue_rows=[]
    for r in allrows:
        refs=' · '.join(link('Result '+str(i+1),x) for i,x in enumerate(r.get('result_links',[])[:2]))
        sources=' · '.join(link('Source '+str(i+1),x) for i,x in enumerate(r.get('source_links',[])[:2]))
        issue_rows.append(f'<tr><td>{link(r["id"],r["definition"])}<br><b>{esc(priority_text(r))}</b></td><td><p><b>Why:</b> {esc(r["reason"])}</p><p><b>Observed:</b> {esc(r["observed_user_impact"])}</p><p><b>Treatment:</b> {esc(disposition(r))}.</p><details><summary>Action, limits, and evidence</summary><p>{esc(r["next_action"])}</p><p class="note">Owner: {esc(r["owner"])}. {esc(" ".join(r.get("limits",[])))}</p><p>{sources} · {refs}</p></details></td></tr>')
    register='<section id="priority-register"><h2>Current issue priorities</h2><p>These records include aliases and shared causes. They are not a count of distinct defects.</p><p>Potential severity remains separate from priority. This table supersedes older priority and blanket-hold wording in retained evidence.</p><table class="case-table"><thead><tr><th>Issue and priority</th><th>Reason, impact, and treatment</th></tr></thead><tbody>'+''.join(issue_rows)+'</tbody></table></section>'
    details=details.replace('<section id="case-explorer">',register+'<section id="case-explorer">',1)
    details=details.replace('evidence/report-clarity-20261029/validation.json',PREFIX+'validation.json')
    (TASK/'10-release-confidence-details.html').write_text(details)
    make_markdown(byid,cases,audit)
    update_catalogue(audit)
    index=TASK/'evidence/index.md';s=index.read_text();marker='## Direct evidence\n'
    addition=f'''\nLatest priority and layout rule: [preserved instruction](user-input-20261029-impact-priority-layout.txt).
The [current issue triage](report-impact-priority-20261029/issue-priority-audit.json) supersedes earlier priorities and blanket verification holds.
The [285-case priority audit](report-impact-priority-20261029/case-priority-audit.json) preserves every execution status.
The [concise release report](../10-release-confidence.html) links the [detailed evidence view](../10-release-confidence-details.html).
The [validation](report-impact-priority-20261029/validation.json) and [source manifest](report-impact-priority-20261029/source-manifest.json) bind this update.
'''
    if addition.strip() not in s:s=s.replace(marker,marker+addition,1)
    index.write_text(s)
    (HERE/'presentation-summary.json').write_text(json.dumps({'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'scope':'Compact final report and user-impact priority reassessment. No application execution or outcome changes.',
      'case_priority_summary':cases['summary'],'issue_summary':audit['summary'],
      'release_status':'NO_GO','controlling_issue':'RN-S002','scoped_session_risks':['REVIEW-E2E-01','RN-R020'],
      'policy_source':REQUEST,'main_report':'10-release-confidence.html','details':'10-release-confidence-details.html'},indent=2)+'\n')

def make_markdown(byid,cases,audit):
    report=baseline('10-release-confidence.md').replace('version: 6\n','version: 7\n',1)
    report=report.replace('The remaining risks are not acceptable as a whole.','The logout revocation failure controls this source assessment.')
    report=report.replace('## Metrics summary\n',f'The [latest user-impact rule]({REQUEST}) controls current issue priority and release treatment.\nMissing verification and minimal effects do not create automatic release holds.\n\n## Metrics summary\n',1)
    start=report.index('## How to read case execution')
    end=report.index('## Go-live impact and acceptability',start)
    short='''## User-impact priority and execution reasons

Only **one of the 285 failed or incomplete cases** creates an independent source release hold: [RN-S002](#failure-rn-s002).
The other 284 remain lower-priority follow-up: **273 P3** and **11 P4**.
All 199 partial and 71 blocked results remain unverified. Missing proof alone does not establish disruptive behavior.
Activity and loading cases remain P4 because their runs show no disrupted or unusable session.
Potential severity remains separate from current priority. Raise priority when concrete disruptive impact or genuine blocking applicability appears.

The [detailed HTML](10-release-confidence-details.html) retains every reason, impact, source link, and current priority.
The [case priority audit](evidence/report-impact-priority-20261029/case-priority-audit.json) covers all 285 cases.
The [issue audit](evidence/report-impact-priority-20261029/issue-priority-audit.json) also reassesses historical review entries and general controls.

[AC-1](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L187) fails because continuous mouse input resets the five-second timer.
[AC-2](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L194) and [AC-3](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L201) fail because their renewal bindings are absent.
[AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L208) passed four simulated hours; real SSO and protected-service proof remain unavailable.
These criteria retain their failed or partial status. Their current priority is lower because disruptive user impact remains unproved.
The [coverage matrices](09-renewal-coverage.md) retain the full denominators and source relationships.
Each of 12 changed runtime source files has some passing test evidence. Complete behavior coverage remains unknown.

'''
    report=report[:start]+short+report[end:]
    start=report.index('## Go-live impact and acceptability');end=report.index('## Release scope',start)
    report=report[:start]+'''## Go-live impact and acceptability

| Issue / current priority | Proven effect and material limit | Release treatment |
| --- | --- | --- |
| [RN-S002](#failure-rn-s002), P1 | Current server test renews access after apparent logout. Production reachability remains unverified. | Genuine security blocker for the assessed source. Correct or prove inapplicability. |
| [REVIEW-E2E-01](#failure-review-e2e-01), P2 | Valid replacement access remains behind unusable recovery actions in the historical controlled browser flow. Current persistence is source-based. | Blocking in that flow. Establish supported caller applicability; correct ownership when reachable. |
| [RN-R020](06-test-cases.md#rn-r020), P2 | Older expired-token response clears renewed credentials and emits a sign-in-again error in source integration. | Targeted session-risk verification. Provider occurrence and actual forced logout remain unverified. |
| Activity and loading checks, P4 | No interrupted or unusable session was demonstrated. | Backlog. No independent release hold. |
| Conditional exposures and incomplete cases, P3 | Real receiver, supported caller, provider contract, or complete result is unavailable. | Planned investigation. Escalate if disruptive impact or a genuine blocking path is demonstrated. |

The [latest instruction](evidence/user-input-20261029-impact-priority-layout.txt) authorizes lower priority under these conditions.
It does not convert failed checks into passes or authorize deployment.
Potential impact severity and production likelihood remain separate from action priority.

'''+report[end:]
    report=report.replace('The [latest clarity request]',f'The [latest layout and priority instruction]({REQUEST}) controls this update.\n\nThe [earlier clarity request]',1)
    report=report.replace('| Conditional security paths are understood | Actual callers, gateway controls, and service execution | **LIMITED**;',
      '| Conditional security follow-up | Actual callers, gateway controls, and service execution | **P3 LIMITED; not an independent hold**;')
    report=report.replace('| Consumer and lifecycle assertions execute | Required real services, native controls, transaction observations | **LIMITED**;',
      '| Consumer and lifecycle verification | Required real services, native controls, transaction observations | **P3 LIMITED; not an independent hold**;')
    # The failure point, observed impact, source links, and outcome remain intact.
    lines=[]
    for line in report.splitlines():
        match=re.search(r'<a id="failure-[^\"]+\"></a>\[([^]]+)\]',line)
        if match and match[1] in byid:
            row=byid[match[1]];cells=line.split(' | ')
            if len(cells)>=6:
                severity=potential_severity(row)
                cells[3]=f'**{row["new_priority"]}: {disposition(row)}.** {row["reason"]} Potential severity: {severity}.'
                line=' | '.join(cells)
        lines.append(line)
    report='\n'.join(lines)+'\n'
    start=report.index('### Risks within passing or partial observations')
    end=report.index('## Risks and exceptions',start)
    section=[]
    for line in report[start:end].splitlines():
        match=re.match(r'\| \[([A-Z0-9-]+)\]',line)
        if match and match[1] in byid:
            row=byid[match[1]];cells=line.split(' | ')
            if len(cells)==4:
                cells[2]=f'**{row["new_priority"]}: {disposition(row)}.** {row["reason"]}'
                line=' | '.join(cells)
        section.append(line)
    report=report[:start]+'\n'.join(section)+'\n\n'+report[end:]
    report=report.replace('Acceptance remains blocked by the missing diagnostic contract.','P3 diagnostic follow-up. The missing contract creates no independent release hold.')
    start=report.index('## Risks and exceptions');end=report.index('## Confidence score and release status',start)
    report=report[:start]+'''## Risks and exceptions

The [latest user-impact rule](evidence/user-input-20261029-impact-priority-layout.txt) applies to every finding and incomplete verification item.
P3 and P4 items remain planned follow-up or backlog. They do not create independent release holds on current evidence.
The logout security failure remains a genuine blocker. The two demonstrated session effects require targeted applicability checks.
Lower priority does not establish passing execution, a safe production path, or a human deployment decision.
Release artifacts remain excluded. No artifact gate or penalty applies to this source assessment.

'''+report[end:]
    for name in ['Intent and conformance','Assertions and executions','Conditional security','Business impact','System and consumers']:
        report=report.replace(f'| {name} | 3/5 LIMITED | yes |',f'| {name} | 3/5 LIMITED | no automatic hold |')
    report=report.replace('| Code review | 3/5 LIMITED | yes |','| Code review | 3/5 LIMITED | scoped session risk |')
    report=report.replace('| <a id="a2"></a>A2 | P1 investigation;', '| <a id="a2"></a>A2 | P3 planned investigation;')
    report=report.replace('Resolve conditional High risks; reassess with actual composed path results.','No independent hold. Escalate after concrete disruptive exposure; reassess with composed results.')
    report=report.replace('Resolve supported replacement-login callers, pending policy, activity scope, and loading-defect disposition.',
      'Verify supported replacement-login callers and older-response session clearing. Retest the demonstrated session effects when applicable.')
    report=report.replace('| <a id="a4"></a>A4 | P2;', '| <a id="a4"></a>A4 | P3 verification follow-up;')
    report=report.replace('Complete risk-selected acceptance evidence; reassess after retained source-matching runs.',
      'No automatic hold. Increase verification when a material disruptive path is supported.')
    report=report.replace('blocking_action_refs: ["#a1", "#a2", "#a3", "#a4"]','blocking_action_refs: ["#a1"]')
    report=report.replace('close the release holds and applicable risks','close the controlling hold and review applicable session risks')
    report=report.replace('evidence/report-clarity-20261029/validation.json',PREFIX+'validation.json')
    report=report.replace('evidence/report-clarity-20261029/source-manifest.json',PREFIX+'source-manifest.json')
    report=report.replace('| Latest presentation instruction |',
      f'| Latest priority and layout instruction | [Preserved input]({REQUEST}) | User message, 29 October 2026; authorizes impact-based priority and concise layout |\n| Earlier presentation instruction |',1)
    (TASK/'10-release-confidence.md').write_text(report)


def update_catalogue(audit):
    path=TASK/'10-issue-catalog.md';s=baseline('10-issue-catalog.md').replace('version: 3\n','version: 4\n',1)
    start=s.index('> **Critical conclusions:');end=s.index('## Scope and source facts',start)
    intro=f'''> **Current conclusion: NO_GO for the demonstrated logout security failure.**
> Action: correct or prove inapplicable [RN-S002](10-release-confidence.md#failure-rn-s002), then verify replay rejection.
> Consequence: apparent logout leaves valid refresh credentials usable. Owner: unknown authentication owner.
> Evidence: [current assessment](10-release-confidence.md). Production reachability remains unverified.

The [latest user-impact instruction]({REQUEST}) supersedes older priority and blanket-hold wording below.
The [current priority audit]({PREFIX}issue-priority-audit.json) reassesses every retained failure and review entry.
It also covers additional observed session risks, verification gaps, and general release controls.
Minor or unproved disruptive effects remain P3/P4 follow-up. Missing verification alone creates no automatic source-release hold.
The stale recovery dialog and older-response credential clearing retain P2 targeted verification.
This catalogue retains historical source identities and findings. Use the current audit for priority and release treatment.
Release artifacts remain outside the current source assessment.

'''
    s=s[:start]+intro+s[end:]
    s=s.replace('Proposed P2 means investigate before release, P3 means planned follow-up, and P4 means backlog.',
      'Current P2 means targeted investigation of demonstrated session effects. P3 means planned follow-up; P4 means backlog.')
    s=s.replace('The final candidate is `e0030f5','The historical candidate is `e0030f5',1)
    # Preserve the old technical narratives, but replace their priority labels with the current assessment.
    for row in audit['review_entries']:
        slug=row['id'].lower()
        pattern=r'(\| <a id="'+re.escape(slug)+r'"[\s\S]*?— )P[1-4]'
        s=re.sub(pattern,lambda m:m[1]+row['new_priority'],s,count=1)
    s=s.replace('Production remains `BLOCKED`. No deployment authorization is recorded.',
      'The current source assessment is `NO_GO` for logout revocation. No deployment authorization is recorded.\nHistorical missing-evidence controls below are not independent product-failure holds under the current rule.')
    s=s.replace('Reassess only after the release holds and applicable risks have closure evidence.',
      'Reassess after the controlling security failure closes. Reevaluate scoped session effects against supported callers and provider behavior.')
    s=s.replace('## Proposed responses\n','## Proposed responses\n\nThese entries retain the earlier broader release scope. Apply current priorities from the linked audit.\n',1)
    (TASK/'10-issue-catalog.md').write_text(s)

if __name__=='__main__':main()
