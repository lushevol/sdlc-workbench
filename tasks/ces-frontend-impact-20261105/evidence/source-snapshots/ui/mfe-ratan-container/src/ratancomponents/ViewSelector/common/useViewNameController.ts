import { useContext, useEffect, useState } from "react";
import { GridApi } from "ag-grid-community";
import { Context, removeView, saveView } from "../store";
import {
  getUser,
  hasPrivatePermission,
  hasPublicPermission,
} from "../../../ratanutils/authenticator";
import { getEnable } from "../../../ratanutils/componentEnabling";

const useViewNameController = (props, messageApi) => {
  const { viewFieldType, ems2Subject, tradeGridReady = {} } = props;
  const [isModify, setIsModify] = useState<boolean>(false);
  const [isReadOnly, setIsReadOnly] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isRemoveLoading, setIsRemoveLoading] = useState(false);
  const [newName, setNewName] = useState("");
  const [newRole, setNewRole] = useState("");
  const [chooseAuthority, setChooseAuthority] = useState(true);
  const { state, dispatch } = useContext(Context);
  const { currentView, viewList } = state;
  const { role } = getUser();

  const { api }: { api: GridApi } = tradeGridReady;

  const { rowKey, name = "", isPublic }: any = currentView || {};

  const thisViewHasPermission = () => {
    return (
      hasPrivatePermission(ems2Subject ?? viewFieldType) === !isPublic ||
      hasPublicPermission(ems2Subject ?? viewFieldType) === isPublic
    );
  };

  const saveBuilder = () => {
    if (
      !isModify &&
      viewList &&
      viewList[viewFieldType].find((item: any) => item.name === newName)
    ) {
      messageApi.error("View name already exists!");
    } else {
      const newId = isModify ? rowKey : "";
      const moduleOwner = isModify ? currentView?.moduleOwner || role : role;
      const newBody = api?.getColumnState();
      setIsLoading(true);
      const newParams = {
        rowKey: newId,
        name: newName,
        viewFieldType,
        assigneeList: newRole,
        moduleOwner: newRole ? moduleOwner : "",
        body: newBody,
        chooseAuthority,
      };
      saveView(newParams)
        .then((res: any) => {
          dispatch({ type: "UPDATE_CURRENT_VIEW", data: res });
          if (isModify) {
            dispatch({ type: "UPDATE_VIEW", data: res });
          } else {
            dispatch({ type: "ADD_VIEW", data: res });
          }
          messageApi.success("Save view successful!");
          setIsLoading(false);
        })
        .catch(() => {
          messageApi.error("Save view failed!");
          setIsLoading(false);
        });
    }
  };

  const removeBuilder = () => {
    setIsRemoveLoading(true);
    const newParams = {
      rowKey,
      moduleOwner: currentView?.moduleOwner,
    };
    removeView(newParams, viewFieldType)
      .then(() => {
        dispatch({
          type: "REMOVE_VIEW",
          data: { rowKey, viewFieldType },
        });
        dispatch({ type: "UPDATE_CURRENT_VIEW", data: {} });
        messageApi.success("View removed successfully!");
        setIsRemoveLoading(false);
      })
      .catch(() => {
        messageApi.error("Remove view failed!");
        setIsRemoveLoading(false);
      });
  };

  const compareViewRole = (newRole: string | string[]) => {
    const assigneeList = Array.isArray(newRole) ? newRole.join(",") : newRole;
    setNewRole(assigneeList);
    setChooseAuthority(!newRole);
  };

  const cancel = () => {
    messageApi.info("Cancel Remove!");
  };

  useEffect(() => {
    if (getEnable("View_Builder_POC", props.viewFieldType)) {
      setIsModify(!!newName && newName === currentView?.name);
      setIsReadOnly(
        currentView?.moduleOwner && currentView?.moduleOwner !== role
      );
    } else {
      setIsModify(thisViewHasPermission() && name !== "" && name === newName);
    }
  }, [newName, name, role, currentView]);

  return {
    saveBuilder,
    removeBuilder,
    setChooseAuthority,
    thisViewHasPermission,
    newName,
    newRole,
    setNewName,
    compareViewRole,
    isLoading,
    isRemoveLoading,
    chooseAuthority,
    isModify,
    isReadOnly,
    cancel,
  };
};
export default useViewNameController;
