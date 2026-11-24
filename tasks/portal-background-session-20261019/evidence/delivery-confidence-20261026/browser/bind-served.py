from pathlib import Path
import urllib.request,json,hashlib,re,datetime
root=Path.cwd();stage=root/'tasks/portal-background-session-20261019/evidence/delivery-confidence-20261026/browser';bindings=json.loads((stage/'source-bindings.json').read_text());op=urllib.request.build_opener(urllib.request.ProxyHandler({}));result={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'refs':{}}
for label,source in bindings['refs'].items():
 port=source['mfe_port'];host=f'http://127.0.0.1:{port}';base=op.open(host+'/base.js').read();urls=['base.js.map'];urls+=list(set(re.findall(r'([a-f0-9]+\.src_pages_Home_index_tsx\.base\.js)',base.decode())))
 # Webpack development chunks have deterministic names. Get loaded chunk filename from bootstrap.
 if len(urls)==1:
  for suffix in re.findall(r'([a-f0-9]+)"?[^\n]{0,50}?src_pages_Home_index_tsx',base.decode()):urls.append(suffix+'.src_pages_Home_index_tsx.base.js')
 # Development listing includes every generated asset.
 listing=op.open(host+'/webpack-dev-server').read().decode()
 for name in re.findall(r'[^"\s<>/]*src_pages_Home_index_tsx[^"\s<>/]*\.js',listing):urls.append(name)
 maps=[];matched={};mismatches=[]
 for url in list(dict.fromkeys(urls)):
  if not url.endswith('.map'):url+='.map'
  try:raw=op.open(host+'/'+url).read();m=json.loads(raw)
  except Exception:continue
  maps.append({'url':host+'/'+url,'sha256':hashlib.sha256(raw).hexdigest(),'source_count':len(m['sources'])})
  for name,content in zip(m['sources'],m.get('sourcesContent',[])):
   if '/src/' not in name or content is None:continue
   local='src/'+name.split('/src/',1)[1].split('?',1)[0]
   expected=source['files'].get(local)
   if not expected:continue
   digest=hashlib.sha256(content.encode()).hexdigest();item={'expected_sha256':expected,'served_sha256':digest,'map':url};matched[local]=item
   if digest!=expected:mismatches.append(local)
 result['refs'][label]={'ref':source['ref'],'maps':maps,'matched_app_sources':matched,'mismatches':mismatches,'status':'PASSED' if not mismatches and matched else 'FAILED','limits':['Only sources present in fetched bundles are bound. Runtime webpack substitutions remain disclosed.']}
(stage/'served-source-binding.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:{'status':v['status'],'matched':len(v['matched_app_sources']),'maps':len(v['maps']),'mismatches':v['mismatches']} for k,v in result['refs'].items()}))
