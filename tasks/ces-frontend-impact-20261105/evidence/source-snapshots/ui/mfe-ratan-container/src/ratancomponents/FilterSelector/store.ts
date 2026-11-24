import { createContext } from "react";
import { deepClone } from "../../ratanutils/utils";
import {
  getFilterList,
  getFilterDetails,
  putUpdateFilter,
  postSaveFilter,
  deleteFilter,
} from "../../ratanutils/http/api";
import { getUser } from "../../ratanutils/authenticator";
import { getEnable } from "../../ratanutils/componentEnabling";

export const defaultState: any = {
  filterList: {},
  currentFilter: null,
  temporaryFilter: {},
};
export const Context = createContext(defaultState);
const list: any = {};

// Action
export const getFilters = (type: string) => {
  const { id, role } = getUser();

  const params = getEnable("Filter_Builder_POC", type)
    ? {
        type: type,
        creator: id,
        assignee: role,
        moduleOwner: role,
        searchAll: true,
      }
    : {
        type: type,
        owner: id,
        searchAll: true,
      };

  return getFilterList(params).then((res: any) => {
    list[type] = res;
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

export const getFilter = (rowKey: string, type: string) => {
  return getFilterDetails(rowKey, type).then((res: any) => {
    res.body = JSON.parse(res.body);
    return res;
  });
};

export const saveFilter = ({
  rowKey,
  name,
  assigneeList,
  moduleOwner,
  body,
  filterFieldType,
}) => {
  const { id } = getUser();
  const promise = rowKey
    ? putUpdateFilter.bind(null, rowKey)
    : postSaveFilter.bind(null);

  const params = getEnable("Filter_Builder_POC", filterFieldType)
    ? {
        name,
        creator: id.toString(),
        body: JSON.stringify(body),
        type: filterFieldType,
        assigneeList,
        moduleOwner,
        isPublic: false,
      }
    : {
        name,
        owner: id.toString(),
        body: JSON.stringify(body),
        type: filterFieldType,
        isPublic: false,
      };

  return promise(params);
};

export const removeFilter = ({ rowKey, moduleOwner }, filterFieldType) => {
  const { id } = getUser();
  const params = getEnable("Filter_Builder_POC", filterFieldType)
    ? {
        rowKey,
        creator: id.toString(),
        moduleOwner,
      }
    : rowKey;
  return deleteFilter(params, filterFieldType);
};

// Reducer
export const reducer = (state: any, action: any) => {
  const newState = deepClone(state);
  switch (action.type) {
    case "UPDATE_FILTERS":
      newState.filterList = action.data;
      return newState;
    case "UPDATE_CURRENT_FILTER":
      newState.currentFilter = action.data;
      if (action.data) {
        newState.temporaryFilter = action.data;
      }
      return newState;
    case "UPDATE_TEMPORARY_FILTER":
      newState.temporaryFilter = {
        ...newState.temporaryFilter,
        ...action.data,
      };
      return newState;
    case "RESET_TEMPORARY_FILTER":
      newState.temporaryFilter = { body: state.bodyDefaultValue };
      return newState;
    case "CHANGE_FILTER":
      newState.filterList[action.data.type] = newState.filterList[
        action.data.type
      ].map((item: any) => {
        if (item.rowKey === action.data.rowKey) {
          return action.data;
        }
        return item;
      });
      return newState;
    case "ADD_FILTER":
      newState.filterList[action.data.type].unshift(action.data);
      return newState;
    case "REMOVE_FILTER":
      newState.filterList[action.data.filterFieldType] = newState.filterList[
        action.data.filterFieldType
      ].filter((item: any) => item.rowKey !== action.data.rowKey);
      return newState;
    default:
      return state;
  }
};
