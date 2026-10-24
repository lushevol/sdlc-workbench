import React from "react";
import { useContext } from "../../../hooks/provider";
import useDispatcher from "../../../hooks/dispathcer";
import { Workspace } from "../../../hooks/model/workspaces";
import {
  validateWorkspace,
  aOrb,
  getJWTPayload,
} from "../../../utils/common";
import { getRefreshToken } from "../../../hooks/service";
import { extend } from "../../../hooks/service/util/extend";
import useAnalytics from "../../../analytics";
import { AnalyticsData } from "../../../analytics/model";
import { handleLoginEntities } from "../../../utils/login";
import { setDetail, refreshTabUtil } from "./util";
const analyticsData: AnalyticsData = { container: "Base", tile: "home" };
const REFRESH_BEFORE_ACCESS_EXPIRY_MS = 25_000;

const useController = () => {
  const [store, dispatch] = useContext();
  const { ButtonEvent, TileEvent, TabEvent } = useAnalytics();
  const {
    dispacthLoading,
    dispacthWorkspaces,
    dispacthCurrentWorkspace,
    addWorkspace,
    dispacthErrorMessage,
  } = useDispatcher();
  const timerPopup = React.useRef<any>(0);
  const timerMouseMove = React.useRef<any>(0);
  const [showTimeout, setShowTimeout] = React.useState(false);
  const [value, setValue] = React.useState(1);
  const [ready, setReady] = React.useState(false);
  const [validateWorkspaceReady, setValidateWorkspaceReady] =
    React.useState(false);
  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    const target = event.target as HTMLElement;
    if (
      !target.parentElement?.parentElement?.id?.includes(
        "deleteWorkspace-"
      )
    ) {
      const workspaces = [...(store?.workspaces as Workspace[])];
      const workspace = workspaces[newValue - 1];
      if (!workspace) return;
      let container = "base";
      let tile = "home";
      let title = workspace.label;
      setDetail(workspace, title, container, tile);
      TabEvent("click", {
        name: "select workspace",
        value: title,
        container,
        tile,
      });
      dispacthCurrentWorkspace(workspace);
      dispacthErrorMessage(undefined);
    }
  };
  const runExtend = () => {
    extend(store?.expiredIn, store.isOnLogout, store.token);
  };
  const mouseMove = () => {
    if (timerMouseMove.current) {
      clearTimeout(timerMouseMove.current);
    }
    timerMouseMove.current = setTimeout(runExtend, 5000);
  };
  const clearAllTimeout = () => {
    if (timerPopup.current) {
      clearTimeout(timerPopup.current);
    }
    if (timerMouseMove.current) {
      clearTimeout(timerMouseMove.current);
    }
  };

  React.useEffect(() => {
    const params: any = new URLSearchParams(window.location.search);
    if (params?.get("code")) {
      handleLoginEntities(store.entities, dispatch, store.drawers);
    }
    setReady(true);
    dispacthLoading(false);
    return () => {
      clearAllTimeout();
    };
  }, []);

  React.useEffect(() => {
    if (store?.token && ready) {
      const difftime = 1000 * aOrb(store?.expiredIn, 0) - new Date().getTime();
      timerPopup.current = setTimeout(() => {
        setShowTimeout(true);
      }, difftime);
    }
    return () => {
      if (timerPopup.current) {
        clearTimeout(timerPopup.current);
      }
    };
  }, [store?.token, store?.expiredIn, ready]);

  React.useEffect(() => {
    if (!ready || !store?.token) return;

    const accessExpiresAt = 1000 * aOrb(store.expiredIn, 0);
    let refreshExpiresAt = 0;
    if (store.refreshToken) {
      try {
        const payload = getJWTPayload(store.refreshToken);
        refreshExpiresAt = payload ? (payload.exp ?? 0) * 1000 : 0;
      } catch {
        // An invalid token has no usable expiry timestamp.
      }
    }

    const reconcileExpiry = () => {
      if (
        accessExpiresAt <= Date.now() ||
        (refreshExpiresAt > 0 && refreshExpiresAt <= Date.now())
      ) {
        setShowTimeout(true);
      }
    };
    const requestRefresh = () => {
      if (
        accessExpiresAt > Date.now() &&
        !showTimeout &&
        !store.isOnLogout &&
        (!refreshExpiresAt || refreshExpiresAt > Date.now()) &&
        (!refreshExpiresAt ||
          accessExpiresAt - Date.now() >= REFRESH_BEFORE_ACCESS_EXPIRY_MS)
      ) {
        getRefreshToken();
      }
    };
    let acquisitionTimer: ReturnType<typeof setTimeout> | undefined;
    const scheduleAcquisition = () => {
      clearTimeout(acquisitionTimer);
      const delay = accessExpiresAt - REFRESH_BEFORE_ACCESS_EXPIRY_MS - Date.now();
      // A missed deadline must not replay an acquisition when the page returns.
      if (document.visibilityState === "visible" && delay > 0) {
        acquisitionTimer = setTimeout(() => {
          if (document.visibilityState === "visible") requestRefresh();
        }, delay);
      }
    };
    let previousVisibility = document.visibilityState;
    const handleVisibilityChange = () => {
      const visibility = document.visibilityState;
      if (visibility === previousVisibility) return;
      previousVisibility = visibility;
      clearTimeout(acquisitionTimer);
      if (visibility === "hidden") {
        requestRefresh();
      } else {
        reconcileExpiry();
        scheduleAcquisition();
      }
    };
    if (
      !refreshExpiresAt &&
      (document.visibilityState === "hidden" ||
        accessExpiresAt - Date.now() <= REFRESH_BEFORE_ACCESS_EXPIRY_MS)
    ) {
      requestRefresh();
    }
    scheduleAcquisition();
    document.addEventListener("visibilitychange", handleVisibilityChange);
    const refreshExpiryTimer = refreshExpiresAt
      ? setTimeout(reconcileExpiry, Math.max(0, refreshExpiresAt - Date.now()))
      : undefined;
    return () => {
      document.removeEventListener("visibilitychange", handleVisibilityChange);
      clearTimeout(acquisitionTimer);
      clearTimeout(refreshExpiryTimer);
    };
  }, [
    ready,
    store?.token,
    store?.expiredIn,
    store?.refreshToken,
    store?.isOnLogout,
    showTimeout,
  ]);

  React.useEffect(() => {
    if (
      store?.workspaces &&
      store?.currentWorkspace &&
      store?.currentWorkspace?.id
    ) {
      const workspaces = [...(store?.workspaces as Workspace[])];
      const index = workspaces.findIndex(
        (w) => w.id === store?.currentWorkspace?.id
      );
      setValue(index + 1);
    }
  }, [store.currentWorkspace]);

  const add = () => {
    addWorkspace();
    ButtonEvent("click", { name: "add workspace", ...analyticsData });
    dispacthErrorMessage(undefined);
  };

  const edit = (item: Workspace) => (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const workspaces = [...(store?.workspaces as Workspace[])];
    const index = workspaces.findIndex((w) => w.id === item.id);
    workspaces[index].label = event.target.value;
    dispacthWorkspaces(workspaces);
  };

  const updateValue = (
    workspaces: Workspace[],
    index_: number,
    value_: number
  ) => {
    if (index_ + 1 < value_) {
      setValue((v) => v - 1);
    } else if (index_ + 1 === value_) {
      const nextWorkspace = workspaces[index_ - 1] ?? workspaces[index_ + 1];
      if (nextWorkspace) dispacthCurrentWorkspace(nextWorkspace);
    }
  };
  const remove = (item: Workspace) => (event: React.MouseEvent) => {
    event.stopPropagation();
    let workspaces = [...(store?.workspaces as Workspace[])];
    const index = workspaces.findIndex((w) => w.id === item.id);
    const workspace = workspaces[index];
    let container = "base";
    let tile = "home";
    let title = workspace.label;
    setDetail(workspace, title, container, tile);
    ButtonEvent("click", {
      name: "remove workspace",
      value: title,
      container,
      tile,
    });
    TileEvent("close", { name: title, container, tile });
    updateValue(workspaces, index, value);
    workspaces.splice(index, 1);
    dispacthWorkspaces(workspaces);
    dispacthErrorMessage(undefined);
    return false;
  };

  const refreshTab = (item: Workspace) => (event: React.MouseEvent) => {
    event.stopPropagation();
    refreshTabUtil(
      store?.refreshTab as Record<string, () => void> | undefined,
      store?.workspaces as Workspace[] | undefined,
      item.id,
      setDetail,
      ButtonEvent
    );
  };

  const focus = (id: number) => () => {
    const workspaces = [...(store?.workspaces as Workspace[])];
    const workspace = workspaces[id - 1];
    let container = "base";
    let tile = "home";
    let title = workspace.label;
    setDetail(workspace, title, container, tile);
    ButtonEvent("click", {
      name: "edit workspace",
      value: title,
      container,
      tile,
    });
    document.getElementById(`edit-${workspace.id}`)?.focus();
  };

  React.useEffect(() => {
    if (ready) {
      if (store?.workspaces?.length) {
        const validWorkspaces = validateWorkspace(
          store?.workspaces,
          store.entities,
          store.drawers
        );
        dispacthWorkspaces(validWorkspaces);
        if (validWorkspaces[0]) {
          dispacthCurrentWorkspace(validWorkspaces[0]);
        }
      }
      setValidateWorkspaceReady(true);
    }
  }, [ready]);
  return {
    store,
    value,
    handleChange,
    add,
    edit,
    focus,
    remove,
    ready,
    showTimeout,
    setShowTimeout,
    mouseMove,
    validateWorkspaceReady,
    runExtend,
    updateValue,
    refreshTab,
  };
};

export default useController;
