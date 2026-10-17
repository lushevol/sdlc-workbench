import { z } from 'zod';

const WEB_PROMPTS = {
  WEB_SEARCH: {
    name: 'web-search',
    description: 'Search the web for current information using DuckDuckGo (no API key required). Returns titles, URLs, and text snippets.',
    arguments: [
      { name: 'query', description: 'The search query to look up on the web', required: true }
    ]
  },
  WEB_FETCH: {
    name: 'web-fetch',
    description: 'Fetch and read the plain-text content of a specific URL. Use this after web-search to read a result page in full.',
    arguments: [
      { name: 'url', description: 'The full HTTPS URL of the page to fetch', required: true }
    ]
  },
  WEB_CRAWL: {
    name: 'web-crawl',
    description: 'Crawl a website from a seed URL, following links within the same domain. Choose a mode: urls (URL list), summary (URL+title+snippet), full (URL+title+full text), or links (URL+outbound links).',
    arguments: [
      { name: 'url', description: 'The seed URL to start crawling from', required: true },
      { name: 'mode', description: 'Output mode: urls, summary, full, or links (default: urls)', required: false }
    ]
  },
  WEB_CRAWL_BROWSER: {
    name: 'web-crawl-browser',
    description: 'Crawl a JavaScript-rendered (SPA) website using the system Chrome or Edge browser. Use this when web_crawl returns empty results because the site uses React, Angular, or Vue. Requires Chrome or Edge installed.',
    arguments: [
      { name: 'url', description: 'The seed URL to start crawling from', required: true },
      { name: 'mode', description: 'Output mode: urls, summary (default), full, or links', required: false }
    ]
  }
};

const generateWebPromptMessage = (name, args, ctx) => {
  if (name === 'web-search') {
    return `Search the web for: "${args.query || '(enter your search query)'}"\n\nUse web_search with:\n- query: "${args.query || '(enter your search query)'}"\n\nThe tool will return titles, URLs, and text snippets from DuckDuckGo results.\nTo read a full page from the results, follow up with the web-fetch prompt or call web_fetch directly with the URL.`;
  }
  if (name === 'web-fetch') {
    return `Fetch the content of the following URL:\n${args.url || '(enter the URL to fetch)'}\n\nUse web_fetch with:\n- url: "${args.url || '(enter the URL)'}"\n\nThe tool will return the plain-text content of the page (up to 15,000 characters).`;
  }
  if (name === 'web-crawl') {
    const mode = args.mode || 'urls';
    return `Crawl the website at: ${args.url || '(enter the seed URL)'}\n\nUse web_crawl with:\n- url: "${args.url || '(enter the seed URL)'}"\n- mode: "${mode}" (urls | summary | full | links)\n- maxDepth: 3 (optional, default 3)\n- maxPages: 50 (optional, default 50)\n- delayMs: 500 (optional, delay between requests in ms)\n\nThe tool crawls within the same domain only. Use mode 'urls' for discovery, 'summary' for a quick overview, 'full' for complete page text, or 'links' to map the site structure.`;
  }
  if (name === 'web-crawl-browser') {
    const mode = args.mode || 'summary';
    return `Crawl the JavaScript-rendered website at: ${args.url || '(enter the seed URL)'}\n\nUse web_crawl_browser with:\n- url: "${args.url || '(enter the seed URL)'}"\n- mode: "${mode}" (urls | summary | full | links)\n- maxDepth: 2 (optional, recommended lower depth — browser is slower)\n- maxPages: 20 (optional, recommended lower page count)\n- delayMs: 1000 (optional, default 1000ms — allow JS to render)\n\nUse this instead of web_crawl when the site uses React, Angular, Vue, or any JavaScript framework. Requires Google Chrome or Microsoft Edge installed on the system.`;
  }
  return 'Unknown prompt';
};

const CONTEXTUAL_OPTIONAL_FIELDS = new Set([]);

export function configureWebPrompts(server, { getContext = () => null } = {}) {
  Object.values(WEB_PROMPTS).forEach(prompt => {
    const callback = async (args) => {
      const ctx = getContext();
      const message = generateWebPromptMessage(prompt.name, args ?? {}, ctx);
      return { messages: [{ role: 'user', content: { type: 'text', text: message } }] };
    };

    if (prompt.arguments.length === 0) {
      server.prompt(prompt.name, prompt.description, callback);
    } else {
      const argsSchema = Object.fromEntries(
        prompt.arguments.map(arg => [
          arg.name,
          (!arg.required || CONTEXTUAL_OPTIONAL_FIELDS.has(arg.name))
            ? z.string().optional().describe(arg.description)
            : z.string().describe(arg.description)
        ])
      );
      server.prompt(prompt.name, prompt.description, argsSchema, callback);
    }
  });
  console.error(`Registered ${Object.keys(WEB_PROMPTS).length} Web prompts`);
}

export { WEB_PROMPTS, generateWebPromptMessage };
