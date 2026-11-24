import { CanceledError, type AxiosAdapter, type InternalAxiosRequestConfig } from "axios";
import { getHooksBase } from "../HooksBase";
import rootReducer from "../reducer/root.reducers";
import rootReducer0 from "../reducer/root0.reducers";
import service from "./config";
import { invalidateSession } from "../../utils/sessionEpoch";

describe("Shared service cancellation preservation", () => {
  const hooks = getHooksBase();
  const adapter = service.defaults.adapter;
  const store = hooks.store;
  const dispatch = hooks.baseDispatch;
  afterEach(() => { service.defaults.adapter = adapter; hooks.setStore(store); hooks.setBaseDispatch(dispatch); });
  it("[DEL-14] clears the loading state after the final current-session request is canceled", async () => {
    hooks.setStore({ token: "session-a", workspaces: [] });
    hooks.setBaseDispatch(action => {
      hooks.setStore(rootReducer(rootReducer0(hooks.store, action), action));
    });
    let requestConfig: InternalAxiosRequestConfig | undefined;
    const deferred: AxiosAdapter = config => new Promise((_resolve, reject) => {
      requestConfig = config;
      config.signal?.addEventListener?.("abort", () => reject(new CanceledError("User canceled", config)));
    });
    service.defaults.adapter = deferred;
    const controller = new AbortController();
    const result = service.get("/api/portfolio/positions", { signal: controller.signal });
    const rejection = result.catch(error => error);
    for (let step = 0; step < 8; step++) await Promise.resolve();
    expect(requestConfig).toBeDefined();
    expect(hooks.store.isLoading).toBe(true);
    controller.abort();
    await expect(rejection).resolves.toMatchObject({ code: "ERR_CANCELED" });
    expect(hooks.store.token).toBe("session-a");
    expect(hooks.store.errorMsg).toBeUndefined();
    expect(hooks.store.isLoading).toBe(false);
  });

  it("[DEL-19] keeps loading while a replacement request remains pending after cancellation", async () => {
    hooks.setStore({ token: "session-a", workspaces: [] });
    hooks.setBaseDispatch(action => {
      hooks.setStore(rootReducer(rootReducer0(hooks.store, action), action));
    });
    const held: Array<{ config: InternalAxiosRequestConfig; resolve: (value: any) => void }> = [];
    const deferred: AxiosAdapter = config => new Promise((resolve, reject) => {
      held.push({ config, resolve });
      config.signal?.addEventListener?.("abort", () => reject(new CanceledError("User canceled", config)));
    });
    service.defaults.adapter = deferred;
    const controller = new AbortController();
    const first = service.get("/api/portfolio/positions", { signal: controller.signal });
    const firstRejection = first.catch(error => error);
    const replacement = service.get("/api/portfolio/positions?request=replacement");
    try {
      for (let step = 0; step < 8; step++) await Promise.resolve();
      expect(held).toHaveLength(2);
      expect(hooks.store.isLoading).toBe(true);
      controller.abort();
      await expect(firstRejection).resolves.toMatchObject({ code: "ERR_CANCELED" });
      expect(hooks.store.isLoading).toBe(true);
      expect(hooks.store.token).toBe("session-a");
      expect(hooks.store.errorMsg).toBeUndefined();
      held[1].resolve({ config: held[1].config, data: { id: "replacement-position" },
        headers: {}, status: 200, statusText: "OK" });
      await expect(replacement).resolves.toMatchObject({ data: { id: "replacement-position" }, status: 200 });
      expect(hooks.store.isLoading).toBe(false);
    } finally {
      for (const request of held) request.resolve({ config: request.config, data: {},
        headers: {}, status: 200, statusText: "OK" });
      await Promise.allSettled([firstRejection, replacement]);
    }
  });

  it("[DEL-21] keeps loading when a silent request starts and finishes beside pending work", async () => {
    hooks.setStore({ token: "session-a", workspaces: [] });
    hooks.setBaseDispatch(action => {
      hooks.setStore(rootReducer(rootReducer0(hooks.store, action), action));
    });
    const held: Array<{ config: InternalAxiosRequestConfig; resolve: (value: any) => void }> = [];
    service.defaults.adapter = config => new Promise((resolve, reject) => {
      held.push({ config, resolve });
      config.signal?.addEventListener?.("abort", () => reject(new CanceledError("User canceled", config)));
    });
    const controller = new AbortController();
    const first = service.get("/api/portfolio/positions", { signal: controller.signal });
    const firstRejection = first.catch(error => error);
    const silent = service.get("/api/portfolio/positions?request=silent", { headers: { "show-loading": "false" } });
    try {
      for (let step = 0; step < 8; step++) await Promise.resolve();
      expect(held).toHaveLength(2);
      expect(hooks.store.isLoading).toBe(true);
      held[1].resolve({ config: held[1].config, data: { id: "silent-position" },
        headers: {}, status: 200, statusText: "OK" });
      await expect(silent).resolves.toMatchObject({ data: { id: "silent-position" }, status: 200 });
      expect(hooks.store.isLoading).toBe(true);
      controller.abort();
      await expect(firstRejection).resolves.toMatchObject({ code: "ERR_CANCELED" });
      expect(hooks.store.isLoading).toBe(false);
      expect(hooks.store.token).toBe("session-a");
      expect(hooks.store.errorMsg).toBeUndefined();
    } finally {
      for (const request of held) request.resolve({ config: request.config, data: {},
        headers: {}, status: 200, statusText: "OK" });
      await Promise.allSettled([firstRejection, silent]);
    }
  });

  it("[DEL-22] ignores an old cancellation while the new session request remains pending", async () => {
    hooks.setStore({ token: "session-a", workspaces: [] });
    hooks.setBaseDispatch(action => {
      hooks.setStore(rootReducer(rootReducer0(hooks.store, action), action));
    });
    const held: Array<{ config: InternalAxiosRequestConfig; resolve: (value: any) => void }> = [];
    service.defaults.adapter = config => new Promise((resolve, reject) => {
      held.push({ config, resolve });
      config.signal?.addEventListener?.("abort", () => reject(new CanceledError("User canceled", config)));
    });
    const controller = new AbortController();
    const oldRequest = service.get("/api/portfolio/positions", { signal: controller.signal });
    const oldRejection = oldRequest.catch(error => error);
    for (let step = 0; step < 8; step++) await Promise.resolve();
    expect(held).toHaveLength(1);
    expect(hooks.store.isLoading).toBe(true);
    invalidateSession();
    hooks.setStore({ token: "session-b", workspaces: [] });
    const current = service.get("/api/portfolio/positions?request=current-session");
    try {
      for (let step = 0; step < 8; step++) await Promise.resolve();
      expect(held).toHaveLength(2);
      expect(hooks.store.isLoading).toBe(true);
      controller.abort();
      await expect(oldRejection).resolves.toMatchObject({ code: "ERR_CANCELED" });
      expect(hooks.store.isLoading).toBe(true);
      expect(hooks.store.token).toBe("session-b");
      expect(hooks.store.errorMsg).toBeUndefined();
      held[1].resolve({ config: held[1].config, data: { id: "current-position" },
        headers: {}, status: 200, statusText: "OK" });
      await expect(current).resolves.toMatchObject({ data: { id: "current-position" }, status: 200 });
      expect(hooks.store.isLoading).toBe(false);
    } finally {
      for (const request of held) request.resolve({ config: request.config, data: {},
        headers: {}, status: 200, statusText: "OK" });
      await Promise.allSettled([oldRejection, current]);
    }
  });
  it("[DEL-23] clears loading after a response transform fails without request config", async () => {
    hooks.setStore({ token: "session-a", workspaces: [] });
    hooks.setBaseDispatch(action => {
      hooks.setStore(rootReducer(rootReducer0(hooks.store, action), action));
    });
    let requests = 0;
    service.defaults.adapter = async config => {
      requests += 1;
      return { config, data: { id: "position" }, headers: {}, status: 200, statusText: "OK" };
    };
    const failure = service.get("/api/portfolio/positions", {
      transformResponse: [() => { throw new Error("Invalid positions payload"); }],
    });
    expect(hooks.store.isLoading).toBe(true);
    await expect(failure).rejects.toBeDefined();
    expect(hooks.store.errorMsg).toContain("Invalid positions payload");
    expect(hooks.store.isLoading).toBe(false);
    expect(hooks.store.token).toBe("session-a");
    await expect(service.get("/api/portfolio/positions?request=next")).resolves.toMatchObject({
      data: { id: "position" }, status: 200,
    });
    expect(requests).toBe(2);
    expect(hooks.store.isLoading).toBe(false);
  });
  it("[DEL-24] releases completed loading work when response handling throws", async () => {
    hooks.setStore({ token: "session-a", workspaces: [] });
    hooks.setBaseDispatch(action => {
      hooks.setStore(rootReducer(rootReducer0(hooks.store, action), action));
    });
    let requests = 0;
    service.defaults.adapter = async config => {
      requests += 1;
      return { config, data: requests === 1 ? { userInfo: "{" } : { id: "position" },
        headers: {}, status: 200, statusText: "OK" };
    };
    await expect(service.get("/api/auth/v2/sso/validate")).rejects.toThrow(SyntaxError);
    expect(hooks.store.isLoading).toBe(false);
    expect(hooks.store.token).toBe("session-a");
    await expect(service.get("/api/portfolio/positions")).resolves.toMatchObject({
      data: { id: "position" }, status: 200,
    });
    expect(requests).toBe(2);
    expect(hooks.store.isLoading).toBe(false);
  });
});
