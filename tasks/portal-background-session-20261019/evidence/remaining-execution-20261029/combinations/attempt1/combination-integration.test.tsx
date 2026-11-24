import React from 'react';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {Buffer} from 'buffer';
import {AxiosAdapter, AxiosError, AxiosResponse, InternalAxiosRequestConfig} from 'axios';
import {act,cleanup,render} from '@testing-library/react';
import Provider from '../hooks/provider';
import {getHooksBase} from '../hooks/HooksBase';
import service from '../hooks/service/config';
import {getRefreshToken,relogin,signal} from '../hooks/service';
import {extendToken,signal as activitySignal} from '../hooks/service/util/extend';
import useServices from '../services';
import useTimeout from '../components/Timeout/common/useController';
import {currentSessionEpoch} from '../utils/sessionEpoch';
import {getJWTPayload} from '../utils/common';

jest.mock('../analytics',()=>()=>({ButtonEvent:jest.fn(),TileEvent:jest.fn(),TabEvent:jest.fn(),ModalEvent:jest.fn()}));

const out=process.env.COMBINATION_OUTPUT!;
const definitions=JSON.parse(fs.readFileSync(process.env.COMBINATION_DEFINITIONS!,'utf8'));
const revision='66c6411ade58e4d134e381c2baee8ad3f76a8dbf';
const now=Date.parse('2026-10-29T02:00:00Z');
const sha=(x:any)=>crypto.createHash('sha256').update(typeof x==='string'?x:JSON.stringify(x)).digest('hex');
const token=(subject:string,remaining:number,label='access')=>`Bearer e30.${Buffer.from(JSON.stringify({sub:subject,jti:label,iat:Math.floor(now/1000)-1,exp:(Date.now()+remaining)/1000})).toString('base64')}.synthetic`;
interface Pending {config:InternalAxiosRequestConfig;resolve:(x:AxiosResponse)=>void;reject:(e:any)=>void;settled?:boolean;}
const rows=[...definitions.pairwise_rows.map((r:any)=>({...r,outline:'RN-C001'})),...definitions.risk_rows.map((r:any)=>({...r,outline:'RN-C002'})),...definitions.order_rows.map((r:any)=>({...r,outline:'RN-O001'}))];
let controller:any,services:any;
const Timeout=()=>{controller=useTimeout({setOpen:()=>{}} as any);return null;};
const Fixture=({manual}:{manual:boolean})=>{services=useServices();return manual?<Timeout/>:null;};
const originalAdapter=service.defaults.adapter;
const originalVisibility=Object.getOwnPropertyDescriptor(document,'visibilityState');

const rawSnapshot=()=>{const s=getHooksBase().store;return{token:s.token,refresh:s.refreshToken,expiry:s.expiredIn,iat:s.iat,user:s.user,error:s.errorMsg,onLogout:s.isOnLogout,local:localStorage.getItem('SET_TOKEN'),session:sessionStorage.getItem('SET_TOKEN')};};
const safeSnapshot=()=>{const s=rawSnapshot();return{subject:s.token?getJWTPayload(s.token)?.sub:null,access_sha256:s.token?sha(s.token):null,refresh_sha256:s.refresh?sha(s.refresh):null,expiry:s.expiry,iat:s.iat,user_sha256:s.user?sha(s.user):null,error:s.error,onLogout:s.onLogout,local_access_sha256:s.local?sha(s.local):null,session_access_sha256:s.session?sha(s.session):null};};
const flush=async()=>{await act(async()=>{await Promise.resolve();await Promise.resolve();});};

describe('Source-bound renewal combinations',()=>{
 beforeEach(()=>{jest.useFakeTimers();jest.setSystemTime(now);localStorage.clear();sessionStorage.clear();controller=undefined;services=undefined;Object.defineProperty(document,'visibilityState',{configurable:true,value:'visible'});});
 afterEach(async()=>{signal.getRefreshToken?.abort();signal.relogin?.abort();activitySignal.extendToken?.abort();signal.getRefreshToken=undefined;signal.relogin=undefined;activitySignal.extendToken=undefined;cleanup();service.defaults.adapter=originalAdapter;jest.clearAllTimers();jest.useRealTimers();if(originalVisibility)Object.defineProperty(document,'visibilityState',originalVisibility);else Reflect.deleteProperty(document,'visibilityState');localStorage.clear();sessionStorage.clear();});
 for(const row of rows){
  it(`${row.outline}/${row.row_id}`,async()=>{
   const folder=path.join(out,row.outline+'-'+row.row_id);fs.mkdirSync(folder,{recursive:true});
   const result:any={case_id:row.outline,instance_id:row.outline+'/'+row.row_id,row_id:row.row_id,inputs:row,revision,definition:'../../../06-test-cases.md#'+row.outline.toLowerCase(),started_at:new Date().toISOString(),execution_level:'actual-source React/Axios integration in jsdom',status:'RUNNING',assertions:[],events:[],requests:[],blocked_predicates:[],limits:['Exact product React Provider, reducers, Timeout hook, session ownership, service helpers, Axios interceptors execute.','Synthetic unsigned JWTs and controlled Axios adapter replace identity/provider/network responses.','No real HTTP server, native lifecycle, transport connection, protected business endpoint, or durable mutation service.'],source_binding:'../source-binding.json'};
   const save=()=>fs.writeFileSync(path.join(folder,'result.json'),JSON.stringify(result,null,2)+'\n');save();
   const pending:Pending[]=[];
   const inFlight:Promise<any>[]=[];
   const requestSummaries=new Map<Pending,any>();
   const recordCheck=(name:string,actual:any,expected:any)=>{const ok=JSON.stringify(actual)===JSON.stringify(expected);result.assertions.push({name,actual,expected,status:ok?'PASSED':'FAILED'});expect(actual).toEqual(expected);};
   const adapter:AxiosAdapter=config=>new Promise((resolve,reject)=>{const q={config,resolve,reject} as Pending;pending.push(q);const note={url:config.url,epoch:(config as any).sessionEpoch,aborted:!!config.signal?.aborted,settled:false};result.requests.push(note);requestSummaries.set(q,note);if(config.url?.endsWith('/logout')||config.url?.endsWith('/imeta/logout')){q.settled=true;note.settled=true;resolve({config,data:{result:true},headers:{},status:200,statusText:'OK'});}});
   service.defaults.adapter=adapter;
   const selected=(endpoint:string)=>pending.filter(p=>!p.settled&&p.config.url?.endsWith('/'+endpoint));
   const settle=async(q:Pending,outcome:string,subject:string)=>{if(!q||q.settled)return;const note=requestSummaries.get(q);q.settled=true;note.settled=true;note.outcome=outcome;note.aborted_at_delivery=!!q.config.signal?.aborted;note.epoch_at_delivery=currentSessionEpoch();await act(async()=>{if(outcome==='rejected')q.reject(new AxiosError('Controlled rejection','ERR_BAD_REQUEST',q.config,undefined,{config:q.config,data:{errorMessage:'Controlled rejection'},headers:{},status:503,statusText:'Unavailable'}));else if(outcome==='timeout')q.reject(new AxiosError('Controlled timeout','ECONNABORTED',q.config));else {let headers:any={};if(q.config.url?.endsWith('/refreshtoken'))headers={'single-ui-refresh':outcome==='malformed'?'Bearer invalid':token(subject,4*60*60_000,'refresh-response')};else if(q.config.url?.endsWith('/login')||q.config.url?.endsWith('/relogin')||q.config.url?.endsWith('/extend'))headers={'single-ui-authorization':outcome==='malformed'?'Bearer invalid':token(subject,120_000,'access-response')};q.resolve({config:q.config,data:{result:true},headers,status:200,statusText:'OK'});}await Promise.resolve();});};
   const launch=(f:()=>any)=>{try{const p=f();if(p?.then)inFlight.push(Promise.resolve(p).catch(()=>undefined));}catch(e){result.events.push({at:Date.now(),driver_call_error:String(e)});}};
   const start=async(trigger:string)=>{await act(async()=>{if(trigger==='manual'){if(controller)launch(()=>controller.extend());else launch(()=>relogin());}else if(trigger==='refresh-acquisition')launch(()=>getRefreshToken());else launch(()=>extendToken());});await flush();};
   const loginB=async()=>{await act(async()=>{launch(()=>services.login({code:'synthetic-B'}));});await flush();const q=selected('login').slice(-1)[0];if(!q)throw new Error('Fixture login B did not reach actual Axios adapter');await settle(q,'usable','B');await flush();};
   try{
    const accessRemaining=Number(row.access_ms??60000);
    let refresh=token('A',4*60*60_000,'refresh-initial');
    if(row.refresh==='valid-two-seconds')refresh=token('A',2000,'refresh-initial');
    if(row.refresh==='expired')refresh=token('A',-1000,'refresh-initial');
    if(row.refresh==='missing')refresh=undefined as any;
    const workspaces=Array.from({length:Number(row.workspaces??1)},(_,i)=>({id:'WA-'+i,label:'Workspace '+i,tileData:[]}));
    render(<Provider data={{token:token('A',accessRemaining),refreshToken:refresh,expiredIn:(now+accessRemaining)/1000,workspaces,currentWorkspace:workspaces[0] as any}}><Fixture manual={row.outline!=='RN-O001'&&row.trigger==='manual'}/></Provider>);
    await flush();result.initial=safeSnapshot();
    if(row.outline==='RN-O001'){
     let requestA:Pending|undefined,requestB:Pending|undefined;
     for(const event of row.events.split(' > ')){
      const before=rawSnapshot();
      if(event==='start-A'){await start('manual');requestA=selected('relogin').slice(-1)[0];recordCheck('start-A creates one actual renewal request',!!requestA,true);}
      else if(event==='logout-A'){await act(async()=>services.logout());await flush();recordCheck('logout-A clears access',!!getHooksBase().store.token,false);}
      else if(event==='login-B'){await loginB();recordCheck('login-B installs B subject',safeSnapshot().subject,'B');}
      else if(event==='start-B'){await start('manual');requestB=selected('relogin').slice(-1)[0];recordCheck('start-B creates an actual renewal request',!!requestB,true);}
      else if(event==='reply-B'){await settle(requestB!,'usable','B');await flush();recordCheck('reply-B installs B subject',safeSnapshot().subject,'B');}
      else if(event==='reply-A'){
       await settle(requestA!,row.old_response,'A');await flush();
       if(row.events.indexOf('logout-A')<row.events.indexOf('reply-A'))recordCheck('late A delivery changes zero current authentication fields',rawSnapshot(),before);
      }
      result.events.push({event,epoch:currentSessionEpoch(),snapshot:safeSnapshot()});save();
     }
     recordCheck('final installed credential subject equals B',safeSnapshot().subject,'B');result.status='PASSED';result.acceptance='Observed proposed invariant only; no business approval.';
    }else{
     const loading=row.loading??'idle';const loadingCount=loading==='idle'?0:loading==='one-request'?1:2;
     for(let i=0;i<loadingCount;i++)launch(()=>service.get('/api/combinations-fixture/read-'+i));await flush();
     await start(row.trigger);const renewal=pending.filter(q=>!q.settled&&/\/(relogin|refreshtoken|extend)$/.test(q.config.url??''));
     result.guard_observation={accepted_renewal_requests:renewal.length,access_remaining:accessRemaining,trigger:row.trigger};
     if(row.ownership==='logout-A'){await act(async()=>services.logout());await flush();}
     else if(row.ownership==='replace-with-B')await loginB();
     if(row.lifecycle==='hidden-after-start')Object.defineProperty(document,'visibilityState',{configurable:true,value:'hidden'});
     if(row.lifecycle==='resume-before-delivery'){Object.defineProperty(document,'visibilityState',{configurable:true,value:'hidden'});document.dispatchEvent(new Event('visibilitychange'));Object.defineProperty(document,'visibilityState',{configurable:true,value:'visible'});document.dispatchEvent(new Event('visibilitychange'));}
     if(row.lifecycle==='unmount-after-start'){cleanup();result.events.push({event:'react-fixture-unmounted'});}
     const protectedBefore=rawSnapshot();
     const order=row.delivery==='reverse'?[...renewal].reverse():renewal;
     for(const q of order)await settle(q,row.response,'A');await flush();
     if(row.ownership!=='unchanged-A')recordCheck('obsolete epoch response installs zero authentication changes',rawSnapshot(),protectedBefore);
     else recordCheck('no obsolete epoch response was created',renewal.filter(q=>(q.config as any).sessionEpoch!==currentSessionEpoch()).length,0);
     for(const q of pending.filter(q=>!q.settled&&q.config.url?.includes('/combinations-fixture/')))await settle(q,loading==='mixed-outcomes'?'rejected':'usable','A');await flush();
     result.final=safeSnapshot();
     result.bounded_execution={status:'PASSED',assertions:result.assertions.length,predicates:'Actual source epoch/credential isolation only. Not the complete canonical business/transport oracle.'};
     result.blocked_predicates.push({predicate:'unauthorized protected business mutations equal 0',reason:'No protected business mutation endpoint, server authorization context, or durable commit observation is defined or available in this isolated fixture.',required_evidence:'Named protected operation, authoritative identity/authorization service, and retained server transaction outcomes.'});
     if(row.outline==='RN-C001'){
      result.blocked_predicates.push({predicate:'each business operation identifier has at most 1 committed mutation',reason:'Canonical design has no business operation identifier source or durable transaction ledger.',required_evidence:'Reviewed operation/idempotency contract and instrumented transaction service.'});
      result.blocked_predicates.push({predicate:'concurrent transport and named network/lifecycle schedule',reason:'The selected '+row.transport+' connection, '+row.network+' network schedule, and native browser lifecycle are not executed by this jsdom integration.',required_evidence:'Actual selected transport service and browser/network controller for this row.'});
     }
     result.status='BLOCKED';result.execution_status='PARTIALLY_EXECUTED';
    }
   }catch(error){result.error=String((error as Error).message);if(row.outline==='RN-O001'){result.status='FAILED';result.execution_status='EXECUTED';}else{result.status='BLOCKED';result.execution_status='PARTIALLY_EXECUTED';result.bounded_execution={status:'FAILED',error:result.error};result.blocked_predicates.push({predicate:'complete canonical scenario',reason:'The source-integration probe did not complete; see failed bounded assertion and environment limits.'});}throw error;}
   finally{result.completed_at=new Date().toISOString();result.final=safeSnapshot();for(const q of pending.filter(q=>!q.settled)){q.settled=true;q.resolve({config:q.config,data:{result:true},headers:{},status:200,statusText:'OK'});}await act(async()=>{await Promise.allSettled(inFlight);});save();}
  },20000);
 }
});
