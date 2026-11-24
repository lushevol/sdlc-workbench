import { RootModel } from "../model/root";
import { IAction } from "./util/ActionType";
import rootReducer0 from "./root0.reducers";
import rootReducer from "./root.reducers";
import workspacesReducer from "./workspaces.reducers";
import { getHooks } from "..";
import { getHooksBase } from "../HooksBase";

export const reducers = (state: RootModel, action: IAction): RootModel => {
  Object.freeze(state);
  let store: RootModel = { ...state };
  store = rootReducer0(store, action);
  store = rootReducer(store, action);
  store = workspacesReducer(store, action);
  const hooksBase = getHooksBase();
  hooksBase.setStore({ ...store });
  const hooks = getHooks();
  hooks.setStore({ ...hooks.store, ...store });
  return store;
};
