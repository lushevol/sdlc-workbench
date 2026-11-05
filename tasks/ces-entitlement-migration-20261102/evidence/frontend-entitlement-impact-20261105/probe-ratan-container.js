// Run from any directory: node /absolute/path/to/probe-ratan-container.js
// This capture probe edits evidence only. It does not modify application source.
import { createRequire } from "module";
import { fileURLToPath } from "url";
const require = createRequire(import.meta.url);
const __filename = fileURLToPath(import.meta.url);
const fs = require("fs");
const path = require("path");
const __dirname = path.dirname(__filename);
const crypto = require("crypto");
const { execFileSync } = require("child_process");
const root = path.resolve(__dirname, "../../../..");
const sourcePath = "repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts";
const capturePath = "tasks/ces-entitlement-migration-20261102/ces migration/login-response.json";
const dumpPath = "tasks/ces-entitlement-migration-20261102/ces migration/application_tile_1105.csv";
const evidencePath = path.join(__dirname, "ratan-container.json");
const read = (p) => fs.readFileSync(path.join(root, p));
const hash = (bytes) => crypto.createHash("sha256").update(bytes).digest("hex");
const evidence = JSON.parse(fs.readFileSync(evidencePath, "utf8"));
for (const p of [sourcePath, capturePath, dumpPath]) {
  const binding = evidence.files.find((f) => f.path === p);
  if (!binding || hash(read(p)) !== binding.sha256) throw new Error("Source binding changed: " + p);
}
const ts = require(require.resolve("typescript", { paths: [path.join(root, "repos/ui/mfe-base")] }));
const capture = JSON.parse(read(capturePath));
const user = JSON.parse(capture.userInfo);
const payload = JSON.parse(Buffer.from(capture.entitlementsToken.split(".")[1], "base64url").toString());
user.entitlements = typeof payload.entitlements === "string" ? JSON.parse(payload.entitlements) : payload.entitlements;
user.id = user.sub;
user.fullName = user.fullName || user.sub;
let store = { user, entities: capture.entities };
const compiled = ts.transpileModule(read(sourcePath).toString(), {
  compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020 },
}).outputText;
const moduleObject = { exports: {} };
new Function("require", "module", "exports", compiled)(
  (name) => {
    if (name === "../Root/import") return { Hooks: { getHooks: () => ({ store }) } };
    throw new Error("Unexpected module import: " + name);
  },
  moduleObject,
  moduleObject.exports
);
const api = moduleObject.exports;
const app = capture.entities.find((e) => e.name === "RATAN_ENTITLEMENT_RULE");
const configuredFeatureCounts = JSON.parse(execFileSync("python3", ["-c", [
  "import csv,json,sys,collections",
  "rows=list(csv.DictReader(open(sys.argv[1],newline='')))",
  "counts=collections.Counter(r['entitlement_app_feature'] for r in rows if r['entitlement_source']=='EMS3' and r['entitlement_app_name']=='RATAN_ENTITLEMENT_RULE')",
  "print(json.dumps(dict(counts)))",
].join("\n"), path.join(root, dumpPath)], { encoding: "utf8" }));
const allGrants = app.subjects.flatMap((subject) => subject.actions.map((action) => {
  const code = subject.name + ":" + action.name;
  return {
    code,
    captured_grant: true,
    actual: api.hasPermission(code),
    classification: configuredFeatureCounts[subject.name]
      ? "feature referenced by supplied tile dump"
      : "captured grant; no exact feature reference in supplied tile dump",
    configured_feature_rows: configuredFeatureCounts[subject.name] || 0,
  };
}));
const negativeControls = [
  "RATAN_CASHFLOW_BLOTTER:F_Custom_View_Builder_Public",
  "RATAN_CASHFLOW_BLOTTER:NONEXISTENT_ACTION",
].map((code) => ({ code, captured_grant: false, actual: api.hasPermission(code) }));
const actualRole = api.getUser().role ?? null;
const exceptionPage = api.hasExceptionPagePermission();
store = { user, entities: capture.entities.map((e) => e === app ? { ...e, name: "X_RATANONE" } : e) };
const shapeControl = allGrants.map(({ code }) => ({ code, actual: api.hasPermission(code) }));
const shapeNegativeControls = negativeControls.map(({ code }) => ({ code, actual: api.hasPermission(code) }));
const summary = {
  captured_grants: allGrants.length,
  current_true: allGrants.filter((x) => x.actual).length,
  current_false: allGrants.filter((x) => !x.actual).length,
  configured_feature_grants: allGrants.filter((x) => x.configured_feature_rows > 0).length,
  configured_feature_true: allGrants.filter((x) => x.configured_feature_rows > 0 && x.actual).length,
  no_exact_tile_feature_reference: allGrants.filter((x) => !x.configured_feature_rows).length,
  shape_control_true: shapeControl.filter((x) => x.actual).length,
};
if (summary.captured_grants !== 31 || summary.current_true !== 1 || summary.current_false !== 30
    || summary.shape_control_true !== 31 || negativeControls.some((x) => x.actual)
    || shapeNegativeControls.some((x) => x.actual) || actualRole !== null || exceptionPage !== false) {
  throw new Error("Capture probe result differs from retained expectations.");
}
evidence.probe.case_id = "TC-FE-CES-001";
evidence.probe.canonical_case = "../../06-test-cases.md#tc-fe-ces-001";
evidence.probe.completed_at = new Date().toISOString();
evidence.probe.steps = [
  "Verify original source and capture hashes against retained bindings.",
  "Transpile the original helper and inject the captured entities and decoded user into Hooks.getHooks.",
  "Call hasPermission for every captured CES feature/action pair and both absent-action controls.",
  "Read getUser().role and hasExceptionPagePermission().",
  "Rename only the captured CES entity to X_RATANONE and repeat the permission calls as a synthetic shape control.",
  "Save outcomes immediately. Classify grants by exact feature references in the supplied tile dump.",
];
evidence.probe.all_captured_grants = allGrants;
evidence.probe.negative_controls = negativeControls;
evidence.probe.summary = summary;
evidence.probe.shape_control = {
  change: "Only rename captured CES entity to X_RATANONE. Permissions and role values remain unchanged.",
  checks: shapeControl,
  negative_controls: shapeNegativeControls,
  classification: "Synthetic shape control. Actual EMS2 baseline is unavailable.",
};
evidence.probe.actual_role = actualRole;
evidence.probe.actual_exception_page_permission = exceptionPage;
evidence.probe.reproduction = {
  command: "node tasks/ces-entitlement-migration-20261102/evidence/frontend-entitlement-impact-20261105/probe-ratan-container.js",
  cwd: "Workbench repository root",
  script_sha256: hash(fs.readFileSync(__filename)),
  node_version: process.version,
  typescript_version: ts.version,
  python_use: "Parse the supplied CSV with the standard csv module. No network or downloads.",
};
evidence.probe.classification_limit = "Tile dump reference counts include all supplied rows. They do not establish active deployment or complete business requirements. Unreferenced captured features remain capture observations only.";
if (!evidence.files.some((f) => f.path === dumpPath)) evidence.files.push({ path: dumpPath, sha256: hash(read(dumpPath)) });
fs.writeFileSync(evidencePath, JSON.stringify(evidence, null, 2) + "\n");
console.log(JSON.stringify({ case_id: evidence.probe.case_id, summary, assertion_status: "PASSED", evidence: path.relative(root, evidencePath) }));
