import { CanceledError, type AxiosAdapter, type InternalAxiosRequestConfig } from "axios";
import { getHooksBase } from "../HooksBase";
import rootReducer from "../reducer/root.reducers";
import rootReducer0 from "../reducer/root0.reducers";
import service from "./config";

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
});
