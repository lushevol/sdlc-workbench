"""tda/collectors/release.py — Release WI and directly-linked WI data collection.

Collects: Release WI fields, Application WI approvals, Bug details, PT checks,
Testing types, SNOW, unit tests, Sonar, Genie, PIT — everything gathered in Step 3.

All results are returned (not appended to globals), so the caller (ResultStore)
owns the accumulation.
"""

from __future__ import annotations

import logging
import re

from bs4 import BeautifulSoup

from tda.config import Config
from tda.http_client import ADOClient, WIResponseAdapter
from tda.integrations import snow as snow_mod
from tda.integrations import sonar as sonar_mod
from tda.integrations import genie as genie_mod
from tda.integrations import genie_test_management as genie_test_mgmt_mod
from tda.integrations import doc_links


# ---------------------------------------------------------------------------
# Check 4: Architecture document type validation
# ---------------------------------------------------------------------------

# Keywords in a Confluence page title that indicate the wrong document type
# has been linked — e.g. a Solution Intent page instead of an Architecture doc.
_WRONG_ARCH_TITLE_KEYWORDS: tuple[str, ...] = (
    'solution intent',
    'conceptual design',
    'si conceptual',
    'si -',
    ' si:',
    '(si)',
    'logical design',
    'high level design',
    'hld',
)


def _check_arch_doc_title(page_title: str) -> str:
    """Return the disqualifying keyword found in the page title, or '' if OK."""
    title_lower = page_title.lower()
    for kw in _WRONG_ARCH_TITLE_KEYWORDS:
        if kw in title_lower:
            return kw.strip()
    return ''


def check_arch_doc_type(arch_urls: list[str],
                         cfg: Config,
                         client: ADOClient) -> list[dict]:
    """Fetch architecture document page titles and flag wrong types.

    Dispatches each URL to Confluence or SC Wiki via ``doc_links.validate_page()``
    based on its host, so this works unchanged regardless of which platform a
    given stream's Application WI links to.

    Returns a list of dicts (one per URL)::

        {
            'url':        str,
            'page_title': str,
            'status':     'OK' | 'WRONG_TYPE:<keyword>' | 'INACCESSIBLE'
        }
    """
    results: list[dict] = []
    for url in arch_urls:
        if not url:
            continue
        try:
            page_result = doc_links.validate_page(url, cfg, client)
            if page_result['Page Accessible'] != 'YES':
                results.append({'url': url, 'page_title': '', 'status': 'INACCESSIBLE'})
                continue
            title   = page_result.get('Page Title', '')
            bad_kw  = _check_arch_doc_title(title)
            status  = f'WRONG_TYPE:{bad_kw}' if bad_kw else 'OK'
            results.append({'url': url, 'page_title': title, 'status': status})
            if bad_kw:
                logging.warning(
                    "check_arch_doc_type: '%s' looks like a '%s' document, not Architecture",
                    title, bad_kw,
                )
        except Exception as exc:
            logging.warning("check_arch_doc_type: error for '%s' — %s", url, exc)
            results.append({'url': url, 'page_title': '', 'status': 'INACCESSIBLE'})
    return results


# ---------------------------------------------------------------------------
# HTML/text helpers
# ---------------------------------------------------------------------------

def html_to_text(html: str) -> str:
    return BeautifulSoup(html, 'html.parser').get_text()


def return_hyperlinks(html_content: str) -> list[str]:
    soup = BeautifulSoup(html_content, 'html.parser')
    return [link.get('href') for link in soup.find_all('a')]


_BARE_URL_RE = re.compile(r'https?://[^\s<>"\')\]]+', re.IGNORECASE)
_URL_TRAILING_PUNCT = '.,;:)]}>\'"'


def extract_urls_from_rich_text(html_content: str) -> list[str]:
    """Extract candidate URLs from a free-form rich-text ADO field that may mix
    narrative text with a document link (e.g. a "Review Comments"-style field
    where someone typed notes AND pasted a PIT page URL in the same box).

    Unlike ``return_hyperlinks()``, this does NOT assume every URL is wrapped
    in an ``<a href>`` anchor tag — ADO's rich-text editor only auto-converts
    a pasted URL into a real hyperlink some of the time (depends on how the
    text was entered/edited), so relying on anchor parsing alone would
    silently miss a URL that was typed or pasted as plain text alongside
    other comments.

    Returns anchor hrefs first (most reliable — explicit links), followed by
    any additional bare-text URLs found in the page's plain text that were
    not already captured as an anchor, in first-seen order, deduplicated.
    Trailing sentence punctuation (``.``, ``,``, ``)``, etc.) commonly left
    stuck to a bare URL by normal prose is stripped.
    """
    if not html_content:
        return []
    soup = BeautifulSoup(html_content, 'html.parser')
    anchor_urls = [href for a in soup.find_all('a') if (href := a.get('href'))]
    plain_text = soup.get_text(separator=' ')
    bare_urls = [
        m.group(0).rstrip(_URL_TRAILING_PUNCT)
        for m in _BARE_URL_RE.finditer(plain_text)
    ]
    seen = set(anchor_urls)
    merged = list(anchor_urls)
    for url in bare_urls:
        if url not in seen:
            seen.add(url)
            merged.append(url)
    return merged


_RAW_SONAR_BRANCH_HINTS = {
    'main',
}

def resolve_sonar_pipeline_branch(version_hint: str) -> str:
    """Turn a YAML Sonar version hint into the actual Sonar branch name.

    Numeric release annotations such as ``185.0.14`` map to
    ``release/185.0.14``. Explicit branch-like hints such as ``main`` or
    ``release/foo`` are already full branch identifiers and must be used as-is.
    """
    hint = str(version_hint).strip()
    if hint.startswith('refs/heads/'):
        hint = hint[len('refs/heads/'):]
    if hint in _RAW_SONAR_BRANCH_HINTS or '/' in hint:
        return hint
    return f'release/{hint}'


# ---------------------------------------------------------------------------
# Generic WI field extractor
# ---------------------------------------------------------------------------

def extract_fields(parsing_keys: list[str], response) -> dict:
    """Extract field values from an ADO work item response using dot-path keys.

    Keys with '-' are split: 'fields-Custom.Foo' → response.json()['fields']['Custom.Foo']
    Keys without '-' are top-level: 'id' → response.json()['id']
    """
    # Fields whose values are HTML containing <a href="..."> links — parsed into
    # a list of URL strings via return_hyperlinks(). These are always populated
    # via ADO's "insert hyperlink" action (dedicated document-link fields), so
    # a strict anchor-only parse is reliable here.
    _HYPERLINK_FIELDS = {
        'Custom.AIGandRollbackdocumentLink',
        'Custom.ApplicationArchitectureDocumentLink',
        'Custom.NFRDocumentLink',
        'Custom.TestStrategyDocumentLink',
        'Custom.ASRMDocumentLink',
        'Custom.TestEnvironmentDocumentLink',
    }
    # Free-form fields that may mix narrative text with a document link, where
    # the link is not guaranteed to be wrapped in an <a href> anchor (e.g. a
    # pasted-but-not-auto-linked URL) — parsed via extract_urls_from_rich_text()
    # instead, which also catches bare-text URLs.
    _MIXED_TEXT_LINK_FIELDS = {
        'Custom.ReviewComments',
    }
    result: dict = {}
    for key in parsing_keys:
        if '-' in key:
            parts = key.split('-', 1)
            try:
                value = response.json()[parts[0]][parts[1]]
                if parts[1] in _HYPERLINK_FIELDS:
                    value = return_hyperlinks(value)
                elif parts[1] in _MIXED_TEXT_LINK_FIELDS:
                    value = extract_urls_from_rich_text(value)
                result[parts[1]] = value
            except KeyError:
                result[parts[1]] = 'NOT FOUND'
        else:
            try:
                result[key] = response.json()[key]
            except KeyError:
                result[key] = 'NOT FOUND'
    return result


_ROLLBACK_SECTION_RE = re.compile(r'rollback', re.IGNORECASE)


def extract_aig_rollback_check(release_checks: dict, build_id: str,
                                client: ADOClient | None) -> dict:
    """Determine AIG/Rollback documentation coverage for this release.

    Two independent, mutually-exclusive sources are recognised (per the
    eSDLC "Pre-Deployment Verification" control's AIG+Rollback evidence):
      1. Release WI link (Custom.AIGandRollbackdocumentLink) — some teams
         (e.g. Apollo Rules-style applications) link the document directly.
      2. An 'AIG'-named build artifact on the MASTER release build — other
         teams (e.g. Blade-style applications) instead publish it as a build
         artifact, surfaced in ADO's UI under the build's "Extensions" tab
         but fetchable via the standard Build Artifacts API. The rollback
         steps are embedded within this same document.

    Only falls back to the build-artifact check when the RWI link is NOT
    populated, to skip an extra ADO call for releases where the RWI link
    already satisfies the control. Returns a single dict (caller wraps it
    in a list, matching the pit_result list-of-one-dict convention):

        {
            'Present':                bool,
            'Source':                 'rwi_link' | 'build_artifact' | 'not_found',
            'Document Link':          str | None,  # set when source is rwi_link
            'Build Id':               str | None,  # set when source is build_artifact
            'Artifact Name':          str | None,
            'Rollback Section Found': bool | None,  # None when source is rwi_link
                                                     # (content not fetched/verifiable)
            'Document Title':         str | None,   # best-effort <h1> text
            'Error':                  str | None,   # set only on an unexpected fetch failure
        }
    """
    rwi_link = release_checks.get('Custom.AIGandRollbackdocumentLink')
    rwi_urls = rwi_link if isinstance(rwi_link, list) else ([rwi_link] if rwi_link else [])
    rwi_urls = [u for u in rwi_urls if u and u != 'NOT FOUND']

    if rwi_urls:
        return {
            'Present': True,
            'Source': 'rwi_link',
            'Document Link': rwi_urls[0],
            'Build Id': None,
            'Artifact Name': None,
            'Rollback Section Found': None,
            'Document Title': None,
            'Error': None,
        }

    if client is None or not build_id:
        return {
            'Present': False, 'Source': 'not_found', 'Document Link': None,
            'Build Id': build_id or None, 'Artifact Name': None,
            'Rollback Section Found': None, 'Document Title': None, 'Error': None,
        }

    result = client.get_aig_rollback_document(build_id)
    if not result.get('found'):
        return {
            'Present': False, 'Source': 'not_found', 'Document Link': None,
            'Build Id': build_id, 'Artifact Name': None,
            'Rollback Section Found': None, 'Document Title': None,
            'Error': result.get('error'),
        }

    content = result.get('content') or ''
    rollback_found = bool(_ROLLBACK_SECTION_RE.search(content)) if content else None
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    title = html_to_text(title_match.group(1)).strip() if title_match else None

    return {
        'Present': True,
        'Source': 'build_artifact',
        'Document Link': None,
        'Build Id': build_id,
        'Artifact Name': result.get('artifact_name'),
        'Rollback Section Found': rollback_found,
        'Document Title': title,
        'Error': result.get('error'),
    }


# ---------------------------------------------------------------------------
# Application WI
# ---------------------------------------------------------------------------

def extract_application_checks(response, cfg: Config,
                                client: ADOClient | None = None,
                                post_approval_check: bool = False) -> dict:
    """Extract approval-expiry fields from an Application WI.

    When ``post_approval_check`` is True AND ``client`` is supplied, also
    fetches every documentation hyperlink on the WI (Confluence OR SC Wiki —
    see ``tda.integrations.doc_links``), retrieves each page's last-modified
    timestamp, and compares it against the most recent approver comment
    timestamp to detect pages edited after their ADO approval was recorded.
    Results are stored under the key ``'confluence_post_approval_checks'`` as
    a list of dicts:

        {
          'url':           str,   # the hyperlink URL
          'label':         str,   # ADO relation comment/label (document name)
          'page_title':    str,   # actual page title (Confluence or SC Wiki)
          'last_modified': str,   # ISO-8601 timestamp of latest page edit
          'last_approval': str,   # ISO-8601 timestamp of latest approver comment, or ''
          'status':        str,   # 'OK' | 'EDITED_AFTER_APPROVAL' |
                                  # 'NO_APPROVAL_RECORDED' | 'PAGE_INACCESSIBLE'
        }

    Always runs Check 4 (architecture document title type check) when a
    ``client`` is supplied, regardless of ``post_approval_check``.
    """
    checks = extract_fields(cfg.application_wi_keys, response)

    if not (post_approval_check and client is not None):
        # Check 4: still run arch doc title check even without post_approval_check
        checks['confluence_post_approval_checks'] = []
        if client is not None:
            arch_val = checks.get('Custom.ApplicationArchitectureDocumentLink')
            arch_urls: list[str] = []
            if isinstance(arch_val, list):
                arch_urls = [u for u in arch_val if u]
            elif arch_val and arch_val != 'NOT FOUND':
                arch_urls = [arch_val]
            checks['arch_doc_type_check'] = (
                check_arch_doc_type(arch_urls, cfg, client) if arch_urls else []
            )
        else:
            checks['arch_doc_type_check'] = []
        return checks

    # --- Collect documentation links (Confluence OR SC Wiki) from the dedicated ADO fields ---
    # Each field may return a list of URLs (parsed from HTML by extract_fields),
    # 'NOT FOUND' (field absent on this WI type), or an empty list.
    _DOC_LINK_FIELDS = {
        'Custom.ApplicationArchitectureDocumentLink': 'Application Architecture',
        'Custom.ASRMDocumentLink':                    'ASRM',
        'Custom.NFRDocumentLink':                     'NFR',
        'Custom.TestStrategyDocumentLink':            'Test Strategy',
        'Custom.TestEnvironmentDocumentLink':         'Test Environment',
    }
    doc_links_found: list[dict] = []
    for field, label in _DOC_LINK_FIELDS.items():
        val = checks.get(field)
        if not val or val == 'NOT FOUND':
            continue
        urls = val if isinstance(val, list) else [val]
        for url in urls:
            if not url:
                continue
            # Only follow links that point at a known documentation host
            # (Confluence or SC Wiki — skip ADO / other hosts).
            if not doc_links.is_known_doc_host(url, cfg):
                continue
            doc_links_found.append({'url': url, 'label': label})

    if not doc_links_found:
        checks['confluence_post_approval_checks'] = []
        return checks

    print(
        f"        [AppConfluenceCheck] Found {len(doc_links_found)} documentation link(s) "
        "on Application WI — checking for post-approval edits...",
        flush=True,
    )

    results: list[dict] = []
    for link in doc_links_found:
        url   = link['url']
        label = link['label']
        page_result = doc_links.validate_page(url, cfg, client)

        if page_result['Page Accessible'] != 'YES':
            results.append({
                'url': url, 'label': label,
                'page_title': '', 'last_modified': '',
                'last_approval': '', 'status': 'PAGE_INACCESSIBLE',
            })
            continue

        last_modified = page_result.get('Page Last Modified', '')
        timestamps    = page_result.get('Approved Timestamp', [])
        last_approval = max(timestamps) if timestamps else ''

        if not last_approval:
            status = 'NO_APPROVAL_RECORDED'
        elif last_modified and last_modified > last_approval:
            status = 'EDITED_AFTER_APPROVAL'
        else:
            status = 'OK'

        results.append({
            'url': url,
            'label': label,
            'page_title': page_result.get('Page Title', ''),
            'last_modified': last_modified,
            'last_approval': last_approval,
            'status': status,
        })
        logging.info(
            "AppConfluenceCheck: '%s' last_modified=%s last_approval=%s -> %s",
            page_result.get('Page Title', url), last_modified, last_approval, status,
        )

    edited = [r for r in results if r['status'] == 'EDITED_AFTER_APPROVAL']
    no_approval = [r for r in results if r['status'] == 'NO_APPROVAL_RECORDED']
    print(
        f"        [AppConfluenceCheck] {len(results)} page(s) checked — "
        f"{len(edited)} edited after approval, {len(no_approval)} with no approval recorded.",
        flush=True,
    )
    checks['confluence_post_approval_checks'] = results

    # Check 4: architecture document title type — reuse page_title already fetched
    # above when post_approval_check is True (avoids a second Confluence call).
    arch_findings_from_post_check = [
        r for r in results if r.get('label') == 'Application Architecture'
    ]
    if arch_findings_from_post_check:
        checks['arch_doc_type_check'] = [
            {
                'url':        r['url'],
                'page_title': r['page_title'],
                'status':     (
                    'INACCESSIBLE' if r['status'] == 'PAGE_INACCESSIBLE'
                    else (
                        f"WRONG_TYPE:{_check_arch_doc_title(r['page_title'])}"
                        if _check_arch_doc_title(r['page_title'])
                        else 'OK'
                    )
                ),
            }
            for r in arch_findings_from_post_check
        ]
    return checks


# ---------------------------------------------------------------------------
# Bug WI
# ---------------------------------------------------------------------------

def extract_bug_checks(response, cfg: Config) -> dict:
    checks = extract_fields(cfg.bug_wi_keys, response)
    checks['Tested By'] = []
    for rel in response.json().get('relations', []):
        if rel['rel'] == 'Microsoft.VSTS.Common.TestedBy-Forward':
            checks['Tested By'].append(rel['url'].split('workItems/')[1])

    # Clean rich-text fields (Description / Acceptance Criteria) for the
    # informational Desc/AC quality review — strip HTML and truncate so the
    # JSON output stays readable. Bugs frequently have no Acceptance Criteria
    # field at all; extract_fields() already returns 'NOT FOUND' gracefully
    # in that case, so this is a no-op when the field is absent.
    for html_key in ('System.Description', 'Microsoft.VSTS.Common.AcceptanceCriteria'):
        raw = checks.get(html_key)
        if raw and raw != 'NOT FOUND':
            checks[html_key] = html_to_text(raw).strip()[:2000]
    return checks


# ---------------------------------------------------------------------------
# Release WI
# ---------------------------------------------------------------------------

def extract_release_checks(response, cfg: Config,
                            supplied_build_id: str,
                            client: ADOClient,
                            rwi_only: bool = False) -> dict:
    checks = extract_fields(cfg.release_wi_keys, response)

    # Prefer the primary CHG ID field, but fall back to the alternate ADO field
    # when some streams populate the change request there instead.
    chg_id = checks.get('Custom.CHGID', 'NOT FOUND')
    if chg_id in ('', 'NOT FOUND', None):
        fallback_chg_id = checks.get('Custom.ADOCHGID', 'NOT FOUND')
        if fallback_chg_id not in ('', 'NOT FOUND', None):
            checks['Custom.CHGID'] = fallback_chg_id
            chg_id = fallback_chg_id
            logging.info(
                "extract_release_checks: using Custom.ADOCHGID as fallback CHG ID (%s)",
                fallback_chg_id,
            )

    # Parent Application WI (ADO hierarchy-parent relation)
    parent_app_wi = 'NOT FOUND'
    try:
        for rel in response.json().get('relations', []):
            if rel.get('rel') == 'System.LinkTypes.Hierarchy-Reverse':
                parent_app_wi = rel['url'].split('workItems/')[-1]
                break
    except Exception as e:
        logging.warning("extract_release_checks: could not extract parent WI — %s", e)
    checks['Parent Application WI'] = parent_app_wi

    # Resolve build ID
    if supplied_build_id:
        checks['Build Id'] = supplied_build_id
    elif rwi_only:
        # No build_id in rwi-only mode — set sentinel values and skip ADO build calls.
        checks['Build Id'] = 'N/A (rwi-only)'
        checks['Branch Id'] = 'N/A (rwi-only)'
        checks['Project']   = 'N/A (rwi-only)'
        return checks
    else:
        latest_pipeline = checks.get('Custom.LatestPipelineRuns', '')
        m = re.search(r'buildId=(\d+)', latest_pipeline or '')
        if m:
            checks['Build Id'] = m.group(1)
        else:
            raise ValueError(
                "Could not extract Build ID from Custom.LatestPipelineRuns. "
                f"Raw value: {latest_pipeline!r}. "
                "Supply the build ID explicitly as the second CLI argument."
            )

    checks['Branch Id'] = client.get_branch_from_build(checks['Build Id'])
    checks['Project']   = client.get_project_from_build(checks['Build Id'])
    return checks


def extract_release_pt_checks(release_checks: dict,
                               cfg: Config, client: ADOClient) -> dict:
    pt = {
        'ReleasePTPlanExists': [], 'ReleasePTReportExists': [],
        'ReleasePTPlanLink': [], 'ReleasePTReportLink': [],
        'ReleasePTPlanApproval': [], 'ReleasePTReportApproval': [],
        'ReleasePTIAExists': '', 'ReleasePTIAApproval': '', 'ReleasePTIAPageTitle': '',
    }
    try:
        for link in return_hyperlinks(release_checks['Custom.ReleasePTPlanDocumentLink']):
            pt['ReleasePTPlanExists'].append('YES')
            pt['ReleasePTPlanLink'].append(link)
            pt['ReleasePTPlanApproval'].append(
                doc_links.validate_page(link, cfg, client)
            )
    except KeyError:
        pt['ReleasePTPlanExists'] = 'NO'

    try:
        for link in return_hyperlinks(release_checks['Custom.ReleasePTReportDocumentLink']):
            pt['ReleasePTReportExists'].append('YES')
            pt['ReleasePTReportLink'].append(link)
            pt['ReleasePTReportApproval'].append(
                doc_links.validate_page(link, cfg, client)
            )
    except KeyError:
        pt['ReleasePTReportExists'] = 'NO'

    try:
        ptia = release_checks['Custom.RationaleforNotdoingPerformanceTesting']
        if 'href' in ptia and 'https' in ptia:
            pt['ReleasePTIAExists'] = 'YES'
            ptia_approval = doc_links.validate_page(
                ptia.split('href="')[1].split('"')[0], cfg, client
            )
            pt['ReleasePTIAApproval'] = ptia_approval
            pt['ReleasePTIAPageTitle'] = ptia_approval.get('Page Title', '')
            pt['ReleasePTIAJustification'] = ''
        else:
            # Field present but no hyperlink — may be plain-text or HTML justification.
            # Strip HTML tags to get the readable text and store it for SKILL evaluation.
            from bs4 import BeautifulSoup
            plain = BeautifulSoup(ptia, 'html.parser').get_text(separator=' ').strip() if ptia else ''
            if plain and plain.upper() not in ('NOT FOUND', 'N/A', 'NA', 'NONE', ''):
                pt['ReleasePTIAExists'] = 'TEXT'       # link-less justification present
                pt['ReleasePTIAApproval'] = 'N/A'      # no Confluence page to approve
                pt['ReleasePTIAJustification'] = plain[:500]  # cap at 500 chars for JSON
            else:
                pt['ReleasePTIAExists'] = 'NO'
                pt['ReleasePTIAApproval'] = 'NO'
                pt['ReleasePTIAJustification'] = ''
    except KeyError:
        pt['ReleasePTIAExists'] = 'NO'
        pt['ReleasePTIAApproval'] = 'NO'
        pt['ReleasePTIAJustification'] = ''
    return pt


# ---------------------------------------------------------------------------
# Check 5: Regression justification boilerplate detection
# ---------------------------------------------------------------------------

# Phrases that indicate a generic / reused regression justification.
# Compared case-insensitively against the stripped plain-text value.
_BOILERPLATE_REGRESSION_PHRASES: tuple[str, ...] = (
    'not applicable',
    'not required',
    'n/a',
    'na',
    'no regression',
    'regression not required',
    'same as previous',
    'same as last release',
    'same as before',
    'reused from previous',
    'carried over',
    'as per previous release',
    'refer previous',
    'see previous release',
    'no changes to regression',
    'no impact',
    'no functional change',
)


def extract_regression_justification(release_checks: dict) -> dict:
    """Classify the regression justification field from the Release WI.

    Returns::

        {
            'RegressionJustificationExists':   str,   # 'YES' | 'TEXT' | 'NO'
            'RegressionJustificationText':     str,   # plain text, up to 500 chars
            'RegressionJustificationCheck':    str,   # 'OK' | 'BOILERPLATE' | 'NO_JUSTIFICATION'
        }
    """
    raw = release_checks.get('Custom.RationaleforNotdoingRegression', '')
    result = {
        'RegressionJustificationExists': 'NO',
        'RegressionJustificationText':   '',
        'RegressionJustificationCheck':  'NO_JUSTIFICATION',
    }
    if not raw or raw == 'NOT FOUND':
        return result

    from bs4 import BeautifulSoup
    plain = BeautifulSoup(raw, 'html.parser').get_text(separator=' ').strip() if raw else ''
    if not plain or plain.upper() in ('NOT FOUND', 'N/A', 'NA', 'NONE', ''):
        return result

    result['RegressionJustificationExists'] = 'TEXT'
    result['RegressionJustificationText']   = plain[:500]

    # Boilerplate check: look for generic phrases in the normalised text
    normalised = plain.lower()
    is_boilerplate = any(phrase in normalised for phrase in _BOILERPLATE_REGRESSION_PHRASES)
    # Also flag very short text as likely boilerplate (under 30 chars of real content)
    if is_boilerplate or len(plain) < 30:
        result['RegressionJustificationCheck'] = 'BOILERPLATE'
    else:
        result['RegressionJustificationCheck'] = 'OK'

    return result


def extract_testing_types(release_checks: dict) -> dict:
    types = {
        'System Testing': 'N', 'Integration Testing': 'N',
        'Acceptance Testing': 'N', 'Regression Testing': 'N', 'Performance Testing': 'N',
    }
    raw = release_checks.get('Custom.Testingtypeinscope')
    if not raw or raw == 'NOT FOUND':
        logging.warning(
            "extract_testing_types: 'Custom.Testingtypeinscope' missing — "
            "all testing types default to N."
        )
        return types
    for tt in raw.split(';'):
        tt = tt.strip()
        if tt in types:
            types[tt] = 'Y'
        elif tt:
            logging.warning("extract_testing_types: unrecognised type '%s' — skipping.", tt)
    return types


# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------

def get_unit_test_coverage(pipeline_name: str, build_id: str,
                            client: ADOClient) -> dict:
    """Fetch unit test summary for one pipeline build.

    Returns a coverage dict.  The caller appends it to the result store.
    """
    coverage = {
        'Pipeline Name': pipeline_name, 'Total Tests': 0,
        'Passed': 0, 'Failed': 0, 'Not Executed': 0,
        'increaseInTotalTests': 0, 'increaseInFailures': 0,
        'increaseInPassedTests': 0, 'increaseInNonImpactedTests': 0,
        'increaseInOtherTests': 0,
    }
    r = client.get('UnitTestByBuild', build_id)
    analysis = r.json()['aggregatedResultsAnalysis']
    coverage['Total Tests'] = analysis['totalTests']
    outcomes = analysis.get('resultsByOutcome', {})
    coverage['Passed'] = outcomes.get('Passed', {}).get('count', 0)
    coverage['Failed'] = outcomes.get('Failed', {}).get('count', 0)
    coverage['Not Executed'] = outcomes.get('NotExecuted', {}).get('count', 0)
    try:
        diff = analysis['resultsDifference']
        for k in ('increaseInTotalTests', 'increaseInFailures', 'increaseInPassedTests',
                  'increaseInNonImpactedTests', 'increaseInOtherTests'):
            coverage[k] = diff[k]
    except KeyError:
        pass
    return coverage


# ---------------------------------------------------------------------------
# Step 3 orchestrator — collect all release-level data
# ---------------------------------------------------------------------------

def collect_release_data(release_id: str,
                          supplied_build_id: str,
                          release_stream: str,
                          blade_release_builds: dict,
                          sonar_stream_config: dict,
                          sonar_key_overrides: dict,
                          pit_links: dict,
                          supplied_release_version: str,
                          cfg: Config,
                          client: ADOClient,
                          rwi_only: bool = False,
                          genie_enabled: bool = True,
                          regression_run_filter: str = "",
                          ado_regression_skip: bool = False,
                          genie_test_management_app_id: str = "") -> dict:
    """Fetch and return all Step-3 data as a plain dict.

    Returns keys: release, release_pt, testing_types, snow, unit_tests,
                  sonar, genie_count, genie_failures, genie_tags, genie_story_tags,
                  genie_story_type_breakdown, pit_content, aig_rollback_check,
                  work_item_relations
    """
    response = client.get('WorkItemsForRelease', release_id)
    release_checks = extract_release_checks(response, cfg, supplied_build_id, client,
                                            rwi_only=rwi_only)

    # Release WI comments (clone detection)
    release_checks['Comments'] = []
    release_checks['RWI Cloned Flag'] = 'False'
    comments_resp = client.get('CommentsForRelease', release_id)
    for comment in comments_resp.json()['comments']:
        text = comment['text']
        if 'Copied from' in text or 'Copied with' in text:
            release_checks['RWI Cloned Flag'] = 'True'
        release_checks['Comments'].append(html_to_text(text)[:100])

    # AIG + Rollback document (dual-source: RWI link, else build artifact)
    aig_rollback_result = extract_aig_rollback_check(release_checks, supplied_build_id, client)

    # SNOW
    if cfg.snow_enabled:
        chg_id = release_checks['Custom.CHGID']
        print(f"        [SNOW] Fetching change record details for {chg_id}...", flush=True)
        snow_data = snow_mod.get_snow_details(chg_id, cfg)
        if any(snow_data.get(field) for field in cfg.snow_fields):
            print(
                f"        [SNOW] Done. state={snow_data.get('state')} "
                f"type={snow_data.get('type')}",
                flush=True,
            )
        else:
            print(
                f"        [SNOW] ⚠️  No change record data returned for {chg_id} "
                "(all fields empty — check CHG number, SNOW credentials, or "
                "instance connectivity).",
                flush=True,
            )
    else:
        print("        [SNOW] Skipped — SNOW_ENABLED=false", flush=True)
        snow_data = {}

    # PT checks
    release_pt = extract_release_pt_checks(release_checks, cfg, client)

    # Check 5: regression justification boilerplate
    regression_justification = extract_regression_justification(release_checks)

    # Testing types
    testing_types = extract_testing_types(release_checks)

    # Unit tests
    unit_tests = []
    if rwi_only:
        print("        [Unit Tests] Skipped — rwi-only mode", flush=True)
    else:
        for p_name, b_id in blade_release_builds.items():
            unit_tests.append(get_unit_test_coverage(p_name, b_id, client))

    # Genie
    genie_count    = {'passed': 0, 'failed': 0}
    genie_failures: list = []
    genie_tags:     list = []
    genie_story_tags: list = []
    genie_story_type_breakdown: list = []
    if rwi_only:
        print("        [Genie] Skipped — rwi-only mode", flush=True)
    elif not genie_enabled and genie_test_management_app_id:
        # Opt-in alternative regression source (see tda/integrations/
        # genie_test_management.py) — a stream can set genie_enabled: false
        # (skipping the scenario-traceability Genie API) AND supply a
        # genie_test_management_app_id in stream_config.yaml to instead pull
        # automated regression results from Genie's separate test-management
        # API. NOTE: this fetches only the FIRST PAGE of results — pagination
        # for this API is not yet confirmed (see module docstring); watch for
        # genie_count['pagination_incomplete'] in the output.
        print(
            f"        [Genie Test-Management] genie_enabled=false but "
            f"genie_test_management_app_id='{genie_test_management_app_id}' is set "
            "— fetching regression results from the Genie test-management API...",
            flush=True,
        )
        genie_count, genie_failures, genie_tags, genie_story_tags, genie_story_type_breakdown = (
            genie_test_mgmt_mod.get_test_management_regression_results(
                release_id, genie_test_management_app_id, cfg, client
            )
        )
        _pg_warn = " ⚠️  pagination_incomplete=true (more results may exist)" if genie_count.get('pagination_incomplete') else ""
        print(
            f"        [Genie Test-Management] done. Passed={genie_count['passed']} "
            f"Failed={genie_count['failed']} Total={genie_count['total']}{_pg_warn}",
            flush=True,
        )
    elif not genie_enabled:
        # ADO-native regression fetch is GLOBALLY DISABLED for now (2026-07-30),
        # regardless of the stream's regression_config.skip setting in
        # stream_config.yaml. It was found to issue a very large number of ADO
        # API calls (test/runs polling across every associated build, with no
        # run-name filter applied by default) while there is still no agreed
        # approach for reliably extracting non-Genie regression results — the
        # aggregated totals were misleading (e.g. NotApplicable/Incomplete
        # outcomes folded into 'total' alongside passed/failed) and unsafe to
        # run at volume. Until that is resolved, streams with genie_enabled:
        # false simply report "no regression data collected" instead of
        # falling back to the ADO fetch. ado_regression_skip / regression_run_filter
        # are still loaded from stream_config.yaml but are intentionally unused here.
        print(
            "        [ADO Regression] Skipped — ADO-native regression fetch is "
            "globally disabled for now (unclear/unsafe extraction approach). "
            "No regression data collected.",
            flush=True,
        )
        genie_count = {
            'passed': 0, 'failed': 0, 'total': 0,
            'genie_source': 'skipped',
            'skip_reason': 'ADO-native regression fetch globally disabled pending a '
                           'clearer, safer extraction approach (see release.py collect_release_data)',
        }
    else:
        print("        Fetching Genie regression results...", flush=True)
        genie_count, genie_failures, genie_tags, genie_story_tags, genie_story_type_breakdown = genie_mod.get_genie_regression_failures(
            release_id, cfg, client
        )
        print(
            f"        Genie done. Passed={genie_count['passed']} Failed={genie_count['failed']}",
            flush=True,
        )

    # Branch / Sonar branch resolution
    branch_id = release_checks['Branch Id']
    sonar_branch_id = branch_id
    if supplied_release_version:
        branch_id = supplied_release_version
        sonar_branch_id = f'release/{supplied_release_version}'
    else:
        fmt = sonar_stream_config.get('branch_version_format', 'standard')
        if fmt == 'bcf':
            parts = branch_id.split('/')
            branch_id = ' '.join(parts[1:4]) if len(parts) >= 4 else branch_id
            sonar_branch_id = branch_id
        elif fmt != 'raw' and '/' in branch_id:
            last = branch_id.split('/')[-1]
            branch_id = last.split('-', 1)[1] if '-' in last else last
            sonar_branch_id = 'release/' + branch_id

    # PIT (Confluence or SC Wiki — see tda.integrations.doc_links)
    pit_result = doc_links.get_and_validate_pit_link(
        release_stream, branch_id, pit_links, cfg, client
    )
    pit_result['PIT Source'] = 'stream_config_pit_url'
    if pit_result.get('Page Accessible') != 'YES':
        # Fallback: some teams embed the PIT Confluence/SC Wiki page link
        # directly in the Release WI's "Review Comments" field
        # (Custom.ReviewComments, rich-text HTML) instead of relying on the
        # version-templated pit_url in stream_config.yaml. extract_fields()
        # already parsed this field into a list of URLs (see _HYPERLINK_FIELDS
        # in extract_fields() above). Try each known-host URL found there
        # before falling back further to the plain-text Custom.PITPlan field
        # (handled entirely in SKILL.md/gen_tda_report.py, not here).
        review_comment_urls = release_checks.get('Custom.ReviewComments', [])
        if isinstance(review_comment_urls, list):
            for url in review_comment_urls:
                if not url or not doc_links.is_known_doc_host(url, cfg):
                    continue
                candidate = doc_links.validate_page(url, cfg, client)
                if candidate.get('Page Accessible') == 'YES':
                    candidate['PIT Source'] = 'rwi_review_comments'
                    pit_result = candidate
                    # Keep the content-parsing step below in sync with the
                    # URL that actually resolved, not the (inaccessible)
                    # stream_config.yaml template.
                    pit_links[release_stream.upper()] = url
                    print(
                        "        [PIT] Resolved via RWI 'Review Comments' field "
                        f"fallback: {url}",
                        flush=True,
                    )
                    break
    pit_content = {}
    if pit_result.get('Page Accessible') == 'YES':
        pit_content = doc_links.get_and_validate_pit_content_if_supported(
            release_stream, pit_links, cfg, client
        )

    # Sonar
    sonar_coverage = []
    sonar_quality_gates = []
    sonar_quality_gate_statuses = []
    sonar_exclusions = []
    sonar_new_code_periods = []
    sonar_skipped = False
    sonar_skip_reason = ''
    if rwi_only:
        sonar_skipped = True
        sonar_skip_reason = 'rwi-only mode — build-dependent checks are not run'
        print(f"        [Sonar] Skipped — rwi-only mode", flush=True)
    elif sonar_stream_config.get('skip', False):
        sonar_skipped = True
        sonar_skip_reason = (
            f"skip: true in sonar_config for stream '{release_stream}' "
            "(stream_config.yaml) — no Sonar project configured for this stream"
        )
        print(f"        [Sonar] Skipped for stream '{release_stream}'", flush=True)
    else:
        _branch_strategy   = sonar_stream_config.get('branch_strategy', 'build_branch')
        _shared_prefix     = sonar_stream_config.get('shared_repo_prefix', '')
        _pipeline_versions = sonar_stream_config.get('_pipeline_versions', {})
        for key_pipeline, value_pipeline in blade_release_builds.items():
            ado_proj = client.get_project_from_build(value_pipeline)
            sonar_proj = sonar_key_overrides.get(key_pipeline, ado_proj)
            # Version annotation in YAML takes priority — avoids an ADO API call
            # and guarantees the exact branch used for that component's Sonar scan.
            if key_pipeline in _pipeline_versions:
                pipeline_branch = resolve_sonar_pipeline_branch(
                    _pipeline_versions[key_pipeline]
                )
            elif _shared_prefix and ado_proj.startswith(_shared_prefix):
                pipeline_branch = client.get_branch_from_build(value_pipeline)
            elif _branch_strategy == 'release_branch':
                pipeline_branch = sonar_branch_id
            else:
                pipeline_branch = client.get_branch_from_build(value_pipeline)
            metrics = sonar_mod.get_coverage_metrics(
                key_pipeline, sonar_proj, pipeline_branch, cfg, client
            )
            if metrics is not None:
                sonar_coverage.append(metrics)
            quality_gate = sonar_mod.get_quality_gate_name(
                key_pipeline, sonar_proj, cfg, client
            )
            if quality_gate is not None:
                sonar_quality_gates.append(quality_gate)
            gate_status = sonar_mod.get_quality_gate_status(
                key_pipeline, sonar_proj, pipeline_branch, cfg, client
            )
            if gate_status is not None:
                sonar_quality_gate_statuses.append(gate_status)
            exclusions = sonar_mod.get_project_exclusions(
                key_pipeline, sonar_proj, cfg, client
            )
            if exclusions is not None:
                sonar_exclusions.append(exclusions)
            new_code_period = sonar_mod.get_new_code_period(
                key_pipeline, sonar_proj, pipeline_branch, cfg, client
            )
            if new_code_period is not None:
                sonar_new_code_periods.append(new_code_period)

    # Strip internal-only keys before returning
    for key in cfg.remove_release_level_keys:
        release_checks.pop(key, None)

    # Work item relations for Step 4
    relations = response.json().get('relations', [])
    work_items = [
        wi for wi in relations
        if wi['rel'] in (
            'System.LinkTypes.Related',
            'Microsoft.VSTS.Common.TestedBy-Forward',
            'Microsoft.VSTS.Common.TestedBy-Reverse',
            'System.LinkTypes.Hierarchy-Reverse',
        )
    ]

    return {
        'release':           [release_checks],
        'release_pt':        [release_pt],
        'regression_justification': [regression_justification],
        'testing_types':     [testing_types],
        'snow':              [snow_data] if snow_data else [],
        'snow_enabled':      cfg.snow_enabled,
        'pit_result':        [pit_result],
        'pit_content':       [pit_content] if pit_content else [],
        'aig_rollback_check': [aig_rollback_result],
        'unit_tests':        unit_tests,
        'sonar':             sonar_coverage,
        'sonar_quality_gates': sonar_quality_gates,
        'sonar_quality_gate_statuses': sonar_quality_gate_statuses,
        'sonar_exclusions':  sonar_exclusions,
        'sonar_new_code_periods': sonar_new_code_periods,
        'sonar_skipped':     sonar_skipped,
        'sonar_skip_reason': sonar_skip_reason,
        'genie_count':       [genie_count],
        'genie_failures':    genie_failures,
        'genie_tags':        genie_tags,
        'genie_story_tags':  genie_story_tags,
        'genie_story_type_breakdown': genie_story_type_breakdown,
        'work_item_relations': work_items,
    }
