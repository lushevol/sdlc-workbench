import React from "react";
import { Buffer } from "buffer";
import { AxiosError, type AxiosAdapter, type AxiosResponse, type InternalAxiosRequestConfig } from "axios";
import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";
import Provider, { useContext } from "../../../hooks/provider";
import { getHooksBase } from "../../../hooks/HooksBase";
import { signal } from "../../../hooks/service";
import service from "../../../hooks/service/config";
import { signal as extendSignal } from "../../../hooks/service/util/extend";
import useServices from "../../../services";
import Timeout from "../../../components/Timeout";
import useController from "./useController";

jest.mock("../../../analytics", () => () => ({
  ButtonEvent: jest.fn(), TileEvent: jest.fn(), TabEvent: jest.fn(), ModalEvent: jest.fn(),
}));

interface PendingRequest {
  config: InternalAxiosRequestConfig;
  resolve: (response: AxiosResponse) => void;
  reject: (error: AxiosError) => void;
}

const now = Date.parse("2026-10-25T00:00:00Z");
const minute = 60_000;
const accessLifetime = 30_000;
const refreshLead = 25_000;
const jwt = (payload: unknown) =>
  `Bearer e30.${Buffer.from(JSON.stringify(payload)).toString("base64")}.test-signature`;
const token = (subject: string, expiresAt: number, issuedAt = now) =>
  jwt({ sub: subject, iat: issuedAt / 1000, exp: expiresAt / 1000 });
const originalAccess = token("initial-access", now + accessLifetime);
const refreshToken = token("initial-refresh", now + 4 * 60 * minute);
const renewedAccess = token("renewed-access", now + 20 * minute, now + accessLifetime);
const newLoginAccess = token("replacement-login", now + 25 * minute, now + accessLifetime);
const originalAdapter = service.defaults.adapter;
const originalVisibility = Object.getOwnPropertyDescriptor(document, "visibilityState");

const Session = ({ onClose }: { onClose: () => void }) => {
  const { showTimeout, setShowTimeout } = useController();
  return (
    <main data-testid="session-workspace">
      Session workspace
      {showTimeout && <Timeout setOpen={(open) => {
        if (!open) onClose();
        setShowTimeout(open);
      }} />}
    </main>
  );
};

const SessionRoute = ({ onClose }: { onClose: () => void }) => {
  const [store] = useContext();
  const { login } = useServices();
  return <>
    {store.token ? <Session onClose={onClose} /> : <div>Signed out</div>}
    <button data-testid="replacement-login" onClick={() => login({ code: "replacement-login" })}>
      Replacement sign-in callback
    </button>
  </>;
};

describe("Pending session renewal and recovery", () => {
  let pending: PendingRequest[];
  let requests: InternalAxiosRequestConfig[];
  let closeTransitions: jest.Mock;

  const requestsTo = (endpoint: string) =>
    requests.filter(({ url }) => url === `/api/auth/v2/sso/${endpoint}`);
  const pendingTo = (endpoint: string) =>
    pending.filter(({ config }) => config.url === `/api/auth/v2/sso/${endpoint}`);
  const advance = async (elapsed: number) => {
    await act(async () => jest.advanceTimersByTime(elapsed));
  };
  const click = async (name: string) => {
    await act(async () => fireEvent.click(screen.getByRole("button", { name })));
  };
  const finish = async (request: PendingRequest, headers: Record<string, string>) => {
    await act(async () => request.resolve({
      config: request.config, data: {}, headers, status: 200, statusText: "OK",
    }));
  };
  const rejectRetryable = async (request: PendingRequest) => {
    await act(async () => request.reject(new AxiosError(
      "Request failed with status code 503", "ERR_BAD_RESPONSE", request.config, undefined,
      { config: request.config, data: { errorMessage: "Temporary authentication failure" },
        headers: {}, status: 503, statusText: "Unavailable" }
    )));
  };
  const renderSession = async (withRefresh = true) => {
    render(<Provider data={{ token: originalAccess, expiredIn: (now + accessLifetime) / 1000,
      refreshToken: withRefresh ? refreshToken : undefined, workspaces: [], currentWorkspace: undefined }}>
      <SessionRoute onClose={closeTransitions} />
    </Provider>);
    await act(async () => undefined);
  };
  const openPrompt = async () => {
    await renderSession();
    await advance(accessLifetime);
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Extend" })).toBeEnabled();
  };
  const openPromptWithPendingAcquisition = async () => {
    await renderSession(false);
    await advance(accessLifetime - refreshLead);
    expect(pendingTo("refreshtoken")).toHaveLength(1);
    expect(JSON.parse(pendingTo("refreshtoken")[0].config.data)).toEqual({ singleUIAuthorization: originalAccess });
    await advance(refreshLead);
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    return pendingTo("refreshtoken")[0];
  };
  const expectSuccessfulRenewal = () => {
    expect(getHooksBase().store.token).toBe(renewedAccess);
    expect(getHooksBase().store.expiredIn).toBe((now + 20 * minute) / 1000);
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(closeTransitions).toHaveBeenCalledTimes(1);
  };

  beforeEach(() => {
    jest.useFakeTimers();
    jest.setSystemTime(now);
    Object.defineProperty(document, "visibilityState", { configurable: true, value: "visible" });
    localStorage.clear(); sessionStorage.clear();
    pending = []; requests = []; closeTransitions = jest.fn();
    const adapter: AxiosAdapter = (config) => {
      requests.push(config);
      if (["/api/auth/v2/sso/refreshtoken", "/api/auth/v2/sso/relogin", "/api/auth/v2/sso/login"].includes(config.url ?? "")) {
        return new Promise<AxiosResponse>((resolve, reject) => pending.push({ config, resolve, reject }));
      }
      return Promise.resolve({ config, data: {}, headers: {}, status: 200, statusText: "OK" });
    };
    service.defaults.adapter = adapter;
  });

  afterEach(async () => {
    await act(async () => {
      for (const request of pending) request.resolve({ config: request.config, data: {}, headers: {}, status: 200, statusText: "OK" });
    });
    cleanup();
    signal.getRefreshToken?.abort(); signal.relogin?.abort(); extendSignal.extendToken?.abort();
    signal.getRefreshToken = undefined; signal.relogin = undefined; extendSignal.extendToken = undefined;
    service.defaults.adapter = originalAdapter;
    jest.clearAllTimers(); jest.useRealTimers();
    if (originalVisibility) Object.defineProperty(document, "visibilityState", originalVisibility);
    else Reflect.deleteProperty(document, "visibilityState");
    localStorage.clear(); sessionStorage.clear();
  });

  it("[PEND-01] keeps the prompt open during manual renewal and closes once after valid access arrives", async () => {
    await openPrompt();
    await click("Extend");
    expect(requestsTo("relogin")).toHaveLength(1);
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    expect(closeTransitions).not.toHaveBeenCalled();
    expect(getHooksBase().store.token).toBe(originalAccess);
    await finish(pendingTo("relogin")[0], { "single-ui-authorization": renewedAccess });
    expectSuccessfulRenewal();
    await act(async () => undefined);
    expect(closeTransitions).toHaveBeenCalledTimes(1);
  });

  it("[PEND-02] keeps the prompt open after retryable failure and completes a second attempt", async () => {
    await openPrompt();
    await click("Extend");
    await rejectRetryable(pendingTo("relogin")[0]);
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    expect(closeTransitions).not.toHaveBeenCalled();
    expect(screen.getByRole("button", { name: "Extend" })).toBeEnabled();
    expect(getHooksBase().store.token).toBe(originalAccess);
    await click("Extend");
    expect(requestsTo("relogin")).toHaveLength(2);
    await finish(pendingTo("relogin")[1], { "single-ui-authorization": renewedAccess });
    expectSuccessfulRenewal();
  });

  it.each([
    ["PEND-03", "missing", undefined],
    ["PEND-04", "malformed", "not-a-jwt"],
    ["PEND-05", "expired", token("expired-access", now + accessLifetime)],
    ["PEND-06", "missing iat", jwt({ sub: "missing-iat", exp: (now + 20 * minute) / 1000 })],
  ])("[%s] rejects %s access before store mutation and allows retry", async (_id, _description, returnedAccess) => {
    await openPrompt();
    await click("Extend");
    await finish(pendingTo("relogin")[0], returnedAccess ? { "single-ui-authorization": returnedAccess } : {});
    expect(getHooksBase().store.token).toBe(originalAccess);
    expect(getHooksBase().store.expiredIn).toBe((now + accessLifetime) / 1000);
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    expect(closeTransitions).not.toHaveBeenCalled();
    expect(screen.getByRole("button", { name: "Extend" })).toBeEnabled();
    await click("Extend");
    await finish(pendingTo("relogin")[1], { "single-ui-authorization": renewedAccess });
    expectSuccessfulRenewal();
  });

  it("[PEND-07] sends only one relogin for rapid repeated Extend clicks", async () => {
    await openPrompt();
    const button = screen.getByRole("button", { name: "Extend" });
    await act(async () => { fireEvent.click(button); fireEvent.click(button); fireEvent.click(button); });
    expect(requestsTo("relogin")).toHaveLength(1);
    expect(closeTransitions).not.toHaveBeenCalled();
    await finish(pendingTo("relogin")[0], { "single-ui-authorization": renewedAccess });
    expectSuccessfulRenewal();
  });

  it("[PEND-08] permits Logout during pending manual renewal and cancels the held relogin", async () => {
    await openPrompt();
    await click("Extend");
    const renewal = pendingTo("relogin")[0];
    expect(screen.getByRole("button", { name: "Logout" })).toBeEnabled();
    await click("Logout");
    expect(renewal.config.signal?.aborted).toBe(true);
    await advance(1000);
    expect(requestsTo("logout")).toHaveLength(1);
    expect(getHooksBase().store.token).toBeUndefined();
    await finish(renewal, { "single-ui-authorization": renewedAccess });
    expect(getHooksBase().store.token).toBeUndefined();
    expect(closeTransitions).toHaveBeenCalledTimes(1);
  });

  it("[PEND-09] waits for scheduled acquisition across access expiry then permits explicit recovery", async () => {
    const acquisition = await openPromptWithPendingAcquisition();
    expect(getHooksBase().store.isOnLogout).toBe(false);
    expect(screen.getByRole("button", { name: "Extend" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Logout" })).toBeEnabled();
    await advance(1001);
    expect(requestsTo("logout")).toHaveLength(0);
    expect(getHooksBase().store.token).toBe(originalAccess);
    await finish(acquisition, { "single-ui-refresh": refreshToken });
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Extend" })).toBeEnabled();
    expect(requestsTo("relogin")).toHaveLength(0);
    await click("Extend");
    expect(closeTransitions).not.toHaveBeenCalled();
    await finish(pendingTo("relogin")[0], { "single-ui-authorization": renewedAccess });
    expectSuccessfulRenewal();
  });

  it("[PEND-10] prevents an old delayed Logout callback from clearing a newer login", async () => {
    await openPrompt();
    await click("Logout");
    await act(async () => fireEvent.click(screen.getByTestId("replacement-login")));
    await finish(pendingTo("login")[0], { "single-ui-authorization": newLoginAccess });
    expect(getHooksBase().store.token).toBe(newLoginAccess);
    await advance(1000);
    expect(requestsTo("logout")).toHaveLength(0);
    expect(getHooksBase().store.token).toBe(newLoginAccess);
    expect(localStorage.getItem("SET_TOKEN")).toBe(newLoginAccess);
    expect(closeTransitions).not.toHaveBeenCalled();
  });

  it("[PEND-11] permits Logout during pending acquisition and discards its later delivery", async () => {
    const acquisition = await openPromptWithPendingAcquisition();
    expect(screen.getByRole("button", { name: "Logout" })).toBeEnabled();
    await click("Logout");
    expect(acquisition.config.signal?.aborted).toBe(true);
    await advance(1000);
    expect(getHooksBase().store.token).toBeUndefined();
    await finish(acquisition, { "single-ui-refresh": refreshToken });
    expect(getHooksBase().store.token).toBeUndefined();
    expect(getHooksBase().store.refreshToken).toBeUndefined();
    expect(requestsTo("logout")).toHaveLength(1);
    expect(closeTransitions).toHaveBeenCalledTimes(1);
  });

  it("[PEND-12] rejects a stale rendered Extend control after the refresh cutoff passes without timer delivery", async () => {
    await openPrompt();
    const button = screen.getByRole("button", { name: "Extend" });
    expect(button).toBeEnabled();
    jest.setSystemTime(now + 4 * 60 * minute - 1000);
    await act(async () => fireEvent.click(button));
    expect(requestsTo("relogin")).toHaveLength(0);
    expect(closeTransitions).not.toHaveBeenCalled();
    expect(getHooksBase().store.token).toBe(originalAccess);
  });

  it("[PEND-13] settles failed pending acquisition and applies the existing logout fallback", async () => {
    const acquisition = await openPromptWithPendingAcquisition();
    await rejectRetryable(acquisition);
    await advance(1000);
    expect(requestsTo("relogin")).toHaveLength(0);
    expect(requestsTo("logout")).toHaveLength(1);
    expect(getHooksBase().store.token).toBeUndefined();
    expect(getHooksBase().store.refreshToken).toBeUndefined();
    expect(closeTransitions).toHaveBeenCalledTimes(1);
  });
});
