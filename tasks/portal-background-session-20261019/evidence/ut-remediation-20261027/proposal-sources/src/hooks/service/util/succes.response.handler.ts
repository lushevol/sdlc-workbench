import { AxiosError, AxiosResponse, CanceledError } from "axios";
import { getHooksBase } from "../../HooksBase";
import { ActionType } from "../../reducer/util/ActionType";
import {
  handleLogin,
  handleUser,
  handleDrawers,
  handleRefreshToken,
  handleEntities,
  handleEntitlementsToken,
} from "../../../utils/login";
import { handleStandardResponse } from "../../../utils/ratan";
import { getJWTPayload } from "../../../utils/common";
import { errorHandler } from "./error.response.handler";
import { finishRequestLoading } from "./requestLoading";
import {
  currentSessionEpoch,
  invalidateSession,
  isFreshLogin,
  isStaleSessionRequest,
  SessionRequestConfig,
} from "../../../utils/sessionEpoch";

const standardResponseURLS = ["/api/ratan/", "/api/idns/"];

const isStandardResponse = (response: AxiosResponse) => {
  const requestUrl = response?.config?.url ?? "";

  return (
    standardResponseURLS.some((url) => requestUrl.includes(url)) ||
    response?.config?.headers?.["standard-response"] === "true"
  );
};

export const successHandler = (response: AxiosResponse): any => {
  if (
    isStaleSessionRequest(response.config) ||
    response.config?.signal?.aborted
  ) {
    finishRequestLoading(response.config);
    throw new CanceledError(
      "Discarded an ended session response",
      response.config
    );
  }
  const loginAccess =
    response.headers?.["single-ui-authorization"] ??
    response.headers?.["Single-UI-Authorization"];
  if (response.config?.url?.includes("/auth/v2/sso/relogin")) {
    try {
      const payload =
        typeof loginAccess === "string" ? getJWTPayload(loginAccess) : "";
      if (
        !payload ||
        typeof payload.exp !== "number" ||
        !Number.isFinite(payload.exp * 1000) ||
        payload.exp * 1000 <= Date.now() ||
        typeof payload.iat !== "number" ||
        !Number.isFinite(payload.iat) ||
        payload.iat <= 0 ||
        payload.exp <= payload.iat
      ) {
        throw new Error("Unusable renewal access");
      }
    } catch {
      return errorHandler(
        new AxiosError(
          "Relogin did not return usable access",
          "ERR_BAD_RESPONSE",
          response.config
        )
      );
    }
  }
  if (isFreshLogin(response.config?.url) && loginAccess) {
    // Requests started while login was pending still belong to the old session.
    invalidateSession();
    (response.config as SessionRequestConfig).sessionEpoch =
      currentSessionEpoch();
    getHooksBase().baseDispatch({
      type: ActionType.SET_REFRESH_TOKEN,
      data: { refreshToken: undefined },
    });
  }
  if (
    response?.config?.url?.includes("/api/auth/v2/sso/login") ||
    response?.config?.url?.includes("/api/auth/v3/sso/login") ||
    response?.config?.url?.includes("/api/auth/v2/sso/relogin") ||
    response?.config?.url?.includes("/api/auth/v2/sso/validate") ||
    response?.config?.url?.includes("/api/auth/v2/sso/extend")
  ) {
    handleDrawers(response);
    handleEntities(response);
    handleEntitlementsToken(response);
    handleUser(response);
    handleLogin(response);
  }
  if (response?.config?.url?.includes("/api/auth/v2/sso/refreshtoken")) {
    handleRefreshToken(response);
  }
  finishRequestLoading(response.config);
  if (isStandardResponse(response)) {
    return handleStandardResponse(response);
  }
  return response;
};
