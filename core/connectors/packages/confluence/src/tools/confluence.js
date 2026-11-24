
import { z } from "zod";
import axios from "axios";
import { HttpsProxyAgent } from 'https-proxy-agent';

// Tool names
const CONF_TOOLS = {
  list_my_confluence_pages: "confluence_list_my_pages",
  search: "confluence_search",
  update_page: "confluence_update_page",
  get_page_id: "confluence_get_page_id",
  create_page: "confluence_create_page",
  read_page: "confluence_read_page",
  get_page: "confluence_get_page",
  find_page: "confluence_find_page",
  get_page_children: "confluence_get_page_children",
  list_spaces: "confluence_list_spaces",
  get_space: "confluence_get_space",
  delete_page: "confluence_delete_page",
  add_comment: "confluence_add_comment",
  get_labels: "confluence_get_labels",
  add_label: "confluence_add_label"
};

/**
 * Returns Bearer auth headers for Confluence.
 *
 * X-Atlassian-Token: no-check bypasses Confluence's XSRF check, which otherwise
 * rejects state-changing requests (POST/PUT/DELETE) from non-browser clients like
 * this one with a bare 403 Forbidden — even with a valid, correctly-scoped PAT.
 * GET requests are unaffected by XSRF checks, which is why reads succeed while
 * writes (e.g. add_comment, create_page) fail with 403.
 */
function getAuthHeaders(token) {
  return {
    Authorization: `Bearer ${token}`,
    Accept: 'application/json',
    'Content-Type': 'application/json',
    'X-Atlassian-Token': 'no-check'
  };
}

/**
 * Build a full Axios request config with auth headers and explicit proxy/agent settings.
 *
 * Pass `proxy` explicitly (from confluenceConfig.proxy) rather than relying on the
 * HTTPS_PROXY environment variable, which is set to the ADO proxy route and may not
 * reach Confluence. An empty string ('') means direct connection (no proxy).
 * Undefined falls back to the env var for backward compatibility.
 *
 * Axios's built-in https_proxy env-var handling uses its own CONNECT tunnel implementation
 * which can fail against certain corporate proxies (502 Bad Gateway). Using HttpsProxyAgent
 * directly — the same approach as the proxy probe — avoids this issue.
 *
 * @param {string} token - Confluence Bearer token
 * @param {string} [proxy] - Proxy URL or '' for direct; undefined falls back to env var
 */
function buildAxiosConfig(token, proxy) {
  const config = {
    headers: getAuthHeaders(token),
    proxy: false, // disable Axios's built-in proxy; we control the agent ourselves
  };
  // If proxy explicitly provided ('' or URL), use it directly.
  // If undefined (not yet passed), fall back to env var for backward compatibility.
  const proxyUrl = proxy === undefined ? (process.env.HTTPS_PROXY || process.env.https_proxy || '') : proxy;
  if (proxyUrl) {
    config.httpsAgent = new HttpsProxyAgent(proxyUrl);
  }
  return config;
}

/**
 * Guard: returns an error response if config is missing required fields.
 * Returns null if config is valid.
 */
function checkConfig(confluenceConfig) {
  if (!confluenceConfig || !confluenceConfig.baseUrl || !confluenceConfig.token) {
    return { content: [{ type: "text", text: "Confluence config missing. Please provide baseUrl and token." }], isError: true };
  }
  return null;
}

/**
 * Configure Confluence tools
 * @param {*} server
 * @param {Object} [confluenceConfig] - { baseUrl, token }
 */
function configureConfTools(server, confluenceConfig) {

  // List pages created by the authenticated user (CQL: creator=currentUser())
  server.tool(
    CONF_TOOLS.list_my_confluence_pages,
    "List Confluence pages created by the authenticated user.",
    {
      limit: z.number().optional().describe("Max number of pages to return (default 10)"),
      spaceKey: z.string().optional().describe("Confluence space key to filter by (optional)")
    },
    async ({ limit = 10, spaceKey }) => {
      const err = checkConfig(confluenceConfig);
      if (err) return err;
      try {
        const { baseUrl, token } = confluenceConfig;
        let cql = 'creator=currentUser()+AND+type=page';
        if (spaceKey) cql += `+AND+space.key="${encodeURIComponent(spaceKey)}"`;
        const url = `${baseUrl}/rest/api/content/search?cql=${cql}&limit=${limit}&expand=version,history`;
        const response = await axios.get(url, buildAxiosConfig(token, confluenceConfig.proxy));
        const pages = response.data.results || [];
        return { content: [{ type: "text", text: JSON.stringify(pages, null, 2) }] };
      } catch (error) {
        console.error("Error listing Confluence pages:", error?.message ?? String(error));
        return { content: [{ type: "text", text: error && error.message ? error.message : String(error) }], isError: true };
      }
    }
  );

  // Search Confluence pages with an arbitrary CQL query
  server.tool(
    CONF_TOOLS.search,
    "Search Confluence content using a CQL (Confluence Query Language) query.",
    {
      cql: z.string().describe("CQL query string, e.g. 'type=page AND space.key=\"TEAM\"'"),
      limit: z.number().optional().describe("Max number of results to return (default 10)")
    },
    async ({ cql, limit = 10 }) => {
      const err = checkConfig(confluenceConfig);
      if (err) return err;
      try {
        const { baseUrl, token } = confluenceConfig;
        const url = `${baseUrl}/rest/api/content/search?cql=${encodeURIComponent(cql)}&limit=${limit}&expand=version,space,history`;
        const response = await axios.get(url, buildAxiosConfig(token, confluenceConfig.proxy));
        const results = response.data.results || [];
        return { content: [{ type: "text", text: JSON.stringify(results, null, 2) }] };
      } catch (error) {
        console.error("Error searching Confluence:", error?.message ?? String(error));
        return { content: [{ type: "text", text: error && error.message ? error.message : String(error) }], isError: true };
      }
    }
  );

  // Update the content of an existing Confluence page
  server.tool(
    CONF_TOOLS.update_page,
    "Update the content of an existing Confluence page. Body must be in Confluence Storage Format (XHTML).",
    {
      pageId: z.string().describe("Confluence page ID (numeric string)"),
      body: z.string().describe("New page body in Confluence Storage Format (XHTML)"),
      title: z.string().optional().describe("New page title (optional — keeps existing title if omitted)")
    },
    async ({ pageId, body, title }) => {
      const err = checkConfig(confluenceConfig);
      if (err) return err;
      try {
        const { baseUrl, token } = confluenceConfig;
        const axiosConfig = buildAxiosConfig(token, confluenceConfig.proxy);

        // Step 1: fetch current version and title
        const getResponse = await axios.get(`${baseUrl}/rest/api/content/${pageId}`, axiosConfig);
        const currentVersion = getResponse.data.version.number;
        const currentTitle = getResponse.data.title;

        // Step 2: update page with incremented version
        const putResponse = await axios.put(
          `${baseUrl}/rest/api/content/${pageId}`,
          {
            version: { number: currentVersion + 1 },
            title: title || currentTitle,
            type: 'page',
            body: {
              storage: {
                value: body,
                representation: 'storage'
              }
            }
          },
          axiosConfig
        );

        return { content: [{ type: "text", text: JSON.stringify(putResponse.data, null, 2) }] };
      } catch (error) {
        console.error("Error updating Confluence page:", error?.message ?? String(error));
        return { content: [{ type: "text", text: error && error.message ? error.message : String(error) }], isError: true };
      }
    }
  );

  // Resolve a Confluence page URL to its page ID and metadata
  server.tool(
    CONF_TOOLS.get_page_id,
    "Look up a Confluence page ID and metadata from its URL. Useful when you know the page URL but need the page ID for other tools like confluence_update_page.",
    {
      pageUrl: z.string().describe("Full Confluence page URL (e.g. https://confluence.example.com/wiki/spaces/TEAM/pages/123456789/Page+Title)")
    },
    async ({ pageUrl }) => {
      const err = checkConfig(confluenceConfig);
      if (err) return err;
      try {
        const { baseUrl, token } = confluenceConfig;

        // Strategy 1: extract page ID from URL — supports:
        //   viewpage.action?pageId=XXXXXXX  (classic Server format)
        //   /pages/XXXXXXX/Title            (Cloud format)
        const pageIdFromUrl =
          pageUrl.match(/[?&]pageId=(\d+)/)?.[1] ??
          pageUrl.match(/\/pages\/(\d+)/)?.[1];

        if (pageIdFromUrl) {
          const getResponse = await axios.get(
            `${baseUrl}/rest/api/content/${pageIdFromUrl}?expand=space,version`,
            buildAxiosConfig(token, confluenceConfig.proxy)
          );
          const { id, title, space, version, _links } = getResponse.data;
          return {
            content: [{
              type: "text",
              text: JSON.stringify({ id, title, space: space?.key, version: version?.number, url: _links?.webui ? `${baseUrl}${_links.webui}` : pageUrl }, null, 2)
            }]
          };
        }

        // Strategy 2: Server-style URL — derive title from URL and search via CQL
        const titleMatch = pageUrl.match(/\/display\/([^/]+)\/(.+)/);
        if (titleMatch) {
          const spaceKey = decodeURIComponent(titleMatch[1]);
          const titleRaw = decodeURIComponent(titleMatch[2].replaceAll('+', ' '));
          const cql = `type=page AND space.key="${spaceKey}" AND title="${titleRaw}"`;
          const searchResponse = await axios.get(
            `${baseUrl}/rest/api/content/search?cql=${encodeURIComponent(cql)}&limit=1&expand=space,version`,
            buildAxiosConfig(token, confluenceConfig.proxy)
          );
          const results = searchResponse.data.results || [];
          if (results.length === 0) {
            return { content: [{ type: "text", text: `No page found matching URL: ${pageUrl}` }], isError: true };
          }
          const { id, title, space, version, _links } = results[0];
          return {
            content: [{
              type: "text",
              text: JSON.stringify({ id, title, space: space?.key, version: version?.number, url: _links?.webui ? `${baseUrl}${_links.webui}` : pageUrl }, null, 2)
            }]
          };
        }

        return { content: [{ type: "text", text: `Could not parse page ID from URL: ${pageUrl}. Expected format: .../pages/viewpage.action?pageId=123456789, .../pages/123456789/Title, or .../display/SPACE/Title` }], isError: true };
      } catch (error) {
        console.error("Error resolving Confluence page URL:", error?.message ?? String(error));
        return { content: [{ type: "text", text: error?.message ?? String(error) }], isError: true };
      }
    }
  );

  // Create a new Confluence page as a child of a parent page identified by URL
  server.tool(
    CONF_TOOLS.create_page,
    "Create a new Confluence page under a parent page. Pass the parent page URL — the tool will resolve the parent ID and space automatically.",
    {
      parentPageUrl: z.string().describe("Full URL of the parent Confluence page (e.g. https://confluence.example.com/wiki/spaces/TEAM/pages/123456789/Parent+Title)"),
      title: z.string().describe("Title for the new page"),
      body: z.string().optional().describe("Page body in Confluence Storage Format (XHTML). Defaults to an empty page if omitted.")
    },
    async ({ parentPageUrl, title, body = '<p></p>' }) => {
      const err = checkConfig(confluenceConfig);
      if (err) return err;
      try {
        const { baseUrl, token } = confluenceConfig;
        const axiosConfig = buildAxiosConfig(token, confluenceConfig.proxy);

        // Step 1: Resolve parent page ID from URL
        // Strategy 1: URL contains numeric ID — viewpage.action?pageId= or /pages/{id}
        let parentId;
        let spaceKey;

        const parentPageIdFromUrl =
          parentPageUrl.match(/[?&]pageId=(\d+)/)?.[1] ??
          parentPageUrl.match(/\/pages\/(\d+)/)?.[1];

        if (parentPageIdFromUrl) {
          parentId = parentPageIdFromUrl;
          const parentResponse = await axios.get(
            `${baseUrl}/rest/api/content/${parentId}?expand=space`,
            axiosConfig
          );
          spaceKey = parentResponse.data.space?.key;
        } else {
          // Strategy 2: Server-style URL — /display/SPACE/Title
          const titleMatch = parentPageUrl.match(/\/display\/([^/]+)\/(.+)/);
          if (!titleMatch) {
            return { content: [{ type: "text", text: `Could not parse parent page ID from URL: ${parentPageUrl}. Expected format: .../pages/viewpage.action?pageId=123456789, .../pages/123456789/Title, or .../display/SPACE/Title` }], isError: true };
          }
          spaceKey = decodeURIComponent(titleMatch[1]);
          const titleRaw = decodeURIComponent(titleMatch[2].replaceAll('+', ' '));
          const cql = `type=page AND space.key="${spaceKey}" AND title="${titleRaw}"`;
          const searchResponse = await axios.get(
            `${baseUrl}/rest/api/content/search?cql=${encodeURIComponent(cql)}&limit=1&expand=space`,
            axiosConfig
          );
          const results = searchResponse.data.results || [];
          if (results.length === 0) {
            return { content: [{ type: "text", text: `No parent page found matching URL: ${parentPageUrl}` }], isError: true };
          }
          parentId = results[0].id;
        }

        // Step 2: POST new child page
        const postResponse = await axios.post(
          `${baseUrl}/rest/api/content`,
          {
            type: 'page',
            title,
            ancestors: [{ id: parentId }],
            space: { key: spaceKey },
            body: {
              storage: {
                value: body,
                representation: 'storage'
              }
            }
          },
          axiosConfig
        );

        const { id, title: createdTitle, space, _links } = postResponse.data;
        return {
          content: [{
            type: "text",
            text: JSON.stringify({
              id,
              title: createdTitle,
              space: space?.key,
              url: _links?.webui ? `${baseUrl}${_links.webui}` : null
            }, null, 2)
          }]
        };
      } catch (error) {
        console.error("Error creating Confluence page:", error?.message ?? String(error));
        return { content: [{ type: "text", text: error?.message ?? String(error) }], isError: true };
      }
    }
  );

  // Read the full content of a Confluence page given its URL
  server.tool(
    CONF_TOOLS.read_page,
    "Read the full content of a Confluence page from its URL. Accepts both Cloud-style (/wiki/spaces/SPACE/pages/{id}/Title) and Server-style (/display/SPACE/Title) URLs.",
    {
      pageUrl: z.string().describe("Full Confluence page URL (Cloud or Server-style)")
    },
    async ({ pageUrl }) => {
      const err = checkConfig(confluenceConfig);
      if (err) return err;
      try {
        const { baseUrl, token } = confluenceConfig;
        const axiosConfig = buildAxiosConfig(token, confluenceConfig.proxy);
        let pageId;

        // Strategy 1: extract page ID from URL — supports:
        //   viewpage.action?pageId=XXXXXXX  (classic Server format)
        //   /pages/XXXXXXX/Title            (Cloud format)
        pageId =
          pageUrl.match(/[?&]pageId=(\d+)/)?.[1] ??
          pageUrl.match(/\/pages\/(\d+)/)?.[1];

        if (!pageId) {
          // Strategy 2: Server-style URL — /display/SPACE/Title, resolve via CQL
          const titleMatch = pageUrl.match(/\/display\/([^/]+)\/(.+)/);
          if (!titleMatch) {
            return { content: [{ type: "text", text: `Could not parse page ID from URL: ${pageUrl}. Expected format: .../pages/viewpage.action?pageId=123456789, .../pages/123456789/Title, or .../display/SPACE/Title` }], isError: true };
          }
          const spaceKey = decodeURIComponent(titleMatch[1]);
          const titleRaw = decodeURIComponent(titleMatch[2].replaceAll('+', ' '));
          const cql = `type=page AND space.key="${spaceKey}" AND title="${titleRaw}"`;
          const searchResponse = await axios.get(
            `${baseUrl}/rest/api/content/search?cql=${encodeURIComponent(cql)}&limit=1`,
            axiosConfig
          );
          const results = searchResponse.data.results || [];
          if (results.length === 0) {
            return { content: [{ type: "text", text: `No page found matching URL: ${pageUrl}` }], isError: true };
          }
          pageId = results[0].id;
        }

        const response = await axios.get(
          `${baseUrl}/rest/api/content/${pageId}?expand=body.view,body.storage,body.export_view,space,version,history`,
          axiosConfig
        );
        const { id, title, space, version, body, _links } = response.data;
        return {
          content: [{
            type: "text",
            text: JSON.stringify({
              id,
              title,
              space: space?.key,
              version: version?.number,
              url: _links?.webui ? `${baseUrl}${_links.webui}` : pageUrl,
              body: {
                view: body?.view?.value,
                storage: body?.storage?.value,
                export_view: body?.export_view?.value
              }
            }, null, 2)
          }]
        };
      } catch (error) {
        console.error("Error reading Confluence page:", error?.message ?? String(error));
        return { content: [{ type: "text", text: error?.message ?? String(error) }], isError: true };
      }
    }
  );

  // Get a Confluence page by its numeric ID
  server.tool(
    CONF_TOOLS.get_page,
    "Get a Confluence page by its ID. Returns content in view, storage, and export_view formats (export_view captures tab content).",
    {
      pageId: z.string().describe("Confluence page ID (numeric string)")
    },
    async ({ pageId }) => {
      const err = checkConfig(confluenceConfig);
      if (err) return err;
      try {
        const { baseUrl, token } = confluenceConfig;
        const response = await axios.get(
          `${baseUrl}/rest/api/content/${pageId}?expand=body.view,body.storage,body.export_view,space,version,history`,
          buildAxiosConfig(token, confluenceConfig.proxy)
        );
        const { id, title, space, version, body, _links } = response.data;
        return {
          content: [{
            type: "text",
            text: JSON.stringify({
              id,
              title,
              space: space?.key,
              version: version?.number,
              url: _links?.webui ? `${baseUrl}${_links.webui}` : null,
              body: {
                view: body?.view?.value,
                storage: body?.storage?.value,
                export_view: body?.export_view?.value
              }
            }, null, 2)
          }]
        };
      } catch (error) {
        console.error("Error getting Confluence page:", error?.message ?? String(error));
        return { content: [{ type: "text", text: error?.message ?? String(error) }], isError: true };
      }
    }
  );

  // Find a Confluence page by space key and title
  server.tool(
    CONF_TOOLS.find_page,
    "Find a Confluence page by space key and exact title. Returns page metadata including ID.",
    {
      spaceKey: z.string().describe("Confluence space key (e.g. TEAM, PLAT)"),
      title: z.string().describe("Exact page title to search for")
    },
    async ({ spaceKey, title }) => {
      const err = checkConfig(confluenceConfig);
      if (err) return err;
      try {
        const { baseUrl, token } = confluenceConfig;
        const cql = `type=page AND space.key="${spaceKey}" AND title="${title}"`;
        const response = await axios.get(
          `${baseUrl}/rest/api/content/search?cql=${encodeURIComponent(cql)}&limit=1&expand=version,space,history`,
          buildAxiosConfig(token, confluenceConfig.proxy)
        );
        const results = response.data.results || [];
        if (results.length === 0) {
          return { content: [{ type: "text", text: `No page found with title "${title}" in space "${spaceKey}"` }], isError: true };
        }
        const { id, title: foundTitle, space, version, _links } = results[0];
        return {
          content: [{
            type: "text",
            text: JSON.stringify({
              id,
              title: foundTitle,
              space: space?.key,
              version: version?.number,
              url: _links?.webui ? `${baseUrl}${_links.webui}` : null
            }, null, 2)
          }]
        };
      } catch (error) {
        console.error("Error finding Confluence page:", error?.message ?? String(error));
        return { content: [{ type: "text", text: error?.message ?? String(error) }], isError: true };
      }
    }
  );

  // Get child pages of a Confluence page
  server.tool(
    CONF_TOOLS.get_page_children,
    "List the child pages of a Confluence page by its ID.",
    {
      pageId: z.string().describe("Confluence page ID (numeric string)"),
      limit: z.number().optional().describe("Max number of children to return (default 25)")
    },
    async ({ pageId, limit = 25 }) => {
      const err = checkConfig(confluenceConfig);
      if (err) return err;
      try {
        const { baseUrl, token } = confluenceConfig;
        const response = await axios.get(
          `${baseUrl}/rest/api/content/${pageId}/child/page?expand=version,space&limit=${limit}`,
          buildAxiosConfig(token, confluenceConfig.proxy)
        );
        const children = (response.data.results || []).map(({ id, title, space, _links }) => ({
          id,
          title,
          space: space?.key,
          url: _links?.webui ? `${baseUrl}${_links.webui}` : null
        }));
        return { content: [{ type: "text", text: JSON.stringify(children, null, 2) }] };
      } catch (error) {
        console.error("Error getting Confluence page children:", error?.message ?? String(error));
        return { content: [{ type: "text", text: error?.message ?? String(error) }], isError: true };
      }
    }
  );

  // List Confluence spaces
  server.tool(
    CONF_TOOLS.list_spaces,
    "List Confluence spaces (global spaces by default).",
    {
      limit: z.number().optional().describe("Max spaces to return (default 50)")
    },
    async ({ limit = 50 }) => {
      const err = checkConfig(confluenceConfig);
      if (err) return err;
      try {
        const { baseUrl, token } = confluenceConfig;
        const response = await axios.get(
          `${baseUrl}/rest/api/space?type=global&expand=description.plain&limit=${limit}`,
          buildAxiosConfig(token, confluenceConfig.proxy)
        );
        const spaces = (response.data.results || []).map(({ key, name, type, _links }) => ({
          key,
          name,
          type,
          url: _links?.webui ? `${baseUrl}${_links.webui}` : null
        }));
        return { content: [{ type: "text", text: JSON.stringify(spaces, null, 2) }] };
      } catch (error) {
        console.error("Error listing Confluence spaces:", error?.message ?? String(error));
        return { content: [{ type: "text", text: error?.message ?? String(error) }], isError: true };
      }
    }
  );

  // Get a Confluence space by key
  server.tool(
    CONF_TOOLS.get_space,
    "Get details of a Confluence space by its key.",
    {
      spaceKey: z.string().describe("Confluence space key (e.g. TEAM, PLAT)")
    },
    async ({ spaceKey }) => {
      const err = checkConfig(confluenceConfig);
      if (err) return err;
      try {
        const { baseUrl, token } = confluenceConfig;
        const response = await axios.get(
          `${baseUrl}/rest/api/space/${spaceKey}?expand=description.plain,homepage,metadata.labels`,
          buildAxiosConfig(token, confluenceConfig.proxy)
        );
        const { key, name, type, description, homepage, _links } = response.data;
        return {
          content: [{
            type: "text",
            text: JSON.stringify({
              key,
              name,
              type,
              description: description?.plain?.value,
              homepageId: homepage?.id,
              url: _links?.webui ? `${baseUrl}${_links.webui}` : null
            }, null, 2)
          }]
        };
      } catch (error) {
        console.error("Error getting Confluence space:", error?.message ?? String(error));
        return { content: [{ type: "text", text: error?.message ?? String(error) }], isError: true };
      }
    }
  );

  // Delete a Confluence page (with title confirmation)
  server.tool(
    CONF_TOOLS.delete_page,
    "Delete a Confluence page by ID. The provided title must match the page's actual title exactly (confirmation check).",
    {
      pageId: z.string().describe("Confluence page ID (numeric string)"),
      title: z.string().describe("Page title for confirmation — must match the actual page title exactly")
    },
    async ({ pageId, title }) => {
      const err = checkConfig(confluenceConfig);
      if (err) return err;
      try {
        const { baseUrl, token } = confluenceConfig;
        const axiosConfig = buildAxiosConfig(token, confluenceConfig.proxy);

        // Step 1: Fetch page to verify title matches
        const getResponse = await axios.get(`${baseUrl}/rest/api/content/${pageId}`, axiosConfig);
        const actualTitle = getResponse.data.title;
        if (actualTitle !== title) {
          return {
            content: [{ type: "text", text: `Title mismatch: expected "${title}" but page has title "${actualTitle}". Delete cancelled.` }],
            isError: true
          };
        }

        // Step 2: DELETE the page
        await axios.delete(`${baseUrl}/rest/api/content/${pageId}`, axiosConfig);
        return {
          content: [{ type: "text", text: JSON.stringify({ deleted: true, id: pageId, title: actualTitle }, null, 2) }]
        };
      } catch (error) {
        console.error("Error deleting Confluence page:", error?.message ?? String(error));
        return { content: [{ type: "text", text: error?.message ?? String(error) }], isError: true };
      }
    }
  );

  // Add a page-level comment to a Confluence page
  server.tool(
    CONF_TOOLS.add_comment,
    "Add a page-level comment to a Confluence page. Body must be in Confluence Storage Format (XHTML).",
    {
      pageId: z.string().describe("Confluence page ID (numeric string)"),
      body: z.string().describe("Comment body in Confluence Storage Format (XHTML)")
    },
    async ({ pageId, body }) => {
      const err = checkConfig(confluenceConfig);
      if (err) return err;
      try {
        const { baseUrl, token } = confluenceConfig;
        const postResponse = await axios.post(
          `${baseUrl}/rest/api/content`,
          {
            type: "comment",
            container: { id: pageId, type: "page" },
            body: {
              storage: {
                value: body,
                representation: "storage"
              }
            }
          },
          buildAxiosConfig(token, confluenceConfig.proxy)
        );
        const { id, _links } = postResponse.data;
        return {
          content: [{
            type: "text",
            text: JSON.stringify({
              id,
              pageId,
              url: _links?.webui ? `${baseUrl}${_links.webui}` : null
            }, null, 2)
          }]
        };
      } catch (error) {
        console.error("Error adding Confluence comment:", error?.message ?? String(error));
        return { content: [{ type: "text", text: error?.message ?? String(error) }], isError: true };
      }
    }
  );

  // Get labels on a Confluence page
  server.tool(
    CONF_TOOLS.get_labels,
    "Get all labels on a Confluence page.",
    {
      pageId: z.string().describe("Confluence page ID (numeric string)")
    },
    async ({ pageId }) => {
      const err = checkConfig(confluenceConfig);
      if (err) return err;
      try {
        const { baseUrl, token } = confluenceConfig;
        const response = await axios.get(
          `${baseUrl}/rest/api/content/${pageId}/label`,
          buildAxiosConfig(token, confluenceConfig.proxy)
        );
        const labels = response.data.results || [];
        return { content: [{ type: "text", text: JSON.stringify(labels, null, 2) }] };
      } catch (error) {
        console.error("Error getting Confluence page labels:", error?.message ?? String(error));
        return { content: [{ type: "text", text: error?.message ?? String(error) }], isError: true };
      }
    }
  );

  // Add a label to a Confluence page
  server.tool(
    CONF_TOOLS.add_label,
    "Add a label to a Confluence page.",
    {
      pageId: z.string().describe("Confluence page ID (numeric string)"),
      label: z.string().describe("Label name (lowercase, no spaces)")
    },
    async ({ pageId, label }) => {
      const err = checkConfig(confluenceConfig);
      if (err) return err;
      try {
        const { baseUrl, token } = confluenceConfig;
        const response = await axios.post(
          `${baseUrl}/rest/api/content/${pageId}/label`,
          [{ prefix: "global", name: label }],
          buildAxiosConfig(token, confluenceConfig.proxy)
        );
        const labels = response.data.results || [];
        return { content: [{ type: "text", text: JSON.stringify(labels, null, 2) }] };
      } catch (error) {
        console.error("Error adding Confluence page label:", error?.message ?? String(error));
        return { content: [{ type: "text", text: error?.message ?? String(error) }], isError: true };
      }
    }
  );

}

export { CONF_TOOLS, configureConfTools };
