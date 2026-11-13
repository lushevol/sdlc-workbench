const claims = evaluate("architectureContext.document.investigations");
assert.equal(claims.length,23);
assert.equal(evaluate("new Set(Object.values(V.nodes).filter(node=>node.architecture_layer).map(node=>node.architecture_layer.id)).size"),4);
set('origin','INVESTIGATED');
const represented=new Set(evaluate("matching.flatMap(edge=>canonical(edge).flatMap(item=>(item.properties?.architecture_claims||[]).map(claim=>claim.claim_id)))"));
assert.equal(represented.size,claims.length);
for(const value of ['SUPPORTED','INFERRED','UNVERIFIED','OUT_OF_SCOPE']){
 set('assessment',value);
 assert(matches().length);
 assert(matches().every(edge=>edge.assessments.includes(value)));
}
set('assessment','SUPPORTED');
const supported=matches()[0];vm.runInContext(`selected={kind:'edge',id:${JSON.stringify(supported.id)}};renderDetail()`,context);
assert.match(elements.get('detail').innerHTML,/Instruction investigation/);
assert.match(elements.get('detail').innerHTML,/SHA-256/);
console.log(JSON.stringify({status:'PASSED',claims:claims.length,checks:['main_graph_claim_reconciliation','four_layer_lanes','investigation_filters','rationale_and_hashed_source_inspector'],visual_review:'NOT_PERFORMED'}));
