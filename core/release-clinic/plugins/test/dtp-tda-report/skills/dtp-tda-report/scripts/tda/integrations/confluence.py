"""tda/integrations/confluence.py — Confluence page validation and PIT content extraction."""

from __future__ import annotations

import logging
import os
from urllib.parse import parse_qs, unquote_plus, urlparse

from atlassian import Confluence
from bs4 import BeautifulSoup

from tda.config import Config
from tda.http_client import ADOClient
from tda.call_tracker import tracker as call_tracker


def _make_client(cfg: Config, *, direct_only: bool = True) -> Confluence:
    # Default to direct access for internal Confluence hosts, but allow a
    # proxy-enabled fallback for environments where direct routing is blocked.
    if not cfg.confluence_user:
        logging.warning("Confluence USER_EMAIL is empty — authentication may fail even with a token.")
    if not cfg.confluence_token:
        logging.warning("Confluence token is empty — Confluence page access will fail.")
    client = Confluence(
        url=cfg.confluence_url,
        username=cfg.confluence_user,
        token=cfg.confluence_token,
        verify_ssl=False,
    )
    # atlassian-python-api stores the session as _session
    if direct_only:
        # trust_env=False stops requests from reading HTTPS_PROXY / Windows registry.
        # proxies.clear() removes any proxy that may have been set at construction time.
        client._session.trust_env = False
        client._session.proxies.clear()
    return client


def _normalize_confluence_url(url: str, cfg: Config, *, direct_only: bool = True) -> str:
    """Normalize Confluence URLs prior to page-id extraction.

    Expands short-link URLs (/x/<token>) by following redirects so downstream
    logic can parse canonical /display/... or pageId forms.
    """
    if not url:
        return url
    parsed = urlparse(url)
    path_parts = [p for p in parsed.path.split('/') if p]
    if len(path_parts) >= 2 and path_parts[0].lower() == 'x':
        try:
            c = _make_client(cfg, direct_only=direct_only)
            call_tracker.record('Confluence')
            resp = c._session.get(url, allow_redirects=True, verify=False, timeout=20)
            if resp is not None and getattr(resp, 'url', None):
                return resp.url
        except Exception as exc:
            logging.info("_normalize_confluence_url: failed to expand short URL '%s': %s", url, exc)
    return url


def get_page_id(url: str, cfg: Config, *, direct_only: bool = True, log_warnings: bool = True) -> str | None:
    """Resolve a Confluence page URL to its numeric page ID.

    Handles three URL formats:
    - Numeric ID:  .../pages/viewpage.action?pageId=12345[&...]
    - Query-param: .../pages/viewpage.action?spaceKey=SPACE&title=Page+Title
                   Works for ANY space, not just the configured default.
    - Path-based:  .../display/SPACE/Page+Title  (standard modern format)
    """
    client = _make_client(cfg, direct_only=direct_only)
    url = _normalize_confluence_url(url, cfg, direct_only=direct_only)
    for old, new in [('%28', '('), ('%29', ')'), ('?src=contextnavpagetreemode', '')]:
        url = url.replace(old, new)
    page_id = None
    if not url:
        return page_id
    try:
        if 'pageId=' in url:
            # Extract numeric page ID; strip any trailing query params (e.g. &src=...)
            page_id = url.split('pageId=')[1].split('&')[0]
        elif 'spaceKey=' in url and 'title=' in url:
            # Legacy query-parameter format — parse_qs handles URL-decoding and
            # '+'-as-space, and works for any space (not just the configured default).
            parsed = urlparse(url)
            qs = parse_qs(parsed.query)
            space = (qs.get('spaceKey') or [None])[0]
            title = (qs.get('title') or [None])[0]
            if space and title:
                call_tracker.record('Confluence')
                page_id = client.get_page_id(space, title)
        else:
            # Standard /display/SPACE/Page+Title path format, robust to
            # trailing slashes and query/hash suffixes.
            parsed = urlparse(url)
            path_parts = [p for p in parsed.path.split('/') if p]
            if len(path_parts) >= 3 and path_parts[0].lower() == 'display':
                space = path_parts[1]
                title = path_parts[2]
            else:
                space, title = url.split('/')[-2:]
            title_decoded = unquote_plus(title)
            call_tracker.record('Confluence')
            page_id = client.get_page_id(space, title_decoded)
    except Exception as e:
        if log_warnings:
            logging.warning("get_page_id: failed to resolve '%s': %s", url, e)
        else:
            logging.info("get_page_id: failed to resolve '%s': %s", url, e)
    return page_id


def validate_confluence_page(url: str, cfg: Config,
                              client: ADOClient) -> dict:
    """Check whether a Confluence page is accessible and collect approver comments.

    Returns {
        'Approved By': [...],
        'Approved Timestamp': [...],
        'Page Accessible': 'YES'|'NO',
        'Page Title': str,            # actual Confluence page title, or '' if inaccessible
        'Page Last Modified': str,    # ISO-8601 timestamp of the latest page edit,
                                      # or '' if inaccessible. Populated from
                                      # page['version']['when'] (already fetched via
                                      # expand='version' — no extra API call).
    }.
    """
    result = {'Approved By': [], 'Approved Timestamp': [], 'Page Accessible': 'YES',
              'Page Title': '', 'Page Last Modified': ''}
    client.unset_proxy()
    try:
        # Try direct path first, then retry once with proxy-enabled session.
        for direct_only in (True, False):
            page_id = get_page_id(
                url,
                cfg,
                direct_only=direct_only,
                log_warnings=(not direct_only),
            )
            if page_id is None:
                if direct_only:
                    continue
                result['Page Accessible'] = 'NO'
                return result

            confluence = _make_client(cfg, direct_only=direct_only)
            try:
                # Fetch title and comments in one call by expanding both.
                call_tracker.record('Confluence')
                page = confluence.get_page_by_id(page_id, expand='version')
                result['Page Title'] = page.get('title', '')
                result['Page Last Modified'] = (page.get('version') or {}).get('when', '')
                call_tracker.record('Confluence')
                comments = confluence.get_page_comments(
                    page_id, expand='body.storage,history.createdBy'
                )
                for comment in comments['results']:
                    result['Approved By'].append(
                        comment['history']['createdBy']['displayName']
                    )
                    result['Approved Timestamp'].append(comment['history']['createdDate'])
                return result
            except Exception:
                if direct_only:
                    logging.info(
                        "validate_confluence_page: direct access failed for '%s' — retrying with proxy", url
                    )
                    continue
                logging.info("validate_confluence_page: error accessing '%s'", url)
                result['Page Accessible'] = 'NO'
                result['Page Title'] = ''
                result['Page Last Modified'] = ''
                return result
    finally:
        # Always restore the proxy — even on early return or exception.
        client.set_proxy()
    return result


def get_and_validate_pit_link(stream: str, release_version: str,
                               pit_links: dict, cfg: Config,
                               client: ADOClient) -> dict:
    """Resolve and validate the PIT Confluence page for this stream/release.

    ``pit_links`` is the dict populated from stream_config.yaml (`pit_url` per
    stream), keyed by uppercase stream name.  The resolved URL is written back
    into pit_links so that validate_pit_content() can find it.
    """
    url_template = pit_links.get(stream.upper())
    if not url_template:
        logging.warning(
            "get_and_validate_pit_link: no PIT URL template for stream '%s' — skipping",
            stream,
        )
        return {'Approved By': [], 'Approved Timestamp': [], 'Page Accessible': 'NO'}

    def _build_url(v: str) -> str:
        return url_template.replace('{{version}}', v)

    def _probe(version: str, suppress_errors: bool = False) -> tuple[str, dict]:
        """Try one URL, optionally silencing the atlassian logger."""
        url = _build_url(version)
        if suppress_errors:
            # The atlassian library logs ERROR when a page is not found.
            # Silence it during probe attempts so the user only sees a warning
            # if *all* fallbacks are exhausted.
            ado_logger = logging.getLogger('atlassian.confluence')
            old_level = ado_logger.level
            ado_logger.setLevel(logging.CRITICAL)
            try:
                res = validate_confluence_page(url, cfg, client)
            finally:
                ado_logger.setLevel(old_level)
        else:
            res = validate_confluence_page(url, cfg, client)
        return url, res

    # Primary attempt — suppress atlassian noise because a fallback may exist
    pit_url, result = _probe(release_version, suppress_errors=True)

    if result['Page Accessible'] == 'NO' and release_version.endswith('.0'):
        # Fallback 1: strip trailing '.0'  (e.g. '74.0' → '74')
        stripped = release_version[:-2]
        logging.info(
            "get_and_validate_pit_link: '%s' not found, retrying with version '%s'",
            release_version, stripped,
        )
        pit_url, result = _probe(stripped, suppress_errors=False)

    # Write resolved URL back so validate_pit_content can use it
    pit_links[stream.upper()] = pit_url
    return result


def validate_pit_content(stream: str, pit_links: dict,
                          cfg: Config, client: ADOClient) -> dict:
    """Parse the PIT Confluence page and return a flat dict of its table contents."""
    url = pit_links.get(stream.upper(), pit_links.get(stream))
    if not url:
        return {}
    page_id = get_page_id(url, cfg)
    if page_id is None:
        return {}
    confluence = _make_client(cfg)
    try:
        call_tracker.record('Confluence')
        page = confluence.get_page_by_id(page_id=page_id, expand='body.storage')
    except Exception as e:
        logging.warning("validate_pit_content: failed to fetch page_id '%s': %s", page_id, e)
        return {}

    html_cont = page['body']['storage']['value']
    try:
        soup = BeautifulSoup(html_cont, features='lxml')
    except Exception:
        # lxml is an optional dependency (bs4.FeatureNotFound if not installed) —
        # fall back to the built-in parser rather than crashing the whole job.
        # lxml is still preferred (faster, more lenient with malformed HTML) — see
        # requirements.txt; this is a safety net, not a substitute for installing it.
        logging.warning("validate_pit_content: lxml parser unavailable, falling back to html.parser")
        soup = BeautifulSoup(html_cont, features='html.parser')
    tables_raw = []
    for table in soup.find_all('table'):
        table_data = [
            [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
            for row in table.find_all('tr')
        ]
        tables_raw.append(table_data)

    pit_content: dict = {}
    for items in tables_raw:
        if not items:
            continue
        if items[0][0] in ('Release', 'Change Ticket # :'):
            for item in items:
                if len(item) >= 2:
                    pit_content[item[0]] = item[1]
        else:
            transposed = list(map(list, zip(*items)))
            for col in transposed:
                rec = 1
                for cell in col[1:]:
                    if cell:
                        pit_content[f"{col[0]}-{rec}"] = cell
                        rec += 1
    return pit_content
