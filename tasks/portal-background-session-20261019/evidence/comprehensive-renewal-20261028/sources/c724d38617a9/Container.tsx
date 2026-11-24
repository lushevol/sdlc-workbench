import React, { ReactElement, Suspense } from "react";
import { Container as ContainerProps } from "../../../hooks/model/workspaces";
import Splash from "../../../components/Splash";
import ErrorBoundry from "../../../components/ErrorBoundry";
const AdminModule = React.lazy(() => import("../../../admin"));

const Container: React.FC<ContainerProps> = (
  props: ContainerProps
): ReactElement => {
  const Comp = React.useMemo(
    () => React.lazy(() => System.import(props.container)),
    []
  );
  return (
    <ErrorBoundry emailSupport={props.emailSupport}>
      <Suspense fallback={<Splash />}>
        {props.container === "@fm/base" ? (
          <AdminModule
            module={props.module}
            tile={props.tile}
            parameters={props.parameters ?? {}}
            panelId={props.panelId}
            tabId={props.tabId}
          />
        ) : (
          <Comp
            module={props.module}
            tile={props.tile}
            parameters={props.parameters ?? {}}
            panelId={props.panelId}
            tabId={props.tabId}
          />
        )}
      </Suspense>
    </ErrorBoundry>
  );
};

export default React.memo(Container);
