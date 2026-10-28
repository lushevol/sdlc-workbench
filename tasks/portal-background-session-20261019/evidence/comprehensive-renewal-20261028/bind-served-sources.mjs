import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
const out=path.join(process.cwd(),'tasks/portal-background-session-20261019/evidence/comprehensive-renewal-20261028');
const binding=JSON.parse(await fs.readFile(path.join(out,'execution-source-binding.json'),'utf8'));
const hash=x=>crypto.createHash('sha256').update(x).digest('hex');
const base='http://127.0.0.1:8242/';
const targets=['src/components/Timeout/common/useController.ts','src/components/Timeout/index.tsx','src/hooks/reducer/root0.reducers.ts','src/hooks/service/index.ts','src/hooks/service/config.ts','src/hooks/service/util/error.response.handler.ts','src/hooks/service/util/succes.response.handler.ts','src/hooks/service/util/success.request.handler.ts','src/hooks/service/util/requestLoading.ts','src/pages/Home/common/useController.ts','src/pages/Home/index.tsx','src/utils/common.ts','src/utils/sessionEpoch.ts'];
const result={revision:binding.revision,captured_at:new Date().toISOString(),matches:[],unmatched:[],map_urls:[],limit:'Development source maps bind source bytes, not a production artifact or an independent server signature.'};
const script=await(await fetch(base+'base.js')).text();
const mappings=JSON.parse(script.match(/__webpack_require__\.u = \(chunkId\) => \((\{[^\n]+?\})\[chunkId\]/)[1]);
const urls=[base+'base.js.map'];
for(const [chunk,contentHash] of Object.entries(mappings))urls.push(base+contentHash+'.'+chunk+'.base.js.map');
const pending=new Set(targets);
for(const url of [...new Set(urls)]){
 if(!pending.size)break;
 let map;try{const response=await fetch(url);if(!response.ok)continue;map=await response.json();}catch{continue;}
 result.map_urls.push(url);
 for(let index=0;index<map.sources.length;index++)for(const target of [...pending])if(map.sources[index].replaceAll('\\','/').endsWith('/'+target)||map.sources[index].endsWith('./'+target)){
  const served=hash(map.sourcesContent[index]);const expected=binding.source_hashes[target];
  result.matches.push({path:target,source_map_url:url,sha256:served,expected_sha256:expected,match:served===expected});pending.delete(target);
 }
}
result.unmatched=[...pending];result.status=result.unmatched.length===0&&result.matches.every(x=>x.match)?'PASSED':'INCOMPLETE';
await fs.writeFile(path.join(out,'served-source-binding.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({status:result.status,matches:result.matches.length,unmatched:result.unmatched}));
