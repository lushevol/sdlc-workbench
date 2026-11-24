import { AxiosResponse } from "axios";
import { getHooksBase } from "../hooks/HooksBase";
import { User } from "../hooks/model/root";
import { ActionType, IAction } from "../hooks/reducer/util/ActionType";
import {
  clearStorageWhenLogout,
  getJWTPayload,
  JWTPayload,
  storeData,
} from "./common";
import { getEntities } from "./entities";
import type { Dispatch } from "react";
import { Entity, Tiles } from "../hooks/model/root";

export const setAuthorization = (token: string) => {
  const { baseDispatch } = getHooksBase();
  baseDispatch({
    type: ActionType.SET_TOKEN,
    data: { token },
  });
  storeData(ActionType.SET_TOKEN, token);
  const payload = getJWTPayload(token);
  if (payload != "") {
    dispacthUserLoginTime(payload);
  }
};

export const dispacthUserLoginTime = (payload: JWTPayload) => {
  if (payload.exp && payload.iat) {
    const { baseDispatch } = getHooksBase();
    baseDispatch({
      type: ActionType.SET_EXPIRED_TOKEN,
      data: {
        expiredIn: payload.exp,
        iat: payload.iat,
        userLoginTime: new Date(),
      },
    });
  }
};

const setUser = (user: User) => {
  const { baseDispatch } = getHooksBase();
  user.id = user.sub;
  user.userId = user.sub;
  baseDispatch({
    type: ActionType.SET_USER,
    data: { user },
  });
  storeData(ActionType.SET_USER, JSON.stringify(user));
};

export const handleLogin = (response: AxiosResponse) => {
  if (
    response?.headers &&
    (response?.headers["Single-UI-Authorization"] ||
      response?.headers["single-ui-authorization"])
  ) {
    const token = `${
      response.headers["Single-UI-Authorization"] ??
      response.headers["single-ui-authorization"]
    }`;
    setAuthorization(token);
  }
};

export const handleUser = (response: AxiosResponse) => {
  if (response?.data?.userInfo) {
    const userInfo = JSON.parse(response?.data?.userInfo);
    if (response?.data?.entitlementsToken) {
      const payload = getJWTPayload("B " + response?.data?.entitlementsToken);
      if (payload != "" && payload.entitlements != null) {
        userInfo.entitlements = JSON.parse(payload.entitlements);
      }
    }
    userInfo.entities = response?.data?.entities ?? [];
    userInfo.id = userInfo.sub;
    userInfo.fullName = userInfo.fullName ?? userInfo.sub;
    userInfo.name = userInfo.sub;
    userInfo.userId = userInfo.sub;
    if (userInfo.oud) {
      userInfo.oud = JSON.parse(userInfo.oud);
      userInfo.fullName = userInfo.oud.fullName;
    }
    setUser(userInfo);
  }
};

export const handleEntities = (response: AxiosResponse) => {
  if (response?.data?.entities) {
    const entities = response?.data?.entities;
    const { baseDispatch } = getHooksBase();
    baseDispatch({
      type: ActionType.SET_ENTITIES,
      data: { entities },
    });
  }
};

export const handleDrawers = (response: AxiosResponse) => {
  if (response?.data?.drawers?.length) {
    const drawers = response?.data?.drawers;
    const { baseDispatch } = getHooksBase();
    baseDispatch({
      type: ActionType.SET_DRAWERS,
      data: { drawers },
    });
  }
};

export const setRefreshToken = (refreshToken: string) => {
  const { baseDispatch } = getHooksBase();
  baseDispatch({
    type: ActionType.SET_REFRESH_TOKEN,
    data: { refreshToken },
  });
};

export const handleRefreshToken = (response: AxiosResponse) => {
  if (
    response?.headers &&
    (response?.headers["Single-UI-Refresh"] ||
      response?.headers["single-ui-refresh"])
  ) {
    const refreshToken = `${
      response.headers["Single-UI-Refresh"] ??
      response.headers["single-ui-refresh"]
    }`;
    setRefreshToken(refreshToken);
  }
};

export const handleEntitlementsToken = (response: AxiosResponse) => {
  if (response?.data?.entitlementsToken) {
    const { baseDispatch } = getHooksBase();
    baseDispatch({
      type: ActionType.SET_ENTITLEMENTS_TOKEN,
      data: { entitlementsToken: response?.data?.entitlementsToken },
    });
  }
};

export const handleLoginEntities = (
  entities_: Entity[] | undefined,
  dispatch: Dispatch<IAction>,
  drawers: Tiles[] | undefined
) => {
  let isValid = false;
  const entities = Object.keys(getEntities(drawers));
  entities_?.every((curr: Entity) => {
    if (entities.includes(curr.name)) {
      isValid = true;
    }
    return !isValid;
  });
  const { history } = window;
  history.replaceState(null, "", "/");
  if (!isValid) {
    clearStorageWhenLogout(dispatch);
    dispatch({
      type: ActionType.SET_ERRORMSG,
      data: { errorMsg: "No entitlements found." },
    });
  }
};
