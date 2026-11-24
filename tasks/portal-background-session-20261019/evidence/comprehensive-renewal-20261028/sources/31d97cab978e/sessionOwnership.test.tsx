import React from "react";
import { Buffer } from "buffer";
import {
  AxiosError,
  type AxiosAdapter,
  type AxiosResponse,
  type InternalAxiosRequestConfig,
} from "axios";
import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";
import Provider, { useContext } from "../../../hooks/provider";
import { getHooksBase } from "../../../hooks/HooksBase";
import service from "../../../hooks/service/config";
import { getRefreshToken, signal } from "../../../hooks/service";
import useServices from "../../../services";
import useController from "./useController";

jest.mock("../../../analytics", () => () => ({
  ButtonEvent: jest.fn(),
  TileEvent: jest.fn(),
  TabEvent: jest.fn(),
  ModalEvent: jest.fn(),
}));

interface PendingRequest {
  config: InternalAxiosRequestConfig;
  resolve: (response: AxiosResponse) => void;
  reject: (error: AxiosError) => void;
}

const now = Date.parse("2026-10-25T00:00:00Z");
const minute = 60_000;
const token = (subject: string, remaining: number) =>
  `Bearer e30.${Buffer.from(
    JSON.stringify({ sub: subject, iat: now / 1000, exp: (now + remaining) / 1000 })
  ).toString("base64")}.test-signature`;
const initialAccess = token("old-session-access", 15 * minute);
const initialRefresh = token("old-session-refresh", 1000);
const oldRefreshResponse = token("late-old-session-refresh", 4 * 60 * minute);
const nextAccess = token("new-session-access", 20 * minute);
const rotatedAccess = token("same-session-rotated-access", 20 * minute);
const originalAdapter = service.defaults.adapter;
const originalVisibility = Object.getOwnPropertyDescriptor(document, "visibilityState");

const HomeSession = () => {
  useController();
  return <div>Session workspace</div>;
};

const SessionFixture = () => {
  const [store] = useContext();
  const { login, loginEntra, logout } = useServices();
  return (
    <>
      {store.token ? <HomeSession /> : <div>Signed out</div>}
      <button onClick={logout}>Logout</button>
      <button onClick={() => login({ code: "new-session" })}>Sign in</button>
      <button onClick={() => loginEntra({ code: "entra-session" })}>Entra sign in</button>
    </>
  );
};

describe("Session ownership across logout and fresh login", () => {
  let pending: PendingRequest[];
  let requests: InternalAxiosRequestConfig[];
  let calls: Array<Promise<unknown> | void>;

  const requestsTo = (endpoint: string) =>
    requests.filter(({ url }) => url === `/api/auth/v2/sso/${endpoint}`);
  const pendingTo = (endpoint: string) =>
    pending.filter(({ config }) => config.url === `/api/auth/v2/sso/${endpoint}`);

  const finish = async (request: PendingRequest, headers: Record<string, string>) => {
    await act(async () => {
      request.resolve({
        config: request.config,
        data: {},
        headers,
        status: 200,
        statusText: "OK",
      });
    });
  };

  const failExpired = async (request: PendingRequest) => {
    await act(async () => {
      request.reject(new AxiosError(
        "Request failed with status code 401",
        "ERR_BAD_REQUEST",
        request.config,
        undefined,
        {
          config: request.config,
          data: { errorMessage: "TOKEN_INVALID_EXPIRED" },
          headers: {},
          status: 401,
          statusText: "Unauthorized",
        }
      ));
    });
  };

  const logout = async () => {
    await act(async () => fireEvent.click(screen.getByRole("button", { name: "Logout" })));
    expect(getHooksBase().store.token).toBeUndefined();
  };

  const startLogin = async () => {
    await act(async () => fireEvent.click(screen.getByRole("button", { name: "Sign in" })));
    return pendingTo("login")[0];
  };

  const completeLogin = async () => {
    await finish(await startLogin(), { "single-ui-authorization": nextAccess });
    expect(getHooksBase().store.token).toBe(nextAccess);
  };

  const renderSession = async (startAutomaticRefresh = true) => {
    render(
      <Provider data={{
        token: initialAccess,
        refreshToken: initialRefresh,
        expiredIn: (now + 15 * minute) / 1000,
        workspaces: [],
        currentWorkspace: undefined,
      }}>
        <SessionFixture />
      </Provider>
    );
    await act(async () => undefined);
    if (startAutomaticRefresh) {
      await act(async () => jest.advanceTimersByTime(1000));
      expect(requestsTo("refreshtoken")).toHaveLength(1);
      expect(JSON.parse(requestsTo("refreshtoken")[0].data)).toEqual({
        singleUIAuthorization: initialAccess,
      });
    }
  };

  beforeEach(() => {
    jest.useFakeTimers();
    jest.setSystemTime(now);
    Object.defineProperty(document, "visibilityState", {
      configurable: true,
      value: "visible",
    });
    localStorage.clear();
    sessionStorage.clear();
    pending = [];
    requests = [];
    calls = [];
    const adapter: AxiosAdapter = (config) => {
      requests.push(config);
      if (
        config.url === "/api/auth/v2/sso/refreshtoken" ||
        config.url === "/api/auth/v2/sso/login" ||
        config.url === "/api/auth/v3/sso/login"
      ) {
        return new Promise<AxiosResponse>((resolve, reject) => {
          pending.push({ config, resolve, reject });
        });
      }
      return Promise.resolve({
        config,
        data: {},
        headers: config.url?.endsWith("/extend")
          ? { "single-ui-authorization": rotatedAccess }
          : {},
        status: 200,
        statusText: "OK",
      });
    };
    service.defaults.adapter = adapter;
  });

  afterEach(async () => {
    await act(async () => {
      for (const request of pending) request.resolve({
        config: request.config,
        data: {},
        headers: {},
        status: 200,
        statusText: "OK",
      });
      await Promise.allSettled(calls);
    });
    cleanup();
    service.defaults.adapter = originalAdapter;
    signal.getRefreshToken?.abort();
    signal.getRefreshToken = undefined;
    jest.clearAllTimers();
    jest.useRealTimers();
    if (originalVisibility) {
      Object.defineProperty(document, "visibilityState", originalVisibility);
    } else {
      Reflect.deleteProperty(document, "visibilityState");
    }
    localStorage.clear();
    sessionStorage.clear();
  });

  it("[OWN-01] discards automatic refresh success delivered after logout and before new login", async () => {
    await renderSession();
    await logout();
    await finish(pendingTo("refreshtoken")[0], { "single-ui-refresh": oldRefreshResponse });
    expect(getHooksBase().store.refreshToken).toBeUndefined();
    await completeLogin();
    expect(getHooksBase().store.refreshToken).toBeUndefined();
  });

  it("[OWN-02] discards automatic refresh success delivered after a new login", async () => {
    await renderSession();
    await logout();
    await completeLogin();
    await finish(pendingTo("refreshtoken")[0], { "single-ui-refresh": oldRefreshResponse });
    expect(getHooksBase().store.token).toBe(nextAccess);
    expect(getHooksBase().store.refreshToken).toBeUndefined();
  });

  it("[OWN-03] discards automatic refresh invalid-token errors delivered after a new login", async () => {
    await renderSession();
    await logout();
    await completeLogin();
    await failExpired(pendingTo("refreshtoken")[0]);
    expect(getHooksBase().store.token).toBe(nextAccess);
    expect(getHooksBase().store.errorMsg).toBeUndefined();
  });

  it.each([
    ["OWN-04", "success"],
    ["OWN-05", "error"],
  ])(
    "[%s] discards refresh %s started while fresh login was pending",
    async (_id, outcome) => {
      await renderSession();
      expect(getHooksBase().store.refreshToken).toBe(initialRefresh);
      const login = await startLogin();
      // Check the reset before either login or the held refresh can complete.
      expect(getHooksBase().store.refreshToken).toBeUndefined();
      calls.push(service.post("/api/auth/v2/sso/refreshtoken", {
        singleUIAuthorization: initialAccess,
      }).catch(() => undefined));
      await act(async () => undefined);
      expect(pendingTo("refreshtoken")).toHaveLength(2);
      const duringLogin = pendingTo("refreshtoken")[1];
      await finish(login, { "single-ui-authorization": nextAccess });
      if (outcome === "success") {
        await finish(duringLogin, { "single-ui-refresh": oldRefreshResponse });
      } else {
        await failExpired(duringLogin);
      }
      expect(getHooksBase().store.token).toBe(nextAccess);
      expect(getHooksBase().store.refreshToken).toBeUndefined();
      expect(getHooksBase().store.errorMsg).toBeUndefined();
    }
  );

  it("[OWN-06] accepts automatic refresh success after access rotates within the same session", async () => {
    await renderSession();
    await act(async () => {
      await service.post("/api/auth/v2/sso/extend", { singleUIAuthorization: initialAccess });
    });
    expect(getHooksBase().store.token).toBe(rotatedAccess);
    await finish(pendingTo("refreshtoken")[0], { "single-ui-refresh": oldRefreshResponse });
    expect(getHooksBase().store.token).toBe(rotatedAccess);
    expect(getHooksBase().store.refreshToken).toBe(oldRefreshResponse);
  });

  it("[OWN-07] still clears authentication after a current-session invalid-token error", async () => {
    await renderSession();
    await failExpired(pendingTo("refreshtoken")[0]);
    expect(getHooksBase().store.token).toBeUndefined();
    expect(getHooksBase().store.refreshToken).toBeUndefined();
    expect(getHooksBase().store.errorMsg).toBe("Expired Session, please login again.");
  });

  it("[OWN-08] captures refresh ownership before logout without yielding to Axios", async () => {
    await renderSession(false);
    await act(async () => {
      calls.push(getRefreshToken());
      fireEvent.click(screen.getByRole("button", { name: "Logout" }));
    });
    expect(pendingTo("refreshtoken")).toHaveLength(1);
    await finish(pendingTo("refreshtoken")[0], { "single-ui-refresh": oldRefreshResponse });
    expect(getHooksBase().store.token).toBeUndefined();
    expect(getHooksBase().store.refreshToken).toBeUndefined();
  });

  it("[OWN-09] replaces a prior pending refresh after fresh login starts with the same stored access", async () => {
    await renderSession();
    await startLogin();
    calls.push(getRefreshToken());
    await act(async () => undefined);
    expect(pendingTo("refreshtoken")).toHaveLength(2);
    expect(pendingTo("refreshtoken")[0].config.signal?.aborted).toBe(true);
    expect(pendingTo("refreshtoken")[1].config.signal?.aborted).toBe(false);
    expect(getHooksBase().store.refreshToken).toBeUndefined();
  });

  it("[DEL-01] clears prior refresh immediately when Entra login starts", async () => {
    await renderSession(false);
    expect(getHooksBase().store.refreshToken).toBe(initialRefresh);
    await act(async () => fireEvent.click(screen.getByRole("button", { name: "Entra sign in" })));
    const login = pending.find(({ config }) => config.url === "/api/auth/v3/sso/login");
    expect(login).toBeDefined();
    expect(getHooksBase().store.refreshToken).toBeUndefined();
    expect(getHooksBase().store.token).toBe(initialAccess);
    await finish(login!, { "single-ui-authorization": nextAccess });
    expect(getHooksBase().store.token).toBe(nextAccess);
    expect(getHooksBase().store.refreshToken).toBeUndefined();
  });

  it.each([
    ["DEL-02", "success"],
    ["DEL-03", "error"],
  ])("[%s] preserves the newest of two fresh logins after old %s", async (_id, outcome) => {
    await renderSession(false);
    const olderLogin = await startLogin();
    await startLogin();
    const newerLogin = pendingTo("login")[1];
    expect(pendingTo("login")).toHaveLength(2);
    await finish(newerLogin, { "single-ui-authorization": nextAccess });
    if (outcome === "success") {
      await finish(olderLogin, { "single-ui-authorization": initialAccess });
    } else {
      await failExpired(olderLogin);
    }
    expect(getHooksBase().store.token).toBe(nextAccess);
    expect(getHooksBase().store.expiredIn).toBe((now + 20 * minute) / 1000);
    expect(localStorage.getItem("SET_TOKEN")).toBe(nextAccess);
    expect(getHooksBase().store.refreshToken).toBeUndefined();
    expect(getHooksBase().store.errorMsg).toBeUndefined();
  });
});
