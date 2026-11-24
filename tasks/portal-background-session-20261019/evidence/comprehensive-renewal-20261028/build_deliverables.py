"""Render retained design inputs into the one canonical task catalog."""
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
TASK = HERE.parent.parent
ROOT = TASK.parent.parent
CATALOG = TASK / "06-test-cases.md"
MARKER = "\n## Comprehensive renewal expansion\n"
PREFIX = "evidence/comprehensive-renewal-20261028/"

def load(name):
    return json.loads((HERE/name).read_text())

def array(name):
    value=load(name)
    return value if isinstance(value,list) else value['cases']

def digest(data):
    return hashlib.sha256(data).hexdigest()

def textvalue(value):
    return " ".join(map(str,value)) if isinstance(value,list) else str(value)

def criterion(ac):
    lines={"AC-1":187,"AC-2":194,"AC-3":201,"AC-4":208,"AC-5":216,"AC-6":223,"AC-7":230}
    return f"[{ac}](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L{lines[ac]})"

inputs=["core-cases.json","workspace-transport-cases.json","security-cases.json","new-e2e-cases.json"]
cases=[]
for name in inputs:
    if not (HERE/name).exists():
        raise RuntimeError(f"Await required input {name}")
    for c in array(name):
        c['_input']=name
        cases.append(c)
ids=[c['id'] for c in cases]
assert len(ids)==len(set(ids)),"Duplicate canonical IDs"
security_results={r['case_id']:r for r in load('security-probe-execution.json')['cases']}
for c in cases:
    if c['id'] in security_results:
        r=security_results[c['id']]
        passed=r.get('assertions_passed',r.get('security_assertion_passed'))
        c['execution_status']='PASSED' if passed else 'FAILED'
        c['execution_refs']=[PREFIX+'security-probe-execution.json']
        c['limits']='Actual BFF controller integration with RSA validation; mocked repositories and entitlements, servlet mocks. No HTTP, browser, provider, replica, or production verification.'

repositories=[ROOT/p for p in ["repos/ui/mfe-base","repos/services/single-ui-bff","repos/libraries/single-ui-sdk-starter","repos/ui/mfe-root-config","repos/ui/mfe-ratan-container","repos/ui/mfe-cashflow-blotter"]]
snapshots={}
for c in cases:
    for s in c['sources']:
        key=(s['path'],s.get('revision'),s.get('sha256'))
        if key in snapshots:
            continue
        path=ROOT/s['path']
        repo=next((r for r in repositories if path.is_relative_to(r)),None)
        data=None
        origin=None
        if s.get('sha256') and path.exists() and digest(path.read_bytes())==s['sha256']:
            data=path.read_bytes();origin="inspected-worktree-hash"
        if data is None and repo and (repo/'.git').exists() and s.get('revision'):
            attempt=subprocess.run(['git','-C',str(repo),'show',f"{s['revision']}:{path.relative_to(repo)}"],capture_output=True)
            if attempt.returncode==0 and (not s.get('sha256') or digest(attempt.stdout)==s['sha256']):
                data=attempt.stdout;origin="committed-source"
        if data is None and path.exists() and not s.get('sha256'):
            data=path.read_bytes();origin="filesystem-snapshot"
        if data is None:
            raise RuntimeError(f"Unavailable exact source bytes: {s}")
        sha=digest(data)
        dest=HERE/'sources'/sha[:12]/path.name
        dest.parent.mkdir(parents=True,exist_ok=True)
        if dest.exists():
            assert dest.read_bytes()==data
        else:
            dest.write_bytes(data)
        line_count=len(data.decode().splitlines())
        raw_bounds=s.get('lines',[1,line_count])
        bounds=[int(x) for x in re.findall(r'\d+',raw_bounds)] if isinstance(raw_bounds,str) else raw_bounds
        valid_bounds=[max(1,min(bounds[0],line_count)),max(1,min(bounds[-1],line_count))]
        snapshots[key]={**s,'lines':valid_bounds,'sha256':sha,'snapshot':str(dest.relative_to(ROOT)),
                        'origin':origin,'line_count':line_count}

def source_link(s):
    snap=snapshots[(s['path'],s.get('revision'),s.get('sha256'))]
    raw=s.get('lines',[1,snap['line_count']])
    numbers=[int(x) for x in re.findall(r'\d+',raw)] if isinstance(raw,str) else raw
    start=max(1,min(numbers[0],snap['line_count']))
    end=max(start,min(numbers[-1],snap['line_count']))
    return f"[{Path(s['path']).name}]({Path(snap['snapshot']).relative_to(TASK.relative_to(ROOT))}#L{start}-L{end})"

raw=CATALOG.read_text()
base=raw.split(MARKER)[0].rstrip()+"\n"
base=re.sub(r'(?m)^version: 18$', 'version: 19',base,count=1)
if '  - SRC-comprehensive-renewal-20261028' not in base:
    base=base.replace('source_refs:\n','source_refs:\n  - SRC-comprehensive-renewal-20261028\n',1)
base=base.replace('Current invocation: [verify review issues through E2E execution](evidence/user-input-20261028-review-e2e-proof.txt).',
    'Current invocation: [comprehensive renewal and security request](evidence/user-input-20261028-comprehensive-renewal.txt).\n'
    'Read the [new expansion](#comprehensive-renewal-expansion), [use cases](03-use-cases-renewal.md), and [security review](07-security-review-renewal.md).\n'
    'Earlier execution results retain their original source identities.')

counts=Counter(c['family'] for c in cases)
parts=[MARKER, '\nDefinition version: 1 for every new RN case. Earlier definitions and results remain preserved.\n',
    '\n> **Critical conclusions: A logout revocation gap is reproduced in the isolated BFF integration.**\n'
    '> Action: review and correct revocation before security acceptance. Consequence: copied refresh credentials can remain usable.\n'
    '> Owner: unknown service owner. Evidence: [security review](07-security-review-renewal.md#findings-and-actions).\n',
    '\nThe [request](evidence/user-input-20261028-comprehensive-renewal.txt) authorizes this expansion.\n'
    'The [strategy](05-test-strategy-renewal.md) states its scope and finite coverage limits.\n'
    'The [coverage record](09-renewal-coverage.md) separates definitions, assertions, source conformance, and execution.\n',
    '\n### Renewal fixture and oracles\n',
    '\nUser A and User B are synthetic portal users with distinct session identifiers and entitlements.\n'
    'WA, WB, and W-A/W-B identify fixture workspaces. A case states their permissions before each protected action.\n'
    'Access credentials authorize protected requests. Refresh credentials authorize the service relogin operation.\n'
    'The shell epoch identifies local session ownership. It does not establish server revocation.\n'
    'Use isolated accounts, local services, and controlled responses. Never execute these attacks against production.\n'
    'Record request ID, workspace ID, session owner, clock, endpoint, authorization result, and state transitions.\n'
    'Replace real credentials with labels in exported evidence. Reset fixture accounts and close contexts after each case.\n'
    'Abort owned operations, close sockets, and verify cleanup after each experiment. Keep policy-specific cleanup expectations separate.\n'
    'A successful renewal requires usable returned access and protected validation. Dialog closure alone is insufficient.\n'
    'UI controls use the source-defined timeout dialog and Extend or Logout buttons.\n'
    'Runtime uniqueness remains unverified except within the three new browser probes.\n'
    'See [workspace fixtures](evidence/comprehensive-renewal-20261028/workspace-transport-fixtures.json) and '
    '[component inventory](evidence/comprehensive-renewal-20261028/workspace-transport-components.json).\n'
    'Source observations are regression checks. Proposed security invariants require applicable owner review.\n'
    'Policy-open cases record observations. Their business acceptance remains blocked.\n'
    'Case priorities are test-planning proposals. They do not replace recorded business backlog priorities.\n',
    '\n### Expansion navigation\n\n| Family | New definitions | Case links |\n| --- | --- | --- |\n']
for family,count in sorted(counts.items()):
    members=[c for c in cases if c['family']==family]
    parts.append(f"| {family} | {count} | "+", ".join(f"[{c['id']}](#{c['id'].lower()})" for c in members)+" |\n")

case_lines={}
for c in cases:
    links=", ".join(criterion(a) for a in c.get('ac_ids',[])) or "No separate approved criterion; see the stated evidence class."
    status=c.get('execution_status','NOT_RUN')
    result=c.get('actual_results')
    refs=c.get('execution_refs',c.get('retained_execution_refs',[]))
    if not refs and c['id'].startswith('RN-X'):
        refs=[f"{PREFIX}{c['id'].lower()}/result.json"]
    parts.extend([f"\n### {c['id']}\n\n",f"**{c['title']}**\n\n",
        f"Use case: [{c['use_case']}](03-use-cases-renewal.md#{c['use_case'].lower()}). "
        f"Level: `{c['level']}`. Evidence class: `{c['basis']}`.\n\n",
        f"Criteria: {links}\n\n",
        "Source: "+"; ".join(source_link(s) for s in c['sources'])+". Exact identities: [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json).\n\n",
        '```gherkin\n',f"Feature: {c['title']}\n",f"  @{c['basis'].replace('-','_')} @{c['id']}\n",f"  Scenario: {c['id']}\n"])
    for keyword,field in [('Given','given'),('When','when'),('Then','then')]:
        assert c[field],c['id']
        for i,step in enumerate(c[field]):
            step=step.replace('Extend button in the expiry dialog','button labeled "Extend" in the dialog named "Your session has been expired"')
            step=step.replace('Extend button again','button labeled "Extend" inside the dialog named "Your session has been expired" again')
            step=step.replace('Logout button while renewal is pending','button labeled "Logout" inside the dialog named "Your session has been expired" while renewal is pending')
            step=step.replace('Logout button while renewal remains pending','button labeled "Logout" inside the dialog named "Your session has been expired" while renewal remains pending')
            step=step.replace('inside the timeout dialog','inside the dialog named "Your session has been expired"')
            if c['id'].startswith('RN-X') and 'dialog' in step:
                step=step.replace('the pending expiry dialog','the dialog named "Your session has been expired"')
                step=step.replace('the expiry dialog','the dialog named "Your session has been expired"')
                step=re.sub(r'the dialog(?! named)', 'the dialog named "Your session has been expired"',step)
                step += ' in the portal'
            parts.append(f"    {keyword if i==0 else 'And'} {step.rstrip('.')}\n")
    binding='See the exact browser runner and results below.' if c['id'].startswith('RN-X') else 'See [controller probe](evidence/comprehensive-renewal-20261028/SecurityLogoutProbe.java) and its retained per-case results.' if c['id'] in security_results else 'UNVERIFIED for this new definition; existing test links require direct predicate comparison.'
    parts.extend(['```\n\n',f"Assertion binding: {binding}\n\n",
        f"Execution: `{status}`. ",f"Limits: {textvalue(c.get('limits','New specification only.'))}\n"])
    if refs:
        parts.append("\nResults: "+"; ".join(f"[retained execution]({r})" for r in refs)+".\n")
    if c.get('policy_gap'):
        parts.append(f"\nAcceptance: BLOCKED. Policy gap: {textvalue(c['policy_gap'])}\n")

comb=load('combinations.json')
parts.append('\n### RN-C001\n\n**Pairwise interaction design**\n\n'
    'Use case: [UC-C01](03-use-cases-renewal.md#uc-c01). Level: planned browser and service integration.\n'
    'Evidence class: proposed-security. Execution: `NOT_RUN`. Each row has one independent context.\n'
    'Begin a renewal attempt, then apply lifecycle, ownership, and response events in the named order.\n'
    'A guarded action can send zero POST requests. Record that outcome without fabricating a response.\n'
    'The transport factor names a concurrent connection. It does not declare that transport eligible user activity.\n'
    'The fixture creates the named loading state before the renewal attempt.\n'
    'All source and policy limits from the linked individual cases also apply.\n\n'
    '```gherkin\nFeature: Renewal interaction invariants\n  @proposed_security @RN-C001\n'
    '  Scenario Outline: RN-C001\n'
    '    Given User A has <workspaces> isolated workspaces with loading state <loading>\n'
    '    And access has <access_ms> milliseconds remaining and refresh state equals <refresh>\n'
    '    And the concurrent transport equals <transport> and network schedule equals <network>\n'
    '    When the fixture attempts renewal through <trigger>\n'
    '    And the fixture applies ownership change <ownership>\n'
    '    And the fixture applies lifecycle change <lifecycle>\n'
    '    And the fixture settles accepted requests with <response> using delivery order <delivery>\n'
    '    Then obsolete-epoch responses install exactly 0 credentials\n'
    '    And unauthorized protected business mutations equal 0\n'
    '    And each business operation identifier has at most 1 committed mutation\n'
    '    Examples:\n')
keys=list(comb['factors'])
parts.append('      | row_id | '+' | '.join(keys)+' |\n')
for row in comb['pairwise_rows']:
    parts.append('      | '+row['row_id']+' | '+' | '.join(row[k] for k in keys)+' |\n')
parts.append('```\n\n[Measured pair coverage](evidence/comprehensive-renewal-20261028/combinations.json): '
    f"{comb['coverage']['covered_pairs']} / {comb['coverage']['required_pairs']} declared factor-value pairs.\n"
    f"The selected {len(comb['pairwise_rows'])} rows represent a {comb['cartesian_population']:,}-row Cartesian design population.\n"
    'This measures design coverage. It establishes no passing execution or security assurance.\n')

parts.append('\n### RN-C002\n\n**Enumerate the selected four-factor risk subset**\n\n'
    'Use case: [UC-C01](03-use-cases-renewal.md#uc-c01). Evidence class: proposed-security. Execution: `NOT_RUN`.\n'
    'Use one workspace, idle loading, valid four-hour refresh, visible lifecycle, HTTP, and an online FIFO fixture.\n'
    'This subset enumerates every declared trigger, access boundary, response, and ownership combination.\n\n'
    '```gherkin\nFeature: Renewal risk interactions\n  @proposed_security @RN-C002\n'
    '  Scenario Outline: RN-C002\n'
    '    Given User A has access remaining <access_ms> milliseconds in the fixed risk fixture\n'
    '    When the fixture attempts renewal through <trigger>\n'
    '    And the fixture applies ownership change <ownership>\n'
    '    And the fixture settles accepted requests with <response>\n'
    '    Then obsolete-epoch responses install exactly 0 credentials\n'
    '    And unauthorized protected business mutations equal 0\n'
    '    Examples:\n      | row_id | trigger | access_ms | response | ownership |\n')
for row in comb['risk_rows']:
    parts.append('      | '+' | '.join(row[k] for k in ['row_id','trigger','access_ms','response','ownership'])+' |\n')
parts.append('```\n\nThe 144 examples exhaust this declared subset. Other interactions remain outside that claim.\n')

parts.append('\n### RN-O001\n\n**Enumerate late-session response orderings**\n\n'
    'Use case: [UC-C02](03-use-cases-renewal.md#uc-c02). Evidence class: proposed-security. Execution: `NOT_RUN`.\n'
    'Events start-A and start-B create requests under their respective session epochs.\n'
    'Events logout-A and login-B invalidate A and establish B. Event reply-B installs usable B access.\n'
    'Event reply-A delivers the specified old response. Each sequence uses a new context.\n\n'
    '```gherkin\nFeature: Late response ordering isolation\n  @proposed_security @RN-O001\n'
    '  Scenario Outline: RN-O001\n'
    '    Given User A has a valid session and User B has separate synthetic credentials\n'
    '    And the old response outcome equals <old_response>\n'
    '    When the fixture executes event sequence <events>\n'
    '    Then the final installed credential subject equals B\n'
    '    And A response deliveries after logout change exactly 0 B authentication fields\n'
    '    Examples:\n      | row_id | old_response | events |\n')
for row in comb['order_rows']:
    parts.append('      | '+' | '.join(row[k] for k in ['row_id','old_response','events'])+' |\n')
parts.append('```\n\nThe 15 rows exhaust this six-event partial order with three old-response outcomes.\n'
    'They do not exhaust arbitrary session histories or infinite loops.\n')

CATALOG.write_text(base+''.join(parts))
content=CATALOG.read_text()
for n,line in enumerate(content.splitlines(),1):
    match=re.fullmatch(r'### (RN-[A-Z]\d+)',line)
    if match:case_lines[match.group(1)]=n
manifest={"version":1,"specification":str(CATALOG.relative_to(ROOT)),"sha256":digest(CATALOG.read_bytes()),
    "cases":[{"id":c['id'],"line":case_lines[c['id']],"family":c['family'],"basis":c['basis'],"use_case":c['use_case'],
        "ac_ids":c.get('ac_ids',[]),"design_input":c['_input'],"execution_status":c.get('execution_status','NOT_RUN')} for c in cases],
    "outlines":[{"id":cid,"line":case_lines[cid],"examples":len(comb[key])} for cid,key in [('RN-C001','pairwise_rows'),('RN-C002','risk_rows'),('RN-O001','order_rows')]],
    "counts":{"individual_definitions":len(cases),"outlines":3,"outline_examples":sum(len(comb[k]) for k in ['pairwise_rows','risk_rows','order_rows']),
        "expanded_test_instances":len(cases)+sum(len(comb[k]) for k in ['pairwise_rows','risk_rows','order_rows']),"families":dict(counts),"basis":dict(Counter(c['basis'] for c in cases))},
    "limits":["Design inputs are retained authoring provenance. Only 06-test-cases.md defines current readable cases.","No passing result is inferred from scenario definition or combinatorial coverage."]}
(HERE/'design-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(HERE/'source-manifest.json').write_text(json.dumps({"version":1,"sources":list(snapshots.values()),"intent":{"path":"knowledge/candidates/requirements/REQ-active-session-renewal.md","sha256":digest((ROOT/'knowledge/candidates/requirements/REQ-active-session-renewal.md').read_bytes()),"version":5},"request":{"path":str((TASK/'evidence/user-input-20261028-comprehensive-renewal.txt').relative_to(ROOT)),"sha256":digest((TASK/'evidence/user-input-20261028-comprehensive-renewal.txt').read_bytes())}},indent=2)+'\n')
print(json.dumps(manifest['counts']))
