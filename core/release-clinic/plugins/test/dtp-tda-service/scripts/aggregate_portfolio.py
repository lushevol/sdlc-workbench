"""scripts/aggregate_portfolio.py — Admin-only TDA portfolio/trend aggregator.

Reads the append-only job registry (JSONL) written by
``service/registry.py`` after every completed or failed TDA collection job,
and produces one compact aggregate JSON summarising usage, releases covered,
trends over time, and recurring/fragile patterns — across one stream or all
streams.

This script does NOT re-implement any of dtp-tda-report/SKILL.md's judgement
based analysis rules (severity classification, gate verdicts). It only
aggregates the raw/structural facts already captured per job (counts,
pass/fail totals, field completeness, Sonar quality gate names, Genie
failure scenario names). A companion Copilot skill (e.g.
dtp-tda-portfolio-report) is expected to turn this aggregate JSON into a
narrative management summary.

Intended audience: admins only. Requires filesystem access to the registry
file (or, in a future iteration, an auth-gated admin API endpoint) — this
script has no built-in access control of its own.

Usage:
    python aggregate_portfolio.py \\
        --registry /path/to/tda_job_registry.jsonl \\
        [--stream RATES FXO ...] \\
        [--since 2026-01-01] [--until 2026-12-31] \\
        [--top-n 10] \\
        [--output portfolio_summary.json]

If --registry is omitted, it falls back to the TDA_REGISTRY_PATH env var,
then to <TDA_OUTPUT_DIR>/tda_job_registry.jsonl, then to
./AutoTDAReports/tda_job_registry.jsonl.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def default_registry_path() -> str:
    override = os.environ.get("TDA_REGISTRY_PATH", "").strip()
    if override:
        return override
    output_dir = os.environ.get("TDA_OUTPUT_DIR", "./AutoTDAReports")
    return os.path.join(output_dir, "tda_job_registry.jsonl")


def load_records(registry_path: str) -> List[dict]:
    if not os.path.exists(registry_path):
        raise FileNotFoundError(f"Registry file not found: {registry_path}")

    records: List[dict] = []
    with open(registry_path, "r", encoding="utf-8-sig") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                print(
                    f"WARNING: skipping malformed line {line_no} in {registry_path}: {exc}",
                    file=sys.stderr,
                )
    return records


def _parse_dt(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        # Service records use UTC offsets. Interpret older naive records as UTC.
        parsed = datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except ValueError:
        return None


def _date_boundary(value: Optional[str], *, end: bool = False) -> Optional[datetime]:
    """Read a complete UTC filter day and reject invalid or ambiguous dates."""
    if value is None:
        return None
    parsed = datetime.strptime(value, "%Y-%m-%d")
    if parsed.date().isoformat() != value:
        raise ValueError("Use YYYY-MM-DD.")
    if end:
        parsed = parsed.replace(hour=23, minute=59, second=59, microsecond=999999)
    return parsed.replace(tzinfo=timezone.utc)


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

def filter_records(records: Iterable[dict], streams: Optional[List[str]],
                    since: Optional[datetime], until: Optional[datetime]) -> List[dict]:
    streams_upper = {s.upper() for s in streams} if streams else None
    out = []
    for rec in records:
        if streams_upper and (rec.get("release_stream") or "").upper() not in streams_upper:
            continue
        completed_at = _parse_dt(rec.get("completed_at")) or _parse_dt(rec.get("submitted_at"))
        if since and completed_at and completed_at < since:
            continue
        if until and completed_at and completed_at > until:
            continue
        out.append(rec)
    return out


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def aggregate(records: List[dict], top_n: int = 10) -> dict:
    total_jobs   = len(records)
    complete     = [r for r in records if r.get("status") == "complete"]
    failed       = [r for r in records if r.get("status") == "failed"]
    releases     = {(r.get("release_stream"), r.get("release_id")) for r in records if r.get("release_id")}

    per_stream: Dict[str, dict] = defaultdict(lambda: {
        "job_count": 0, "complete_count": 0, "failed_count": 0,
        "releases": set(), "genie_fail_rates": [], "missing_app_id_rates": [],
        "missing_story_type_rates": [], "sonar_non_standard_count": 0,
    })

    genie_failure_names: Counter = Counter()
    genie_failure_names_by_stream: Dict[str, Counter] = defaultdict(Counter)
    fragile_missing_app_id: Counter = Counter()
    fragile_missing_story_type: Counter = Counter()
    sonar_non_standard_pipelines: Counter = Counter()
    failure_reasons: Counter = Counter()
    trends_by_month: Dict[str, dict] = defaultdict(lambda: {
        "job_count": 0, "complete_count": 0, "failed_count": 0,
    })

    for rec in records:
        stream = (rec.get("release_stream") or "UNKNOWN").upper()
        bucket = per_stream[stream]
        bucket["job_count"] += 1
        if rec.get("release_id"):
            bucket["releases"].add(rec["release_id"])

        completed_at = _parse_dt(rec.get("completed_at")) or _parse_dt(rec.get("submitted_at"))
        month_key = completed_at.strftime("%Y-%m") if completed_at else "unknown"
        month_bucket = trends_by_month[month_key]
        month_bucket["job_count"] += 1

        if rec.get("status") == "complete":
            bucket["complete_count"] += 1
            month_bucket["complete_count"] += 1

            genie = rec.get("genie") or {}
            if genie.get("fail_rate_pct") is not None:
                bucket["genie_fail_rates"].append(genie["fail_rate_pct"])
            for name in genie.get("failed_scenarios") or []:
                genie_failure_names[name] += 1
                genie_failure_names_by_stream[stream][name] += 1

            gates = rec.get("sonar_quality_gates") or {}
            bucket["sonar_non_standard_count"] += gates.get("non_standard_count", 0)
            for p in gates.get("non_standard_pipelines") or []:
                pipeline = p.get("pipeline")
                if pipeline:
                    sonar_non_standard_pipelines[pipeline] += 1

            completeness = rec.get("story_field_completeness") or {}
            total_stories = completeness.get("total_stories") or 0
            if total_stories:
                bucket["missing_app_id_rates"].append(
                    100 * completeness.get("missing_app_id_count", 0) / total_stories
                )
                bucket["missing_story_type_rates"].append(
                    100 * completeness.get("missing_story_type_count", 0) / total_stories
                )
            for wi_id in completeness.get("missing_app_id_wi_ids") or []:
                if wi_id:
                    fragile_missing_app_id[str(wi_id)] += 1
            for wi_id in completeness.get("missing_story_type_wi_ids") or []:
                if wi_id:
                    fragile_missing_story_type[str(wi_id)] += 1
        else:
            bucket["failed_count"] += 1
            month_bucket["failed_count"] += 1
            error = rec.get("error") or "Unknown error"
            reason = error.split(":", 1)[0].strip()
            failure_reasons[reason] += 1

    def _avg(values: List[float]) -> Optional[float]:
        return round(sum(values) / len(values), 1) if values else None

    per_stream_out = {}
    for stream, bucket in per_stream.items():
        per_stream_out[stream] = {
            "job_count":                  bucket["job_count"],
            "complete_count":             bucket["complete_count"],
            "failed_count":               bucket["failed_count"],
            "releases_covered":           sorted(bucket["releases"]),
            "avg_genie_fail_rate_pct":    _avg(bucket["genie_fail_rates"]),
            "avg_missing_app_id_rate_pct":     _avg(bucket["missing_app_id_rates"]),
            "avg_missing_story_type_rate_pct": _avg(bucket["missing_story_type_rates"]),
            "sonar_non_standard_gate_occurrences": bucket["sonar_non_standard_count"],
            "top_recurring_genie_failures": [
                {"name": name, "occurrences": count}
                for name, count in genie_failure_names_by_stream[stream].most_common(top_n)
            ],
        }

    return {
        "meta": {
            "generated_at":  datetime.now(timezone.utc).isoformat(),
            "total_records": total_jobs,
        },
        "summary": {
            "total_jobs":        total_jobs,
            "complete_jobs":     len(complete),
            "failed_jobs":       len(failed),
            "releases_covered":  len(releases),
            "streams_covered":   sorted(per_stream.keys()),
        },
        "per_stream": per_stream_out,
        "trends_by_month": dict(sorted(trends_by_month.items())),
        "recurring_genie_failures_top": [
            {"name": name, "occurrences": count}
            for name, count in genie_failure_names.most_common(top_n)
        ],
        "fragile_stories": {
            "missing_app_id_top": [
                {"wi_id": wi_id, "occurrences": count}
                for wi_id, count in fragile_missing_app_id.most_common(top_n)
            ],
            "missing_story_type_top": [
                {"wi_id": wi_id, "occurrences": count}
                for wi_id, count in fragile_missing_story_type.most_common(top_n)
            ],
        },
        "sonar_non_standard_pipelines_top": [
            {"pipeline": pipeline, "occurrences": count}
            for pipeline, count in sonar_non_standard_pipelines.most_common(top_n)
        ],
        "job_failure_reasons_top": [
            {"reason": reason, "occurrences": count}
            for reason, count in failure_reasons.most_common(top_n)
        ],
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Aggregate the dtp-tda-service job registry into a portfolio/trend summary (admin-only).",
    )
    parser.add_argument("--registry", default=None, help="Path to tda_job_registry.jsonl (defaults to TDA_REGISTRY_PATH / TDA_OUTPUT_DIR).")
    parser.add_argument("--stream", nargs="*", default=None, help="Filter to one or more streams (e.g. RATES FXO). Omit for all streams.")
    parser.add_argument("--since", default=None, help="Only include jobs completed on/after this UTC date (YYYY-MM-DD).")
    parser.add_argument("--until", default=None, help="Only include jobs completed on/before this UTC date (YYYY-MM-DD).")
    parser.add_argument("--top-n", type=int, default=10, help="Number of entries to keep in each 'top recurring' list (default 10).")
    parser.add_argument("--output", default=None, help="Write the aggregate JSON to this path (default: print to stdout).")
    args = parser.parse_args()

    try:
        since = _date_boundary(args.since)
        until = _date_boundary(args.until, end=True)
    except ValueError:
        parser.error("--since and --until require valid dates in YYYY-MM-DD format.")
    if since and until and since > until:
        parser.error("--since must be on or before --until.")

    for ancestor in Path(__file__).resolve().parents:
        if (ancestor / "release_clinic_env.py").is_file():
            sys.path.insert(0, str(ancestor))
            break
    from release_clinic_env import load_environment
    load_environment()

    registry_path = args.registry or default_registry_path()

    records = load_records(registry_path)
    filtered = filter_records(records, args.stream, since, until)

    result = aggregate(filtered, top_n=args.top_n)
    result["meta"]["registry_path"] = registry_path
    result["meta"]["filters"] = {
        "stream": args.stream,
        "since": args.since,
        "until": args.until,
    }
    result["meta"]["total_records_before_filter"] = len(records)

    output_json = json.dumps(result, indent=2, default=str)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_json)
        print(f"Portfolio summary written to {args.output}")
    else:
        print(output_json)


if __name__ == "__main__":
    main()
