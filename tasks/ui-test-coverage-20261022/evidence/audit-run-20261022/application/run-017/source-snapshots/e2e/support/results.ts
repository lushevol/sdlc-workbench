import { createHash } from 'node:crypto';

export type ExecutionScope = 'synthetic-fixture' | 'configured-application';
export type AssertionResult = {
  id: string;
  status: 'passed' | 'failed' | 'unverified';
  actual: unknown;
};

export function sha256(value: string): string {
  return createHash('sha256').update(value).digest('hex');
}

export function assertion(id: string, passed: boolean, actual: unknown): AssertionResult {
  return { id, status: passed ? 'passed' : 'failed', actual };
}
