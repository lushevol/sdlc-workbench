(() => {
  const state = { navigation: null, docs: new Map(), current: null, raw: false };
  const $ = (id) => document.getElementById(id);
  const escapeHtml = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const safeUrl = (value) => { const raw = String(value || '').trim(); return /^(javascript|data|vbscript):/i.test(raw) ? '#' : raw; };

  const wikiKey = (target) => {
    const clean = target.replace(/^\.?\//, '').replace(/\.md$/, '');
    return [...state.docs.values()].find((doc) => doc.collection === 'wiki' && (doc.path.endsWith(`${clean}.md`) || doc.path.endsWith(clean)))?.key;
  };

  const inline = (source) => {
    const tokens = [];
    const token = (html) => { const marker = `\u0000${tokens.length}\u0000`; tokens.push(html); return marker; };
    let value = String(source).replace(/`([^`]+)`/g, (_, code) => token(`<code>${escapeHtml(code)}</code>`));
    value = value.replace(/\[\[([^\]|#]+)(?:\|([^\]]+))?\]\]/g, (_, target, label) => {
      const key = wikiKey(target.trim());
      return token(key ? `<a href="?key=${encodeURIComponent(key)}">${escapeHtml(label || target)}</a>` : `<span title="Unresolved wiki link">${escapeHtml(label || target)}</span>`);
    });
    value = value.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, label, href) => token(`<a href="${escapeHtml(safeUrl(href))}">${escapeHtml(label)}</a>`));
    value = escapeHtml(value).replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>').replace(/~~([^~]+)~~/g, '<del>$1</del>').replace(/\*([^*]+)\*/g, '<em>$1</em>');
    return value.replace(/\u0000(\d+)\u0000/g, (_, id) => tokens[Number(id)]);
  };

  const renderTable = (rows) => {
    const cells = (line) => line.trim().replace(/^\||\|$/g, '').split('|').map((cell) => inline(cell.trim()));
    const head = cells(rows[0]);
    const body = rows.slice(2).map((row) => `<tr>${cells(row).map((cell) => `<td>${cell}</td>`).join('')}</tr>`).join('');
    return `<div class="table-wrap"><table><thead><tr>${head.map((cell) => `<th scope="col">${cell}</th>`).join('')}</tr></thead><tbody>${body}</tbody></table></div>`;
  };

  const renderMarkdown = (source) => {
    const withoutFrontmatter = source.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, '');
    const lines = withoutFrontmatter.split(/\r?\n/);
    let html = '', paragraph = [], list = null, quote = [], code = null, tableRows = [], seen = {};
    const flushParagraph = () => { if (paragraph.length) { html += `<p>${inline(paragraph.join(' '))}</p>`; paragraph = []; } };
    const flushList = () => { if (list) { html += `<${list.kind}>${list.items.join('')}</${list.kind}>`; list = null; } };
    const flushQuote = () => { if (quote.length) { html += `<blockquote>${inline(quote.join(' '))}</blockquote>`; quote = []; } };
    const flushTable = () => { if (tableRows.length >= 2 && /^\s*\|?\s*:?-{3,}/.test(tableRows[1])) html += renderTable(tableRows); tableRows = []; };
    for (let i = 0; i < lines.length; i += 1) {
      const line = lines[i];
      const fence = line.match(/^\s*(```+|~~~+)(.*)$/);
      if (fence) { if (code) { html += `<pre><code class="language-${escapeHtml(code.lang)}">${escapeHtml(code.lines.join('\n'))}</code></pre>`; code = null; } else { flushParagraph(); flushList(); flushQuote(); flushTable(); code = { lang: fence[2].trim().split(/\s+/)[0] || 'text', lines: [] }; } continue; }
      if (code) { code.lines.push(line); continue; }
      if (/^\s*\|/.test(line) && i + 1 < lines.length && /^\s*\|/.test(lines[i + 1])) { flushParagraph(); flushList(); flushQuote(); tableRows.push(line); continue; }
      if (tableRows.length) flushTable();
      const heading = line.match(/^\s*(#{1,6})\s+(.+?)\s*#*\s*$/);
      if (heading) { flushParagraph(); flushList(); flushQuote(); const text = heading[2].trim(); let id = text.toLowerCase().replace(/[^a-z0-9 -]/g, '').trim().replace(/\s+/g, '-') || 'section'; const count = seen[id] || 0; seen[id] = count + 1; if (count) id += `-${count}`; html += `<h${heading[1].length} id="${id}">${inline(text)}</h${heading[1].length}>`; continue; }
      if (/^\s*([-*_])(?:\s*\1){2,}\s*$/.test(line)) { flushParagraph(); flushList(); flushQuote(); html += '<hr>'; continue; }
      const bullet = line.match(/^\s*[-*+]\s+(.+)$/); const ordered = line.match(/^\s*\d+[.)]\s+(.+)$/);
      if (bullet || ordered) { flushParagraph(); flushQuote(); const kind = ordered ? 'ol' : 'ul'; if (!list || list.kind !== kind) { flushList(); list = { kind, items: [] }; } list.items.push(`<li>${inline((bullet || ordered)[1])}</li>`); continue; }
      const quoteLine = line.match(/^\s*>\s?(.*)$/); if (quoteLine) { flushParagraph(); flushList(); quote.push(quoteLine[1]); continue; }
      if (!line.trim()) { flushParagraph(); flushList(); flushQuote(); continue; }
      paragraph.push(line.trim());
    }
    if (code) html += `<pre><code class="language-${escapeHtml(code.lang)}">${escapeHtml(code.lines.join('\n'))}</code></pre>`;
    flushParagraph(); flushList(); flushQuote(); flushTable(); return html;
  };

  const metadataHtml = (metadata) => Object.entries(metadata || {}).map(([key, value]) => `<dt>${escapeHtml(key)}</dt><dd>${escapeHtml(typeof value === 'string' ? value : JSON.stringify(value))}</dd>`).join('');
  const bindInternalLinks = () => document.querySelectorAll('#article a[href^="?"]').forEach((link) => link.addEventListener('click', (event) => { event.preventDefault(); const key = new URL(link.href).searchParams.get('key'); if (key) openDocument(key); }));

  const openDocument = async (key, push = true) => {
    const response = await fetch(`/api/document?key=${encodeURIComponent(key)}`); if (!response.ok) return;
    const doc = await response.json(); state.current = doc; if (push) history.pushState({}, '', `?key=${encodeURIComponent(key)}`); document.title = `${doc.title} · Knowledge preview`;
    $('welcome').classList.add('hidden'); $('article').classList.remove('hidden');
    const meta = doc.metadata || {}; const warning = meta.status === 'draft' || meta.governance_state === 'candidate' ? '<span class="badge warning">Draft / candidate</span>' : '';
    $('article').innerHTML = `<div class="crumb">${escapeHtml(doc.collection)} / ${escapeHtml(doc.path)}</div><div class="article-actions"><button id="raw-toggle">Raw source</button><button id="copy-link">Copy link</button></div><div class="meta-bar"><span class="badge">${escapeHtml(meta.type || doc.collection)}</span>${warning}<span class="badge">${escapeHtml(doc.sha256.slice(0, 12))}</span></div><h1>${escapeHtml(doc.title)}</h1><div id="article-body">${renderMarkdown(doc.content)}</div>`;
    $('article').querySelector('#raw-toggle').onclick = () => { state.raw = !state.raw; $('article-body').innerHTML = state.raw ? `<pre class="raw">${escapeHtml(doc.content)}</pre>` : renderMarkdown(doc.content); $('article').querySelector('#raw-toggle').textContent = state.raw ? 'Rendered view' : 'Raw source'; bindInternalLinks(); };
    $('article').querySelector('#copy-link').onclick = async () => { if (navigator.clipboard) await navigator.clipboard.writeText(location.href); };
    $('details').innerHTML = `<h3>Identity</h3><dl><dt>Collection</dt><dd>${escapeHtml(doc.collection)}</dd><dt>Path</dt><dd>${escapeHtml(doc.path)}</dd><dt>Bytes</dt><dd>${doc.bytes}</dd><dt>SHA-256</dt><dd>${escapeHtml(doc.sha256)}</dd></dl><h3>Metadata</h3><dl>${metadataHtml(meta)}</dl><h3>Contents</h3><nav class="toc">${(doc.headings || []).map((heading) => `<a class="level-${heading.level}" href="#${heading.slug}">${escapeHtml(heading.text)}</a>`).join('') || '<span class="muted">No headings</span>'}</nav>`;
    document.querySelectorAll('.doc-link').forEach((link) => link.classList.toggle('active', link.dataset.key === key)); bindInternalLinks();
  };

  const renderNavigation = () => {
    const collections = state.navigation.collections || []; $('count').textContent = `${state.navigation.health.documents} documents`;
    $('scope').innerHTML = '<option value="">All collections</option>' + collections.map((collection) => `<option value="${escapeHtml(collection.id)}">${escapeHtml(collection.label)}</option>`).join('');
    $('collections').innerHTML = collections.map((collection) => `<details class="collection" open><summary>${escapeHtml(collection.label)} <span class="collection-count">${collection.count}</span></summary><div class="doc-list">${collection.documents.map((doc) => `<button class="doc-link" data-key="${escapeHtml(doc.key)}" title="${escapeHtml(doc.path)}"><span>${escapeHtml(doc.title)}</span><small>${escapeHtml(doc.path)}</small></button>`).join('')}</div></details>`).join('');
    document.querySelectorAll('.doc-link').forEach((button) => { button.onclick = () => openDocument(button.dataset.key); });
  };

  const doSearch = async () => {
    const query = $('search').value.trim(); if (query.length < 2) { $('search-panel').classList.add('hidden'); return; }
    const response = await fetch(`/api/search?q=${encodeURIComponent(query)}&collection=${encodeURIComponent($('scope').value)}`); const payload = await response.json(); $('search-panel').classList.remove('hidden');
    $('results').innerHTML = payload.results.length ? payload.results.map((result) => `<button class="search-result" data-key="${escapeHtml(result.key)}"><strong>${escapeHtml(result.title)}</strong><small>${escapeHtml(result.collection)} / ${escapeHtml(result.path)}</small><span>${escapeHtml(result.snippet)}</span></button>`).join('') : '<p class="muted" style="padding:18px">No matches in the selected collections.</p>';
    document.querySelectorAll('.search-result').forEach((button) => { button.onclick = () => { $('search-panel').classList.add('hidden'); openDocument(button.dataset.key); }; });
  };

  const boot = async () => {
    state.navigation = await (await fetch('/api/navigation')).json(); state.navigation.collections.flatMap((collection) => collection.documents).forEach((doc) => state.docs.set(doc.key, doc)); renderNavigation();
    $('search').addEventListener('input', doSearch); $('scope').addEventListener('change', doSearch); $('close-search').onclick = () => $('search-panel').classList.add('hidden');
    $('refresh').onclick = async () => { await fetch('/api/refresh'); state.navigation = await (await fetch('/api/navigation')).json(); state.docs.clear(); state.navigation.collections.flatMap((collection) => collection.documents).forEach((doc) => state.docs.set(doc.key, doc)); renderNavigation(); };
    document.addEventListener('keydown', (event) => { if (event.key === '/' && document.activeElement !== $('search')) { event.preventDefault(); $('search').focus(); } });
    const key = new URLSearchParams(location.search).get('key'); const first = state.navigation.collections.find((collection) => collection.id === 'records')?.documents[0] || state.navigation.collections[0]?.documents[0];
    if (key) openDocument(key, false); else if (first) openDocument(first.key, false);
  };
  window.addEventListener('popstate', () => { const key = new URLSearchParams(location.search).get('key'); if (key) openDocument(key, false); }); boot();
})();
