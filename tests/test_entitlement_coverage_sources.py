"""Preserve source conflicts and extra migrated content in coverage results."""

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from ai_sdlc_workbench import entitlement_coverage as coverage
from ai_sdlc_workbench.entitlement_reconciliation import normalize_ces_catalog


APP = "APP"
ENTITY = "LEGACY"
USER = "fixture-account"


def old_response(role="R", feature="F"):
    def part(name):
        return {"name": name, "entity": {"name": ENTITY}}
    return {USER: {"count": 1, "entitlements": [
        {"subject": part(feature), "role": part(role), "action": part("View")}]}}


def user_response(pairs=None, roles=None):
    return [{"user_data": {"user_id": USER, "app_name": APP}, "entitlements": {
        "entitlement_name": ["R"] if roles is None else roles,
        "role_entitlements": [{"feature": feature, "action": action} for feature, action in
                              ([("F", "View")] if pairs is None else pairs)]}}]


def catalog_response(pairs=None, members=None):
    return [{"entitlement_name": "R", "role_entitlements": [
        {"feature": feature, "action": action} for feature, action in
        ([("F", "View")] if pairs is None else pairs)],
        "user_ids": [USER] if members is None else members}]


def baseline():
    return {"features": [(APP, "F")], "profiles": [(APP, "R")],
            "assignments": [(USER, APP, "R")], "grants": [(APP, "R", "F", "View")],
            "users": [USER], "matrices": [{"app": APP, "sha256": "controlled-matrix",
            "features": ["F"], "profiles": [[APP, "R"]], "missing_profile_definitions": []}]}


def config():
    return {"schema_version": 1, "scope": "Controlled source comparison", "workspace_root": ".",
            "output_dir": "runs", "workers": 1,
            "entities": [{"name": ENTITY, "app": APP, "id": "ENTITY-ID", "workbook": "matrix.xlsx"}],
            "ems2": {"entitlements_path": "/permissions", "subjects_path": "/entity/{entity_id}/subjects",
                     "roles_path": "/entity/{entity_id}/roles"},
            "ces": {"user_path": "/app/{app}/user/{user}", "catalog_path": "/app/{app}"}}


class StubCollector:
    """Use controlled records; no HTTP client or external service is involved."""

    def __init__(self, old=None, user=None, catalog=None, subject="F", role="R"):
        self.old = old_response() if old is None else old
        self.user = user_response() if user is None else user
        self.catalog = catalog_response() if catalog is None else catalog
        self.subject, self.role = subject, role

    def get(self, service, path, body=None):
        if service == "ems2":
            if path.endswith("/subjects"):
                return {"subjects": [{"name": self.subject}], "count": 1}
            if path.endswith("/roles"):
                return {"roles": [{"name": self.role}], "count": 1}
            return self.old
        return self.user if "/user/" in path else self.catalog


class CoverageSourceRegressionTests(unittest.TestCase):
    def compare(self, collector, settings=None, matrix=None):
        settings = config() if settings is None else settings
        matrix = baseline() if matrix is None else matrix
        catalog = normalize_ces_catalog(collector.catalog, APP)
        return coverage._case(USER, collector, settings, settings["entities"], matrix, {APP: catalog})

    def test_new_business_feature_is_additional_and_never_a_match(self):
        pairs = [("F", "View"), ("NEW_BUSINESS_FEATURE", "Edit")]
        record = self.compare(StubCollector(user=user_response(pairs), catalog=catalog_response(pairs)))
        self.assertEqual(record["status"], "DIFFERENT")
        self.assertEqual(record["effective"]["additional"], [[APP, "NEW_BUSINESS_FEATURE", "Edit"]])
        self.assertEqual(record["profile_grants"]["additional"], [[APP, "R", "NEW_BUSINESS_FEATURE", "Edit"]])
        self.assertEqual(record["outside_scope_permissions"], [])

    def test_explicit_feature_exclusion_does_not_hide_another_new_feature(self):
        pairs = [("F", "View"), ("MANAGEMENT", "Admin"), ("NEW_BUSINESS_FEATURE", "Edit")]
        settings = config(); settings["excluded_features"] = [{"app": APP, "feature": "MANAGEMENT"}]
        record = self.compare(StubCollector(user=user_response(pairs), catalog=catalog_response(pairs)), settings)
        self.assertEqual(record["status"], "DIFFERENT")
        self.assertEqual(record["outside_scope_permissions"], [[APP, "MANAGEMENT", "Admin"]])
        self.assertEqual(record["effective"]["additional"], [[APP, "NEW_BUSINESS_FEATURE", "Edit"]])

    def test_empty_added_profile_assignment_is_not_silently_dropped(self):
        catalog = catalog_response() + [{"entitlement_name": "ADDED_PROFILE", "role_entitlements": [],
                                         "user_ids": [USER]}]
        record = self.compare(StubCollector(user=user_response(roles=["R", "ADDED_PROFILE"]), catalog=catalog))
        self.assertEqual(record["status"], "DIFFERENT")
        self.assertEqual(record["assignments"]["additional"], [[APP, "ADDED_PROFILE"]])

    def test_catalog_membership_conflict_is_explicit_and_keeps_semantic_limit(self):
        record = self.compare(StubCollector(catalog=catalog_response(members=[])))
        self.assertEqual(record["effective"]["equal"], True)
        self.assertEqual(record["catalog_membership"]["status"], "UNASSESSED")
        self.assertEqual(record["catalog_membership"]["comparison"]["additional"], [[APP, "R"]])
        self.assertIn("inheritance", record["catalog_membership"]["limit"])

    def test_membership_only_conflict_remains_visible_in_html_and_csv(self):
        record = self.compare(StubCollector(catalog=catalog_response(members=[])))
        result = {"mode": "controlled", "started_at": "2026-11-03T00:00:00Z", "scope": "Controlled source conflict",
                  "inventory": {"baseline_users": [USER], "users": [USER]}, "users": [record],
                  "entitlements": {}, "excluded": [], "limits": [], "errors": []}
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            coverage._finish(result, directory)
            html = (directory / "report.html").read_text()
            csv = (directory / "differences.csv").read_text()
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertIn(USER, html.split("<tbody>", 1)[1].split("</tbody>", 1)[0])
        self.assertIn("catalog_membership", csv)

    def test_stale_matrix_assignment_does_not_change_equal_live_comparison(self):
        matrix = baseline(); matrix["assignments"] = [(USER, APP, "STALE_MATRIX_ROLE")]
        record = self.compare(StubCollector(), matrix=matrix)
        self.assertEqual(record["status"], "MATCH")
        self.assertTrue(record["assignments"]["equal"])
        self.assertEqual(record["matrix_assignment_comparison"]["missing"], [[APP, "STALE_MATRIX_ROLE"]])
        self.assertEqual(record["matrix_assignment_comparison"]["additional"], [[APP, "R"]])

    def test_live_inventories_apply_confirmed_subject_and_role_renames(self):
        settings = config()
        settings["role_mapping"] = {ENTITY: {"OLD_ROLE": "R"}}
        settings["subject_mapping"] = {ENTITY: {"OLD_FEATURE": "F"}}
        collector = StubCollector(old=old_response(role="OLD_ROLE", feature="OLD_FEATURE"),
                                  subject="OLD_FEATURE", role="OLD_ROLE")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); path = root / "config.json"; path.write_text(json.dumps(settings))
            with patch.object(coverage, "_baseline", return_value=baseline()), \
                 patch.object(coverage, "Collector", return_value=collector), redirect_stdout(io.StringIO()):
                result, _ = coverage.run(path, output=root / "out")
        self.assertEqual(result["status"], "FUNCTIONAL_MATCH")
        self.assertTrue(all(item["comparison"]["equal"] for item in result["entitlements"]["live_inventories"]))
        self.assertEqual(result["users"][0]["status"], "MATCH")


if __name__ == "__main__":
    unittest.main()
