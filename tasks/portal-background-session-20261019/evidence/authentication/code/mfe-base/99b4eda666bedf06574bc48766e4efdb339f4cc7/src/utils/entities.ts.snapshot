import { Tile, Tiles } from "../components/Drawer/common/interface";

export const getEntities = (drawers: Tiles[] | undefined) => {
  const entities = (drawers ?? []).reduce<Record<string, 1>>(
    (aggr, categories) => {
    categories.tiles.forEach((tile: Tile) => {
      tile?.entity?.forEach((entity) => {
        aggr[entity] = 1;
      });
    });
    return aggr;
      },
    {}
  );
  return entities;
};
