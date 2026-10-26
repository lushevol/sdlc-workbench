import { AxiosError, type AxiosAdapter, type AxiosResponse, type InternalAxiosRequestConfig } from "axios";
import { getHooksBase } from "../HooksBase";
import rootReducer from "../reducer/root.reducers";
import rootReducer0 from "../reducer/root0.reducers";
import { ActionType } from "../reducer/util/ActionType";
import service from "./config";

interface PendingRequest {
  config: InternalAxiosRequestConfig;
  resolve: (response: AxiosResponse) => void;
  reject: (error: AxiosError) => void;
}

const now = Date.parse("2026-10-26T00:00:00Z");
const token = (subject: string, lifetime: number) =>
  `Bearer e30.${btoa(JSON.stringify({ sub: subject, iat: now / 1000, exp: (now + lifetime) / 1000 }))}.test`;
const access = token("session-access", 60_000);
const rotatedAccess = token("rotated-access", 120_000);
const refresh = token("session-refresh", 14_400_000);
const flush = async () => { for (let step = 0; step < 8; step++) await Promise.resolve(); };

// These cases run real Axios interceptors and reducers. The adapter controls only transport.
describe("Shared service compatibility across renewal", () => {
  const hooks = getHooksBase();
  const originalAdapter = service.defaults.adapter;
  const originalStore = hooks.store;
  const originalDispatch = hooks.baseDispatch;
  let pending: PendingRequest[];
  let calls: Array<Promise<unknown>>;

  const start = (url: string) => {
    const request = service.get(url);
    // Attach rejection handling immediately; cases still assert the original promise.
    calls.push(request.catch(() => undefined));
    return request;
  };
  const succeed = (request: PendingRequest, data: unknown, headers = {}) => {
    request.resolve({ config: request.config, data, headers, status: 200, statusText: "OK" });
  };
  const fail = (request: PendingRequest, message: string) => {
    request.reject(new AxiosError("Request failed with status code 401", "ERR_BAD_REQUEST", request.config,
      undefined, { config: request.config, data: { errorMessage: message }, headers: {}, status: 401,
        statusText: "Unauthorized" }));
  };

  beforeEach(() => {
    jest.spyOn(Date, "now").mockReturnValue(now);
    localStorage.clear(); sessionStorage.clear();
    pending = []; calls = [];
    hooks.setStore({ token: access, refreshToken: refresh, expiredIn: (now + 60_000) / 1000,
      user: { sub: "operator-a", userId: "operator-a" }, workspaces: [] });
    hooks.setBaseDispatch((action) => {
      const next = rootReducer0(hooks.store, action);
      hooks.setStore(rootReducer(next, action));
    });
    const adapter: AxiosAdapter = (config) => new Promise<AxiosResponse>((resolve, reject) =>
      pending.push({ config, resolve, reject }));
    service.defaults.adapter = adapter;
  });

  afterEach(async () => {
    for (const request of pending) succeed(request, {});
    await Promise.allSettled(calls);
    service.defaults.adapter = originalAdapter;
    hooks.setStore(originalStore);
    hooks.setBaseDispatch(originalDispatch);
    localStorage.clear(); sessionStorage.clear();
    jest.restoreAllMocks();
  });

  it("[DEL-09] preserves protected-request credentials and response data", async () => {
    const response = start("/api/portfolio/positions");
    await flush();
    expect(pending[0].config.headers["Single-UI-Authorization"]).toBe(access);
    expect(pending[0].config.headers["userId"]).toBe("operator-a");
    expect(pending[0].config.headers["Content-Type"]).toBe("application/json");
    const data = { positions: [{ id: "position-a", amount: 17 }] };
    succeed(pending[0], data);
    await expect(response).resolves.toMatchObject({ data, status: 200 });
    expect(hooks.store.token).toBe(access);
    expect(hooks.store.refreshToken).toBe(refresh);
    expect(hooks.store.isLoading).toBe(false);
  });

  it("[DEL-10] accepts pending protected responses after same-session access rotation", async () => {
    const response = start("/api/portfolio/positions");
    await flush();
    const rotation = service.post("/api/auth/v2/sso/extend", { singleUIAuthorization: access });
    calls.push(rotation.catch(() => undefined));
    await flush();
    succeed(pending[1], {}, { "single-ui-authorization": rotatedAccess });
    await rotation;
    expect(hooks.store.token).toBe(rotatedAccess);
    expect(hooks.store.refreshToken).toBe(refresh);
    succeed(pending[0], { id: "position-a" });
    await expect(response).resolves.toMatchObject({ data: { id: "position-a" }, status: 200 });
    expect(hooks.store.token).toBe(rotatedAccess);
    expect(hooks.store.refreshToken).toBe(refresh);
  });

  it("[DEL-11] preserves ordinary current-session service error reporting", async () => {
    const response = start("/api/portfolio/positions");
    await flush();
    fail(pending[0], "Position data unavailable");
    await expect(response).rejects.toMatchObject({ response: { status: 401 } });
    expect(hooks.store.errorMsg).toBe("Position data unavailable");
    expect(hooks.store.token).toBe(access);
    expect(hooks.store.refreshToken).toBe(refresh);
    expect(hooks.store.isLoading).toBe(false);
  });

  it("[DEL-12] preserves current-session invalidation for expired protected access", async () => {
    localStorage.setItem("SET_TOKEN", access);
    const response = start("/api/portfolio/positions");
    await flush();
    fail(pending[0], "TOKEN_INVALID_EXPIRED");
    await expect(response).rejects.toMatchObject({ response: { status: 401 } });
    expect(hooks.store.token).toBeUndefined();
    expect(hooks.store.refreshToken).toBeUndefined();
    expect(localStorage.getItem("SET_TOKEN")).toBeNull();
    expect(hooks.store.errorMsg).toBe("Expired Session, please login again.");
  });

  it.each(["/api/analytics/event", "/api/sse/events", "/api/auth/v2/sso/logout"])(
    "[DEL-13] preserves ignored error behavior for %s", async (url) => {
      hooks.baseDispatch({ type: ActionType.SET_ERRORMSG, data: { errorMsg: "Existing notice" } });
      const response = start(url);
      await flush();
      fail(pending[0], "TOKEN_INVALID_EXPIRED");
      await expect(response).rejects.toMatchObject({ response: { status: 401 } });
      expect(hooks.store.token).toBe(access);
      expect(hooks.store.refreshToken).toBe(refresh);
      expect(hooks.store.errorMsg).toBe("Existing notice");
      expect(hooks.store.isLoading).toBe(false);
    }
  );
});
