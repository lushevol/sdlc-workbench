import { AxiosResponse } from "axios";
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

export const successHandler = (response: AxiosResponse): any => {
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
  const { baseDispatch } = getHooksBase();
  baseDispatch({
    type: ActionType.SET_IS_LOADING,
    data: { isLoading: false },
  });
  if (
    response?.config?.url?.includes("/api/ratan/") ||
    response?.config?.headers?.["standard-response"] === "true"
  ) {
    return handleStandardResponse(response);
  }
  return response;
};
