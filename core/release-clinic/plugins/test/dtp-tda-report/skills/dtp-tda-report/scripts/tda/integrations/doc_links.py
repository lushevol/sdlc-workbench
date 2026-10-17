"""tda/integrations/doc_links.py — provider-agnostic documentation-link dispatcher.

SC Wiki is expected to (eventually, not immediately) replace Confluence as the
org's documentation platform — see tda/integrations/confluence.py and
tda/integrations/scwiki.py. Rather than have every collector call site decide
"is this a Confluence or SC Wiki URL?" itself, this module centralises that
decision:

    from tda.integrations import doc_links

    result = doc_links.validate_page(url, cfg, client)   # works for either host

``validate_page()`` inspects the URL's host against ``cfg.confluence_url`` /
``cfg.scwiki_url`` and dispatches to ``confluence.validate_confluence_page()``
or ``scwiki.validate_scwiki_page()`` accordingly — both already return the
same dict shape (``Approved By`` / ``Approved Timestamp`` / ``Page
Accessible`` / ``Page Title`` / ``Page Last Modified``), so callers do not
need to change based on which provider actually served the page.

As individual streams migrate their documentation from Confluence to SC Wiki,
no collector code needs to change — only the URL stored on the ADO work item
(or in stream_config.yaml's ``pit_url`` template) changes, and this module
routes to the correct backend automatically.

Known limitation: ``validate_pit_content()`` (parsing a PIT page's HTML
tables for release-metadata cross-checks) remains Confluence-only for now —
SC Wiki's REST API returns page content in wiki syntax, not rendered HTML, so
the existing BeautifulSoup table-parsing approach does not apply as-is. See
``get_and_validate_pit_content_if_supported()`` below.
"""

from __future__ import annotations

import logging
from urllib.parse import urlparse

from tda.config import Config
from tda.http_client import ADOClient
from tda.integrations import confluence as confluence_mod
from tda.integrations import scwiki as scwiki_mod

_INACCESSIBLE_RESULT = {
    'Approved By': [], 'Approved Timestamp': [], 'Page Accessible': 'NO',
    'Page Title': '', 'Page Last Modified': '',
}


def _host_of(url: str) -> str:
    return urlparse(url).netloc.lower() if url else ''


def detect_provider(url: str, cfg: Config) -> str:
    """Return 'confluence', 'scwiki', or 'unknown' based on the URL's host.

    Compares against ``cfg.confluence_url`` / ``cfg.scwiki_url`` (either may
    be unset/empty, in which case that provider can never match). Comparison
    is host-only (not full-URL-prefix) so it is robust to trailing slashes,
    http vs https, and query-string variations.
    """
    if not url:
        return 'unknown'
    host = _host_of(url)
    if not host:
        return 'unknown'
    confluence_host = _host_of(cfg.confluence_url)
    scwiki_host = _host_of(cfg.scwiki_url)
    if confluence_host and host == confluence_host:
        return 'confluence'
    if scwiki_host and host == scwiki_host:
        return 'scwiki'
    return 'unknown'


def is_known_doc_host(url: str, cfg: Config) -> bool:
    """True if ``url`` points at either the configured Confluence or SC Wiki host."""
    return detect_provider(url, cfg) != 'unknown'


def validate_page(url: str, cfg: Config, client: ADOClient) -> dict:
    """Validate a documentation page link, dispatching by host.

    Returns the same dict shape for either provider (see module docstring).
    Unrecognized hosts return an inaccessible-result stub with a warning
    logged, rather than raising — callers already handle 'Page Accessible':
    'NO' as a normal outcome (missing/broken link), so this keeps behaviour
    consistent instead of introducing a new failure mode.
    """
    provider = detect_provider(url, cfg)
    if provider == 'confluence':
        return confluence_mod.validate_confluence_page(url, cfg, client)
    if provider == 'scwiki':
        return scwiki_mod.validate_scwiki_page(url, cfg, client)
    logging.warning(
        "doc_links.validate_page: '%s' does not match the configured Confluence "
        "(%s) or SC Wiki (%s) host — treating as inaccessible.",
        url, cfg.confluence_url, cfg.scwiki_url,
    )
    return dict(_INACCESSIBLE_RESULT)


def get_and_validate_pit_link(stream: str, release_version: str,
                               pit_links: dict, cfg: Config,
                               client: ADOClient) -> dict:
    """Resolve and validate the PIT document link for this stream/release.

    Provider-agnostic equivalent of confluence.get_and_validate_pit_link():
    same version-fallback probing (tries the exact version, then falls back
    to stripping a trailing '.0'), but dispatches each probe through
    ``validate_page()`` so a stream's ``pit_url`` template in
    stream_config.yaml may point at either a Confluence or an SC Wiki page.
    The resolved URL is written back into ``pit_links`` exactly as before.
    """
    url_template = pit_links.get(stream.upper())
    if not url_template:
        logging.warning(
            "get_and_validate_pit_link: no PIT URL template for stream '%s' — skipping",
            stream,
        )
        return dict(_INACCESSIBLE_RESULT)

    def _build_url(v: str) -> str:
        return url_template.replace('{{version}}', v)

    def _probe(version: str, suppress_errors: bool = False) -> tuple[str, dict]:
        """Try one URL, optionally silencing noisy provider-SDK 'not found' logging."""
        url = _build_url(version)
        if suppress_errors:
            # The atlassian library logs ERROR when a Confluence page is not found.
            # Harmless no-op for SC Wiki URLs (this logger is never touched by
            # tda.integrations.scwiki), so it's safe to always apply this guard
            # regardless of which provider the template resolves to.
            ado_logger = logging.getLogger('atlassian.confluence')
            old_level = ado_logger.level
            ado_logger.setLevel(logging.CRITICAL)
            try:
                res = validate_page(url, cfg, client)
            finally:
                ado_logger.setLevel(old_level)
        else:
            res = validate_page(url, cfg, client)
        return url, res

    # Primary attempt — suppress SDK noise because a fallback may exist
    pit_url, result = _probe(release_version, suppress_errors=True)

    if result['Page Accessible'] == 'NO' and release_version.endswith('.0'):
        # Fallback 1: strip trailing '.0'  (e.g. '74.0' → '74')
        stripped = release_version[:-2]
        logging.info(
            "get_and_validate_pit_link: '%s' not found, retrying with version '%s'",
            release_version, stripped,
        )
        pit_url, result = _probe(stripped, suppress_errors=False)

    # Write resolved URL back so a subsequent content-parsing step can use it
    pit_links[stream.upper()] = pit_url
    return result


def get_and_validate_pit_content_if_supported(stream: str, pit_links: dict,
                                               cfg: Config, client: ADOClient) -> dict:
    """Parse the resolved PIT page's table contents, ONLY when Confluence-hosted.

    Provider-agnostic wrapper around confluence.validate_pit_content(). SC
    Wiki's REST API returns page content in wiki syntax (not rendered HTML),
    so the existing BeautifulSoup table-parsing approach does not apply as-is
    — a stream whose resolved PIT URL is SC Wiki-hosted gets an empty dict
    here (logged, not a hard failure) until a wiki-syntax-aware equivalent is
    built. Confluence-hosted PIT pages behave exactly as before.
    """
    url = pit_links.get(stream.upper(), pit_links.get(stream))
    provider = detect_provider(url, cfg) if url else 'unknown'
    if provider == 'scwiki':
        logging.info(
            "get_and_validate_pit_content_if_supported: PIT page for stream '%s' is "
            "SC Wiki-hosted — table-content parsing not yet supported for SC Wiki, "
            "skipping (page accessibility/approval checks are unaffected).",
            stream,
        )
        return {}
    return confluence_mod.validate_pit_content(stream, pit_links, cfg, client)
