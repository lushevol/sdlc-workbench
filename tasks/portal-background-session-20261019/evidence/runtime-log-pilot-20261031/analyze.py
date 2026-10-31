"""Assess declared local observations without treating event names as behavior proof."""
from pathlib import Path
import collections
import datetime
import hashlib
import json

OUT = Path(__file__).resolve().parent
read = lambda path: json.loads(path.read_text())
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
RUN = OUT / read(OUT / "latest-run.json")["path"]
PLAN = read(OUT / "observation-plan.json")
BINDING = read(OUT / "local-source-binding.json")
CASES = {}
for path in RUN.glob("*/result.json"):
    result = read(path)
    events = [json.loads(line) for line in (path.parent / "application-events.ndjson").read_text().splitlines() if line]
    CASES[path.parent.name] = (result, events, path)


def complete(result, events):
    capture = result["collection"]
    return (capture["parse_errors"] == 0 and capture["emitted"] == len(events)
            and [event["seq"] for event in events] == list(range(1, len(events) + 1)))


def assess(row, override=None):
    key = row["label"] + "-" + row["case"].lower()
    result, original, path = CASES[key]
    events = original if override is None else override
    start = next(event["seq"] for event in events if event["event"] == "timeout.extend.accepted")
    relevant = [event for event in events if event["seq"] >= start]
    matched = {}
    for name in row["required_events"]:
        selected = [event for event in relevant if event["event"] == name]
        if name == "auth.response.received":
            selected = [event for event in selected if event["fields"].get("path") == "/api/auth/v2/sso/relogin"]
        if name == "auth.response.error":
            selected = [event for event in selected if event["fields"].get("path") == "/api/auth/v2/sso/relogin"
                        and event["fields"].get("status") == 503]
        if name == "auth.response.discarded":
            # A discarded logout response cannot establish discarded renewal access.
            selected = [event for event in selected if event["fields"].get("path") == "/api/auth/v2/sso/relogin"]
        if name == "session.state_transition":
            action = "CLEAR" if row["id"] == "OBS-05" else "SET_TOKEN"
            selected = [event for event in selected if event["fields"].get("action") == action]
        matched[name] = [event["seq"] for event in selected]
    missing = [name for name, sequences in matched.items() if not sequences]
    acquisition = complete(result, events) and not missing
    binding = acquisition and all(event["revision"] == result["revision"]
                                 and event["run"] == row["label"] + "-" + row["case"] for event in events)
    binding = binding and result["revision"] == BINDING["source"][row["label"]]["revision"]
    binding = binding and any(script.get("instrumentation_marker_present") for script in result.get("served_scripts", []))
    passed = all(assertion["status"] == "PASSED" for assertion in result["assertions"])
    if row["id"] == "OBS-03":
        passed = passed and len(matched["timeout.renewal.failed"]) == 6
    if row["id"] == "OBS-04":
        passed = passed and len(matched["timeout.renewal.success"]) == 6 and len(result["cycles"]) == 6
    if row["id"] == "OBS-06":
        passed = None
    return {"id": row["id"], "case": row["case"], "mode": row["mode"],
            "essential_path": row["essential_path"], "intent_status": row["intent_status"],
            "experiment_definition_supported": True, "acquired": acquisition, "bound": binding,
            "analyzed": True, "evidence_assessed": acquisition and binding,
            "passing_behavior": passed if acquisition and binding else None,
            "matched_event_sequences": matched, "missing_or_unbound_events": missing,
            "result_ref": str(path.relative_to(OUT)), "result_sha256": sha(path),
            "log_ref": str((path.parent / "application-events.ndjson").relative_to(OUT)),
            "log_sha256": sha(path.parent / "application-events.ndjson"),
            "limit": "Experiment definitions do not establish reviewed product AC conformance."
            if row["id"] != "OBS-06" else
            "Relogin was canceled. The retained discarded response concerns logout; stale renewal delivery remains unexercised. "
            "The discard event omits path correlation required by this analyzer; instrumentation must identify the request before a future run can qualify this row."}


rows = [assess(row) for row in PLAN["required_observation_rows"]]
summary = read(RUN / "browser-summary.json")
console_counts = collections.Counter()
for result, events, path in CASES.values():
    if result["label"] != "candidate":
        continue
    for signal in result.get("console_signals", []):
        message = signal["message"]
        category = ("controlled_503" if "503" in message else "http_404" if "404" in message else
                    "react_or_css_development_warning" if any(term in message for term in ["Warning:", "css properties", "pseudo class"]) else "unclassified")
        console_counts[category] += 1

timelines = {}
for label in ["candidate", "baseline"]:
    result, events, path = CASES[label + "-rn-x002"]
    received = next(event["seq"] for event in events if event["event"] == "auth.response.received"
                    and event["fields"].get("path") == "/api/auth/v2/sso/relogin")
    close = next(event["seq"] for event in events if event["event"] == "timeout.prompt.close_requested")
    installed = next(event["seq"] for event in events if event["seq"] > received
                     and event["event"] == "session.state_transition" and event["fields"].get("action") == "SET_TOKEN")
    timelines[label] = {"renewal_response_sequence": received, "close_requested_sequence": close,
                        "installed_reducer_sequence": installed, "close_requested_before_response": close < received,
                        "failed_assertions": [assertion for assertion in result["assertions"] if assertion["status"] == "FAILED"]}

candidate_results = [result for result, events, path in CASES.values() if result["label"] == "candidate"]
report = {"schema_version": 1, "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "source_kind": "local_development", "run": str(RUN.relative_to(OUT)),
          "uat": {"status": "NOT_RUN", "source_kind": None, "required_observations": None,
                  "metric": "N/A", "limit": "No remote UAT inventory, source queries, deployment bindings, or logs were collected."},
          "local_metrics": {"required_observations": len(rows),
                            **{name: sum(row[name] is True for row in rows) for name in
                               ["experiment_definition_supported", "acquired", "bound", "analyzed", "evidence_assessed", "passing_behavior"]}},
          "candidate_cases": {"passed": sum(result["status"] == "PASSED" for result in candidate_results),
                              "failed": sum(result["status"] == "FAILED" for result in candidate_results),
                              "assertions_passed": sum(assertion["status"] == "PASSED" for result in candidate_results for assertion in result["assertions"]),
                              "events": sum(len(events) for result, events, path in CASES.values() if result["label"] == "candidate")},
          "baseline_comparison": timelines, "observations": rows, "console_signal_categories": dict(console_counts),
          "limits": PLAN["scope_limits"] + ["Console 404s lack endpoint correlation in this capture; their originating operation remains unknown.",
                    "React development warnings occur with the toolkit substitute; target occurrence and user impact remain unverified.",
                    "A close request precedes reducer commit after response validation. It does not establish early visible closure."],
          "analysis_script_sha256": sha(Path(__file__))}
(OUT / "analysis.json").write_text(json.dumps(report, indent=2) + "\n")

# Consequential negative control: a dropped event must invalidate collection completeness.
result, events, _ = CASES["candidate-rn-x002"]
dropped = next(event for event in events if event["event"] == "renewal.service.start")
altered = [event for event in events if event is not dropped]
control_rows = [assess(row, altered) if row["case"] == "RN-X002" else assess(row)
                for row in PLAN["required_observation_rows"]]
control = {"kind": "synthetic_collector_negative_control", "source_run": str(RUN.relative_to(OUT)),
           "removed_event_sequence": dropped["seq"], "original_assessed": report["local_metrics"]["evidence_assessed"],
           "altered_assessed": sum(row["evidence_assessed"] for row in control_rows),
           "collection_completeness_rejected": not complete(result, altered)}
assert control["collection_completeness_rejected"] and control["altered_assessed"] < control["original_assessed"]
(OUT / "collector-negative-control.json").write_text(json.dumps(control, indent=2) + "\n")
print(json.dumps({"local_metrics": report["local_metrics"], "candidate": report["candidate_cases"],
                  "baseline_timeline": timelines, "console_categories": dict(console_counts), "negative_control": control}, indent=2))
