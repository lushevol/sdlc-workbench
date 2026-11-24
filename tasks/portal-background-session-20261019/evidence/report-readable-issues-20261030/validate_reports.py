"""Validate the wording update without changing historical audits or execution evidence.

Run only after report rendering, peer review, and the current HTML QA are complete.
The checks cover presentation consistency. They do not rerun application tests.
"""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import datetime
import hashlib
import html
import json
import re
import subprocess
from collections import Counter
from html.parser import HTMLParser

HERE=Path(__file__).resolve().parent
TASK=HERE.parent.parent
ROOT=TASK.parent.parent
RUN=TASK/'evidence/remaining-execution-20261029'
OLD=TASK/'evidence/release-report-execution-20261029'
CLARITY=TASK/'evidence/report-clarity-20261029'
PRIOR=TASK/'evidence/report-impact-priority-20261029'
COLLAPSED=TASK/'evidence/report-collapsed-details-20261029'
REQUEST=TASK/'evidence/user-input-20261030-readable-issues.txt'
BASELINE_REVISION='2a332378d'
# Prior audit bytes captured when this wording-only validator was authored.
PRESERVED_PRIOR_HASHES={'evidence/report-collapsed-details-20261029/collapsed-default.png': '93ed4607c9a3b15e5b5758c68b7edc9859f7f22e45aca4b88b9d6702c61cec82', 'evidence/report-collapsed-details-20261029/expanded-criterion.png': '8341ad4a8c83a814185a673fdb7315b0987c5fa01e4c54f7c5dcfe091c12855a', 'evidence/report-collapsed-details-20261029/expanded-failure.png': '2f776be4a77c746a89f8f0ede891acd529fb35cf5196569b6a92319143f9a0ac', 'evidence/report-collapsed-details-20261029/html-qa.json': '524b2234ffbfa08d01939f70266970fd8c16525e5bfb1e9ef0fc01326f38085e', 'evidence/report-collapsed-details-20261029/html_qa.mjs': '4b37486bd910e416bb0b30c8bca827afb6829b1202903226a0a88eced91dcff0', 'evidence/report-collapsed-details-20261029/peer-review.json': 'b46fdfc7589483bc0ac9a60b6bc7d4ec8fdc887cb78df164d559c39ab0d495bb', 'evidence/report-collapsed-details-20261029/presentation-summary.json': 'c68f6d0994f677b39211b68e975f69501180365770b57fefd3b4fd21cbbbb2fb', 'evidence/report-collapsed-details-20261029/source-manifest.json': '460e67027df700505fe24f21b0fe95a3cf3d8575a00cce8c191ee3e8c1bcae2b', 'evidence/report-collapsed-details-20261029/update_report.py': '0d66eaf4e471c8db5c38fc8b1a4e73b01b72717e7c98c5e633af055941adc237', 'evidence/report-collapsed-details-20261029/validate_reports.py': '4c13ae6444e679db776107ae17fec3d50e5b8663af46ea751f181ff5684d556c', 'evidence/report-collapsed-details-20261029/validation.json': '27c7067d7f68093fc992a458cef84d0a4140eafdf3adb190874cc9e8fa7b0dd1', 'evidence/report-impact-priority-20261029/build_case_priorities.py': 'b5bced1c0f370568742e3a6628dfba7dff63d74d2441eca4f9a064b049aa43d2', 'evidence/report-impact-priority-20261029/build_priority_audit.py': '3ab56f53ea3be90f1c90fce99bcd92411095aac21a699056af4a41f30ded862a', 'evidence/report-impact-priority-20261029/case-priority-audit.json': '0907697c3d1c5f68b9db1d4a72a95d59c2b24cc435c92f9b5509fafafe4ea493', 'evidence/report-impact-priority-20261029/case-priority-validation.json': '1e3668da69ad19d47c91c7cc1029ed0465186ae594f48f8f8805c1fcbd610dca', 'evidence/report-impact-priority-20261029/expanded-coverage.png': 'f53eadd5a343acd72e792eb0134e35b59b70d7cc352312d0d07a56e3fa0632f6', 'evidence/report-impact-priority-20261029/html-qa.json': '4c3bc6873b9c7b3fef617e14311bf472b72e2a986d458ef90d2ea43c273c18f0', 'evidence/report-impact-priority-20261029/html_qa.mjs': '82e2ae1f2e2cdf0d51d01e836e7c4bc869932438c385669091f0a1c3a212ef02', 'evidence/report-impact-priority-20261029/issue-priorities.png': '30dd5b99c1de984f67823c8aa00598f3ecf7e8a68d6e60880a53fe199d5cffca', 'evidence/report-impact-priority-20261029/issue-priority-audit.json': '3689b4e0c808e87c657c2e303f28128fd455432df974b639c533735133b175f3', 'evidence/report-impact-priority-20261029/main-1280.png': '4802e42efe86c5a88a967aad4b9004cc22b9bea07828a80f1c255367c3d17957', 'evidence/report-impact-priority-20261029/main-390.png': 'a5870efd86fe3c4b0f71076adea5e56059a1458768ff637fd92808dd970dd127', 'evidence/report-impact-priority-20261029/main-715.png': 'bf34d2d7757d7868dec76ec9d35ea9b2e01469555b440ebe5bfde94d691aaf48', 'evidence/report-impact-priority-20261029/peer-review.json': 'd84f320af03f766ecaa80baa229437034908cdd4184a10d95f80915969d23838', 'evidence/report-impact-priority-20261029/presentation-summary.json': 'c3f57094bd1ed854fd7843c0baaaccf495e2b9f5022e8ebd77d4d8ab2cfb3935', 'evidence/report-impact-priority-20261029/render_report.py': '68ead3d60aeace5cb78ac7a4428caf4817d018c0ecef44b770656b07a3305ceb', 'evidence/report-impact-priority-20261029/report-template.html': 'cb2e743e08bde173b11ac58a7ee622c8b9ac3873b80a853181a0f845bfb1ac69', 'evidence/report-impact-priority-20261029/source-manifest.json': '317d5d64f7935d5537269b13082d2fa9ca76903d5c6e503cc5385fded43ebc54', 'evidence/report-impact-priority-20261029/validate_reports.py': '13eb7c2def822527bc68e84f19e5d0abde1e401925c3cb4638942441a33fb8ab', 'evidence/report-impact-priority-20261029/validation.json': 'e6a0c617774933e39d6cd03b524393c8827c62e116c83205446a20933bb2be06', 'evidence/report-clarity-20261029/ac-explanation-audit.json': 'c9adc8bfa7bbe6daac4d71f7f026636dd25e3a6fd5212e17b8a30595bd4b755f', 'evidence/report-clarity-20261029/build_execution_reasons.py': '3ec1ce7ca33cac283c140191878a5edac92e0e7f4e31066f546416e14ca30769', 'evidence/report-clarity-20261029/cases-1280.png': '1048eb4cf1757b7454a62fa2a7dcfbb5094f25cea0cdc39e11df613b45c73a2e', 'evidence/report-clarity-20261029/cases-390.png': 'dec987d2b93af9632b63dd1eca696d8e406e3c263f5fff7a33d2076bb087727f', 'evidence/report-clarity-20261029/cases-715.png': '9251181b34ae04d7737895f5ebb7d93877f5dea8e25344e84e50dad6d1c2b239', 'evidence/report-clarity-20261029/criteria-1280.png': '28efc378a74ca4f0b20f7721efddd9134a3bad468a1f064bef03c9e5c736d601', 'evidence/report-clarity-20261029/criteria-390.png': '3107350cca3d472a0897e1019025a08159c2bdda04e7385576f81836d906e42c', 'evidence/report-clarity-20261029/criteria-715.png': 'b00435c14c67d7343ee13ec5a06d461e4fe69c40f6afebeec5b490a4e7141644', 'evidence/report-clarity-20261029/execution-reason-audit.json': 'e5cfc9e5f695d20f84a0fb80c1718088f18037afc323b07bdb14369265af8fea', 'evidence/report-clarity-20261029/execution-reason-validation.json': '14ce1a7e9b364d6d4411a9c400a9983fa8c606a64f8ca80eb98f332911e8ef26', 'evidence/report-clarity-20261029/html-1280.png': '920367df22a92cd419fc2d95f42368dc615ea2a578986f6362241222cf6f6ecd', 'evidence/report-clarity-20261029/html-qa.json': '4f6a61065b86ec4bd76c7d4a1b5279a1a57fef0d0663114b467b438b46ea8527', 'evidence/report-clarity-20261029/html_qa.mjs': '821a00f89a4b63f176feb3034e7d6e540d3883cff893b2f03e05ee3131d66a31', 'evidence/report-clarity-20261029/peer-review.json': 'be0d61f2dd052a124203995f49a60fc5f9ac18bf51c61a6bc5d591214174d0ca', 'evidence/report-clarity-20261029/presentation-summary.json': 'cb8c575fc539312e90cde4efbb09f2403bfe23bfab052163fa7604eba00f1da5', 'evidence/report-clarity-20261029/render_clarity.py': '055d37092a21a6a5c503dbaaec2723d08d651a862d4745671faf324dd50c7304', 'evidence/report-clarity-20261029/report-template.html': 'c4c9869a6e418a13f1fb13feb3c741e20d235311931a32252893ddbd160fb001', 'evidence/report-clarity-20261029/source-manifest.json': '336ab9d46b24a4a64685f88ebc6908ab16f39122c90b0bee17016fba98d0bfbc', 'evidence/report-clarity-20261029/top-1280.png': '549821595069e764befcc5842d17f926a1a0086d018ffe133ff85014ac90b639', 'evidence/report-clarity-20261029/top-390.png': 'f74420c28d26320eb3b315d5183cb329e11da24815d67adf8670bee2c064a1d9', 'evidence/report-clarity-20261029/top-715.png': '6a3b1117df13bfb3470e5ac9d0b051fa03fc46b80c0d7754314c822298e8093d', 'evidence/report-clarity-20261029/validate_reports.py': 'e7e1d9a4d9637c90a6d6770524c26df9b98bed3aca381c81fc414bc326686e08', 'evidence/report-clarity-20261029/validation.json': '32b4574637fd34760d3cb788946767c5cae3db17d33804ef7f42163ebdc897fe'}
COPY_FIELDS=['what_happened','reason','user_impact','missing_check',
             'priority_reason','next_action','limits','owner']
DOCUMENTS=[TASK/n for n in ['08-test-execution-renewal.md','09-renewal-coverage.md',
                           '10-release-confidence.md','10-release-confidence.html','10-release-confidence-details.html',
                           '10-issue-catalog.md','evidence/index.md']]+[ROOT/'AGENTS.md']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def slug(text):
    text=re.sub('<[^>]*>','',text)
    return re.sub(r'[^\w\- ]','',text.lower()).replace(' ','-')


def normalized(value):
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]*>',' ',value))).strip()


class ReportNodes(HTMLParser):
    """Retain element spans for the report's existing IDs and disclosures."""
    VOID={'area','base','br','col','embed','hr','img','input','link',
          'meta','param','source','track','wbr'}

    def __init__(self,source):
        super().__init__(convert_charrefs=False)
        self.source=source;self.offsets=[0];self.stack=[]
        self.nodes={};self.details=[];self.duplicate_ids=[]
        for match in re.finditer('\n',source):self.offsets.append(match.end())
        self.feed(source)
        self.close()

    def position(self):
        line,column=self.getpos()
        return self.offsets[line-1]+column

    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        node={'tag':tag,'attrs':attrs,'start':self.position()}
        if tag=='details':self.details.append(node)
        id=attrs.get('id')
        if id:
            if id in self.nodes:self.duplicate_ids.append(id)
            self.nodes[id]=node
        if tag not in self.VOID:self.stack.append(node)

    def handle_endtag(self,tag):
        for index in range(len(self.stack)-1,-1,-1):
            if self.stack[index]['tag']==tag:
                node=self.stack[index]
                node['end']=self.source.find('>',self.position())+1
                node['html']=self.source[node['start']:node['end']]
                self.stack=self.stack[:index]
                return


def read_json(path):
    return json.loads(path.read_text())


def read_copy_rows(path):
    value=read_json(path)
    return value['rows'] if isinstance(value,dict) else value


def validate_readability(errors):
    """Compare display text with retained sources and the prior presentation."""
    checks={}
    required=[HERE/'readable-copy.json',HERE/'presentation-summary.json',
              HERE/'case-copy.json',HERE/'combination-copy.json',
              HERE/'group-review-copy.json',HERE/'editorial-copy.json']
    absent=[str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if absent:
        errors.append({'type':'missing-readability-output','paths':absent})
        return {'status':'INCOMPLETE','missing_outputs':absent}
    copy=read_json(HERE/'readable-copy.json')
    cases=read_json(PRIOR/'case-priority-audit.json')
    issues=read_json(PRIOR/'issue-priority-audit.json')
    criteria=read_json(CLARITY/'ac-explanation-audit.json')['criteria']
    source_cases={row['id']:row for row in cases['rows']}
    source_issues={row['id']:row for row in issues['issues']+issues['review_entries']+issues['additional_controls']}
    source_groups={row['id']:row for row in cases['groups']}
    source_criteria={row['id']:row for row in criteria}
    copy_cases={row['id']:row for row in copy['cases']}
    copy_groups={row['id']:row for row in copy['groups']}
    copy_issues=copy['issues']
    if isinstance(copy_issues,list):copy_issues={row['id']:row for row in copy_issues}
    copy_criteria={row['id']:row for row in copy['criteria']}
    copy_reviews={row['id']:row for row in copy['reviews']}
    for name,actual,expected,count in [
        ('cases',copy_cases,source_cases,285),('issues',copy_issues,source_issues,62),
        ('groups',copy_groups,source_groups,21),('criteria',copy_criteria,source_criteria,7),
        ('reviews',copy_reviews,{row['id']:row for row in issues['review_entries']},18)]:
        checks[name]={'expected':count,'actual':len(actual),
                      'missing':sorted(set(expected)-set(actual)),
                      'extra':sorted(set(actual)-set(expected))}
        if len(actual)!=count or set(actual)!=set(expected):
            errors.append({'type':'copy-coverage-mismatch','kind':name,**checks[name]})
    constituent=read_copy_rows(HERE/'case-copy.json')+read_copy_rows(HERE/'combination-copy.json')
    if len(copy['cases'])!=285 or len(constituent)!=285 or len({r['id'] for r in constituent})!=285:
        errors.append({'type':'duplicate-or-missing-case-copy'})
    if {row['id']:row for row in constituent}!=copy_cases:
        errors.append({'type':'consolidated-case-copy-mismatch'})
    for row in copy_cases.values():
        absent_fields=[field for field in ['title']+COPY_FIELDS if not row.get(field)]
        if absent_fields:errors.append({'type':'missing-case-explanation','id':row['id'],'fields':absent_fields})
    # Copy records may retain machine status fields. If present, they must agree.
    for collection,source in [(copy_cases,source_cases),(copy_issues,source_issues),(copy_criteria,source_criteria)]:
        for id,row in collection.items():
            if id not in source:continue
            for field in ['status','new_priority','release_blocking']:
                if field in row and field in source[id] and row[field]!=source[id][field]:
                    errors.append({'type':'copy-disposition-changed','id':id,'field':field})
    sentence_findings=[];paragraph_findings=[]
    for kind,rows in [('case',copy_cases),('issue',copy_issues),('group',copy_groups),('criterion',copy_criteria)]:
        for id,row in rows.items():
            for field in COPY_FIELDS:
                text=row.get(field,'')
                for paragraph in text.split('\n\n'):
                    sentences=[s for s in re.split(r'(?<=[.!?])\s+',paragraph) if s.strip()]
                    if len(sentences)>6:paragraph_findings.append({'kind':kind,'id':id,'field':field,'sentences':len(sentences)})
                    for sentence in sentences:
                        if len(sentence.split())>20:
                            sentence_findings.append({'kind':kind,'id':id,'field':field,'words':len(sentence.split()),'text':sentence})
    if sentence_findings:errors.append({'type':'copy-sentence-length','rows':sentence_findings})
    if paragraph_findings:errors.append({'type':'copy-paragraph-length','rows':paragraph_findings})
    checks['readability']={'sentences_over_20_words':len(sentence_findings),
                           'paragraphs_over_six_sentences':len(paragraph_findings),
                           'asd_review':'PENDING'}
    main=(TASK/'10-release-confidence.html').read_text()
    detail=(TASK/'10-release-confidence-details.html').read_text()
    reports={name:(text,ReportNodes(text)) for name,text in [('main',main),('details',detail)]}
    for name,(text,nodes) in reports.items():
        baseline=subprocess.check_output(['git','show',BASELINE_REVISION+':'+str(TASK.relative_to(ROOT)/('10-release-confidence.html' if name=='main' else '10-release-confidence-details.html'))],cwd=ROOT,text=True)
        for block in ['style','script']:
            old=re.findall(r'<'+block+r'\b[^>]*>([\s\S]*?)</'+block+r'>',baseline)
            new=re.findall(r'<'+block+r'\b[^>]*>([\s\S]*?)</'+block+r'>',text)
            if old!=new:errors.append({'type':'layout-or-behavior-changed','report':name,'block':block})
        if nodes.duplicate_ids:errors.append({'type':'duplicate-html-id','report':name,'ids':nodes.duplicate_ids})
        if any('open' in node['attrs'] for node in nodes.details):
            errors.append({'type':'detail-open-by-default','report':name})
        if 'NO_GO' not in text or '100/100' not in text:
            errors.append({'type':'release-conclusion-changed','report':name})
        checks[name]={'detail_count':len(nodes.details),'open_by_default':sum('open' in d['attrs'] for d in nodes.details),
                      'style_and_script_baseline':BASELINE_REVISION}
    main_nodes=reports['main'][1]
    if len(main_nodes.details)!=341:errors.append({'type':'main-disclosure-count','expected':341,'actual':len(main_nodes.details)})

    def require_text(fragment,copy_row,location,fields=None):
        for field in fields or ['title']+COPY_FIELDS:
            value=copy_row.get(field,'')
            if value and normalized(value) not in normalized(fragment):
                errors.append({'type':'rendered-copy-missing','location':location,'id':copy_row['id'],'field':field})

    def require_links(fragment,row,location,kind):
        hrefs=re.findall(r'(?:href|src)=["\']([^"\']+)["\']',fragment)
        hrefs={html.unescape(href) for href in hrefs}
        expected=[row['definition']]
        if kind=='case':expected.append(row['result'])
        if kind=='case' and row.get('assertion_link'):expected.append(row['assertion_link'])
        expected.extend(row.get('result_links',[]))
        expected.extend(row.get('assertion_links',[]))
        expected.extend(row.get('source_links',[]))
        for href in expected:
            if href not in hrefs:
                errors.append({'type':'retained-evidence-link-missing','location':location,'id':row['id'],'link':href})

    for id,row in source_cases.items():
        node=main_nodes.nodes.get('case-'+id.lower(),{})
        fragment=node.get('html','')
        if not fragment:errors.append({'type':'missing-inline-case','id':id});continue
        require_text(fragment,copy_cases[id],'main case')
        require_links(fragment,row,'main case','case')
        summary=re.search(r'<summary[^>]*>([\s\S]*?)</summary>',fragment)
        if not summary or f"{id} · {row['new_priority']} ·" not in normalized(summary[1]):
            errors.append({'type':'rendered-case-priority-changed','id':id})
    for id,row in source_groups.items():
        fragment=main_nodes.nodes.get('group-'+id,{}).get('html','')
        require_text(fragment,copy_groups[id],'main group',['title','reason','user_impact','next_action'])
        for case_id in row['case_ids']:
            if 'id="case-'+case_id.lower()+'"' not in fragment:
                errors.append({'type':'case-group-changed','group':id,'id':case_id})
    for id in ['AC-1','AC-2','AC-3','AC-4']:
        fragment=main_nodes.nodes.get('criterion-'+id.lower(),{}).get('html','')
        require_text(fragment,copy_criteria[id],'main criterion')
        require_links(fragment,source_criteria[id],'main criterion','criterion')
    for id,row in copy_reviews.items():
        fragment=main_nodes.nodes.get('review-'+id.lower(),{}).get('html','')
        require_text(fragment,row,'main review')
        require_links(fragment,source_issues[id],'main review','issue')
    for id in ['RN-S002','REVIEW-E2E-01','RN-R020']:
        fragment=main_nodes.nodes.get('attention-'+id.lower(),{}).get('html','')
        require_text(fragment,copy_issues[id],'main attention',COPY_FIELDS)
        require_text(main_nodes.nodes['attention']['html'],copy_issues[id],'main attention table',['title'])
        require_links(fragment,source_issues[id],'main attention','issue')
    case_rows=re.findall(r'<tr class="case-row"[\s\S]*?</tr>',detail)
    rendered_cases={}
    for fragment in case_rows:
        first=re.search(r'<a\b[^>]*>([^<]+)</a>',fragment)
        if first:rendered_cases[html.unescape(first[1])]=fragment
    if len(case_rows)!=285 or set(rendered_cases)!=set(source_cases):
        errors.append({'type':'detail-case-coverage','rows':len(case_rows),'unique':len(rendered_cases)})
    for id,row in source_cases.items():
        fragment=rendered_cases.get(id,'')
        require_text(fragment,copy_cases[id],'details case')
        require_links(fragment,row,'details case','case')
        if f'data-status="{row["status"]}"' not in fragment or f'data-group="{row["group_id"]}"' not in fragment:
            errors.append({'type':'rendered-case-status-or-group-changed','id':id})
        if f'<p>{row["new_priority"]}</p>' not in fragment:
            errors.append({'type':'details-case-priority-changed','id':id})
    for section,sources,copies,kind in [('priority-register',source_issues,copy_issues,'issue'),
                                         ('acceptance-criteria',source_criteria,copy_criteria,'criterion')]:
        section_html=reports['details'][1].nodes.get(section,{}).get('html','')
        rendered={}
        for fragment in re.findall(r'<tr\b[^>]*>[\s\S]*?</tr>',section_html):
            first=re.search(r'<a\b[^>]*>([^<]+)</a>',fragment)
            if first:rendered[html.unescape(first[1])]=fragment
        if set(rendered)!=set(sources):errors.append({'type':'rendered-register-coverage','section':section,'actual':len(rendered),'expected':len(sources)})
        for id,row in sources.items():
            fragment=rendered.get(id,'')
            require_text(fragment,copies[id],section)
            # The detailed AC view retains result and code links; main AC panels retain assertions.
            required=row if kind=='issue' else {key:value for key,value in row.items() if key not in ['assertion_links']}
            require_links(fragment,required,section,kind)
            if kind=='issue':
                display={'NONE_CLOSED':'Corrected in local tests','NOT_A_DEFECT_PRIORITY':'Separate authorization record'}.get(row['new_priority'],row['new_priority'])
                if f'<b>{display}</b>' not in fragment:errors.append({'type':'rendered-issue-priority-changed','id':id})
            else:
                display={'FAILED':'Failed','PARTIAL':'Partial','PASSED':'Passed'}[row['status']]
                if f' · {display}' not in fragment:errors.append({'type':'rendered-criterion-status-changed','id':id})
    summary=read_json(HERE/'presentation-summary.json')
    expected_summary={'case_descriptions':285,'reason_groups':21,'review_descriptions':18,
                      'issue_records':62,'criteria':7,'release_status':'NO_GO',
                      'case_status_changes':0,'priority_changes':0,'new_executions':0}
    for key,value in expected_summary.items():
        if summary.get(key)!=value:errors.append({'type':'presentation-summary-mismatch','field':key})
    if summary.get('status_counts')!=dict(Counter(row['status'] for row in source_cases.values())):
        errors.append({'type':'presentation-status-count-mismatch'})
    if summary.get('priorities')!=dict(Counter(row['new_priority'] for row in source_cases.values())):
        errors.append({'type':'presentation-priority-count-mismatch'})
    for value in ['197/467','3/7','36 files','471/471']:
        if value not in main:errors.append({'type':'essential-metric-changed','value':value})
    request='Rewrite all the issue descriptions in this HTML report so they are easy for people to read.'
    if not REQUEST.is_file() or request not in REQUEST.read_text():errors.append({'type':'readability-request-not-preserved'})
    if 'evidence/user-input-20261030-readable-issues.txt' not in (TASK/'10-release-confidence.md').read_text():
        errors.append({'type':'active-report-request-link-missing'})
    changed=[]
    for name,expected in PRESERVED_PRIOR_HASHES.items():
        path=TASK/name
        if not path.is_file() or sha(path)!=expected:changed.append(name)
    if changed:errors.append({'type':'prior-audit-bytes-changed','paths':changed})
    checks['prior_audits']={'files_checked':len(PRESERVED_PRIOR_HASHES),'changed':changed}
    checks['request']={'path':str(REQUEST.relative_to(TASK)),'sha256':sha(REQUEST)}
    return checks


def main():
    errors=[];warnings=[];commands=[];checked=0;referenced=set()
    readability=validate_readability(errors)
    for doc in DOCUMENTS:
        body=doc.read_text()
        links=re.findall(r'\]\(([^)\s]+)(?:\s+"[^"]*")?\)',body)
        links+=re.findall(r'(?:href|src)=["\']([^"\']+)["\']',body)
        for raw in links:
            raw=html.unescape(raw.strip('<>'))
            parsed=urlsplit(raw)
            if parsed.scheme or raw.startswith('//'):
                continue
            target=(doc.parent/unquote(parsed.path)).resolve() if parsed.path else doc
            checked+=1
            if not target.is_file():
                errors.append({'type':'missing-link-target','document':str(doc.relative_to(ROOT)),'link':raw})
                continue
            referenced.add(target)
            fragment=unquote(parsed.fragment)
            if not fragment:continue
            text=target.read_text(errors='replace')
            line=re.fullmatch(r'L(\d+)(?:-L?(\d+))?',fragment)
            if line:
                first,last=int(line[1]),int(line[2] or line[1])
                if not 1<=first<=last<=len(text.splitlines()):
                    errors.append({'type':'invalid-line-locator','link':raw})
            elif target.suffix.lower() in ['.md','.html']:
                anchors=set(re.findall(r'id=["\']([^"\']+)["\']',text))
                anchors.update(slug(m) for m in re.findall(r'^#{1,6}\s+(.+?)\s*#*$',text,re.M))
                if fragment not in anchors:
                    errors.append({'type':'missing-anchor','document':str(doc.relative_to(ROOT)),'link':raw})
    for doc in DOCUMENTS[:3]+[TASK/'10-issue-catalog.md']:
        args=[str(ROOT/'.venv/bin/ai-sdlc'),'lint',str(doc.relative_to(ROOT))]
        p=subprocess.run(args,cwd=ROOT,text=True,capture_output=True)
        result=json.loads(p.stdout) if p.stdout.strip().startswith('{') else p.stdout+p.stderr
        commands.append({'command':args,'exit_code':p.returncode,'result':result})
        if p.returncode:errors.append({'type':'artifact-lint','path':str(doc),'exit_code':p.returncode})
    for args in [[str(ROOT/'.venv/bin/ai-sdlc'),'--workspace',str(ROOT),'validate'],['git','diff','--check']]:
        p=subprocess.run(args,cwd=ROOT,text=True,capture_output=True)
        result=json.loads(p.stdout) if p.stdout.strip().startswith('{') else p.stdout+p.stderr
        commands.append({'command':args,'exit_code':p.returncode,'result':result})
        if p.returncode:errors.append({'type':'command','command':args,'exit_code':p.returncode})
    audit=json.loads((CLARITY/'execution-reason-audit.json').read_text())
    criteria=json.loads((CLARITY/'ac-explanation-audit.json').read_text())['criteria']
    if Counter(r['status'] for r in audit['rows'])!={'FAILED':15,'PARTIALLY_EXECUTED':199,'BLOCKED':71}:
        errors.append({'type':'explanation-count-mismatch'})
    if len(criteria)!=7:errors.append({'type':'criterion-count-mismatch'})
    case_priorities=json.loads((PRIOR/'case-priority-audit.json').read_text())
    issue_priorities=json.loads((PRIOR/'issue-priority-audit.json').read_text())
    issue_rows=issue_priorities['issues']+issue_priorities['review_entries']+issue_priorities['additional_controls']
    byid={r['id']:r for r in case_priorities['rows']}
    for row in issue_rows:
        if row['id'] in byid and row['new_priority']!=byid[row['id']]['new_priority']:
            errors.append({'type':'priority-mismatch','id':row['id']})
    if len(byid)!=285 or Counter(r['new_priority'] for r in byid.values())!={'P1':1,'P3':273,'P4':11}:
        errors.append({'type':'priority-count-mismatch'})
    for row in audit['rows']:
        if byid[row['id']]['status']!=row['status']:
            errors.append({'type':'execution-status-changed','id':row['id']})
    binding=json.loads((RUN/'execution-source-binding.json').read_text())
    source=Path(binding['source']);mismatches=[]
    for name,expected in binding['source_hashes'].items():
        f=source/name
        if not f.is_file() or sha(f)!=expected:mismatches.append(name)
    if mismatches:errors.append({'type':'immutable-source-mismatch','paths':mismatches})
    freshness={}
    for name,location,expected in [
        ('frontend','repos/ui/mfe-base','66c6411ade58e4d134e381c2baee8ad3f76a8dbf'),
        ('bff','repos/services/single-ui-bff','19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a'),
        ('sdk','repos/libraries/single-ui-sdk-starter','b0aa82005e7f14202f85f5ef583f25e42da9eeb3')]:
        actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT/location,text=True).strip()
        recorded_exists=subprocess.run(['git','cat-file','-e',expected+'^{commit}'],cwd=ROOT/location,capture_output=True).returncode==0
        freshness[name]={'assessed_revision':expected,'head':actual,'head_matches_assessed':actual==expected,
                         'assessed_revision_available':recorded_exists}
        if not recorded_exists:errors.append({'type':'assessed-revision-unavailable','repository':name})
        if actual!=expected:
            warnings.append({'type':'checkout-differs-from-assessed-revision','repository':name,
                             'assessed_revision':expected,'head':actual,
                             'limit':'Presentation validation covers retained evidence. It does not assess the newer checkout.'})
            for filename in ['10-release-confidence.html','10-release-confidence-details.html','10-release-confidence.md']:
                if 'newer server code has not been assessed here' not in (TASK/filename).read_text():
                    errors.append({'type':'source-scope-limit-missing','document':filename})
    for file,expected in [
        (TASK/'06-test-cases.md','5622dab3b635113ff0137fbf66489f385bbcb11dc4444ec0070f7203d19a7037'),
        (ROOT/'knowledge/candidates/requirements/REQ-active-session-renewal.md','3db69ca6827b4afa0eb9f3182f15045f80dac012f9d37004d62144740424c359')]:
        if sha(file)!=expected:errors.append({'type':'definition-hash-mismatch','path':str(file.relative_to(ROOT))})
    inv=json.loads((RUN/'aggregate/final-inventory.json').read_text())
    for r in inv['rows']:
        if not r.get('result') or sha(TASK/r['result'])!=r['result_sha256']:
            errors.append({'type':'result-hash-mismatch','id':r['id']})
    impact=json.loads((OLD/'failure-impacts.json').read_text())
    md=(TASK/'10-release-confidence.md').read_text()
    for f in impact['cases']:
        if f['case_id'] not in md:errors.append({'type':'missing-failure-row','id':f['case_id']})
    # Check fixture credentials privately. Only a zero/nonzero result is retained.
    fixture=ROOT/'.workbench/portal-session-real-20261019/local-bff/runner/local/portalsession/LocalSessionApplication.java'
    credentials=[]
    if fixture.exists():
        fixture_text=fixture.read_text()
        for field in ['PASSWORD']:
            match=re.search(r'public static final String '+field+r'="([^"]+)"',fixture_text)
            if match:credentials.append(match[1].encode())
    secret_matches=[]
    for base in [RUN,HERE]:
        for f in base.rglob('*'):
            if f.is_file() and f.suffix in ['.json','.log','.mjs','.py','.java','.md','.html']:
                data=f.read_bytes()
                if any(value in data for value in credentials):secret_matches.append(str(f.relative_to(ROOT)))
    if secret_matches:errors.append({'type':'fixture-credential-retained','paths':secret_matches})
    source_files=[]
    for base in [RUN,HERE]:
        for f in sorted(base.rglob('*')):
            if f.is_file() and '__pycache__' not in f.parts and f.name not in ['source-manifest.json','validation.json']:
                source_files.append({'path':str(f.relative_to(ROOT)),'sha256':sha(f),'bytes':f.stat().st_size})
    source_files.extend({'path':str(f.relative_to(ROOT)),'sha256':sha(f),'bytes':f.stat().st_size} for f in DOCUMENTS)
    existing={f['path'] for f in source_files}
    for f in sorted(referenced):
        if f in [HERE/'validation.json',HERE/'source-manifest.json']:
            continue
        name=str(f.relative_to(ROOT))
        if name not in existing:
            source_files.append({'path':name,'sha256':sha(f),'bytes':f.stat().st_size})
            existing.add(name)
    (HERE/'source-manifest.json').write_text(json.dumps({'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'files':source_files,'limits':['Hashes bind retained bytes. They do not establish source authority, business acceptance, or deployment identity.']},indent=2)+'\n')
    qa=json.loads((HERE/'html-qa.json').read_text()) if (HERE/'html-qa.json').exists() else {'status':'NOT_RUN'}
    if qa['status']!='PASSED' or qa.get('visual_review')!='PASSED':errors.append({'type':'html-qa-incomplete'})
    data={'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASSED' if not errors else 'FAILED',
          'scope':'Plain-language issue descriptions in both HTML views. All outcomes, priorities, and the release recommendation remain unchanged. No new case execution.',
          'request':str(REQUEST.relative_to(TASK)),'readability':readability,
          'commands':commands,'links':{'checked':checked,'errors':[x for x in errors if 'link' in x.get('type','') or 'anchor' in x.get('type','')]},
          'immutable_source':{'files_checked':len(binding['source_hashes']),'mismatches':mismatches},
          'candidate_freshness':freshness,
          'inventory':{'total':inv['total'],'counts':inv['counts'],'result_hashes_checked':len(inv['rows'])},
          'failure_impacts':{'rows':len(impact['cases']),'all_current_failed_cases_covered':not impact['missing_current_failures']},
          'fixture_credentials':{'password_values_retained':bool(secret_matches),'matching_files':len(secret_matches),
                                 'synthetic_principal_identity':'Retained where account ownership is an asserted predicate.'},
          'priority_reconciliation':{'cases':285,'case_priorities':case_priorities['summary']['priorities'],
              'retained_impact_rows':len(issue_priorities['issues']),'review_rows':len(issue_priorities['review_entries']),
              'additional_controls':len(issue_priorities['additional_controls']),'status_changes':0},
          'html_qa':qa,'source_manifest_sha256':sha(HERE/'source-manifest.json'),
          'writing_review':{'standard':'ASD-STE100','automated_check':'PASSED' if not errors else 'FAILED',
                            'asd_review':'PENDING','reviewer':None,'reviewed_at':None,
                            'limitations':['Automated checks do not check the complete approved dictionary or grammar rules.']},
          'errors':errors,'warnings':warnings,
          'limits':['Automated validation does not establish business correctness, human acceptance, or release authorization.',
                    'All release results apply to the recorded source scope. A checkout change does not update that assessment.']}
    (HERE/'validation.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'status':data['status'],'links_checked':checked,'source_files_checked':len(binding['source_hashes']),
                      'result_hashes_checked':len(inv['rows']),'errors':errors},indent=2))
    raise SystemExit(bool(errors))


if __name__=='__main__':
    main()
