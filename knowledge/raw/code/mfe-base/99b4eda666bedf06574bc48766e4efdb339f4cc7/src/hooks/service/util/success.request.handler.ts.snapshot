import { getHooksBase } from "../../HooksBase";
import { ActionType } from "../../reducer/util/ActionType";

export const requestHandler = (request: any) => {
  const { store, baseDispatch } = getHooksBase();
  /**
   * Prevent showing loading when request is sent
   * application set "show-loading" header to "false".
   */
  if (request.headers["show-loading"] !== "false") {
    baseDispatch({
      type: ActionType.SET_IS_LOADING,
      data: { isLoading: true },
    });
  }

  request.headers["userId"] = store.user?.userId;
  if (request.url?.includes("/sso/relogin")) {
    request.headers["Single-UI-Refresh"] = store.refreshToken;
  } else if (
    !request.url?.includes("/api/auth/") &&
    !request.url?.includes("/api/analytics/") &&
    !request.url?.includes("/api/sse/")
  ) {
    request.headers["Single-UI-Authorization"] = store.token;
  } else if (request.url?.includes("/api/auth/v1/fmo/admin")) {
    request.headers["Single-UI-Authorization"] = store.token;
  }
  if (
    request.url?.includes("?loader=false") ||
    request.url?.includes("&loader=false") ||
    request.url?.includes("/api/auth/v2/sso/extend") ||
    request.url?.includes("/api/ratan/bff/v1/esLogging") ||
    request.url?.includes("/api/ratan/bff/v1/apiStatus") ||
    request.url?.includes("/api/ratan/bff/v1/preference") ||
    request.url?.includes("/api/ratan/bff/v1/trade/affirmation") ||
    request.url?.includes("/api/ratan/v1/da/monitor") ||
    request.url?.includes("/api/analytics/") ||
    request.url?.includes("/api/ratan/v1/esLogging") ||
    request.url?.includes("/api/ratan/v1/apiStatus") ||
    request.url?.includes("/api/ratan/v1/preference") ||
    request.url?.includes("/api/ratan/v1/trade/affirmation") ||
    request.url?.includes("/api/ratan/da/v1/monitor")
  ) {
    baseDispatch({
      type: ActionType.SET_IS_LOADING,
      data: { isLoading: false },
    });
  }
  return request;
};
