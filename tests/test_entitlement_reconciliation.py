"""Check permission identity, complete data parsing, and comparison boundaries."""

from __future__ import annotations

import copy
import unittest

from ai_sdlc_workbench.entitlement_reconciliation import (
    ReconciliationError,
    compare_sets,
    normalize_ces_catalog,
    normalize_ces_user,
    normalize_ems2_permissions,
    split_user_ids,
)


def ems_permission(entity="OLD_APP", role="Reader", subject="Ledger", action="View"):
    return {key: {"name": name, "entity": {"name": entity}}
            for key, name in (("role", role), ("subject", subject), ("action", action))}


def ems_response(*rows):
    return {"007": {"count": len(rows), "entitlements": list(rows)}}


def ces_catalog(role="Reader", users=None, feature="Ledger", action="View"):
    return [{"entitlement_name": role, "role_entitlements": [{"feature": feature, "action": action}],
             "user_ids": ["007"] if users is None else users}]


def ces_user(role="Reader", user="007", app="NEW_APP", feature="Ledger", action="View"):
    return [{"user_data": {"user_id": user, "app_name": app},
             "entitlements": {"entitlement_name": [role],
                              "role_entitlements": [{"feature": feature, "action": action}],
                              "data_profiles": {"data_profile_rules": [{"name": "Global"}]},
                              "data_entitlements": [{"key": "Region", "values": ["A1", "003"]}]}}]


class AccountCellTests(unittest.TestCase):
    def test_all_ids_in_large_cells_and_nested_arrays_are_expanded(self):
        """Given 5000 account IDs in one cell and overlapping array values
        When account IDs are expanded
        Then every unique ID remains and string leading zeroes remain
        """
        cell = ";\n".join(f"u{number}" for number in range(5000))
        result = split_user_ids([cell, '["007", "u1", "srv.alpha.001"]', 123.0])
        self.assertEqual(len(result), 5003)
        self.assertTrue({"u0", "u4999", "007", "srv.alpha.001", "123"}.issubset(result))

    def test_ambiguous_identifier_values_fail_instead_of_becoming_accounts(self):
        """Given invalid account cell values
        When account IDs are expanded
        Then parsing fails instead of inventing users
        """
        for value in (True, {"user": "007"}, 1.5, float("nan"), "[007,008]"):
            with self.subTest(value=type(value).__name__):
                with self.assertRaises(ReconciliationError):
                    split_user_ids(value)
        self.assertEqual(split_user_ids(None), [])
        self.assertEqual(split_user_ids(" 007,008|007 \t srv.alpha.001 "), ["007", "008", "srv.alpha.001"])


class EmsContractTests(unittest.TestCase):
    def test_scoped_mapping_keeps_app_role_subject_and_action_identity(self):
        """Given names shared by two EMS entities
        When explicit scoped mappings are applied
        Then both application contexts remain and all four names are mapped
        """
        response = ems_response(ems_permission(), ems_permission(entity="OTHER_APP"))
        result = normalize_ems2_permissions(response, {"OLD_APP": "NEW_APP", "OTHER_APP": "SECOND_APP"},
            role_mapping={"OLD_APP": {"Reader": "Read Only"}},
            subject_mapping={"OLD_APP": {"Ledger": "Transactions"}},
            action_mapping={"OLD_APP": {"View": "Read"}})["users"]["007"]
        self.assertEqual(result["grants"], [["NEW_APP", "Read Only", "Transactions", "Read"],
                                            ["SECOND_APP", "Reader", "Ledger", "View"]])
        self.assertEqual(result["assignments"], [["NEW_APP", "Read Only"], ["SECOND_APP", "Reader"]])
        self.assertEqual(result["assignment_source"], "PERMISSION_ROWS_ONLY")
        self.assertEqual(result["data_scope_assessment"], "UNASSESSED")

    def test_duplicate_rows_do_not_inflate_permissions(self):
        """Given duplicate EMS2 permission rows
        When the source row count is valid
        Then one unique grant and one effective permission remain
        """
        row = ems_permission()
        result = normalize_ems2_permissions(ems_response(row, row), {"OLD_APP": "NEW_APP"})["users"]["007"]
        self.assertEqual(len(result["grants"]), 1)
        self.assertEqual(len(result["effective_permissions"]), 1)

    def test_count_mismatch_unknown_entity_and_conflicting_context_fail(self):
        """Given incomplete rows or ambiguous entity mappings
        When the source is normalized
        Then parsing fails instead of comparing partial or wrongly scoped grants
        """
        response = ems_response(ems_permission())
        truncated = copy.deepcopy(response)
        truncated["007"]["count"] = 2
        conflict = copy.deepcopy(response)
        conflict["007"]["entitlements"][0]["action"]["entity"]["name"] = "OTHER_APP"
        for value, mapping in ((truncated, {"OLD_APP": "NEW_APP"}), (response, {}),
                               (conflict, {"OLD_APP": "NEW_APP"})):
            with self.subTest(response=value):
                with self.assertRaises(ReconciliationError):
                    normalize_ems2_permissions(value, mapping)

    def test_error_and_missing_permission_fields_never_become_empty_success(self):
        """Given an error response or omitted entitlement rows
        When the response is normalized
        Then the source is unavailable for comparison
        """
        for response in ({"error": "unavailable"}, {"007": {}}, {"007": {"entitlements": None}},
                         {"007": {"entitlements": []}}, None):
            with self.subTest(response=response):
                with self.assertRaises(ReconciliationError):
                    normalize_ems2_permissions(response, {"OLD_APP": "NEW_APP"})
        result = normalize_ems2_permissions(ems_response(), {"OLD_APP": "NEW_APP"})
        self.assertEqual(result["users"]["007"]["grants"], [])


class CesContractTests(unittest.TestCase):
    def test_catalog_membership_expands_all_accounts_and_retains_empty_roles(self):
        """Given delimited catalog users and an empty entitlement definition
        When the CES catalog is normalized
        Then all users and both entitlement definitions remain
        """
        body = ces_catalog(users=["007,008", "srv.alpha.001\nsrv.beta.001", "007"])
        body.append({"entitlement_name": "Empty role", "role_entitlements": [], "user_ids": ["009"]})
        result = normalize_ces_catalog(body, "NEW_APP")
        self.assertEqual(result["users"], ["007", "008", "009", "srv.alpha.001", "srv.beta.001"])
        self.assertIn(["009", "NEW_APP", "Empty role"], result["assignments"])
        self.assertEqual(result["entitlements"], ["Empty role", "Reader"])
        self.assertEqual(result["grants"], [["NEW_APP", "Reader", "Ledger", "View"]])

    def test_missing_membership_or_duplicate_entitlement_names_fail(self):
        """Given an incomplete membership field or ambiguous catalog identity
        When the CES catalog is normalized
        Then the catalog cannot establish complete assignment parity
        """
        absent = ces_catalog()
        del absent[0]["user_ids"]
        null = ces_catalog()
        null[0]["user_ids"] = None
        duplicate = ces_catalog() + ces_catalog(feature="Other feature")
        for body in (absent, null, duplicate, {"error": "unavailable"}):
            with self.subTest(body=body):
                with self.assertRaises(ReconciliationError):
                    normalize_ces_catalog(body, "NEW_APP")

    def test_effective_response_retains_assignments_and_data_without_role_fabrication(self):
        """Given an effective CES response with role names and data filters
        When permissions are normalized
        Then grants retain application context and role provenance remains unavailable
        """
        result = normalize_ces_user(ces_user(), "NEW_APP", expected_user="007")["users"]["007"]
        self.assertEqual(result["assignments"], [["NEW_APP", "Reader"]])
        self.assertEqual(result["effective_permissions"], [["NEW_APP", "Ledger", "View"]])
        self.assertNotIn("grants", result)
        self.assertEqual(result["role_provenance"], "UNAVAILABLE")
        self.assertEqual(result["data_scope_assessment"], "UNASSESSED")
        self.assertEqual(result["data_scope"]["data_entitlements"][0]["values"], ["A1", "003"])

    def test_wrong_user_app_or_duplicate_records_fail_context_binding(self):
        """Given a response for a different context or duplicate account records
        When the requested user is bound
        Then normalization rejects the response
        """
        for body in (ces_user(user="008"), ces_user(app="OTHER_APP"), ces_user() + ces_user()):
            with self.subTest(body=body):
                with self.assertRaises(ReconciliationError):
                    normalize_ces_user(body, "NEW_APP", expected_user="007")

    def test_explicit_absence_and_malformed_response_have_distinct_outcomes(self):
        """Given an explicit absent user and malformed responses
        When CES user content is normalized
        Then absence remains empty and malformed content fails
        """
        self.assertEqual(normalize_ces_user([], "NEW_APP", expected_user="007")["users"], {})
        missing = ces_user()
        del missing[0]["entitlements"]["role_entitlements"]
        for body in (missing, {"error": "unavailable"}, None):
            with self.subTest(body=body):
                with self.assertRaises(ReconciliationError):
                    normalize_ces_user(body, "NEW_APP", expected_user="007")


class SetComparisonTests(unittest.TestCase):
    def test_missing_and_extra_rows_stay_visible_while_matches_leave_differences(self):
        """Given one preserved, one missing, and one additional permission
        When permission sets are compared
        Then the rate uses the complete baseline and differences exclude matches
        """
        old = [["App", "Role", "A", "View"], ["App", "Role", "B", "View"]]
        new = [["App", "Role", "A", "View"], ["App", "Role", "C", "View"]]
        result = compare_sets(old, new)
        self.assertEqual(result["status"], "DIFFERENT")
        self.assertEqual(result["coverage_percent"], 50)
        self.assertEqual(result["matched"], [old[0]])
        self.assertEqual(result["differences"], {"missing": [old[1]], "additional": [new[1]]})
        self.assertFalse(result["preserved"])
        self.assertFalse(result["equal"])

    def test_effective_union_cannot_hide_changed_role_content(self):
        """Given identical effective grants under different role definitions
        When complete role and permission identities are compared
        Then the role comparison differs despite equal effective permissions
        """
        old = normalize_ems2_permissions(ems_response(ems_permission()), {"OLD_APP": "NEW_APP"})["users"]["007"]
        new = normalize_ces_catalog(ces_catalog(role="Other Reader"), "NEW_APP")
        effective = normalize_ces_user(ces_user(role="Other Reader"), "NEW_APP", expected_user="007")["users"]["007"]
        self.assertEqual(compare_sets(old["effective_permissions"], effective["effective_permissions"])["status"], "PASS")
        self.assertEqual(compare_sets(old["grants"], new["grants"])["missing_count"], 1)
        self.assertEqual(compare_sets(old["assignments"], effective["assignments"])["status"], "DIFFERENT")

    def test_case_application_and_unexpected_grants_affect_equality(self):
        """Given same-name grants in another application or another case
        When exact identities are compared
        Then they remain missing or additional rather than matched
        """
        baseline = [["App", "Feature", "View"]]
        result = compare_sets(baseline, baseline + [["Other App", "Feature", "View"]])
        self.assertEqual(result["coverage_percent"], 100)
        self.assertTrue(result["preserved"])
        self.assertFalse(result["equal"])
        self.assertEqual(result["status"], "DIFFERENT")
        self.assertEqual(compare_sets(baseline, [["App", "Feature", "view"]])["matched_count"], 0)

    def test_empty_unavailable_and_incompatible_dimensions_cannot_get_full_coverage(self):
        """Given empty, unavailable, or incompatible comparison inputs
        When comparison runs
        Then zero baseline has no rate and unavailable inputs fail
        """
        empty = compare_sets([], [])
        self.assertEqual(empty["status"], "EMPTY")
        self.assertIsNone(empty["coverage_percent"])
        self.assertEqual(compare_sets([], [["App", "Role"]])["status"], "DIFFERENT")
        for old, new in ((None, []), ([], None), ("App", []), ([["App"]], [["App", "Role"]]),
                         ([["App"], ["App", "Role"]], [])):
            with self.subTest(old=old, new=new):
                with self.assertRaises(ReconciliationError):
                    compare_sets(old, new)


if __name__ == "__main__":
    unittest.main()
