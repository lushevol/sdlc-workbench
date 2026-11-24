import { describe, it, expect } from 'vitest';
import { formatError } from '../src/errors.js';

describe('formatError', () => {
  it('returns the message of an Error instance', () => {
    expect(formatError(new Error('boom'))).toBe('boom');
  });

  it('falls back to String(error) when the thrown value has no message', () => {
    expect(formatError('plain string error')).toBe('plain string error');
  });

  it('falls back to String(error) for a plain object without a message', () => {
    expect(formatError({ code: 500 })).toBe('[object Object]');
  });
});
