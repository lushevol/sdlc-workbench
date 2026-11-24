import React, { useContext, useEffect } from "react";
import { getEnable } from "../../../ratanutils/componentEnabling";
import { getUser } from "../../../ratanutils/authenticator";
import { Context, saveFilter, removeFilter } from "../store";
import { useAnalytics } from "../../../Root/import";

interface ValidateType {
  validate: boolean;
  message?: string;
}

const useFieldNameController = (props) => {
  const { filterFieldType, messageApi, onRemove, onSavedFilter } = props;

  const [isModify, setIsModify] = React.useState<any>();
  const [isReadOnly, setIsReadOnly] = React.useState<any>();
  const [isLoading, setIsLoading] = React.useState(false);
  const [isRemoveLoading, setIsRemoveLoading] = React.useState(false);

  const { state, dispatch } = useContext(Context);
  const { filterList, temporaryFilter, currentFilter } = state;
  const { rowKey, name = "", body, assigneeList = "" } = temporaryFilter;
  const { role } = getUser();
  const { ButtonEvent } = useAnalytics();

  useEffect(() => {
    setIsModify(name && name === currentFilter?.name);
    setIsReadOnly(
      currentFilter?.moduleOwner && currentFilter?.moduleOwner !== role
    );
  }, [name, role, currentFilter]);

  const checkItem: (item: any) => ValidateType = (item) => {
    const isArray = Array.isArray(item.values);
    if (isArray) {
      if (item.values.length === 0 || item.values[0] === "") {
        return {
          validate: false,
          message: "The value of all fields cannot be empty!",
        };
      }
    } else {
      if (item.values === "" || typeof item.values === "undefined") {
        return {
          validate: false,
          message: "The value of all fields cannot be empty!",
        };
      }
    }
    return {
      validate: true,
    };
  };

  const validateFilterExitst: () => ValidateType = () => {
    if (getEnable("Filter_Builder_POC", filterFieldType)) {
      return {
        validate: true,
        message: "",
      };
    }
    const isExist =
      !isModify &&
      filterList[filterFieldType]?.find(
        (item: any) => item.type === filterFieldType && item.name === name
      );
    if (isExist) {
      return {
        validate: false,
        message: "Filter name already exists!",
      };
    } else {
      return {
        validate: true,
        message: "",
      };
    }
  };

  const saveBuilder = () => {
    const validateFilterExitstReuslt = validateFilterExitst();
    if (!validateFilterExitstReuslt.validate) {
      messageApi.error(validateFilterExitstReuslt.message);
      return false;
    }
    if (body.length) {
      for (const item of body) {
        const validdateItem = checkItem(item);
        if (!validdateItem.validate) {
          messageApi.error(validdateItem.message);
          return false;
        }
      }
    } else if (!body?.filter?.rules?.length) {
      messageApi.error("The value of all fields cannot be empty!");
      return false;
    }
    setIsLoading(true);
    const newId = isModify ? rowKey : "";
    const moduleOwner = isModify ? currentFilter?.moduleOwner || role : role;
    const newParams = {
      rowKey: newId,
      name,
      filterFieldType,
      assigneeList,
      moduleOwner: assigneeList ? moduleOwner : "",
      body,
    };

    saveFilter(newParams)
      .then((res: any) => {
        res.body = JSON.parse(res.body);

        if (newId) {
          dispatch({ type: "CHANGE_FILTER", data: res });
        } else {
          dispatch({ type: "ADD_FILTER", data: res });
        }

        dispatch({ type: "UPDATE_CURRENT_FILTER", data: res });
        setIsModify(true);
        setIsLoading(false);
        onSavedFilter && onSavedFilter({ json: res.body.filter });
        ButtonEvent("click", {
          name: "Save Filter Builder",
          value: isModify ? "Modify" : "Create",
        });
        messageApi.success("Save filter successful!");
      })
      .catch(() => {
        setIsModify(false);
        setIsLoading(false);
        messageApi.error("Save filter failed!");
      });
  };
  const removeBuilder = () => {
    setIsRemoveLoading(true);
    const newParams = {
      rowKey,
      moduleOwner: currentFilter?.moduleOwner,
    };
    removeFilter(newParams, filterFieldType)
      .then(() => {
        setIsRemoveLoading(false);
        onRemove(rowKey, "REMOVED");
        dispatch({ type: "UPDATE_CURRENT_FILTER", data: {} });
        dispatch({ type: "RESET_TEMPORARY_FILTER" });

        messageApi.success("Filter removed successfully!");
      })
      .catch(() => {
        setIsRemoveLoading(false);
        messageApi.error("Remove filter failed!");
      });
  };
  const compareFilterName = (newName: string) => {
    dispatch({ type: "UPDATE_TEMPORARY_FILTER", data: { name: newName } });
  };
  const compareFilterRole = (newRole: string | string[]) => {
    const assigneeList = Array.isArray(newRole) ? newRole.join(",") : newRole;
    dispatch({
      type: "UPDATE_TEMPORARY_FILTER",
      data: { assigneeList },
    });
  };
  const cancel = () => {
    messageApi.info("Cancel Remove!");
  };
  return {
    saveBuilder,
    removeBuilder,
    compareFilterName,
    compareFilterRole,
    isLoading,
    isModify,
    isRemoveLoading,
    cancel,
    isReadOnly,
  };
};

export default useFieldNameController;
