from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
import hashlib,json,sys
from ai_sdlc_workbench.release_report_render import render_review_summary
sys.path.insert(0,str(Path.cwd()/'tests'))
from test_release_report_render import Elements
root=Path.cwd();base=Path(__file__).resolve().parent
for name in ['session-refresh','ces']:
 index=base/('session-refresh-index.json' if name=='session-refresh' else 'ces-migration-index.json');payload=json.loads(index.read_text());before={r['path']:hashlib.sha256((root/r['path']).read_bytes()).hexdigest() for r in payload['artifacts']}
 out=render_review_summary(index,root,base/(name+'-summary.html'));dom=Elements(out.read_text());visible=dom.text(initial=True)
 checks={'input_bytes_unchanged':all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in before.items()),'no_active_or_remote_content':not any(tag in {'script','iframe','img','link'} for tag,_ in dom.tags),'supporting_details_collapsed':all('open' not in attrs for tag,attrs in dom.tags if tag=='details'),'unknown_authorization_visible':'Human deployment authorization: UNKNOWN' in visible}
 if name=='session-refresh':
  counts=Counter(r['outcome'] for r in payload['executions']);checks.update({'467_records':sum(counts.values())==467,'all_outcomes_preserved':counts=={'PASSED':182,'FAILED':15,'PARTIAL':199,'BLOCKED':71},'285_priority_rows':len(payload['assessment']['issues'])==285,'hold_visible':all(s in visible for s in ['NO_GO','RN-S002','issued new access','authentication owner','Correct the applicable revocation']),'minor_disruption_not_invented':not next(r for r in payload['assessment']['issues'] if r['id']=='RN-A001')['release_blocking']})
 else:checks.update({'unknown_release_preserved':'INSUFFICIENT_EVIDENCE' in visible,'no_invented_execution':'0 retained execution records' in visible,'unknown_scope':set(payload['inventory_completeness'].values())=={'UNKNOWN'}})
 receipt={'case_id':'SUMMARY-'+name.upper(),'status':'PASSED' if all(checks.values()) else 'FAILED','checked_at':datetime.now(timezone.utc).isoformat(),'checks':checks,'files':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [index,out,root/'core/release_report_render.py',root/'core/cli.py',root/'core/schemas/review-index.schema.json']},'limits':['Retained historical assessment only. Newer source composition requires independent assessment.','HTML structure and source integrity are checked. Business acceptance remains separate.']}
 (base/(name+'-result.json')).write_text(json.dumps(receipt,indent=2)+'\n');print(name,receipt['status']);assert all(checks.values()),checks
