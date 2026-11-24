"""Reconcile the targeted screenshot corrections against retained execution bytes."""
import hashlib
import json
from pathlib import Path
import subprocess
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent / "audit-run-20261022"
BASE = "9e489fef435bd0a79055c7827b7882e48cd234d8"


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ref(path):
    return {"path": str(path.relative_to(ROOT)), "sha256": sha(path)}


def frames(run, case):
    path = next((AUDIT / "application" / run / "cases").glob(f"{case.lower()}*/frames.json"))
    return path, read(path)["frames"]


def step(items, number):
    return next(item for item in items if item["phase"] == f"step-{number:02}")


attempts = []
for run in ("run-082", "run-083", "run-084", "run-085"):
    directory = AUDIT / "application" / run
    inputs = read(directory / "run-inputs.json")
    integrity = read(directory / "source-integrity.json")
    assert integrity["status"] == "SOURCE_UNCHANGED_DURING_RUN"
    for source in inputs["sourceHashes"]:
        assert sha(Path(source["snapshotPath"])) == source["sha256"]
    for path in sorted((directory / "cases").glob("*/result.json")):
        result = read(path)
        capture = read(path.with_name("frames.json"))
        assert result["actualStatus"] == "passed" and result["assertionsSatisfied"]
        assert result["scope"] == "ACTUAL_APPLICATION_LOCAL_SERVICES"
        assert capture["completeStepEvidence"] and not capture["captureGaps"]
        for frame in capture["frames"]:
            assert sha(Path(frame["path"])) == frame["sha256"]
        attempts.append({"run": run, "caseId": capture["canonical"]["caseId"],
                         "result": ref(path), "frames": ref(path.with_name("frames.json")),
                         "status": "PASS", "frameCount": len(capture["frames"]),
                         "sourceIntegrity": ref(directory / "source-integrity.json")})
assert len(attempts) == 19 and len({item["caseId"] for item in attempts}) == 14

path084, auth084 = frames("run-084", "AUTH-084")
home = next(item for item in auth084 if item["phase"] == "session-home-before-expiry")
boundary = step(auth084, 5)
for group in ("observationsBefore", "observationsAfter"):
    session = boundary[group]["session"]
    assert session["clock"]["elapsedMs"] == 597999
    assert session["clock"]["cutoffRemainingMs"] == 1
    assert session["ui"]["dialogVisible"] and session["ui"]["extendVisible"] and session["ui"]["extendEnabled"]
    assert not session["state"]["isOnLogout"]
assert not home["observationsAfter"]["session"]["ui"]["dialogVisible"]
assert home["sha256"] != step(auth084, 1)["sha256"]
assert boundary["sha256"] == step(auth084, 6)["sha256"] == step(auth084, 7)["sha256"]

path116, auth116 = frames("run-082", "AUTH-116")
assert all(step(auth116, number)["targetPageLabel"] == "CTX-B" for number in (8, 9, 10))
assert step(auth116, 7)["targetPageLabel"] == "CTX-A"
assert not step(auth116, 7)["observationsAfter"]["session"]["state"]["accessPresent"]
assert step(auth116, 10)["observationsAfter"]["session"]["state"]["accessPresent"]
assert step(auth116, 7)["sha256"] != step(auth116, 10)["sha256"]

path115, auth115 = frames("run-082", "AUTH-115")
assert all(step(auth115, number)["targetPageLabel"] == "TAB-B" for number in (3, *range(6, 14)))
assert step(auth115, 5)["observationsAfter"]["sharedSession"]["loginVisible"]
assert not step(auth115, 6)["observationsAfter"]["sharedSession"]["loginVisible"]
assert step(auth115, 7)["observationsAfter"]["sharedSession"]["loginVisible"]

path017, ux017 = frames("run-085", "UX-017")
assert step(ux017, 1)["observationsAfter"]["browser"]["focus"]["rowId"] == "101"
assert step(ux017, 2)["observationsAfter"]["browser"]["focus"]["rowId"] == "102"
assert step(ux017, 2)["observationsAfter"]["browser"]["focus"]["field"] == "label"
assert step(ux017, 1)["sha256"] == step(ux017, 2)["sha256"]

historical = []
for name in ("report-001", "report-002"):
    directory = AUDIT / name
    subprocess.run(["git", "diff", "--exit-code", BASE, "--", str(directory.relative_to(ROOT))],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    historical.append({"report": name, "trackedBytesUnchangedFrom": BASE,
                       "manifest": ref(directory / "report-manifest.json")})
assert historical[1]["manifest"]["sha256"] == "57c671a3b2fe514206e4a67e6bbe23dc5581d166317aa69f32f11c80d5172b69"

validation = read(HERE / "report-006-validation.json")
gallery = read(HERE / "gallery-ui-check.json")
shutdown = read(HERE / "environment/shutdown-health-04.json")
assert validation["status"] == gallery["status"] == shutdown["status"] == "PASSED"
assert not any(item["listenerPresentAfterShutdown"] for item in shutdown["ports"])

visual_samples = []
for run, case, phase, finding in (
    ("run-082", "AUTH-084", "session-home-before-expiry", "Partially rendered preparatory Home; superseded by run-084."),
    ("run-082", "AUTH-084", "step-05", "Expired-session dialog shows Extend at the controlled boundary."),
    ("run-082", "AUTH-116", "step-07", "CTX-A shows login after logout."),
    ("run-082", "AUTH-116", "step-10", "CTX-B retains authenticated Home and WS-A."),
    ("run-084", "AUTH-084", "session-home-before-expiry", "Fully rendered Home precedes the expired-session dialog."),
):
    _, items = frames(run, case)
    frame = next(item for item in items if item["phase"] == phase)
    visual_samples.append({"caseId": case, "image": ref(Path(frame["path"])), "reviewer": "Codex",
                           "method": "Direct image inspection", "finding": finding})

output = {"status": "PASSED", "checkedAt": datetime.now(timezone.utc).isoformat(),
          "script": ref(Path(__file__).resolve()), "attemptCount": len(attempts), "uniqueCaseCount": 14,
          "attempts": attempts, "auth084": {"frames": ref(path084), "homeSequence": home["sequence"],
              "boundarySequence": boundary["sequence"], "elapsedMs": 597999, "cutoffRemainingMs": 1,
              "extendEnabledBeforeAndAfterCapture": True, "unchangedAssertions": [5, 6, 7]},
          "auth115": {"frames": ref(path115), "targetTabBSteps": [3, *range(6, 14)]},
          "auth116": {"frames": ref(path116), "targetContextBSteps": [8, 9, 10]},
          "ux017": {"frames": ref(path017), "focusRows": ["101", "102"], "field": "label", "identicalImage": True},
          "historicalReports": historical, "reportValidation": ref(HERE / "report-006-validation.json"),
          "galleryCheck": ref(HERE / "gallery-ui-check.json"), "directVisualSamples": visual_samples,
          "galleryVisualSamples": gallery["evidence"], "shutdown": ref(HERE / "environment/shutdown-health-04.json"),
          "limits": ["The baseline inventory checks all 4555 latest report-002 bindings; nine original frames received direct visual inspection.",
                     "This correction review inspects five raw frames and two gallery presentations. It does not visually review every frame.",
                     "Machine observations remain separate from unmodified application screenshots.",
                     "Retained source snapshots identify execution variants; earlier runs need not match the final harness bytes."]}
(HERE / "correction-verification.json").write_text(json.dumps(output, indent=2) + "\n")
print(json.dumps({"status": output["status"], "attemptCount": len(attempts), "uniqueCaseCount": 14}))
