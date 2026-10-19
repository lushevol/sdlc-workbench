import React, { ReactElement, Suspense } from "react";
import useController from "./common/useController";
import PageLoader from "../components/Loader/PageLoader";
import Splash from "../components/Splash";
import Root, { classes, PREFIX } from "./common/style";
import Snackbar from "../components/Snackbar";
import Login from "../pages/Login";
import { Entity } from "../hooks/model/root";

const Home = React.lazy(() => import("../pages/Home"));
export const RoutingComponent = (
  token: string | undefined,
  entities: Entity[] | undefined
) =>
  token && entities ? <Home /> : <Login />;

const Routing: React.FC = (_props): ReactElement => {
  const { store, handleCloseErrorMessage, isReady } = useController();
  if (!isReady) {
    return (
      <Root className={classes.root} data-testid={`${PREFIX}`}>
        <PageLoader />
      </Root>
    );
  }
  return (
    <Root className={classes.root} data-testid={`${PREFIX}`}>
      <Suspense fallback={<Splash />}>
        {RoutingComponent(store.token, store.entities)}
      </Suspense>
      {store.isLoading && <PageLoader />}
      {store.errorMsg && (
        <Snackbar
          open={!!store.errorMsg}
          onClose={handleCloseErrorMessage}
          message={store?.errorMsg}
          variant="standard"
          severity="error"
        />
      )}
    </Root>
  );
};

export default Routing;
