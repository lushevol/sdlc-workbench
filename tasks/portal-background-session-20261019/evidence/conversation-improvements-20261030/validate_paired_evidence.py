"""Audit saved paired results, exact source bindings, and unchanged canonical inputs."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
REPO = ROOT / "repos/services/single-ui-bff"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    execution = json.loads((OUT / "paired-execution.json").read_text())
    comparison = json.loads((OUT / "paired-comparison.json").read_text())
    checks = []

    def check(name, condition):
        checks.append({"name": name, "status": "PASSED" if condition else "FAILED"})

    check("four completed case instances", len(execution["cases"]) == 4)
    check("application failures remain failed", execution["counts"] == {"PASSED": 2, "FAILED": 2, "ERROR": 0})
    check("comparison binds execution", comparison["execution_sha256"] == digest(OUT / "paired-execution.json"))
    check("shared runner identity", execution["runner_sha256"] == digest(OUT / "run_paired_security_probe.py"))
    check("shared probe identity", execution["probe_sha256"] == digest(OUT / "SecurityLogoutProbe.java"))
    check("user input identity", execution["user_input_sha256"] == digest(OUT / "user-input.md"))
    check("frozen canonical bytes unchanged", execution["canonical_before"] == execution["canonical_after"]
          == {name: digest(OUT.parents[1] / name) for name in execution["canonical_before"]})
    source_count = 0
    for label, build in execution["builds"].items():
        check(label + " compilation passed", build["compile_exit"] == 0)
        check(label + " compile log identity", build["compile_log_sha256"] == digest(OUT / build["compile_log"]))
        for item in build["source_inputs"]:
            if item["path"].startswith("src/"):
                data = subprocess.check_output(["git", "-C", str(REPO), "show", build["revision"] + ":" + item["path"]])
                check(label + " source " + item["path"], hashlib.sha256(data).hexdigest() == item["sha256"])
                source_count += 1
            else:
                check(label + " probe source", digest(Path(item["path"])) == item["sha256"])
        classes = Path(execution["scratch"]) / (label + "-classes")
        check(label + " compiled class identities", all(digest(classes / item["path"]) == item["sha256"]
                                                       for item in build["compiled_classes"]))
    check("offline dependency identities", all(digest(Path(item["path"])) == item["sha256"]
                                                for item in execution["dependencies"]))
    for case in execution["cases"]:
        prefix = case["revision_label"] + " " + case["case_id"]
        check(prefix + " saved result identity", digest(OUT / case["result"]) == case["result_sha256"])
        check(prefix + " output identity", digest(OUT / case["output"]) == case["output_sha256"])
        passed = all(case["assertions"].values())
        check(prefix + " status follows assertions", (case["status"] == "PASSED") == passed)
        if case["case_id"] == "RN-S002":
            check(prefix + " meaningful failure retained", case["status"] == "FAILED"
                  and case["relogin_status"] == 200 and case["new_access_issued"]
                  and case["blacklist_entries"] == 0 and case["execution_exit"] == 2)
    check("paired observables match", all(row["same_observables"] for row in comparison["comparisons"]))
    check("business checkout unchanged", subprocess.check_output(["git", "-C", str(REPO), "status", "--porcelain"], text=True) == "")
    dispositions = json.loads((OUT / "contract-dispositions.json").read_text())
    check("retained contract evidence identities", all(digest(OUT.parent / row["path"]) == row["sha256"]
                                                       for row in dispositions["source_evidence"]))
    broken = []
    for name in ("01-paired-verification-stage.md", "02-paired-verification-report.md"):
        document = OUT / name
        content = document.read_text()
        check(name + " ASD review remains pending", "asd_review: PENDING" in content)
        check(name + " contains critical conclusion", "**" in content.split("\n## ", 1)[0])
        for locator in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
            target = locator.split("#", 1)[0]
            if target and target != "validation.json" and not (document.parent / target).exists():
                broken.append({"document": name, "locator": locator})
    check("new report links resolve", not broken)
    result = {
        "recorded_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "status": "PASSED" if all(row["status"] == "PASSED" for row in checks) else "FAILED",
        "scope": "Automated evidence integrity, result reconciliation, source identity, and local document links",
        "application_assertions": {"PASSED": 2, "FAILED": 2, "ERROR": 0},
        "source_inputs_compared_to_git": source_count,
        "checks": checks,
        "broken_links": broken,
        "writing_review": {"standard": "ASD-STE100", "automated_check": "PASSED" if not broken else "FAILED",
                           "asd_review": "PENDING", "reviewer": None, "reviewed_at": None,
                           "limitations": ["Automated checks do not check the complete approved dictionary or grammar rules."]},
    }
    (OUT / "validation.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "checks": len(checks), "source_inputs_compared_to_git": source_count,
                      "failed_checks": [row["name"] for row in checks if row["status"] != "PASSED"]}, indent=2))
    return int(result["status"] != "PASSED")


if __name__ == "__main__":
    raise SystemExit(main())
