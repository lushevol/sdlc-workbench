"""Render plain-language copy without modifying execution or priority evidence."""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
import hashlib,html,json,re,subprocess
HERE=Path(__file__).resolve().parent
TASK=HERE.parent.parent
ROOT=TASK.parent.parent
PRIOR=TASK/'evidence/report-impact-priority-20261029'
CLARITY=TASK/'evidence/report-clarity-20261029'
REQUEST='evidence/user-input-20261030-readable-issues.txt'
PREFIX='evidence/report-readable-issues-20261030/'

def read(path):return json.loads(path.read_text())
def esc(value):return html.escape(str(value),quote=True)
def link(label,href):return f'<a href="{esc(href)}">{esc(label)}</a>'
def links(label,hrefs):return ' · '.join(link(f'{label} {i+1}',h) for i,h in enumerate(hrefs))
def baseline(name):return subprocess.check_output(['git','show','2a332378d:'+str(TASK.relative_to(ROOT)/name)],cwd=ROOT,text=True)
def para(label,text):
    if isinstance(text,list):text=' '.join(text)
    return f'<p><b>{esc(label)}:</b> {esc(text)}</p>' if text else ''
def detail(id,title,body,kind='item-detail'):return f'<details class="{kind}" id="{esc(id)}"><summary>{title}</summary>{body}</details>'

class Spans(HTMLParser):
    VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self,source):
        super().__init__(convert_charrefs=False);self.source=source;self.offsets=[0];self.stack=[];self.spans={}
        for m in re.finditer('\n',source):self.offsets.append(m.end())
        self.feed(source)
    def position(self):
        line,col=self.getpos();return self.offsets[line-1]+col
    def handle_starttag(self,tag,attrs):
        if tag not in self.VOID:self.stack.append((tag,self.position(),dict(attrs).get('id')))
    def handle_endtag(self,tag):
        if not self.stack:return
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==tag:
                item=self.stack[i];self.stack=self.stack[:i]
                if item[2]:self.spans[item[2]]=(item[1],self.source.find('>',self.position())+1)
                return

def replace_ids(source,replacements):
    spans=Spans(source).spans;edits=[]
    for id,value in replacements.items():
        assert id in spans,id
        edits.append((*spans[id],value))
    edits.sort()
    for a,b in zip(edits,edits[1:]):assert a[1]<=b[0],(a[:2],b[:2])
    for start,end,value in reversed(edits):source=source[:start]+value+source[end:]
    return source

def body(copy):
    labels=[('what_happened','What happened'),('reason','Why'),('user_impact','What this means for users'),
            ('missing_check','What still needs checking'),('priority_reason','Why this priority'),
            ('next_action','Next step'),('limits','Test limits')]
    value=''.join(para(label,copy.get(key,'')) for key,label in labels)
    if copy.get('owner'):value+=f'<p class="note">{esc(copy["owner"])}</p>'
    return value

def case_proof(row):
    value=link('Test description',row['definition'])+' · '+link('Test result',row['result'])
    if row.get('assertion_link'):value+=' · '+link('Checks performed',row['assertion_link'])
    if row.get('source_links'):value+=' · '+links('Code',row['source_links'])
    return f'<p class="note">{value}</p>'

def issue_proof(row):
    value=link('Issue definition',row['definition'])
    if row.get('result_links'):value+=' · '+links('Test result',row['result_links'])
    if row.get('source_links'):value+=' · '+links('Code or evidence',row['source_links'])
    if row.get('assertion_links'):value+=' · '+links('Checks performed',row['assertion_links'])
    return f'<p class="note">{value}</p>'

def root_decision(copy):
    return '''<section class="decision" aria-label="Release conclusion"><div class="badge">NO_GO · Sign-out security failure</div>
<p><strong>Signing out does not fully end the session in the server test.</strong></p>
<p>The server says sign-out succeeded, but its saved renewal token can still obtain new access.
This token is also called a refresh credential.</p>
<p>Someone holding a copied renewal token could regain access after sign-out. That token lets the app renew a session.</p>
<p><b>Next step:</b> correct the sign-out code or prove this release cannot reach it. Then repeat the test.</p>
<p class="note">P1 · Potential security impact: High. Production exposure remains unverified. Authentication owner not assigned.
'''+link('Code and test evidence','10-release-confidence.md#failure-rn-s002')+'''.
Confidence in the hold: HIGH, 100/100. This is not a release-readiness score.</p></section>'''

def main():
    cases=read(PRIOR/'case-priority-audit.json');aud=read(PRIOR/'issue-priority-audit.json')
    ac_sources=read(CLARITY/'ac-explanation-audit.json')['criteria']
    group_reviews=read(HERE/'group-review-copy.json');root=read(HERE/'editorial-copy.json')
    combined=read(HERE/'combination-copy.json')
    copy_rows=read(HERE/'case-copy.json')['rows']+(combined if isinstance(combined,list) else combined['rows'])
    copies={r['id']:r for r in copy_rows};byid={r['id']:r for r in cases['rows']}
    assert len(copy_rows)==len(copies)==285 and set(copies)==set(byid)
    groups={r['id']:r for r in group_reviews['groups']};reviews={r['id']:r for r in group_reviews['reviews']}
    issue_copies={r['id']:r for r in group_reviews.get('issues',[])}
    issue_copies.update({id:c for id,c in copies.items() if id in {r['id'] for r in aud['issues']}})
    issue_copies.update(reviews);issue_copies.update({r['id']:r for r in root['attention']})
    allissues=aud['issues']+aud['review_entries']+aud['additional_controls']
    assert all(r['id'] in issue_copies for r in allissues),[r['id'] for r in allissues if r['id'] not in issue_copies]
    ac={r['id']:r for r in root['criteria']};acbyid={r['id']:r for r in ac_sources}
    replacements={}
    for g in cases['groups']:
        c=groups[g['id']];groupbody=para('Why these tests are incomplete' if g['status']!='FAILED' else 'What went wrong',c['reason'])
        groupbody+=para('What this means for users',c['user_impact'])+para('Next step',c['next_action'])
        for id in g['case_ids']:
            row=byid[id];copy=copies[id]
            treatment='This security failure blocks release for the code reviewed.' if row['release_blocking'] else 'This item does not create a separate release hold.'
            groupbody+=detail('case-'+id.lower(),f'{esc(id)} · {esc(row["new_priority"])} · {esc(copy["title"])}',body(copy)+para('Release decision',treatment)+case_proof(row))
        count=g['count'];noun='case' if count==1 else 'cases'
        replacements['group-'+g['id']]=detail('group-'+g['id'],f'{esc(c["title"])} · {count} {noun} · {esc(", ".join(sorted(g["priorities"])))}',groupbody,'reason-detail')
    for row in aud['review_entries']:
        c=reviews[row['id']]
        replacements['review-'+row['id'].lower()]=detail('review-'+row['id'].lower(),f'{row["id"]} · {row["new_priority"]} · {esc(c["title"])}',body(c)+issue_proof(row))
    for c in root['attention']:
        row=next(r for r in allissues if r['id']==c['id'])
        replacements['attention-'+c['id'].lower()]=detail('attention-'+c['id'].lower(),'What happened, impact, and evidence',body(c)+issue_proof(row))
    for id in ['AC-1','AC-2','AC-3','AC-4']:
        c=ac[id];row=acbyid[id];priority='P3' if id=='AC-4' else 'P4'
        proof=link('Requirement',row['definition'])+' · '+links('Checks performed',row['assertion_links'])+' · '+links('Test result',row['result_links'])+' · '+links('Code',row['source_links'])
        replacements['criterion-'+id.lower()]=detail('criterion-'+id.lower(),f'{id} · {priority} · {esc(c["title"])}',body(c)+f'<p class="note">{priority}. This item does not create a separate release hold. Application and test owners not assigned.</p><p class="note">{proof}</p>')
    mainhtml=replace_ids(baseline('10-release-confidence.html'),replacements)
    # The main conclusion, concise table, and criterion table use the same plain descriptions.
    mainhtml=re.sub(r'<section class="decision"[\s\S]*?</section>',root_decision(root['attention'][0]),mainhtml,count=1)
    first={'RN-S002':('High potential security impact','This blocks release for the code reviewed.'),
           'REVIEW-E2E-01':('High potential impact','The test blocked recovery. Check whether a supported application can trigger it.'),
           'RN-R020':('Moderate potential impact','The test cleared a renewed session. Check whether real services can trigger this sequence.')}
    rows=[]
    for c in root['attention']:
        id=c['id'];priority='P1' if id=='RN-S002' else 'P2';rating,treatment=first[id]
        oldspan=Spans(mainhtml).spans['attention-'+id.lower()];disclosure=mainhtml[slice(*oldspan)]
        rows.append(f'<tr><td>{priority} · {esc(c["title"])}<br><span class="note">{rating}</span></td><td>{esc(c["what_happened"])}</td><td>{esc(treatment)} {disclosure}</td></tr>')
    mainhtml=replace_ids(mainhtml,{'attention':'<table id="attention"><thead><tr><th>Priority and issue</th><th>What happened</th><th>Next decision</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table>'})
    # Rewrite the short AC descriptions above the expandable details.
    start=mainhtml.index('<details class="disclosure" id="sdlc-coverage"');table_start=mainhtml.index('<table>',start);table_end=mainhtml.index('</table>',table_start)+len('</table>')
    acrows=[]
    for row in ac_sources:
        c=ac[row['id']];status={'FAILED':'Failed','PARTIAL':'Partial','PASSED':'Passed'}[row['status']]
        summary=c['what_happened']+' '+(c['reason'] if row['status'] in ['FAILED','PARTIAL'] else '')
        acrows.append(f'<tr><td>{link(row["id"],row["definition"])} · {status}</td><td>{esc(summary)} {link("Test result",row["result_links"][0])}</td></tr>')
    mainhtml=mainhtml[:table_start]+'<table><thead><tr><th>Requirement and result</th><th>What the test showed</th></tr></thead><tbody>'+''.join(acrows)+'</tbody></table>'+mainhtml[table_end:]
    mainhtml=simplify_static(mainhtml)
    mainhtml=mainhtml.replace('evidence/report-collapsed-details-20261029/validation.json',PREFIX+'validation.json')
    (TASK/'10-release-confidence.html').write_text(mainhtml)
    make_details(cases,aud,copies,groups,reviews,issue_copies,ac,acbyid,root)
    md=baseline('10-release-confidence.md').replace('version: 8\n','version: 9\n',1)
    md=md.replace('## User-impact priority and execution reasons\n',f'## User-impact priority and execution reasons\n\nThe [latest readability request]({REQUEST}) requires plain-language issue descriptions in both HTML views.\nEach description explains what happened, the user impact, the missing checks, and the next step.\n',1)
    md=md.replace('## Release scope\n','## Release scope\n\nThis wording update retains the recorded source versions; newer server code has not been assessed here.\nThe [source-scope note]('+PREFIX+'source-scope-note.json) records the changed server checkout.\n',1)
    md=md.replace('evidence/report-collapsed-details-20261029/validation.json',PREFIX+'validation.json').replace('evidence/report-collapsed-details-20261029/source-manifest.json',PREFIX+'source-manifest.json')
    (TASK/'10-release-confidence.md').write_text(md)
    index=TASK/'evidence/index.md';text=index.read_text();addition='\nLatest wording instruction: [plain-language issue descriptions](user-input-20261030-readable-issues.txt).\nThe [copy review](report-readable-issues-20261030/peer-review.json) and [validation](report-readable-issues-20261030/validation.json) check this presentation update.\n'
    if addition.strip() not in text:text=text.replace('## Direct evidence\n','## Direct evidence\n'+addition,1)
    index.write_text(text)
    allcopy={'scope':'Wording only; no new execution, priorities, acceptance, or deployment decision.',
      'request':REQUEST,'cases':copy_rows,'groups':list(groups.values()),'reviews':list(reviews.values()),'issues':issue_copies,'criteria':list(ac.values())}
    (HERE/'readable-copy.json').write_text(json.dumps(allcopy,indent=2)+'\n')
    summary={'case_descriptions':len(copies),'reason_groups':len(groups),'review_descriptions':len(reviews),'issue_records':len(allissues),'criteria':7,
       'status_counts':dict(Counter(r['status'] for r in byid.values())),'priorities':dict(Counter(r['new_priority'] for r in byid.values())),
       'release_status':'NO_GO','case_status_changes':0,'priority_changes':0,'new_executions':0}
    (HERE/'presentation-summary.json').write_text(json.dumps(summary,indent=2)+'\n')


def simplify_static(text):
    replacements={
     'P2 items need targeted applicability checks. They are not evidence that every deployed session fails. Owners: unknown application and provider owners.':'For P2 issues, check whether supported applications and services can trigger the tested failure. Responsible owners are not assigned.',
     '<b>Lower priority under your rule:</b> minor activity/loading defects and unproved exposures remain P3/P4 follow-up.':'<b>Lower priority under your rule:</b> minor renewal and loading problems, and risks without proven user harm, remain P3/P4 follow-up.',
     'The 270 partial or blocked cases are verification gaps, not automatic release blockers.':'The 270 partial or blocked cases need more testing. Their incomplete results do not automatically block release.',
     '15 failed:</b> 10 activity-renewal cases, 1 logout-revocation case, 1 loading-indicator case, and 3 conditional security checks.':'15 failed:</b> 10 activity-renewal tests, 1 sign-out security test, 1 loading-indicator test, and 3 other security tests.',
     '199 partial:</b> 181 combination cases lack real business-write checks; 18 lack specific service, lifecycle, or observation checks.':'199 partial:</b> 181 combined-condition tests did not check real business updates. Another 18 need specific service or browser checks.',
     '71 blocked:</b> required services, native controls, or exact test bindings were unavailable. This does not prove application failure.':'71 blocked:</b> required services, browser or device controls, or complete test steps were unavailable. This does not prove application failure.',
     'Current triage for these 285 cases: 1 P1 blocker, 273 P3 follow-ups, and 11 P4 backlog cases.':'Current priorities for these 285 cases: 1 P1 blocker, 273 P3 follow-ups, and 11 P4 backlog items.',
     'Case results: failure reasons and missing verification':'Case results: what failed and what still needs testing',
     'SDLC coverage and acceptance-criterion explanations':'Requirements, test coverage, and reasons for incomplete results',
     'All 7 criteria have test and code associations. Three have bounded implementation matches; one is partial; three have gaps.':'All 7 requirements link to code and tests. Three match the tested behavior; one is only partly verified; three have gaps.',
     'No acceptance criterion has a blocked disposition. AC-4 remains partial because specific verification is missing.':'No requirement has a blocked result. AC-4 is partial because the real sign-in and protected-service checks are missing.',
     '<b>Changed-file evidence:</b> each of 12 changed runtime source files has at least one inspected passing test.':'<b>Changed-file evidence:</b> each of 12 changed application files has at least one checked test that passed.',
     'This does not prove complete behavior coverage.':'This does not prove that every changed behavior works.',
     'The review covers 36 historical changed files and the later Timeout delta. A complete current independent review is unavailable.':'An earlier review covered 36 changed files. The later Timeout change was also inspected. A complete independent review of the current code is unavailable.',
     'Current review priorities retain one P2 session blocker. Other observations are P3/P4, locally closed, or outside this source report.':'One review issue remains P2 because its browser test blocked recovery. Other findings are lower priority, corrected locally, or outside this report.',
     'No unit result is partial or blocked in this declared suite. These counts are separate from the 467 expanded cases.':'No unit test is partial or blocked in this suite. These counts are separate from the 467 release test cases.',
     'Source assessment; release artifacts excluded.':'This report assesses code and tests. Release artifacts are excluded.',
     'Historical code review':'Earlier code review',
     'Complete case results':'Cases with a final result',
     'Acceptance criteria passed':'Requirements passed in local tests',
     'Complete behavior coverage is unknown.':'Some required behavior remains unverified.',
     'Full current independent review unavailable.':'No complete independent review of the current code.',
     'Later Timeout change also inspected.':'The later Timeout change was also inspected.',
     'Code or evidence':'Code or test evidence',
    }
    for old,new in replacements.items():text=text.replace(old,new)
    for finding in read(HERE/'static-copy-review.json')['findings']:
        pairs={finding['find']:finding['replace'],**finding.get('also_replace',{})}
        for old,new in pairs.items():
            text=re.sub(r'\s+'.join(re.escape(word) for word in old.split()),lambda _:new,text)
    text=text.replace('Case ID or words, such as renewal or transport','Case ID or words, such as renewal or sign-out')
    text=text.replace('ASD writing review: PENDING.',
        'This wording update retains the recorded source versions; newer server code has not been assessed here. '
        +link('Source scope',PREFIX+'source-scope-note.json')+'. ASD writing review: PENDING.')
    return text


def make_details(cases,aud,copies,groups,reviews,issue_copies,ac,acbyid,root):
    text=baseline('10-release-confidence-details.html')
    replacements={}
    for status,id in [('FAILED','failed-reasons'),('PARTIALLY_EXECUTED','partial-reasons'),('BLOCKED','blocked-reasons')]:
        label={'FAILED':'Why 15 tests failed','PARTIALLY_EXECUTED':'Why 199 tests are incomplete','BLOCKED':'Why 71 tests could not finish'}[status]
        cards=[]
        for g in cases['groups']:
            if g['status']!=status:continue
            c=groups[g['id']];proof=' · '.join(link(x, next(r['result'] for r in cases['rows'] if r['id']==x)) for x in g['case_ids'][:3])
            title=f'{esc(c["title"])} · {g["count"]} '+('case' if g['count']==1 else 'cases')
            cards.append(f'<article class="reason-card"><h3>{title}</h3><p><b>Priority:</b> {esc(", ".join(sorted(g["priorities"])))}.</p>'+para('Why',c['reason'])+para('What this means for users',c['user_impact'])+para('Next step',c['next_action'])+f'<p class="note">{proof}</p><button class="text-button group-button" data-group="{g["id"]}">Show these cases ↓</button></article>')
        replacements[id]=f'<section id="{id}"><h2>{label}</h2><div class="reason-grid">'+''.join(cards)+'</div></section>'
    issue_rows=[]
    for row in aud['issues']+aud['review_entries']+aud['additional_controls']:
        c=issue_copies[row['id']];priority=row['new_priority']
        if priority=='NONE_CLOSED':priority='Corrected in local tests'
        if priority=='NOT_A_DEFECT_PRIORITY':priority='Separate authorization record'
        issue_rows.append(f'<tr><td>{link(row["id"],row["definition"])}<br>{esc(c["title"])}<br><b>{esc(priority)}</b></td><td>'+body(c)+issue_proof(row)+'</td></tr>')
    replacements['priority-register']='<section id="priority-register"><h2>Issue priorities and explanations</h2><p>Some records describe the same problem. They are not separate defects.</p><p>The priorities below apply now. Potential severity remains separate from priority.</p><table class="case-table"><thead><tr><th>Issue and priority</th><th>What happened and what users could experience</th></tr></thead><tbody>'+''.join(issue_rows)+'</tbody></table></section>'
    text=replace_ids(text,replacements)
    def row(m):
        old=m.group(0);id=html.unescape(re.search(r'06-test-cases.md#[^\"]+\">([^<]+)</a>',old).group(1))
        c=copies[id];r=next(x for x in cases['rows'] if x['id']==id)
        status={'FAILED':'Failed','PARTIALLY_EXECUTED':'Partial','BLOCKED':'Blocked'}[r['status']]
        cls={'FAILED':'failed','PARTIALLY_EXECUTED':'partial','BLOCKED':'blocked'}[r['status']]
        search=' '.join([id]+[value for value in c.values() if isinstance(value,str)]).lower()
        return f'<tr class="case-row" data-status="{r["status"]}" data-group="{r["group_id"]}" data-search="{esc(search)}"><td><b>{link(id,r["definition"])}</b><span class="status {cls}">{status}</span><p>{esc(c["title"])}</p><p>{r["new_priority"]}</p></td><td>'+body(c)+case_proof(r)+'</td></tr>'
    text,n=re.subn(r'<tr class="case-row"[\s\S]*?</tr>',row,text);assert n==285
    text=re.sub(r'<section class="decision"[\s\S]*?</section>',root_decision(root['attention'][0]),text,count=1)
    acrows=[]
    for id,c in ac.items():
        r=acbyid[id];status={'FAILED':'Failed','PARTIAL':'Partial','PASSED':'Passed'}[r['status']]
        acrows.append(f'<tr><td>{link(id,r["definition"])} · {status}<p>{esc(c["title"])}</p></td><td>'+body(c)+f'<p class="note">'+links('Test result',r['result_links'])+' · '+links('Code',r['source_links'])+'</p></td></tr>')
    section='<section id="acceptance-criteria"><h2>Requirement results explained</h2><p>Three requirements passed the local checks, three failed, and one is partial.</p><table class="ac-table"><thead><tr><th>Requirement and result</th><th>What happened and why</th></tr></thead><tbody>'+''.join(acrows)+'</tbody></table></section>'
    text=replace_ids(text,{'acceptance-criteria':section})
    text=simplify_static(text).replace('evidence/report-impact-priority-20261029/validation.json',PREFIX+'validation.json')
    text=text.replace('This update explains existing results. It adds no test execution or deployment approval.','This wording update uses existing test results. It does not add tests or approve deployment.')
    (TASK/'10-release-confidence-details.html').write_text(text)

if __name__=='__main__':main()
