"""tda/collectors/testing.py — Test plan, test result, and story WI collection.

Functions here talk to ADO Test Plans / Test Suites / Test Results APIs and
populate the result store with plan-level checks, result-level checks
(with optional step evidence), test case details, and story WI features.
"""

from __future__ import annotations

import logging
import re
import threading
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Any

try:
    from rapidfuzz import fuzz as _fuzz
except ImportError:
    from fuzzywuzzy import fuzz as _fuzz  # type: ignore[no-redef]

from tda.config import Config
from tda.http_client import ADOClient


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

def _clean_wi_text(html: str, max_len: int = 2000) -> str:
    """Strip HTML tags and collapse whitespace from an ADO rich-text field.

    Used to retain a readable, truncated copy of Description/Acceptance
    Criteria text (in addition to the existing presence flag and similarity
    ratio) so the SKILL can assess clarity/sufficiency as an informational
    finding — never a CRITICAL/MODERATE gate.
    """
    if not html:
        return ''
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:max_len]


# ---------------------------------------------------------------------------
# BR / AC placeholder detection
# ---------------------------------------------------------------------------

# Exact tokens (after normalisation) that by themselves constitute a placeholder
_PLACEHOLDER_EXACT: frozenset[str] = frozenset({
    '', 'na', 'n/a', 'tbd', 'tbc', 'none', 'nil', '-', '--',
    'not applicable', 'not required', 'same as description',
    'as per description', 'refer description', 'refer to description',
})

# Sub-phrases that flag a field as a cross-reference without a hyperlink
_PLACEHOLDER_PHRASES: tuple[str, ...] = (
    'as mentioned in confluence',
    'refer to confluence',
    'see confluence',
    'as mentioned in jira',
    'refer above',
    'as above',
    'refer description',
    'as per description',
    'as mentioned above',
    'details in confluence',
    'please refer confluence',
)


def _classify_ac_text(text: str, wi_relations: list[dict] | None = None) -> str:
    """Classify a Description or Acceptance Criteria plain-text value.

    Returns one of:
      'EMPTY'                — field is blank / not present
      'PLACEHOLDER'          — field contains only a placeholder token/phrase
      'CONFLUENCE_NO_LINK'   — mentions Confluence but WI has no Confluence relation link
      'OK'                   — field appears to have substantive content

    ``wi_relations`` (list of ADO relation dicts with 'url' key) is used for
    the confluence-no-link check.  If omitted the check is skipped.
    """
    if not text or not text.strip():
        return 'EMPTY'

    normalised = text.lower().strip()

    # Short text that matches an exact placeholder token
    if normalised in _PLACEHOLDER_EXACT:
        return 'PLACEHOLDER'

    # Short text dominated by a placeholder phrase
    for phrase in _PLACEHOLDER_PHRASES:
        if phrase in normalised and len(normalised) < len(phrase) + 60:
            return 'PLACEHOLDER'

    # Mentions "confluence" but no Confluence URL exists among WI relations
    if 'confluence' in normalised and wi_relations is not None:
        has_confluence_link = any(
            'confluence' in (rel.get('url') or '').lower()
            for rel in wi_relations
        )
        if not has_confluence_link:
            return 'CONFLUENCE_NO_LINK'

    return 'OK'


# ---------------------------------------------------------------------------
# Check 2: Test case step expected-result quality
# ---------------------------------------------------------------------------

# Tokens (after strip/lower) that count as an empty expected result
_EMPTY_EXPECTED_TOKENS: frozenset[str] = frozenset({
    '', '-', '--', 'na', 'n/a', 'tbd', 'tbc', 'none', 'nil',
    'not applicable', 'pass', 'passed',
})


def _analyse_tc_steps(steps_xml: str) -> dict:
    """Parse ADO ``Microsoft.VSTS.TCM.Steps`` XML and report step quality.

    Returns::

        {
            'total_steps':          int,   # ActionStep steps + Shared Steps refs (compref)
            'empty_expected':       int,   # steps whose expectedresult is blank/placeholder
            'tc_steps_check':       str,   # 'OK' | 'EMPTY_EXPECTED' | 'NO_STEPS' | 'PARSE_ERROR'
        }

    The ADO format is::

        <steps id="0" last="N">
          <step id="2" type="ActionStep">    <!-- or type="ValidateStep" -->
            <parameterizedString isformatted="true">action text</parameterizedString>
            <parameterizedString isformatted="true">expected result text</parameterizedString>
            <description/>
          </step>
          <compref id="3" ref="12345"/>   <!-- Shared Steps reference -->
          ...
        </steps>

    Both ``ActionStep`` and ``ValidateStep`` step types are counted — ``ActionStep``
    is the standard ADO type; ``ValidateStep`` is used by some streams (e.g. KDB)
    and has an identical XML structure.  HTML tags inside the string are stripped before the emptiness check.

    ``<compref>`` elements are Shared Steps references — a common ADO authoring
    pattern where one or more steps are defined in a separate shared test case
    and referenced here.  The parser counts each ``<compref>`` as one logical
    step so that test cases authored entirely via Shared Steps are not
    incorrectly reported as having zero steps (NO_STEPS).  The expected-result
    quality check is skipped for compref entries since their step content is
    defined externally.
    """
    if not steps_xml or not steps_xml.strip():
        return {'total_steps': 0, 'empty_expected': 0, 'tc_steps_check': 'NO_STEPS'}

    try:
        root = ET.fromstring(steps_xml)
    except ET.ParseError as exc:
        logging.warning("_analyse_tc_steps: XML parse error — %s", exc)
        return {'total_steps': 0, 'empty_expected': 0, 'tc_steps_check': 'PARSE_ERROR'}

    total = 0
    empty = 0

    # Inline step elements — ActionStep (standard) and ValidateStep (used by some streams e.g. KDB)
    for step in root.findall('.//step'):
        total += 1
        # The second parameterizedString is the expected result
        pstrings = step.findall('parameterizedString')
        if len(pstrings) < 2:
            empty += 1
            continue
        raw_html = ET.tostring(pstrings[1], encoding='unicode', method='xml')
        # Strip XML/HTML tags to get plain text
        plain = re.sub(r'<[^>]+>', '', raw_html).strip()
        if plain.lower() in _EMPTY_EXPECTED_TOKENS:
            empty += 1

    # Shared Steps references (compref) — count each as one logical step
    total += len(root.findall('.//compref'))

    check = 'NO_STEPS' if total == 0 else ('EMPTY_EXPECTED' if empty > 0 else 'OK')
    return {'total_steps': total, 'empty_expected': empty, 'tc_steps_check': check}


# ---------------------------------------------------------------------------
# Test-suite helpers
# ---------------------------------------------------------------------------

def return_test_suites(test_plan_id: str, client: ADOClient) -> list[dict]:
    """Return the flat list of test suites for a given test plan."""
    r = client.get('TestSuitesForTestPlan', test_plan_id)
    return r.json().get('value', [])


def return_test_cases_from_suite(test_plan_id: str,
                                  test_suites: list[dict],
                                  client: ADOClient) -> list[dict]:
    """Return all test cases across every suite in a test plan."""
    all_tcs: list[dict] = []
    for suite in test_suites:
        suite_id = str(suite['id'])
        r = client.get2('TestCasesForTestSuite', test_plan_id, suite_id)
        tcs = r.json().get('value', [])
        for tc in tcs:
            tc['suiteId'] = suite_id
        all_tcs.extend(tcs)
    return all_tcs


def populate_test_case_details(test_case_ids: list[str],
                                client: ADOClient,
                                cfg=None,
                                prefetched_batch: dict | None = None) -> list[dict]:
    """Batch-fetch WI details for a list of test case IDs.

    Includes Custom.TestType (or the configured test_type_field) so the report
    can classify each TC as System / Integration / Acceptance / Performance Testing.

    ``prefetched_batch``, when supplied (e.g. the ``tc_fields_batch`` already
    fetched by ``build_traceability`` for this exact same TC set), is used
    directly instead of issuing a second identical ``workitemsbatch`` call.

    Returns a list of detail dicts (one per TC).
    """
    if not test_case_ids:
        return []

    test_type_field = cfg.test_type_field if cfg else 'Custom.TestType'

    batch = prefetched_batch if prefetched_batch is not None else client.fetch_work_items_batch(test_case_ids)
    details: list[dict] = []
    for tc_id in test_case_ids:
        wi = batch.get(str(tc_id), {})
        f = wi.get('fields', {})
        # Check 2: analyse step expected results from the already-fetched batch field
        steps_xml = f.get('Microsoft.VSTS.TCM.Steps', '') or ''
        step_analysis = _analyse_tc_steps(steps_xml)
        details.append({
            'TC Id': tc_id,
            'TC Title': f.get('System.Title', ''),
            'TC State': f.get('System.State', ''),
            'TC Priority': f.get('Microsoft.VSTS.Common.Priority', ''),
            'TC Automated': f.get('Microsoft.VSTS.TCM.AutomationStatus', ''),
            'TC TestType': f.get(test_type_field, ''),
            # Check 2 fields
            'TC Total Steps':    step_analysis['total_steps'],
            'TC Empty Expected': step_analysis['empty_expected'],
            'TC Steps Check':    step_analysis['tc_steps_check'],
        })
    return details


# ---------------------------------------------------------------------------
# Test plan level checks
# ---------------------------------------------------------------------------

def extract_test_plan_checks(response,
                              client: ADOClient) -> dict:
    """Extract plan-level metadata from a test-plan ADO response."""
    try:
        data = response.json()
        checks = {
            'Test Plan Id': data.get('id', ''),
            'Test Plan Name': data.get('name', ''),
            'State': data.get('state', ''),
            'Start Date': data.get('startDate', ''),
            'End Date': data.get('endDate', ''),
        }
        owner = data.get('owner', {})
        checks['Owner'] = owner.get('uniqueName', owner.get('displayName', ''))
        return checks
    except Exception as e:
        logging.warning("extract_test_plan_checks: failed — %s", e)
        return {}


# ---------------------------------------------------------------------------
# Test result level checks (with step evidence)
# ---------------------------------------------------------------------------

def _parse_result_row(run_id: str, tres: dict) -> dict:
    """Parse a single result dict already enriched with iterationDetails.

    ``tres`` comes from GET /test/Runs/{id}/results?detailsToInclude=Iterations
    so it already contains 'comment' and 'iterationDetails' inline — no extra
    HTTP calls needed for comment or step evidence.
    """
    result_id = str(tres.get('id', ''))
    tc_id     = str(tres.get('testCase', {}).get('id', 'UNKNOWN'))

    comment = tres.get('comment', '') or ''

    iter_outcome_comment: list[str] = []
    step_outcomes:        list[str] = []
    step_attachments:     list[str] = []
    # Tracks whether any iteration carries a genuine (non-empty) comment of its
    # own — distinct from `iter_outcome_comment`, which is a list of debug
    # display strings that is ALWAYS non-empty once a TC has >=1 iteration
    # (it embeds a 'NOT AVAILABLE' placeholder rather than being empty). Using
    # that list's truthiness to decide whether an attachment check is needed
    # meant the check was almost never True in practice (every executed TC has
    # >=1 iteration), so _fetch_attachments() effectively never ran and
    # result-level attachments (e.g. a .docx uploaded against the test result,
    # not the step) were silently missed even when they exist in ADO.
    has_real_iteration_comment = False

    for iteration in tres.get('iterationDetails', []):
        raw_iter_comment = iteration.get('comment', '') or ''
        if raw_iter_comment.strip():
            has_real_iteration_comment = True
        iter_outcome_comment.append(
            f"{iteration.get('id','')}-"
            f"{iteration.get('outcome','NOT AVAILABLE')}-"
            f"{iteration.get('comment','NOT AVAILABLE')}"
        )
        for action in iteration.get('actionResults', []):
            step_outcomes.append(
                f"{action.get('stepIdentifier','NOT AVAILABLE')}-"
                f"{action.get('outcome','NOT AVAILABLE')}"
            )
        for step_attach in iteration.get('attachments', []):
            step_attachments.append(str(step_attach.get('name', 'NOT AVAILABLE')))

    return {
        'TestCase Id': tc_id,
        'Test Name':   tres.get('testCase', {}).get('name', ''),
        'Outcome':     tres.get('outcome', ''),
        'Run Id':      run_id,
        'Result Id':   result_id,
        'Comment':                           comment if comment else 'NOT AVAILABLE',
        'AttachmentName':                    'NOT AVAILABLE',  # filled by _fetch_attachments if needed
        'AttachmentSource':                  'Step' if step_attachments else 'NOT AVAILABLE',
        'iterationId-outcome-comment':       iter_outcome_comment,
        'Step-Iteration-Identifier-Outcome': step_outcomes,
        'Step-Attachments':                  step_attachments,
        # Fetch result-level attachments unless we already have step-level
        # attachments (free, inline) — a real comment (top-level or
        # per-iteration) does NOT by itself prove an attachment doesn't also
        # exist, so it no longer suppresses the check.
        '_needs_attachment_check':           not step_attachments,
    }


def _fetch_attachments(result: dict, client: ADOClient) -> dict:
    """Fetch result-level attachments for one row (called only when no other evidence)."""
    try:
        attach_resp = client.get2(
            'TestResultAttachment', result['Run Id'], result['Result Id']
        )
        for attach in attach_resp.json().get('value', []):
            result['AttachmentName'] = attach.get('fileName', 'NOT AVAILABLE')
            result['AttachmentSource'] = 'Result'
            break  # first attachment is enough
    except Exception as e:
        logging.warning(
            "_fetch_attachments: TC %s — %s", result.get('TestCase Id', '?'), e
        )
    result.pop('_needs_attachment_check', None)
    return result


def extract_test_result_checks(response,
                                 test_plan_id: str,
                                 cfg: Config,
                                 client: ADOClient) -> list[dict]:
    """Collect run outcomes and evidence for every result in the test plan.

    Optimised call pattern (replaces 3 calls/result with 1):
      1. GET /test/runs?planId=…            — list runs          (1 call)
      2. GET /test/Runs/{id}/results
             ?detailsToInclude=Iterations   — results + steps    (1 call per run)
      3. GET …/attachments                  — only for results
                                              with no other evidence (rare)

    Before this change: ~622 results × 3 calls = ~1,866 ADO calls.
    After:              (runs) + (runs) + (sparse attachments) ≈ tens of calls.
    """
    runs_resp = client.get('TestRunByPlanId', test_plan_id)
    parsed: list[dict] = []
    # Run-level attachments: uploaded to the run summary page (_a=runSummary).
    # Keyed by run_id → first attachment filename.  Used as a fallback for
    # results that have no step-level or result-level evidence (see below).
    run_level_attachments: dict[str, str] = {}

    for run in runs_resp.json().get('value', []):
        if str(run.get('state', '')) == '255':   # aborted/cancelled
            continue
        run_id = str(run['id'])
        try:
            # Single call returns results WITH inline comment + iterationDetails
            results_resp = client.get('TestResultByRunIdWithIterations', run_id)
            for tres in results_resp.json().get('value', []):
                if 'outcome' not in tres or 'testCase' not in tres:
                    continue
                parsed.append(_parse_result_row(run_id, tres))
        except Exception as e:
            logging.warning(
                "extract_test_result_checks: run %s fetch failed — %s", run_id, e
            )

        # Fetch run-level attachments (evidence uploaded to the run summary
        # page rather than to an individual result).  One extra GET per run —
        # negligible compared to the iterations call above.
        try:
            run_attach_resp = client.get('TestRunAttachment', run_id)
            run_attach_list = run_attach_resp.json().get('value', [])
            if run_attach_list:
                run_level_attachments[run_id] = run_attach_list[0].get(
                    'fileName', 'NOT AVAILABLE'
                )
        except Exception as e:
            logging.warning(
                "extract_test_result_checks: run %s run-level attachment fetch failed — %s",
                run_id, e,
            )

    # -----------------------------------------------------------------------
    # Deduplicate: keep only the latest run per test case.
    # ADO run IDs are sequential integers — highest run ID = most recent run.
    # Without this, every re-run of a TC produces an extra row, inflating the
    # total count and potentially surfacing intermediate Paused/Failed outcomes
    # that were subsequently fixed in a later run.
    # -----------------------------------------------------------------------
    latest: dict[str, dict] = {}
    for row in parsed:
        tc_id = row['TestCase Id']
        existing = latest.get(tc_id)
        if existing is None or int(row['Run Id']) > int(existing['Run Id']):
            latest[tc_id] = row
    deduped = list(latest.values())

    logging.info(
        "extract_test_result_checks: plan=%s — %d raw result(s) across all runs, "
        "deduplicated to %d unique test cases (latest run per TC kept). "
        "%d need attachment check",
        test_plan_id, len(parsed), len(deduped),
        sum(1 for r in deduped if r.get('_needs_attachment_check')),
    )
    parsed = deduped

    # Sparse attachment fetch — only results with no comment and no step evidence
    needs_attach = [r for r in parsed if r.get('_needs_attachment_check')]
    no_attach    = [r for r in parsed if not r.get('_needs_attachment_check')]
    for r in no_attach:
        r.pop('_needs_attachment_check', None)

    if needs_attach:
        if cfg.parallel_enabled:
            # Kept modest (not 8) — see traceability.py for the on-prem ADO Server
            # 'Concurrency' resource-governor rationale (2026-07-14 incident).
            with ThreadPoolExecutor(max_workers=5) as ex:
                futures = {ex.submit(_fetch_attachments, r, client): r for r in needs_attach}
                for fut in as_completed(futures):
                    try:
                        fut.result()
                    except Exception as e:
                        logging.warning("extract_test_result_checks: attachment fetch error — %s", e)
        else:
            for r in needs_attach:
                _fetch_attachments(r, client)

        # Fallback: if a result still has no evidence after the result-level
        # attachment check, use the run-level attachment (evidence uploaded to
        # the run summary page — _a=runSummary — rather than to the result).
        for r in needs_attach:
            if r.get('AttachmentName', 'NOT AVAILABLE') == 'NOT AVAILABLE':
                run_attach = run_level_attachments.get(r['Run Id'])
                if run_attach:
                    r['AttachmentName'] = run_attach
                    r['AttachmentSource'] = 'Run'
                    logging.info(
                        "extract_test_result_checks: TC %s — no result-level attachment found; "
                        "using run-level attachment '%s' from run %s",
                        r.get('TestCase Id', '?'), run_attach, r['Run Id'],
                    )

    return no_attach + needs_attach


# ---------------------------------------------------------------------------
# Story items
# ---------------------------------------------------------------------------

def get_story_items_in_release(work_items: list[dict],
                                batch: dict,
                                cfg: Config,
                                client: ADOClient | None = None) -> list[dict]:
    """Extract story-level WI data from the pre-fetched batch.

    ``batch`` is a dict keyed by WI ID string (from fetch_work_items_batch).
    When ``client`` is supplied, story last comments are fetched in parallel
    and the Desc-AC similarity ratio is computed via fuzzywuzzy/rapidfuzz.
    Returns a list of story feature dicts.
    """
    story_features: list[dict] = []

    for wi in work_items:
        wi_url  = wi.get('url', '')
        wi_id   = wi_url.split('workItems/')[-1]
        wi_data = batch.get(wi_id, {})
        fields  = wi_data.get('fields', {})

        wi_type = fields.get('System.WorkItemType', '')
        if wi_type not in ('User Story', 'Product Backlog Item', 'Story'):
            continue

        # Desc-AC similarity — compute from batch fields if present
        story_desc = fields.get('System.Description') or ''
        story_ac   = fields.get('Microsoft.VSTS.Common.AcceptanceCriteria') or ''
        try:
            similarity = _fuzz.partial_ratio(story_desc, story_ac)
        except Exception:
            similarity = 'ERROR'

        # Raw text (HTML-stripped, truncated) kept alongside the presence
        # flags above so the SKILL can assess Description/AC *clarity and
        # sufficiency* as an informational finding — this is never a gate
        # (CRITICAL/MODERATE), only a MINOR/Info observation.
        story_desc_text = _clean_wi_text(story_desc)
        story_ac_text    = _clean_wi_text(story_ac)

        # Placeholder / cross-reference-without-link detection (Check 1).
        # Uses WI relations from the batch (expanded via $expand=relations).
        wi_relations = wi_data.get('relations') or []
        desc_classification = _classify_ac_text(story_desc_text, wi_relations)
        ac_classification   = _classify_ac_text(story_ac_text,   wi_relations)

        feature: dict[str, Any] = {
            'WI Id': wi_id,
            'WI Title': fields.get('System.Title', ''),
            'WI Type': wi_type,
            'WI State': fields.get('System.State', ''),
            'WI App Id': fields.get(cfg.story_app_id_field, ''),
            'WI Tags': fields.get('System.Tags', ''),
            'Automated': fields.get(cfg.story_type_field, ''),
            'Test Type': fields.get(cfg.test_type_field, ''),
            'Desc Present': 'OK' if story_desc else 'No',
            'AC Present':   'OK' if story_ac   else 'No',
            'Desc-AC-Similary-Ratio': similarity,
            'Description Text':          story_desc_text,
            'Acceptance Criteria Text':  story_ac_text,
            # Check 1: placeholder / insufficient-content classification
            'Desc Classification':  desc_classification,
            'AC Classification':    ac_classification,
            'Story Last Comment':    'NA',
            'Story Last Comment By': 'NA',
            'PO Reprioritization Check':     'NA',
            'PO Reprioritization Findings':  [],
            'PO Reprioritization Comment':   {},
        }
        story_features.append(feature)

    # Parallel fan-out: fetch last comment for each story.
    # Gated by cfg.story_comments_enabled (streams.<STREAM>.story_comments_enabled
    # in stream_config.yaml, default False) — when disabled, this whole block
    # (and its one CommentByStoryId ADO call per story) is skipped entirely,
    # not merely serialized, reducing total ADO API call volume for the run.
    if not cfg.story_comments_enabled:
        print(f'        Story comment fetch disabled for this stream '
              f'(story_comments_enabled: false in stream_config.yaml) — skipping '
              f'{len(story_features)} CommentByStoryId call(s).', flush=True)
    elif client and story_features:
        def _fetch_comment(feat: dict) -> None:
            try:
                r = client.get('CommentByStoryId', feat['WI Id'])
                data = r.json()
                if data.get('count', 0) > 0:
                    first = data['comments'][0]
                    text = first.get('text', '') or ''
                    # strip HTML tags for readability
                    text = re.sub(r'<[^>]+>', '', text)[:150].strip()
                    feat['Story Last Comment']    = text
                    feat['Story Last Comment By'] = (
                        first.get('createdBy', {}).get('displayName', 'Unknown')
                    )
            except Exception as exc:
                logging.warning('CommentByStoryId failed for WI %s — %s', feat['WI Id'], exc)

        if cfg.parallel_enabled:
            print(f'        [Thread] Fetching comments for {len(story_features)} stories in parallel...', flush=True)
            with ThreadPoolExecutor(max_workers=5) as ex:
                list(ex.map(_fetch_comment, story_features))
        else:
            print(f'        Fetching comments for {len(story_features)} stories sequentially '
                  f'(PARALLEL_ENABLED=false)...', flush=True)
            for feat in story_features:
                _fetch_comment(feat)

    # Parallel fan-out: PO re-prioritization check for each story.
    # Gated by cfg.po_reprioritization_check_enabled
    # (streams.<STREAM>.po_reprioritization_check_enabled in stream_config.yaml,
    # default False) — when disabled, this whole block (and its one
    # WorkItemUpdates/revision-history ADO call per story) is skipped entirely.
    #
    # Detects Description / Acceptance Criteria edits made *after* the story
    # first transitioned into the 'Prioritized' state — per governance
    # guidelines, a story whose scope (Description/AC) changes post-
    # prioritization should have been re-prioritized by the PO. This walks
    # the WI revision history (not just current-state fields) since that is
    # the only way to see historical state transitions and field diffs.
    if not cfg.po_reprioritization_check_enabled:
        print(f'        PO re-prioritization check disabled for this stream '
              f'(po_reprioritization_check_enabled: false in stream_config.yaml) — '
              f'skipping {len(story_features)} WorkItemUpdates call(s).', flush=True)
    elif client and story_features:
        def _check_reprioritization(feat: dict) -> None:
            try:
                r = client.get('WorkItemUpdates', feat['WI Id'])
                updates = r.json().get('value', [])

                # Find the FIRST revision where System.State transitioned
                # into 'Prioritized'.
                prioritized_rev: int | None = None
                for u in updates:
                    state_change = (u.get('fields') or {}).get('System.State')
                    if not state_change:
                        continue
                    new_state = str(state_change.get('newValue', '') or '').strip().lower()
                    if new_state == 'prioritized':
                        prioritized_rev = u.get('rev')
                        break

                if prioritized_rev is None:
                    feat['PO Reprioritization Check'] = 'NOT_PRIORITIZED'
                    return

                # Any Description / Acceptance Criteria edits in revisions
                # AFTER the prioritization revision.
                post_changes: list[dict] = []
                for u in updates:
                    rev = u.get('rev')
                    if rev is None or rev <= prioritized_rev:
                        continue
                    fields_changed = u.get('fields') or {}
                    changed_by = (u.get('revisedBy') or {}).get('displayName', 'Unknown')
                    changed_date = u.get('revisedDate', '')
                    for field_ref, label in (
                        ('System.Description', 'Description'),
                        ('Microsoft.VSTS.Common.AcceptanceCriteria', 'Acceptance Criteria'),
                    ):
                        if field_ref in fields_changed:
                            post_changes.append({
                                'Field':        label,
                                'Changed By':   changed_by,
                                'Changed Date': changed_date,
                            })

                feat['PO Reprioritization Findings'] = post_changes
                feat['PO Reprioritization Check'] = 'MODIFIED_AFTER' if post_changes else 'OK'

                # When MODIFIED_AFTER: fetch comments to find a PO acceptance
                # recorded AFTER the last scope change. This runs regardless of
                # story_comments_enabled — it is targeted evidence collection
                # for a specific governance check, not general comment display.
                if post_changes:
                    latest_change_date = max(
                        (c.get('Changed Date', '') for c in post_changes), default=''
                    )
                    try:
                        r_cmt = client.get('CommentByStoryId', feat['WI Id'])
                        cmt_data = r_cmt.json()
                        if cmt_data.get('count', 0) > 0:
                            # Find all comments posted AFTER the latest change date
                            post_cmt = [
                                c for c in cmt_data['comments']
                                if c.get('createdDate', '') > latest_change_date
                            ]
                            if post_cmt:
                                best = max(post_cmt, key=lambda c: c.get('createdDate', ''))
                                cmt_text = re.sub(r'<[^>]+>', '', best.get('text', '') or '').strip()[:500]
                                feat['PO Reprioritization Comment'] = {
                                    'text': cmt_text,
                                    'by':   best.get('createdBy', {}).get('displayName', 'Unknown'),
                                    'date': best.get('createdDate', ''),
                                }
                    except Exception as cmt_exc:
                        logging.warning(
                            'CommentByStoryId (reprioritization evidence) failed for WI %s — %s',
                            feat['WI Id'], cmt_exc,
                        )
            except Exception as exc:
                logging.warning('WorkItemUpdates failed for WI %s — %s', feat['WI Id'], exc)
                feat['PO Reprioritization Check'] = 'ERROR'

        if cfg.parallel_enabled:
            print(f'        [Thread] Checking PO re-prioritization for {len(story_features)} stories in parallel...', flush=True)
            with ThreadPoolExecutor(max_workers=5) as ex:
                list(ex.map(_check_reprioritization, story_features))
        else:
            print(f'        Checking PO re-prioritization for {len(story_features)} stories sequentially '
                  f'(PARALLEL_ENABLED=false)...', flush=True)
            for feat in story_features:
                _check_reprioritization(feat)

    return story_features
