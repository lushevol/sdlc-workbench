
import { z } from "zod";
import axios from "axios";
import { HttpsProxyAgent } from 'https-proxy-agent';
import { URLSearchParams } from 'node:url';

// Tool names
const SCWIKI_TOOLS = {
  search: "scwiki_search",
  get_page: "scwiki_get_page",
  find_page: "scwiki_find_page",
  create_page: "scwiki_create_page",
  update_page: "scwiki_update_page",
  delete_page: "scwiki_delete_page",
  get_page_children: "scwiki_get_page_children",
  list_spaces: "scwiki_list_spaces",
  list_my_pages: "scwiki_list_my_pages",
  add_comment: "scwiki_add_comment",
  get_labels: "scwiki_get_labels",
  add_label: "scwiki_add_label",
  get_page_history: "scwiki_get_page_history",
  list_attachments: "scwiki_list_attachments"
};

/**
 * Returns Bearer auth headers for SC Wiki (XWiki).
 *
 * Unlike Confluence, XWiki's Token Authenticator REST calls needed no CSRF/form-token
 * bypass header in live testing — a Bearer-authenticated PUT succeeded with just this header set.
 */
function getAuthHeaders(token, contentType = 'application/json') {
  return {
    Authorization: `Bearer ${token}`,
    Accept: 'application/json',
    'Content-Type': contentType
  };
}

/**
 * Build a full Axios request config with auth headers and explicit proxy/agent settings.
 * @param {string} token - SC Wiki Bearer token
 * @param {string} [proxy] - Proxy URL or '' for direct; undefined falls back to env var
 * @param {string} [contentType] - Request Content-Type (defaults to application/json for GET/DELETE)
 */
function buildAxiosConfig(token, proxy, contentType) {
  const config = {
    headers: getAuthHeaders(token, contentType),
    proxy: false, // disable Axios's built-in proxy; we control the agent ourselves
  };
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
function checkConfig(scwikiConfig) {
  if (!scwikiConfig?.baseUrl || !scwikiConfig?.token) {
    return { content: [{ type: "text", text: "SC Wiki config missing. Please provide baseUrl and token." }], isError: true };
  }
  return null;
}

/** Format a caught error for logging/response text, tolerating non-Error rejection values. */
function formatError(error) {
  return error?.message ?? String(error);
}

/**
 * Split a dotted XWiki page reference (e.g. "Sandbox.S2B NG.WebHome") into an optional wiki
 * prefix, the chain of (possibly nested) space names, and the final page name. A literal dot
 * inside a space/page name must be escaped as "\." in the reference.
 * @param {string} reference
 * @returns {{ wiki: string|undefined, spaceSegments: string[], pageName: string }}
 */
function parsePageReference(reference) {
  if (!reference || typeof reference !== 'string') {
    throw new Error('Invalid page reference: expected a non-empty string like "Space.PageName".');
  }
  let ref = reference.trim();
  let wiki;
  const colonIndex = ref.indexOf(':');
  const firstDotIndex = ref.indexOf('.');
  if (colonIndex !== -1 && (firstDotIndex === -1 || colonIndex < firstDotIndex)) {
    wiki = ref.slice(0, colonIndex);
    ref = ref.slice(colonIndex + 1);
  }

  const rawParts = ref.split(/(?<!\\)\./).map(part => part.replaceAll(String.raw`\.`, '.'));
  if (rawParts.length < 2 || rawParts.some(part => part.length === 0)) {
    throw new Error(`Invalid page reference "${reference}" — expected format "Space.PageName" or "Space.NestedSpace.PageName".`);
  }

  const pageName = rawParts.at(-1);
  const spaceSegments = rawParts.slice(0, -1);
  return { wiki, spaceSegments, pageName };
}

/**
 * Build the "/wikis/{wiki}/spaces/{s1}/spaces/{s2}/.../pages/{page}" REST path for a reference.
 * @param {{ wiki: string|undefined, spaceSegments: string[], pageName: string }} parsed
 * @param {string} defaultWiki - wiki name to use when the reference has no "wiki:" prefix
 */
function buildPagePath(parsed, defaultWiki) {
  const wikiName = parsed.wiki || defaultWiki;
  const spacesPath = parsed.spaceSegments.map(s => `/spaces/${encodeURIComponent(s)}`).join('');
  return `/wikis/${encodeURIComponent(wikiName)}${spacesPath}/pages/${encodeURIComponent(parsed.pageName)}`;
}

/**
 * Parse a browser "/bin/view/Space/NestedSpace/Page" URL into a dotted page reference.
 * A URL with a trailing slash and no distinct final page segment defaults to page "WebHome"
 * (confirmed XWiki behavior: /bin/view/Sandbox/S2B%20NG/ resolves to Sandbox.S2B NG.WebHome).
 * @param {string} pageUrl
 * @returns {string} dotted page reference
 */
function parseViewUrl(pageUrl) {
  const viewPathRegex = /\/bin\/view\/([^?#]+)/;
  const match = viewPathRegex.exec(pageUrl);
  if (!match) {
    throw new Error(`Could not parse a "/bin/view/..." path from URL: ${pageUrl}`);
  }
  const rawPath = match[1];
  const endsWithSlash = rawPath.endsWith('/');
  const segments = rawPath.split('/').filter(Boolean).map(decodeURIComponent);
  if (segments.length === 0) {
    throw new Error(`No space/page segments found in URL: ${pageUrl}`);
  }
  const pageName = endsWithSlash ? 'WebHome' : segments.pop();
  return [...segments, pageName].map(s => s.replaceAll('.', String.raw`\.`)).join('.');
}

/**
 * Fetch a page's metadata + content by its dotted reference. Field set is the subset confirmed
 * present in live XWiki REST responses (not a full pass-through, unlike the listing endpoints
 * below whose exact JSON shape hasn't been individually verified).
 */
async function fetchPageByReference(scwikiConfig, reference) {
  const { baseUrl, token, wiki, proxy } = scwikiConfig;
  const parsed = parsePageReference(reference);
  const path = buildPagePath(parsed, wiki);
  const response = await axios.get(`${baseUrl}/rest${path}?media=json`, buildAxiosConfig(token, proxy));
  return pickPageFields(response.data, baseUrl);
}

/**
 * Cherry-pick the confirmed-stable subset of fields from a raw XWiki page JSON response.
 */
function pickPageFields(data, baseUrl) {
  const { id, fullName, wiki, space, name, title, version, content, syntax, parent, created, creator, modified, modifier, xwikiAbsoluteUrl } = data;
  return { id, fullName, wiki, space, name, title, version, content, syntax, parent, created, creator, modified, modifier, url: xwikiAbsoluteUrl || null, baseUrl };
}

/**
 * Create or update a page's title/content/parent via a form-urlencoded PUT — the only accepted
 * media type (besides raw XML) that lets title and content be set together in one request.
 */
async function putPageContent(scwikiConfig, reference, { title, content, parent } = {}) {
  const { baseUrl, token, wiki, proxy } = scwikiConfig;
  const parsed = parsePageReference(reference);
  const path = buildPagePath(parsed, wiki);

  const form = new URLSearchParams();
  if (title !== undefined) form.append('title', title);
  if (content !== undefined) form.append('content', content);
  if (parent !== undefined) form.append('parent', parent);

  const response = await axios.put(
    `${baseUrl}/rest${path}`,
    form.toString(),
    buildAxiosConfig(token, proxy, 'application/x-www-form-urlencoded')
  );
  return pickPageFields(response.data, baseUrl);
}

/**
 * Configure SC Wiki (XWiki) tools
 * @param {*} server
 * @param {Object} [scwikiConfig] - { baseUrl, token, wiki, proxy }
 */
function configureScwikiTools(server, scwikiConfig) {

  // Keyword search across page titles/content/names
  server.tool(
    SCWIKI_TOOLS.search,
    "Search SC Wiki pages by keyword across title, content, and page name.",
    {
      query: z.string().describe("Keywords to search for"),
      limit: z.number().optional().describe("Max number of results to return (default 10)")
    },
    async ({ query, limit = 10 }) => {
      const err = checkConfig(scwikiConfig);
      if (err) return err;
      try {
        const { baseUrl, token, wiki, proxy } = scwikiConfig;
        const url = `${baseUrl}/rest/wikis/${encodeURIComponent(wiki)}/search?q=${encodeURIComponent(query)}&scope=title,content,name&number=${limit}&media=json`;
        const response = await axios.get(url, buildAxiosConfig(token, proxy));
        return { content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }] };
      } catch (error) {
        console.error("Error searching SC Wiki:", formatError(error));
        return { content: [{ type: "text", text: formatError(error) }], isError: true };
      }
    }
  );

  // Get a page's metadata and content by its dotted reference
  server.tool(
    SCWIKI_TOOLS.get_page,
    "Get an SC Wiki page's metadata and content by its dotted reference (e.g. \"Sandbox.S2B NG.WebHome\").",
    {
      pageReference: z.string().describe("Dotted XWiki page reference, e.g. \"Space.PageName\" or \"Space.NestedSpace.PageName\"")
    },
    async ({ pageReference }) => {
      const err = checkConfig(scwikiConfig);
      if (err) return err;
      try {
        const page = await fetchPageByReference(scwikiConfig, pageReference);
        return { content: [{ type: "text", text: JSON.stringify(page, null, 2) }] };
      } catch (error) {
        console.error("Error getting SC Wiki page:", formatError(error));
        return { content: [{ type: "text", text: formatError(error) }], isError: true };
      }
    }
  );

  // Resolve a browser view URL to a page reference and fetch its metadata/content
  server.tool(
    SCWIKI_TOOLS.find_page,
    "Look up an SC Wiki page from its browser URL (e.g. .../bin/view/Sandbox/S2B%20NG/) and return its metadata and content.",
    {
      pageUrl: z.string().describe("Full SC Wiki page URL, e.g. https://scwiki.global.standardchartered.com/bin/view/Sandbox/S2B%20NG/")
    },
    async ({ pageUrl }) => {
      const err = checkConfig(scwikiConfig);
      if (err) return err;
      try {
        const reference = parseViewUrl(pageUrl);
        const page = await fetchPageByReference(scwikiConfig, reference);
        return { content: [{ type: "text", text: JSON.stringify({ pageReference: reference, ...page }, null, 2) }] };
      } catch (error) {
        console.error("Error resolving SC Wiki page URL:", formatError(error));
        return { content: [{ type: "text", text: formatError(error) }], isError: true };
      }
    }
  );

  // Create a new page (or overwrite one if it already exists — XWiki PUT is an upsert)
  server.tool(
    SCWIKI_TOOLS.create_page,
    "Create a new SC Wiki page at the given dotted reference. XWiki PUT is an upsert — an existing page at that reference will be overwritten.",
    {
      pageReference: z.string().describe("Dotted XWiki page reference for the new page, e.g. \"Space.NestedSpace.PageName\""),
      title: z.string().describe("Title for the new page"),
      content: z.string().optional().describe("Page content in XWiki syntax (defaults to empty page if omitted)")
    },
    async ({ pageReference, title, content = '' }) => {
      const err = checkConfig(scwikiConfig);
      if (err) return err;
      try {
        const page = await putPageContent(scwikiConfig, pageReference, { title, content });
        return { content: [{ type: "text", text: JSON.stringify(page, null, 2) }] };
      } catch (error) {
        console.error("Error creating SC Wiki page:", formatError(error));
        return { content: [{ type: "text", text: formatError(error) }], isError: true };
      }
    }
  );

  // Update the title and/or content of an existing page
  server.tool(
    SCWIKI_TOOLS.update_page,
    "Update the title and/or content of an existing SC Wiki page. At least one of title/content must be provided.",
    {
      pageReference: z.string().describe("Dotted XWiki page reference, e.g. \"Space.PageName\""),
      title: z.string().optional().describe("New page title (optional — keeps existing title if omitted)"),
      content: z.string().optional().describe("New page content in XWiki syntax (optional — keeps existing content if omitted)")
    },
    async ({ pageReference, title, content }) => {
      const err = checkConfig(scwikiConfig);
      if (err) return err;
      if (title === undefined && content === undefined) {
        return { content: [{ type: "text", text: "At least one of title or content must be provided." }], isError: true };
      }
      try {
        const page = await putPageContent(scwikiConfig, pageReference, { title, content });
        return { content: [{ type: "text", text: JSON.stringify(page, null, 2) }] };
      } catch (error) {
        console.error("Error updating SC Wiki page:", formatError(error));
        return { content: [{ type: "text", text: formatError(error) }], isError: true };
      }
    }
  );

  // Delete a page (with title confirmation), same confirm-by-title pattern as Confluence
  server.tool(
    SCWIKI_TOOLS.delete_page,
    "Delete an SC Wiki page by its dotted reference. The provided title must match the page's actual title exactly (confirmation check). The page is moved to the recycle bin, not permanently deleted.",
    {
      pageReference: z.string().describe("Dotted XWiki page reference, e.g. \"Space.PageName\""),
      title: z.string().describe("Page title for confirmation — must match the actual page title exactly")
    },
    async ({ pageReference, title }) => {
      const err = checkConfig(scwikiConfig);
      if (err) return err;
      try {
        const { baseUrl, token, wiki, proxy } = scwikiConfig;
        const parsed = parsePageReference(pageReference);
        const path = buildPagePath(parsed, wiki);
        const axiosConfig = buildAxiosConfig(token, proxy);

        const getResponse = await axios.get(`${baseUrl}/rest${path}?media=json`, axiosConfig);
        const actualTitle = getResponse.data.title;
        if (actualTitle !== title) {
          return {
            content: [{ type: "text", text: `Title mismatch: expected "${title}" but page has title "${actualTitle}". Delete cancelled.` }],
            isError: true
          };
        }

        await axios.delete(`${baseUrl}/rest${path}`, axiosConfig);
        return { content: [{ type: "text", text: JSON.stringify({ deleted: true, pageReference, title: actualTitle }, null, 2) }] };
      } catch (error) {
        console.error("Error deleting SC Wiki page:", formatError(error));
        return { content: [{ type: "text", text: formatError(error) }], isError: true };
      }
    }
  );

  // List the direct children of a page
  server.tool(
    SCWIKI_TOOLS.get_page_children,
    "List the direct child pages of an SC Wiki page by its dotted reference.",
    {
      pageReference: z.string().describe("Dotted XWiki page reference, e.g. \"Space.PageName\""),
      limit: z.number().optional().describe("Max number of children to return (default 25)")
    },
    async ({ pageReference, limit = 25 }) => {
      const err = checkConfig(scwikiConfig);
      if (err) return err;
      try {
        const { baseUrl, token, wiki, proxy } = scwikiConfig;
        const parsed = parsePageReference(pageReference);
        const path = buildPagePath(parsed, wiki);
        const response = await axios.get(`${baseUrl}/rest${path}/children?number=${limit}&media=json`, buildAxiosConfig(token, proxy));
        return { content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }] };
      } catch (error) {
        console.error("Error getting SC Wiki page children:", formatError(error));
        return { content: [{ type: "text", text: formatError(error) }], isError: true };
      }
    }
  );

  // List spaces in the configured wiki
  server.tool(
    SCWIKI_TOOLS.list_spaces,
    "List the top-level spaces in the configured SC Wiki instance.",
    {
      limit: z.number().optional().describe("Max spaces to return (default 50)")
    },
    async ({ limit = 50 }) => {
      const err = checkConfig(scwikiConfig);
      if (err) return err;
      try {
        const { baseUrl, token, wiki, proxy } = scwikiConfig;
        const url = `${baseUrl}/rest/wikis/${encodeURIComponent(wiki)}/spaces?number=${limit}&media=json`;
        const response = await axios.get(url, buildAxiosConfig(token, proxy));
        return { content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }] };
      } catch (error) {
        console.error("Error listing SC Wiki spaces:", formatError(error));
        return { content: [{ type: "text", text: formatError(error) }], isError: true };
      }
    }
  );

  // List pages created by the authenticated user (XWQL: doc.creator = <current user>)
  server.tool(
    SCWIKI_TOOLS.list_my_pages,
    "List SC Wiki pages created by the authenticated user.",
    {
      limit: z.number().optional().describe("Max number of pages to return (default 10)")
    },
    async ({ limit = 10 }) => {
      const err = checkConfig(scwikiConfig);
      if (err) return err;
      try {
        const { baseUrl, token, wiki, proxy } = scwikiConfig;
        const axiosConfig = buildAxiosConfig(token, proxy);

        const userResponse = await axios.get(`${baseUrl}/rest/wikis/${encodeURIComponent(wiki)}/user?media=json`, axiosConfig);
        const creatorId = userResponse.data.id || userResponse.data.username || userResponse.data.userReference;
        if (!creatorId) {
          return { content: [{ type: "text", text: "Could not resolve the authenticated user's identity from SC Wiki." }], isError: true };
        }

        const xwql = `where doc.creator = '${creatorId}'`;
        const url = `${baseUrl}/rest/wikis/${encodeURIComponent(wiki)}/query?q=${encodeURIComponent(xwql)}&type=xwql&number=${limit}&media=json`;
        const response = await axios.get(url, axiosConfig);
        return { content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }] };
      } catch (error) {
        console.error("Error listing my SC Wiki pages:", formatError(error));
        return { content: [{ type: "text", text: formatError(error) }], isError: true };
      }
    }
  );

  // Add a comment to a page
  server.tool(
    SCWIKI_TOOLS.add_comment,
    "Add a comment to an SC Wiki page.",
    {
      pageReference: z.string().describe("Dotted XWiki page reference, e.g. \"Space.PageName\""),
      text: z.string().describe("Comment text")
    },
    async ({ pageReference, text }) => {
      const err = checkConfig(scwikiConfig);
      if (err) return err;
      try {
        const { baseUrl, token, wiki, proxy } = scwikiConfig;
        const parsed = parsePageReference(pageReference);
        const path = buildPagePath(parsed, wiki);
        const form = new URLSearchParams({ text });
        const response = await axios.post(
          `${baseUrl}/rest${path}/comments`,
          form.toString(),
          buildAxiosConfig(token, proxy, 'application/x-www-form-urlencoded')
        );
        return { content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }] };
      } catch (error) {
        console.error("Error adding SC Wiki comment:", formatError(error));
        return { content: [{ type: "text", text: formatError(error) }], isError: true };
      }
    }
  );

  // Get all tags on a page
  server.tool(
    SCWIKI_TOOLS.get_labels,
    "Get all tags on an SC Wiki page.",
    {
      pageReference: z.string().describe("Dotted XWiki page reference, e.g. \"Space.PageName\"")
    },
    async ({ pageReference }) => {
      const err = checkConfig(scwikiConfig);
      if (err) return err;
      try {
        const { baseUrl, token, wiki, proxy } = scwikiConfig;
        const parsed = parsePageReference(pageReference);
        const path = buildPagePath(parsed, wiki);
        const response = await axios.get(`${baseUrl}/rest${path}/tags?media=json`, buildAxiosConfig(token, proxy));
        return { content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }] };
      } catch (error) {
        console.error("Error getting SC Wiki page tags:", formatError(error));
        return { content: [{ type: "text", text: formatError(error) }], isError: true };
      }
    }
  );

  // Add a tag to a page
  server.tool(
    SCWIKI_TOOLS.add_label,
    "Add a tag to an SC Wiki page.",
    {
      pageReference: z.string().describe("Dotted XWiki page reference, e.g. \"Space.PageName\""),
      tag: z.string().describe("Tag name")
    },
    async ({ pageReference, tag }) => {
      const err = checkConfig(scwikiConfig);
      if (err) return err;
      try {
        const { baseUrl, token, wiki, proxy } = scwikiConfig;
        const parsed = parsePageReference(pageReference);
        const path = buildPagePath(parsed, wiki);
        const form = new URLSearchParams({ tag });
        const response = await axios.put(
          `${baseUrl}/rest${path}/tags`,
          form.toString(),
          buildAxiosConfig(token, proxy, 'application/x-www-form-urlencoded')
        );
        return { content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }] };
      } catch (error) {
        console.error("Error adding SC Wiki page tag:", formatError(error));
        return { content: [{ type: "text", text: formatError(error) }], isError: true };
      }
    }
  );

  // Get a page's version history
  server.tool(
    SCWIKI_TOOLS.get_page_history,
    "Get the version history of an SC Wiki page.",
    {
      pageReference: z.string().describe("Dotted XWiki page reference, e.g. \"Space.PageName\""),
      limit: z.number().optional().describe("Max number of versions to return (default 25)")
    },
    async ({ pageReference, limit = 25 }) => {
      const err = checkConfig(scwikiConfig);
      if (err) return err;
      try {
        const { baseUrl, token, wiki, proxy } = scwikiConfig;
        const parsed = parsePageReference(pageReference);
        const path = buildPagePath(parsed, wiki);
        const response = await axios.get(`${baseUrl}/rest${path}/history?number=${limit}&media=json`, buildAxiosConfig(token, proxy));
        return { content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }] };
      } catch (error) {
        console.error("Error getting SC Wiki page history:", formatError(error));
        return { content: [{ type: "text", text: formatError(error) }], isError: true };
      }
    }
  );

  // List a page's attachments (metadata only — contents are not downloaded)
  server.tool(
    SCWIKI_TOOLS.list_attachments,
    "List the attachments on an SC Wiki page (name, size, MIME type — contents are not downloaded).",
    {
      pageReference: z.string().describe("Dotted XWiki page reference, e.g. \"Space.PageName\"")
    },
    async ({ pageReference }) => {
      const err = checkConfig(scwikiConfig);
      if (err) return err;
      try {
        const { baseUrl, token, wiki, proxy } = scwikiConfig;
        const parsed = parsePageReference(pageReference);
        const path = buildPagePath(parsed, wiki);
        const response = await axios.get(`${baseUrl}/rest${path}/attachments?media=json`, buildAxiosConfig(token, proxy));
        return { content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }] };
      } catch (error) {
        console.error("Error listing SC Wiki page attachments:", formatError(error));
        return { content: [{ type: "text", text: formatError(error) }], isError: true };
      }
    }
  );

}

export { SCWIKI_TOOLS, configureScwikiTools, parsePageReference, buildPagePath, parseViewUrl, checkConfig, formatError, buildAxiosConfig };
