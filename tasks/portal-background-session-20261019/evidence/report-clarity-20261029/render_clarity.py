"""Explain retained release evidence in plain language; never change case outcomes."""
from pathlib import Path
from collections import Counter
import hashlib
import html
import json
import subprocess

HERE=Path(__file__).resolve().parent
TASK=HERE.parent.parent
ROOT=TASK.parent.parent
RUN=TASK/'evidence/remaining-execution-20261029'
OLD=TASK/'evidence/release-report-execution-20261029'
P='evidence/report-clarity-20261029/'


def read(path):
    return json.loads(path.read_text())


def esc(value):
    return html.escape(str(value),quote=True)


def a(label,href):
    return f'<a href="{esc(href)}">{esc(label)}</a>'


def md(label,href):
    return f'[{label}]({href})'


def content(value):
    if isinstance(value,list):return ' '.join(str(x) for x in value)
    return str(value or '')


def criterion_observation(criterion):
    # Human explanations stay separate from the retained machine assertion records.
    return {
        'AC-4': 'The browser completed four simulated hours. Renewal continued, and no local sign-in field appeared.',
        'AC-5': 'The expiry dialog stayed open while the renewal request remained pending.',
        'AC-6': 'Successful renewal closed the dialog once. The substitute service accepted the installed access credential.',
        'AC-7': 'Failed renewal left the dialog open and the retry button enabled.',
    }.get(criterion['id'], criterion['observed'])


def criterion_status(criterion):
    return 'PARTIALLY_EXECUTED' if criterion['status']=='PARTIAL' else criterion['status']


def main():
    reasons=read(HERE/'execution-reason-audit.json')
    ac=read(HERE/'ac-explanation-audit.json')
    inventory=read(RUN/'aggregate/final-inventory.json')
    impacts=read(OLD/'failure-impacts.json')
    byid={r['id']:r for r in inventory['rows']}
    groups=reasons['groups']; rows=reasons['rows']; criteria=ac['criteria']
    assert Counter(r['status'] for r in rows)=={'FAILED':15,'PARTIALLY_EXECUTED':199,'BLOCKED':71}
    assert len({r['id'] for r in rows})==285
    assert {r['id'] for r in rows}=={r['id'] for r in inventory['rows'] if r['status']!='PASSED'}
    assert len(criteria)==7
    status_names={'FAILED':'Failed','PARTIALLY_EXECUTED':'Partial','BLOCKED':'Blocked','PASSED':'Passed'}
    impact_map={r['case_id']:r for r in impacts['cases']}
    # Preserve the prior complete assessment. This stage clarifies presentation only.
    report=subprocess.check_output(['git','show','f3de127ee:'+str(TASK.relative_to(ROOT)/'10-release-confidence.md')],cwd=ROOT,text=True)
    report=report.replace('version: 5\n','version: 6\n',1)
    report=report.replace('**12/12 runtime paths reach selected assertions and passing tests**',
        '**12/12 changed runtime source files have at least one inspected assertion and passing test**')
    report=report.replace('Full changed-predicate coverage remains unknown. Six paths are behavioral; six support maintenance.',
        'This counts files with some test evidence. It does not prove every changed behavior. Six files are behavioral; six support maintenance.')
    report=report.replace('Twelve runtime paths | 12/12 selected direct assertion chains and passing tests',
        'Twelve changed runtime source files | Each file has at least one inspected assertion and matching passing result')
    report=report.replace('## Release scope\n','## Release scope\n\nThe [latest clarity request](evidence/user-input-20261029-report-clarity.txt) requires visible reasons and plain coverage explanations.\n',1)
    report=report.replace('| Latest user instruction |',
        '| Latest presentation instruction | [Preserved clarity request](evidence/user-input-20261029-report-clarity.txt) | User message, 29 October 2026; requires execution reasons and understandable coverage |\n| Latest execution instruction |',1)
    report=report.replace('The [validation record](evidence/release-report-execution-20261029/validation.json) separates structural checks from business execution and pending ASD review.',
        'The [clarity validation](evidence/report-clarity-20261029/validation.json) checks reasons, links, and interactive presentation.\nThe [earlier execution validation](evidence/release-report-execution-20261029/validation.json) retains its original scope. Full ASD review remains pending.')
    report=report.replace('| Report integrity | [Source manifest](evidence/release-report-execution-20261029/source-manifest.json), [validation](evidence/release-report-execution-20261029/validation.json) | SHA-256 and actual automated checks; full writing review pending |',
        '| Current report integrity | [Source manifest](evidence/report-clarity-20261029/source-manifest.json), [validation](evidence/report-clarity-20261029/validation.json) | SHA-256 and actual automated checks; full writing review pending |\n| Earlier report integrity | [Source manifest](evidence/release-report-execution-20261029/source-manifest.json), [validation](evidence/release-report-execution-20261029/validation.json) | Preserved validation for the earlier execution refresh |')
    definitions='''
## How to read case execution

The total is **467 cases**: 182 passed, 15 failed, 199 partial, and 71 blocked.
The latest run covered the 451 previously unrun cases. Sixteen earlier cases remain in the total.

- **Failed:** an executed check produced a different result from its stated expectation.
- **Partial:** some required checks ran, but the complete case remains unverified.
- **Blocked:** a required check could not run or finish because its environment, service, or observation was unavailable.

Blocked cases can include preparatory actions. Partial and blocked cases are not evidence that the application passed or failed.
The [HTML case list](10-release-confidence.html#case-explorer) shows each reason, missing check, and next action.

'''
    for status,title in [('FAILED','Why 15 cases failed'),('PARTIALLY_EXECUTED','Why 199 cases are partial'),('BLOCKED','Why 71 cases are blocked')]:
        definitions+=f'### {title}\n\n| Cases | Reason | Required next step |\n| --- | --- | --- |\n'
        for g in groups:
            if g['status']!=status:continue
            definitions+=f'| **{g["count"]}: {g["title"]}** | {content(g["reason"])} | {content(g["next_action"])} |\n'
        definitions+='\n'
    definitions+='''## Why acceptance criteria failed or remain partial

An acceptance criterion (AC) defines an expected user outcome. Several test cases can check one criterion.
The three passing criteria concern manual renewal in the controlled local environment.

| Criterion | Result | What happened and why | Missing proof or user consequence |
| --- | --- | --- | --- |
'''
    for c in criteria:
        definitions+=f'| {md(c["id"],c["definition"])}: {c["title"]} | **{status_names[criterion_status(c)]}** | {criterion_observation(c)} {content(c["reason"])} | {content(c.get("missing"))} {content(c.get("impact"))} |\n'
    definitions+='''
## What “12 changed files have some passing test evidence” means

“Path” meant a source file, such as the Timeout controller. The earlier label was unclear.
The denominator includes **12 changed runtime source files**. It excludes the other 24 test or configuration paths.
For each file, at least one inspected test checks relevant behavior and has a matching passing result.
For example, a Timeout test checks that successful renewal closes the dialog once.
That result does not prove every timing condition, failure path, or user journey in the file.
The loading helper also has passing tests. However, [RN-Q009](#failure-rn-q009) shows another behavior in that file fails.
**12/12 therefore means every selected file has some passing test evidence. Complete behavior coverage remains unknown.**
See the [file-to-test matrix](09-renewal-coverage.md#code-change-to-test-case-coverage) for the exact twelve relationships.

'''
    report=report.replace('## Go-live impact and acceptability',definitions+'## Go-live impact and acceptability',1)
    (TASK/'10-release-confidence.md').write_text(report)
    make_html(groups,rows,criteria,byid,impact_map)
    index=TASK/'evidence/index.md';text=index.read_text()
    marker='## Direct evidence\n'
    addition=f'''\nClarity request: [explain failed, partial, blocked, AC results, and changed-file metrics](user-input-20261029-report-clarity.txt).
The [execution reason audit](report-clarity-20261029/execution-reason-audit.json) explains all 285 nonpassing or incomplete cases.
The [criterion explanation audit](report-clarity-20261029/ac-explanation-audit.json) explains all seven criteria and the twelve-file measure.
The [clarity validation](report-clarity-20261029/validation.json) checks the new HTML explanations and interactive case filters.
The [clarity source manifest](report-clarity-20261029/source-manifest.json) binds this presentation update.
'''
    if 'Current instruction:' in text:
        start=text.index(marker)+len(marker)
        end=text.index('Current instruction:',start)
        text=text[:start]+addition+'\n'+text[end:]
    elif addition.strip() not in text:
        text=text.replace(marker,marker+addition,1)
    index.write_text(text)
    (HERE/'presentation-summary.json').write_text(json.dumps({'scope':'Presentation clarification only; no new test executions or outcome changes.',
        'counts':inventory['counts'],'reason_rows':len(rows),'criteria':7,
        'request':'evidence/user-input-20261029-report-clarity.txt',
        'sources':{'inventory_sha256':hashlib.sha256((RUN/'aggregate/final-inventory.json').read_bytes()).hexdigest(),
                   'failure_impacts_sha256':hashlib.sha256((OLD/'failure-impacts.json').read_bytes()).hexdigest()}},indent=2)+'\n')


def make_html(groups,rows,criteria,byid,impact_map):
    labels={'FAILED':'Failed','PARTIALLY_EXECUTED':'Partial','BLOCKED':'Blocked','PASSED':'Passed'}
    cls={'FAILED':'failed','PARTIALLY_EXECUTED':'partial','BLOCKED':'blocked','PASSED':'passed'}
    sections=[]
    for status,title,intro in [
        ('FAILED','Why 15 cases failed','Each group below has an executed check that did not meet its expectation.'),
        ('PARTIALLY_EXECUTED','Why 199 cases are partial','Some checks ran. The missing checks below prevent a complete result.'),
        ('BLOCKED','Why 71 cases are blocked','A required check could not run or finish. Preparatory actions may still have run.')]:
        cards=[]
        for g in groups:
            if g['status']!=status:continue
            ids=g['case_ids']
            evidence=' · '.join(a(x,byid[x]['result']) for x in ids[:3])
            source_links=[]
            for row in rows:
                if row['id'] in ids:
                    for source in row.get('source_links',[]):
                        if source not in source_links:source_links.append(source)
            source_evidence=' · '.join(a('Source '+str(i+1),v) for i,v in enumerate(source_links[:3]))
            extra=''
            if status=='FAILED':
                f=next((impact_map[x] for x in ids if x in impact_map),None)
                if f:
                    extra=f'<p><b>User impact:</b> {esc(f["observed_user_impact"])} {esc(f["conditional_user_impact"])}</p><p class="note"><b>Severity:</b> {esc(f["severity"])} {esc(f["acceptability"])}</p>'
            cards.append(f'''<article class="reason-card"><div class="card-top"><h3>{esc(g['title'])}</h3><span class="count">{g['count']} {'case' if g['count']==1 else 'cases'}</span></div>
<p><b>Why:</b> {esc(content(g['reason']))}</p>
{f'<p><b>What ran:</b> {esc(content(g["what_ran"]))}</p>' if status!='FAILED' else ''}
{f'<p><b>Still missing:</b> {esc(content(g["missing"]))}</p>' if g.get('missing') else ''}
{extra}<details><summary>Next step and evidence</summary><p>{esc(content(g['next_action']))}</p>
<p class="note">Owner: {esc(g.get('owner','unknown'))}. Evidence: {evidence}. {source_evidence}</p></details>
<button class="text-button group-button" data-group="{esc(g['id'])}">View these {g['count']} cases ↓</button></article>''')
        sections.append(f'<section id="{cls[status]}-reasons"><h2>{title}</h2><p class="section-intro">{intro}</p><div class="reason-grid">'+''.join(cards)+'</div></section>')
    acrows=[]
    for c in criteria:
        links=' · '.join(a('Result '+str(i+1),v) for i,v in enumerate(c.get('result_links',[])[:3]))
        sources=' · '.join(a('Source '+str(i+1),v) for i,v in enumerate(c.get('source_links',[])[:2]))
        acrows.append(f'''<tr><td><b>{a(c['id'],c['definition'])} · {esc(c['title'])}</b><span class="status {cls[criterion_status(c)]}">{labels[criterion_status(c)]}</span></td>
<td><p>{esc(criterion_observation(c))}</p><p><b>Why this result:</b> {esc(content(c['reason']))}</p>
{f'<p><b>Still missing:</b> {esc(content(c["missing"]))}</p>' if c.get('missing') else ''}
<p class="note">{esc(content(c.get('impact')))}</p><p class="note">{links} · {sources}</p></td></tr>''')
    caserows=[]
    for r in rows:
        original=byid[r['id']]
        sources=' · '.join(a('Source '+str(i+1),v) for i,v in enumerate(r.get('source_links',[])))
        severity=f'<p><b>Severity:</b> {esc(r["severity"])}</p>' if r.get('severity') else ''
        search=' '.join([r['id'],original['title'],content(r.get('reason')),content(r.get('missing'))]).lower()
        caserows.append(f'''<tr class="case-row" data-status="{esc(r['status'])}" data-group="{esc(r['group_id'])}" data-search="{esc(search)}">
<td><b>{a(r['id'],original['definition'])}</b><span class="status {cls[r['status']]}">{labels[r['status']]}</span><p>{esc(original['title'])}</p></td>
<td><p><b>Reason:</b> {esc(content(r['reason']))}</p>
<p><b>Impact:</b> {esc(content(r.get('impact')))}</p>{severity}
<details><summary>What ran, what is missing, and next step</summary>
<p><b>What ran:</b> {esc(content(r.get('what_ran')))}</p><p><b>Missing:</b> {esc(content(r.get('missing')))}</p>
<p><b>Next step:</b> {esc(content(r.get('next_action')))}</p><p class="note">Owner: {esc(r.get('owner','unknown'))}. {sources}</p></details>
<p class="note">{a('Case definition',original['definition'])} · {a('Execution evidence',original['result'])}</p></td></tr>''')
    template=(HERE/'report-template.html').read_text()
    historical='''<details class="historical"><summary>Earlier failures and additional risks</summary>
<p>The 15-case count covers the current expanded catalog. Earlier investigations also found a stale recovery dialog and other retained issues.</p>
<p>An older unauthorized response cleared renewed credentials in a passing observation case. Its proposed severity is Moderate, conditional.</p>
<p>Passing observation cases record behavior. They do not establish that the behavior is acceptable.</p>
<p>'''+a('All historical failures, additional risks, severity, and source links','10-release-confidence.md#all-failed-cases-and-observed-user-impact')+'</p></details>'
    document=template.replace('@@REASON_SECTIONS@@','\n'.join(sections)).replace('@@AC_ROWS@@','\n'.join(acrows))
    document=document.replace('@@CASE_ROWS@@','\n'.join(caserows)).replace('@@HISTORICAL@@',historical)
    (TASK/'10-release-confidence.html').write_text(document)


if __name__=='__main__':
    main()
