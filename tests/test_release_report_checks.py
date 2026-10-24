"""Verify report failure summaries against explicit retained observations."""

from copy import deepcopy
import unittest

from ai_sdlc_workbench.release_report_checks import release_checks


class ReleaseReportChecksTests(unittest.TestCase):
    def test_failed_build_tests_and_gate_keep_their_reasons(self):
        """
        Scenario: Explain retained failed checks
          Given a failed build has a compiler issue
          And one requirement has failed tests
          And its Sonar gate has a failed coverage condition
          When the report derives its failure summary
          Then the compiler reason and condition values remain visible
          And absent test reasons are identified explicitly
          And the snapshot remains unchanged
        """
        snapshot = {
            "builds": [{"id": 101, "build": {"result": "failed"}, "timeline": {"records": [
                {"name": "Compile", "result": "failed", "issues": [{"type": "error", "message": "Missing package."}]}]}}],
            "tests": [{"build_id": 101, "requirementCoverages": [{"id": 201,
                "testExecutionStatusStats": {"countByType": {"FAILED": 2}}}]}],
            "sonarqube": [{"build_id": 101, "component": "app", "association_status": "matched", "gate": {
                "projectStatus": {"status": "ERROR", "conditions": [{"status": "ERROR", "metricKey": "coverage",
                    "comparator": "LT", "actualValue": "61", "errorThreshold": "80"}]}}}],
        }
        before = deepcopy(snapshot)
        checks = release_checks(snapshot)
        failed = [item for item in checks if item["severity"] == "failed"]
        self.assertEqual(len(failed), 3)
        self.assertTrue(any("Compile: Missing package." in item["reason"] for item in failed))
        self.assertTrue(any("2 failed test(s)" in item["reason"] and "does not provide" in item["reason"] for item in failed))
        self.assertTrue(any("coverage: observed 61; failure condition < 80" in item["reason"] for item in failed))
        self.assertEqual(snapshot, before)

    def test_missing_evidence_is_unavailable_and_never_passed(self):
        """
        Scenario: Separate missing evidence from failed execution
          Given an unavailable production comparison and denied source read
          And tests are blocked without failed assertions
          When the report derives its checks
          Then each limit has an unavailable status and a reason
          And no failed or passed execution is invented
        """
        checks = release_checks({
            "builds": [{"id": 101, "comparisons": {"production": {"status": "unavailable", "reason": "No deployed commit."}}}],
            "tests": [{"build_id": 101, "requirementCoverages": [{"id": 201,
                "testExecutionStatusStats": {"countByType": {"BLOCKED": 1}}}]}],
            "errors": [{"code": "TOOL_NOT_GRANTED", "tool": "report_coverage",
                        "message": "The requested report information is unavailable."}],
        })
        self.assertEqual({item["severity"] for item in checks}, {"unavailable"})
        self.assertTrue(all(item["reason"] for item in checks))
        self.assertTrue(any("No deployed commit." in item["reason"] for item in checks))
        self.assertTrue(any("does not grant" in item["reason"] for item in checks))
        self.assertTrue(any("1 blocked" in item["reason"] for item in checks))

    def test_current_sonar_failure_is_deduplicated_without_build_association_claim(self):
        """
        Scenario: Share one current Sonar observation across builds
          Given two builds share one current Sonar gate failure
          And neither analysis is matched to a build
          When the report derives its summary
          Then one gate failure remains with the unverified association limit
          And both build identities remain in its reason
        """
        item = {"component": "app", "branch": "release/1", "status": "complete", "association_status": "current_snapshot",
                "gate": {"projectStatus": {"status": "ERROR", "conditions": []}}}
        checks = release_checks({"sonarqube": [{**item, "build_id": 101}, {**item, "build_id": 102}]})
        self.assertEqual(len(checks), 1)
        self.assertEqual(checks[0]["severity"], "failed")
        self.assertIn("101, 102", checks[0]["reason"])
        self.assertIn("unverified", checks[0]["reason"])
        self.assertIn("without failed condition details", checks[0]["reason"])

    def test_comparison_direction_and_complete_counts_control_git_failures(self):
        """
        Scenario: Explain candidate and baseline differences
          Given a candidate differs from its branch tip and lacks main commits
          And another comparison has unknown counts
          When the report derives its checks
          Then branch and main differences have precise direction and reasons
          And unknown counts remain unavailable
          And absent merge-only evidence is not assumed
        """
        checks = release_checks({"builds": [{"id": 101, "comparisons": {
            "branch": {"status": "complete", "aheadCount": 1, "behindCount": 0},
            "main": {"status": "complete", "aheadCount": 0, "behindCount": 3},
            "production": {"status": "complete", "aheadCount": None, "behindCount": None},
        }}]})
        self.assertEqual([item["severity"] for item in checks], ["failed", "failed", "unavailable"])
        self.assertTrue(any("1 commit(s) ahead and 0 commit(s) behind" in item["reason"] for item in checks))
        self.assertTrue(any("lacks 3 commit(s) from main" in item["reason"] and
                            "Merge-only exceptions were not evaluated" in item["reason"] for item in checks))

    def test_counts_stay_build_specific_and_order_is_deterministic(self):
        """
        Scenario: Keep separate failed test counts
          Given two builds report different failures for one requirement
          And a duplicate report repeats the same observation
          When the report derives checks twice
          Then each build has its own count with no combined total
          And duplicates disappear and output order is stable
        """
        reports = [{"build_id": build, "requirementCoverages": [{"id": 201,
            "testExecutionStatusStats": {"countByType": {"FAILED": count}}}]} for build, count in ((101, 1), (102, 2))]
        snapshot = {"tests": [*reports, reports[0]]}
        checks = release_checks(snapshot)
        self.assertEqual(len(checks), 2)
        self.assertEqual(checks, release_checks(snapshot))
        self.assertIn("Build 101", checks[0]["entity"])
        self.assertIn("1 failed", checks[0]["reason"])
        self.assertIn("Build 102", checks[1]["entity"])
        self.assertIn("2 failed", checks[1]["reason"])

    def test_success_and_low_numeric_coverage_do_not_create_failed_checks(self):
        """
        Scenario: Avoid inventing quality rules
          Given successful build evidence and low numeric coverage
          And all complete comparisons have zero differences
          When the report derives checks
          Then no failure or passing approval is created
          And coverage has no invented threshold
        """
        checks = release_checks({"builds": [{"id": 101, "build": {"result": "succeeded"},
            "comparisons": {"branch": {"status": "complete", "aheadCount": 0, "behindCount": 0}}}],
            "coverage": [{"build_id": 101, "summary": {"line_coverage": 0}}]})
        self.assertEqual(checks, [])

    def test_failed_timeline_step_remains_visible_under_a_successful_build(self):
        """
        Scenario: Preserve a failed optional build step
          Given the build result is succeeded
          And one timeline step explicitly reports failed with an error
          When the report derives checks
          Then the step failure and error remain visible
          And the build result is not changed
        """
        snapshot = {"builds": [{"id": 101, "build": {"result": "succeeded"}, "timeline": {"records": [
            {"id": "optional-check", "name": "Optional integration", "result": "failed", "issues": [
                {"type": "error", "message": "Integration endpoint timed out."}]}]}}]}
        checks = release_checks(snapshot)
        self.assertEqual(len(checks), 1)
        self.assertEqual(checks[0]["severity"], "failed")
        self.assertIn("Optional integration", checks[0]["title"])
        self.assertEqual(checks[0]["reason"], "Integration endpoint timed out.")
        self.assertEqual(snapshot["builds"][0]["build"]["result"], "succeeded")


if __name__ == "__main__":
    unittest.main()
