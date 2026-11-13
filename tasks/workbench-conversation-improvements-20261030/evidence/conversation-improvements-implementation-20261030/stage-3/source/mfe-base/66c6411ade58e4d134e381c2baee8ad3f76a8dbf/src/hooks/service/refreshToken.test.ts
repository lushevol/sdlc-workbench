import {
  AxiosError,
  type AxiosAdapter,
  type AxiosResponse,
  type InternalAxiosRequestConfig,
} from 'axios';
import { getHooksBase } from '../HooksBase';
import type { RootModel } from '../model/root';
import rootReducer from '../reducer/root.reducers';
import rootReducer0 from '../reducer/root0.reducers';
import { getRefreshToken, signal } from './index';
import service from './config';

interface PendingRequest {
  config: InternalAxiosRequestConfig;
  resolve: (response: AxiosResponse) => void;
  reject: (reason: unknown) => void;
}

const now = Date.parse('2026-10-18T00:00:00Z');
const threeHours = 3 * 60 * 60 * 1000;
const tokenForPayload = (payload: unknown) =>
  `Bearer header.${btoa(JSON.stringify(payload))}.signature`;
const tokenExpiringIn = (remaining: number) => tokenForPayload({ exp: (now + remaining) / 1000 });

// Axios dispatches after its request interceptor; let the real interceptor chain run.
const flushRequests = async () => {
  for (let step = 0; step < 8; step++) await Promise.resolve();
};

describe('refresh token request reuse', () => {
  const hooksBase = getHooksBase();
  const originalAdapter = service.defaults.adapter;
  const originalStore = hooksBase.store;
  const originalDispatch = hooksBase.baseDispatch;
  let requests: PendingRequest[];
  let calls: Array<ReturnType<typeof getRefreshToken>>;

  const requestRefresh = () => {
    const result = getRefreshToken();
    calls.push(result);
    return result;
  };

  const complete = (request: PendingRequest, refreshToken?: string) => {
    request.resolve({
      config: request.config,
      status: 200,
      statusText: 'OK',
      headers: refreshToken ? { 'single-ui-refresh': refreshToken } : {},
      data: { result: true },
    });
  };

  beforeEach(() => {
    jest.spyOn(Date, 'now').mockReturnValue(now);
    requests = [];
    calls = [];
    hooksBase.setStore({ token: 'access-token', workspaces: [] });
    hooksBase.setBaseDispatch((action) => {
      const store = rootReducer0(hooksBase.store, action);
      hooksBase.setStore(rootReducer(store, action));
    });
    const adapter: AxiosAdapter = (config) =>
      new Promise<AxiosResponse>((resolve, reject) => {
        requests.push({ config, resolve, reject });
      });
    service.defaults.adapter = adapter;
  });

  afterEach(async () => {
    for (const request of requests) complete(request);
    await Promise.allSettled(calls);
    await flushRequests();
    service.defaults.adapter = originalAdapter;
    hooksBase.setStore(originalStore);
    hooksBase.setBaseDispatch(originalDispatch);
    signal.getRefreshToken = undefined;
    jest.restoreAllMocks();
  });

  it('reuses the existing token while more than three hours remain, checking expiry on each trigger', async () => {
    const refreshToken = tokenExpiringIn(threeHours + 1000);
    hooksBase.store.refreshToken = refreshToken;

    requestRefresh();
    requestRefresh();
    await flushRequests();

    expect(requests).toHaveLength(0);
    expect(hooksBase.store.refreshToken).toBe(refreshToken);

    jest.mocked(Date.now).mockReturnValue(now + 1000);
    requestRefresh();
    await flushRequests();

    expect(requests).toHaveLength(1);
  });

  it.each([
    ['exactly three hours', threeHours],
    ['less than three hours', threeHours - 1000],
    ['expired', -1000],
  ])('requests renewal with %s remaining', async (_description, remaining) => {
    hooksBase.store.refreshToken = tokenExpiringIn(remaining);

    requestRefresh();
    await flushRequests();

    expect(requests).toHaveLength(1);
    expect(requests[0].config.url).toBe('/api/auth/v2/sso/refreshtoken');
    expect(JSON.parse(requests[0].config.data)).toEqual({
      singleUIAuthorization: 'access-token',
    });
  });

  it.each([
    ['missing token', undefined],
    ['malformed token', 'Bearer header.invalid.signature'],
    ['missing expiry', tokenForPayload({})],
    ['null payload', tokenForPayload(null)],
    ['null expiry', tokenForPayload({ exp: null })],
    ['string expiry', tokenForPayload({ exp: String((now + 4 * threeHours) / 1000) })],
    ['non-finite expiry', `Bearer header.${btoa('{"exp":1e309}')}.signature`],
  ])('requests a token when the existing token has %s', async (_description, refreshToken) => {
    hooksBase.store.refreshToken = refreshToken;

    expect(() => requestRefresh()).not.toThrow();
    await flushRequests();

    expect(requests).toHaveLength(1);
  });

  it('shares one pending request across overlapping triggers without aborting it', async () => {
    const first = requestRefresh();
    await flushRequests();
    const firstSignal = requests[0].config.signal;
    const second = requestRefresh();
    const third = requestRefresh();
    await flushRequests();

    expect(first).toBeInstanceOf(Promise);
    expect(second).toBe(first);
    expect(third).toBe(first);
    expect(requests).toHaveLength(1);
    expect(firstSignal?.aborted).toBe(false);

    const refreshToken = tokenExpiringIn(threeHours + 1000);
    complete(requests[0], refreshToken);
    await first;
    requestRefresh();
    await flushRequests();

    expect(hooksBase.store.refreshToken).toBe(refreshToken);
    expect(requests).toHaveLength(1);
  });

  it('allows another request after a successful response without a reusable token', async () => {
    const first = requestRefresh();
    await flushRequests();
    complete(requests[0]);
    await first;

    const second = requestRefresh();
    await flushRequests();

    expect(requests).toHaveLength(2);
    expect(second).not.toBe(first);
  });

  it('allows retry after a failed request', async () => {
    const first = requestRefresh();
    await flushRequests();
    requests[0].reject(new AxiosError('Refresh failed', 'ERR_NETWORK', requests[0].config));
    await first;

    const second = requestRefresh();
    await flushRequests();

    expect(requests).toHaveLength(2);
    expect(second).not.toBe(first);
    expect(requests[1].config.signal?.aborted).toBe(false);
  });

  it('allows immediate retry when a pending request was cancelled', async () => {
    const first = requestRefresh();
    await flushRequests();
    signal.getRefreshToken?.abort();

    const second = requestRefresh();
    await flushRequests();

    expect(requests).toHaveLength(2);
    expect(second).not.toBe(first);
    expect(requests[0].config.signal?.aborted).toBe(true);
    expect(requests[1].config.signal?.aborted).toBe(false);

    complete(requests[0]);
    await first;
    expect(requestRefresh()).toBe(second);
    await flushRequests();
    expect(requests).toHaveLength(2);
  });

  it('replaces an old-access-token request and keeps the newer guard when the old request settles', async () => {
    const first = requestRefresh();
    await flushRequests();
    const nextStore: RootModel = { token: 'next-access-token', workspaces: [] };
    hooksBase.setStore(nextStore);

    const second = requestRefresh();
    await flushRequests();

    expect(requests).toHaveLength(2);
    expect(second).not.toBe(first);
    expect(requests[0].config.signal?.aborted).toBe(true);
    expect(requests[1].config.signal?.aborted).toBe(false);
    expect(JSON.parse(requests[1].config.data)).toEqual({
      singleUIAuthorization: 'next-access-token',
    });

    complete(requests[0], tokenExpiringIn(threeHours + 1000));
    await first;

    expect(hooksBase.store.refreshToken).toBeUndefined();
    expect(requestRefresh()).toBe(second);
    await flushRequests();
    expect(requests).toHaveLength(2);

    const refreshToken = tokenExpiringIn(threeHours + 2000);
    complete(requests[1], refreshToken);
    await second;
    expect(hooksBase.store.refreshToken).toBe(refreshToken);
  });
});
