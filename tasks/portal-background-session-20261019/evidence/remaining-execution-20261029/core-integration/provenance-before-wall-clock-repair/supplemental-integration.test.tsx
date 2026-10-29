import React from 'react';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {Buffer} from 'buffer';
import {AxiosAdapter,AxiosError,AxiosResponse,InternalAxiosRequestConfig} from 'axios';
import {act,cleanup,render} from '@testing-library/react';
import Provider from '../hooks/provider';
import {getHooksBase} from '../hooks/HooksBase';
import service from '../hooks/service/config';
import {getRefreshToken,getPendingRefreshToken,relogin,signal} from '../hooks/service';
import {signal as activitySignal} from '../hooks/service/util/extend';
import useTimeout from '../components/Timeout/common/useController';
import useServices from '../services';
import {currentSessionEpoch} from '../utils/sessionEpoch';
import {getJWTPayload} from '../utils/common';

jest.mock('../analytics',()=>()=>({ButtonEvent:jest.fn(),TileEvent:jest.fn(),TabEvent:jest.fn(),ModalEvent:jest.fn()}));
const out=process.env.CORE_INTEGRATION_OUTPUT!;
const all=JSON.parse(fs.readFileSync(process.env.CORE_INTEGRATION_DEFINITIONS!,'utf8'));
const ids=[...Array.from({length:6},(_,i)=>'RN-R'+String(i+15).padStart(3,'0')),'RN-M007','RN-M010'];
const cases=all.filter((c:any)=>ids.includes(c.id));
const now=Date.parse('2026-10-29T02:00:00Z');
const sha=(s:any)=>crypto.createHash('sha256').update(typeof s==='string'?s:JSON.stringify(s)).digest('hex');
const token=(sub:string,remaining:number,id='fixture')=>'Bearer e30.'+Buffer.from(JSON.stringify({sub,jti:id,iat:Math.floor(Date.now()/1000)-1,exp:(Date.now()+remaining)/1000})).toString('base64')+'.synthetic';
let controller:any,services:any,closures:number;
const Timeout=()=>{controller=useTimeout({setOpen:(open:boolean)=>{if(!open)closures++;}} as any);return null;};
const Fixture=({show}:{show:boolean})=>{services=useServices();return show?<Timeout/>:null;};
const originalAdapter=service.defaults.adapter;
const state=()=>{const s=getHooksBase().store;return {access:s.token,refresh:s.refreshToken,expiry:s.expiredIn,iat:s.iat,user:s.user,error:s.errorMsg,logout:s.isOnLogout};};
const safe=()=>{const s=state();return{subject:s.access?(getJWTPayload(s.access) as any).sub:null,access_sha256:s.access?sha(s.access):null,refresh_sha256:s.refresh?sha(s.refresh):null,expiry:s.expiry,iat:s.iat,logout:s.logout,error:s.error,closures,epoch:currentSessionEpoch()};};
const flush=async()=>{await act(async()=>{await Promise.resolve();await Promise.resolve();});};
interface Pending{config:InternalAxiosRequestConfig;resolve:(v:AxiosResponse)=>void;reject:(e:any)=>void;settled?:boolean;}

describe('Exact remaining hook ownership and ordering predicates',()=>{
 beforeEach(()=>{jest.useFakeTimers();jest.setSystemTime(now);localStorage.clear();sessionStorage.clear();controller=undefined;services=undefined;closures=0;});
 afterEach(()=>{signal.getRefreshToken?.abort();signal.relogin?.abort();activitySignal.extendToken?.abort();signal.getRefreshToken=undefined;signal.relogin=undefined;activitySignal.extendToken=undefined;cleanup();service.defaults.adapter=originalAdapter;jest.clearAllTimers();jest.useRealTimers();localStorage.clear();sessionStorage.clear();});
 for(const c of cases){it(c.id+' '+c.title,async()=>{
  const folder=path.join(out,c.id);fs.mkdirSync(folder,{recursive:true});
  const result:any={case_id:c.id,definition:'../../../../06-test-cases.md#'+c.id.toLowerCase(),revision:'66c6411ade58e4d134e381c2baee8ad3f76a8dbf',status:'RUNNING',started_at:new Date().toISOString(),given:c.given,when:c.when,then:c.then,policy_open:c.basis==='policy-open',execution_level:'Actual React/source integration in jsdom',assertions:[],requests:[],orders:[],source_binding:'../source-binding.json',limits:['Actual React Provider, mounted Timeout hook, reducers, services, and Axios interceptors execute.','Synthetic credentials, controlled adapter, and fake clock isolate the declared predicates.','No native browser, real network, live protected business service, or production environment executes.','Passing observational cases do not approve unresolved policy.']};
  const save=()=>fs.writeFileSync(path.join(folder,'result.json'),JSON.stringify(result,null,2)+'\n');save();
  const check=(name:string,actual:any,expected:any)=>{const ok=JSON.stringify(actual)===JSON.stringify(expected);result.assertions.push({name,actual,expected,status:ok?'PASSED':'FAILED'});expect(actual).toEqual(expected);};
  let pending:Pending[]=[];let calls:Promise<any>[]=[];let view:any;
  const adapter:AxiosAdapter=config=>new Promise((resolve,reject)=>{const q={config,resolve,reject} as Pending;pending.push(q);result.requests.push({url:config.url,method:config.method,epoch:(config as any).sessionEpoch,at:Date.now()});if(config.url?.endsWith('/logout')||config.url?.endsWith('/imeta/logout')){q.settled=true;resolve({config,data:{result:true},headers:{},status:200,statusText:'OK'});}});
  service.defaults.adapter=adapter;
  const launch=(f:()=>any)=>{const p=f();if(p?.then)calls.push(Promise.resolve(p).catch(()=>undefined));return p;};
  const req=(name:string)=>pending.filter(p=>!p.settled&&p.config.url?.endsWith('/'+name));
  const deliver=(q:Pending,headers:any={},failure=false)=>{q.settled=true;if(failure)q.reject(new AxiosError('Request failed with status code 401','ERR_BAD_REQUEST',q.config,undefined,{config:q.config,data:{errorMessage:'TOKEN_INVALID_EXPIRED'},headers:{},status:401,statusText:'Unauthorized'}));else q.resolve({config:q.config,data:{result:true},headers,status:200,statusText:'OK'});};
  const finish=async(q:Pending,headers:any={},failure=false)=>{await act(async()=>{deliver(q,headers,failure);await Promise.resolve();});await flush();};
  const mount=async(show=false,refresh:any=token('A',60_000,'initial-refresh'))=>{view=render(<Provider data={{token:token('A',60_000,'initial-access'),expiredIn:(Date.now()+60_000)/1000,refreshToken:refresh,workspaces:[]}}><Fixture show={show}/></Provider>);await flush();};
  const toggle=async(show:boolean)=>{view.rerender(<Provider><Fixture show={show}/></Provider>);await flush();};
  const reset=async()=>{for(const q of pending.filter(x=>!x.settled))deliver(q);await act(async()=>{await Promise.allSettled(calls);});cleanup();pending=[];calls=[];closures=0;jest.clearAllTimers();jest.setSystemTime(now);};
  try{
   if(['RN-R015','RN-R016','RN-R017'].includes(c.id)){
    await mount();let oldPromise:any,newPromise:any;await act(async()=>{oldPromise=launch(()=>getRefreshToken());});await flush();const old=req('refreshtoken')[0];check('old acquisition pending',!!old,true);
    if(c.id==='RN-R017'){
     await act(async()=>{launch(()=>services.login({code:'B'}));});await finish(req('login')[0],{'single-ui-authorization':token('B',120_000,'login-B')});
    }else{
     await act(async()=>{launch(()=>service.post('/api/auth/v2/sso/extend',{}));});await finish(req('extend')[0],{'single-ui-authorization':token('A',120_000,'rotated-access')});
    }
    const currentAccess=getHooksBase().store.token;await act(async()=>{newPromise=launch(()=>getRefreshToken());});await flush();const newer=req('refreshtoken').filter(p=>p!==old).slice(-1)[0];check('new acquisition accepted',!!newer,true);
    check('old request signal is aborted',old.config.signal?.aborted,true);
    check('new request owns current access',JSON.parse(newer.config.data as string).singleUIAuthorization,currentAccess);
    if(c.id==='RN-R015')check('new request signal remains active',newer.config.signal?.aborted,false);
    else if(c.id==='RN-R016'){
     await finish(old,{'single-ui-refresh':token('A',4*60*60_000,'obsolete')});await oldPromise;
     check('pending pointer remains the exact new promise',getPendingRefreshToken()===newPromise,true);
     check('public pending pointer does not identify old promise',getPendingRefreshToken()===oldPromise,false);
    }else{
     check('the two requests carry different epochs',(old.config as any).sessionEpoch!==(newer.config as any).sessionEpoch,true);
     const currentRefresh=token('B',4*60*60_000,'current');await finish(newer,{'single-ui-refresh':currentRefresh});const afterCurrent=state();await finish(old,{'single-ui-refresh':token('A',4*60*60_000,'obsolete')});
     check('reverse old response changes zero current authentication fields',state(),afterCurrent);check('only current epoch refresh is installed',getHooksBase().store.refreshToken,currentRefresh);
    }
   }else if(c.id==='RN-R018'){
    for(const order of ['response-first','timer-first']){
     const requestStart=result.requests.length;await mount(false,token('A',7000,'deadline-refresh'));await act(async()=>{launch(()=>relogin());});await flush();const held=req('relogin')[0];const at=now+5000;let responseFired=false;
     const callback=()=>{responseFired=true;deliver(held,{'single-ui-authorization':token('A',120_000,'due-response')});};
     if(order==='response-first')setTimeout(callback,5000);await toggle(true);if(order==='timer-first')setTimeout(callback,5000);
     check(order+' has an actual pending relogin',!!held,true);check(order+' hooks timer is scheduled at the response due time',!!controller.timerPopup.current,true);
     await act(async()=>{await jest.advanceTimersByTimeAsync(5000);});await flush();await act(async()=>{await jest.advanceTimersByTimeAsync(1001);});await flush();
     const row={order,due_at:at,response_fired:responseFired,closure_count:closures,logout_count:result.requests.slice(requestStart).filter((r:any)=>r.url?.endsWith('/sso/logout')&&r.at>=now).length,final_owner:safe().subject,final:safe(),request_count:pending.length};result.orders.push(row);check(order+' response delivered',responseFired,true);check(order+' records closure count',typeof row.closure_count,'number');check(order+' records logout count',typeof row.logout_count,'number');save();await reset();
    }
    check('both deadline delivery orders recorded',result.orders.length,2);
   }else if(c.id==='RN-R019'){
    for(const order of ['protected-first','relogin-first']){
     await mount(false,token('A',4*60*60_000,'initial-refresh'));await act(async()=>{launch(()=>service.get('/api/fixture/protected-read'));launch(()=>relogin());});await flush();const protectedRequest=req('protected-read')[0],renewal=req('relogin')[0];check(order+' both responses pending',!!protectedRequest&&!!renewal,true);
     const updated=token('A',120_000,'renewed');for(const which of order==='protected-first'?['protected','relogin']:['relogin','protected'])await finish(which==='protected'?protectedRequest:renewal,which==='protected'?{}:{'single-ui-authorization':updated});
     const final=safe();check(order+' final owner remains A',final.subject,'A');check(order+' trace records renewed access expiry',final.expiry,(getJWTPayload(updated) as any).exp);result.orders.push({order,at:Date.now(),final});save();await reset();
    }
    check('both protected/relogin response orders recorded',result.orders.length,2);
   }else if(c.id==='RN-R020'){
    await mount(false,token('A',4*60*60_000,'initial-refresh'));await act(async()=>{launch(()=>service.get('/api/fixture/protected-read'));launch(()=>relogin());});await flush();const protectedRequest=req('protected-read')[0];await finish(req('relogin')[0],{'single-ui-authorization':token('A',120_000,'renewed')});const renewed=safe();check('session has renewed access before unauthorized delivery',renewed.subject,'A');await finish(protectedRequest,{},true);const after=safe();result.unauthorized_observation={renewed,after,renewed_session_cleared:!getHooksBase().store.token,same_epoch_request:true,meaning:'Old access request remains in the same session epoch. Its TOKEN_INVALID_EXPIRED failure clears the renewed session in this controlled source flow.'};check('trace records whether old response cleared the renewed session',typeof result.unauthorized_observation.renewed_session_cleared,'boolean');
   }else if(c.id==='RN-M007'){
    await mount(true,token('A',4*60*60_000,'initial-refresh'));await act(async()=>{launch(()=>controller.extend());});await flush();const held=req('relogin')[0];check('manual relogin pending before unmount',!!held,true);await toggle(false);const before=closures;await finish(held,{'single-ui-authorization':token('A',120_000,'after-unmount')});check('later response causes zero unmounted controller closure callbacks',closures-before,0);
   }else if(c.id==='RN-M010'){
    await mount(false,null);await act(async()=>{launch(()=>getRefreshToken());});await flush();const held=req('refreshtoken')[0];check('access-only acquisition is pending before Timeout mounts',!!held,true);check('initial refresh credential is absent',!!getHooksBase().store.refreshToken,false);await toggle(true);check('mounted controller waits for pending acquisition',controller.canExtend,false);const before=state();let settled=false;getPendingRefreshToken()?.then(()=>{settled=true;});await finish(held,{});await flush();result.settlement_observation={promise_settled:settled,refresh_installed:!!getHooksBase().store.refreshToken,access_changed:getHooksBase().store.token!==before.access,successful_renewal_count:closures,can_extend:controller.canExtend};check('promise settlement is observed separately',settled,true);check('settlement without returned access creates zero successful renewal',closures,0);check('settlement installs zero refresh credentials',!!getHooksBase().store.refreshToken,false);check('settlement installs zero new access',getHooksBase().store.token,before.access);
   }
   result.status='PASSED';
  }catch(error){result.status='FAILED';result.error=String((error as Error).message);throw error;}
  finally{for(const q of pending.filter(p=>!p.settled))deliver(q);await act(async()=>{await Promise.allSettled(calls);});result.final=safe();result.completed_at=new Date().toISOString();save();}
 },30000);}
});
