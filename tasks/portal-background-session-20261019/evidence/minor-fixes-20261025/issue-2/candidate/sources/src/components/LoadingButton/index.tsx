import React, { ReactElement } from "react";
import Button from "@mui/material/Button";
import { LoadingButtonProps } from "./interface";
import CircularProgress from "@mui/material/CircularProgress";

const LoadingButton: React.FC<LoadingButtonProps> = (
  props: LoadingButtonProps
): ReactElement => {
  const { loading, children, loadingSize, ...others } = props;
  const ls = loadingSize ?? 14;
  return loading ? (
    <Button {...others} disabled>
      <CircularProgress
        color="inherit"
        size={ls}
        style={{ marginRight: `${ls}px` }}
      />
      {children}
    </Button>
  ) : (
    <Button {...others}>
      <span style={{ width: `${ls}px` }}></span>
      {children}
      <span style={{ width: `${ls}px` }}></span>
    </Button>
  );
};

export default LoadingButton;
