"""Render scope-specific evidence matrices without inferring complete coverage."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

D=Path(__file__).resolve().parent
T=D.parent.parent
R=T.parent.parent
A=json.loads((D/'assertion-map.json').read_text())
M=json.loads((D/'design-manifest.json').read_text())
records=[]
def retain(source):
    path=R/source['path'];rev=source.get('revision')
    roots=[R/p for p in ['repos/ui/mfe-base','repos/testing/ratan-test-engine']]
    repo=next((r for r in roots if path.is_relative_to(r)),None)
    if repo and rev:
        data=subprocess.check_output(['git','-C',str(repo),'show',f'{rev}:{path.relative_to(repo)}'])
    else:data=path.read_bytes()
    sha=hashlib.sha256(data).hexdigest()
    if source.get('sha256'):assert sha==source['sha256'],source
    dest=D/'sources'/sha[:12]/path.name
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(data)
    records.append({**source,'sha256':sha,'snapshot':str(dest.relative_to(R))})
    bounds=source.get('lines',[1,len(data.decode().splitlines())])
    return f"[{path.name}]({dest.relative_to(T)}#L{bounds[0]}-L{bounds[-1]})"
def tc(cid):return f'[{cid}](06-test-cases.md#{cid.lower()})'
def ac(cid):
    num={'AC-1':187,'AC-2':194,'AC-3':201,'AC-4':208,'AC-5':216,'AC-6':223,'AC-7':230}[cid]
    return f'[{cid}](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L{num})'

lines=['---\nartifact_kind: traceability-record\nid: COVERAGE-comprehensive-session-renewal\nversion: 1\nstatus: draft\nowner: unknown\nsource_refs: [SRC-comprehensive-renewal-20261028]\nrelated_ids: [REQ-active-session-renewal, PLAN-comprehensive-session-renewal]\nreview:\n  state: pending\n  reviewer: null\n  reviewed_at: null\nwriting_review:\n  standard: ASD-STE100\n  automated_check: NOT_RUN\n  asd_review: PENDING\n  reviewer: null\n  reviewed_at: null\n  limitations:\n    - Automated checks do not check the complete approved dictionary or grammar rules.\n---\n',
 '# Session renewal coverage and remaining evidence\n\n'
 '> **Critical conclusions: Security acceptance is blocked by one reproduced inherited revocation defect.**\n'
 '> Action: correct [SEC-01](07-security-review-renewal.md#sec-01) and collect target evidence. Consequence: secure deployment cannot be recommended.\n'
 '> Owner: unknown authentication owner. Evidence: [failed controller case](evidence/comprehensive-renewal-20261028/expired-logout-case.json).\n\n',
 '## Scope and identities\n\n'
 'Scope: the [current request](evidence/user-input-20261028-comprehensive-renewal.txt), seven renewal criteria, and 12 changed shell runtime paths.\n'
 'Capability: single-ui-authentication. Related capabilities include workspace composition and E2E verification.\n'
 'Repositories: mfe-base, single-ui-bff, authentication SDK, application consumers, and ratan-test-engine.\n'
 'Contracts: token family, shared HTTP client, container props, and test-suite execution.\n'
 f"Shell comparison: `{A['comparison']['base']}` to `{A['comparison']['head']}`.\n"
 'Local Home-controller edits remain excluded from current execution claims. Worktree observations have separate source hashes.\n\n',
 '## Requirement and criterion declarations\n\n'
 f"Requirement version 5 SHA-256: `{A['requirement_sha256']}`. Publication review remains pending.\n\n"
 '| Requirement or defect ID | Criterion ID | Measurable expected behavior | Source revision | Knowledge review state |\n| --- | --- | --- | --- | --- |\n']
labels=['Mouse input renews during 15 seconds','Keyboard input renews during 15 seconds','Scroll input renews during 15 seconds','Four controlled hours cross initial refresh expiry without elapsed-time SSO','Pending renewal has zero early closures','Successful renewal closes exactly once','Rejected renewal preserves retry']
for i,label in enumerate(labels,1):lines.append(f'| REQ-active-session-renewal | {ac(f"AC-{i}")} | {label} | v5; hash above | pending |\n')
lines+=['\n## Coverage inventories and summary\n\n'
 'Target: `TC >= AC = Code Change` concerns behavior containment and equivalence. Counts cannot establish that equivalence.\n'
 'New catalog inventory: **271 individual cases plus three outlines, with 196 example rows: 467 expanded instances.**\n'
 'The [40 use cases](03-use-cases-renewal.md#main-flow) link those definitions. Historical cases remain separately preserved.\n'
 'The expansion includes 60 policy-open individual cases. They are not 60 approved new requirements.\n'
 'New execution inventory: 3 browser cases and 13 controller cases. Fifteen pass; one security case fails.\n'
 'The other 451 expanded instances remain `NOT_RUN`. Existing unit tests are counted separately.\n\n'
 '| Metric | Qualified / total | Percentage | Incomplete or failed IDs | Evidence and limit |\n| --- | --- | --- | --- | --- |\n'
 '| AC with canonical definitions | 7 / 7 | 100% definition only | none | New and retained definitions cover the seven named targets |\n'
 '| AC with inspected direct assertions | 7 / 7 | 100% relationship only | Broader boundaries remain incomplete | [Assertion map](evidence/comprehensive-renewal-20261028/assertion-map.json); no conformance claim |\n'
 '| AC with current matching local passing execution | 3 / 7 | 42.9% within disclosed fixture | AC-4 partial; AC-1, AC-2, AC-3 not rerun | Synthetic manual recovery only |\n'
 '| AC with inspected implementation locations | 7 / 7 | 100% mapping only | AC-1 contradictory; AC-2 and AC-3 missing; AC-4 partial | Locations do not establish conformance |\n'
 '| Complete business conformance | UNKNOWN / 7 | UNKNOWN | Target and policy limits remain | No complete equivalence claim |\n'
 '| Changed runtime paths with selected direct assertions | 12 / 12 | 100% relationship only | Complete branch coverage UNKNOWN | Includes six supporting-maintenance paths |\n'
 '| Changed runtime paths with selected passing tests | 12 / 12 | 100% selected predicates only | Complete path behavior UNKNOWN | [Current executions](08-test-execution-renewal.md) |\n'
 '| Behavioral-change justification | UNKNOWN / 6 | UNKNOWN | Policy and scope review incomplete | Six runtime paths classified behavioral; six supporting maintenance |\n'
 '| Complete changed-behavior assertion coverage | UNKNOWN / 12 | UNKNOWN | Full changed-predicate denominator unavailable | Path counts are not behavior completeness |\n'
 '| Declared factor-value pair design coverage | 797 / 797 | 100% design only | Execution NOT_RUN | 37 rows across 11 declared factors |\n'
 '| Instrumented line or branch coverage | UNKNOWN | UNKNOWN | No instrumentation collected here | Keep separate from behavioral coverage |\n\n'
 'The [design manifest](evidence/comprehensive-renewal-20261028/design-manifest.json) lists every new case and its evidence class.\n'
 'The Cartesian population has 1,866,240 rows. Pair coverage does not execute that population.\n'
 'The selected four-factor subset has 144 explicit rows. Fifteen more rows enumerate one finite response-order model.\n\n'
 '## Relationship evidence\n\n'
 '| From ID | Relationship | To ID | Evidence | Evidence class | Limit |\n| --- | --- | --- | --- | --- | --- |\n'
 '| User request | Authorizes | Test design and assessment | [Exact input](evidence/user-input-20261028-comprehensive-renewal.txt) | user intent | No application fix or deployment performed |\n'
 '| Seven criteria | Have case and source links | Canonical and executable cases | [Assertion map](evidence/comprehensive-renewal-20261028/assertion-map.json) | inspected relationship | Complete equivalence remains unestablished |\n'
 '| Local executions | Establish stated assertions | Local candidate and fixtures | [Execution report](08-test-execution-renewal.md) | retained execution | No target or provider parity |\n\n'
 '## Inspected implementation and assertions\n\n'
 '### AC to test case coverage\n\n'
 '| AC version | Predicate | Canonical cases | Inspected assertion | Definition / assertion status | Matching execution | Gap and limit |\n| --- | --- | --- | --- | --- | --- | --- |\n']
for row in A['ac_to_assertions']:
    cid=row['ac_id']
    defs=[c['id'] for c in M['cases'] if cid in c['ac_ids']]
    # Link a representative new partition and every directly inspected execution case.
    links=list(dict.fromkeys(row['cases']+defs[:2]))
    lines.append(f"| {ac(cid)} v5 | {labels[int(cid[-1])-1]} | {', '.join(tc(c) for c in links)} | "+'; '.join(retain(s) for s in row['assertions'])+
        f" | Defined; inspected selected predicates | {row['passing_execution']} | {' '.join(row['limits'])} |\n")
lines.append('\n### AC to code change coverage\n\n| AC version | Intended predicate | Change ID or UNCHANGED | Exact old/new source | Conformance | Gap and evidence limit |\n| --- | --- | --- | --- | --- | --- |\n')
for row in A['ac_to_assertions']:
    cid=row['ac_id']
    if cid in ['AC-1','AC-2','AC-3']:
        change='UNCHANGED activity handler inside changed Home file'
    else:
        units=[c['id'] for c in A['code_changes'] if cid in c['ac_ids']]
        change=', '.join(f'[{c}](#{c.lower()})' for c in units)
    lines.append(f"| {ac(cid)} v5 | {labels[int(cid[-1])-1]} | {change} | "+'; '.join(retain(s) for s in row['code'])+
        f"; baseline links below | {row['conformance']} | Source assessment; new definitions cannot approve their own behavior |\n")
lines.append('\n### Code change to test case coverage\n\n| Change ID | Kind and changed path | Exact old/new bytes | Direct assertion chain | Canonical cases | Current execution | Limit |\n| --- | --- | --- | --- | --- | --- | --- |\n')
for c in A['code_changes']:
    before='New file; baseline absent'
    if c['base_sha256']:
        before=retain(dict(path='repos/ui/mfe-base/'+c['path'],revision=c['base'],sha256=c['base_sha256']))
    after=retain(dict(path='repos/ui/mfe-base/'+c['path'],revision=c['head'],sha256=c['head_sha256']))
    found=re.findall(r'(?:PEND|OWN|DEL)-\d+',c['asserted_cases'])
    cases=', '.join(tc(x) for x in found) if found else tc('REVIEW-F01-RECOVERY') if c['asserted_cases']=='SR11' else tc('RN-R009')
    lines.append(f"| <a id=\"{c['id'].lower()}\"></a>{c['id']} | {c['classification']}; `{c['path']}` | Old: {before}; new: {after} | {retain(c['direct_assertion'])} | {cases} | [Selected passing run]({c['matching_execution']}) | {c['limits']} |\n")
lines+=['\n## Retained execution and verification\n\n'
 'Targeted units: **157 / 157 passed across ten suites**, with zero failures, skips, or runner errors.\n'
 'New browser cases: **3 / 3 passed**, with 56 assertions. Actual shell DOM and Axios ran with substituted authentication.\n'
 'Security controller cases: **12 / 13 passed**. The inherited logout replay case failed.\n'
 'The security runner exits with failure when its security assertion fails. A successful compilation does not override that result.\n'
 'See [unit and browser evidence](08-test-execution-renewal.md), [controller evidence](07-security-review-renewal.md#security-verification), '
 'and [source-map binding](evidence/comprehensive-renewal-20261028/served-source-binding.json).\n'
 'The full application suite was not rerun. This stage makes no delivery recommendation.\n\n'
 '## Coverage gaps\n\n'
 'Real application data, dirty forms, lazy modules, live WebSockets, STOMP, SSE, and long transfers remain unexecuted.\n'
 'Target identity-provider integration, deployed settings, revocation replicas, and physical sleep remain unverified.\n'
 'Activity targets retain their prior backlog disposition. Their source gaps remain visible above.\n'
 'Full four-hour current-candidate browser verification remains absent. Component and historical executions have narrower claims.\n'
 'Use the [policy register](05-test-strategy-renewal.md#policy-questions) for unresolved acceptance decisions.\n\n'
 '## Facts, inferences, and unresolved questions\n\n'
 'Facts: the retained executions establish only their asserted fixture outcomes. One security assertion fails.\n'
 'Inference: broader workspace and transport interactions require additional implementation-specific execution.\n'
 'Unknowns: deployed composition, complete policy inventory, and target security controls remain unavailable.\n\n'
 '## Findings\n\n| Evidence | Consequence | Owner | Next action |\n| --- | --- | --- | --- |\n'
 '| [SEC-01](07-security-review-renewal.md#sec-01) | Logout can leave refresh usable in the isolated path | unknown authentication owner | Correct revocation and rerun replay assertions |\n'
 '| [Policy-open cases](evidence/comprehensive-renewal-20261028/design-manifest.json) | Acceptance remains blocked for those outcomes | unknown business and security owners | Resolve the consolidated policy questions |\n'
 '| [Source and execution limits](08-test-execution-renewal.md) | Local passes cannot establish secure target behavior | unknown test owner | Bind and execute the reviewed target composition |\n\n'
 '## Sources\n\n'
 '| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |\n| --- | --- | --- | --- | --- |\n'
 '| User request | [Exact input](evidence/user-input-20261028-comprehensive-renewal.txt) | user-message-20261028 | [Source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json) | User; test and security scope |\n'
 '| Requirement and source | [Source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json) | Per-source exact revisions | SHA-256 per item | Candidate intent and inspected source remain separate |\n'
 '| Direct assertion and baseline bytes | [Coverage manifest](evidence/comprehensive-renewal-20261028/coverage-source-manifest.json) | Per-item revisions | SHA-256 per item | Selected predicate chains only |\n']
(T/'09-renewal-coverage.md').write_text(''.join(lines))
unique={ (s['path'],s.get('revision'),s['sha256']):s for s in records}
(D/'coverage-source-manifest.json').write_text(json.dumps({'sources':list(unique.values())},indent=2)+'\n')
print(json.dumps({'criterion_rows':len(A['ac_to_assertions']),'changed_runtime_paths':len(A['code_changes']),'retained_sources':len(unique)}))
