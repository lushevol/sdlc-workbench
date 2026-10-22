import { test as base, expect, type Page, type TestInfo } from '@playwright/test';
import { createHash } from 'node:crypto';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';

export type AuditScope = 'SYNTHETIC_HARNESS' | 'ACTUAL_APPLICATION_LOCAL_SERVICES' | 'CONFIGURED_APPLICATION';
type AuditOptions = { auditScope: AuditScope; auditFixture: string };
export const auditEnabled = () => Boolean(process.env.E2E_AUDIT_OUTPUT);
export function auditOutput(): string {
  if (!process.env.E2E_AUDIT_OUTPUT) throw new Error('E2E_AUDIT_OUTPUT is required for durable audit capture.');
  return path.resolve(process.env.E2E_AUDIT_OUTPUT);
}
export function auditCaseId(testId: string, title: string, retry = 0): string {
  const slug = title.replace(/[^a-zA-Z0-9]+/g, '-').replace(/^-|-$/g, '').toLowerCase().slice(0, 75);
  return `${slug}-${createHash('sha256').update(testId).digest('hex').slice(0, 12)}-attempt-${retry + 1}`;
}
export const digest = (bytes: Buffer | string) => createHash('sha256').update(bytes).digest('hex');
export async function saveAuditJson(file: string, value: unknown): Promise<void> {
  await mkdir(path.dirname(file), { recursive: true });
  await writeFile(file, `${JSON.stringify(value, null, 2)}\n`, { mode: 0o600 });
}

type Frame = {
  sequence: number; phase: string; capturedAt: string; path: string; sha256: string;
  claim: string; step: string; url: string; viewport: unknown; scope: AuditScope;
  method: 'Playwright Page.screenshot'; limits: string[];
};

export class AuditCapture {
  private frames: Frame[] = [];
  private gaps: { phase: string; capturedAt: string; error: string }[] = [];
  private sequence = 0;
  readonly caseId: string;
  readonly directory: string | null;

  constructor(readonly page: Page, readonly testInfo: TestInfo, readonly scope: AuditScope, readonly fixture: string) {
    this.caseId = auditCaseId(testInfo.testId, testInfo.title, testInfo.retry);
    this.directory = auditEnabled() ? path.join(auditOutput(), 'cases', this.caseId) : null;
  }

  async capture(phase: string, claim: string, step = 'Named test assertion at the corresponding source location'): Promise<void> {
    if (!this.directory) return;
    const sequence = ++this.sequence;
    const safePhase = phase.replace(/[^a-zA-Z0-9-]+/g, '-').toLowerCase();
    const filename = `${String(sequence).padStart(3, '0')}-${safePhase}.png`;
    try {
      await mkdir(this.directory, { recursive: true });
      const file = path.join(this.directory, filename);
      await this.page.screenshot({ path: file, fullPage: true, animations: 'disabled', timeout: 10000 });
      const frame: Frame = { sequence, phase, capturedAt: new Date().toISOString(), path: file,
        sha256: digest(await readFile(file)), claim, step, url: this.page.url(),
        viewport: this.page.viewportSize(), scope: this.scope, method: 'Playwright Page.screenshot',
        limits: ['The screenshot establishes visible state only. It does not prove request, storage, timing, or business results.',
          ...(this.scope === 'SYNTHETIC_HARNESS' ? ['The browser rendered a controlled fixture. The real MFE and BFF were not executed.'] : [])] };
      this.frames.push(frame);
      await saveAuditJson(path.join(this.directory, filename.replace('.png', '.json')), frame);
      await this.testInfo.attach(`${phase} (${this.scope})`, { path: file, contentType: 'image/png' });
    } catch (error) {
      this.gaps.push({ phase, capturedAt: new Date().toISOString(), error: error instanceof Error ? error.name : 'UnknownError' });
    }
    await this.persist();
  }

  async record(name: string, observations: unknown): Promise<void> {
    if (!this.directory) return;
    const filename = `${name.replace(/[^a-zA-Z0-9-]+/g, '-').toLowerCase()}.json`;
    await saveAuditJson(path.join(this.directory, filename), { recordedAt: new Date().toISOString(),
      caseId: this.caseId, scope: this.scope, observations });
  }

  async persist(): Promise<void> {
    if (!this.directory) return;
    await saveAuditJson(path.join(this.directory, 'frames.json'), {
      caseId: this.caseId, testId: this.testInfo.testId, title: this.testInfo.title,
      scope: this.scope, fixture: this.fixture, source: this.testInfo.file,
      browserVersion: this.page.context().browser()?.version() ?? null,
      captureStatus: this.gaps.length ? 'INCOMPLETE' : this.frames.length ? 'CAPTURED' : 'NO_FRAMES',
      frames: this.frames, captureGaps: this.gaps,
      canonicalBusinessStatus: this.scope === 'SYNTHETIC_HARNESS' ? 'NOT_RUN' : 'LOCAL_CONTROLLED_ASSERTIONS',
    });
  }
}

export const test = base.extend<AuditOptions & { audit: AuditCapture }>({
  auditScope: ['SYNTHETIC_HARNESS', { option: true }],
  auditFixture: ['Source-shaped controlled DOM and routed responses; no actual MFE or BFF execution.', { option: true }],
  audit: async ({ page, auditScope, auditFixture }, use, testInfo) => {
    const audit = new AuditCapture(page, testInfo, auditScope, auditFixture);
    testInfo.annotations.push({ type: 'audit-scope', description: auditScope });
    testInfo.annotations.push({ type: 'audit-fixture', description: auditFixture });
    try { await use(audit); }
    finally {
      await audit.capture(testInfo.status === testInfo.expectedStatus ? 'final-result' : 'failure-result',
        testInfo.status === testInfo.expectedStatus ? 'The final visible state after the named test assertions.' : 'The visible state when the test failed.',
        `Test source: ${testInfo.file}:${testInfo.line}`);
      await audit.persist();
    }
  },
});
export { expect };
