from pathlib import Path
import urllib.request,json,hashlib,re,datetime
root=Path.cwd();stage=root/'tasks/portal-background-session-20261019/evidence/ut-remediation-20261027/final-cancellation-browser';binding=json.loads((stage/'source-binding.json').read_text());op=urllib.request.build_opener(urllib.request.ProxyHandler({}));host='http://127.0.0.1:8142'
base=op.open(host+'/base.js').read();listing=op.open(host+'/webpack-dev-server').read().decode();urls=['base.js.map']
for name in re.findall(r'[^"\s<>/]*src_pages_Home_index_tsx[^"\s<>/]*\.js',listing):urls.append(name+'.map')
maps=[];matched={};mismatches=[]
for url in dict.fromkeys(urls):
 try:raw=op.open(host+'/'+url).read();m=json.loads(raw)
 except Exception:continue
 maps.append({'url':host+'/'+url,'sha256':hashlib.sha256(raw).hexdigest(),'source_count':len(m['sources'])})
 for name,content in zip(m['sources'],m.get('sourcesContent',[])):
  if '/src/' not in name or content is None:continue
  local='src/'+name.split('/src/',1)[1].split('?',1)[0];expected=binding['source_files'].get(local)
  if not expected:continue
  digest=hashlib.sha256(content.encode()).hexdigest();matched[local]={'expected_sha256':expected,'served_sha256':digest,'map':url}
  if digest!=expected:mismatches.append(local)
required=['src/hooks/service/util/requestLoading.ts','src/hooks/service/util/succes.response.handler.ts','src/hooks/service/util/success.request.handler.ts','src/hooks/service/util/error.response.handler.ts','src/components/Loader/PageLoader.tsx','src/routing/index.tsx']
missing=[p for p in required if p not in matched]
result={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate_commit':binding['candidate_commit'],'base_bundle_sha256':hashlib.sha256(base).hexdigest(),'maps':maps,'matched_app_sources':matched,'mismatches':mismatches,'required_paths':required,'missing_required':missing,'status':'PASSED' if not mismatches and not missing else 'FAILED','limits':['Only sources present in fetched bundles are bound. Local webpack and toolkit substitutions remain disclosed.']}
(stage/'served-source-binding.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'matched':len(matched),'missing_required':missing,'mismatches':mismatches}));assert result['status']=='PASSED'
