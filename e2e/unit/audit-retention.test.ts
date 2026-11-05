import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, readFileSync, readdirSync, realpathSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import test, { type TestContext } from 'node:test';
import type { FullConfig, Suite, TestCase, TestResult } from '@playwright/test/reporter';
import AuditReporter from '../audit.reporter.js';
import { auditCaseId, digest } from '../support/audit-fixture.js';
import { auditHtmlReport, auditTraceMode } from '../support/audit-settings.js';

const case_ = { id: 'retention-test', title: 'RETENTION-001 preserves trace evidence',
  location: { file: 'controlled.spec.ts', line: 1, column: 1 }, expectedStatus: 'passed', annotations: [],
  outcome: () => 'expected' } as unknown as TestCase;
const id = auditCaseId(case_.id, case_.title);
function setup(t: TestContext) {
  const temporary = mkdtempSync(path.join(tmpdir(), 'audit-retention-'));
  t.after(() => rmSync(temporary, { recursive: true, force: true }));
  const output = path.join(temporary, 'run');
  mkdirSync(output);
  const reporter = new AuditReporter({ output });
  const result = (attachments: TestResult['attachments']) => ({ attachments, retry: 0,
    startTime: new Date('2026-11-05T00:00:00Z'), duration: 1, status: 'passed', errors: [], steps: [] }) as unknown as TestResult;
  const read = (name: string) => JSON.parse(readFileSync(path.join(output, 'cases', id, name), 'utf8'));
  return { temporary, output, reporter, result, read };
}

test('Given a trace inside the run, When its case completes, Then results and manifest reference its only retained payload', t => {
  const { output, reporter, result, read } = setup(t);
  const file = path.join(output, 'playwright-artifacts', 'trace.zip');
  mkdirSync(path.dirname(file));
  writeFileSync(file, 'controlled trace bytes');
  reporter.onTestBegin(case_, result([]));
  reporter.onTestEnd(case_, result([{ name: 'trace', path: file, contentType: 'application/zip' }]));
  const attachment = read('result.json').attachments[0];
  assert.equal(attachment.originalPath, file);
  assert.equal(attachment.retainedPath, realpathSync(file));
  assert.equal(attachment.retention, 'REUSED_RUN_ARTIFACT');
  assert.equal(attachment.sha256, digest(readFileSync(file)));
  assert.ok(!readdirSync(path.join(output, 'cases', id)).includes('attachments'));
  const artifacts = read('artifact-manifest.json').artifacts as { path: string; sha256: string; bytes: number }[];
  assert.equal(artifacts.filter(item => item.path === realpathSync(file)).length, 1);
  assert.equal(artifacts.find(item => item.path === realpathSync(file))?.sha256, attachment.sha256);
  assert.ok(artifacts.some(item => item.path.endsWith('result.json')));
  assert.ok(artifacts.some(item => item.path.endsWith('started.json')));
});

test('Given an external volatile trace, When its case completes, Then one byte-identical durable copy survives source removal', t => {
  const { temporary, output, reporter, result, read } = setup(t);
  const file = path.join(temporary, 'volatile.zip');
  writeFileSync(file, 'external trace bytes');
  reporter.onTestEnd(case_, result([{ name: 'trace', path: file, contentType: 'application/zip' }]));
  const attachment = read('result.json').attachments[0];
  assert.ok(attachment.retainedPath.startsWith(path.join(output, 'cases', id, 'attachments')));
  assert.equal(attachment.retention, 'COPIED_EXTERNAL_ARTIFACT');
  assert.equal(attachment.sha256, digest(readFileSync(file)));
  rmSync(file);
  assert.equal(readFileSync(attachment.retainedPath, 'utf8'), 'external trace bytes');
  assert.ok(read('artifact-manifest.json').artifacts.some((item: { path: string }) => item.path === realpathSync(attachment.retainedPath)));
});

test('Given a sibling path sharing the run prefix, When retaining an attachment, Then it is copied into the durable run', t => {
  const { output, reporter, result, read } = setup(t);
  const sibling = `${output}-other`;
  mkdirSync(sibling);
  const file = path.join(sibling, 'trace.zip');
  writeFileSync(file, 'sibling bytes');
  reporter.onTestEnd(case_, result([{ name: 'trace', path: file, contentType: 'application/zip' }]));
  assert.notEqual(read('result.json').attachments[0].retainedPath, file);
});

test('Given an in-run symlink to external bytes, When retaining the attachment, Then volatile bytes receive a durable copy', t => {
  const { temporary, output, reporter, result, read } = setup(t);
  const file = path.join(temporary, 'external.zip');
  const link = path.join(output, 'linked.zip');
  writeFileSync(file, 'external linked trace');
  try { symlinkSync(file, link); }
  catch (error) {
    if (process.platform === 'win32' && (error as NodeJS.ErrnoException).code === 'EPERM') {
      t.skip('This Windows account cannot create symbolic links.'); return;
    }
    throw error;
  }
  reporter.onTestEnd(case_, result([{ name: 'trace', path: link, contentType: 'application/zip' }]));
  const attachment = read('result.json').attachments[0];
  assert.notEqual(attachment.retainedPath, link);
  rmSync(file);
  assert.equal(readFileSync(attachment.retainedPath, 'utf8'), 'external linked trace');
});

test('Given capture settings, When run inputs are saved, Then safe resolved modes are recorded without private configuration', t => {
  const { output, reporter } = setup(t);
  const config = { workers: 1, metadata: { auditCapture: { htmlReport: false }, privateValue: 'must-not-be-retained' },
    projects: [{ name: 'controlled', use: { trace: { mode: 'on', sources: true }, screenshot: 'on', video: 'off',
      storageState: 'must-not-be-retained' } }] } as unknown as FullConfig;
  reporter.onBegin(config, { allTests: () => [case_] } as unknown as Suite);
  const inputs = JSON.parse(readFileSync(path.join(output, 'run-inputs.json'), 'utf8'));
  assert.deepEqual(inputs.captureSettings, { htmlReport: false,
    projects: [{ name: 'controlled', trace: 'on', screenshot: 'on', video: 'off' }] });
  assert.ok(!JSON.stringify(inputs).includes('must-not-be-retained'));
});

test('Given an external alias to durable run bytes, When the alias is removed, Then retained evidence resolves through the canonical run path', t => {
  const { temporary, output, reporter, result, read } = setup(t);
  const file = path.join(output, 'trace.zip');
  const alias = path.join(temporary, 'external-alias.zip');
  writeFileSync(file, 'durable bytes');
  try { symlinkSync(file, alias); }
  catch (error) {
    if (process.platform === 'win32' && (error as NodeJS.ErrnoException).code === 'EPERM') {
      t.skip('This Windows account cannot create symbolic links.'); return;
    }
    throw error;
  }
  reporter.onTestEnd(case_, result([{ name: 'trace', path: alias, contentType: 'application/zip' }]));
  const attachment = read('result.json').attachments[0];
  assert.equal(attachment.originalPath, alias);
  assert.equal(attachment.retainedPath, realpathSync(file));
  assert.equal(attachment.retention, 'REUSED_RUN_ARTIFACT');
  rmSync(alias);
  assert.equal(readFileSync(attachment.retainedPath, 'utf8'), 'durable bytes');
  assert.equal(read('artifact-manifest.json').artifacts.filter((item: { path: string }) => item.path === attachment.retainedPath).length, 1);
});

test('Given no capture overrides, When choosing audit settings, Then successful traces and HTML copies are omitted', () => {
  assert.equal(auditTraceMode({}), 'retain-on-failure');
  assert.equal(auditHtmlReport({}), false);
});

test('Given explicit capture controls, When choosing audit settings, Then supported modes apply and invalid values fail', () => {
  for (const trace of ['on', 'off', 'retain-on-failure'] as const)
    assert.equal(auditTraceMode({ E2E_AUDIT_TRACE: trace }), trace);
  assert.equal(auditHtmlReport({ E2E_AUDIT_HTML: '1' }), true);
  assert.equal(auditHtmlReport({ E2E_AUDIT_HTML: '0' }), false);
  for (const trace of ['', 'true', 'retain-on-fail'])
    assert.throws(() => auditTraceMode({ E2E_AUDIT_TRACE: trace }), /E2E_AUDIT_TRACE must be/);
  for (const value of ['', 'true', 'yes'])
    assert.throws(() => auditHtmlReport({ E2E_AUDIT_HTML: value }), /E2E_AUDIT_HTML must be/);
});
