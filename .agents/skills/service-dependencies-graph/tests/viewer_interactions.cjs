"use strict";

// Exercise the shipped script with a small DOM substitute. No browser is used.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const html = fs.readFileSync(process.argv[2], "utf8");
const elements = new Map();
const familyInputs = [];
const priorityButtons = [];

class Element {
  constructor(tag, attributes) {
    this.tag = tag;
    this.attributes = attributes;
    this.value = attributes.value || "";
    this.dataset = Object.fromEntries(Object.entries(attributes)
      .filter(([key]) => key.startsWith("data-"))
      .map(([key, value]) => [key.slice(5).replace(/-([a-z])/g, (_, letter) => letter.toUpperCase()), value]));
    this.style = {};
    this.listeners = new Map();
    this.checked = "checked" in attributes;
    this.disabled = "disabled" in attributes;
    this.hidden = "hidden" in attributes;
    this.innerHTML = "";
    this.textContent = "";
  }
  setAttribute(name, value) { this.attributes[name] = value; }
  addEventListener(name, listener) { this.listeners.set(name, listener); }
  closest(selector) {
    if (selector === "label") return {style: {}};
    if (selector === "[data-level]" && this.dataset.level) return this;
    if (selector === "[data-edge]" && this.dataset.edge) return this;
    if (selector === "[data-node]" && this.dataset.node) return this;
    if (selector === "[data-boundary-status]" && this.dataset.boundaryStatus) return this;
    if (selector === "[data-trace]" && this.dataset.trace) return this;
    if (selector === "[data-repo-view]" && this.dataset.repoView) return this;
    return null;
  }
  fire(name, target = this) {
    assert(this.listeners.has(name), `${this.attributes.id || this.tag} lacks ${name} handler`);
    this.listeners.get(name)({target});
  }
}

for (const match of html.matchAll(/<([a-z][\w-]*)\b([^>]*)>/gi)) {
  const attributes = {};
  for (const item of match[2].matchAll(/([\w-]+)(?:="([^"]*)")?/g)) attributes[item[1]] = item[2] || "";
  const element = new Element(match[1].toLowerCase(), attributes);
  if (attributes.id) elements.set(attributes.id, element);
  if (element.tag === "input" && attributes.name === "family") familyInputs.push(element);
  if (element.tag === "button" && attributes["data-level"]) priorityButtons.push(element);
}
for (const match of html.matchAll(/<select\b[^>]*id="([^"]+)"[^>]*>([\s\S]*?)<\/select>/g)) {
  const option = match[2].match(/<option\b[^>]*value="([^"]*)"/);
  if (option) elements.get(match[1]).value = option[1];
}
const scripts = [...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/g)];
for (const match of scripts) {
  const id = match[1].match(/\bid="([^"]+)"/);
  if (id) elements.get(id[1]).textContent = match[2];
}
const document = {
  listeners: new Map(),
  getElementById(id) {
    assert(elements.has(id), `Missing DOM element ${id}`);
    return elements.get(id);
  },
  querySelectorAll(selector) {
    if (selector === "#priority button") return priorityButtons;
    if (selector === 'input[name="family"]') return familyInputs;
    if (selector === 'input[name="family"]:checked') return familyInputs.filter(input => input.checked);
    throw new Error(`Unsupported DOM selector ${selector}`);
  },
  addEventListener(name, listener) { this.listeners.set(name, listener); },
};
const context = vm.createContext({document, console});
const script = scripts.find(match => !/\btype="application\/json"/.test(match[1]));
assert(script, "The viewer must ship an executable script");
vm.runInContext(script[2], context, {timeout: 5000});
const evaluate = expression => JSON.parse(vm.runInContext(`JSON.stringify(${expression})`, context));
const matches = () => evaluate("matching");
const set = (id, value, event = "change") => {
  const element = elements.get(id); element.value = value; element.fire(event);
};
const level = value => elements.get("priority").fire("click", priorityButtons.find(button => button.dataset.level === value));

if (process.argv[3] === "user-context") {
  assert.equal(elements.get("architecture-context").hidden, false);
  assert.equal([...elements.get("context-layers").innerHTML.matchAll(/class="context-layer"/g)].length, 4);
  assert.match(elements.get("context-layers").innerHTML, /Root/);
  assert.match(elements.get("context-layers").innerHTML, /Shell/);
  assert.match(elements.get("context-relationships").innerHTML, /Portal shell → Remote tile/);
  assert.match(elements.get("context-relationships").innerHTML, /USER_REPORTED/);
  assert.match(elements.get("context-layers").innerHTML, /OUT_OF_SCOPE/);
  assert.match(elements.get("context-layers").innerHTML, /&lt;script&gt;unsafe\(\)&lt;\/script&gt;/);
  assert.match(elements.get("context-sources").innerHTML, /SHA-256/);
  const canonicalBefore = evaluate("matching");
  // Given a distinct layer label, when search selects it, then its subjects and adjacent links remain visible.
  vm.runInContext("architectureContext.document.layers.find(row=>row.id==='layer:shell').label='Presentation tier'", context);
  set("context-search", "presentation tier", "input");
  assert.match(elements.get("context-layers").innerHTML, /Portal shell/);
  assert.match(elements.get("context-relationships").innerHTML, /Portal shell → Remote tile/);
  assert.deepEqual(evaluate("matching"), canonicalBefore);
  set("context-search", "no-supplied-subject-matches", "input");
  assert.match(elements.get("context-relationships").innerHTML, /No supplied relationships/);
  assert.deepEqual(evaluate("matching"), canonicalBefore);
  set("context-search", "", "input");
  set("context-repository", "unbound");
  assert.match(elements.get("context-relationships").innerHTML, /LOADS_REMOTE_UI/);
  assert.match(elements.get("context-counts").textContent, /Adjacent subjects remain visible/);
  assert.deepEqual(evaluate("matching"), canonicalBefore);
  console.log("User architecture context hierarchy, escaping, filters, and canonical isolation passed.");
  process.exit(0);
}

if (process.argv[3] === "architecture") {
  assert.equal(elements.get("repository-overview").hidden, false);
  assert.match(elements.get("repository-overview").innerHTML, /Provided APIs/);
  assert.match(elements.get("repository-overview").innerHTML, /Config keys/);
  assert.match(elements.get("repository-overview").innerHTML, /unmatched \/ ambiguous boundaries/);
  document.listeners.get("click")({target:new Element("button", {"data-repo-view":"configuration","data-repo":"repo:orders"})});
  assert.equal(elements.get("scope").value, "repo:orders");
  assert.equal(elements.get("repository-view").value, "configuration");
  const expected = "orders.integration.authentication.client.connection.timeout.milliseconds";
  assert.equal(evaluate(`wrapLabel(${JSON.stringify(expected)}).join('')`), expected);
  assert.match(elements.get("diagram").innerHTML, /<tspan/);
  assert(!elements.get("diagram").innerHTML.includes("…"));
  assert.match(elements.get("diagram").innerHTML, /CONFIGURATION/);
  assert.match(elements.get("diagram").innerHTML, /HANDLERS \/ CONTROLLERS/);
  assert.equal([...elements.get("diagram").innerHTML.matchAll(/class="wire"/g)].length,
               [...elements.get("diagram").innerHTML.matchAll(/text-anchor="middle"/g)].length,
               "Every rendered relationship must retain its visible label above twelve edges");
  assert(matches().length > 12);
  document.listeners.get("click")({target:new Element("button", {"data-trace":"operation:orders:get"})});
  assert.equal(evaluate("traceAnchor"), "operation:orders:get");
  assert(matches().some(edge=>edge.id==="edge:fixture:invoke"));
  assert(matches().some(edge=>edge.id==="edge:fixture:call"));
  assert(matches().some(edge=>edge.id==="edge:fixture:config:0"));
  assert(!matches().some(edge=>edge.relationship==='INJECTS'),"Focused traces omit type/injection context by default");
  assert(evaluate("graphProjection().nodes.some(node=>node.id==='operation:orders:get')"),"The trace begins with its API anchor");
  assert.match(elements.get("trace-summary").innerHTML, /Type dependencies and mappings do not establish executed calls/);
  assert.match(elements.get("diagram").innerHTML, /method path/);
  assert.match(elements.get("diagram").innerHTML, /getOrder\(\)/,"Handler method names remain visible in trace cards");
  assert.match(elements.get("diagram").innerHTML, /load\(\)/,"Selected target method names remain visible in trace cards");
  assert.match(elements.get("trace-summary").innerHTML, /visible \/ .* retained/);
  elements.get("trace-context").checked=true;elements.get("trace-context").fire("change");
  assert.deepEqual(new Set(matches().map(edge=>edge.id)),new Set(evaluate("V.traces[traceAnchor].edge_ids")));
  assert.match(elements.get("diagram").innerHTML, /IMPLEMENTATION \/ FUNCTIONS/);
  assert.match(elements.get("diagram").innerHTML, /HANDLERS \/ CONTROLLERS/);
  elements.get("clear-trace").fire("click");
  assert.equal(evaluate("traceAnchor"), null);
  set("repository-view", "components");
  const wirePaths=[...elements.get("diagram").innerHTML.matchAll(/class="wire" d="([^"]+)"/g)].map(match=>match[1]);
  assert.equal(new Set(wirePaths).size, wirePaths.length,"Separate same-lane relationships need separate routes");
  console.log(JSON.stringify({checks:["architecture_inventory","inventory_drilldown","complete_multiline_labels",
    "semantic_lanes","all_edge_labels","api_dependency_trace","same_lane_routes"]}));
  process.exit(0);
}

if (process.argv[3] === "recovery") {
  assert.equal(elements.get("boundary-summary").hidden, false);
  assert.match(elements.get("boundary-summary").innerHTML, /Unresolved/);
  level("medium");
  set("scope", "repo:orders");
  const expectedEdges = new Set(matches().map(edge => edge.id));
  const expectedNodes = new Set(evaluate("matchingNodes.map(node=>node.id)"));
  assert(expectedNodes.has("component:orders:isolated"), "Owned isolated nodes must remain indexed");
  const diagramEdges = new Set(), diagramNodes = new Set();
  let diagramPages = 0;
  for (;;) {
    const projection = evaluate("graphProjection()");
    assert(projection.nodes.length <= 36);
    assert(projection.edges.length <= 48);
    for (const edge of projection.edges) diagramEdges.add(edge.id);
    for (const node of projection.nodes) diagramNodes.add(node.id);
    diagramPages++;
    if (elements.get("graph-next").disabled) break;
    assert(diagramPages < 100, "Diagram pagination must finish");
    elements.get("graph-next").fire("click");
  }
  assert(diagramPages > 1);
  assert.deepEqual(diagramEdges, expectedEdges, "Every indexed edge must appear on a diagram page");
  assert.deepEqual(diagramNodes, expectedNodes, "Every indexed node must appear on a diagram page");

  elements.get("node-view").fire("click");
  const listedNodes = new Set();
  for (;;) {
    for (const match of elements.get("node-rows").innerHTML.matchAll(/data-node="([^"]+)"/g)) listedNodes.add(match[1]);
    if (elements.get("node-next").disabled) break;
    elements.get("node-next").fire("click");
  }
  assert.deepEqual(listedNodes, expectedNodes, "The node index must retain all pages");

  assert(!evaluate("matchingNodes.some(node=>node.repository==='repo:testing')"));
  set('scope', 'all');
  set('dependency-scope', 'all');
  assert(evaluate("matchingNodes.some(node=>node.repository==='repo:testing')"));
  assert(matches().some(edge=>edge.id==='edge:testing:http'));
  set('dependency-scope', 'PRODUCTION');
  assert(!matches().some(edge=>edge.dependency_scope==='TESTING'));
  set('scope', 'repo:testing');
  assert.equal(elements.get('dependency-scope').value, 'TESTING');
  assert(matches().every(edge=>edge.dependency_scope==='TESTING'));
  assert(matches().some(edge=>edge.id==='edge:testing:resource'&&edge.family==='shared'));
  assert.match(elements.get('relationship-rows').innerHTML, /TESTING/);
  assert.equal(evaluate("V.repository_roots['repo:testing']"), 'component:testing:root');
  document.listeners.get("click")({target:new Element("button", {"data-trace":"component:testing:root"})});
  assert.equal(elements.get('dependency-scope').value,'TESTING');
  assert(matches().some(edge=>edge.id==='edge:testing:http'),"A testing trace retains testing scope");
  set('scope', 'repo:orders');
  assert.equal(elements.get('dependency-scope').value, 'PRODUCTION');

  set("repository-view", "storage");
  const storageTables = evaluate("matchingNodes.filter(node=>node.type==='TABLE').length");
  const storageReads = matches().filter(edge=>edge.relationship === "READS").length;
  assert.equal(storageTables, 7);
  assert.equal(storageReads, 8);
  assert(evaluate("matchingNodes.some(node=>node.type==='COLUMN')"));
  set("repository-view", "configuration");
  assert.deepEqual(matches().map(edge=>edge.id), ["edge:config"]);
  set("repository-view", "messages");
  assert.deepEqual(matches().map(edge=>edge.id), ["edge:publish"]);
  set("repository-view", "provided");
  assert(matches().every(edge=>["EXPOSES","INVOKES"].includes(edge.relationship)));
  assert(matches().length > 100);
  set("repository-view", "outbound");
  assert(matches().every(edge=>!["EXPOSES","INVOKES"].includes(edge.relationship)));
  assert(matches().every(edge=>evaluate(`byId.get(${JSON.stringify(edge.source)}).repository`) === "repo:orders"));
  set("repository-view", "components");
  assert(matches().some(edge=>edge.id === "edge:class"));
  assert.equal(matches().find(edge=>edge.id === "edge:class").assertion_status, "INFERRED");
  set("dimension", "BUSINESS");
  assert.deepEqual(matches().map(edge=>edge.id), ["edge:business"]);
  set("dimension", "RUNTIME");
  assert(!matches().some(edge=>edge.id === "edge:business"));

  set("repository-view", "all");
  set("search", "IsolatedOrdersUtility", "input");
  assert.equal(matches().length, 0);
  assert.deepEqual(evaluate("matchingNodes.map(node=>node.id)"), ["component:orders:isolated"]);
  document.listeners.get("click")({target: new Element("button", {"data-node": "component:orders:isolated"})});
  assert.equal(elements.get("graph-panel").hidden, false);
  assert.deepEqual(evaluate("graphProjection().nodes.map(node=>node.id)"), ["component:orders:isolated"]);
  assert.match(elements.get("detail").innerHTML, /0 selected relationships/);
  set("search", "", "input");
  document.listeners.get("click")({target: new Element("button", {"data-node": "component:orders:handler"})});
  assert.match(elements.get("detail").innerHTML, /CONTROLLER/);
  assert.match(elements.get("detail").innerHTML, /Handles order creation/);
  assert.match(elements.get("detail").innerHTML, /OrdersHandler.java/);
  assert.match(elements.get("detail").innerHTML, /entrypoint/);
  assert.match(elements.get("detail").innerHTML, /\[redacted\]/);
  assert(!elements.get("detail").innerHTML.includes("fixture-secret"));
  document.listeners.get("click")({target: new Element("button", {"data-node": "config:orders"})});
  assert(!elements.get("detail").innerHTML.includes("fixture-value"));
  console.log(JSON.stringify({checks:["complete_diagram_pages","complete_node_index","storage_recovery",
    "repository_slices","business_dimension","isolated_focus","full_safe_inspector","boundary_summary"],
    diagram_pages:diagramPages,storage_tables:storageTables,storage_reads:storageReads}));
  process.exit(0);
}

const initial = matches();
assert(initial.length > 0);
assert(initial.every(edge => edge.level === "highest" && edge.status === "resolved" && edge.family !== "package"));
assert.equal(initial.length, evaluate("V.system_links.filter(edge => edge.level === 'highest').length"));
assert.match(elements.get("diagram").innerHTML, /marker-end="url\(#arrow-/);
assert.match(elements.get("diagram").innerHTML, /API calls/);
assert.match(elements.get("diagram").innerHTML, /Imports shared module/);

level("medium");
set("status", "unresolved");
set("search", "GraphQL", "input");
assert.deepEqual(matches().map(edge => edge.id), ["edge:graphql:external"]);
const unresolved = new Element("button", {"data-edge": "edge:graphql:external"});
document.listeners.get("click")({target: unresolved});
assert.match(elements.get("detail").innerHTML, /does not mean broken/i);
assert.match(elements.get("detail").innerHTML, /UNRESOLVED/);

level("medium");
const mediumCount = matches().length;
set("scope", "repo:base");
assert.deepEqual(matches().map(edge => edge.id), ["edge:module"]);
assert(matches().length < mediumCount);
set("boundary", "external");
assert.equal(matches().length, 0);
set("scope", "all");
assert(matches().length > 0);
assert(matches().every(edge => !evaluate(`byId.get(${JSON.stringify(edge.target)}).repository`)));
level("medium");
for (const input of familyInputs) { input.checked = input.value === "data"; }
familyInputs[0].fire("change");
assert.deepEqual(matches().map(edge => edge.id), ["edge:reads"]);

level("low");
assert(matches().length > 25);
assert(matches().every(edge => edge.family === "package" && edge.relationship === "DEPENDS_ON_PACKAGE"));
const expected = new Set(matches().map(edge => edge.id));
elements.get("list-view").fire("click");
assert.equal(elements.get("list-panel").hidden, false);
assert.equal(elements.get("graph-panel").hidden, true);
const listed = [];
let pages = 0;
for (;;) {
  listed.push(...[...elements.get("relationship-rows").innerHTML.matchAll(/data-edge="([^"]+)"/g)].map(match => match[1]));
  pages++;
  if (elements.get("next").disabled) break;
  assert(pages < 10, "Pagination must finish");
  elements.get("next").fire("click");
}
assert(pages > 1);
assert.equal(listed.length, expected.size);
assert.deepEqual(new Set(listed), expected);
assert.match(elements.get("page-label").textContent, new RegExp(`of ${expected.size}$`));
console.log(JSON.stringify({checks: ["default_priority", "directed_labels", "unresolved_search", "repository_filter",
  "boundary_filter", "family_filter", "build_separation", "complete_pagination"], pages, package_relationships: listed.length}));
