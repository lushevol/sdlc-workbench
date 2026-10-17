import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { getNexusConnection } from '../src/connection.js';

describe('getNexusConnection', () => {
  let originalEnv;

  beforeEach(() => {
    originalEnv = process.env.NODE_TLS_REJECT_UNAUTHORIZED;
  });

  afterEach(() => {
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = originalEnv;
    vi.restoreAllMocks();
  });

  it('returns an object with baseUrl and headers', () => {
    const conn = getNexusConnection('myuser', 'mypassword');
    expect(conn).toHaveProperty('baseUrl');
    expect(conn).toHaveProperty('headers');
  });

  it('sets baseUrl to the hardcoded Nexus IQ URL', () => {
    const conn = getNexusConnection('myuser', 'mypassword');
    expect(conn.baseUrl).toBe('https://sonatypenexus.global.standardchartered.com');
  });

  it('sets Authorization header as Basic with base64-encoded credentials', () => {
    const conn = getNexusConnection('user123', 'pass456');
    const expected = `Basic ${Buffer.from('user123:pass456').toString('base64')}`;
    expect(conn.headers['Authorization']).toBe(expected);
  });

  it('sets Content-Type and Accept headers to application/json', () => {
    const conn = getNexusConnection('u', 'p');
    expect(conn.headers['Content-Type']).toBe('application/json');
    expect(conn.headers['Accept']).toBe('application/json');
  });

  it('sets NODE_TLS_REJECT_UNAUTHORIZED to 0', () => {
    getNexusConnection('u', 'p');
    expect(process.env.NODE_TLS_REJECT_UNAUTHORIZED).toBe('0');
  });

  it('handles special characters in credentials', () => {
    const conn = getNexusConnection('user@domain.com', 'p@ss:word');
    const expected = `Basic ${Buffer.from('user@domain.com:p@ss:word').toString('base64')}`;
    expect(conn.headers['Authorization']).toBe(expected);
  });
});
