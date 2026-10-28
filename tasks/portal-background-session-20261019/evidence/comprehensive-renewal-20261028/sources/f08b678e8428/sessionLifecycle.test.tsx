import React from "react";
import { Buffer } from "buffer";
import type { AxiosAdapter, InternalAxiosRequestConfig } from "axios";
import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";
import { it } from "@jest/globals";
import Provider, { useContext } from "../../../hooks/provider";
import { getHooksBase } from "../../../hooks/HooksBase";
import type { RootModel } from "../../../hooks/model/root";
import { ActionType } from "../../../hooks/reducer/util/ActionType";
import service from "../../../hooks/service/config";
import { signal as sessionSignals } from "../../../hooks/service";
import { signal as extendSignal } from "../../../hooks/service/util/extend";
import useServices from "../../../services";
import Timeout from "../../../components/Timeout";
import useController from "./useController";

jest.mock("../../../analytics", () => () => ({
  ButtonEvent: jest.fn(),
  TileEvent: jest.fn(),
  TabEvent: jest.fn(),
  ModalEvent: jest.fn(),
}));

const minute = 60_000;
const accessLifetime = 15 * minute;
const refreshLead = 25_000;
// The tests use the server-provided exp, including a four-hour refresh fixture.
// They do not assert that production configuration issues this lifetime.
const refreshLifetime = 4 * 60 * minute;
const serverRefreshLifetime = 225 * minute + 24_000;
const now = Date.parse("2026-09-21T00:00:00Z");
const originalAdapter = service.defaults.adapter;
const originalVisibility = Object.getOwnPropertyDescriptor(
  document,
  "visibilityState"
);

const token = (subject: string, expiresAt: number, issuedAt = now) =>
  `Bearer e30.${Buffer.from(
    JSON.stringify({ sub: subject, iat: issuedAt / 1000, exp: expiresAt / 1000 })
  ).toString("base64")}.test-signature`;

const setVisibility = (visibility: DocumentVisibilityState) => {
  Object.defineProperty(document, "visibilityState", {
    configurable: true,
    value: visibility,
  });
  document.dispatchEvent(new Event("visibilitychange"));
};

// Exercise the real session controller and dialog together without rendering
// unrelated workspaces, FDC3 connections or micro-frontends.
const Session = () => {
  const { mouseMove, showTimeout, setShowTimeout } = useController();
  return (
    <main data-testid="session-workspace" onMouseMove={mouseMove}>
      Session workspace
      {showTimeout && <Timeout setOpen={setShowTimeout} />}
    </main>
  );
};

const SessionRoute = () => {
  const [store] = useContext();
  const { login } = useServices();
  return store.token ? (
    <Session />
  ) : (
    <button onClick={() => login({ code: "new-login-code" })}>Sign in</button>
  );
};

describe("Session lifecycle across browser minimize and return", () => {
  let requests: InternalAxiosRequestConfig[];
  let responseAccessToken: string;
  let responseRefreshToken: string;

  const requestsTo = (endpoint: string) =>
    requests.filter(({ url }) => url === `/api/auth/v2/sso/${endpoint}`);

  const renderSession = async (data: RootModel = {}) => {
    render(
      <Provider
        data={{
          token: token("initial-access", now + accessLifetime),
          expiredIn: (now + accessLifetime) / 1000,
          workspaces: [],
          currentWorkspace: undefined,
          ...data,
        }}
      >
        <SessionRoute />
      </Provider>
    );
    await act(async () => undefined);
  };

  const returnAfterSuspension = async (elapsed: number) => {
    await act(async () => {
      setVisibility("hidden");
    });
    await act(async () => {
      // A frozen browser does not run its timers. Jumping wall-clock time
      // after the hide request completes preserves that distinction from
      // a background tab whose timers run.
      jest.setSystemTime(now + elapsed);
      setVisibility("visible");
    });
  };

  const advanceTime = async (elapsed: number) => {
    await act(async () => {
      jest.advanceTimersByTime(elapsed);
    });
  };

  const continueWorking = async () => {
    fireEvent.mouseMove(screen.getByTestId("session-workspace"));
    await advanceTime(5000);
  };

  beforeEach(() => {
    jest.useFakeTimers();
    jest.setSystemTime(now);
    setVisibility("visible");
    localStorage.clear();
    sessionStorage.clear();
    requests = [];
    responseAccessToken = token("renewed-access", now + 25 * minute);
    responseRefreshToken = token("initial-refresh", now + refreshLifetime);
    const adapter: AxiosAdapter = async (config) => {
      requests.push(config);
      const headers: Record<string, string> = {};
      switch (config.url) {
        case "/api/auth/v2/sso/refreshtoken":
          headers["single-ui-refresh"] = responseRefreshToken;
          break;
        case "/api/auth/v2/sso/extend":
        case "/api/auth/v2/sso/relogin":
        case "/api/auth/v2/sso/login":
          headers["single-ui-authorization"] = responseAccessToken;
          break;
        case "/api/auth/v2/sso/logout":
        case "/api/ssiplus/imeta/logout":
          break;
        default:
          throw new Error(`Unexpected request: ${config.url}`);
      }
      return { config, data: {}, headers, status: 200, statusText: "OK" };
    };
    service.defaults.adapter = adapter;
  });

  afterEach(() => {
    cleanup();
    service.defaults.adapter = originalAdapter;
    sessionSignals.getRefreshToken?.abort();
    sessionSignals.relogin?.abort();
    extendSignal.extendToken?.abort();
    sessionSignals.getRefreshToken = undefined;
    sessionSignals.relogin = undefined;
    extendSignal.extendToken = undefined;
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

  it.each(["running", "suspended"])(
    "Given Home starts hidden with %s timers, When access expires and the user returns, Then Extend succeeds",
    async (timers) => {
      setVisibility("hidden");
      await renderSession();
      expect(requestsTo("refreshtoken")).toHaveLength(1);
      if (timers === "running") {
        await advanceTime(accessLifetime);
      } else {
        jest.setSystemTime(now + accessLifetime);
      }
      await act(async () => setVisibility("visible"));
      expect(screen.getByRole("dialog")).toBeInTheDocument();
      await act(async () => {
        fireEvent.click(screen.getByRole("button", { name: "Extend" }));
      });
      expect(requestsTo("relogin")[0].headers["Single-UI-Refresh"]).toBe(
        responseRefreshToken
      );
      expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
      expect(screen.getByTestId("session-workspace")).toBeInTheDocument();
    }
  );

  it("Given Home first mounts after the acquisition deadline, Then it obtains missing refresh while access is still valid", async () => {
    await renderSession({
      token: token("late-access", now + 10_000),
      expiredIn: (now + 10_000) / 1000,
    });
    expect(requestsTo("refreshtoken")).toHaveLength(1);
    await advanceTime(10_000);
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: "Extend" }));
    });
    expect(requestsTo("relogin")[0].headers["Single-UI-Refresh"]).toBe(
      responseRefreshToken
    );
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("Given a page that never hides, When access expires, Then the visible timer has prepared a refresh token for manual Extend", async () => {
    await renderSession();
    expect(requestsTo("refreshtoken")).toHaveLength(0);

    await advanceTime(accessLifetime - refreshLead - 1);
    expect(requestsTo("refreshtoken")).toHaveLength(0);
    await advanceTime(1);

    expect(requestsTo("refreshtoken")).toHaveLength(1);
    expect(JSON.parse(requestsTo("refreshtoken")[0].data)).toEqual({
      singleUIAuthorization: token("initial-access", now + accessLifetime),
    });
    expect(getHooksBase().store.refreshToken).toBe(responseRefreshToken);
    expect(getHooksBase().store.expiredIn).toBe((now + accessLifetime) / 1000);
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();

    await advanceTime(refreshLead);
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    expect(requestsTo("relogin")).toHaveLength(0);
    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: "Extend" }));
    });

    expect(requestsTo("relogin")).toHaveLength(1);
    expect(requestsTo("relogin")[0].headers["Single-UI-Refresh"]).toBe(
      responseRefreshToken
    );
    expect(getHooksBase().store.token).toBe(responseAccessToken);
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(requestsTo("refreshtoken")).toHaveLength(1);
  });

  it.each([1, refreshLead - 1])(
    "Given a usable refresh and %i ms of access remaining, When the page hides, Then the session remains manually extendable",
    async (remaining) => {
      await renderSession();
      await advanceTime(accessLifetime - refreshLead);
      const acquiredRefresh = getHooksBase().store.refreshToken;
      expect(acquiredRefresh).toBeDefined();

      const adapter = service.defaults.adapter as AxiosAdapter;
      let rejectLateAcquisition: (() => void) | undefined;
      service.defaults.adapter = async (config) => {
        const response = await adapter(config);
        if (config.url === "/api/auth/v2/sso/refreshtoken") {
          await new Promise<void>((_resolve, reject) => {
            rejectLateAcquisition = () =>
              reject({
                config,
                message: "Request failed with status code 401",
                response: {
                  ...response,
                  status: 401,
                  data: { errorMessage: "TOKEN_INVALID_EXPIRED" },
                },
              });
          });
        }
        return response;
      };
      await advanceTime(refreshLead - remaining);
      await act(async () => setVisibility("hidden"));
      await advanceTime(remaining + 1);
      await act(async () => {
        rejectLateAcquisition?.();
        setVisibility("visible");
      });

      expect(screen.getByRole("dialog")).toBeInTheDocument();
      expect(requestsTo("refreshtoken")).toHaveLength(1);
      await act(async () => {
        fireEvent.click(screen.getByRole("button", { name: "Extend" }));
      });
      expect(requestsTo("relogin")[0].headers["Single-UI-Refresh"]).toBe(
        acquiredRefresh
      );
      expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
      expect(screen.getByTestId("session-workspace")).toBeInTheDocument();
    }
  );

  it("Given the page is hidden across the timer deadline, When it returns in the final 25 seconds, Then no hidden or catch-up timer request runs", async () => {
    await renderSession();
    await act(async () => {
      setVisibility("hidden");
    });
    expect(requestsTo("refreshtoken")).toHaveLength(1);

    // Background timers run in this case; the separate suspension helper
    // covers browsers whose timers are frozen instead.
    await advanceTime(accessLifetime - refreshLead + 5000);
    expect(requestsTo("refreshtoken")).toHaveLength(1);
    await act(async () => {
      setVisibility("visible");
    });
    await advanceTime(0);
    expect(requestsTo("refreshtoken")).toHaveLength(1);
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();

    await advanceTime(refreshLead - 5000);
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    await act(async () => {
      setVisibility("hidden");
      setVisibility("visible");
      setVisibility("hidden");
    });
    expect(requestsTo("refreshtoken")).toHaveLength(1);
    expect(requestsTo("relogin")).toHaveLength(0);
  });

  describe("Delayed refresh delivery after access expiry", () => {
    beforeEach(async () => {
      const adapter = service.defaults.adapter as AxiosAdapter;
      let finishRefresh!: () => void;
      const responseReady = new Promise<void>((resolve) => {
        finishRefresh = resolve;
      });
      service.defaults.adapter = async (config) => {
        const response = await adapter(config);
        if (config.url === "/api/auth/v2/sso/refreshtoken") {
          await responseReady;
        }
        return response;
      };
      await renderSession();
      await advanceTime(accessLifetime - refreshLead - 1000);
      await act(async () => {
        setVisibility("hidden");
      });
      expect(requestsTo("refreshtoken")).toHaveLength(1);
      expect(getHooksBase().store.refreshToken).toBeUndefined();

      await act(async () => {
        jest.setSystemTime(now + accessLifetime);
        setVisibility("visible");
      });
      expect(screen.getByRole("dialog")).toBeInTheDocument();
      await act(async () => {
        finishRefresh();
      });

      expect(getHooksBase().store.refreshToken).toBe(responseRefreshToken);
      expect(getHooksBase().store.token).toBe(
        token("initial-access", now + accessLifetime)
      );
      expect(screen.getByRole("dialog")).toBeInTheDocument();
      expect(requestsTo("relogin")).toHaveLength(0);
      expect(requestsTo("refreshtoken")).toHaveLength(1);
    });

    it("keeps recovery available after delayed credentials arrive", () => {
      expect(getHooksBase().store.isOnLogout).toBe(false);
      expect(screen.getByRole("button", { name: "Extend" })).toBeEnabled();
    });

    it("Given a hide request is slow, When access expires before its response arrives, Then manual Extend renews the session", async () => {
      await act(async () => {
        fireEvent.click(screen.getByRole("button", { name: "Extend" }));
      });
      expect(getHooksBase().store.token).toBe(responseAccessToken);
      expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    });
  });

  it("Given a pending hide request, When the page is shown and hidden again, Then the request is shared and its token is reused", async () => {
    const adapter = service.defaults.adapter as AxiosAdapter;
    const finishRefresh: Array<() => void> = [];
    const acquiredRefresh = responseRefreshToken;
    service.defaults.adapter = async (config) => {
      const response = await adapter(config);
      if (config.url === "/api/auth/v2/sso/refreshtoken") {
        await new Promise<void>((resolve) => finishRefresh.push(resolve));
      }
      return response;
    };
    await renderSession();
    await act(async () => setVisibility("hidden"));
    expect(requestsTo("refreshtoken")).toHaveLength(1);
    responseRefreshToken = token("second-hide-refresh", now + refreshLifetime);
    await act(async () => setVisibility("visible"));
    await act(async () => setVisibility("hidden"));

    expect(requestsTo("refreshtoken")).toHaveLength(1);
    expect(requestsTo("refreshtoken")[0].signal?.aborted).toBe(false);
    await act(async () => finishRefresh[0]());
    expect(getHooksBase().store.refreshToken).toBe(acquiredRefresh);

    await act(async () => setVisibility("visible"));
    await act(async () => setVisibility("hidden"));
    expect(getHooksBase().store.refreshToken).toBe(acquiredRefresh);
    expect(requestsTo("refreshtoken")).toHaveLength(1);
    expect(requestsTo("relogin")).toHaveLength(0);
  });

  it.each([
    { remaining: 10_801_000, expectedRequests: 0 },
    { remaining: 10_800_000, expectedRequests: 1 },
    { remaining: 10_799_000, expectedRequests: 1 },
  ])(
    "Given refresh has $remaining ms left, When Home hides, Then it sends $expectedRequests refresh requests",
    async ({ remaining, expectedRequests }) => {
      const existingRefresh = token("existing-refresh", now + remaining);
      await renderSession({ refreshToken: existingRefresh });
      await act(async () => setVisibility("hidden"));

      expect(requestsTo("refreshtoken")).toHaveLength(expectedRequests);
      expect(getHooksBase().store.refreshToken).toBe(
        expectedRequests ? responseRefreshToken : existingRefresh
      );
    }
  );

  it("[SR08] Given a minimized browser, When the user returns before access expiry and works, Then access renews and the refresh token is preserved", async () => {
    await renderSession();
    expect(requestsTo("refreshtoken")).toHaveLength(0);
    expect(getHooksBase().store.refreshToken).toBeUndefined();

    await returnAfterSuspension(10 * minute);
    const refreshToken = getHooksBase().store.refreshToken;
    expect(refreshToken).toBe(responseRefreshToken);

    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(requestsTo("extend")).toHaveLength(0);
    expect(requestsTo("relogin")).toHaveLength(0);

    await continueWorking();

    expect(requestsTo("extend")).toHaveLength(1);
    expect(JSON.parse(requestsTo("extend")[0].data)).toEqual({
      singleUIAuthorization: token("initial-access", now + accessLifetime),
    });
    expect(getHooksBase().store.token).toBe(responseAccessToken);
    expect(getHooksBase().store.expiredIn).toBe((now + 25 * minute) / 1000);
    expect(getHooksBase().store.refreshToken).toBe(refreshToken);
    expect(requestsTo("refreshtoken")).toHaveLength(1);

    // The old access-token deadline must not interrupt renewed activity.
    await advanceTime(5 * minute);
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it.each([15, 30, 60, 120, 239])(
    "[SR09] Given return after %i minutes, When the user explicitly extends and continues working, Then the original refresh token remains in use",
    async (minutesAway) => {
      await renderSession();
      await returnAfterSuspension(minutesAway * minute);
      const refreshToken = getHooksBase().store.refreshToken;
      expect(refreshToken).toBe(responseRefreshToken);

      expect(screen.getByRole("dialog")).toHaveTextContent(
        "Your session has been expired"
      );
      expect(requestsTo("relogin")).toHaveLength(0);
      expect(requestsTo("extend")).toHaveLength(0);
      expect(requestsTo("logout")).toHaveLength(0);
      expect(requestsTo("refreshtoken")).toHaveLength(1);

      responseAccessToken = token(
        "manually-extended-access",
        Date.now() + accessLifetime,
        Date.now()
      );
      await act(async () => {
        fireEvent.click(screen.getByRole("button", { name: "Extend" }));
      });

      expect(requestsTo("relogin")).toHaveLength(1);
      expect(requestsTo("relogin")[0].headers["Single-UI-Refresh"]).toBe(
        refreshToken
      );
      expect(getHooksBase().store.token).toBe(responseAccessToken);
      expect(getHooksBase().store.refreshToken).toBe(refreshToken);
      expect(screen.queryByRole("dialog")).not.toBeInTheDocument();

      const manualAccessToken = responseAccessToken;
      responseAccessToken = token(
        "continued-operation-access",
        Date.now() + accessLifetime + 5000,
        Date.now() + 5000
      );
      await continueWorking();

      expect(requestsTo("extend")).toHaveLength(1);
      expect(JSON.parse(requestsTo("extend")[0].data)).toEqual({
        singleUIAuthorization: manualAccessToken,
      });
      expect(getHooksBase().store.token).toBe(responseAccessToken);
      expect(getHooksBase().store.refreshToken).toBe(refreshToken);
      expect(requestsTo("refreshtoken")).toHaveLength(1);
      expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    }
  );

  it("[SR10] Given access expired during suspension, When the user returns and moves the mouse, Then expired access is not restored silently", async () => {
    await renderSession();
    await returnAfterSuspension(30 * minute);
    await continueWorking();

    expect(requestsTo("extend")).toHaveLength(0);
    expect(requestsTo("relogin")).toHaveLength(0);
    expect(requestsTo("refreshtoken")).toHaveLength(1);
    expect(getHooksBase().store.token).toBe(
      token("initial-access", now + accessLifetime)
    );
    expect(screen.getByRole("dialog")).toBeInTheDocument();
  });

  it.each([
    [30_000, 1],
    [29_999, 0],
  ])(
    "Given access has %i milliseconds remaining on return, When the activity delay elapses, Then %i extension requests respect the existing cutoff",
    async (remainingAtReturn, expectedRequests) => {
      await renderSession();
      await returnAfterSuspension(accessLifetime - remainingAtReturn);
      await continueWorking();

      expect(requestsTo("extend")).toHaveLength(expectedRequests);
      expect(requestsTo("relogin")).toHaveLength(0);
      // The visible deadline reuses the token acquired when the page hid.
      expect(requestsTo("refreshtoken")).toHaveLength(1);
      expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    }
  );

  it("[SR11] Given repeated successful activity, When the original refresh expires, Then access remains active and later renewal uses its replacement", async () => {
    await renderSession();
    await returnAfterSuspension(0);

    for (let operation = 0; operation < 23; operation += 1) {
      await advanceTime(10 * minute);
      responseAccessToken = token(
        `operation-${operation}`,
        Date.now() + accessLifetime + 5000,
        Date.now() + 5000
      );
      await continueWorking();
      expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    }

    expect(requestsTo("extend")).toHaveLength(23);
    expect(requestsTo("refreshtoken")).toHaveLength(1);
    expect(getHooksBase().store.refreshToken).toBe(responseRefreshToken);
    expect(getHooksBase().store.expiredIn).toBeGreaterThan(
      (now + refreshLifetime) / 1000
    );
    const activeAccessToken = getHooksBase().store.token;
    const activeAccessExpiry = getHooksBase().store.expiredIn;
    const initialRefreshToken = responseRefreshToken;
    responseRefreshToken = token(
      "replacement-refresh",
      Date.now() + refreshLifetime,
      Date.now()
    );
    await advanceTime(now + refreshLifetime - Date.now());
    await advanceTime(0);
    expect(requestsTo("refreshtoken")).toHaveLength(2);
    expect(JSON.parse(requestsTo("refreshtoken")[1].data)).toEqual({
      singleUIAuthorization: activeAccessToken,
    });
    expect(getHooksBase().store.refreshToken).toBe(responseRefreshToken);
    expect(getHooksBase().store.refreshToken).not.toBe(initialRefreshToken);
    expect(getHooksBase().store.token).toBe(activeAccessToken);
    expect(getHooksBase().store.expiredIn).toBe(activeAccessExpiry);
    expect(getHooksBase().store.isOnLogout).toBe(false);
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    await advanceTime(1000);

    expect(requestsTo("logout")).toHaveLength(0);
    expect(requestsTo("relogin")).toHaveLength(0);
    expect(requestsTo("extend")).toHaveLength(23);
    expect(screen.getByTestId("session-workspace")).toBeInTheDocument();

    // The replacement must also support the existing later idle recovery path.
    await advanceTime((activeAccessExpiry as number) * 1000 - Date.now());
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Extend" })).not.toBeDisabled();
    responseAccessToken = token(
      "manual-access-after-refresh-replacement",
      Date.now() + accessLifetime,
      Date.now()
    );
    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: "Extend" }));
    });
    expect(requestsTo("relogin")).toHaveLength(1);
    expect(requestsTo("relogin")[0].headers["Single-UI-Refresh"]).toBe(
      responseRefreshToken
    );
    expect(getHooksBase().store.token).toBe(responseAccessToken);
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(requestsTo("logout")).toHaveLength(0);
  });

  it("[SR12] Given the expiration alert is untouched, When the refresh deadline is reached, Then logout clears authentication and stored access", async () => {
    await renderSession();
    await advanceTime(accessLifetime - refreshLead);
    expect(requestsTo("refreshtoken")).toHaveLength(1);
    await advanceTime(refreshLead);
    expect(screen.getByRole("dialog")).toBeInTheDocument();

    await advanceTime(refreshLifetime - accessLifetime - 2001);
    expect(requestsTo("logout")).toHaveLength(0);
    expect(getHooksBase().store.isOnLogout).toBe(false);
    await advanceTime(1);
    expect(getHooksBase().store.isOnLogout).toBe(true);
    expect(screen.getByRole("button", { name: "Extend" })).toBeDisabled();

    // Preserve the existing two-second lead and one-second logout delay.
    await advanceTime(1000);
    expect(requestsTo("logout")).toHaveLength(1);
    expect(requestsTo("relogin")).toHaveLength(0);
    expect(screen.getByRole("button", { name: "Sign in" })).toBeInTheDocument();
    expect(getHooksBase().store.token).toBeUndefined();
    expect(getHooksBase().store.refreshToken).toBeUndefined();
    expect(getHooksBase().store.expiredIn).toBeUndefined();
    expect(localStorage.getItem(ActionType.SET_TOKEN)).toBeNull();
    expect(sessionStorage.getItem(ActionType.SET_TOKEN)).toBeNull();
  });

  it("Given manual Extend just before refresh expiry, When the original refresh expires, Then renewed access stays active and refresh is replaced", async () => {
    await renderSession();
    await returnAfterSuspension(239 * minute);
    responseAccessToken = token(
      "access-valid-beyond-refresh",
      now + 254 * minute,
      Date.now()
    );
    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: "Extend" }));
    });
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(getHooksBase().store.expiredIn).toBe((now + 254 * minute) / 1000);

    const initialRefreshToken = responseRefreshToken;
    responseRefreshToken = token(
      "replacement-after-manual-extend",
      now + 479 * minute,
      Date.now()
    );
    await advanceTime(minute);
    await advanceTime(0);
    expect(getHooksBase().store.isOnLogout).toBe(false);
    await advanceTime(1000);

    expect(screen.getByTestId("session-workspace")).toBeInTheDocument();
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(requestsTo("logout")).toHaveLength(0);
    expect(requestsTo("relogin")).toHaveLength(1);
    expect(requestsTo("refreshtoken")).toHaveLength(2);
    expect(getHooksBase().store.token).toBe(responseAccessToken);
    expect(getHooksBase().store.refreshToken).toBe(responseRefreshToken);
    expect(getHooksBase().store.refreshToken).not.toBe(initialRefreshToken);
  });

  it.each([
    { label: "225m24s", elapsed: serverRefreshLifetime },
    { label: "4 hours", elapsed: 4 * 60 * minute },
    { label: "4 hours and 1 millisecond", elapsed: 4 * 60 * minute + 1 },
    { label: "8 hours", elapsed: 8 * 60 * minute },
    { label: "24 hours", elapsed: 24 * 60 * minute },
  ])(
    "[SR05] Given a 225m24s refresh lifetime and suspension for $label, When the user returns, Then logout completes without renewing",
    async ({ elapsed }) => {
      responseRefreshToken = token(
        "backend-refresh-lifetime",
        now + serverRefreshLifetime
      );
      await renderSession();
      await returnAfterSuspension(elapsed);
      await advanceTime(0);

      expect(getHooksBase().store.isOnLogout).toBe(true);
      expect(screen.getByRole("button", { name: "Extend" })).toBeDisabled();
      await advanceTime(1000);

      expect(screen.getByRole("button", { name: "Sign in" })).toBeInTheDocument();
      expect(requestsTo("logout")).toHaveLength(1);
      expect(requestsTo("relogin")).toHaveLength(0);
      expect(requestsTo("extend")).toHaveLength(0);
      expect(requestsTo("refreshtoken")).toHaveLength(1);
      expect(getHooksBase().store.refreshToken).toBeUndefined();
    }
  );

  it("[SR13] Given the user logs out from the alert, When another login succeeds and the page hides, Then it obtains a new refresh token rather than reusing the previous session", async () => {
    await renderSession();
    await returnAfterSuspension(30 * minute);
    const previousRefreshToken = getHooksBase().store.refreshToken;
    fireEvent.click(screen.getByRole("button", { name: "Logout" }));
    await advanceTime(1000);

    expect(getHooksBase().store.token).toBeUndefined();
    expect(getHooksBase().store.refreshToken).toBeUndefined();
    responseAccessToken = token(
      "new-login-access",
      Date.now() + accessLifetime,
      Date.now()
    );
    responseRefreshToken = token(
      "new-login-refresh",
      Date.now() + refreshLifetime,
      Date.now()
    );
    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: "Sign in" }));
    });

    expect(requestsTo("login")).toHaveLength(1);
    expect(requestsTo("refreshtoken")).toHaveLength(1);
    expect(getHooksBase().store.refreshToken).toBeUndefined();
    await act(async () => {
      setVisibility("hidden");
    });
    expect(requestsTo("refreshtoken")).toHaveLength(2);
    expect(JSON.parse(requestsTo("refreshtoken")[1].data)).toEqual({
      singleUIAuthorization: responseAccessToken,
    });
    expect(getHooksBase().store.refreshToken).toBe(responseRefreshToken);
    expect(getHooksBase().store.refreshToken).not.toBe(previousRefreshToken);
    expect(getHooksBase().store.isOnLogout).toBe(false);
    expect(screen.getByTestId("session-workspace")).toBeInTheDocument();
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });
});
