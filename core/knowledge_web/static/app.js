(() => {
  const state = { navigation: null, docs: new Map(), current: null, raw: false, graph: false, documentRequest: 0, searchRequest: 0 };
  const $ = (id) => document.getElementById(id);
  const escapeHtml = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const api = async (path) => {
    const response = await fetch(path);
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || 'The request could not be read.');
    return payload;
  };
  const notify = (message = '') => { $('notice').textContent = message; $('notice').classList.toggle('hidden', !message); };
  const localLink = (target, text) => `<a href="#" data-target="${escapeHtml(target)}">${text}</a>`;
  const headingText = (tokens) => tokens.map((token) => token.tokens ? headingText(token.tokens) : token.text || '').join('');

  const renderMarkdown = (source) => {
    const headings = [], seen = new Map();
    const renderer = new marked.Marked({
      gfm: true,
      renderer: {
        html({ text }) { return escapeHtml(text); },
        link({ href, title, tokens }) {
          const label = this.parser.parseInline(tokens);
          const target = String(href || '').trim();
          const compact = target.replace(/[\u0000-\u0020\u007f]/g, '');
          if (/^[a-z][a-z0-9+.-]*:/i.test(compact) || compact.startsWith('//')) {
            if (!/^(https?:|mailto:|\/\/)/i.test(compact)) return `<span class="unavailable" title="Unsupported link">${label}</span>`;
            return `<a href="${escapeHtml(target)}"${title ? ` title="${escapeHtml(title)}"` : ''} target="_blank" rel="noopener noreferrer">${label}</a>`;
          }
          return localLink(target, label);
        },
        image({ text }) { return `<span class="missing-asset" role="note">Image unavailable${text ? `: ${escapeHtml(text)}` : ''}</span>`; },
        heading({ tokens, depth }) {
          const text = headingText(tokens);
          let slug = text.toLowerCase().replace(/[^\p{L}\p{N}\p{M}_ -]/gu, '').trim().replace(/ /g, '-') || 'section';
          const occurrence = seen.get(slug) || 0; seen.set(slug, occurrence + 1);
          if (occurrence) slug += `-${occurrence}`;
          headings.push({ level: depth, text, slug });
          return `<h${depth} id="${escapeHtml(slug)}">${this.parser.parseInline(tokens)}</h${depth}>\n`;
        },
      },
      extensions: [{
        name: 'emptyAnchor', level: 'inline',
        start(source) { return source.search(/<a\s/i); },
        tokenizer(source) {
          const match = /^<a\s+(?:id|name)\s*=\s*(["'])([^"']+)\1\s*>\s*<\/a>/i.exec(source);
          if (match) return { type: 'emptyAnchor', raw: match[0], anchor: match[2] };
          return undefined;
        },
        renderer(token) { return `<span id="${escapeHtml(token.anchor)}"></span>`; },
      }, {
        name: 'wikilink', level: 'inline',
        start(source) { return source.indexOf('[['); },
        tokenizer(source) {
          const match = /^\[\[([^\]\n]+)\]\]/.exec(source);
          if (!match) return undefined;
          const [target, ...label] = match[1].split('|');
          if (!target.trim()) return undefined;
          return { type: 'wikilink', raw: match[0], target: target.trim(), text: label.join('|').trim() || target.trim() };
        },
        renderer(token) { return localLink(`wiki:${token.target}`, escapeHtml(token.text)); },
      }],
    });
    const body = source.replace(/^---\r?\n[\s\S]*?\r?\n---(?:\r?\n|$)/, '');
    return { html: renderer.parse(body), headings };
  };

  const metadataHtml = (metadata) => Object.entries(metadata || {}).map(([key, value]) => `<dt>${escapeHtml(key)}</dt><dd>${key === 'full_text' && typeof value === 'string' ? localLink(value, escapeHtml(value)) : escapeHtml(typeof value === 'string' ? value : JSON.stringify(value))}</dd>`).join('');
  const rawHtml = (content) => `<pre class="raw">${content.split(/\r?\n/).map((line, index) => `<span class="source-line" id="L${index + 1}" data-line="${index + 1}">${escapeHtml(line) || ' '}</span>`).join('\n')}</pre>`;
  const scrollToFragment = (fragment) => {
    if (!fragment) { window.scrollTo({ top: 0 }); return; }
    let decoded; try { decoded = decodeURIComponent(fragment.replace(/^#/, '')); } catch { decoded = fragment; }
    const lines = /^L(\d+)(?:-L?(\d+))?$/.exec(decoded);
    if (!lines && state.raw && state.current) { state.raw = false; displayDocumentBody(state.current); }
    if (lines && state.current) {
      state.raw = true; $('article-body').innerHTML = rawHtml(state.current.content); $('raw-toggle').textContent = 'Rendered view';
      const start = Number(lines[1]), end = Number(lines[2] || lines[1]);
      $('article-body').querySelectorAll('.source-line').forEach((line) => line.classList.toggle('highlight', Number(line.dataset.line) >= start && Number(line.dataset.line) <= end));
      decoded = `L${start}`;
    }
    const target = document.getElementById(decoded);
    if (target) target.scrollIntoView({ block: 'start' });
    else notify(`This document has no section named “${decoded}”.`);
  };

  const displayDocumentBody = (doc) => {
    const rendered = renderMarkdown(doc.content);
    $('article-body').innerHTML = state.raw ? rawHtml(doc.content) : rendered.html;
    $('raw-toggle').textContent = state.raw ? 'Rendered view' : 'Raw source';
    $('document-title').classList.toggle('hidden', rendered.headings.some((heading) => heading.level === 1));
    $('article-body').querySelectorAll('table').forEach((table) => { const wrapper = document.createElement('div'); wrapper.className = 'table-wrap'; table.replaceWith(wrapper); wrapper.append(table); });
    const toc = rendered.headings.map((heading) => `<a class="level-${heading.level}" href="#${escapeHtml(heading.slug)}" data-fragment="${escapeHtml(heading.slug)}">${escapeHtml(heading.text)}</a>`).join('') || '<span class="muted">No headings</span>';
    $('details').innerHTML = `<h3>Identity</h3><dl><dt>Collection</dt><dd>${escapeHtml(doc.collection)}</dd><dt>Path</dt><dd>${escapeHtml(doc.path)}</dd><dt>Bytes</dt><dd>${doc.bytes}</dd><dt>SHA-256</dt><dd>${escapeHtml(doc.sha256)}</dd></dl><h3>Metadata</h3><dl>${metadataHtml(doc.metadata)}</dl><h3>Contents</h3><nav class="toc">${toc}</nav>`;
  };
  const hideBrowse = () => { $('shell').classList.remove('browse-open'); $('browse-toggle').setAttribute('aria-expanded', 'false'); };
  const markCurrent = () => {
    document.querySelectorAll('.doc-link').forEach((link) => {
      const active = !state.graph && link.dataset.key === state.current?.key;
      link.classList.toggle('active', active);
      if (active) { link.setAttribute('aria-current', 'page'); let folder = link.parentElement; while (folder) { if (folder.tagName === 'DETAILS') folder.open = true; folder = folder.parentElement; } }
      else link.removeAttribute('aria-current');
    });
    $('graph-button').classList.toggle('active', state.graph);
    $('graph-button').setAttribute('aria-pressed', String(state.graph));
  };

  const openDocument = async (key, push = true, fragment = '') => {
    const request = ++state.documentRequest;
    try {
      const doc = await api(`/api/document?key=${encodeURIComponent(key)}`);
      if (request !== state.documentRequest) return;
      state.current = doc; state.raw = false; state.graph = false; notify();
      if (push) history.pushState({}, '', `?key=${encodeURIComponent(key)}${fragment ? `#${fragment}` : ''}`);
      document.title = `${doc.title} · Knowledge`;
      $('welcome').classList.add('hidden'); $('graph-view').classList.add('hidden'); $('article').classList.remove('hidden'); $('shell').classList.remove('show-graph');
      const meta = doc.metadata || {};
      const authority = doc.collection === 'wiki' ? 'Derived wiki' : doc.collection === 'records' ? 'Canonical record' : doc.collection === 'guide' ? 'Knowledge guide' : 'Source material';
      const badges = [authority, meta.type, meta.status, meta.governance_state].filter(Boolean);
      $('article').innerHTML = `<div class="crumb">${escapeHtml(doc.path)}</div><div class="article-actions"><button id="raw-toggle">Raw source</button><button id="copy-link">Copy link</button></div><div class="meta-bar">${badges.map((badge) => `<span class="badge${['draft', 'candidate', 'contested', 'stale'].includes(badge) ? ' warning' : ''}">${escapeHtml(badge)}</span>`).join('')}</div>${doc.collection === 'wiki' ? '<p class="authority-note">Derived navigation. Open the canonical sources for intent, status, and evidence.</p>' : ''}<h1 id="document-title">${escapeHtml(doc.title)}</h1><details class="inline-metadata"><summary>Document metadata</summary><dl>${metadataHtml(meta) || '<dt>No frontmatter</dt>'}</dl></details><div id="article-body"></div>`;
      displayDocumentBody(doc); markCurrent(); hideBrowse(); scrollToFragment(fragment);
      $('raw-toggle').onclick = () => { state.raw = !state.raw; displayDocumentBody(doc); };
      $('copy-link').onclick = async () => { try { await navigator.clipboard.writeText(location.href); notify('Document link copied.'); } catch { notify('Copy the document URL from the address bar.'); } };
    } catch (error) { if (request === state.documentRequest) notify(error.message); }
  };

  const openGraph = async (push = true) => {
    const request = ++state.documentRequest;
    try {
      const graph = await api('/api/graph');
      if (request !== state.documentRequest) return;
      state.graph = true; notify();
      if (push) history.pushState({}, '', '?view=graph');
      document.title = 'Wiki graph · Knowledge';
      $('welcome').classList.add('hidden'); $('article').classList.add('hidden'); $('graph-view').classList.remove('hidden'); $('shell').classList.add('show-graph');
      $('graph-content').innerHTML = graph.available ? `<iframe title="Wiki relationship graph" src="${escapeHtml(graph.url)}" sandbox="allow-scripts" referrerpolicy="no-referrer"></iframe>` : `<div class="graph-empty"><h2>Wiki graph unavailable</h2><p>${escapeHtml(graph.reason || 'The existing wiki graph has not been generated.')}</p><p>Generate it through the existing wiki workflow, then refresh this view.</p></div>`;
      markCurrent(); hideBrowse(); window.scrollTo({ top: 0 });
    } catch (error) { if (request === state.documentRequest) notify(error.message); }
  };

  const relativePath = (doc) => doc.path.replace(/^knowledge\/(?:records\/|llm-wiki\/wiki\/|evidence\/)?/, '');
  const docButton = (doc) => `<button class="doc-link" data-key="${escapeHtml(doc.key)}" title="${escapeHtml(doc.path)}"><span>${escapeHtml(doc.title)}</span><small>${escapeHtml(doc.id || doc.path.split('/').pop())}</small></button>`;
  const renderTree = (documents) => {
    const tree = { documents: [], folders: new Map() };
    for (const doc of documents) {
      const parts = relativePath(doc).split('/'); parts.pop(); let node = tree;
      for (const part of parts) { if (!node.folders.has(part)) node.folders.set(part, { documents: [], folders: new Map() }); node = node.folders.get(part); }
      node.documents.push(doc);
    }
    const order = { summaries: 0, concepts: 1, entities: 2, explorations: 3 };
    const render = (node) => node.documents.slice().sort((a, b) => {
      const index = (doc) => /\/(index|README)\.md$/i.test(doc.path) ? 0 : 1;
      return index(a) - index(b) || a.title.localeCompare(b.title);
    }).map(docButton).join('') + [...node.folders].sort(([a], [b]) => (order[a] ?? 4) - (order[b] ?? 4) || a.localeCompare(b)).map(([name, folder]) => `<details class="folder"${name === 'candidates' ? ' open' : ''}><summary>${escapeHtml(name)}</summary><div class="folder-content">${render(folder)}</div></details>`).join('');
    return render(tree);
  };
  const renderNavigation = () => {
    const collections = state.navigation.collections || [], previousScope = $('scope').value;
    $('count').textContent = `${state.navigation.health.documents} documents`;
    $('scope').innerHTML = '<option value="">All knowledge</option>' + collections.map((collection) => `<option value="${escapeHtml(collection.id)}">${escapeHtml(collection.label)}</option>`).join('');
    if (collections.some((collection) => collection.id === previousScope)) $('scope').value = previousScope;
    const order = { records: 0, wiki: 1, evidence: 2, guide: 3 };
    $('collections').innerHTML = collections.slice().sort((a, b) => (order[a.id] ?? 4) - (order[b.id] ?? 4)).map((collection) => `<details class="collection"${['records', 'wiki'].includes(collection.id) ? ' open' : ''}><summary>${escapeHtml(collection.label)} <span class="collection-count">${collection.count}</span></summary><div class="doc-list">${renderTree(collection.documents)}</div></details>`).join('');
    markCurrent();
  };

  const doSearch = async () => {
    const request = ++state.searchRequest;
    const query = $('search').value.trim();
    if (query.length < 2) { $('search-panel').classList.add('hidden'); return; }
    try {
      const payload = await api(`/api/search?q=${encodeURIComponent(query)}&collection=${encodeURIComponent($('scope').value)}&limit=30`);
      if (request !== state.searchRequest) return;
      $('search-panel').classList.remove('hidden');
      $('results').innerHTML = payload.results.length ? payload.results.map((result) => `<button class="search-result" data-key="${escapeHtml(result.key)}"><strong>${escapeHtml(result.title)}</strong><small>${escapeHtml(result.collection)} / ${escapeHtml(result.path)}</small><span>${escapeHtml(result.snippet)}</span></button>`).join('') : '<p class="empty-results">No matches in the selected knowledge collections.</p>';
      $('search-limit').textContent = payload.results.length === 30 ? 'Showing up to 30 matches. Refine your search to see other results.' : `${payload.results.length} matches`;
    } catch (error) { if (request === state.searchRequest) notify(error.message); }
  };

  const navigateLocation = () => {
    const query = new URLSearchParams(location.search);
    if (query.get('view') === 'graph') return openGraph(false);
    const first = [...state.docs.values()].find((doc) => doc.path === 'knowledge/records/candidates/index.md') || [...state.docs.values()].find((doc) => doc.path === 'knowledge/records/index.md') || [...state.docs.values()].find((doc) => doc.path === 'knowledge/llm-wiki/wiki/index.md') || state.docs.values().next().value;
    if (query.get('key')) return openDocument(query.get('key'), false, location.hash.slice(1));
    if (first) { history.replaceState({}, '', `?key=${encodeURIComponent(first.key)}`); return openDocument(first.key, false); }
  };
  const loadNavigation = async () => {
    state.navigation = await api('/api/navigation'); state.docs.clear();
    state.navigation.collections.flatMap((collection) => collection.documents).forEach((doc) => state.docs.set(doc.key, doc)); renderNavigation();
  };
  const boot = async () => {
    try { await loadNavigation(); await navigateLocation(); } catch (error) { notify(error.message); }
  };
  $('collections').addEventListener('click', (event) => { const button = event.target.closest('[data-key]'); if (button) openDocument(button.dataset.key); });
  $('results').addEventListener('click', (event) => { const button = event.target.closest('[data-key]'); if (button) { ++state.searchRequest; $('search-panel').classList.add('hidden'); openDocument(button.dataset.key); } });
  $('article').addEventListener('click', async (event) => {
    const link = event.target.closest('a[data-target]'); if (!link) return;
    event.preventDefault(); const key = state.current?.key;
    if (!key) return;
    try {
      const target = await api(`/api/resolve?from=${encodeURIComponent(key)}&target=${encodeURIComponent(link.dataset.target)}`);
      if (key !== state.current?.key || state.graph) return;
      await openDocument(target.key, true, String(target.fragment || '').replace(/^#/, ''));
    } catch { notify(`This destination is unavailable in the knowledge folder: ${link.dataset.target.replace(/^wiki:/, '')}`); }
  });
  $('details').addEventListener('click', async (event) => {
    const source = event.target.closest('[data-target]');
    if (source) {
      event.preventDefault();
      try { const target = await api(`/api/resolve?from=${encodeURIComponent(state.current.key)}&target=${encodeURIComponent(source.dataset.target)}`); await openDocument(target.key, true, target.fragment || ''); }
      catch { notify(`This source is unavailable in the knowledge folder: ${source.dataset.target}`); }
      return;
    }
    const link = event.target.closest('[data-fragment]'); if (!link) return;
    event.preventDefault(); history.replaceState({}, '', `?key=${encodeURIComponent(state.current.key)}#${encodeURIComponent(link.dataset.fragment)}`); scrollToFragment(link.dataset.fragment);
  });
  $('search').addEventListener('input', doSearch); $('scope').addEventListener('change', doSearch);
  $('close-search').onclick = () => { ++state.searchRequest; $('search-panel').classList.add('hidden'); $('search').focus(); };
  $('graph-button').onclick = () => openGraph();
  $('graph-refresh').onclick = () => openGraph(false);
  $('browse-toggle').onclick = () => { const open = $('shell').classList.toggle('browse-open'); $('browse-toggle').setAttribute('aria-expanded', String(open)); };
  $('refresh').onclick = async () => {
    $('refresh').disabled = true;
    try { await api('/api/refresh'); await loadNavigation(); await navigateLocation(); notify('Knowledge refreshed.'); } catch (error) { notify(error.message); }
    finally { $('refresh').disabled = false; }
  };
  document.addEventListener('keydown', (event) => {
    if (event.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) { event.preventDefault(); $('search').focus(); }
    if (event.key === 'Escape') { ++state.searchRequest; $('search-panel').classList.add('hidden'); hideBrowse(); }
  });
  window.addEventListener('popstate', navigateLocation); boot();
})();
