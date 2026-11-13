from pathlib import Path
import hashlib,json,re
root=Path('/Users/lushevol/code/github/ratan-release-impact/workbench')
out=root/'docs/evidence/conversation-improvements-implementation-20261030/stage-2'
task=Path('tasks/portal-background-session-20261019')
aggregate=task/'evidence/remaining-execution-20261029/aggregate/final-inventory.json'
assertion_map=task/'evidence/comprehensive-renewal-20261028/assertion-map.json'
priority=task/'evidence/report-impact-priority-20261029/case-priority-audit.json'
source=json.loads((root/aggregate).read_text())
mapping=json.loads((root/assertion_map).read_text())
triage=json.loads((root/priority).read_text())
artifacts={}
def artifact(rel,kind):
    rel=Path(rel).as_posix()
    key=(rel,kind)
    if key not in artifacts:
        artifacts[key]={'id':'ART-'+hashlib.sha256((rel+':'+kind).encode()).hexdigest()[:20],'kind':kind,'path':rel,'sha256':hashlib.sha256((root/rel).read_bytes()).hexdigest()}
    return {'artifact_id':artifacts[key]['id']}
def empty(identifier,scope,title):
    return {'schema_version':1,'id':identifier,'scope_id':scope,'title':title,'inventory_completeness':{'criteria':'UNKNOWN','changes':'UNKNOWN','cases':'UNKNOWN'},'artifacts':[],'criteria':[],'changes':[],'cases':[],'assertions':[],'links':[],'executions':[],'limits':[]}
payload=empty('session-refresh-summary-pilot','portal-background-session-20261019','Session Refresh: recorded release assessment')
aggregate_ref=artifact(aggregate,'SOURCE')
map_ref=artifact(assertion_map,'SOURCE')
for entry in mapping['ac_to_assertions']:
    loc=artifact(entry['requirement']['path'],'INTENT')|{'start_line':entry['requirement']['lines'][0],'end_line':entry['requirement']['lines'][1]}
    payload['criteria'].append({'id':entry['ac_id'],'definition':loc,'required_levels':['SYSTEM'],'limits':['Candidate requirement; review and publication state remain separate.','This pilot imports definitions; it does not assert required-level completeness.']})
selected=[row['id'] for row in source['rows']]
for row in source['rows']:
    if row['id'] not in selected:continue
    cid=row['id']
    relative,_,anchor=row['definition'].partition('#')
    loc=artifact(task/relative,'INTENT')
    loc |= {'start_line':int(anchor[1:]),'end_line':int(anchor[1:])} if re.fullmatch(r'L\d+',anchor) else {'anchor':anchor}
    payload['cases'].append({'id':cid,'definition':loc,'limits':row['limits']+['Definition references identify current retained catalog bytes; historical definition/source mismatches remain recorded in the original inventory.']})
    execution={'id':'EXEC-'+cid,'case_id':cid,'source':artifact(row['result_workspace_path'],'EXECUTION'),'original_status':row.get('original_status'),'outcome':{'PARTIALLY_EXECUTED':'PARTIAL'}.get(row['status'],row['status']),'characterization':row['characterization'],'level':'UNKNOWN','mode':'UNKNOWN','assertion_ids':[],'environment_id':None,'limits':row['limits']+['Outcome and characterization are imported declarations from the retained aggregate.','Assertion completeness and target identity were not verified by this index pilot.']}
    if row.get('source_binding'):execution['source_binding']=artifact(task/row['source_binding'],'SOURCE')
    payload['executions'].append(execution)
    for ac in row.get('ac_ids',[]):
        if ac in {a['id'] for a in payload['criteria']}:
            payload['links'].append({'id':'LINK-'+ac+'-'+cid,'relationship':'AC_CASE','from_id':ac,'to_id':cid,'evidence':[aggregate_ref],'assertion_ids':[],'predicate_scope':'SELECTED','conformance':'UNKNOWN','limits':['Association supplied by the retained catalog; no direct assertion chain is claimed.']})
issues=[]
priority_ref=artifact(priority,'ASSESSMENT')
for row in triage['rows']:
    if row['id'] in selected:
        issues.append({'id':row['id'],'title':row['title'],'observed_impact':row['observed_user_impact'],'priority':row['new_priority'],'release_blocking':row['release_blocking'],'owner':row['owner'],'next_action':row['next_action'],'evidence':[priority_ref,artifact(task/row['result'],'EXECUTION')],'limits':row.get('evidence_limits',[])+['Historical source assessment. Production reachability and newer server applicability remain unverified.']})
payload['assessment']={'source':artifact(task/'10-release-confidence.md','ASSESSMENT'),'recommendation':'NO_GO','decision_certainty':'HIGH','summary':'Recorded assessment holds the assessed source composition because logout permits credential replay. Newer servers remain outside that assessment.','review_state':'pending','issues':issues,'limits':['This imports a recorded assessment. It is not a new release recommendation or deployment authorization.']}
payload['inventory_completeness']={'criteria':'COMPLETE','changes':'UNKNOWN','cases':'COMPLETE'}
payload['limits']=['All467 retained instances. This inventory does not establish complete intended behavior.','Original artifacts, statuses, characterization, and case priority dispositions are preserved.','The seven criteria concern the named candidate requirement. They do not establish approved business scope.','No source implementation or business behavior was executed by this reference-validation pilot.']
payload['artifacts']=list(artifacts.values())
(out/'session-refresh-index.json').write_text(json.dumps(payload,indent=2)+'\n')
artifacts.clear()
ces=empty('ces-migration-reference-pilot','CES-MIGRATION','CES migration: draft criterion with unknown approved inventories')
ces['criteria']=[{'id':'MIG-AC-001','definition':artifact('tasks/ces-entitlement-migration-20261102/01-intake.md','INTENT')|{'anchor':'mig-ac-001'},'required_levels':['SYSTEM'],'limits':['Draft criterion only. The approved AC denominator remains unknown.','System observation is the proposed verification method in the intake, not executed acceptance.']}]
ces['limits']=['The real intake permits understanding handoff. Implementation planning remains NEEDS_CLARIFICATION.','Approved criterion, complete change, and case inventories remain UNKNOWN. No executions are declared.']
ces['artifacts']=list(artifacts.values())
(out/'ces-migration-index.json').write_text(json.dumps(ces,indent=2)+'\n')
print(json.dumps({'session_selected_cases':len(payload['cases']),'session_execution_outcomes':{r['case_id']:r['outcome'] for r in payload['executions']},'ces_draft_criteria':len(ces['criteria']),'ces_inventory':ces['inventory_completeness']},indent=2))
