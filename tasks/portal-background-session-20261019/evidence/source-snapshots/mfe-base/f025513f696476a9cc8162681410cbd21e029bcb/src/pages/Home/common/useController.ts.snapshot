import React from "react";
import { useContext } from "../../../hooks/provider";
import useDispatcher from "../../../hooks/dispathcer";
import { Workspace } from "../../../hooks/model/workspaces";
import { validateWorkspace, aOrb } from "../../../utils/common";
import { getRefreshToken } from "../../../hooks/service";
import { extend } from "../../../hooks/service/util/extend";
import useAnalytics from "../../../analytics";
import { AnalyticsData } from "../../../analytics/model";
import { handleLoginEntities } from "../../../utils/login";
import { setDetail, refreshTabUtil } from "./util";
const analyticsData: AnalyticsData = { container: "Base", tile: "home" };

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
  const timerRefreshToken = React.useRef<any>(0);
  const [showTimeout, setShowTimeout] = React.useState(false);
  const [value, setValue] = React.useState(1);
  const [ready, setReady] = React.useState(false);
  const [validateWorkspaceReady, setValidateWorkspaceReady] =
    React.useState(false);
  const handleChange = (event, newValue: number) => {
    if (
      !event.target?.parentElement?.parentElement?.id?.includes(
        "deleteWorkspace-"
      )
    ) {
      const workspaces = [...(store?.workspaces as Workspace[])];
      const workspace = workspaces[newValue - 1];
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
    if (timerRefreshToken.current) {
      clearTimeout(timerRefreshToken.current);
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
      timerRefreshToken.current = setTimeout(() => {
        getRefreshToken();
      }, difftime - 25000);
    }
    return () => {
      clearAllTimeout();
    };
  }, [store?.token, store?.expiredIn, ready]);

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

  const edit = (item: Workspace) => (event) => {
    const workspaces = [...(store?.workspaces as Workspace[])];
    const index = workspaces.findIndex((w) => w.id === item.id);
    workspaces[index].label = event.target.value;
    dispacthWorkspaces(workspaces);
  };

  const updateValue = (workspaces, index_, value_) => {
    if (index_ + 1 < value_) {
      setValue((v) => v - 1);
    } else if (index_ + 1 === value_) {
      dispacthCurrentWorkspace(workspaces[index_ - 1]);
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
      store?.refreshTab,
      store?.workspaces,
      item.id,
      setDetail,
      ButtonEvent
    );
  };

  const focus = (id) => () => {
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
        dispacthCurrentWorkspace(validWorkspaces[0]);
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
