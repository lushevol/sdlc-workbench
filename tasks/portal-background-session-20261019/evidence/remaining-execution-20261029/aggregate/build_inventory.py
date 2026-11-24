"""Reconcile release case evidence without promoting partial probes into full passes."""
from __future__ import annotations
import argparse
import collections
import datetime
import hashlib
import json
from pathlib import Path
import re
import sys

OUT = Path(__file__).resolve().parent
RUN = OUT.parent
TASK = RUN.parent.parent
ROOT = TASK.parent.parent
OLD = TASK / 'evidence/comprehensive-renewal-20261028'
STATUSES = ('PASSED', 'FAILED', 'PARTIALLY_EXECUTED', 'BLOCKED', 'ERROR', 'NOT_RUN')


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def json_sha(value) -> str:
    return sha(json.dumps(value, sort_keys=True, separators=(',', ':')).encode())


def task_path(path: Path) -> str:
    return path.resolve().relative_to(TASK).as_posix()


def workspace_path(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def count(rows):
    values = collections.Counter(row['status'] for row in rows)
    result = {key: values[key] for key in STATUSES}
    result['FULL_EXECUTED'] = values['PASSED'] + values['FAILED']
    result['TOTAL'] = len(rows)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--core-summary', type=Path, default=RUN/'core-browser/reconciled-summary.json')
    parser.add_argument('--require-complete', action='store_true')
    args = parser.parse_args()
    inputs = {}
    issues = []
    pending_inputs = []

    def read(path):
        path = path.resolve()
        data = path.read_bytes()
        inputs[workspace_path(path)] = sha(data)
        return json.loads(data)

    catalog = TASK / '06-test-cases.md'
    catalog_bytes = catalog.read_bytes()
    inputs[workspace_path(catalog)] = sha(catalog_bytes)
    lines = catalog_bytes.decode().splitlines(keepends=True)
    headings = []
    for index, line in enumerate(lines):
        match = re.match(r'^(#{2,3}) (RN-[A-Z]\d{3})\b', line)
        if match:
            headings.append((match.group(2), index))
    positions = {}
    for index, (case_id, line) in enumerate(headings):
        end = headings[index+1][1] if index+1 < len(headings) else len(lines)
        if case_id in positions:
            issues.append({'kind':'duplicate-canonical-heading','id':case_id})
        positions[case_id] = (line, end)

    definitions = {}
    inventories = [
        ('core', OLD/'core-cases.json'),
        ('security', OLD/'security-cases.json'),
        ('workspace-transport', OLD/'workspace-transport-cases.json'),
        ('prior-browser', OLD/'new-e2e-cases.json'),
    ]
    for group, path in inventories:
        data = read(path)
        for case in data if isinstance(data, list) else data['cases']:
            identifier = case['id']
            if identifier in definitions:
                issues.append({'kind':'duplicate-definition-id','id':identifier})
            definitions[identifier] = {'case':case,'path':path,'group':group}
    combination_path = OLD/'combinations.json'
    combinations = read(combination_path)
    for outline, key in [('RN-C001','pairwise_rows'),('RN-C002','risk_rows'),('RN-O001','order_rows')]:
        for row in combinations[key]:
            identifier = outline+'/'+row['row_id']
            definitions[identifier] = {'case':{'id':outline,'title':outline+' '+row['row_id'],'family':'combinations','basis':'proposed-security' if outline != 'RN-O001' else 'observed','sources':[]},'path':combination_path,'group':'combinations','row':row}
    if len(definitions) != 467:
        issues.append({'kind':'definition-total','actual':len(definitions),'expected':467})

    frontend_binding_path = RUN/'execution-source-binding.json'
    frontend_binding = read(frontend_binding_path)
    candidate_hashes = {'repos/ui/mfe-base/'+key:value for key,value in frontend_binding['source_hashes'].items()}
    server_binding = read(RUN/'security/server-execution.json')
    for source in server_binding['sources']:
        candidate_hashes[source['repository']+'/'+source['path']] = source['sha256']
    evidence = {}

    def resolve_result(value, summary_path):
        path = Path(value)
        options = [path] if path.is_absolute() else [summary_path.parent/path, ROOT/path, TASK/path, RUN/path]
        for option in options:
            if option.is_file():
                return option.resolve()
        raise FileNotFoundError(f'{value}: summary={summary_path}')

    def add_result(identifier, path, group, summary_path=None, summary_row=None, status_override=None, binding=None):
        if identifier in evidence:
            issues.append({'kind':'duplicate-result-id','id':identifier,'old':str(evidence[identifier]['path']),'new':str(path)})
            return
        raw = read(path)
        declared_id = raw.get('instance_id') or raw.get('case_id') or raw.get('id')
        if declared_id and declared_id != identifier:
            issues.append({'kind':'result-id-mismatch','id':identifier,'declared':declared_id,'path':workspace_path(path)})
        row = summary_row or {}
        expected_hash = row.get('sha256') or row.get('result_sha256')
        if expected_hash and expected_hash != sha(path.read_bytes()):
            issues.append({'kind':'summary-result-hash-mismatch','id':identifier,'path':workspace_path(path)})
        original_status = status_override or row.get('status') or raw.get('status')
        execution_status = row.get('execution_status') or raw.get('execution_status') or raw.get('execution_class')
        if original_status in ('PASSED','FAILED','ERROR','NOT_RUN'):
            status = original_status
        elif original_status in ('PARTIALLY_EXECUTED','PARTIAL') or execution_status in ('PARTIALLY_EXECUTED','partial-blocked'):
            status = 'PARTIALLY_EXECUTED'
        elif isinstance(original_status,str) and original_status.startswith('BLOCKED'):
            status = 'BLOCKED'
        else:
            status = 'ERROR'
            issues.append({'kind':'unrecognized-result-status','id':identifier,'status':original_status})
        assertions = raw.get('assertions')
        if isinstance(assertions,list):
            assertions_count = len(assertions)
            failed_assertions = sum(a.get('status') == 'FAILED' or a.get('passed') is False for a in assertions)
        else:
            assertions_count = None
            failed_assertions = None
        if status == 'PASSED' and failed_assertions:
            issues.append({'kind':'pass-with-failed-assertion','id':identifier})
        normalization = None
        if status == 'FAILED' and failed_assertions == 0 and raw.get('error'):
            status = 'ERROR'
            normalization = 'Raw FAILED is an execution error: no assertion failed and the retained result records a setup or runner exception.'
        elif status == 'FAILED' and failed_assertions == 0:
            issues.append({'kind':'failed-without-failed-assertion','id':identifier,'limit':'Retained source may express a Boolean assertion outside the list.'})
        blockers = raw.get('blocked_predicates') or raw.get('unexecuted_predicates') or []
        blocker = raw.get('blocker') or row.get('blocker') or raw.get('reason')
        if isinstance(blockers,str): blockers = [blockers]
        if status in ('BLOCKED','PARTIALLY_EXECUTED') and not blockers and not blocker:
            blocker = raw.get('blocked_reason') or raw.get('error') or 'Inspect the linked retained result limits for the unavailable canonical predicates.'
        evidence[identifier] = {'path':path,'raw':raw,'group':group,'status':status,'original_status':original_status,'execution_status':execution_status,'assertion_count':assertions_count,'failed_assertions':failed_assertions,'blocked_predicates':blockers,'blocker':blocker,'summary_path':summary_path,'binding':binding,'status_normalization':normalization}

    prior_browser_summary = OLD/'new-e2e-summary.json'
    browser = read(prior_browser_summary)
    for row in browser.get('cases',browser.get('results',[])):
        identifier = row.get('id') or row.get('case_id')
        value = row.get('result') or identifier.lower()+'/result.json'
        add_result(identifier,resolve_result(value,prior_browser_summary),'prior-browser',prior_browser_summary,row,binding=OLD/'execution-source-binding.json')
    prior_security_summary = OLD/'security-probe-execution.json'
    security = read(prior_security_summary)
    for row in security['cases']:
        identifier = row['case_id']
        path = OLD/({'RN-S001':'valid-logout-case.json','RN-S002':'expired-logout-case.json'}.get(identifier,identifier+'-credential-case.json'))
        raw = read(path)
        passed = raw.get('assertions_passed',raw.get('security_assertion_passed'))
        add_result(identifier,path,'prior-security',prior_security_summary,row,'PASSED' if passed else 'FAILED',prior_security_summary)

    for relative, group, key in [('security/security-summary.json','security','results'),('workspace-transport/summary.json','workspace-transport','cases'),('combinations/combination-summary.json','combinations','results')]:
        summary_path = RUN/relative
        summary = read(summary_path)
        for row in summary[key]:
            identifier = row.get('instance_id') or row.get('case_id') or row.get('id')
            result_path=resolve_result(row['result'],summary_path)
            raw_for_binding=read(result_path)
            explicit_binding=None
            if group=='security':
                explicit_binding=frontend_binding_path if 'browser' in str(raw_for_binding.get('execution_level','')).lower() else RUN/'security/server-execution.json'
            add_result(identifier,result_path,group,summary_path,row,binding=explicit_binding)

    integration = RUN/'core-integration'
    for path in sorted(integration.glob('RN-*/result.json')):
        identifier = path.parent.name
        add_result(identifier,path,'core-integration',binding=integration/'source-binding.json')

    core_summary = args.core_summary.resolve()
    if core_summary.is_file():
        core = read(core_summary)
        for row in core.get('results',core.get('rows',core.get('cases',[]))):
            identifier = row.get('instance_id') or row.get('case_id') or row.get('id')
            add_result(identifier,resolve_result(row['result'],core_summary),'core-browser',core_summary,row,binding=frontend_binding_path)
    else:
        pending_inputs.append(workspace_path(core_summary))

    unknown = sorted(set(evidence)-set(definitions))
    if unknown: issues.append({'kind':'undefined-execution-ids','ids':unknown})
    rows=[]
    mismatch_cases=[]
    mismatch_associations=[]
    missing_source_hashes=[]
    for identifier,item in definitions.items():
        case = item['case']
        case_id = case['id']
        if case_id not in positions:
            issues.append({'kind':'missing-canonical-heading','id':case_id})
            continue
        line,end = positions[case_id]
        definition = {'path':'06-test-cases.md','anchor':case_id.lower(),'heading_line':line+1,'catalog_sha256':sha(catalog_bytes),'block_sha256':sha(''.join(lines[line:end]).encode()),'inventory':task_path(item['path']),'inventory_sha256':sha(item['path'].read_bytes()),'entry_sha256':json_sha(item.get('row',case))}
        definition_link = '06-test-cases.md#'+case_id.lower()
        if 'row' in item:
            row_id=item['row']['row_id']
            found=[number for number in range(line,end) if re.search(r'\|\s*'+re.escape(row_id)+r'\s*\|',lines[number])]
            if len(found)!=1: issues.append({'kind':'example-row-locator','id':identifier,'matches':len(found)})
            else:
                definition['example_row_line']=found[0]+1
                definition['example_row_sha256']=sha(lines[found[0]].encode())
                definition_link='06-test-cases.md#L'+str(found[0]+1)
        source_associations=[]
        for source in case.get('sources',[]):
            actual=candidate_hashes.get(source['path'])
            declared=source.get('sha256')
            match=actual==declared if actual and declared else None
            association={'path':source['path'],'definition_revision':source.get('revision'),'definition_sha256':declared,'candidate_sha256':actual,'matches':match}
            source_associations.append(association)
            if match is False:
                mismatch_associations.append({'id':identifier,**association})
            elif match is None:
                missing_source_hashes.append({'id':identifier,'path':source['path'],'reason':'Definition hash or selected candidate source hash is unavailable.'})
        if any(a['matches'] is False for a in source_associations):mismatch_cases.append(identifier)
        result=evidence.get(identifier)
        if result is None:
            group='core-browser' if item['group']=='core' else item['group']
            rows.append({'id':identifier,'status':'NOT_RUN','group':group,'newly_requested':True,'title':case.get('title'),'family':case.get('family'),'use_case':case.get('use_case'),'ac_ids':case.get('ac_ids',[]),'definition':definition_link,'definition_identity':definition,'definition_sources':source_associations,'result':None,'result_sha256':None,'blocker':'Final reconciled source-bound execution result has not been supplied.','blocked_predicates':case.get('then',[]),'basis':case.get('basis'),'characterization':case.get('basis')=='policy-open'})
            continue
        raw=result['raw']
        actual_binding=result['binding']
        if actual_binding is None and raw.get('source_binding'):
            try:
                actual_binding=resolve_result(raw['source_binding'],result['path'])
            except FileNotFoundError:
                issues.append({'kind':'unresolved-source-binding','id':identifier,'value':raw['source_binding']})
        binding_digest=None
        if actual_binding:
            read(actual_binding)
            binding_digest=sha(actual_binding.read_bytes())
        policy=raw.get('business_acceptance') or ('BLOCKED_POLICY' if case.get('basis')=='policy-open' else 'PENDING_HUMAN_REVIEW' if case.get('basis')=='proposed-security' else 'NOT_ASSESSED')
        rows.append({'id':identifier,'status':result['status'],'group':result['group'],'newly_requested':not result['group'].startswith('prior-'),'title':case.get('title'),'family':case.get('family'),'use_case':case.get('use_case'),'ac_ids':case.get('ac_ids',[]),'definition':definition_link,'definition_identity':definition,'definition_sources':source_associations,'result':task_path(result['path']),'result_workspace_path':workspace_path(result['path']),'result_sha256':sha(result['path'].read_bytes()),'summary':task_path(result['summary_path']) if result['summary_path'] else None,'summary_sha256':sha(result['summary_path'].read_bytes()) if result['summary_path'] else None,'source_binding':task_path(actual_binding) if actual_binding else None,'source_binding_sha256':binding_digest,'revision':raw.get('revision'),'execution_level':raw.get('execution_level') or raw.get('execution_mode'),'original_status':result['original_status'],'status_normalization':result['status_normalization'],'execution_status':result['execution_status'],'assertion_count':result['assertion_count'],'failed_assertions':result['failed_assertions'],'blocked_predicates':result['blocked_predicates'],'blocker':result['blocker'],'error':raw.get('error'),'basis':case.get('basis'),'characterization':case.get('basis')=='policy-open' or 'characterization' in str(raw.get('execution_level','')).lower(),'business_acceptance':policy,'limits':raw.get('limits',[])})
    rows.sort(key=lambda row:row['id'])
    groups={}
    for group in sorted({r['group'] for r in rows}):
        members=[r for r in rows if r['group']==group]
        groups[group]={'counts':count(members),'ids':[r['id'] for r in members]}
    missing=[r['id'] for r in rows if r['status']=='NOT_RUN']
    prior=[r for r in rows if not r['newly_requested']]
    new=[r for r in rows if r['newly_requested']]
    if len(prior)!=16:issues.append({'kind':'prior-count','actual':len(prior),'expected':16})
    if len(new)!=451:issues.append({'kind':'new-count','actual':len(new),'expected':451})
    if len(rows)!=467:issues.append({'kind':'reconciled-total','actual':len(rows),'expected':467})
    audit={'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PENDING_INPUT' if pending_inputs or missing else 'FAILED' if issues else 'PASSED','inputs_complete':not pending_inputs and not missing,'total':len(rows),'expected_total':467,'prior_count':len(prior),'new_count':len(new),'duplicate_or_unknown_result_ids':unknown,'missing_results':missing,'pending_inputs':pending_inputs,'issues':issues,'canonical_definition_source_mismatches':{'case_count':len(mismatch_cases),'association_count':len(mismatch_associations),'cases':mismatch_cases,'associations':mismatch_associations,'hash_unavailable_association_count':len(missing_source_hashes),'hash_unavailable_associations':missing_source_hashes},'inputs':[{'path':path,'sha256':digest} for path,digest in sorted(inputs.items())],'rules':['A case instance has one final disposition. Prior sixteen executions remain separate from the newly requested451.','Partial source assertions remain PARTIALLY_EXECUTED even when their runner passed.','ERROR denotes a failed execution mechanism and does not establish a failed business predicate.','PASSED observation cases do not approve unresolved policy.','Unit tests and historical27 E2E cases are separate inventories and do not enter the467 denominator.']}
    final={'recorded_at':audit['recorded_at'],'status':audit['status'],'total':len(rows),'newly_requested':451,'previously_executed':16,'counts':count(rows),'new_counts':count(new),'prior_counts':count(prior),'groups':groups,'rows':rows,'failed_ids':[r['id'] for r in rows if r['status']=='FAILED'],'partial_ids':[r['id'] for r in rows if r['status']=='PARTIALLY_EXECUTED'],'blocked_ids':[r['id'] for r in rows if r['status']=='BLOCKED'],'error_ids':[r['id'] for r in rows if r['status']=='ERROR'],'not_run_ids':missing,'characterization_passed_ids':[r['id'] for r in rows if r['status']=='PASSED' and r.get('characterization')],'source_definition_mismatch_count':len(mismatch_cases),'source_definition_mismatch_ids':mismatch_cases,'audit':'reconciliation-audit.json','scope_limits':audit['rules']}
    (OUT/'final-inventory.json').write_text(json.dumps(final,indent=2)+'\n')
    (OUT/'reconciliation-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    print(json.dumps({'status':audit['status'],'counts':final['counts'],'new_counts':final['new_counts'],'issues':issues,'pending_inputs':pending_inputs,'source_definition_mismatch_count':len(mismatch_cases)},indent=2))
    return 1 if issues or (args.require_complete and (missing or pending_inputs)) else 0


if __name__=='__main__':
    sys.exit(main())
