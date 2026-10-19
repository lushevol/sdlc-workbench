import { Hooks } from ".";
import { initialData, RootModel } from "./model/root";
import { IAction } from "./reducer/util/ActionType";

export interface HooksBase extends Hooks {
  baseDispatch: React.Dispatch<IAction>;
  setBaseDispatch: (dispacth: React.Dispatch<IAction>) => void;
}

export const hooksBase: HooksBase = {
  store: initialData,
  setStore(store: RootModel) {
    this.store = store;
  },
  baseDispatch: () => {
    console.info("baseDispatch");
  },
  setBaseDispatch(dispatch: React.Dispatch<IAction>) {
    this.baseDispatch = dispatch;
  },
};

export const getHooksBase = () => hooksBase;
