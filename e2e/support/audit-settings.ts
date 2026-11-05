export type AuditTraceMode = 'off' | 'on' | 'retain-on-failure';

export function auditTraceMode(environment: NodeJS.ProcessEnv = process.env): AuditTraceMode {
  const value = environment.E2E_AUDIT_TRACE ?? 'retain-on-failure';
  if (value !== 'off' && value !== 'on' && value !== 'retain-on-failure')
    throw new Error('E2E_AUDIT_TRACE must be off, on, or retain-on-failure.');
  return value;
}

export function auditHtmlReport(environment: NodeJS.ProcessEnv = process.env): boolean {
  const value = environment.E2E_AUDIT_HTML ?? '0';
  if (value !== '0' && value !== '1') throw new Error('E2E_AUDIT_HTML must be 0 or 1.');
  return value === '1';
}
