"""Add native collapsed details without changing the release assessment or outcomes."""
from pathlib import Path
from collections import Counter
import hashlib,html,json,re,subprocess
HERE=Path(__file__).resolve().parent
TASK=HERE.parent.parent
ROOT=TASK.parent.parent
PRIOR=TASK/'evidence/report-impact-priority-20261029'
CLARITY=TASK/'evidence/report-clarity-20261029'
REQUEST='evidence/user-input-20261029-collapsed-result-details.txt'
PREFIX='evidence/report-collapsed-details-20261029/'

def read(p):return json.loads(p.read_text())
def esc(s):return html.escape(str(s),quote=True)
def link(label,url):return f'<a href="{esc(url)}">{esc(label)}</a>'
def baseline(name):return subprocess.check_output(['git','show','7713ed7c7:'+str(TASK.relative_to(ROOT)/name)],cwd=ROOT,text=True)
def links(label,values):return ' · '.join(link(label+' '+str(i+1),x) for i,x in enumerate(values))
def plain(value):return ' '.join(value) if isinstance(value,list) else str(value or '')
def disclosure(id,title,body,kind='item-detail'):
    return f'<details class="{kind}" id="{esc(id)}"><summary>{title}</summary>{body}</details>'
def paragraph(label,value):return f'<p><b>{esc(label)}:</b> {esc(plain(value))}</p>'

def case_details(c,reason,issue=None):
    body=paragraph('Reason',c['execution_reason'])
    body+=paragraph('What ran',reason.get('what_ran'))
    body+=paragraph('Observed user impact',c['observed_user_impact'])
    body+=paragraph('Still missing',c['missing_check'])
    body+=paragraph('Why this priority',c['reason'])
    body+=paragraph('Release treatment','Release hold for the assessed source.' if c['release_blocking'] else 'No independent release hold.')
    limits=c.get('evidence_limits') or reason.get('limits') or (issue or {}).get('limits')
    if limits:body+=paragraph('Evidence limits',limits)
    body+=paragraph('Next action',c['next_action'])+f'<p class="note">Owner: {esc(c["owner"])}.</p>'
    body+=f'<p class="note">{link("Case definition",c["definition"])} · {link("Execution evidence",c["result"])}'
    if c.get('assertion_link'):body+=' · '+link('Assertions',c['assertion_link'])
    if c.get('source_links'):body+=' · '+links('Source',c['source_links'])
    body+='</p>'
    return disclosure('case-'+c['id'].lower(),f'{esc(c["id"])} · {esc(c["new_priority"])} · {esc(c["title"])}',body)

def main():
    cases=read(PRIOR/'case-priority-audit.json');audit=read(PRIOR/'issue-priority-audit.json')
    reasons=read(CLARITY/'execution-reason-audit.json');ac=read(CLARITY/'ac-explanation-audit.json')['criteria']
    byid={r['id']:r for r in cases['rows']};reason_byid={r['id']:r for r in reasons['rows']}
    issues={r['id']:r for k in ['issues','review_entries','additional_controls'] for r in audit[k]}
    assert len(byid)==285
    status_labels={'FAILED':'Failed','PARTIALLY_EXECUTED':'Partial','BLOCKED':'Blocked'}
    status_panels=[]
    for status in status_labels:
        rows=[r for r in cases['rows'] if r['status']==status]
        body=''
        for g in cases['groups']:
            if g['status']!=status:continue
            first=reason_byid[g['case_ids'][0]]
            groupbody=paragraph('Reason',first['plain_group_reason'])
            groupbody+=paragraph('User impact',g['observed_user_impact'])
            groupbody+=paragraph('Next action',g['next_action'])
            groupbody+=''.join(case_details(byid[i],reason_byid[i],issues.get(i)) for i in g['case_ids'])
            priorities=', '.join(sorted(g['priorities']))
            noun='case' if g['count']==1 else 'cases'
            body+=disclosure('group-'+g['id'],f'{esc(g["title"])} · {g["count"]} {noun} · {esc(priorities)}',groupbody,'reason-detail')
        status_panels.append(disclosure('cases-'+status.lower(),f'{status_labels[status]} · {len(rows)} cases',body,'status-detail'))
    mainhtml=baseline('10-release-confidence.html')
    styles='''
.status-detail,.reason-detail,.item-detail{border:1px solid var(--line);border-radius:6px;margin:10px 0;padding:10px 12px;background:#fff}
.status-detail>summary{font-size:15px}.reason-detail{background:#fafbf9}.reason-detail>summary,.item-detail>summary{font-size:14px}
.item-detail{font-weight:400}.item-detail p{font-size:14px;margin:8px 0}summary{overflow-wrap:anywhere}.metric .item-detail{padding:8px;margin-bottom:0}
.metric .item-detail summary{font-size:12px;font-weight:650}.metric .item-detail p{font-size:12px}.empty-status{color:var(--muted);font-size:14px}
'''
    mainhtml=mainhtml.replace('</style>',styles+'</style>',1)
    marker='<p>Current triage for these 285 cases: 1 P1 blocker, 273 P3 follow-ups, and 11 P4 backlog cases.</p>'
    assert marker in mainhtml
    mainhtml=mainhtml.replace(marker,marker+'\n'+''.join(status_panels),1)
    # Add source, assertion, and execution evidence beside each adverse AC result.
    ac_panels=[]
    for status,label in [('FAILED','Failed'),('PARTIAL','Partial'),('BLOCKED','Blocked')]:
        rows=[c for c in ac if c['status']==status]
        body=''
        if not rows:body='<p class="empty-status">No acceptance criterion has a blocked disposition. AC-4 remains partial because specific verification is missing.</p>'
        for c in rows:
            priority='P4' if c['status']=='FAILED' else 'P3'
            inner=paragraph('Why this result',c['reason'])+paragraph('Missing proof',c['missing'])+paragraph('User impact and limit',c['impact'])
            inner+=paragraph('Next action',c['next_action'])
            inner+=f'<p class="note">Current priority: {priority}. No independent release hold. Owner: unknown application and verification owners.</p>'
            inner+=f'<p class="note">{link("Criterion definition",c["definition"])} · '+links('Assertions',c['assertion_links'])+' · '+links('Result',c['result_links'])+' · '+links('Source',c['source_links'])+'</p>'
            body+=disclosure('criterion-'+c['id'].lower(),f'{esc(c["id"])} · {priority} · {esc(c["title"])}',inner)
        ac_panels.append(disclosure('criteria-'+status.lower(),f'{label} acceptance criteria · {len(rows)}',body,'status-detail'))
    mainhtml=mainhtml.replace('<p><b>Changed-file evidence:</b>',''.join(ac_panels)+'<p><b>Changed-file evidence:</b>',1)
    # Each attention item retains its concise visible summary and reveals proof on demand.
    def attention(m):
        row=m.group(0)
        if 'Logout revocation' in row:i='RN-S002'
        elif 'Recovery dialog' in row:i='REVIEW-E2E-01'
        else:i='RN-R020'
        r=issues[i]
        body=paragraph('Reason',r['reason'])+paragraph('Limits',r['limits'])+paragraph('Next action',r['next_action'])
        body+=f'<p class="note">Owner: {esc(r["owner"])}. '+links('Result',r['result_links'])+' · '+links('Source',r['source_links'])+'</p>'
        return row.replace('</td></tr>',disclosure('attention-'+i.lower(),'Details and evidence',body)+'</td></tr>',1)
    attention_start=mainhtml.index('<table id="attention">');attention_end=mainhtml.index('</table>',attention_start)+len('</table>')
    table=mainhtml[attention_start:attention_end]
    table=re.sub(r'<tr><td[\s\S]*?</tr>',attention,table)
    mainhtml=mainhtml[:attention_start]+table+mainhtml[attention_end:]
    # Review limits are available from their metric card; no new review outcomes are invented.
    reviewbody='<p>The review covers 36 historical changed files and the later Timeout delta. A complete current independent review is unavailable.</p>'
    reviewbody+='<p>Current review priorities retain one P2 session blocker. Other observations are P3/P4, locally closed, or outside this source report.</p>'
    for r in audit['review_entries']:
        inner=paragraph('Reason and impact',r['reason'])+paragraph('Observed',r['observed_user_impact'])
        inner+=paragraph('Evidence limits',r['limits'])+paragraph('Next action',r['next_action'])
        inner+=f'<p class="note">Owner: {esc(r["owner"])}. {link("Finding definition",r["definition"])} · '+links('Result',r['result_links'])+'</p>'
        reviewbody+=disclosure('review-'+r['id'].lower(),f'{esc(r["id"])} · {esc(r["new_priority"])}',inner)
    reviewbody+=link('All review findings and their current priority','10-release-confidence-details.html#priority-register')
    text='Full current independent review unavailable.</small></div>'
    mainhtml=mainhtml.replace(text,'Full current independent review unavailable.</small>'+disclosure('review-details','Review findings and limits',reviewbody)+'</div>',1)
    unitbody='<p>All 471 tests passed across 123 suites. Failed: 0. Skipped: 0. Runner errors: 0.</p>'
    unitbody+='<p>No unit result is partial or blocked in this declared suite. These counts are separate from the 467 expanded cases.</p>'
    unitbody+=link('Full unit execution evidence','evidence/remaining-execution-20261029/full-unit-execution.json')
    text='Zero failures, skips, or runner errors.</small></div>'
    mainhtml=mainhtml.replace(text,'Zero failures, skips, or runner errors.</small>'+disclosure('unit-details','Suite result details',unitbody)+'</div>',1)
    mainhtml=mainhtml.replace('evidence/report-impact-priority-20261029/validation.json',PREFIX+'validation.json')
    (TASK/'10-release-confidence.html').write_text(mainhtml)
    md=baseline('10-release-confidence.md').replace('version: 7\n','version: 8\n',1)
    md=md.replace('## User-impact priority and execution reasons\n',f'## User-impact priority and execution reasons\n\nThe [latest detail request]({REQUEST}) requires collapsed details within the report.\nThe HTML includes separate failed, partial, and blocked case panels. Each panel starts collapsed.\nAdverse acceptance criteria and attention items also include expandable evidence.\n',1)
    md=md.replace('evidence/report-impact-priority-20261029/validation.json',PREFIX+'validation.json')
    md=md.replace('evidence/report-impact-priority-20261029/source-manifest.json',PREFIX+'source-manifest.json')
    (TASK/'10-release-confidence.md').write_text(md)
    index=TASK/'evidence/index.md';s=index.read_text();marker='## Direct evidence\n'
    addition='\nLatest detail instruction: [collapsed result details](user-input-20261029-collapsed-result-details.txt).\nThe [report presentation validation](report-collapsed-details-20261029/validation.json) checks inline details and default collapsed states.\n'
    if addition.strip() not in s:s=s.replace(marker,marker+addition,1)
    index.write_text(s)
    summary={'scope':'Presentation only. No execution, priority, recommendation, or source changes.',
      'request':REQUEST,'cases':len(byid),'statuses':dict(Counter(r['status'] for r in byid.values())),
      'case_groups':len(cases['groups']),'adverse_criteria':4,'blocked_criteria':0,'attention_details':3,
      'main_sha256':hashlib.sha256((TASK/'10-release-confidence.html').read_bytes()).hexdigest(),
      'source_case_audit_sha256':hashlib.sha256((PRIOR/'case-priority-audit.json').read_bytes()).hexdigest()}
    (HERE/'presentation-summary.json').write_text(json.dumps(summary,indent=2)+'\n')

if __name__=='__main__':main()
