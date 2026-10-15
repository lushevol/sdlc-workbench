import React, { ReactElement } from "react";
import { hooksBase } from "../HooksBase";
import { RootModel, ProviderPropsDefault, initialData } from "../model/root";
import { reducers } from "../reducer";
import { IAction } from "../reducer/util/ActionType";

export const emptyFunction = () => {
  console.info("AppContext");
};

export const AppContext = React.createContext<
  [RootModel, React.Dispatch<IAction>]
>([initialData, emptyFunction]);
export const useContext = (): [RootModel, React.Dispatch<IAction>] =>
  React.useContext(AppContext);

const Provider: React.FC<ProviderPropsDefault> = (
  props: ProviderPropsDefault
): ReactElement => {
  const [store, dispatch] = React.useReducer(reducers, {
    ...initialData,
    ...props.data,
  });
  React.useEffect(() => {
    hooksBase.setBaseDispatch(dispatch);
    hooksBase.setStore(store);
  }, []);
  const data: any = React.useMemo(() => [store, dispatch], [store, dispatch]);
  return (
    <AppContext.Provider value={data}>{props.children}</AppContext.Provider>
  );
};

export default Provider;
