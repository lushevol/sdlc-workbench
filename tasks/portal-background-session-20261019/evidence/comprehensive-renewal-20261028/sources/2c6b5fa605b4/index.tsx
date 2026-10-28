import React, { ReactElement } from "react";
import TextField from "@mui/material/TextField";
import { TabProps } from "./common/interface";
import IconButton from "@mui/material/IconButton";
import DeleteIcon from "@mui/icons-material/Delete";
import RefreshIcon from "@mui/icons-material/Refresh";
import Tooltip from "@mui/material/Tooltip";
import Root, { classes, PREFIX } from "./common/style";
import indonesiaIcon from "../Drawer/common/Indonesia.svg";

const entryIconByName: Record<string, { alt: string; src: string }> = {
  indonesia: {
    alt: "Indonesia icon",
    src: indonesiaIcon,
  },
};

const getEntryIcon = (entryName?: string | null) => {
  const getEntryName = entryName?.trim().toLowerCase();

  return getEntryName ? entryIconByName[getEntryName] : undefined;
};

const TabItem: React.FC<TabProps> = (props: TabProps): ReactElement => {
  const { item, edit, remove, refreshTab, showRemove, showRefresh } = props;
  const firstContainer = item?.containers?.[0];
  const entryIcon = getEntryIcon(firstContainer?.entryName);

  return (
    <Tooltip title={item.label} placement="top-start">
      <Root data-testid={`${PREFIX}`}>
        {entryIcon && (
          <img
            src={entryIcon.src}
            alt={entryIcon.alt}
            className={classes.entryIcon}
          />
        )}
        <div className={classes.textBoxOutter}>
          <TextField
            id={`edit-${item.id}`}
            data-testid={`edit-${item.id}`}
            value={item.label}
            variant="standard"
            onChange={edit(item)}
            fullWidth={true}
            className={classes.textBox}
            onClick={() => {
              document.getElementById(`edit-${item.id}`)?.blur();
            }}
            inputProps={{ "aria-label": "Workspace Name" }}
          />
        </div>
        {showRefresh && (
          <IconButton
            id={`refreshWorkspace-${item.id}`}
            data-testid={`refreshWorkspace-${item.id}`}
            aria-label="refresh"
            size="medium"
            className={classes.button}
            onClick={refreshTab(item)}
          >
            <RefreshIcon fontSize="small" />
          </IconButton>
        )}
        {showRemove && (
          <IconButton
            id={`deleteWorkspace-${item.id}`}
            data-testid={`deleteWorkspace-${item.id}`}
            aria-label="delete"
            size="medium"
            onClick={remove(item)}
            className={classes.button}
          >
            <DeleteIcon fontSize="small" />
          </IconButton>
        )}
      </Root>
    </Tooltip>
  );
};

export default React.memo(TabItem);
