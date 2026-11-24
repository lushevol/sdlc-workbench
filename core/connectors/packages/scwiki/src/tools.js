import { configureScwikiTools as configureScwikiToolsImpl } from './tools/scwiki.js';

export function configureScwikiTools(server, scwikiConfig) {
  configureScwikiToolsImpl(server, scwikiConfig);
}
