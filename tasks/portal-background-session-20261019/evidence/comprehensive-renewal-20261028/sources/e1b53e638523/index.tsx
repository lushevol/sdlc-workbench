import React from "react";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import useController from "./common/useController";
import Button from "../../components/LoadingButton";
import { TimeoutProps } from "./common/interface";

const Timeout: React.FC<TimeoutProps> = (
  props: TimeoutProps
): React.ReactElement => {
  const { continuLogout, extend, loading } = useController(props);
  return (
    <Dialog
      open={true}
      aria-labelledby="timeout-dialog-title"
      aria-describedby="timeout-dialog-description"
    >
      <DialogTitle id="timeout-dialog-title">
        Your session has been expired
      </DialogTitle>
      <DialogContent>
        <DialogContentText id="timeout-dialog-description">
          Do you want to logout or extend the session?
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button
          onClick={extend}
          autoFocus
          variant="contained"
          data-testid="Extend_Btn"
          loading={loading}
        >
          Extend
        </Button>
        <Button
          onClick={continuLogout}
          variant="outlined"
          data-testid="Logout_Btn"
          loading={loading}
        >
          Logout
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default React.memo(Timeout);
