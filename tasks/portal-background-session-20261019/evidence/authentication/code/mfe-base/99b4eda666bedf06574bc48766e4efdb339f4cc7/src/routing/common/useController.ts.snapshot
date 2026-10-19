import React from "react";
import { useContext } from "../../hooks/provider";
import { ActionType } from "../../hooks/reducer/util/ActionType";
import useDispatcher from "../../hooks/dispathcer";
import {
  clearStorageWhenLogout,
  getEnv,
  storeData,
  waitFor,
} from "../../utils/common";
import useServices from "../../services";
import { SnackbarCloseReason } from "@mui/material";
import { validateOpenFinToken } from "../../auth/validation";

const useController = () => {
  const [store, dispatch] = useContext();
  const { dispacthTheme, dispacthErrorMessage } = useDispatcher();
  const { validate } = useServices();
  const [isReady, setIsReady] = React.useState(false);
  const handleCloseErrorMessage = (
    _event?: React.SyntheticEvent | Event,
    reason?: SnackbarCloseReason
  ) => {
    if (reason === "clickaway") {
      return;
    }
    dispacthErrorMessage(undefined);
  };
  const storageHandler = function (event: StorageEvent) {
    if (event.key === ActionType.SET_THEME && event.newValue) {
      dispacthTheme(event.newValue);
    }
  };
  React.useEffect(() => {
    window.addEventListener("storage", storageHandler, false);
    return () => {
      window.removeEventListener("storage", storageHandler, false);
    };
  }, []);
  const checkSession = async () => {
    if (store.token) {
      const result = await validate();
      if (!result) {
        clearStorageWhenLogout(dispatch);
      }
    }
    setIsReady(true);
  };
  const openfinCheckSession = async () => {
    const params = new URLSearchParams(window.location.search);
    const rawToken = params.get("openfintoken");
    const validation = validateOpenFinToken(rawToken);
    if (validation.success) {
      const token = validation.data;
      storeData(ActionType.SET_TOKEN, token);
      await waitFor(1000);
      window.location.href = window.location.href.replace(
        `openfintoken=${encodeURIComponent(token)}`,
        ""
      );
    } else {
      if (rawToken !== null) {
        dispacthErrorMessage("Invalid authentication token.");
      }
      checkSession();
    }
  };
  React.useEffect(() => {
    if (["LOCAL", "DEV"].includes(getEnv()) && window.fin) {
      openfinCheckSession();
    } else {
      checkSession();
    }
  }, []);
  return {
    store,
    isReady,
    storageHandler,
    checkSession,
    handleCloseErrorMessage,
    openfinCheckSession,
  };
};

export default useController;
