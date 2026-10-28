import { Tile, Tiles } from "../components/Drawer/common/interface";
import { getHooksBase } from "../hooks/HooksBase";

export const findTile = (drawers, workspace) => {
  return findTileConfig(
    drawers,
    workspace.containers[0].container,
    workspace.containers[0].module,
    workspace.containers[0].tile
  );
};

export const findTileConfig = (drawers, _container, _module, _tile) => {
  let aggr: any = undefined;
  drawers?.every((category: Tiles) => {
    category.tiles?.every((tile: Tile) => {
      if (
        tile.container === _container &&
        tile.module === _module &&
        tile.tile === _tile
      ) {
        aggr = tile;
      }
      return !aggr;
    });
    return !aggr;
  });
  return aggr;
};

export const getSubject = (entities, tile) => {
  let aggr: any = undefined;
  entities.every((entity) => {
    if (entity.name === tile.entity || tile.entity?.includes(entity.name)) {
      entity.subjects.every((subject) => {
        if (subject.name === tile.subject) {
          aggr = subject;
        }
        return !aggr;
      });
    }
    return !aggr;
  });
  return aggr;
};

export const setTabPanel = (
  value,
  index,
  setIsHidden,
  setIsHidden2,
  isTabPanelLoaded,
  setIsTabPanelLoaded
) => {
  if (value === index) {
    setIsHidden(false);
    const to = setTimeout(() => {
      if (!isTabPanelLoaded) {
        setIsTabPanelLoaded(true);
      }
      setIsHidden2(false);
      clearTimeout(to);
    }, 600);
  } else {
    setIsHidden(true);
    setIsHidden2(true);
  }
};

export const getTile = (workspaces, tabId) => {
  const { store } = getHooksBase();
  const index = workspaces.findIndex((workspace) => workspace.id === tabId);
  if (index < 0) return undefined;
  const workspace = workspaces[index];
  return findTile(store.drawers, workspace);
};
