#!/usr/bin/env node
// Read-only source review. Emit JSON without changing runs, snapshots, or source.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import ts from 'typescript';

const arguments_ = process.argv.slice(2);
const option = (name, fallback) => { const index = arguments_.indexOf(name); return index < 0 ? fallback : arguments_[index + 1]; };
const workspace = path.resolve(option('--workspace', process.cwd()));
const root = path.resolve(workspace, option('--audit-root', 'tasks/ui-test-coverage-20261022/evidence/audit-run-20261022'));
const decisionFile = path.resolve(workspace, option('--scope-exclusions', 'tasks/ui-test-coverage-20261022/evidence/step-audit-20261022/user-scope-exclusions.json'));
const read = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const relative = file => path.relative(workspace, file).split(path.sep).join('/');
const resolve = value => path.isAbsolute(value) ? value : path.resolve(workspace, value);
const digest = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const exists = file => fs.existsSync(file) && fs.statSync(file).isFile();
const currentHash = new Map();
function hash(file) {
  if (!currentHash.has(file)) currentHash.set(file, exists(file) ? digest(fs.readFileSync(file)) : null);
  return currentHash.get(file);
}
function files(directory) {
  if (!fs.existsSync(directory)) return [];
  return fs.readdirSync(directory, {withFileTypes:true}).flatMap(entry => {
    const file = path.join(directory, entry.name);
    return entry.isDirectory() ? files(file) : [file];
  });
}

const inventoryFile = path.join(root, 'inventory/summary.json');
const inventory = read(inventoryFile);
const preflightFile = resolve(inventory.caseRecords.path);
if (hash(preflightFile) !== inventory.caseRecords.sha256) throw new Error('Frozen inventory hash mismatch.');
const rows = fs.readFileSync(preflightFile, 'utf8').trim().split('\n').map(line => JSON.parse(line));
const decision = read(decisionFile);
const excluded = new Set(decision.cases.map(item => item.caseId));
const catalog = inventory.inputs.find(item => item.path.endsWith('test-cases.md'));
if (decision.catalogSha256 !== catalog.sha256 || hash(resolve(catalog.path)) !== catalog.sha256)
  throw new Error('Canonical catalog or scope decision hash mismatch.');
const variants = new Map();
for (const file of files(path.join(root, 'source-variants')).filter(file => file.endsWith('.json'))) {
  const item = read(file);
  if (item.source && item.sha256 && item.snapshot) variants.set(`${item.source}:${item.sha256}`, resolve(item.snapshot));
}
const latest = new Map();
const runs = new Map();
for (const directory of fs.readdirSync(path.join(root, 'application')).filter(name => name.startsWith('run-'))) {
  const run = path.join(root, 'application', directory);
  const inputsFile = path.join(run, 'run-inputs.json');
  if (!exists(inputsFile)) continue;
  const inputs = read(inputsFile);
  runs.set(directory, {directory:run, inputsFile, inputs, sources:new Map(inputs.sourceHashes.map(item => [item.path, item])),
    finalized:exists(path.join(run, 'run-result.json'))});
  const resultFiles = files(path.join(run, 'cases')).filter(file => path.basename(file) === 'result.json');
  for (const file of resultFiles) {
    const result = read(file);
    if (result.canonicalIdsMentioned?.length !== 1) continue;
    const caseId = result.canonicalIdsMentioned[0];
    if (excluded.has(caseId)) continue;
    const key = `${result.endedAt}/${directory}/${path.basename(path.dirname(file))}`;
    if (!latest.has(caseId) || key > latest.get(caseId).key) latest.set(caseId, {key, file, result, run:directory});
  }
}

const parsed = new Map();
function modules(source, file) {
  const key = `${file}:${digest(source)}`;
  if (parsed.has(key)) return parsed.get(key);
  const tree = ts.createSourceFile(file, source, ts.ScriptTarget.Latest, true);
  const imports = [], unresolved = [], browserLoads = [];
  const add = (node, specifier, kind, typeOnly=false) => imports.push({specifier, kind, typeOnly, line:tree.getLineAndCharacterOfPosition(node.getStart(tree)).line+1});
  function visit(node) {
    if (ts.isImportDeclaration(node) && ts.isStringLiteralLike(node.moduleSpecifier)) {
      const clause = node.importClause;
      const named = clause?.namedBindings;
      const typeOnly = Boolean(clause?.isTypeOnly || (!clause?.name && named && ts.isNamedImports(named) && named.elements.length && named.elements.every(item => item.isTypeOnly)));
      add(node, node.moduleSpecifier.text, 'import', typeOnly);
    } else if (ts.isExportDeclaration(node) && node.moduleSpecifier && ts.isStringLiteralLike(node.moduleSpecifier)) {
      const names = node.exportClause;
      add(node, node.moduleSpecifier.text, 'export', Boolean(node.isTypeOnly || (names && ts.isNamedExports(names) && names.elements.length && names.elements.every(item => item.isTypeOnly))));
    } else if (ts.isImportEqualsDeclaration(node) && ts.isExternalModuleReference(node.moduleReference) && node.moduleReference.expression && ts.isStringLiteralLike(node.moduleReference.expression)) {
      add(node, node.moduleReference.expression.text, 'import-equals', node.isTypeOnly);
    } else if (ts.isCallExpression(node)) {
      const expression = node.expression;
      const runtimeImport = expression.kind === ts.SyntaxKind.ImportKeyword || (ts.isIdentifier(expression) && expression.text === 'require');
      if (runtimeImport) {
        if (node.arguments[0] && ts.isStringLiteralLike(node.arguments[0])) add(node, node.arguments[0].text, 'runtime-load');
        else unresolved.push({line:tree.getLineAndCharacterOfPosition(node.getStart(tree)).line+1, expression:node.getText(tree).slice(0,180)});
      } else if (ts.isPropertyAccessExpression(expression) && expression.name.text === 'import') {
        browserLoads.push({line:tree.getLineAndCharacterOfPosition(node.getStart(tree)).line+1, expression:node.getText(tree).slice(0,180)});
      }
    }
    ts.forEachChild(node, visit);
  }
  visit(tree);
  const result = {imports, unresolved, browserLoads};
  parsed.set(key, result);
  return result;
}

function retained(run, sourcePath) {
  const item = run.sources.get(sourcePath);
  if (!item) return {error:'SOURCE_NOT_RECORDED',path:sourcePath};
  const snapshot = item.snapshotPath ? resolve(item.snapshotPath) : variants.get(`${sourcePath}:${item.sha256}`);
  if (snapshot && exists(snapshot)) {
    const bytes = fs.readFileSync(snapshot);
    if (digest(bytes) !== item.sha256) return {error:'RETAINED_SOURCE_HASH_MISMATCH',path:sourcePath,snapshot};
    return {bytes,sha256:item.sha256,snapshot:relative(snapshot),retention:item.snapshotPath?'RUN_SNAPSHOT':'RETAINED_VARIANT'};
  }
  const current = path.resolve(workspace, sourcePath);
  if (hash(current) === item.sha256) return {bytes:fs.readFileSync(current),sha256:item.sha256,snapshot:null,retention:'MATCHING_CURRENT_BYTES'};
  return {error:'HISTORICAL_BYTES_UNAVAILABLE',path:sourcePath,sha256:item.sha256,currentSha256:hash(current)};
}
function modulePath(specifier, importer, run, version) {
  const base = path.posix.normalize(path.posix.join(path.posix.dirname(importer), specifier));
  const candidates = /\.[cm]?jsx?$/.test(base)
    ? [base.replace(/\.js$/,'.ts').replace(/\.jsx$/,'.tsx').replace(/\.mjs$/,'.mts').replace(/\.cjs$/,'.cts'),base]
    : [base,`${base}.ts`,`${base}.tsx`,`${base}.mts`,`${base}.cts`,`${base}.json`,`${base}/index.ts`,`${base}/index.tsx`];
  return candidates.find(candidate => version === 'snapshot' ? run.sources.has(candidate) || exists(path.resolve(workspace,candidate)) : exists(path.resolve(workspace,candidate)));
}
function closure(entries, run, version) {
  const nodes = new Map(), edges = [], errors = [], dynamic = [], browserLoads = [], external = new Set(), typeOnly = [];
  const pending = [...entries];
  while (pending.length) {
    const sourcePath = pending.shift();
    if (nodes.has(sourcePath)) continue;
    const record = version === 'snapshot' ? retained(run,sourcePath) : {bytes:exists(path.resolve(workspace,sourcePath))?fs.readFileSync(path.resolve(workspace,sourcePath)):null,retention:'CURRENT_BYTES'};
    if (!record.bytes) { errors.push(record.error?record:{error:'CURRENT_SOURCE_UNAVAILABLE',path:sourcePath});nodes.set(sourcePath,{path:sourcePath,error:true});continue; }
    nodes.set(sourcePath,{path:sourcePath,sha256:digest(record.bytes),snapshot:record.snapshot??null,retention:record.retention});
    if (!/\.[cm]?[jt]sx?$/.test(sourcePath)) continue;
    const metadata = modules(record.bytes.toString('utf8'),sourcePath);
    dynamic.push(...metadata.unresolved.map(item=>({path:sourcePath,...item})));
    browserLoads.push(...metadata.browserLoads.map(item=>({path:sourcePath,...item})));
    for (const item of metadata.imports) {
      if (item.typeOnly) {typeOnly.push({from:sourcePath,...item});continue;}
      if (!item.specifier.startsWith('.')) {external.add(item.specifier);continue;}
      const target = modulePath(item.specifier,sourcePath,run,version);
      if (!target) {errors.push({error:'UNRESOLVED_LOCAL_IMPORT',path:sourcePath,...item});continue;}
      edges.push({from:sourcePath,to:target,...item});pending.push(target);
    }
  }
  return {nodes:[...nodes.values()].sort((a,b)=>a.path.localeCompare(b.path)),edges,errors,dynamicImports:dynamic,browserRuntimeLoads:browserLoads,externalPackages:[...external].sort(),typeOnlyImports:typeOnly};
}

const closureCache = new Map();
const cases = [];
for (const row of rows.filter(row=>!excluded.has(row.caseId))) {
  const attempt = latest.get(row.caseId);
  if (!attempt) {cases.push({caseId:row.caseId,status:'NO_RETAINED_ATTEMPT'});continue;}
  const run = runs.get(attempt.run);
  const entry = relative(resolve(attempt.result.source.file));
  const entries = [entry,'e2e/audit.config.ts','e2e/audit.reporter.ts'];
  const cacheKey = `${attempt.run}:${entry}`;
  if (!closureCache.has(cacheKey)) closureCache.set(cacheKey,{snapshot:closure(entries,run,'snapshot'),current:closure(entries,run,'current')});
  const graphs = closureCache.get(cacheKey);
  const consumed = new Set([...graphs.snapshot.nodes,...graphs.current.nodes].map(item=>item.path));
  const consumedDrift = [], unconsumedDrift = [];
  for (const item of run.sources.values()) {
    if (!/\.[cm]?tsx?$/.test(item.path)) continue;
    const currentSha256 = hash(path.resolve(workspace,item.path));
    if (currentSha256 === item.sha256) continue;
    (consumed.has(item.path)?consumedDrift:unconsumedDrift).push({path:item.path,recordedSha256:item.sha256,currentSha256,snapshot:item.snapshotPath?relative(resolve(item.snapshotPath)):null});
  }
  for (const item of graphs.current.nodes.filter(item=>!run.sources.has(item.path)))
    consumedDrift.push({path:item.path,recordedSha256:null,currentSha256:item.sha256,reason:'CURRENT_IMPORT_ADDED_WITHOUT_RECORDED_SOURCE'});
  cases.push({caseId:row.caseId,run:attempt.run,attemptPath:relative(attempt.file),attemptSha256:hash(attempt.file),runnerStatus:attempt.result.actualStatus,
    endedAt:attempt.result.endedAt,runFinalized:run.finalized,entryPoint:entry,entryPoints:entries,
    status:graphs.snapshot.errors.length||graphs.current.errors.length?'SOURCE_EVIDENCE_LIMIT':consumedDrift.length?'CONSUMED_IMPORT_BYTES_CHANGED':'CONSUMED_IMPORT_BYTES_MATCH',
    consumedSourceDrift:consumedDrift,unconsumedSourceDrift:unconsumedDrift,graphKey:cacheKey,
    rerunDecision:consumedDrift.length?'REVIEW_CHANGED_SYMBOLS_BEFORE_SCHEDULING':'NO_RERUN_FROM_IMPORT_BYTES',
    scopeLimit:'Import reachability is conservative. It does not prove a changed function or branch executed in this case.'});
}
const groups = new Map();
for (const item of cases) for (const change of item.consumedSourceDrift??[]) {
  const key = `${change.path}:${change.recordedSha256}:${change.currentSha256}`;
  if (!groups.has(key)) groups.set(key,{...change,cases:[],runs:new Set()});
  groups.get(key).cases.push(item.caseId);groups.get(key).runs.add(item.run);
}
const totals = Object.fromEntries([...new Set(cases.map(item=>item.status))].map(status=>[status,cases.filter(item=>item.status===status).length]));
const output = {schemaVersion:1,reviewedAt:new Date().toISOString(),scope:'Latest retained in-scope cases; transitive local runtime imports plus audit configuration and reporter entry points.',
  reviewer:'Codex /root/report_clarity',catalogSha256:catalog.sha256,scopeDecision:{path:relative(decisionFile),sha256:hash(decisionFile)},
  script:{path:relative(new URL(import.meta.url).pathname),sha256:hash(new URL(import.meta.url).pathname)},
  summary:{canonicalCases:rows.length,userExcludedCases:excluded.size,inScopeCases:cases.length,latestRetainedCases:latest.size,statuses:totals,
    uniqueImportClosures:closureCache.size,activeRuns:[...runs].filter(([,run])=>!run.finalized).map(([name])=>name)},
  consumedDriftGroups:[...groups.values()].map(item=>({...item,runs:[...item.runs].sort(),cases:item.cases.sort()})),
  cases,importClosures:Object.fromEntries(closureCache),
  limitations:['The script reads source and retained evidence. It does not change source, database, browser state, or results.',
    'Type-only imports are excluded from runtime reachability. External packages are listed without tracing their dependency tree.',
    'Static import reachability can include unused imports or functions. Changed-symbol review must determine case-specific reruns.',
    'Dynamic browser System.import loads, downloaded bundles, filesystem reads, remote services, environment variables, and native runtimes require separate evidence.',
    'An active run can add later case results. Regenerate this review after final execution and source changes.']};
console.log(JSON.stringify(output,null,2));
