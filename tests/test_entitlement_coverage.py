"""Exercise the complete coverage runner with controlled local HTTP services."""

from __future__ import annotations

from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib.parse import unquote
import xml.etree.ElementTree as ET
from zipfile import ZipFile

from ai_sdlc_workbench import entitlement_coverage as coverage


XML = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PACKAGE_REL = "http://schemas.openxmlformats.org/package/2006/relationships"


def _matrix(path, users="u1,u2", *, role="Reader", feature="Ledger"):
    """Write a minimal XLSX conversion fixture without another authoring tool."""
    sheets = {
        "Application": [["ITAM_ID", "ITAM_NAME", "APPNAME"], ["1", "Controlled fixture", "NEW_APP"]],
        "Feature": [["FEATURENAME", "APPLICATIONNAME"], [feature, "NEW_APP"]],
        "Entitlement": [["ENTITLEMENTNAME", "DESCRIPTION", "OWNER", "APPLICATIONNAME"],
                        [role, "", "", "NEW_APP"]],
        "EntitlementFeatureAction": [["ENTITLEMENTNAME", "APPLICATIONNAME", "FEATURENAME", "ACTIONNAME"],
                                    [role, "NEW_APP", feature, "View"]],
        "UserEntitlement": [["USERNAME", "ENTITLEMENTNAME", "A", "B", "APPNAME"],
                            ["", "", "", "", ""], [users, role, "", "", "NEW_APP"]],
    }
    workbook = ET.Element(f"{{{XML}}}workbook")
    listing = ET.SubElement(workbook, f"{{{XML}}}sheets")
    relations = ET.Element(f"{{{PACKAGE_REL}}}Relationships")
    with ZipFile(path, "w") as archive:
        for number, (name, rows) in enumerate(sheets.items(), 1):
            ET.SubElement(listing, f"{{{XML}}}sheet", {"name": name, "sheetId": str(number),
                                                     f"{{{REL}}}id": f"rId{number}"})
            ET.SubElement(relations, f"{{{PACKAGE_REL}}}Relationship", {
                "Id": f"rId{number}", "Target": f"worksheets/sheet{number}.xml",
                "Type": REL + "/worksheet"})
            worksheet = ET.Element(f"{{{XML}}}worksheet")
            data = ET.SubElement(worksheet, f"{{{XML}}}sheetData")
            for index, values in enumerate(rows, 1):
                row = ET.SubElement(data, f"{{{XML}}}row", {"r": str(index)})
                for column, value in enumerate(values):
                    cell = ET.SubElement(row, f"{{{XML}}}c", {"r": f"{chr(65 + column)}{index}",
                                                           "t": "inlineStr"})
                    inline = ET.SubElement(cell, f"{{{XML}}}is")
                    ET.SubElement(inline, f"{{{XML}}}t").text = value
            archive.writestr(f"xl/worksheets/sheet{number}.xml", ET.tostring(worksheet))
        archive.writestr("xl/workbook.xml", ET.tostring(workbook))
        archive.writestr("xl/_rels/workbook.xml.rels", ET.tostring(relations))
        archive.writestr("[Content_Types].xml", '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>')


def _ems_grant(role="Reader", feature="Ledger", action="View"):
    return {key: {"name": value, "entity": {"name": "OLD_APP"}}
            for key, value in (("role", role), ("subject", feature), ("action", action))}


def _ces_user(user, *, role="Reader", feature="Ledger", action="View"):
    return [{"user_data": {"user_id": user, "app_name": "NEW_APP"}, "entitlements": {
        "entitlement_name": [role], "role_entitlements": [{"feature": feature, "action": action}],
        "data_entitlements": [{"key": "Region", "values": ["A1"]}]}}]


class _ControlledHandler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send(self, status, body):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        state = self.server.state
        state["calls"].append(("GET", self.path, None))
        if self.path in state["errors"]:
            self._send(state["errors"][self.path], {"error": "controlled upstream failure"})
        elif self.path == "/ces/app/NEW_APP":
            self._send(200, state["catalog"])
        elif self.path.startswith("/ces/app/NEW_APP/user/"):
            user = unquote(self.path.rsplit("/", 1)[1])
            self._send(200, state["ces_users"].get(user, []))
        elif self.path == "/ems2/entity/E1/subjects":
            self._send(200, state["subjects"])
        elif self.path == "/ems2/entity/E1/roles":
            self._send(200, state["roles"])
        else:
            self._send(404, {"error": "not in controlled fixture scope"})

    def do_POST(self):
        data = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        state = self.server.state
        state["calls"].append(("POST", self.path, data))
        user = next(iter(data))
        if self.path in state["errors"]:
            self._send(state["errors"][self.path], {"error": "controlled upstream failure"})
        elif self.path == "/ems2/entitlements":
            grants = state["ems_users"].get(user, [])
            self._send(201, {user: {"count": len(grants), "entitlements": grants}})
        else:
            self._send(404, {"error": "not in controlled fixture scope"})


class CoverageRunnerTests(unittest.TestCase):
    """All services and accounts here are controlled fixtures, not live systems."""

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="coverage-runner-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.environment = patch.dict("os.environ", {"HTTP_PROXY": "", "HTTPS_PROXY": "", "http_proxy": "",
                                                       "https_proxy": "", "NO_PROXY": "127.0.0.1", "no_proxy": "127.0.0.1"})
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.state = {
            "calls": [], "errors": {},
            "catalog": [{"entitlement_name": "Reader", "role_entitlements": [{"feature": "Ledger", "action": "View"}],
                         "user_ids": ["u1", "u2;u3", "u3"]}],
            "ems_users": {user: [_ems_grant()] for user in ("u1", "u2", "u3")},
            "ces_users": {user: _ces_user(user) for user in ("u1", "u2", "u3")},
            "subjects": {"count": 1, "subjects": [{"name": "Ledger"}]},
            "roles": {"count": 1, "roles": [{"name": "Reader"}]},
        }
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), _ControlledHandler)
        self.server.state = self.state
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self._stop_server)
        base = f"http://127.0.0.1:{self.server.server_port}"
        self.base_url = base
        _matrix(self.root / "matrix.xlsx")
        self.config = {
            "schema_version": 1, "scope": "Controlled local HTTP coverage fixture; no enterprise access",
            "workspace_root": ".", "output_dir": "runs", "allow_local_http": True,
            "workers": 1, "timeout_seconds": 2, "retries": 0,
            "entities": [{"name": "OLD_APP", "id": "E1", "app": "NEW_APP", "workbook": "matrix.xlsx"},
                         {"name": "FMO PORTAL ADMIN", "id": "FMO", "app": "FMO_PORTAL_ADMIN", "included": False,
                          "priority": "LOW", "reason": "Non-production, unlaunched exception", "workbook": "excluded-not-present.xlsx"}],
            "ems2": {"base_url": base + "/ems2", "entitlements_path": "/entitlements",
                     "subjects_path": "/entity/{entity_id}/subjects", "roles_path": "/entity/{entity_id}/roles"},
            "ces": {"base_url": base + "/ces", "catalog_path": "/app/{app}", "user_path": "/app/{app}/user/{user}"},
            "replay": {"examples": ["examples/*.yml"]},
        }
        self.config_path = self.root / "config.json"
        self._write_config()

    def _stop_server(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def _write_config(self):
        self.config_path.write_text(json.dumps(self.config), encoding="utf-8")

    def _run(self, **kwargs):
        kwargs.setdefault("mode", "live")
        with redirect_stdout(io.StringIO()):
            return coverage.run(self.config_path, **kwargs)

    def _write_examples(self):
        folder = self.root / "examples"
        folder.mkdir(exist_ok=True)
        fixtures = [("catalog", "GET", self.base_url + "/ces/app/NEW_APP", None, 200, self.state["catalog"]),
                    ("subjects", "GET", self.base_url + "/ems2/entity/E1/subjects", None, 200, self.state["subjects"]),
                    ("roles", "GET", self.base_url + "/ems2/entity/E1/roles", None, 200, self.state["roles"])]
        for user, grants in self.state["ems_users"].items():
            fixtures.append(("ems-" + user, "POST", self.base_url + "/ems2/entitlements", {user: ["OLD_APP"]},
                             201, {user: {"count": len(grants), "entitlements": grants}}))
        for user, response in self.state["ces_users"].items():
            fixtures.append(("ces-" + user, "GET", self.base_url + "/ces/app/NEW_APP/user/" + user, None, 200, response))
        for name, method, url, body, status, response in fixtures:
            request = {"method": method, "url": url}
            if body is not None:
                request["body"] = {"type": "json", "data": json.dumps(body)}
            collection = {"http": request, "examples": [{"request": {"method": method, "url": url},
                          "response": {"status": status, "body": {"type": "json", "data": json.dumps(response)}}}]}
            (folder / (name + ".yml")).write_text(json.dumps(collection), encoding="utf-8")
        return folder

    def test_complete_runner_fetches_union_and_filters_matches_but_keeps_counts(self):
        """Given multiple matrix-cell users and different CES catalog users
        When the complete runner fetches controlled local services
        Then every union account is compared and matches leave only the difference view
        """
        result, directory = self._run()
        self.assertEqual(result["inventory"]["users"], ["u1", "u2", "u3"])
        fetched = {next(iter(body)) for method, _, body in self.state["calls"] if method == "POST"}
        self.assertEqual(fetched, {"u1", "u2", "u3"})
        self.assertTrue(all(body[next(iter(body))] == ["OLD_APP"] for method, _, body in self.state["calls"] if method == "POST"))
        self.assertEqual(result["status"], "FUNCTIONAL_MATCH")
        self.assertEqual(result["summary"]["matching_accounts"], 3)
        self.assertEqual(result["summary"]["functional_profile_coverage_percent"], 100)
        self.assertEqual(result["entitlements"]["profile_grants"]["matched_count"], 1)
        self.assertEqual(result["entitlements"]["profile_grants"]["differences"], {"missing": [], "additional": []})
        self.assertTrue(all(x["comparison"]["status"] == "PASS" for x in result["entitlements"]["live_inventories"]))
        self.assertEqual(len((directory / "cases.jsonl").read_text().splitlines()), 3)
        table = (directory / "report.html").read_text().split("<tbody>", 1)[1].split("</tbody>", 1)[0]
        self.assertNotIn("<td>u1</td>", table)
        self.assertNotIn("<td>u2</td>", table)
        self.assertIn("<td>u3</td>", table)
        self.assertIn("matrix_assignment_comparison", table)
        csv_output = (directory / "differences.csv").read_text()
        self.assertEqual(len(csv_output.splitlines()), 2)
        self.assertIn("source_consistency,u3,matrix_assignment_comparison,additional", csv_output)
        self.assertEqual(result["excluded"][0]["name"], "FMO PORTAL ADMIN")
        self.assertFalse(any("FMO" in path for _, path, _ in self.state["calls"]))
        self.assertTrue(all(x["exact_full_profile_status"] == "UNASSESSED" for x in result["users"]))

    def test_changed_role_cannot_hide_behind_equal_effective_permissions(self):
        """Given an extra CES role that retains the same effective feature and action
        When one user's effective role name changes
        Then the user's profile comparison differs despite equal effective grants
        """
        self.state["catalog"].append({"entitlement_name": "Changed Reader", "role_entitlements": [
            {"feature": "Ledger", "action": "View"}], "user_ids": ["u1"]})
        self.state["ces_users"]["u1"] = _ces_user("u1", role="Changed Reader")
        result, _ = self._run()
        account = next(x for x in result["users"] if x["user_id"] == "u1")
        self.assertEqual(account["effective"]["status"], "PASS")
        self.assertEqual(account["status"], "DIFFERENT")
        self.assertEqual(account["profile_grants"]["missing_count"], 1)
        self.assertEqual(account["profile_grants"]["additional_count"], 1)
        self.assertEqual(result["status"], "DIFFERENCES")

    def test_http_failure_stays_unassessed_in_the_complete_denominator(self):
        """Given one controlled upstream failure
        When the user population is compared
        Then the failed account stays unassessed and never becomes an empty pass
        """
        self.state["errors"]["/ces/app/NEW_APP/user/u2"] = 503
        result, directory = self._run()
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(result["summary"]["discovered_accounts"], 3)
        self.assertEqual(result["summary"]["matching_accounts"], 2)
        self.assertEqual(result["summary"]["unassessed_accounts"], 1)
        self.assertIsNone(result["summary"]["functional_profile_coverage_percent"])
        self.assertEqual(result["summary"]["verified_functional_match_lower_bound_percent"], 66.67)
        failed = next(x for x in result["users"] if x["user_id"] == "u2")
        self.assertEqual(failed["errors"][0]["http_status"], 503)
        self.assertIn("unassessed", (directory / "differences.csv").read_text())

    def test_unavailable_live_inventory_prevents_complete_functional_match(self):
        """Given matched user responses but unavailable baseline subject acquisition
        When the run finishes
        Then the complete entitlement coverage result remains incomplete
        """
        self.state["errors"]["/ems2/entity/E1/subjects"] = 503
        result, _ = self._run()
        self.assertEqual(result["summary"]["matching_accounts"], 3)
        self.assertEqual(result["status"], "INCOMPLETE")

    def test_additional_live_subject_prevents_a_matrix_only_success(self):
        """Given a live EMS2 subject absent from the conversion matrix
        When the run checks the complete declared inventory
        Then the missing baseline definition remains a reported gap
        """
        self.state["subjects"] = {"count": 2, "subjects": [{"name": "Ledger"}, {"name": "Unmigrated"}]}
        result, _ = self._run()
        self.assertNotEqual(result["status"], "FUNCTIONAL_MATCH")
        subject_check = next(x for x in result["entitlements"]["live_inventories"] if x["kind"] == "subjects")
        self.assertEqual(subject_check["comparison"]["missing"], [["Unmigrated"]])

    def test_explicit_absent_ces_user_is_a_missing_permission_difference(self):
        """Given a baseline account and an explicit successful empty CES response
        When its profile is compared
        Then missing permissions are differences rather than acquisition errors
        """
        self.state["ces_users"]["u2"] = []
        result, _ = self._run()
        account = next(x for x in result["users"] if x["user_id"] == "u2")
        self.assertEqual(account["status"], "DIFFERENT")
        self.assertEqual(account["errors"], [])
        self.assertEqual(account["effective"]["missing_count"], 1)

    def test_replay_runs_without_network_and_never_claims_current_live_state(self):
        """Given complete stored collection examples
        When replay runs with HTTP disabled by an assertion
        Then captured comparisons run and remain explicitly replay evidence
        """
        self._write_examples()
        with patch.object(coverage.JsonHttpClient, "request", side_effect=AssertionError("Replay made a network call")):
            result, directory = self._run(mode="replay")
        self.assertEqual(result["mode"], "replay")
        self.assertEqual(result["summary"]["matching_accounts"], 3)
        self.assertEqual(self.state["calls"], [])
        self.assertIn("replay", (directory / "report.html").read_text())
        self.assertTrue(any("never establishes current live state" in limit for limit in result["limits"]))

    def test_default_cli_replays_supplied_responses_without_http_or_credentials(self):
        """Given stored responses and unavailable credentials and HTTP access
        When the CLI runs without selecting a mode
        Then it compares the captures and labels every output as mock evidence
        """
        self._write_examples()
        directory = self.root / "default-cli"
        output = io.StringIO()
        with patch.object(coverage, "load_root_env", side_effect=AssertionError("Mock read credentials")), \
             patch.object(coverage, "JsonHttpClient", side_effect=AssertionError("Mock constructed HTTP client")), \
             redirect_stdout(output):
            status = coverage.main(["--config", str(self.config_path), "--output", str(directory)])
        result = json.loads((directory / "result.json").read_text())
        self.assertEqual(status, 0)
        self.assertEqual(result["mode"], "replay")
        self.assertEqual(result["summary"]["matching_accounts"], 3)
        printed = output.getvalue()
        self.assertEqual(json.loads(printed[printed.index("{"):])["evidence_source"], "MOCK: supplied API responses")
        self.assertIn("MOCK: supplied API responses", (directory / "report.html").read_text())
        self.assertEqual(self.state["calls"], [])

    def test_default_run_keeps_uncaptured_users_unassessed_without_http_fallback(self):
        """Given a complete discovery catalog but no paired capture for one account
        When the default runner compares supplied responses with HTTP unavailable
        Then the missing account remains unassessed and final coverage stays unknown
        """
        folder = self._write_examples()
        (folder / "ces-u2.yml").unlink()
        with patch.object(coverage, "load_root_env", side_effect=AssertionError("Mock read credentials")), \
             patch.object(coverage, "JsonHttpClient", side_effect=AssertionError("Mock constructed HTTP client")), \
             redirect_stdout(io.StringIO()):
            result, directory = coverage.run(self.config_path)
        self.assertEqual(result["mode"], "replay")
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(result["summary"]["compared_accounts"], 2)
        self.assertEqual(result["summary"]["unassessed_accounts"], 1)
        self.assertIsNone(result["summary"]["functional_profile_coverage_percent"])
        missing = next(user for user in result["users"] if user["user_id"] == "u2")
        self.assertEqual(missing["errors"][0]["code"], "REPLAY_NOT_CAPTURED")
        self.assertIn("missing captures", result["conclusion"].lower())
        self.assertIn("u2", (directory / "differences.csv").read_text())
        self.assertEqual(self.state["calls"], [])

    def test_resume_uses_saved_cases_and_rejects_changed_matrix_identity(self):
        """Given one durably completed account and a bounded first run
        When unchanged evidence resumes and changed matrix evidence is retried
        Then the first case is retained and the changed source cannot reuse the run
        """
        first, directory = self._run(user_limit=1)
        self.assertEqual(first["status"], "INCOMPLETE")
        first_line = json.loads((directory / "cases.jsonl").read_text().splitlines()[0])
        digest = first_line.pop("record_sha256")
        self.assertEqual(len(digest), 64)
        result, resumed = self._run(resume=directory)
        self.assertEqual(resumed, directory)
        self.assertEqual(result["status"], "FUNCTIONAL_MATCH")
        retained = next(x for x in result["users"] if x["user_id"] == first_line["user_id"])
        self.assertEqual(retained, first_line)
        self.assertEqual(len((directory / "cases.jsonl").read_text().splitlines()), 3)
        _matrix(self.root / "matrix.xlsx", users="u1,u2,u4")
        with self.assertRaises(ValueError):
            self._run(resume=directory)

    def test_completed_case_is_durable_before_later_interruption(self):
        """Given the next account interrupts an otherwise valid run
        When the first account already completed
        Then its checkpoint survives and resume completes the remaining population
        """
        original = coverage._case
        def interrupt(user, *args, **kwargs):
            if user == "u2":
                raise KeyboardInterrupt("Controlled interruption after one completed case")
            return original(user, *args, **kwargs)
        directory = self.root / "interrupted"
        with patch.object(coverage, "_case", side_effect=interrupt):
            with self.assertRaises(KeyboardInterrupt):
                self._run(output=directory)
        lines = (directory / "cases.jsonl").read_text().splitlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(json.loads(lines[0])["user_id"], "u1")
        result, _ = self._run(resume=directory)
        self.assertEqual(result["status"], "FUNCTIONAL_MATCH")
        self.assertEqual(result["summary"]["matching_accounts"], 3)

    def test_resume_rejects_changed_replay_source_bytes(self):
        """Given saved passing replay cases and a changed source response
        When the same replay run resumes
        Then source identity rejects reusing the old passing cases
        """
        folder = self._write_examples()
        _, directory = self._run(mode="replay")
        source = folder / "ces-u1.yml"
        changed = json.loads(source.read_text())
        changed["examples"][0]["response"]["body"]["data"] = json.dumps(_ces_user("u1", action="Edit"))
        source.write_text(json.dumps(changed), encoding="utf-8")
        with self.assertRaises(ValueError):
            self._run(mode="replay", resume=directory)

    def test_resume_rejects_tampered_completed_case(self):
        """Given changed checkpoint content with its original identity hash
        When the saved run resumes
        Then the old completed case cannot contribute passing coverage
        """
        _, directory = self._run()
        checkpoint = directory / "cases.jsonl"
        lines = checkpoint.read_text().splitlines()
        changed = json.loads(lines[0])
        changed["effective"]["missing_count"] = 999
        lines[0] = json.dumps(changed)
        checkpoint.write_text("\n".join(lines) + "\n", encoding="utf-8")
        result, _ = self._run(resume=directory)
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(result["summary"]["matching_accounts"], 0)
        self.assertTrue(result["errors"])

    def test_stored_failed_http_status_cannot_supply_a_passing_user(self):
        """Given a stored failed HTTP capture with valid-looking permission JSON
        When replay evaluates the capture
        Then the failed response remains unavailable for passing comparison
        """
        folder = self._write_examples()
        path = folder / "ces-u2.yml"
        changed = json.loads(path.read_text())
        changed["examples"][0]["response"]["status"] = 503
        path.write_text(json.dumps(changed), encoding="utf-8")
        result, _ = self._run(mode="replay")
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(result["summary"]["matching_accounts"], 2)

    def test_stored_example_for_another_url_cannot_supply_requested_context(self):
        """Given a production example embedded under a different request URL
        When replay evaluates the configured request
        Then mismatched source context cannot supply a passing comparison
        """
        folder = self._write_examples()
        path = folder / "ces-u2.yml"
        changed = json.loads(path.read_text())
        changed["examples"][0]["request"]["url"] = "https://production.example.invalid/ces/app/NEW_APP/user/u2"
        path.write_text(json.dumps(changed), encoding="utf-8")
        result, _ = self._run(mode="replay")
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(result["summary"]["matching_accounts"], 2)


if __name__ == "__main__":
    unittest.main()
