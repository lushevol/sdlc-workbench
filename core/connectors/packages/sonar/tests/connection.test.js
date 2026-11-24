import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { getSonarConnection } from '../src/connection.js';

describe('getSonarConnection', () => {
  let originalEnv;

  beforeEach(() => {
    originalEnv = process.env.NODE_TLS_REJECT_UNAUTHORIZED;
  });

  afterEach(() => {
    if (originalEnv === undefined) delete process.env.NODE_TLS_REJECT_UNAUTHORIZED;
    else process.env.NODE_TLS_REJECT_UNAUTHORIZED = originalEnv;
    vi.restoreAllMocks();
  });

  it('returns an object with baseUrl and headers', () => {
    const conn = getSonarConnection('mytoken');
    expect(conn).toHaveProperty('baseUrl');
    expect(conn).toHaveProperty('headers');
  });

  it('sets baseUrl to the hardcoded SonarQube URL', () => {
    const conn = getSonarConnection('mytoken');
    expect(conn.baseUrl).toBe('https://sonarqube.vx.standardchartered.com');
  });

  it('sets Authorization header as Bearer token', () => {
    const conn = getSonarConnection('my-secret-token');
    expect(conn.headers['Authorization']).toBe('Bearer my-secret-token');
  });

  it('sets Accept header to application/json', () => {
    const conn = getSonarConnection('t');
    expect(conn.headers['Accept']).toBe('application/json');
  });

  it('sets Content-Type header to application/json', () => {
    const conn = getSonarConnection('t');
    expect(conn.headers['Content-Type']).toBe('application/json');
  });

  it.each([undefined, '1'])('preserves the caller TLS setting %s', (value) => {
    if (value === undefined) delete process.env.NODE_TLS_REJECT_UNAUTHORIZED;
    else process.env.NODE_TLS_REJECT_UNAUTHORIZED = value;
    getSonarConnection('t');
    expect(process.env.NODE_TLS_REJECT_UNAUTHORIZED).toBe(value);
  });

  it('handles tokens with special characters', () => {
    const token = 'abc123-def_456.ghi';
    const conn = getSonarConnection(token);
    expect(conn.headers['Authorization']).toBe(`Bearer ${token}`);
  });
});
