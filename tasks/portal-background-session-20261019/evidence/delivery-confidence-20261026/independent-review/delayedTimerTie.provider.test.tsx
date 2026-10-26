import React from 'react';
import { Buffer } from 'buffer';
import type { AxiosAdapter } from 'axios';
import { act, cleanup, render, screen } from '@testing-library/react';
import Provider, { useContext } from '../../../hooks/provider';
import { getHooksBase } from '../../../hooks/HooksBase';
import service from '../../../hooks/service/config';
import { signal } from '../../../hooks/service';
import Timeout from '../../../components/Timeout';
import useController from './useController';

jest.mock('../../../analytics', () => () => ({
  ButtonEvent: jest.fn(), TileEvent: jest.fn(), TabEvent: jest.fn(), ModalEvent: jest.fn(),
}));

const now = Date.parse('2026-10-26T00:00:00Z');
const token = (subject: string, expiresAt: number, issuedAt: number = now) =>
  `Bearer e30.${Buffer.from(JSON.stringify({ sub: subject, iat: issuedAt / 1000, exp: expiresAt / 1000 })).toString('base64')}.fixture`;
const initialAccess = token('session-access', now + 60_000, now - 840_000);
const initialRefresh = token('nearly-expired-refresh', now + 60_000, now - 13_464_000);
const replacementRefresh = token('replacement-refresh', now + 13_524_000);
const originalVisibility = Object.getOwnPropertyDescriptor(document, 'visibilityState');
const Session = () => {
  const { showTimeout, setShowTimeout } = useController();
  return <main>Workspace{showTimeout && <Timeout setOpen={setShowTimeout} />}</main>;
};
const Route = () => {
  const [store] = useContext();
  return store.token ? <Session /> : <div>Signed out</div>;
};

describe('Late acquisition with coincident credential expiry', () => {
  const originalAdapter = service.defaults.adapter;
  let requests: string[];
  beforeEach(() => {
    jest.useFakeTimers();
    jest.setSystemTime(now);
    Object.defineProperty(document, 'visibilityState', { configurable: true, value: 'visible' });
    localStorage.clear(); sessionStorage.clear();
    requests = [];
    const adapter: AxiosAdapter = async (config) => {
      requests.push(config.url ?? '');
      const headers = config.url?.endsWith('/refreshtoken') ? { 'single-ui-refresh': replacementRefresh } : {};
      return { config, data: {}, status: 200, statusText: 'OK', headers };
    };
    service.defaults.adapter = adapter;
  });
  afterEach(() => {
    cleanup();
    signal.getRefreshToken?.abort(); signal.relogin?.abort();
    service.defaults.adapter = originalAdapter;
    jest.clearAllTimers(); jest.useRealTimers();
    if (originalVisibility) Object.defineProperty(document, 'visibilityState', originalVisibility);
    else Reflect.deleteProperty(document, 'visibilityState');
    localStorage.clear(); sessionStorage.clear();
  });
  it('[ADV-M1-COINCIDENT] preserves manual recovery after the acquisition callback runs one millisecond late', async () => {
    render(<Provider data={{ token: initialAccess, refreshToken: initialRefresh,
      expiredIn: (now + 60_000) / 1000, workspaces: [], currentWorkspace: undefined }}><Route /></Provider>);
    await act(async () => undefined);
    const startStore = getHooksBase().store;
    const claims = (value: string) => JSON.parse(Buffer.from(value.split('.')[1], 'base64').toString('utf8'));
    const hash = (value: string) => require('crypto').createHash('sha256').update(value).digest('hex');
    const initial = {
      now: Date.now(), visibility: document.visibilityState,
      requests: [...requests],
      access: { ...claims(startStore.token), sha256: hash(startStore.token) },
      refresh: { ...claims(startStore.refreshToken), sha256: hash(startStore.refreshToken) },
      expiredIn: startStore.expiredIn,
      accessMatchesFixture: startStore.token === initialAccess,
      refreshMatchesFixture: startStore.refreshToken === initialRefresh,
    };
    // A 1ms wall-clock displacement makes the queued pre-expiry callback late.
    jest.setSystemTime(now + 1);
    await act(async () => jest.advanceTimersByTime(35_000));
    const preExpiry = {
      now: Date.now(),
      requests: [...requests],
      refreshToken: getHooksBase().store.refreshToken,
    };
    await act(async () => jest.advanceTimersByTime(25_000));
    const atExpiry = {
      now: Date.now(),
      requests: [...requests],
      isOnLogout: getHooksBase().store.isOnLogout,
      extendEnabled: !screen.queryByRole('button', { name: 'Extend' })?.hasAttribute('disabled'),
    };
    await act(async () => jest.advanceTimersByTime(1000));
    const final = {
      now: Date.now(),
      requests: [...requests],
      token: getHooksBase().store.token,
      refreshToken: getHooksBase().store.refreshToken,
      signedOut: Boolean(screen.queryByText('Signed out')),
      promptVisible: Boolean(screen.queryByRole('dialog')),
    };
    const fs = require('fs');
    fs.writeFileSync(process.env.MFE_REVIEW_OBSERVATION_PATH!, JSON.stringify({
      caseId: 'ADV-M1-COINCIDENT', initial, preExpiry, atExpiry, final,
      expected: { signedOut: false, replacementRefreshAdopted: true, logoutRequests: 0 },
      limits: ['Controlled clocks and immediate Axios adapter responses.', 'One-millisecond clock displacement models callback lateness; it does not measure native timer latency.', 'Equal expiry is seeded. Access and refresh issued lifetimes match the inspected BFF defaults; preceding issuance history remains unobserved.'],
    }, null, 2) + '\n');
    expect(initial.accessMatchesFixture).toBe(true);
    expect(initial.refreshMatchesFixture).toBe(true);
    expect(initial.access.exp).toBe(initial.refresh.exp);
    expect(initial.expiredIn).toBe(initial.access.exp);
    expect(initial.access.exp - initial.access.iat).toBe(900);
    expect(initial.refresh.exp - initial.refresh.iat).toBe(13_524);
    expect(final.signedOut).toBe(false);
    expect(final.refreshToken).toBe(replacementRefresh);
    expect(final.requests.filter((url) => url.endsWith('/logout'))).toHaveLength(0);
    expect(final.promptVisible).toBe(true);
  });
});
