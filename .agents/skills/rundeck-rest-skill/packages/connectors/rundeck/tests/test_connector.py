import io
import sys
import unittest
from http.cookiejar import Cookie
from pathlib import Path
from unittest.mock import patch

CONNECTOR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CONNECTOR))
from client import RundeckClient, SafeRedirectHandler, AuthenticationError
from policy import Policy, PolicyError
from sanitize import scrub, scrub_text
from rdk import parse_job_options, filter_projects, bounded, execution_summary

JOB = "11111111-1111-4111-8111-111111111111"

class ConnectorTest(unittest.TestCase):
    def test_login_posts_form_and_keeps_cookie(self):
        client = RundeckClient("https://rundeck.internal/rundeck", "alice")
        captured = {}
        class FakeResponse:
            status = 200
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def geturl(self): return "https://rundeck.internal/rundeck/menu"
        class FakeOpener:
            def open(self, req, timeout):
                captured["url"] = req.full_url
                captured["data"] = req.data
                return FakeResponse()
        cookie = Cookie(version=0, name="JSESSIONID", value="session", port=None,
                        port_specified=False, domain="rundeck.internal", domain_specified=False,
                        domain_initial_dot=False, path="/rundeck", path_specified=True,
                        secure=True, expires=None, discard=True, comment=None,
                        comment_url=None, rest={}, rfc2109=False)
        client.cookies.set_cookie(cookie)
        client.http = FakeOpener()
        client.login("an-example-password")
        self.assertTrue(captured["url"].endswith("/rundeck/j_security_check"))
        self.assertIn(b"j_username=alice", captured["data"])
        self.assertIn(b"j_password=an-example-password", captured["data"])
        self.assertNotIn("an-example-password", captured["url"])

    def test_login_rejects_missing_cookie(self):
        client = RundeckClient("https://rundeck.internal", "alice")
        class FakeResponse:
            status = 200
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def geturl(self): return "https://rundeck.internal/menu"
        class FakeOpener:
            def open(self, req, timeout): return FakeResponse()
        client.http = FakeOpener()
        with self.assertRaises(AuthenticationError):
            client.login("pw")

    def test_https_required(self):
        with self.assertRaises(ValueError):
            RundeckClient("http://rundeck.internal", "user")

    def test_reject_credentials_in_url(self):
        with self.assertRaises(ValueError):
            RundeckClient("https://u:p@rundeck.internal", "user")

    def test_context_path(self):
        client = RundeckClient("https://rundeck.internal/rundeck", "user")
        self.assertEqual(client.base_url, "https://rundeck.internal/rundeck")

    def test_url_path_encodes_project(self):
        self.assertEqual(RundeckClient._project("Ops Team"), "Ops%20Team")
        with self.assertRaises(ValueError):
            RundeckClient._project("../admin")

    def test_validation(self):
        self.assertEqual(RundeckClient._job_id(JOB), JOB)
        with self.assertRaises(ValueError):
            RundeckClient._job_id("../../admin")
        with self.assertRaises(ValueError):
            RundeckClient._execution_id("1/abort")

    def test_redirect_other_domain(self):
        redirect = SafeRedirectHandler("https://rundeck.internal/rundeck")
        from urllib.request import Request
        with self.assertRaises(AuthenticationError):
            redirect.redirect_request(Request("https://rundeck.internal/rundeck/j_security_check"), None,
                                      302, "Found", {}, "https://example.com/login")

    def test_redirect_login_page(self):
        redirect = SafeRedirectHandler("https://rundeck.internal")
        from urllib.request import Request
        with self.assertRaises(AuthenticationError):
            redirect.redirect_request(Request("https://rundeck.internal/j_security_check"), None,
                                      302, "Found", {}, "https://rundeck.internal/user/login")

    def test_redirect_escapes_context(self):
        redirect = SafeRedirectHandler("https://rundeck.internal/rundeck")
        from urllib.request import Request
        with self.assertRaises(AuthenticationError):
            redirect.redirect_request(Request("https://rundeck.internal/rundeck/j_security_check"), None,
                                      302, "Found", {}, "https://rundeck.internal/other/login")

    def test_read_only_default(self):
        policy = Policy.load()
        with self.assertRaises(PolicyError):
            policy.check_execution("Ops", JOB, {})
        with self.assertRaises(PolicyError):
            policy.check_definition()

    def test_execution_policy(self):
        policy = Policy({"enable_job_execution": True,
                         "allowed_projects": ["DEV"],
                         "executable_jobs": {JOB: {"project": "DEV", "allowed_options": ["target"]}}})
        policy.check_execution("DEV", JOB, {"target": "vm01"})
        with self.assertRaises(PolicyError):
            policy.check_execution("PROD", JOB, {})
        with self.assertRaises(PolicyError):
            policy.check_execution("DEV", JOB, {"secret": "abc"})

    def test_output_redaction(self):
        result = scrub({"password": "leak", "normal": "Authorization: abc123", "nested": {"api_token": "evil"}})
        self.assertEqual(result["password"], "[REDACTED]")
        self.assertEqual(result["nested"]["api_token"], "[REDACTED]")
        self.assertIn("[REDACTED]", result["normal"])

    def test_bearer_redaction(self):
        self.assertNotIn("superlongtoken", scrub_text("Authorization=Bearer superlongtoken"))

    def test_option_parsing(self):
        self.assertEqual(parse_job_options(["target=dev", "mode=dry-run"]),
                         {"target": "dev", "mode": "dry-run"})
        with self.assertRaises(ValueError):
            parse_job_options(["password=abc"])
        with self.assertRaises(ValueError):
            parse_job_options(["a=1", "a=2"])

    def test_project_filter(self):
        policy = Policy({"allowed_projects": ["DEV"]})
        self.assertEqual(len(filter_projects([{"name": "DEV"}, {"name": "PROD"}], policy, 50)), 1)

    def test_execution_summary_excludes_args(self):
        self.assertNotIn("argstring", execution_summary({"id": 1, "argstring": "--password ABC"}))

    def test_response_restricted(self):
        with self.assertRaises(ValueError):
            bounded(201, 200)
        with self.assertRaises(PolicyError):
            Policy({"max_response_bytes": 99999999}).max_response_bytes()


if __name__ == "__main__":
    unittest.main()
