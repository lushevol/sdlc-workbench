import React, { ReactElement } from "react";
import Grid from "@mui/material/Grid";
import Root, { classes, PREFIX } from "./common/tile.style";
import { MenuItemProps, Tile as TileProps } from "./common/interface";
import Tile from "../Tile";
import useController from "./common/MenuItem.useController";

export const Item = (props: MenuItemProps, tile: TileProps) => {
  const { onClick } = useController(props, tile);
  return (
    <Grid item xs={3} key={tile.tile ? tile.tile : tile.title}>
      <Tile
        title={tile.title}
        subtitle={tile.subtitle ?? ""}
        onClick={onClick}
        imageDarkTheme={tile.imageDarkTheme}
        imageLightTheme={tile.imageLightTheme ?? tile.imageDarkTheme}
        disabled={tile.disabled}
      />
    </Grid>
  );
};

const MenuItem: React.FC<MenuItemProps> = (
  props: MenuItemProps
): ReactElement => {
  return (
    <Root data-testid={`${PREFIX}`}>
      <section className={classes.title}>{props.menuItems.label}</section>
      <Grid container spacing={2} className={classes.content}>
        {props.menuItems.tiles.map((item) => Item(props, item))}
      </Grid>
    </Root>
  );
};

export default React.memo(MenuItem);
