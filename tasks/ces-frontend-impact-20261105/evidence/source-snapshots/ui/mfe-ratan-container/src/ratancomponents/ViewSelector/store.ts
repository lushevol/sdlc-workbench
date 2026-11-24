import { createContext } from "react";
import { deepClone } from "../../ratanutils/utils";
import {
  getViewList,
  getViewDetails,
  putUpdateView,
  postSaveView,
  deleteView,
} from "../../ratanutils/http/api";
import { getUser } from "../../ratanutils/authenticator";
import { getEnable } from "../../ratanutils/componentEnabling";

export const defaultState: any = {
  currentView: null,
  viewList: {},
};
export const Context = createContext(defaultState);
const list: any = {};

// Action
export const getViews = (type: string) => {
  const { id, role } = getUser();

  const params = getEnable("View_Builder_POC", type)
    ? {
        type,
        creator: id,
        assignee: role,
        moduleOwner: role,
        searchAll: true,
      }
    : {
        type,
        owner: id,
        searchAll: true,
      };

  return getViewList(params).then((res: any) => {
    list[type] = Array.isArray(res) ? res : [];
    // sort
    list[type] = list[type].sort((param1: any, param2: any) => {
      const one = param1.name || "";
      const two = param2.name || "";
      return one.localeCompare(two);
    });

    list[type].forEach((item: any) => {
      item.body =
        typeof item.body === "string" ? JSON.parse(item.body) : item.body;
    });

    return list;
  });
};

export const getView = (rowKey: string, type: string) => {
  return getViewDetails(rowKey, type).then((res: any) => {
    res.body = JSON.parse(res.body);
    return res;
  });
};

export const saveView = ({
  rowKey,
  name,
  assigneeList,
  moduleOwner,
  body,
  viewFieldType,
  chooseAuthority,
}) => {
  const { id } = getUser();
  const owner = chooseAuthority ? id : "";
  const promise = rowKey
    ? putUpdateView.bind(null, rowKey)
    : postSaveView.bind(null);

  const params = getEnable("View_Builder_POC", viewFieldType)
    ? {
        name,
        creator: id.toString(),
        body: JSON.stringify(body),
        type: viewFieldType,
        assigneeList,
        moduleOwner,
        isPublic: false,
      }
    : {
        name,
        owner: owner.toString(),
        body: JSON.stringify(body),
        type: viewFieldType,
        isPublic: !chooseAuthority,
      };
  return promise(params);
};

export const removeView = ({ rowKey, moduleOwner }, viewFieldType) => {
  const { id } = getUser();
  const params = getEnable("View_Builder_POC", viewFieldType)
    ? {
        rowKey,
        creator: id.toString(),
        moduleOwner,
      }
    : rowKey;
  return deleteView(params, viewFieldType);
};

// Reducer
export const reducer = (state: any, action: any) => {
  const newState = deepClone(state);
  switch (action.type) {
    case "UPDATE_VIEWS":
      newState.viewList = action.data;
      return newState;
    case "UPDATE_CURRENT_VIEW":
      newState.currentView = action.data;
      return newState;
    case "ADD_VIEW":
      action.data.body =
        typeof action.data.body === "string"
          ? JSON.parse(action.data.body)
          : action.data.body;
      newState.viewList[action.data.type].unshift(action.data);
      return newState;
    case "UPDATE_VIEW":
      newState.viewList[action.data.type] = newState.viewList[
        action.data.type
      ].map((item: any) => {
        if (item.rowKey === action.data.rowKey) {
          return {
            ...action.data,
            body:
              typeof action.data.body === "string"
                ? JSON.parse(action.data.body)
                : action.data.body,
            isPublic: action.data.isPublic,
          };
        }
        return item;
      });
      return newState;
    case "REMOVE_VIEW":
      newState.viewList[action.data.viewFieldType] = newState.viewList[
        action.data.viewFieldType
      ].filter((item: any) => item.rowKey !== action.data.rowKey);
      return newState;
    case "CHANGE_VIEW":
      if (!newState.currentView) {
        newState.currentView = {};
      }
      newState.currentView.body = action.data;
      return newState;
    default:
      return state;
  }
};
