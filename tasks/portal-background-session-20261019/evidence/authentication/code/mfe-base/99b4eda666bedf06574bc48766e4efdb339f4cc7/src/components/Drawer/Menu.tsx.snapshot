import React, { ReactElement, Suspense } from "react";
import Box from "@mui/material/Box";
import ErrorBoundry from "../ErrorBoundry";
import { DrawerProps, Tiles } from "./common/interface";
import Splash from "../Splash";
const MenuItem = React.lazy(() => import("./MenuItem"));

const Menu: React.FC<DrawerProps> = (props: DrawerProps): ReactElement => {
  return (
    <ErrorBoundry>
      <Box sx={{ width: 883, padding: "36px" }}>
        <Suspense fallback={<Splash />}>
          {props.drawers?.map((menuItems: Tiles) => {
            return (
              <MenuItem
                key={menuItems.label}
                addTile={props.addTile}
                menuItems={menuItems}
              />
            );
          })}
        </Suspense>
      </Box>
    </ErrorBoundry>
  );
};

export default React.memo(Menu);
