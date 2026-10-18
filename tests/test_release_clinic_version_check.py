"""Check that canonical skill update requests require explicit opt-in."""

import importlib.util
import io
import os
from pathlib import Path
import unittest
from contextlib import redirect_stdout
from unittest.mock import Mock, patch


VERSION_CHECK = (
    Path(__file__).resolve().parents[1]
    / "core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts/tda/version_check.py"
)
_SPEC = importlib.util.spec_from_file_location("release_clinic_version_check_test", VERSION_CHECK)
version_check = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(version_check)


class SkillUpdateOptInTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ, {}, clear=True)
        environment.start()
        self.addCleanup(environment.stop)
        self.client = Mock(spec=["get_remote_skill_version"])

    def test_default_skips_remote_calls_and_preserves_result_contract(self):
        with patch.object(version_check, "read_local_skill_version", return_value="1.2.3"):
            result = version_check.check_skill_staleness(self.client)

        self.client.get_remote_skill_version.assert_not_called()
        self.assertEqual(set(result), {
            "local_version", "latest_stable_version", "source_repo", "source_branch",
            "is_outdated", "checked_at", "check_error",
        })
        self.assertEqual(result["local_version"], "1.2.3")
        self.assertIsNone(result["latest_stable_version"])
        self.assertFalse(result["is_outdated"])
        self.assertIn("TDA_CHECK_SKILL_UPDATES=true", result["check_error"])

        output = io.StringIO()
        with redirect_stdout(output), patch("builtins.input") as prompt:
            version_check.print_staleness_banner(result)
            version_check.confirm_staleness_or_exit(result)
        prompt.assert_not_called()
        self.assertIn("Skipped: Disabled.", output.getvalue())
        self.assertNotIn("up to date", output.getvalue())

    def test_false_or_other_values_do_not_enable_remote_requests(self):
        for value in ("false", "", "1", "yes"):
            with self.subTest(value=value), patch.dict(os.environ, {"TDA_CHECK_SKILL_UPDATES": value}):
                result = version_check.check_skill_staleness(self.client, local_version="1.2.3")
                self.assertIsNotNone(result["check_error"])
                self.client.get_remote_skill_version.assert_not_called()

    def test_true_enables_mocked_remote_comparison(self):
        self.client.get_remote_skill_version.return_value = "1.3.0"
        with patch.dict(os.environ, {"TDA_CHECK_SKILL_UPDATES": "true"}):
            result = version_check.check_skill_staleness(self.client, local_version="1.2.3")

        self.client.get_remote_skill_version.assert_called_once_with(
            org=version_check.CANONICAL_ORG,
            project=version_check.CANONICAL_PROJECT,
            repo=version_check.CANONICAL_REPO,
            path=version_check.CANONICAL_PATH,
            branch=version_check.CANONICAL_BRANCH,
        )
        self.assertEqual(result["latest_stable_version"], "1.3.0")
        self.assertTrue(result["is_outdated"])
        self.assertIsNone(result["check_error"])

    def test_enabled_failure_remains_nonblocking(self):
        self.client.get_remote_skill_version.side_effect = RuntimeError("Access unavailable")
        with patch.dict(os.environ, {"TDA_CHECK_SKILL_UPDATES": "true"}):
            result = version_check.check_skill_staleness(self.client, local_version="1.2.3")

        self.client.get_remote_skill_version.assert_called_once()
        self.assertIsNone(result["latest_stable_version"])
        self.assertFalse(result["is_outdated"])
        self.assertEqual(result["check_error"], "Access unavailable")


if __name__ == "__main__":
    unittest.main()
