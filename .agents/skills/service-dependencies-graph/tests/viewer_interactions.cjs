'use strict';
// Run the actual lazy viewer in a minimal DOM; browser layout is verified separately.
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const {Blob}=require('node:buffer');
const file=process.argv[2],mode=process.argv[3]||'progressive',html=fs.readFileSync(file,'utf8');
const elements=new Map(),requests=new Map();let failNext=false;
class Element{
 constructor(tag,attributes={}){this.tag=tag;this.attributes=attributes;this.dataset=Object.fromEntries(Object.entries(attributes).filter(([key])=>key.startsWith('data-')).map(([key,value])=>[key.slice(5).replace(/-([a-z])/g,(_,x)=>x.toUpperCase()),value]));this.value=attributes.value||'';this.style={};this.listeners=new Map();this.hidden='hidden'in attributes;this.open='open'in attributes;this._html='';this.textContent='';}
 set innerHTML(value){this._html=value;parseElements(value);if(this.tag==='select'){const match=value.match(/<option[^>]*value="([^"]*)"/);if(match)this.value=match[1];}}
 get innerHTML(){return this._html;}
 setAttribute(key,value){this.attributes[key]=value;}
 addEventListener(event,fn){if(!this.listeners.has(event))this.listeners.set(event,[]);this.listeners.get(event).push(fn);}
 closest(selector){if(selector.includes(','))return selector.split(',').map(x=>this.closest(x.trim())).find(Boolean)||null;if(selector.startsWith('#'))return this.attributes.id===selector.slice(1)?this:null;const match=selector.match(/^\[data-([\w-]+)\]$/);if(match)return ('data-'+match[1])in this.attributes?this:null;return null;}
 remove(){}
 getBoundingClientRect(){return {width:1100,height:650,left:0,top:0};}
 setPointerCapture(){}
 matches(){return false;}
 async fire(event){for(const fn of this.listeners.get(event)||[])await fn({target:this});if(this['on'+event])await this['on'+event]({target:this});}
}
function parseElements(source){for(const match of source.matchAll(/<([a-z][\w-]*)\b([^>]*)>/gi)){const attrs={};for(const row of match[2].matchAll(/([\w-]+)(?:="([^"]*)")?/g))attrs[row[1]]=row[2]||'';if(attrs.id)elements.set(attrs.id,new Element(match[1],attrs));}}
parseElements(html);
for(const match of html.matchAll(/<select\b[^>]*id="([^"]+)"[^>]*>([\s\S]*?)<\/select>/g)){elements.get(match[1])._html=match[2];const option=match[2].match(/<option[^>]*value="([^"]*)"/);if(option)elements.get(match[1]).value=option[1];}
const scripts=[...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/g)];
for(const match of scripts){const id=match[1].match(/id="([^"]+)"/);if(id)elements.get(id[1]).textContent=match[2];}
let context;
const document={listeners:new Map(),getElementById(id){assert(elements.has(id),'Missing element '+id);return elements.get(id);},createElement(tag){return new Element(tag);},addEventListener(event,fn){this.listeners.set(event,fn);},head:{appendChild(script){const key=path.basename(script.src,'.js');requests.set(key,(requests.get(key)||0)+1);if(failNext){failNext=false;queueMicrotask(()=>script.onerror());return;}queueMicrotask(()=>{try{vm.runInContext(fs.readFileSync(path.join(path.dirname(file),script.src),'utf8'),context);}catch(error){console.error(error);script.onerror();}});}}};
context=vm.createContext({document,console,setTimeout,clearTimeout,Uint8Array,Blob,Response,DecompressionStream,atob});context.window=context;
const script=scripts.find(match=>!match[1].includes('application/json'))[2];
const value=expression=>vm.runInContext(expression,context);
const json=expression=>JSON.parse(value('JSON.stringify('+expression+')'));
async function main(){
 if(mode==='template-error'){assert.throws(()=>value(script),/Invalid graph data/);assert.equal(elements.get('error').hidden,false);assert.equal(elements.get('main').hidden,true);console.log(JSON.stringify({visible_recovery:true}));return;}
 value(script);await value('Promise.resolve()');
 assert.equal(requests.size,0,'Initial overview must not load canonical data or traces');
 const roots=json('[...rootIds]'),root=roots.find(id=>id.includes('client'))||roots[0];
 if(mode==='user-context'){
  assert.equal(elements.get('context-panel').hidden,false);await value('renderContext()');
  assert.match(elements.get('context-content').innerHTML,/Root|Shell/);
  assert.match(elements.get('context-content').innerHTML,/unsafe|SHA-256/);
  console.log(JSON.stringify({context:true}));return;
 }
 if(mode==='recovery'){
  failNext=true;await assert.rejects(value('expand('+JSON.stringify(root)+')'),/Could not load/);
  assert(!value('expanded.has('+JSON.stringify(root)+')'));assert.equal(value('pending.size'),0);
  await value('expand('+JSON.stringify(root)+')');assert(value('expanded.has('+JSON.stringify(root)+')'));
  console.log(JSON.stringify({retry_succeeded:true,loading_cleared:elements.get('loading').hidden}));return;
 }
 await value('Promise.all([expand('+JSON.stringify(root)+'),expand('+JSON.stringify(root)+')])');
 assert([...requests.values()].every(count=>count===1));
 if(mode==='complete'||mode==='inspection'){
  let queue=[...roots],seen=new Set(),batches=0;
  while(queue.length){const id=queue.shift();if(seen.has(id))continue;seen.add(id);await value('expand('+JSON.stringify(id)+')');const pages=value('nodes.get('+JSON.stringify(id)+').pages');for(let i=1;i<pages;i++){await value('loadPage('+JSON.stringify(id)+')');batches++;}for(const child of json('branches.get('+JSON.stringify(id)+')?[...branches.get('+JSON.stringify(id)+').nodes]:[]'))if(!seen.has(child))queue.push(child);}
  if(mode==='complete'){
   const counts=json('({canonical_nodes:[...nodes.values()].filter(node=>!node.id.startsWith("viewer-")).length,canonical_edges:[...edges.values()].filter(edge=>!edge.navigation).length})');
   console.log(JSON.stringify({...counts,batches}));return;
  }
  elements.get('status').value='unresolved';
  assert(json('projection().edges.filter(edge=>!edge.navigation).map(edge=>edge.status)').every(status=>status==='unresolved'));
  await value("selectItem('edge','edge:external')");
  await value("showRecord(edges.get('edge:external'),document.getElementById('record-content'),selectionVersion)");
  const detail=elements.get('record-content').innerHTML;assert.match(detail,/Source evidence/);assert.match(detail,/fixture.txt/);assert(!detail.includes('DO_NOT_DISPLAY'));assert.match(detail,/redacted/);
  const navigation=json('[...edges.values()].find(edge=>edge.navigation).id');
  await value('selectItem("edge",'+JSON.stringify(navigation)+')');
  assert.match(elements.get('selection').innerHTML,/no canonical relationship or runtime call/);
  console.log(JSON.stringify({unresolved_preserved:true,source_evidence:true,redacted:true}));return;
 }
 const group=json('[...nodes.values()].find(node=>node.type==="DEPENDENCY_GROUP"&&node.parent==='+JSON.stringify(root)+')');assert(group);
 await value('expand('+JSON.stringify(group.id)+','+JSON.stringify(root)+')');
 assert(json('projection().nodes.map(node=>node.id)').length>roots.length);
 for(const id of roots)assert(json('projection().nodes.map(node=>node.id)').includes(id));
 const viewBefore=elements.get('graph').attributes.viewBox;
 value('collapse('+JSON.stringify(root)+')');
 assert.equal(json('projection().nodes.map(node=>node.id)').length,roots.length);
 assert.equal(elements.get('graph').attributes.viewBox,viewBefore,'Collapse preserves the viewport');
 console.log(JSON.stringify({same_graph:true,all_roots_retained:true,collapsed:true,deduplicated_requests:true}));
}
main().catch(error=>{console.error(error);process.exitCode=1;});
