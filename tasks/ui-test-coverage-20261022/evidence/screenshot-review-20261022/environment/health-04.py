from pathlib import Path
import datetime,hashlib,json,urllib.request
root=Path.cwd();out=root/'tasks/ui-test-coverage-20261022/evidence/screenshot-review-20261022/environment';config=json.loads((out/'stack-config-04.json').read_text());rows=[];opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
for url in config['readyUrls']:
 try:
  with opener.open(url,timeout=3) as response:
   data=response.read();rows.append({'url':url,'status':response.status,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
 except Exception as e: rows.append({'url':url,'error':type(e).__name__,'reason':str(e)})
result={'recordedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASSED' if all(row.get('status')==200 for row in rows) else 'FAILED','http':rows,'priorProbe':{'path':str((out/'health-04.json').relative_to(root)),'limit':'Default sandbox localhost probe returned URLError. Elevated read-only probe checks actual service readiness.'},'limits':['This read-only check establishes service readiness only. It does not execute any UI scenario.','Current BFF8090 and PostgreSQL54390 are outside launch04.']};(out/'health-04-local.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'checks':len(rows)}))
