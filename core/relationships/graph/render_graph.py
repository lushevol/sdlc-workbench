#!/usr/bin/env python3
"""Render the schema-v2 Service Dependencies Graph as a dependency-free HTML explorer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


HTML = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Service Dependencies Graph</title><style>
:root{color-scheme:dark;--bg:#07111f;--panel:#0e1b2e;--border:#263b56;--text:#e8f0fa;--muted:#8fa3ba}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:14px Inter,ui-sans-serif,system-ui,sans-serif;overflow:hidden}
header{height:64px;display:flex;align-items:center;gap:10px;padding:11px 16px;background:#0a1728;border-bottom:1px solid var(--border)}h1{font-size:16px;margin:0 12px 0 0;white-space:nowrap}
select,input,button{background:#12233a;color:var(--text);border:1px solid #355071;border-radius:8px;padding:9px 11px}input{min-width:240px}button{cursor:pointer}.spacer{flex:1}.metric{color:var(--muted);font-size:12px;white-space:nowrap}
.layout{display:grid;grid-template-columns:minmax(0,1fr) 360px;height:calc(100vh - 64px)}main{position:relative;min-width:0}canvas{width:100%;height:100%;display:block}.hint{position:absolute;left:14px;bottom:12px;color:var(--muted);pointer-events:none}
aside{overflow:auto;background:var(--panel);border-left:1px solid var(--border);padding:18px}h2{font-size:18px;margin:0 0 8px}h3{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:#a8bed8;margin:22px 0 8px}.muted{color:var(--muted);line-height:1.5}.pill{display:inline-block;padding:3px 7px;margin:2px 4px 2px 0;background:#1d3451;border-radius:99px;font-size:11px}.path{padding:7px 0;border-bottom:1px solid #1c3048;word-break:break-all}a{color:#79caff;text-decoration:none}a:hover{text-decoration:underline}.relation{margin:6px 0}.status{color:#f0bd63}
</style></head><body><header><h1>Service Dependencies Graph</h1><select id="scope"></select><select id="dimension"><option value="RUNTIME">Runtime data flow</option><option value="BUSINESS">Business &amp; functional</option></select><input id="search" placeholder="Find page, component, API, table, topic…"><button id="fit">Fit</button><span class="spacer"></span><span class="metric" id="metric"></span></header>
<div class="layout"><main id="stage"><canvas id="canvas"></canvas><div class="hint">Select a node to inspect meaning, evidence, and linked source paths.</div></main><aside id="detail"></aside></div>
<script id="graph-data" type="application/json">__GRAPH__</script><script>
const G=JSON.parse(document.getElementById('graph-data').textContent),byId=new Map(G.nodes.map(n=>[n.id,n])),stage=document.getElementById('stage'),canvas=document.getElementById('canvas'),ctx=canvas.getContext('2d');
const scope=document.getElementById('scope'),dimension=document.getElementById('dimension'),search=document.getElementById('search'),detail=document.getElementById('detail'),metric=document.getElementById('metric');let selected=null,scene={nodes:[],edges:[]};
const visible=G.repositories.filter(r=>r.visible);scope.innerHTML='<option value="SYSTEM">All repositories</option>'+visible.map(r=>`<option value="${esc(r.id)}">${esc(r.name)}</option>`).join('');
function esc(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function external(n){return !n.repository}function color(n){if(external(n))return'#d57ce8';if(n.type==='BUSINESS_CAPABILITY'||n.type==='PAGE')return'#f2b84b';if(['DATABASE','TABLE','MESSAGE_CHANNEL','DATA_PLATFORM'].includes(n.type))return'#6fa8ff';return'#31c7b4'}
function dedupe(edges){const values=new Map;for(const e of edges){const key=`${e.source}|${e.target}|${e.relationship}`;if(!values.has(key))values.set(key,e)}return[...values.values()]}
function build(){const dim=dimension.value,rid=scope.value;if(rid==='SYSTEM'&&dim==='RUNTIME'){const roots=new Map;for(const n of G.nodes)if(['APPLICATION','SERVICE'].includes(n.type))roots.set(n.repository,n);const nodeMap=new Map([...roots.values()].map(n=>[n.id,n])),systemEdges=[];for(const e of G.edges){if(e.dimension!=='RUNTIME')continue;const a=byId.get(e.source),b=byId.get(e.target),sourceRoot=roots.get(a?.repository),targetRoot=roots.get(b?.repository);if(!sourceRoot)continue;if(targetRoot&&targetRoot.id!==sourceRoot.id){nodeMap.set(targetRoot.id,targetRoot);systemEdges.push({...e,source:sourceRoot.id,target:targetRoot.id});continue}if(!targetRoot&&['DATA_PLATFORM','MESSAGE_CHANNEL','REMOTE_APPLICATION','EXTERNAL_SYSTEM'].includes(b?.type)){nodeMap.set(b.id,b);systemEdges.push({...e,source:sourceRoot.id})}if(b?.type==='DATABASE'){nodeMap.set(b.id,b);systemEdges.push({...e,source:sourceRoot.id})}}scene={nodes:[...nodeMap.values()],edges:dedupe(systemEdges)}}else{const owned=new Set(G.nodes.filter(n=>n.dimensions.includes(dim)&&(rid==='SYSTEM'?n.repository&&visible.some(r=>r.id===n.repository):n.repository===rid)).map(n=>n.id));let edges=G.edges.filter(e=>e.dimension===dim&&(owned.has(e.source)||owned.has(e.target)));const ids=new Set(owned);for(const e of edges){ids.add(e.source);ids.add(e.target)}let nodes=[...ids].map(id=>byId.get(id)).filter(Boolean);if(rid==='SYSTEM'){nodes=nodes.filter(n=>['APPLICATION','SERVICE','BUSINESS_CAPABILITY','PAGE'].includes(n.type));const keep=new Set(nodes.map(n=>n.id));edges=edges.filter(e=>keep.has(e.source)&&keep.has(e.target))}scene={nodes,edges}}metric.textContent=`${scene.nodes.length} nodes · ${scene.edges.length} relationships`;layout();draw();show(scene.nodes.find(n=>n.id===selected)||null)}
function layout(){const w=stage.clientWidth,h=stage.clientHeight,cx=w/2,cy=h/2,n=Math.max(scene.nodes.length,1),rings=Math.max(1,Math.ceil(Math.sqrt(n/10))),maxRadius=Math.max(40,Math.min(w,h)/2-48);scene.nodes.forEach((node,i)=>{const ring=Math.min(rings,1+Math.floor(Math.sqrt(i/8))),slots=Math.max(8,ring*12),angle=(i%slots)/slots*Math.PI*2+ring*.31,radius=24+ring*(maxRadius-24)/rings;node.x=cx+Math.cos(angle)*radius;node.y=cy+Math.sin(angle)*radius;node.r=['APPLICATION','SERVICE','BUSINESS_CAPABILITY'].includes(node.type)?11:7})}
function draw(){ctx.clearRect(0,0,stage.clientWidth,stage.clientHeight);const map=new Map(scene.nodes.map(n=>[n.id,n]));for(const e of scene.edges){const a=map.get(e.source),b=map.get(e.target);if(!a||!b)continue;ctx.strokeStyle=e.resolution_status==='UNRESOLVED'?'#805270':'#29425e';ctx.setLineDash(e.resolution_status==='UNRESOLVED'?[4,4]:[]);ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke()}ctx.setLineDash([]);for(const n of scene.nodes){const hit=search.value&&`${n.name} ${n.functional_role} ${n.business_meaning}`.toLowerCase().includes(search.value.toLowerCase());ctx.fillStyle=color(n);ctx.beginPath();ctx.arc(n.x,n.y,n.r,0,Math.PI*2);ctx.fill();if(n.id===selected||hit){ctx.strokeStyle=hit?'#fff1a8':'#fff';ctx.lineWidth=3;ctx.stroke()}const label=scene.nodes.length<80||hit||n.id===selected||['APPLICATION','SERVICE'].includes(n.type)||(dimension.value==='BUSINESS'&&['BUSINESS_CAPABILITY','PAGE'].includes(n.type));if(label){ctx.fillStyle='#dce8f6';ctx.font='10px sans-serif';ctx.fillText(n.name.slice(0,38),n.x+n.r+4,n.y+3)}}}
function link(path){const prefix=path.split('*')[0].replace(/\/$/,'');return __SOURCE_PREFIX__+prefix}function show(n){if(!n){detail.innerHTML=`<h2>${dimension.value==='RUNTIME'?'Runtime data flow':'Business & functional map'}</h2><p class="muted">${dimension.value==='RUNTIME'?'Remote imports, APIs, service calls, PostgreSQL tables, Kafka topics, and external data platforms.':'Pages and service capabilities mapped to domain, UI, state, utility, client, and infrastructure components.'}</p><h3>Selection</h3><p class="muted">Choose a repository or select a node.</p>`;return}const rel=scene.edges.filter(e=>e.source===n.id||e.target===n.id).map(e=>{const other=byId.get(e.source===n.id?e.target:e.source);return `<div class="relation"><span class="pill">${esc(e.relationship)}</span>${esc(other?.name||'Unknown')} ${e.resolution_status?`<span class="status">${esc(e.resolution_status)}</span>`:''}</div>`}).join('');const paths=(n.source_paths||[]).map(p=>`<div class="path"><a href="${esc(link(p))}">${esc(p)}</a></div>`).join('')||'<p class="muted">External node; evidence is listed on calling components.</p>';detail.innerHTML=`<h2>${esc(n.name)}</h2><span class="pill">${esc(n.type)}</span>${n.component_kind?`<span class="pill">${esc(n.component_kind)}</span>`:''}<h3>Functional usage</h3><p>${esc(n.functional_role)}</p><h3>Business meaning</h3><p>${esc(n.business_meaning)}</p><h3>Source paths</h3>${paths}<h3>Relationships</h3>${rel||'<p class="muted">None in this projection.</p>'}`}
canvas.addEventListener('click',event=>{const box=canvas.getBoundingClientRect(),x=event.clientX-box.left,y=event.clientY-box.top;let found=null,best=28;for(const n of scene.nodes){const d=Math.hypot(n.x-x,n.y-y);if(d<best){found=n;best=d}}if(found){selected=found.id;show(found);draw()}});function resize(){const d=devicePixelRatio||1;canvas.width=stage.clientWidth*d;canvas.height=stage.clientHeight*d;ctx.setTransform(d,0,0,d,0,0);build()}scope.onchange=build;dimension.onchange=build;search.oninput=draw;document.getElementById('fit').onclick=build;window.onresize=resize;resize();
</script></body></html>'''


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-prefix", default="../")
    args = parser.parse_args(argv)
    graph = json.loads(args.graph.read_text(encoding="utf-8"))
    if graph.get("schema_version") != "2.0.0":
        raise ValueError("render_graph requires schema version 2.0.0")
    payload = json.dumps(graph, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(HTML.replace("__GRAPH__", payload).replace("__SOURCE_PREFIX__", json.dumps(args.source_prefix)), encoding="utf-8")
    print(json.dumps({"output": str(args.output.resolve()), "nodes": len(graph["nodes"]), "edges": len(graph["edges"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
