"""tda/collectors/po_approval.py — Acceptance Testing PO-approval email evidence.

For test cases classified as Acceptance Testing (``Custom.TestType``), this
module looks at the attachments on the test case's latest test result and,
for any attachment that is shaped like an email (.eml / .msg), downloads and
parses it to surface the sender, subject, body snippet, any Confluence links
in the body, and any approval-style keywords found.

IMPORTANT — this is a best-effort HEURISTIC only. It can never definitively
prove the sender is the Product Owner (email headers are trivially spoofable,
and there is no reliable ADO field identifying who the PO is for a given
release/application). Callers (the dtp-tda-report SKILL) must treat findings
here as informational/MODERATE evidence for release-manager review, never as
a CRITICAL gate — the existing generic evidence-presence check (Section 6 —
Manual Test Execution) already covers the CRITICAL "is there any evidence at
all" gate regardless of what this module finds.

.eml attachments are parsed with the standard library ``email`` module.
.msg attachments (Outlook binary format) require the optional ``extract-msg``
package — if it is not installed, .msg attachments are still detected and
reported (so the release manager knows one exists) but are marked as
unparsed rather than failing the whole collection run.
"""

from __future__ import annotations

import logging
import os
import re
import tempfile
from email import policy
from email.parser import BytesParser

from bs4 import BeautifulSoup

from tda.config import Config
from tda.http_client import ADOClient

try:
    import extract_msg
    _HAS_EXTRACT_MSG = True
except ImportError:
    _HAS_EXTRACT_MSG = False


_APPROVAL_KEYWORDS = [
    'approve', 'approved', 'approval', 'sign off', 'sign-off', 'signed off',
    'go ahead', 'go-ahead', 'looks good', 'lgtm', 'confirmed', 'authorised',
    'authorized',
]

_EMAIL_EXTENSIONS = ('.eml', '.msg')


def _iteration_attachments_for_result(run_id: str, result_id: str,
                                       client: ADOClient) -> list[dict]:
    """Return raw attachment refs (dicts with 'name'/'id') attached at the
    ITERATION/STEP level for one test result.

    ``get2('TestResultAttachment', ...)`` (the result-level attachments list)
    only returns attachments uploaded directly against the test result — it
    does NOT include attachments uploaded against an individual test step
    (iteration), which is how manual testers most commonly attach evidence
    (e.g. dragging a PO-approval .msg/.eml onto a step). Those only appear
    inline under ``iterationDetails[].attachments[]`` in the
    'TestResultByRunIdWithIterations' response — the same one
    ``tda.collectors.testing`` already reads for 'Step-Attachments', except
    that code only keeps the attachment *name* (for display) and discards
    the 'id' needed to download content. This refetches that response and
    keeps both, scoped to the single result we care about.
    """
    try:
        resp = client.get('TestResultByRunIdWithIterations', run_id)
    except Exception as e:
        logging.warning(
            "_iteration_attachments_for_result: run %s fetch failed — %s", run_id, e
        )
        return []

    for tres in resp.json().get('value', []):
        if str(tres.get('id', '')) != str(result_id):
            continue
        refs: list[dict] = []
        for iteration in tres.get('iterationDetails', []):
            refs.extend(iteration.get('attachments', []))
        return refs
    return []


def _find_confluence_links(text: str, confluence_url: str) -> list[str]:
    if not text or not confluence_url:
        return []
    base = re.escape(confluence_url.rstrip('/'))
    return re.findall(rf'{base}/\S+', text)


def _find_scwiki_links(text: str, scwiki_url: str) -> list[str]:
    """Same pattern as _find_confluence_links(), for the SC Wiki host.

    Additive alongside 'Confluence Links' (not a replacement) — as streams
    migrate PO-approval email evidence links from Confluence to SC Wiki, this
    surfaces them without requiring a schema change to the existing key.
    ``scwiki_url`` may be unset/empty (not every environment has it
    configured yet), in which case this always returns [].
    """
    if not text or not scwiki_url:
        return []
    base = re.escape(scwiki_url.rstrip('/'))
    return re.findall(rf'{base}/\S+', text)


def _find_approval_keywords(text: str) -> list[str]:
    if not text:
        return []
    lower = text.lower()
    return sorted({kw for kw in _APPROVAL_KEYWORDS if kw in lower})


def _parse_eml(content: bytes) -> dict:
    msg = BytesParser(policy=policy.default).parsebytes(content)
    body_part = msg.get_body(preferencelist=('plain', 'html'))
    body = ''
    if body_part is not None:
        raw_body = body_part.get_content()
        if body_part.get_content_type() == 'text/html':
            body = BeautifulSoup(raw_body, 'html.parser').get_text(separator=' ')
        else:
            body = raw_body
    return {
        'sender':  str(msg.get('From', '')),
        'subject': str(msg.get('Subject', '')),
        'body':    (body or '').strip()[:3000],
    }


def _parse_msg(content: bytes) -> dict | None:
    """Parse an Outlook .msg attachment. Returns None if extract-msg is not
    installed — the caller reports the attachment as detected-but-unparsed."""
    if not _HAS_EXTRACT_MSG:
        return None
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix='.msg', delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        # extract_msg.Message holds its own open handle on tmp_path until
        # closed. On Windows, os.unlink() on a still-open file raises
        # WinError 32 ("used by another process") — using it as a context
        # manager (calls .close() on __exit__) releases that handle before
        # the finally block below unlinks the temp file.
        with extract_msg.Message(tmp_path) as m:
            body = m.body or ''
            if not body and getattr(m, 'htmlBody', None):
                html = m.htmlBody
                if isinstance(html, bytes):
                    html = html.decode('utf-8', errors='ignore')
                body = BeautifulSoup(html, 'html.parser').get_text(separator=' ')
            sender = m.sender or ''
            subject = m.subject or ''
        return {
            'sender':  sender,
            'subject': subject,
            'body':    (body or '').strip()[:3000],
        }
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)



def analyze_po_approval_evidence(acceptance_tc_ids: list[str],
                                  tc_to_run_result: dict[str, tuple[str, str]],
                                  cfg: Config,
                                  client: ADOClient) -> list[dict]:
    """For each Acceptance Testing TC, inspect its attachments for an
    email-shaped PO-approval artifact.

    ``tc_to_run_result`` maps TC Id -> (Run Id, Result Id) for the latest run
    of that test case (the same de-duplicated mapping produced by
    ``extract_test_result_checks``).

    Returns a list of finding dicts (one per email-shaped attachment found),
    each with keys:
        'TC Id', 'Attachment Name', 'Parsed' (bool), 'Sender', 'Subject',
        'Confluence Links' (list), 'Approval Keywords Found' (list),
        'Body Snippet'
    Test cases with no email-shaped attachment are simply absent from the
    result — they may still have other evidence (screenshot, doc, URL
    comment) satisfying the generic CRITICAL evidence gate in Section 6.
    """
    findings: list[dict] = []
    for tc_id in acceptance_tc_ids:
        run_result = tc_to_run_result.get(tc_id)
        if not run_result:
            continue
        run_id, result_id = run_result

        # Two distinct attachment sources must both be checked:
        #  1. Result-level attachments (uploaded against the test result as a
        #     whole) — 'fileName' field, from TestResultAttachment.
        #  2. Iteration/step-level attachments (uploaded against an individual
        #     test step — the far more common place a manual tester drags an
        #     approval email) — 'name' field, from iterationDetails[].attachments[].
        # Missing (2) was a real bug: the PO-approval .msg evidence lives here
        # in practice, not in (1), so relying on (1) alone silently produced
        # zero findings even when a matching email attachment clearly existed.
        candidates: list[tuple[str, object]] = []  # (name, id)

        try:
            attach_resp = client.get2('TestResultAttachment', run_id, result_id)
            for attach in attach_resp.json().get('value', []):
                candidates.append((attach.get('fileName', ''), attach.get('id')))
        except Exception as e:
            logging.warning(
                "analyze_po_approval_evidence: TC %s result-level attachment list failed — %s",
                tc_id, e
            )

        for attach in _iteration_attachments_for_result(run_id, result_id, client):
            candidates.append((attach.get('name', ''), attach.get('id')))

        seen_ids: set[str] = set()
        for name, attachment_id in candidates:
            if not name.lower().endswith(_EMAIL_EXTENSIONS):
                continue  # not email-shaped — out of scope for this check

            if attachment_id is None:
                # Fall back to the last URL path segment when 'id' is absent.
                attachment_id = str(name).rstrip('/').split('/')[-1]
            attachment_id = str(attachment_id)
            if attachment_id in seen_ids:
                continue  # same attachment surfaced via both sources
            seen_ids.add(attachment_id)

            try:
                content = client.get_test_attachment_content(run_id, result_id, str(attachment_id))
            except Exception as e:
                logging.warning(
                    "analyze_po_approval_evidence: TC %s attachment download failed — %s", tc_id, e
                )
                findings.append({
                    'TC Id': tc_id, 'Attachment Name': name, 'Parsed': False,
                    'Sender': '', 'Subject': '', 'Confluence Links': [],
                    'Approval Keywords Found': [], 'Body Snippet': '',
                })
                continue

            parsed = None
            lower_name = name.lower()
            try:
                if lower_name.endswith('.eml'):
                    parsed = _parse_eml(content)
                elif lower_name.endswith('.msg'):
                    parsed = _parse_msg(content)
            except Exception as e:
                logging.warning(
                    "analyze_po_approval_evidence: TC %s attachment parse failed — %s", tc_id, e
                )
                parsed = None

            if parsed is None:
                findings.append({
                    'TC Id': tc_id, 'Attachment Name': name, 'Parsed': False,
                    'Sender': '', 'Subject': '', 'Confluence Links': [], 'SCWiki Links': [],
                    'Approval Keywords Found': [], 'Body Snippet': '',
                })
                continue

            findings.append({
                'TC Id': tc_id,
                'Attachment Name': name,
                'Parsed': True,
                'Sender': parsed['sender'],
                'Subject': parsed['subject'],
                'Confluence Links': _find_confluence_links(parsed['body'], cfg.confluence_url),
                'SCWiki Links': _find_scwiki_links(parsed['body'], cfg.scwiki_url),
                'Approval Keywords Found': _find_approval_keywords(
                    parsed['subject'] + ' ' + parsed['body']
                ),
                'Body Snippet': parsed['body'][:500],
            })

    return findings
