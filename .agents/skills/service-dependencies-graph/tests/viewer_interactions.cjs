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
 if(mode==='scale'){
  const first=json('projection()');assert(first.nodes.length<=13,'Hub expansion must be bounded');
  assert(first.nodes.every(node=>node.display_node));
  await value('loadPage('+JSON.stringify(root)+')');value('draw()');
  const second=json('projection()');assert(second.nodes.length>first.nodes.length);assert(second.nodes.length<=25);
  const coordinates=json('[...positions]');value('draw()');assert.deepEqual(json('[...positions]'),coordinates);
  assert(!second.nodes.some(node=>node.id.startsWith('component:')));
  elements.get('collapse').onclick();assert.equal(json('projection().nodes').length,roots.length);
  console.log(JSON.stringify({bounded_focus:true,more_adds_peers:true,stable_layout:true}));return;
 }
 if(mode==='complete'||mode==='inspection'){
  let batches=0;
  for(const kind of ['nodes','edges']){
   elements.get('index-kind').value=kind;
   const total=value('bootstrap['+JSON.stringify(kind==='nodes'?'node_index':'edge_index')+'].length');
   for(let page=0;page<total;page++){value('indexPage='+page);await value('renderIndex()');batches++;}
  }
  if(mode==='complete'){
   const counts=json('({canonical_nodes:[...nodes.values()].filter(node=>!node.id.startsWith("viewer-")).length,canonical_edges:[...edges.values()].filter(edge=>!edge.service_link).length})');
   assert(json('projection().nodes').every(node=>node.display_node));
   await value("expand('component:client:call')");assert(!value("expanded.has('component:client:call')"));
   console.log(JSON.stringify({...counts,batches,only_service_nodes:true}));return;
  }
  elements.get('status').value='unresolved';
  assert(json('projection().edges.filter(edge=>!edge.navigation).map(edge=>edge.status)').every(status=>status==='unresolved'));
  await value("selectItem('edge','edge:external')");
  await value("showRecord(edges.get('edge:external'),document.getElementById('record-content'),selectionVersion)");
  const detail=elements.get('record-content').innerHTML;assert.match(detail,/Source evidence/);assert.match(detail,/fixture.txt/);assert(!detail.includes('DO_NOT_DISPLAY'));assert.match(detail,/redacted/);
  const link=json('[...edges.values(),...overviewEdges.values()].find(edge=>edge.service_link&&edge.target==="external:orders")');
  await value('selectItem("edge",'+JSON.stringify(link.id)+')');
  await value('declarationRows(edges.get('+JSON.stringify(link.id)+')||overviewEdges.get('+JSON.stringify(link.id)+'))');
  assert.match(elements.get('source-rows').innerHTML,/Calls REST/);
  assert(json('projection().nodes').every(node=>node.display_node));
  console.log(JSON.stringify({unresolved_preserved:true,source_evidence:true,redacted:true}));return;
 }
 assert.equal(value('focusId'),root);
 assert(json('projection().nodes').every(node=>node.display_node));
 assert(json('projection().edges').every(edge=>edge.service_link));
 assert(!value('[...nodes.values()].some(node=>node.type==="DEPENDENCY_GROUP")'));
 elements.get('direction').value='outbound';value('draw()');
 assert(json('projection().edges').every(edge=>edge.source===root));
 elements.get('direction').value='inbound';value('draw()');
 assert(json('projection().edges').every(edge=>edge.target===root));
 elements.get('direction').value='both';
 const viewBefore=elements.get('graph').attributes.viewBox;
 value('collapse('+JSON.stringify(root)+')');
 assert.equal(elements.get('graph').attributes.viewBox,viewBefore,'Collapse preserves the viewport');
 elements.get('collapse').onclick();
 assert.equal(value('focusId'),null);assert.equal(json('projection().nodes.map(node=>node.id)').length,roots.length);
 console.log(JSON.stringify({same_graph:true,focused_connections:true,collapsed:true,deduplicated_requests:true}));
}
main().catch(error=>{console.error(error);process.exitCode=1;});
