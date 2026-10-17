"""tda/integrations/scwiki.py — SC Wiki (XWiki-based) REST API integration.

SC Wiki is the organisation's new internal documentation platform and is
expected to eventually replace Confluence for stream documentation (PIT
plans, Application Architecture docs, ASRM, NFR, Test Strategy, etc.) — see
tda/integrations/confluence.py for the integration this is modelled on and
is intended to (eventually, not immediately) sit alongside / replace.

This module is a STANDALONE integration point: nothing in the collector
pipeline (tda/collectors/*, AutoTDAScript.py) calls into it yet. It exists so
that:
  1. The REST plumbing (auth, retries, URL parsing, error handling) is ready
     and independently testable before any stream depends on it.
  2. Function signatures deliberately mirror confluence.py's shape
     (``validate_scwiki_page(url, cfg, client)`` returns the same dict shape
     as ``validate_confluence_page``) so a future per-stream "doc provider"
     switch (e.g. a ``doc_provider: confluence|scwiki`` key in
     stream_config.yaml) can dispatch to either module with minimal call-site
     changes.

Known parity gap vs. Confluence: comments ARE now supported (see
``get_page_comments()``), confirmed live against a Sandbox page at
``GET /wikis/{wiki}/spaces/.../pages/{page}/comments`` — this endpoint is not
documented in the integration write-up supplied for this module but was
discovered via the page resource's own HATEOAS ``links`` array (a
``http://www.xwiki.org/rel/comments`` relation) and confirmed working with a
real 200 response containing actual comment text. One difference from
Confluence: comment authors are returned as XWiki login IDs (e.g.
``XWiki.1615184zone1scbnet``) rather than resolved display names —
``authorName`` was ``null`` in the confirmed test response, so
``_display_name_from_author()`` falls back to a best-effort cleanup of the
login ID when no display name is present.

Authentication: Bearer API key (personal access token), created manually by
each user from their SC Wiki profile's Application tab. Read from the
SCWIKI_API_KEY environment variable — see tda/config.py's Config.scwiki_*
fields and .env.example. There is no username/basic-auth mode (unlike
Confluence's token+email pair) — SC Wiki only supports the bearer-token
method per the integration documentation this module was built from.

Nested pages (confirmed via live testing against a Sandbox page): this SC
Wiki instance has XWiki's "nested pages" feature enabled, so a human-facing
URL such as ``/bin/view/Sandbox/50665 QA/PT-188-REPORT/`` does NOT map to
page ``PT-188-REPORT`` under space ``Sandbox.50665 QA`` (confirmed 404) — it
maps to page ``WebHome`` under space ``Sandbox.50665 QA.PT-188-REPORT``
(confirmed 200). ``_resolve_page()`` tries the nested-page interpretation
first and falls back to the classic terminal-page interpretation, so callers
don't need to special-case this.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from urllib.parse import unquote, urlparse

import requests

from tda.config import Config
from tda.http_client import ADOClient, call_with_retries
from tda.call_tracker import tracker as call_tracker

DEFAULT_WIKI_NAME = 'xwiki'

# HTTP statuses documented as expected/successful by the SC Wiki API docs.
_OK_STATUSES = {200, 201, 204}


def _epoch_ms_to_iso(value) -> str:
    """Convert an XWiki epoch-millisecond timestamp (int) to an ISO-8601 UTC string.

    XWiki's REST API returns 'created'/'modified' as epoch-millisecond
    integers (confirmed via live testing), unlike Confluence's ISO-8601
    string ('version.when'). Normalizing here keeps validate_scwiki_page()'s
    'Page Last Modified' field the same shape/format as
    validate_confluence_page()'s. Returns '' for None/unparseable input.
    """
    if value is None:
        return ''
    try:
        return datetime.fromtimestamp(int(value) / 1000, tz=timezone.utc).isoformat()
    except (TypeError, ValueError, OSError):
        return str(value)


def _display_name_from_author(author: str | None, author_name: str | None) -> str:
    """Best-effort human-readable name for a comment author.

    Prefers ``authorName`` (a resolved display name) when present. XWiki's
    comments endpoint returned ``authorName: null`` in live testing, so this
    falls back to cleaning up the ``author`` login id (e.g.
    ``'XWiki.1615184zone1scbnet'`` -> ``'1615184zone1scbnet'``), which is
    still more useful than an empty string but is NOT a guaranteed display
    name — treat it as a best-effort identifier, not equivalent to
    Confluence's ``history.createdBy.displayName``.
    """
    if author_name:
        return author_name
    if not author:
        return ''
    return author.split('.', 1)[1] if '.' in author else author


# ---------------------------------------------------------------------------
# Session / low-level request helpers
# ---------------------------------------------------------------------------

def _rest_base_url(cfg: Config) -> str:
    """Return the '<scwiki_url>/rest' base, tolerant of a trailing slash on scwiki_url."""
    return cfg.scwiki_url.rstrip('/') + '/rest'


def _make_session(cfg: Config, *, direct_only: bool = True) -> requests.Session:
    """Build a requests.Session authenticated with the SCWIKI_API_KEY bearer token.

    Mirrors confluence._make_client()'s direct-vs-proxy handling: SC Wiki is an
    internal host, so ``direct_only=True`` strips any proxy the process
    environment might otherwise inject (trust_env=False + cleared proxies).
    Callers needing the proxy-enabled fallback pass ``direct_only=False``.
    """
    if not cfg.scwiki_api_key:
        logging.warning("SC Wiki API key (SCWIKI_API_KEY) is empty — SC Wiki requests will fail with 401.")
    session = requests.Session()
    session.headers.update({
        'Authorization': f'Bearer {cfg.scwiki_api_key}',
        'Accept': 'application/json',
    })
    # Internal certificate — same rationale as confluence.py's verify_ssl=False.
    session.verify = False
    if direct_only:
        session.trust_env = False
        session.proxies.clear()
    return session


def _check_response(resp: requests.Response, what: str) -> None:
    """Log a status-code-specific hint per the SC Wiki API docs' status table.

    Does not raise — callers decide whether a non-2xx response is fatal for
    their use case (e.g. 404 on a page-existence probe is often expected).
    """
    if resp.status_code in _OK_STATUSES:
        return
    hints = {
        400: "Bad Request — check the URL and query parameters.",
        401: "Unauthorized — check SCWIKI_API_KEY is set and not expired.",
        403: "Forbidden — authenticated but insufficient rights; ask an admin for access.",
        404: "Not Found — space/page/object does not exist at this path.",
        500: "Server Error — check SC Wiki server logs.",
    }
    hint = hints.get(resp.status_code, f"Unexpected status {resp.status_code}.")
    level = logging.INFO if resp.status_code == 404 else logging.WARNING
    logging.log(level, "%s: %s (%s)", what, hint, resp.request.url if resp.request else '')


# ---------------------------------------------------------------------------
# URL / path helpers
# ---------------------------------------------------------------------------

def _space_segments(space: str | list[str]) -> list[str]:
    """Normalize a space identifier into an ordered list of nested-space segments.

    Accepts either an explicit list (already-split segments) or a single
    string. For a string, splits on '.' to support the dotted nested-space id
    convention shown in the integration docs' sample code (e.g.
    "Global Spaces.ChildSpaceName" -> ["Global Spaces", "ChildSpaceName"]).
    NOTE: this dotted-id convention is inferred from the docs' Python example
    (`sp_id`, an XWiki *space reference*) rather than an explicitly documented
    REST *path* rule — verify against a real nested space if the resulting
    path 404s unexpectedly.
    """
    if isinstance(space, (list, tuple)):
        return [s for s in space if s]
    return [s for s in space.split('.') if s]


def _page_path(space: str | list[str], page: str, wiki_name: str = DEFAULT_WIKI_NAME) -> str:
    """Build the '/wikis/{wiki}/spaces/{s1}/spaces/{s2}/.../pages/{page}' resource path."""
    segments = _space_segments(space)
    path = f"/wikis/{wiki_name}"
    for seg in segments:
        path += f"/spaces/{seg}"
    return f"{path}/pages/{page}"


def _spaces_path(space: str | list[str] | None, wiki_name: str = DEFAULT_WIKI_NAME) -> str:
    """Build the '/wikis/{wiki}/spaces[/{s1}/spaces/{s2}/...]' resource path (no page)."""
    path = f"/wikis/{wiki_name}"
    if space:
        for seg in _space_segments(space):
            path += f"/spaces/{seg}"
    return f"{path}/spaces"


def parse_scwiki_url(url: str) -> tuple[str, list[str], str] | None:
    """Resolve an SC Wiki URL into (wiki_name, space_segments, page_name).

    Handles two URL shapes:
      - REST resource URLs:  .../rest/wikis/{wiki}/spaces/{s1}/spaces/{s2}/pages/{page}
      - Human 'view' URLs:   .../bin/view/{Space1}/{Space2}/{Page}
                              (as shown for profile links in the integration docs)

    Returns None if the URL doesn't match either recognized shape.
    """
    if not url:
        return None
    parsed = urlparse(url)
    parts = [unquote(p) for p in parsed.path.split('/') if p]

    if 'rest' in parts and 'wikis' in parts:
        try:
            wiki_idx = parts.index('wikis')
            wiki_name = parts[wiki_idx + 1]
            rest = parts[wiki_idx + 2:]
            segments: list[str] = []
            i = 0
            page_name = ''
            while i < len(rest):
                if rest[i] == 'spaces' and i + 1 < len(rest):
                    segments.append(rest[i + 1])
                    i += 2
                elif rest[i] == 'pages' and i + 1 < len(rest):
                    page_name = rest[i + 1]
                    i += 2
                else:
                    i += 1
            if page_name:
                return wiki_name, segments, page_name
        except (ValueError, IndexError):
            pass
        return None

    if 'bin' in parts and 'view' in parts:
        view_idx = parts.index('view')
        remainder = parts[view_idx + 1:]
        # Strip any trailing query-string artifacts that leaked into the path list.
        remainder = [r for r in remainder if '?' not in r]
        if len(remainder) >= 2:
            return DEFAULT_WIKI_NAME, remainder[:-1], remainder[-1]
        if len(remainder) == 1:
            return DEFAULT_WIKI_NAME, [], remainder[0]

    return None


# ---------------------------------------------------------------------------
# Spaces endpoints
# ---------------------------------------------------------------------------

def list_spaces(cfg: Config, *, wiki_name: str = DEFAULT_WIKI_NAME,
                 number: int = 500, start: int = 0) -> list[dict]:
    """GET /wikis/{wiki}/spaces — list top-level spaces (paginated)."""
    session = _make_session(cfg)
    url = f"{_rest_base_url(cfg)}/wikis/{wiki_name}/spaces"
    call_tracker.record('SCWiki')
    resp = call_with_retries(
        lambda: session.get(url, params={'number': number, 'start': start}, timeout=30),
        what='SCWiki list_spaces',
    )
    _check_response(resp, 'list_spaces')
    if resp.status_code not in _OK_STATUSES:
        return []
    return resp.json().get('spaces', [])


def list_child_spaces(space: str | list[str], cfg: Config,
                       *, wiki_name: str = DEFAULT_WIKI_NAME) -> list[dict]:
    """GET /wikis/{wiki}/spaces/{spaceName}/spaces — list child spaces of a parent."""
    session = _make_session(cfg)
    url = f"{_rest_base_url(cfg)}{_spaces_path(space, wiki_name)}"
    call_tracker.record('SCWiki')
    resp = call_with_retries(lambda: session.get(url, timeout=30), what='SCWiki list_child_spaces')
    _check_response(resp, 'list_child_spaces')
    if resp.status_code not in _OK_STATUSES:
        return []
    return resp.json().get('spaces', [])


# ---------------------------------------------------------------------------
# Pages endpoints
# ---------------------------------------------------------------------------

def list_pages(space: str | list[str], cfg: Config,
                *, wiki_name: str = DEFAULT_WIKI_NAME) -> list[dict]:
    """GET /wikis/{wiki}/spaces/{spaceName}/pages — list all pages in a space."""
    session = _make_session(cfg)
    segments = _space_segments(space)
    path = f"/wikis/{wiki_name}"
    for seg in segments:
        path += f"/spaces/{seg}"
    url = f"{_rest_base_url(cfg)}{path}/pages"
    call_tracker.record('SCWiki')
    resp = call_with_retries(lambda: session.get(url, timeout=30), what='SCWiki list_pages')
    _check_response(resp, 'list_pages')
    if resp.status_code not in _OK_STATUSES:
        return []
    return resp.json().get('pageSummaries', resp.json().get('pages', []))


def get_page(space: str | list[str], page: str, cfg: Config,
             *, wiki_name: str = DEFAULT_WIKI_NAME) -> dict | None:
    """GET /wikis/{wiki}/spaces/{spaceName}/pages/{pageName} — page metadata + content.

    Returns the parsed JSON body, or None if the page is inaccessible/missing.
    """
    session = _make_session(cfg)
    url = f"{_rest_base_url(cfg)}{_page_path(space, page, wiki_name)}"
    call_tracker.record('SCWiki')
    try:
        resp = call_with_retries(lambda: session.get(url, timeout=30), what='SCWiki get_page')
    except Exception as exc:
        logging.warning("get_page: request failed for space=%s page=%s: %s", space, page, exc)
        return None
    _check_response(resp, f'get_page({space}/{page})')
    if resp.status_code not in _OK_STATUSES:
        return None
    return resp.json()


def get_page_comments(space: str | list[str], page: str, cfg: Config,
                       *, wiki_name: str = DEFAULT_WIKI_NAME) -> list[dict]:
    """GET /wikis/{wiki}/spaces/{spaceName}/pages/{pageName}/comments — page comments.

    Confirmed live against a real Sandbox page (not in the originally supplied
    API docs — discovered via the page resource's own HATEOAS 'comments'
    link). Returns the raw list of comment dicts (each with at least
    ``author``, ``authorName``, ``date`` (epoch-ms), ``text``), or ``[]`` on
    any error/empty response.
    """
    session = _make_session(cfg)
    url = f"{_rest_base_url(cfg)}{_page_path(space, page, wiki_name)}/comments"
    call_tracker.record('SCWiki')
    try:
        resp = call_with_retries(lambda: session.get(url, timeout=30), what='SCWiki get_page_comments')
    except Exception as exc:
        logging.warning("get_page_comments: request failed for space=%s page=%s: %s", space, page, exc)
        return []
    _check_response(resp, f'get_page_comments({space}/{page})')
    if resp.status_code not in _OK_STATUSES:
        return []
    return resp.json().get('comments', [])


def _resolve_page(segments: list[str], page_name: str, cfg: Config,
                   *, wiki_name: str = DEFAULT_WIKI_NAME) -> tuple[dict, list[str], str] | None:
    """Resolve a page, tolerant of XWiki's 'nested pages' convention.

    Modern XWiki instances (nested-pages feature, enabled by default since
    XWiki 7.x) represent every 'page' as its own nested SPACE containing a
    terminal document named ``WebHome``. A URL like
    ``/bin/view/Sandbox/50665 QA/PT-188-REPORT/`` therefore does NOT resolve
    via ``pages/PT-188-REPORT`` under space ``Sandbox.50665 QA`` (confirmed
    404 in testing) — it resolves via ``pages/WebHome`` under space
    ``Sandbox.50665 QA.PT-188-REPORT`` (confirmed 200).

    Tries, in order:
      1. Nested-page form:  segments + [page_name] as the space path, 'WebHome' as the page.
      2. Classic form:      segments as the space path, page_name as the page (only tried
                             when it differs from attempt 1, e.g. explicit REST URLs that
                             already pass a non-WebHome terminal page).

    Returns (page_json, resolved_segments, resolved_page_name) for whichever
    attempt succeeds first, or None if both fail.
    """
    attempts: list[tuple[list[str], str]] = [(segments + [page_name], 'WebHome')]
    if page_name != 'WebHome':
        attempts.append((segments, page_name))
    for cand_segments, cand_page in attempts:
        page = get_page(cand_segments, cand_page, cfg, wiki_name=wiki_name)
        if page is not None:
            return page, cand_segments, cand_page
    return None


def create_or_update_page(space: str | list[str], page: str, title: str, content: str,
                           cfg: Config, *, wiki_name: str = DEFAULT_WIKI_NAME,
                           syntax: str = 'xwiki/2.1') -> dict:
    """PUT /wikis/{wiki}/spaces/{spaceName}/pages/{pageName} — create or update a page.

    Returns {'status_code': int, 'created': bool} — 201 means newly created,
    200 means an existing page was updated (per the docs' status-code table).
    """
    session = _make_session(cfg)
    url = f"{_rest_base_url(cfg)}{_page_path(space, page, wiki_name)}"
    payload = {'title': title, 'content': content, 'syntax': syntax}
    call_tracker.record('SCWiki')
    resp = call_with_retries(lambda: session.put(url, json=payload, timeout=30),
                              what='SCWiki create_or_update_page')
    _check_response(resp, f'create_or_update_page({space}/{page})')
    resp.raise_for_status()
    return {'status_code': resp.status_code, 'created': resp.status_code == 201}


def delete_page(space: str | list[str], page: str, cfg: Config,
                 *, wiki_name: str = DEFAULT_WIKI_NAME) -> bool:
    """DELETE /wikis/{wiki}/spaces/{spaceName}/pages/{pageName}. Requires admin/owner rights.

    Returns True on 204 No Content (success), False otherwise.
    """
    session = _make_session(cfg)
    url = f"{_rest_base_url(cfg)}{_page_path(space, page, wiki_name)}"
    call_tracker.record('SCWiki')
    resp = call_with_retries(lambda: session.delete(url, timeout=30), what='SCWiki delete_page')
    _check_response(resp, f'delete_page({space}/{page})')
    return resp.status_code == 204


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

def search(query: str, cfg: Config, *, wiki_name: str = DEFAULT_WIKI_NAME,
           number: int = 10, start: int = 0, scope: str | None = None) -> list[dict]:
    """GET /wikis/{wiki}/search — full-text search across all pages.

    ``scope`` (optional) is one of: name, content, title, spaces.
    """
    session = _make_session(cfg)
    url = f"{_rest_base_url(cfg)}/wikis/{wiki_name}/search"
    params: dict = {'q': query, 'number': number, 'start': start}
    if scope:
        params['scope'] = scope
    call_tracker.record('SCWiki')
    resp = call_with_retries(lambda: session.get(url, params=params, timeout=30), what='SCWiki search')
    _check_response(resp, 'search')
    if resp.status_code not in _OK_STATUSES:
        return []
    body = resp.json()
    return body.get('searchResults', body if isinstance(body, list) else [])


# ---------------------------------------------------------------------------
# Confluence-parity validation function
# ---------------------------------------------------------------------------

def validate_scwiki_page(url: str, cfg: Config, client: ADOClient | None = None) -> dict:
    """Check whether an SC Wiki page is accessible; parity shape with validate_confluence_page.

    Returns {
        'Approved By': list[str],     # comment author display names (best-effort — see
                                      # _display_name_from_author()), one per comment.
        'Approved Timestamp': list[str],  # ISO-8601 UTC comment dates, same order as 'Approved By'.
        'Page Accessible': 'YES'|'NO',
        'Page Title': str,            # '' if inaccessible
        'Page Last Modified': str,    # ISO-8601 UTC, converted from XWiki's epoch-ms
                                      # 'modified' (falls back to 'created'); '' if inaccessible.
    }
    """
    result = {'Approved By': [], 'Approved Timestamp': [], 'Page Accessible': 'YES',
              'Page Title': '', 'Page Last Modified': ''}

    parsed = parse_scwiki_url(url)
    if parsed is None:
        logging.warning("validate_scwiki_page: could not parse SC Wiki URL '%s'", url)
        result['Page Accessible'] = 'NO'
        return result
    wiki_name, segments, page_name = parsed

    if client is not None:
        client.unset_proxy()
    try:
        resolved = _resolve_page(segments, page_name, cfg, wiki_name=wiki_name)
        if resolved is None:
            result['Page Accessible'] = 'NO'
            return result
        page, resolved_segments, resolved_page = resolved
        result['Page Title'] = page.get('title', '')
        result['Page Last Modified'] = _epoch_ms_to_iso(page.get('modified') or page.get('created'))
        for comment in get_page_comments(resolved_segments, resolved_page, cfg, wiki_name=wiki_name):
            result['Approved By'].append(
                _display_name_from_author(comment.get('author'), comment.get('authorName'))
            )
            result['Approved Timestamp'].append(_epoch_ms_to_iso(comment.get('date')))
        return result
    finally:
        if client is not None:
            client.set_proxy()
