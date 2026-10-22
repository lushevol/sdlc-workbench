import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../../', import.meta.url));
const manifestPath = 'e2e/traceability/bindings.json';
const generatedPath = 'e2e/traceability/cases.json';
const errors = [];
const implementationSources = new Map();
const hash = (value) => createHash('sha256').update(value).digest('hex');
const read = (relative) => fs.readFileSync(path.join(root, relative), 'utf8');
const json = (relative) => JSON.parse(read(relative));
const fail = (message) => errors.push(message);

function assert(condition, message) {
  if (!condition) fail(message);
}

function unique(items, label) {
  const seen = new Set();
  for (const item of items) {
    assert(!seen.has(item), `Duplicate ${label}: ${item}`);
    seen.add(item);
  }
  return seen;
}

function checkReference(reference, owner) {
  if (!reference || typeof reference.path !== 'string' || typeof reference.symbol !== 'string') {
    fail(`${owner}: a source reference requires path and symbol`);
    return;
  }
  const resolved = path.resolve(root, reference.path);
  if (!resolved.startsWith(`${path.resolve(root)}${path.sep}`) || !reference.path.startsWith('e2e/')) {
    fail(`${owner}: implementation reference must stay inside e2e/: ${reference.path}`);
    return;
  }
  if (!fs.existsSync(resolved)) {
    fail(`${owner}: missing implementation file ${reference.path}`);
    return;
  }
  assert(reference.symbol.length > 0, `${owner}: empty implementation symbol`);
  const content = read(reference.path);
  assert(content.includes(reference.symbol), `${owner}: missing symbol ${reference.symbol} in ${reference.path}`);
  implementationSources.set(reference.path, hash(content));
}

function parseCases(catalog) {
  const headings = [...catalog.matchAll(/^#{1,4} .+$/gm)];
  return headings.flatMap((heading, index) => {
    const id = heading[0].match(/^#### ([A-Z]+(?:-[A-Z]+)*-\d+)$/)?.[1];
    if (!id) return [];
    const end = headings[index + 1]?.index ?? catalog.length;
    const block = catalog.slice(heading.index, end);
    const line = catalog.slice(0, heading.index).split('\n').length;
    return [{ id, block, line, sha256: hash(block) }];
  });
}

function matchesComponent(component, identities) {
  return identities.some((identity) =>
    component.type === identity.type &&
    component.identity === identity.identity &&
    component.scope === identity.scope,
  );
}

function build() {
  const bindings = json(manifestPath);
  assert(bindings.schemaVersion === 1, 'Unsupported binding schemaVersion');
  const catalog = read(bindings.canonicalCatalog);
  const catalogHash = hash(catalog);
  const inventory = json(bindings.inventory);
  const reviews = read(bindings.reviews).trim().split('\n').map(JSON.parse);
  const gherkin = json(bindings.gherkinManifest);
  const definitions = parseCases(catalog);
  const inventoryById = new Map(inventory.cases.map((item) => [item.id, item]));
  const reviewsById = new Map(reviews.map((item) => [item.case_id, item]));
  const supportIdentities = new Map();
  const bindingsById = new Map(bindings.caseBindings.map((item) => [item.caseId, item]));
  const definitionIds = unique(definitions.map((item) => item.id), 'canonical case');
  unique(inventory.cases.map((item) => item.id), 'inventory case');
  unique(reviews.map((item) => item.case_id), 'review case');
  unique(bindings.componentSupport.map((item) => item.id), 'component support');
  unique(bindings.caseBindings.map((item) => item.caseId), 'case binding');
  assert(inventory.total === definitions.length, 'Canonical count differs from inventory total');
  assert(inventory.cases.length === definitions.length, 'Canonical count differs from inventory cases');
  assert(reviews.length === definitions.length, 'Canonical count differs from review records');
  assert(Object.keys(gherkin.scenarios).length === definitions.length, 'Canonical count differs from Gherkin manifest');
  for (const id of [...inventoryById.keys(), ...reviewsById.keys(), ...Object.keys(gherkin.scenarios), ...bindingsById.keys()]) {
    assert(definitionIds.has(id), `Orphan case reference: ${id}`);
  }

  for (const support of bindings.componentSupport) {
    assert(Array.isArray(support.canonicalComponents) && support.canonicalComponents.length > 0,
      `${support.id}: no canonical component references`);
    const identities = [];
    for (const reference of support.canonicalComponents ?? []) {
      const component = gherkin.scenarios[reference.caseId]?.components[reference.componentId];
      assert(Boolean(component), `${support.id}: unknown canonical component ${reference.caseId}/${reference.componentId}`);
      if (component) identities.push(component);
    }
    supportIdentities.set(support.id, identities);
    checkReference(support.implementation, support.id);
    checkReference(support.contract, support.id);
    assert(support.grounding === 'SOURCE_DERIVED', `${support.id}: static support cannot claim runtime grounding`);
    for (const method of support.methods ?? []) checkReference(method, support.id);
  }

  const cases = definitions.map((definition) => {
    const item = inventoryById.get(definition.id);
    const review = reviewsById.get(definition.id);
    const scenario = gherkin.scenarios[definition.id];
    if (!item || !review || !scenario) {
      fail(`${definition.id}: missing canonical evidence`);
      return { caseId: definition.id };
    }
    assert(review.canonical_case_sha256 === definition.sha256, `${definition.id}: stale canonical case hash`);
    assert(scenario.sha256 === catalogHash, `${definition.id}: stale Gherkin catalog hash`);
    assert(item.definition_version === review.definition_version, `${definition.id}: definition version differs`);
    const steps = Object.entries(scenario.steps).map(([line, step]) => ({ line: Number(line), ...step }));
    const assertions = steps.filter((step) => step.kind === 'assertion');
    assert(item.assertion_count === assertions.length, `${definition.id}: assertion count differs`);
    const support = bindings.componentSupport.filter((entry) =>
      Object.values(scenario.components).some((component) => matchesComponent(component, supportIdentities.get(entry.id))),
    );
    const binding = bindingsById.get(definition.id);
    const coveredLines = new Set();
    if (binding) {
      assert(binding.definitionSha256 === definition.sha256, `${definition.id}: stale binding definition hash`);
      assert(binding.status === 'PARTIAL' || binding.status === 'COMPLETE', `${definition.id}: invalid binding status`);
      assert(['SYNTHETIC_FIXTURE', 'REAL_APPLICATION'].includes(binding.fixtureScope),
        `${definition.id}: invalid fixture scope`);
      assert(Array.isArray(binding.gaps), `${definition.id}: missing binding gaps`);
      assert(typeof binding.workflowId === 'string' && binding.workflowId.length > 0, `${definition.id}: missing workflowId`);
      for (const reference of [binding.workflow, binding.spec, ...(binding.setup ?? []), ...(binding.cleanup ?? [])]) {
        checkReference(reference, definition.id);
      }
      for (const action of binding.actions ?? []) {
        assert(typeof action.id === 'string' && action.id.length > 0, `${definition.id}: missing action ID`);
        checkReference(action.catalog, `${definition.id}/${action.id}`);
        checkReference(action.implementation, `${definition.id}/${action.id}`);
      }
      unique((binding.steps ?? []).map((step) => step.line), `${definition.id} step binding`);
      for (const step of binding.steps ?? []) {
        const canonical = steps.find((entry) => entry.line === step.line);
        assert(Boolean(canonical), `${definition.id}: unknown canonical step line ${step.line}`);
        assert(['SYNTHETIC_ANALOGUE', 'REAL_APPLICATION'].includes(step.scope),
          `${definition.id}:${step.line}: invalid step scope`);
        assert(Array.isArray(step.assertionIds) && step.assertionIds.length > 0 || canonical?.kind !== 'assertion',
          `${definition.id}:${step.line}: missing assertionIds`);
        checkReference(step.implementation, `${definition.id}:${step.line}`);
        for (const assertionId of step.assertionIds ?? []) {
          checkReference({ ...step.implementation, symbol: assertionId }, `${definition.id}:${step.line}`);
        }
        coveredLines.add(step.line);
      }
      if (binding.status === 'COMPLETE') {
        assert(binding.fixtureScope === 'REAL_APPLICATION', `${definition.id}: complete coverage requires real application fixtures`);
        assert(binding.gaps.length === 0, `${definition.id}: complete binding retains gaps`);
        assert(binding.setup?.length > 0 && binding.cleanup?.length > 0, `${definition.id}: complete binding requires setup and cleanup`);
        assert(binding.actions?.length > 0, `${definition.id}: complete binding requires an action`);
        assert(steps.every((step) => coveredLines.has(step.line)), `${definition.id}: complete binding omits canonical steps`);
        assert(binding.steps.every((step) => step.scope === 'REAL_APPLICATION'),
          `${definition.id}: complete binding contains substitute fixture steps`);
        assert(item.quality_status !== 'FAIL', `${definition.id}: complete binding cannot bypass a failed canonical quality gate`);
      }
    }
    const status = item.quality_status === 'FAIL' ? 'BLOCKED'
      : binding?.status === 'COMPLETE' ? 'COMPLETE_BINDING'
        : binding || support.length > 0 ? 'PARTIAL' : 'UNBOUND';
    return {
      caseId: definition.id,
      definition: `${bindings.canonicalCatalog}#${definition.id.toLowerCase()}`,
      definitionLine: definition.line,
      definitionVersion: item.definition_version,
      definitionSha256: definition.sha256,
      businessIntent: scenario.behavior.intent,
      priority: item.priority,
      basis: item.basis,
      sourceIds: item.source_ids,
      canonicalQualityStatus: item.quality_status,
      canonicalAutomationReady: item.automation_ready,
      canonicalExecutionStatus: item.status,
      review: `${bindings.reviews}#L${review.metadata_line}`,
      assertionCount: assertions.length,
      uiAssertionCount: assertions.filter((step) => step.observation === 'ui').length,
      functionalAssertionCount: assertions.filter((step) => step.observation === 'functional').length,
      supportStatus: status,
      componentSupport: support.map((entry) => entry.id),
      componentSupportLimits: [...new Set(support.flatMap((entry) => entry.limits ?? []))],
      workflowId: binding?.workflowId ?? null,
      workflowBindingStatus: binding?.status ?? null,
      boundSteps: coveredLines.size,
      totalSteps: steps.length,
      boundAssertions: assertions.filter((step) => coveredLines.has(step.line)).length,
      gaps: [
        ...(item.quality_status === 'FAIL' ? ['Canonical UI quality gate failed. Resolve the linked canonical review gaps.'] : []),
        ...(binding?.gaps ?? ['No complete scenario binding exists. Source-derived component support covers only named controls.']),
      ],
      executionEvidence: null,
    };
  });
  const count = (key) => Object.fromEntries([...new Set(cases.map((item) => item[key]))].sort().map((value) =>
    [value, cases.filter((item) => item[key] === value).length],
  ));
  return {
    schemaVersion: 1,
    canonicalCatalog: bindings.canonicalCatalog,
    canonicalCatalogSha256: catalogHash,
    bindings: manifestPath,
    bindingsSha256: hash(read(manifestPath)),
    definitionInputs: [bindings.inventory, bindings.reviews, bindings.gherkinManifest]
      .map((sourcePath) => ({ path: sourcePath, sha256: hash(read(sourcePath)) })),
    implementationSources: [...implementationSources].sort(([left], [right]) => left.localeCompare(right))
      .map(([sourcePath, sha256]) => ({ path: sourcePath, sha256 })),
    limits: [
      'Static references establish POM support only. They do not establish current UI uniqueness or passing business execution.',
      'Synthetic fixtures test harness mechanics. They do not establish deployed application or BFF behavior.',
      'Canonical review, readiness, and execution states remain unchanged.',
    ],
    summary: {
      canonicalCases: cases.length,
      assertions: cases.reduce((total, item) => total + (item.assertionCount ?? 0), 0),
      supportStatus: count('supportStatus'),
      canonicalExecutionStatus: count('canonicalExecutionStatus'),
      sourceDerivedComponentGroups: bindings.componentSupport.length,
      partialWorkflowBindings: bindings.caseBindings.filter((binding) => binding.status === 'PARTIAL').length,
      completeWorkflowBindings: bindings.caseBindings.filter((binding) => binding.status === 'COMPLETE').length,
      measuredLiveComponentCoverage: null,
      verifiedBusinessScenarios: 0,
    },
    cases,
  };
}

try {
  const args = process.argv.slice(2);
  assert(args.every((arg) => arg === '--write'), 'Usage: node e2e/scripts/check-traceability.mjs [--write]');
  const output = build();
  const serialized = `${JSON.stringify(output, null, 2)}\n`;
  if (errors.length === 0 && args.includes('--write')) fs.writeFileSync(path.join(root, generatedPath), serialized);
  if (errors.length === 0 && !args.includes('--write')) {
    assert(fs.existsSync(path.join(root, generatedPath)), `Missing ${generatedPath}; run with --write`);
    if (fs.existsSync(path.join(root, generatedPath))) {
      assert(read(generatedPath) === serialized, `Stale ${generatedPath}; inspect bindings, then run with --write`);
    }
  }
  console.log(JSON.stringify({
    status: errors.length ? 'FAILED' : 'PASSED',
    mode: args.includes('--write') ? 'write' : 'check',
    summary: output.summary,
    errors,
    limitations: output.limits,
  }, null, 2));
  process.exitCode = errors.length ? 1 : 0;
} catch (error) {
  console.error(JSON.stringify({ status: 'FAILED', errors: [...errors, error.message] }, null, 2));
  process.exitCode = 1;
}
