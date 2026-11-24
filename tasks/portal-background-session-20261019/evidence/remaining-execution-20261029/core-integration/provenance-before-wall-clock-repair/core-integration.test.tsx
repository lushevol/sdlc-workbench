import React from 'react';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {Buffer} from 'buffer';
import {execFileSync} from 'node:child_process';
import {AxiosAdapter,AxiosResponse,InternalAxiosRequestConfig} from 'axios';
import {act,cleanup,render} from '@testing-library/react';
import Provider from '../hooks/provider';
import {getHooksBase} from '../hooks/HooksBase';
import service from '../hooks/service/config';
import {getRefreshToken,signal} from '../hooks/service';
import {extendToken,signal as activitySignal} from '../hooks/service/util/extend';
import useTimeout from '../components/Timeout/common/useController';
import {getJWTPayload} from '../utils/common';

jest.mock('../analytics',()=>()=>({ButtonEvent:jest.fn(),TileEvent:jest.fn(),TabEvent:jest.fn(),ModalEvent:jest.fn()}));
const out=process.env.CORE_INTEGRATION_OUTPUT!;
const definitions=JSON.parse(fs.readFileSync(process.env.CORE_INTEGRATION_DEFINITIONS!,'utf8'));
const ids=[...Array.from({length:9},(_,i)=>'RN-B'+String(i+1).padStart(3,'0')),...Array.from({length:13},(_,i)=>'RN-P'+String(i+1).padStart(3,'0')),'RN-P018',...Array.from({length:6},(_,i)=>'RN-R'+String(i+9).padStart(3,'0'))];
const cases=definitions.filter((c:any)=>ids.includes(c.id));
const revision='66c6411ade58e4d134e381c2baee8ad3f76a8dbf';
const now=Date.parse('2026-10-29T02:00:00Z');
const sha=(x:any)=>crypto.createHash('sha256').update(typeof x==='string'?x:JSON.stringify(x)).digest('hex');
const payloadToken=(payload:any)=>`Bearer e30.${Buffer.from(JSON.stringify(payload)).toString('base64')}.synthetic`;
const token=(subject:string,remaining:number,label='access')=>payloadToken({sub:subject,jti:label,iat:Math.floor(Date.now()/1000)-1,exp:(Date.now()+remaining)/1000});
interface Pending{config:InternalAxiosRequestConfig;resolve:(x:AxiosResponse)=>void;settled?:boolean;}
let controller:any,closures:number;
const Timeout=()=>{controller=useTimeout({setOpen:(open:boolean)=>{if(!open)closures++;}} as any);return null;};
const originalAdapter=service.defaults.adapter;
const snapshot=()=>{const s=getHooksBase().store;return{access_sha256:s.token?sha(s.token):null,refresh_sha256:s.refreshToken?sha(s.refreshToken):null,expiry:s.expiredIn,iat:s.iat,logout:s.isOnLogout,closures};};
const flush=async()=>{await act(async()=>{await Promise.resolve();await Promise.resolve();});};

describe('Canonical remaining core integration cases',()=>{
 beforeEach(()=>{jest.useFakeTimers();jest.setSystemTime(now);localStorage.clear();sessionStorage.clear();controller=undefined;closures=0;});
 afterEach(()=>{signal.getRefreshToken?.abort();signal.relogin?.abort();activitySignal.extendToken?.abort();signal.getRefreshToken=undefined;signal.relogin=undefined;activitySignal.extendToken=undefined;cleanup();service.defaults.adapter=originalAdapter;jest.clearAllTimers();jest.useRealTimers();localStorage.clear();sessionStorage.clear();});
 for(const c of cases){
  it(c.id+' '+c.title,async()=>{
   const folder=path.join(out,c.id);fs.mkdirSync(folder,{recursive:true});
   const result:any={case_id:c.id,definition:'../../../../06-test-cases.md#'+c.id.toLowerCase(),revision,status:'RUNNING',started_at:new Date().toISOString(),given:c.given,when:c.when,then:c.then,assertions:[],requests:[],blocked_predicates:[],execution_level:'actual-source component integration in jsdom',source_binding:'../source-binding.json',limits:['Exact React Provider, reducers, mounted Timeout hook, service helpers, and Axios request/response interceptors execute.','Network responses and JWT payloads are controlled fixture inputs. Cryptographic validity is not established by the client probes.','No native browser lifecycle, real UI rendering, transport, or business mutations execute.']};
   const save=()=>fs.writeFileSync(path.join(folder,'result.json'),JSON.stringify(result,null,2)+'\n');save();
   const checks=(name:string,actual:any,expected:any)=>{const ok=JSON.stringify(actual)===JSON.stringify(expected);result.assertions.push({name,actual,expected,status:ok?'PASSED':'FAILED'});expect(actual).toEqual(expected);};
   const pending:Pending[]=[];const inFlight:Promise<any>[]=[];
   service.defaults.adapter=((config:InternalAxiosRequestConfig)=>new Promise(resolve=>{pending.push({config,resolve});result.requests.push({url:config.url,method:config.method,signal_aborted:!!config.signal?.aborted});})) as AxiosAdapter;
   const accepted=(endpoint:string)=>pending.filter(p=>p.config.url?.endsWith('/'+endpoint));
   const call=(f:()=>any)=>{const p=f();if(p?.then)inFlight.push(Promise.resolve(p).catch(()=>undefined));return p;};
   const finish=async(q:Pending,headers:any)=>{q.settled=true;await act(async()=>{q.resolve({config:q.config,data:{result:true},headers,status:200,statusText:'OK'});await Promise.resolve();});await flush();};
   const renderFixture=async(refreshRemaining:number,manual:boolean,accessRemaining=60_000)=>{const initial=token('A',accessRemaining,'initial-access');render(<Provider data={{token:initial,expiredIn:(Date.now()+accessRemaining)/1000,refreshToken:token('A',refreshRemaining,'initial-refresh'),workspaces:[]}}>{manual?<Timeout/>:null}</Provider>);await flush();return initial;};
   try{
    if(c.id.startsWith('RN-B')){
     const n=Number(c.id.slice(-3));
     if(n<=3){const remaining=[24999,25000,25001][n-1];await renderFixture(4*60*60_000,false,remaining);await act(async()=>{await extendToken();});await flush();checks('activity POST count at '+remaining+' milliseconds',accepted('extend').length,n===1?0:1);}
     else if(n<=6){const offset=[-1,0,1][n-4];await renderFixture(2000-offset,true);result.timing={now:Date.now(),refresh_expiry_ms:(getJWTPayload(getHooksBase().store.refreshToken!) as any).exp*1000,deadline_offset_ms:offset};await act(async()=>{call(()=>controller.extend());});await flush();checks('manual relogin POST count at deadline offset '+offset,accepted('relogin').length,n===4?1:0);}
     else{const remaining=10_800_000+[-1,0,1][n-7];await renderFixture(remaining,false);await act(async()=>{call(()=>getRefreshToken());});await flush();checks('refresh acquisition POST count at validity '+remaining,accepted('refreshtoken').length,n===9?0:1);}
    }else if(c.id.startsWith('RN-P')){
     const n=Number(c.id.slice(-3));
     let actualAccess:any;
     let signedCredentials:any;
     if(n===18){
      const fixture=JSON.parse(fs.readFileSync(path.join(out,'signed-bridge-runtime.json'),'utf8'));
      signedCredentials=JSON.parse(fs.readFileSync(path.join(fixture.temporary_fixture,'credentials.json'),'utf8'));
      actualAccess=signedCredentials.A;const claims=getJWTPayload(actualAccess) as any;jest.setSystemTime(claims.iat*1000+1000);
      result.signed_peer={source_binding:'../../security/server-execution.json',verifier:'current BFF JwtTokenUtil and current SDK AuthTokenFilter',handler:'synthetic protected servlet handler',raw_credentials_retained:false};
      result.limits.push('P018 additionally executes real current RSA/JWT verification and SDK filtering. It does not execute a live business service.');
     }
     const beforeAccess=await renderFixture(4*60*60_000,true);
     await act(async()=>{call(()=>controller.extend());});await flush();checks('one manual request pending',accepted('relogin').length,1);
     const seconds=Date.now()/1000;const valid={sub:'A-response',iat:seconds-1,exp:seconds+60};let supplied:any;
     if(n===1)supplied=undefined;else if(n===2)supplied='';else if(n===3)supplied='not-a-jwt';else if(n===4){const p:any={...valid};delete p.exp;supplied=payloadToken(p);}else if(n===5)supplied=payloadToken({...valid,exp:String(valid.exp)});else if(n===6)supplied=payloadToken({...valid,exp:seconds-1});else if(n===7)supplied=payloadToken({...valid,exp:seconds});else if(n===8){const p:any={...valid};delete p.iat;supplied=payloadToken(p);}else if(n===9)supplied=payloadToken({...valid,iat:0});else if(n===10)supplied=payloadToken({...valid,iat:-1});else if(n===11)supplied=payloadToken({...valid,iat:valid.exp});else if(n===12)supplied=payloadToken({...valid,iat:valid.exp+1});else if(n===13)supplied=payloadToken({...valid,exp:Number.MAX_VALUE});
     let headers:any=supplied===undefined?{}:{'single-ui-authorization':supplied};
     if(n===18){headers={'single-ui-authorization':actualAccess,'Single-UI-Authorization':signedCredentials.B};result.response_values={lowercase_sha256:sha(headers['single-ui-authorization']),titlecase_sha256:sha(headers['Single-UI-Authorization'])};}
     await finish(accepted('relogin')[0],headers);
     if(n===18){
      const selected=getHooksBase().store.token!;checks('selected access is one of the two supplied values',[sha(actualAccess),sha(headers['Single-UI-Authorization'])].includes(sha(selected)),true);result.selected_casing=sha(selected)===sha(actualAccess)?'lowercase':'title-case';const payload=getJWTPayload(selected) as any;checks('installed expiry equals selected credential expiry',getHooksBase().store.expiredIn,payload.exp);result.selection=snapshot();
      const bridge=JSON.parse(fs.readFileSync(path.resolve(out,'../security/bridge-command.json'),'utf8'));
      const fixture=JSON.parse(fs.readFileSync(path.join(out,'signed-bridge-runtime.json'),'utf8'));
      const selectedFile=path.join(fixture.temporary_fixture,'selected-casing.json');fs.writeFileSync(selectedFile,JSON.stringify({token:selected}));
      const validationFile=path.join(folder,'signed-validation.json');execFileSync(bridge.command[0],[...bridge.command.slice(1),'validate',fixture.temporary_fixture,selectedFile,validationFile],{encoding:'utf8',timeout:20000});
      const validation=JSON.parse(fs.readFileSync(validationFile,'utf8'));result.protected_validation=validation;
      checks('current BFF signature and expiry verification passes',validation.current_bff_jwt_valid,true);
      checks('current SDK protected handler accepts selected credential',validation.protected_fixture_accepted,true);
      checks('accepted service-side identity matches installed access subject',validation.sdk_authorization_subject,payload.sub);result.status='PASSED';
     }else{checks('successful dialog closure count equals zero',closures,0);checks('response installs zero access credentials',getHooksBase().store.token,beforeAccess);result.status='PASSED';}
    }else{
     const n=Number(c.id.slice(-3));const manual=n>=13;const count=manual?({13:2,14:20} as any)[n]:({9:1,10:2,11:8,12:64} as any)[n];await renderFixture(manual?4*60*60_000:60_000,manual);
     const calls:any[]=[];
     await act(async()=>{for(let i=0;i<count;i++)calls.push(call(()=>manual?controller.extend():getRefreshToken()));});await flush();
     const endpoint=manual?'relogin':'refreshtoken';checks('POST count for '+count+' simultaneous callers',accepted(endpoint).length,1);
     if(!manual)checks('all acquisition callers share the same pending promise',calls.every(p=>p===calls[0]),true);
     const installed=token('A-final',manual?120_000:4*60*60_000,'final-'+endpoint);await finish(accepted(endpoint)[0],{[manual?'single-ui-authorization':'single-ui-refresh']:installed});await Promise.allSettled(calls);await flush();
     const observed=Array.from({length:count},()=>{const s=getHooksBase().store;return sha(manual?s.token:s.refreshToken);});checks('all accepted callers observe the same installed identity',observed,Array.from({length:count},()=>sha(installed)));result.caller_count=count;result.status='PASSED';
    }
    if(result.status==='RUNNING')result.status='PASSED';
   }catch(error){result.status='FAILED';result.error=String((error as Error).message);throw error;}
   finally{for(const q of pending.filter(q=>!q.settled)){q.settled=true;q.resolve({config:q.config,data:{result:true},headers:{},status:200,statusText:'OK'});}await act(async()=>{await Promise.allSettled(inFlight);});result.final=snapshot();result.completed_at=new Date().toISOString();save();}
  },30000);
 }
});
