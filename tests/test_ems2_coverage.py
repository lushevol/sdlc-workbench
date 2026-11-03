"""Verify EMS2 environment comparison with controlled stored responses only."""
from contextlib import redirect_stderr, redirect_stdout
import io
import json
import re
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from ai_sdlc_workbench import ems2_coverage as coverage
from ai_sdlc_workbench import entitlement_coverage as shared
from test_entitlement_coverage import _matrix


def grant(role="Reader", subject="Ledger", action="View", entity="OLD_APP", identifier=1):
    return {key: {"id": identifier, "name": value, "entity": {"id": identifier, "name": entity}}
            for key, value in (("role", role), ("subject", subject), ("action", action))}


class Ems2CoverageTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="ems2-coverage-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        _matrix(self.root / "matrix.xlsx", users="u1;u2")
        self.config = {"schema_version": 1, "scope": "Controlled EMS2 PROD versus UAT", "workspace_root": ".",
                       "output_dir": "runs", "workers": 1, "retries": 0,
                       "entities": [{"name": "OLD_APP", "workbook": "matrix.xlsx", "prod_id": "P1", "uat_id": "U1"},
                                    {"name": "FMO", "included": False, "workbook": "absent.xlsx"}],
                       "replay": {"examples": ["examples/*.yml"]}}
        for environment in ("prod", "uat"):
            self.config[environment] = {"base_url": "https://" + environment + ".example.invalid", "entitlements_path": "/permissions",
                                        "subjects_path": "/entity/{entity_id}/subjects", "roles_path": "/entity/{entity_id}/roles"}
        self.config_path = self.root / "config.json"
        self.save_config()
        self.examples = self.root / "examples"
        self.examples.mkdir()
        for environment, identifier in (("prod", "P1"), ("uat", "U1")):
            for kind, name in (("subjects", "Ledger"), ("roles", "Reader")):
                self.example(environment + "-" + kind, environment, "/entity/" + identifier + "/" + kind,
                             {"count": 1, kind: [{"name": name}]})
            for user in ("u1", "u2"):
                self.user_example(environment, user, [grant(identifier=1 if environment == "prod" else 999)])

    def save_config(self):
        self.config_path.write_text(json.dumps(self.config))

    def example(self, name, environment, path, response, body=None, status=200):
        url = self.config[environment]["base_url"] + path
        request = {"method": "POST" if body is not None else "GET", "url": url}
        if body is not None: request["body"] = {"type": "json", "data": json.dumps(body)}
        value = {"http": request, "examples": [{"request": {"method": request["method"], "url": url},
                   "response": {"status": status, "body": {"type": "json", "data": json.dumps(response)}}}]}
        file = self.examples / (name + ".yml")
        file.write_text(json.dumps(value))
        return file

    def user_example(self, environment, user, grants):
        return self.example(environment + "-" + user, environment, "/permissions",
                            {user: {"count": len(grants), "entitlements": grants}}, {user: ["OLD_APP"]})

    def run_comparison(self, **kwargs):
        with redirect_stderr(io.StringIO()): return coverage.run(self.config_path, **kwargs)

    def change_example(self, name, mutation):
        path = self.examples / (name + ".yml")
        value = json.loads(path.read_text()); mutation(value); path.write_text(json.dumps(value))

    def test_default_cli_replays_without_credentials_or_http_and_ignores_numeric_ids(self):
        """Given paired stored responses with different numeric environment identifiers
        When the default CLI runs with credentials and HTTP construction forbidden
        Then names compare equally and saved outputs remain explicitly mock evidence
        """
        output = io.StringIO(); directory = self.root / "default"
        with patch.object(coverage, "load_root_env", side_effect=AssertionError("Read private environment")), \
             patch.object(shared, "JsonHttpClient", side_effect=AssertionError("Constructed HTTP client")), \
             redirect_stdout(output), redirect_stderr(io.StringIO()):
            status = coverage.main(["--config", str(self.config_path), "--output", str(directory)])
        result = json.loads((directory / "result.json").read_text())
        self.assertEqual(status, 0)
        self.assertEqual(result["summary"]["functional_profile_coverage_percent"], 100)
        self.assertEqual(result["summary"]["subject_coverage_percent"], 100)
        self.assertEqual(json.loads(output.getvalue())["mode"], "replay")
        self.assertIn("MOCK: supplied API responses", (directory / "report.html").read_text())
        self.assertEqual(result["excluded"][0]["name"], "FMO")
        self.assertEqual(len((directory / "differences.csv").read_text().splitlines()), 1)
        active = re.search(r"<table[^>]*id=[\"']users[\"'][^>]*>(.*?)</table>",
                           (directory / "report.html").read_text(), re.S)
        self.assertNotIn("<td>u1</td>", active.group(1) if active else "")
        self.assertIn("u1", (directory / "report.md").read_text())
        self.assertEqual(json.loads(output.getvalue())["markdown_report"], str(directory.resolve() / "report.md"))
        self.assertIn("coverage_reporting.py", result["binding"]["implementation_sha256"])
        context = result["comparison_context"]
        self.assertEqual(context["entities"][0]["prod_id"], "P1")
        self.assertEqual(context["entities"][0]["uat_id"], "U1")
        self.assertEqual(context["matrices"][0]["account_count"], 2)
        self.assertEqual(context["sources"]["baseline"]["base_url"], "https://prod.example.invalid")
        self.assertEqual(result["users"][0]["profile_grants"]["matched"], [["OLD_APP", "Reader", "Ledger", "View"]])

    def test_report_context_omits_credential_settings_and_redacts_url_values(self):
        """Given private URL userinfo and query values in routing configuration
        When report provenance is projected
        Then only safe environment routes and matrix metadata remain
        """
        self.config["prod"].update(base_url="https://private-user:private-password@prod.example.invalid:8443/?access=private-query#private-fragment",
                                   token_env="PRIVATE_TOKEN_REFERENCE", ca_env="PRIVATE_CA_REFERENCE")
        context = shared._comparison_context(self.config, self.root, self.config["entities"][:1],
                                             [shared.read_matrix(self.root / "matrix.xlsx")], family="EMS2_ENVIRONMENTS")
        serialized = json.dumps(context)
        for private in ("private-user", "private-password", "private-query", "private-fragment",
                        "PRIVATE_TOKEN_REFERENCE", "PRIVATE_CA_REFERENCE"):
            self.assertNotIn(private, serialized)
        self.assertEqual(context["sources"]["baseline"]["base_url"],
                         "https://prod.example.invalid:8443/?access=REDACTED")
        self.assertEqual(context["matrices"][0]["sheets"]["grants"], "EntitlementFeatureAction")

    def test_role_change_with_equal_effective_union_is_a_profile_difference(self):
        """Given UAT has the same effective action through a different role
        When the profile comparison runs
        Then role provenance and assignments differ despite effective equality
        """
        self.user_example("uat", "u1", [grant(role="Other")])
        result, _ = self.run_comparison()
        user = next(user for user in result["users"] if user["user_id"] == "u1")
        self.assertTrue(user["effective"]["equal"])
        self.assertEqual(user["status"], "DIFFERENT")
        self.assertEqual(user["assignments"]["missing"], [["OLD_APP", "Reader"]])
        self.assertEqual(user["profile_grants"]["additional"], [["OLD_APP", "Other", "Ledger", "View"]])
        self.assertEqual(result["summary"]["functional_profile_coverage_percent"], 50)

    def test_missing_and_additional_permissions_keep_prod_to_uat_direction(self):
        """Given a PROD View grant replaced by an unrelated UAT Edit grant
        When reports compare the two environments
        Then missing refers to UAT omissions and additional refers to UAT additions
        """
        self.user_example("uat", "u1", [grant(subject="Extra", action="Edit")])
        result, directory = self.run_comparison()
        user = next(user for user in result["users"] if user["user_id"] == "u1")
        self.assertEqual(user["effective"]["missing"], [["OLD_APP", "Ledger", "View"]])
        self.assertEqual(user["effective"]["additional"], [["OLD_APP", "Extra", "Edit"]])
        self.assertIn('missing', (directory / "differences.csv").read_text())
        report = (directory / "report.html").read_text()
        self.assertIn("EMS2 PROD", report)
        self.assertIn("EMS2 UAT", report)
        self.assertIn("Ledger", (directory / "report.md").read_text())
        self.assertIn("Extra", (directory / "report.md").read_text())

    def test_missing_capture_stays_unassessed_with_full_population_denominator(self):
        """Given a discovered user without a UAT response
        When mocks run without HTTP fallback
        Then the account is unassessed and complete profile coverage stays null
        """
        (self.examples / "uat-u2.yml").unlink()
        with patch.object(shared, "JsonHttpClient", side_effect=AssertionError("HTTP fallback")):
            result, directory = self.run_comparison()
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(result["summary"]["compared_accounts"], 1)
        self.assertEqual(result["summary"]["unassessed_accounts"], 1)
        self.assertIsNone(result["summary"]["functional_profile_coverage_percent"])
        self.assertIn("REPLAY_NOT_CAPTURED", (directory / "differences.csv").read_text())

    def test_missing_subject_inventory_does_not_claim_partial_coverage_complete(self):
        """Given paired users but no UAT subject inventory
        When definition coverage is summarized
        Then unknown inventory coverage stays null and its source error remains visible
        """
        (self.examples / "uat-subjects.yml").unlink()
        result, directory = self.run_comparison()
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertIsNone(result["entitlements"]["subjects"]["coverage_percent"])
        self.assertEqual(result["entitlements"]["subjects"]["unassessed_entities"], ["OLD_APP"])
        self.assertEqual(result["summary"]["matching_accounts"], 2)
        self.assertIn("inventory,OLD_APP,subjects,unassessed", (directory / "differences.csv").read_text())

    def test_request_example_environment_mismatch_cannot_supply_uat_user(self):
        """Given a UAT request whose stored example identifies the PROD URL
        When replay resolves the UAT user
        Then the mismatched example cannot become a successful UAT comparison
        """
        self.change_example("uat-u1", lambda value: value["examples"][0]["request"].update(url=self.config["prod"]["base_url"] + "/permissions"))
        result, _ = self.run_comparison()
        user = next(user for user in result["users"] if user["user_id"] == "u1")
        self.assertEqual(user["status"], "UNASSESSED")
        self.assertEqual(user["errors"], [{"source": "uat", "code": "REPLAY_NOT_CAPTURED", "http_status": None}])

    def test_wrong_entity_inventory_cannot_pass_by_matching_names(self):
        """Given equal subject names returned under a contradictory UAT entity
        When inventory coverage checks the requested entity context
        Then the UAT inventory is unassessed instead of a passing name match
        """
        self.example("uat-subjects", "uat", "/entity/U1/subjects", {
            "count": 1, "subjects": [{"name": "Ledger", "entity": {"id": 999, "name": "WRONG_ENTITY"}}]})
        result, _ = self.run_comparison()
        check = next(x for x in result["entitlements"]["inventories"] if x["kind"] == "subjects")
        self.assertEqual(check["status"], "UNASSESSED")
        self.assertEqual(check["errors"], [{"source": "uat", "code": "ENTITY_CONTEXT_MISMATCH", "http_status": None}])
        self.assertIsNone(result["summary"]["subject_coverage_percent"])

    def test_mismatched_counts_and_entity_contexts_cannot_pass(self):
        """Given a partial PROD collection and contradictory UAT entity contexts
        When both source contracts are normalized
        Then both malformed inputs remain unassessed instead of empty passing grants
        """
        self.example("prod-u1", "prod", "/permissions", {"u1": {"count": 2, "entitlements": [grant()]}}, {"u1": ["OLD_APP"]})
        bad = grant(); bad["subject"]["entity"]["name"] = "DIFFERENT_ENTITY"
        self.user_example("uat", "u1", [bad])
        result, _ = self.run_comparison()
        user = next(user for user in result["users"] if user["user_id"] == "u1")
        self.assertEqual(user["status"], "UNASSESSED")
        self.assertEqual({error["source"] for error in user["errors"]}, {"prod", "uat"})
        self.assertNotIn("effective", user)

    def test_entity_identity_prevents_cross_entity_grant_collapse(self):
        """Given equal role names and actions under two distinct entities
        When PROD grants entity A and UAT grants entity B
        Then the entity-specific grant remains missing and additional
        """
        self.config["entities"].append({"name": "SECOND", "workbook": "matrix.xlsx", "prod_id": "P2", "uat_id": "U2"})
        self.save_config()
        for environment in ("prod", "uat"):
            self.example(environment + "-u1", environment, "/permissions", {"u1": {"count": 1, "entitlements": [grant(entity="OLD_APP" if environment == "prod" else "SECOND")]}}, {"u1": ["OLD_APP", "SECOND"]})
        result, _ = self.run_comparison()
        user = next(user for user in result["users"] if user["user_id"] == "u1")
        self.assertEqual(user["profile_grants"]["missing"], [["OLD_APP", "Reader", "Ledger", "View"]])
        self.assertEqual(user["profile_grants"]["additional"], [["SECOND", "Reader", "Ledger", "View"]])

    def test_discovery_expands_request_users_and_explicit_users_without_ces(self):
        """Given a service account in stored requests and another configured account
        When the population is built from matrix cells and request sources
        Then discovery covers the union without requiring a CES catalog
        """
        self.config["users"] = ["explicit;u1"]; self.save_config()
        self.user_example("prod", "service", [grant()]); self.user_example("uat", "service", [grant()])
        result, _ = self.run_comparison()
        self.assertEqual(result["inventory"]["users"], ["explicit", "service", "u1", "u2"])
        self.assertEqual(result["summary"]["compared_accounts"], 3)
        self.assertEqual(result["summary"]["unassessed_accounts"], 1)

    def test_resume_uses_durable_cases_and_rejects_changed_source_hashes(self):
        """Given one checkpoint and unchanged source inputs
        When a run resumes then a modified capture is offered
        Then completed evidence is reused and changed inputs reject reuse
        """
        first, directory = self.run_comparison(user_limit=1)
        self.assertEqual(first["summary"]["unassessed_accounts"], 1)
        first_case = (directory / "cases.jsonl").read_text().splitlines()[0]
        second, _ = self.run_comparison(resume=directory)
        self.assertEqual(second["status"], "FUNCTIONAL_MATCH")
        self.assertEqual((directory / "cases.jsonl").read_text().splitlines()[0], first_case)
        self.user_example("uat", "u2", [grant(action="Edit")])
        with self.assertRaises(ValueError): self.run_comparison(resume=directory)

    def test_tampered_checkpoint_is_not_reused_as_passing_evidence(self):
        """Given a completed case changed without updating its identity hash
        When the saved run resumes
        Then the corrupted case cannot contribute a passing profile rate
        """
        _, directory = self.run_comparison()
        file = directory / "cases.jsonl"; lines = file.read_text().splitlines()
        changed = json.loads(lines[0]); changed["status"] = "DIFFERENT"; lines[0] = json.dumps(changed)
        file.write_text("\n".join(lines) + "\n")
        result, _ = self.run_comparison(resume=directory)
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(result["summary"]["matching_accounts"], 0)
        self.assertIsNone(result["summary"]["functional_profile_coverage_percent"])
        self.assertTrue(result["errors"])

    def test_completed_case_is_saved_before_later_interruption(self):
        """Given interruption while the second account compares
        When the first account already finished
        Then its hash-bound checkpoint survives and resume finishes the population
        """
        original = coverage._case
        def interrupted(user, *args):
            if user == "u2": raise KeyboardInterrupt("Controlled interruption")
            return original(user, *args)
        directory = self.root / "interrupted"
        with patch.object(coverage, "_case", side_effect=interrupted):
            with self.assertRaises(KeyboardInterrupt): self.run_comparison(output=directory)
        self.assertEqual(len((directory / "cases.jsonl").read_text().splitlines()), 1)
        result, _ = self.run_comparison(resume=directory)
        self.assertEqual(result["summary"]["matching_accounts"], 2)

    def test_successful_empty_uat_is_missing_permissions_instead_of_unknown(self):
        """Given an explicit successful empty UAT permission collection
        When it is compared with a nonempty PROD user
        Then the missing grant is a difference rather than unavailable evidence
        """
        self.user_example("uat", "u1", [])
        result, _ = self.run_comparison()
        user = next(user for user in result["users"] if user["user_id"] == "u1")
        self.assertEqual(user["status"], "DIFFERENT")
        self.assertEqual(user["effective"]["missing_count"], 1)
        self.assertEqual(user["errors"], [])

    def test_live_adapter_routes_both_environments_through_the_existing_http_contract(self):
        """Given a controlled HTTP client stub for explicitly selected live mode
        When both environment adapters acquire inventories and account permissions
        Then every configured PROD and UAT route is called with its own request identity
        """
        calls = []
        def request(method, url, *, body=None, token_env=None, ca_env=None):
            calls.append((method, url, body))
            if method == "POST":
                user = next(iter(body))
                data = {user: {"count": 1, "entitlements": [grant()]}}
            else:
                kind = url.rsplit("/", 1)[1]
                data = {"count": 1, kind: [{"name": "Ledger" if kind == "subjects" else "Reader"}]}
            return {"data": data, "at": "controlled-time", "status": 200, "url": url, "sha256": shared._hash(data)}
        with patch.object(coverage, "load_root_env", return_value={}) as environment, \
             patch.object(shared.JsonHttpClient, "request", side_effect=request):
            result, _ = self.run_comparison(mode="live")
        self.assertEqual(result["status"], "FUNCTIONAL_MATCH")
        self.assertEqual(result["evidence_source"], "LIVE: collected API responses")
        self.assertEqual(environment.call_count, 1)
        self.assertEqual(len(calls), 8)
        self.assertTrue(any(url.endswith("/entity/P1/subjects") for _, url, _ in calls))
        self.assertTrue(any(url.endswith("/entity/U1/subjects") for _, url, _ in calls))
        self.assertEqual({next(iter(body)) for method, _, body in calls if method == "POST"}, {"u1", "u2"})

    def test_unavailable_uat_only_discovered_account_keeps_complete_profile_rate_unknown(self):
        """Given two assessed baseline users and an additional UAT request account
        When the additional account has no matching PROD capture
        Then baseline assessment cannot imply complete discovered-population coverage
        """
        self.user_example("uat", "candidate-only", [grant()])
        result, _ = self.run_comparison()
        self.assertEqual(result["summary"]["matching_baseline_accounts"], 2)
        self.assertEqual(result["summary"]["baseline_accounts"], 2)
        self.assertEqual(result["summary"]["unassessed_accounts"], 1)
        self.assertIsNone(result["summary"]["functional_profile_coverage_percent"])


if __name__ == "__main__":
    unittest.main()
