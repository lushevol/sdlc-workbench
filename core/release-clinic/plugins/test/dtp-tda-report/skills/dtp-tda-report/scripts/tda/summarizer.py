"""tda/summarizer.py — Compact TDA Summary Generator

Converts the full AutoTDAResults JSON (~200 KB) into a compact
AutoTDASummary JSON (~60-70 KB) for significantly faster SKILL analysis.

Key size reductions:
  - test_result_features (110 KB): step arrays stripped from Passed TCs;
    only exception TCs (non-Passed / step failure / no evidence) kept in full.
  - story_features (71 KB): replaced with a compact comment index (all 153
    stories, minimal fields) + pre-flagged exception lists (high similarity,
    cloned, concerning comments).

All gate-critical sections are kept verbatim — zero analysis coverage lost.

Usage (called automatically by AutoTDAScript_v2.py after full JSON is written):
    from tda.summarizer import generate_summary
    summary_path = generate_summary(tda_output, output_dir, release_stream, release_id)
"""

from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple


# ─── Keyword lists (sourced from SKILL.md analysis rules) ─────────────────────

CONCERN_KEYWORDS: List[str] = [
    "not working", "pending", "waiting", "failing",
    "to be confirmed", "will be done when", "isn't working",
    "mq issues", "not yet", "to handle", "may not be required",
    "on hold", "investigate", "investigation", "nack",
    "inarrear not accessible", "late change", "raised #",
    "still outstanding", "still to be", "still waiting",
]

CLONE_PATTERN: re.Pattern = re.compile(
    r"Copied with all (?:attachments and )?links from #(\d+)",
    re.IGNORECASE,
)

NEGATIVE_TEST_KEYWORDS: List[str] = [
    "negative", "invalid", "error", "reject", "rejection",
    "fail", "failure", "not found", "unauthori", "unauthorised",
    "unauthorized", "forbidden", "exceed", "cannot", "unable",
    "should not", "must not", "no result", "empty result", "no data",
    "boundary", "out of range", "wrong", "missing field",
    "mandatory field", "bad request", "exception",
]

_EVIDENCE_PATTERNS: List[re.Pattern] = [
    re.compile(r"https?://", re.IGNORECASE),
    re.compile(r"dev\.azure\.com", re.IGNORECASE),
    re.compile(r"#\d{5,}"),
]

HIGH_SIMILARITY_THRESHOLD: float = 85.0


# ─── Helpers ─────────────────────────────────────────────────────────────────


def _evidence_tier(tc: Dict[str, Any]) -> str:
    """Classify evidence presence for a test case into one of four tiers.

    Returns one of:
      "attachment"      — file attached at TC or step level
      "url_link"        — URL or ADO work-item link found in any comment field
      "comment_text"    — non-empty text comment present (may reference external
                          evidence such as linked ADO sub-tasks / testing tickets)
      "none"            — no comment, no attachment, no URL; truly missing
    """
    # Tier 1: file attachment at TC level
    attachment = tc.get("AttachmentName", "NOT AVAILABLE")
    if attachment and attachment != "NOT AVAILABLE":
        return "attachment"

    # Tier 2: step-level file attachments
    if tc.get("Step-Attachments"):
        return "attachment"

    # Collect all text from comment fields
    all_text = " ".join(filter(None, [
        str(tc.get("Comment", "")),
        " ".join(str(x) for x in tc.get("iterationId-outcome-comment", [])),
    ]))

    # Tier 3: URL or ADO work-item link in any comment
    for pat in _EVIDENCE_PATTERNS:
        if pat.search(all_text):
            return "url_link"

    # Tier 4: non-empty text comment (references external evidence)
    if all_text.strip():
        return "comment_text"

    # No evidence at all
    return "none"


def _tc_issues(tc: Dict[str, Any]) -> List[str]:
    """
    Return a list of objective issue strings for a test case. Empty = no issues.

    Only checks outcome and step-level pass/fail — not evidence (evidence
    detection requires AI judgment and is left to the SKILL).
    """
    issues: List[str] = []

    outcome = str(tc.get("Outcome", "")).strip()
    if outcome.lower() != "passed":
        issues.append(f"outcome={outcome}")

    for step in tc.get("Step-Iteration-Identifier-Outcome", []):
        if "-Passed" not in str(step):
            issues.append(f"step not passed: {step}")

    for itr in tc.get("iterationId-outcome-comment", []):
        parts = str(itr).split("-", 2)
        if len(parts) >= 2 and parts[1].lower() != "passed":
            issues.append(f"iteration not passed: {itr}")

    return issues


def _concern_comment(comment: str) -> bool:
    low = comment.lower()
    return any(kw in low for kw in CONCERN_KEYWORDS)


def _clone_source(comment: str) -> Optional[str]:
    m = CLONE_PATTERN.search(comment)
    return f"#{m.group(1)}" if m else None


def _negative_test_in_text(text: str) -> bool:
    low = text.lower()
    return any(kw in low for kw in NEGATIVE_TEST_KEYWORDS)


# ─── Section summarisers ─────────────────────────────────────────────────────


def _summarise_test_results(raw: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compact representation of test_result_features.

    Structure produced:
      _meta:
        total              — total TC count
        by_outcome         — {outcome: count}
        exceptions_count   — TCs with outcome/step failures
        no_evidence_count  — TCs with no detectable evidence (truly empty)
        evidence_tiers     — {tier: count} breakdown across all TCs
      exceptions[]         — full TC objects for outcome/step failures + "_issues" list
      no_evidence[]        — TCs where evidence_tier == "none" (no comment, no
                             attachment, no URL); these are the hard evidence gaps
      passed_brief[]       — clean TCs (passed + steps passed), step arrays stripped;
                             includes {tc_id, tc_name, outcome, run_id,
                             evidence_tier, comment, attachment} so the SKILL
                             can assess evidence quality without reading full results

    Evidence tiers (pre-computed by summarizer):
      "attachment"    — file attached at TC or step level (strongest)
      "url_link"      — URL or ADO work-item link in any comment field
      "comment_text"  — non-empty text comment only (may reference linked tickets)
      "none"          — truly no evidence; appears in no_evidence[]
    """
    if not raw:
        return {
            "_meta": {
                "total": 0, "by_outcome": {},
                "exceptions_count": 0, "no_evidence_count": 0,
                "evidence_tiers": {},
            },
            "exceptions": [],
            "no_evidence": [],
            "passed_brief": [],
        }

    by_outcome: Dict[str, int] = {}
    evidence_tiers: Dict[str, int] = {}
    exceptions: List[Dict[str, Any]] = []
    no_evidence: List[Dict[str, Any]] = []
    passed_brief: List[Dict[str, Any]] = []

    for tc in raw:
        outcome = str(tc.get("Outcome", "unknown")).strip()
        by_outcome[outcome] = by_outcome.get(outcome, 0) + 1

        ev_tier = _evidence_tier(tc)
        evidence_tiers[ev_tier] = evidence_tiers.get(ev_tier, 0) + 1

        issues = _tc_issues(tc)
        if issues:
            exc = dict(tc)
            exc["_issues"] = issues
            exc["_evidence_tier"] = ev_tier
            exceptions.append(exc)
        else:
            # Slim object — step arrays stripped but comment + evidence tier
            # retained so the SKILL can make the evidence call without the
            # full AutoTDAResults JSON.
            brief = {
                "tc_id":          tc.get("TestCase Id"),
                "tc_name":        tc.get("Test Name"),
                "outcome":        outcome,
                "run_id":         tc.get("Run Id"),
                "evidence_tier":  ev_tier,
                "comment":        str(tc.get("Comment", "")).strip()[:300],
                "attachment":     tc.get("AttachmentName", "NOT AVAILABLE"),
                "step_attachments": tc.get("Step-Attachments", []),
            }
            if ev_tier == "none":
                no_evidence.append(brief)
            else:
                passed_brief.append(brief)

    return {
        "_meta": {
            "total":             len(raw),
            "by_outcome":        by_outcome,
            "exceptions_count":  len(exceptions),
            "no_evidence_count": len(no_evidence),
            "evidence_tiers":    evidence_tiers,
        },
        "exceptions":    exceptions,
        "no_evidence":   no_evidence,
        "passed_brief":  passed_brief,
    }


def _summarise_stories(raw: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compact representation of story_features.

    Structure produced:
      _meta:
        total           — total story count
        by_state        — {state: count}
        desc_ok_count   — stories with Desc Present = OK
        ac_ok_count     — stories with AC Present = OK
      high_similarity   — full story objects where ratio >= 85%
      cloned_stories    — stories whose last comment matches clone pattern
      reprioritization_findings — stories where Description/AC were edited
                            after the story was first marked 'Prioritized'
                            (only populated when po_reprioritization_check_enabled
                            is true for the stream; PO Reprioritization Check ==
                            'MODIFIED_AFTER')
      open_comment_pre_flagged — stories with concerning last comment keywords
      negative_test_in_comments — stories whose comment contains negative-test keywords
      all_comments_review — compact per-story index (wi_id, wi_title, wi_state,
                            ratio, last_comment, last_comment_by, desc_present, ac_present,
                            desc_text, ac_text — desc_text/ac_text are HTML-stripped and
                            truncated to 400 chars; used for an INFORMATIONAL-only clarity/
                            sufficiency review of Description and Acceptance Criteria content,
                            never a CRITICAL/MODERATE gate)
    """
    if not raw:
        return {
            "_meta": {
                "total": 0, "by_state": {}, "desc_ok_count": 0, "ac_ok_count": 0,
                "app_id_ok_count": 0, "story_type_ok_count": 0,
            },
            "high_similarity": [],
            "cloned_stories": [],
            "reprioritization_findings": [],
            "open_comment_pre_flagged": [],
            "negative_test_in_comments": [],
            "missing_app_id": [],
            "missing_story_type": [],
            "all_comments_review": [],
        }

    by_state: Dict[str, int] = {}
    desc_ok = 0
    ac_ok = 0
    app_id_ok = 0
    story_type_ok = 0

    high_similarity: List[Dict[str, Any]] = []
    cloned_stories: List[Dict[str, Any]] = []
    reprioritization_findings: List[Dict[str, Any]] = []
    open_comments: List[Dict[str, Any]] = []
    neg_test_comments: List[Dict[str, Any]] = []
    missing_app_id: List[Dict[str, Any]] = []
    missing_story_type: List[Dict[str, Any]] = []
    all_comments: List[Dict[str, Any]] = []

    for story in raw:
        wi_id          = story.get("WI Id", "")
        wi_title       = story.get("WI Title", "")
        wi_state       = story.get("WI State", "")
        ratio          = story.get("Desc-AC-Similary-Ratio", 0)
        comment        = story.get("Story Last Comment", "")
        comment_by     = story.get("Story Last Comment By", "")
        desc_present   = story.get("Desc Present", "")
        ac_present     = story.get("AC Present", "")
        desc_text      = (story.get("Description Text", "") or "")[:400]
        ac_text        = (story.get("Acceptance Criteria Text", "") or "")[:400]
        wi_app_id      = story.get("WI App Id", "") or ""
        wi_story_type  = story.get("Automated", "") or ""
        reprioritization_check    = story.get("PO Reprioritization Check", "NA")
        reprioritization_findings_raw = story.get("PO Reprioritization Findings", [])

        # Aggregates
        by_state[wi_state] = by_state.get(wi_state, 0) + 1
        if desc_present == "OK":
            desc_ok += 1
        if ac_present == "OK":
            ac_ok += 1
        if wi_app_id.strip():
            app_id_ok += 1
        else:
            missing_app_id.append({"wi_id": wi_id, "wi_title": wi_title, "wi_state": wi_state})
        if wi_story_type.strip():
            story_type_ok += 1
        else:
            missing_story_type.append({"wi_id": wi_id, "wi_title": wi_title, "wi_state": wi_state})

        # Compact comment index — minimal fields only.
        # The SKILL uses this to review all comments for open/unresolved issues.
        # State/similarity/desc exceptions are pre-flagged in the dedicated lists below.
        all_comments.append({
            "wi_id":           wi_id,
            "wi_title":        wi_title,
            "last_comment":    comment,
            "last_comment_by": comment_by,
            "desc_present":    desc_present,
            "ac_present":      ac_present,
            "desc_text":       desc_text,
            "ac_text":         ac_text,
        })

        # Pre-flagged: high Desc-AC similarity
        try:
            ratio_f = float(ratio)
        except (TypeError, ValueError):
            ratio_f = 0.0
        if ratio_f >= HIGH_SIMILARITY_THRESHOLD:
            high_similarity.append({
                "wi_id":        wi_id,
                "wi_title":     wi_title,
                "wi_state":     wi_state,
                "ratio":        ratio,
                "last_comment": comment,
            })

        # Pre-flagged: cloned stories
        clone_src = _clone_source(comment)
        if clone_src:
            cloned_stories.append({
                "wi_id":        wi_id,
                "wi_title":     wi_title,
                "wi_state":     wi_state,
                "cloned_from":  clone_src,
                "last_comment": comment,
            })

        # Pre-flagged: concerning last comments
        if comment and _concern_comment(comment):
            open_comments.append({
                "wi_id":            wi_id,
                "wi_title":         wi_title,
                "wi_state":         wi_state,
                "last_comment":     comment,
                "last_comment_by":  comment_by,
            })

        # Pre-flagged: negative test keywords in comment
        if comment and _negative_test_in_text(comment):
            neg_test_comments.append({
                "wi_id":           wi_id,
                "comment_snippet": comment[:300],
            })

        # Pre-flagged: Description/AC modified after PO prioritization
        # (only meaningful when po_reprioritization_check_enabled is true for
        # this stream — otherwise every story's check is 'NA' and this list
        # stays empty).
        if reprioritization_check == "MODIFIED_AFTER":
            reprioritization_findings.append({
                "wi_id":       wi_id,
                "wi_title":    wi_title,
                "wi_state":    wi_state,
                "changes":     reprioritization_findings_raw,
                "po_comment":  story.get("PO Reprioritization Comment", {}),
            })

    return {
        "_meta": {
            "total":              len(raw),
            "by_state":           by_state,
            "desc_ok_count":      desc_ok,
            "ac_ok_count":        ac_ok,
            "app_id_ok_count":    app_id_ok,
            "story_type_ok_count": story_type_ok,
        },
        "high_similarity":            high_similarity,
        "cloned_stories":             cloned_stories,
        "reprioritization_findings":  reprioritization_findings,
        "open_comment_pre_flagged":   open_comments,
        "negative_test_in_comments":  neg_test_comments,
        "missing_app_id":             missing_app_id,
        "missing_story_type":         missing_story_type,
        "all_comments_review":        all_comments,
    }


# ─── Public API ──────────────────────────────────────────────────────────────

#: Sections copied verbatim from the full JSON — they are all small.
_VERBATIM_SECTIONS: Tuple[str, ...] = (
    "release_features",
    "release_pt_features",
    "snow_features",
    "pit_result",
    "pit_content",
    "aig_rollback_check",
    "testing_types",
    "unit_tests",
    "sonar_coverage",
    "sonar_quality_gates",
    "sonar_quality_gate_statuses",
    "sonar_exclusions",
    "sonar_new_code_periods",
    "sonar_skipped",
    "sonar_skip_reason",
    "genie_count",
    "genie_failures",       # 78 objects — kept for scenario-name analysis
    "bug_features",
    "application_features",
    "test_plan_features",
    "test_case_details",
    "traceability",
    "unique_test_cases",
    "blade_release_builds",
    "genie_tag_split",
    "genie_story_tag_split",
    "genie_story_type_breakdown",
    "po_approval_evidence",  # small (0-few entries) — Acceptance TC email evidence
    "snow_enabled",  # bool — whether SNOW collection was enabled for this stream/run
    "ado_organization",  # str — ADO org, used by the skill to build work item hyperlinks
    "ado_project",       # str — ADO project, used by the skill to build work item hyperlinks
    "skill_version_check",  # dict — local vs. canonical main-branch SKILL.md version (2026-10-13)
)


def generate_summary(
    tda_output: Dict[str, Any],
    output_dir: str,
    release_stream: str,
    release_id: str,
) -> str:
    """
    Generate a compact summary JSON alongside the full results file.

    Returns:
        Path to the written summary file.
    """
    summary: Dict[str, Any] = {
        "release_id":     tda_output.get("release_id"),
        "release_stream": tda_output.get("release_stream"),
        "_summary_meta": {
            "generated_from": f"AutoTDAResults_{release_stream}_{release_id}.json",
            "full_json_available": True,
            "note": (
                "Pre-processed compact summary for SKILL analysis. "
                "All gate/control checks preserved. "
                "Pass the AutoTDASummary file to the dtp-tda-report skill "
                "instead of the full AutoTDAResults file for faster analysis."
            ),
        },
    }

    # Copy verbatim sections
    for key in _VERBATIM_SECTIONS:
        summary[key] = tda_output.get(key)

    # Compact representations
    summary["test_results_summary"] = _summarise_test_results(
        tda_output.get("test_result_features", [])
    )
    summary["stories_summary"] = _summarise_stories(
        tda_output.get("story_features", [])
    )

    # Write file
    summary_file = os.path.join(
        output_dir,
        f"AutoTDASummary_{release_stream}_{release_id}.json",
    )
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    return summary_file
