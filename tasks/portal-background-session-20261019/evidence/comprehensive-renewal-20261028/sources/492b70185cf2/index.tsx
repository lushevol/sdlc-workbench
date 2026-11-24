import React, { ReactElement } from "react";
import { TabPanelProps } from "./common/interface";
import ErrorBoundry from "../ErrorBoundry";
import { setTabPanel } from "../../utils/drawer";

const TabPanel: React.FC<TabPanelProps> = (
  props: TabPanelProps
): ReactElement => {
  const { children, value, index, isActive, ...other } = props;
  const [isHidden, setIsHidden] = React.useState(true);
  const [isHidden2, setIsHidden2] = React.useState(true);
  const [isTabPanelLoaded, setIsTabPanelLoaded] = React.useState(false);
  React.useEffect(() => {
    setTabPanel(
      value,
      index,
      setIsHidden,
      setIsHidden2,
      isTabPanelLoaded,
      setIsTabPanelLoaded
    );
  }, [value, index]);

  return (
    <div
      role="tabpanel"
      hidden={isHidden}
      id={`workspaces-tabpanel-${index}`}
      data-testid={`workspaces-tabpanel-${index}`}
      {...other}
    >
      <div
        hidden={isHidden2}
        className="tabmain"
        style={{ position: "relative" }}
      >
        <ErrorBoundry>{isTabPanelLoaded && <>{children}</>}</ErrorBoundry>
      </div>
    </div>
  );
};
export function a11yProps(index: string) {
  return {
    id: `workspaces-tab-${index}`,
    "data-testid": `workspaces-tab-${index}`,
  };
}

export default React.memo(TabPanel);
