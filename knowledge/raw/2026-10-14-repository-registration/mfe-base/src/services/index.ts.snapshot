import React from "react";
import { postService, getService } from "../hooks/service";
import { clearStorageWhenLogout, getEnv } from "../utils/common";
import { useContext } from "../hooks/provider";
import { Workspace } from "../hooks/model/workspaces";
import { findTile } from "../utils/drawer";
import { LoginRequest } from "../auth/validation";

interface ValidationResponse {
  result?: boolean;
}

const useServices = () => {
  const [store, dispacth] = useContext();
  const login = (data: LoginRequest) =>
    postService("/auth/v2/sso/login", { ...data });
  const loginEntra = (data: LoginRequest) =>
    postService("/auth/v3/sso/login", { ...data });
  const logout = () => {
    const arr = [
      postService("/auth/v2/sso/logout", {
        singleUIAuthorization: store.token,
      }),
      getService("/ssiplus/imeta/logout"),
    ];
    Promise.all(arr).catch((e) => {
      console.error("e", e);
    });
    clearStorageWhenLogout(dispacth);
  };
  const validate = async () => {
    try {
      const { data } = await postService<ValidationResponse>(
        "/auth/v2/sso/validate",
        {
        singleUIAuthorization: store.token,
        }
      );
      if (data?.result) {
        return data?.result;
      }
    } catch (e) {}
    return false;
  };
  const ssePublish = async (tabId: string, _payload: unknown) => {
    try {
      if (["LOCAL"].includes(getEnv())) {
        const workspaces = [...(store?.workspaces as Workspace[])];
        const index = workspaces.findIndex(
          (workspace) => workspace.id === tabId
        );
        findTile(store.drawers, workspaces[index]);
      }
    } catch (e) {}
  };
  return {
    login,
    loginEntra,
    validate,
    logout,
    ssePublish,
  };
};

export default useServices;
