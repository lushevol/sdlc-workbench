const fs=require('node:fs');
const vm=require('node:vm');
const {stripTypeScriptTypes}=require('node:module');
const assert=require('node:assert/strict');
const crypto=require('node:crypto');
(async()=>{
 const sourcePath=process.argv[2], outputPath=process.argv[3];
 const source=fs.readFileSync(sourcePath,'utf8');
 let clock=0, sequence=0, calls=0; const timers=new Map();
 const context=vm.createContext({URLSearchParams,window:{location:{search:''}},document:{},setTimeout:(fn,delay)=>{const id=++sequence;timers.set(id,{fn,at:clock+delay});return id;},clearTimeout:id=>timers.delete(id)});
 const react={useRef:v=>({current:v}),useState:v=>[v,()=>{}],useEffect:()=>{}};
 const store={expiredIn:900,isOnLogout:false,token:'fixture',workspaces:[],entities:[],drawers:[]};
 const noop=()=>{};
 const values={
  react:{default:react},'../../../hooks/provider':{useContext:()=>[store,noop]},
  '../../../hooks/dispathcer':{default:()=>({})},'../../../hooks/model/workspaces':{Workspace:null},
  '../../../utils/common':{validateWorkspace:noop,aOrb:(a,b)=>a??b},
  '../../../hooks/service':{getRefreshToken:noop},'../../../hooks/service/util/extend':{extend:()=>{calls++;}},
  '../../../analytics':{default:()=>({ButtonEvent:noop,TileEvent:noop,TabEvent:noop})},'../../../analytics/model':{AnalyticsData:null},
  '../../../utils/login':{handleLoginEntities:noop},'./util':{setDetail:noop,refreshTabUtil:noop}
 };
 const module=new vm.SourceTextModule(stripTypeScriptTypes(source,{mode:'transform'}),{context,identifier:sourcePath});
 await module.link(async specifier=>{
  if(!(specifier in values))throw Error('Unexpected import '+specifier);
  const vals=values[specifier]; return new vm.SyntheticModule(Object.keys(vals),function(){for(const[k,v]of Object.entries(vals))this.setExport(k,v);},{context});
 }); await module.evaluate(); const controller=module.namespace.default();
 function advance(target){while(true){const next=[...timers.entries()].filter(([,t])=>t.at<=target).sort((a,b)=>a[1].at-b[1].at)[0];if(!next)break;clock=next[1].at;timers.delete(next[0]);next[1].fn();}clock=target;}
 for(let second=0;second<1000;second++){advance(second*1000);controller.mouseMove();}
 assert.equal(calls,0); const continuous={mouse_events:1000,event_interval_ms:1000,elapsed_ms:999000,extend_calls:calls};
 advance(1004000);assert.equal(calls,1);const afterPause={pause_after_last_event_ms:5000,extend_calls:calls};
 const result={status:'OBSERVED',sourcePath,sourceSha256:crypto.createHash('sha256').update(source).digest('hex'),continuous_activity:continuous,after_pause:afterPause,limits:['This harness executes the actual Home controller after Node TypeScript transformation.','React state hooks, effects, collaborators, and timers are controlled unit inputs.','Effects are not executed, so this does not establish full browser or backend behavior.','The result characterizes debounce scheduling, not a deployed session outcome.']};
 fs.writeFileSync(outputPath,JSON.stringify(result,null,2)+'\n');process.stdout.write(JSON.stringify({status:result.status,continuous_activity:continuous,after_pause:afterPause,output:outputPath})+'\n');
})().catch(e=>{process.stderr.write(e.stack+'\n');process.exitCode=1;});
