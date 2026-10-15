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
      .map(([key, value]) => [key.slice(5), value]));
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
