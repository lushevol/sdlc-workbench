"""Keep audit outputs in the selected workspace without optional dependencies."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


AUDIT = (Path(__file__).resolve().parents[1] / "core/release-clinic/plugins/test/dtp-tda-report"
         / "skills/dtp-tda-report/scripts/tda_audit")


class ReleaseClinicAuditPathsTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="release-clinic-audit-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.cwd = self.root / "nested"
        self.cwd.mkdir()
        self.environment = {**os.environ, "AI_SDLC_WORKSPACE": str(self.root)}
        for key in ("AI_SDLC_ENV_FILE", "TDA_OUTPUT_DIR"):
            self.environment.pop(key, None)

    def test_help_requires_neither_optional_dependencies_nor_environment_file(self):
        environment = {**self.environment, "AI_SDLC_ENV_FILE": "missing.env"}
        for script in ("run_tda_audit.py", "rwi_tda_presence_check.py"):
            with self.subTest(script=script):
                result = subprocess.run(
                    [sys.executable, "-S", str(AUDIT / script), "--help"],
                    cwd=self.cwd, env=environment, capture_output=True, text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("TDA_OUTPUT_DIR/audit/", result.stdout)
        self.assertEqual(list(self.cwd.iterdir()), [])

    def test_offline_extraction_uses_configured_root_outputs_from_nested_cwd(self):
        (self.root / ".env").write_text("TDA_OUTPUT_DIR=custom/reports\n", encoding="utf-8")
        (self.cwd / ".env").write_text("TDA_OUTPUT_DIR=wrong\n", encoding="utf-8")
        attachments = self.root / "custom/reports/audit/attachments"
        attachments.mkdir(parents=True)
        original = b'<html><div class="verdict pass">PASS</div></html>'
        source = attachments / "TDAReport_EXAMPLE_123.html"
        source.write_bytes(original)
        result = subprocess.run(
            [sys.executable, "-S", str(AUDIT / "run_tda_audit.py"), "--skip-download"],
            cwd=self.cwd, env=self.environment, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        output = self.root / "custom/reports/audit/findings/TDAFindings_EXAMPLE_123.json"
        findings = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual((findings["stream"], findings["release_id"], findings["verdict"]),
                         ("EXAMPLE", "123", "PASS"))
        self.assertEqual(source.read_bytes(), original)
        self.assertFalse((self.cwd / "wrong").exists())

    def test_presence_report_defaults_and_overrides_resolve_from_workspace(self):
        probe = r'''
import runpy
import sys
import types

config = types.ModuleType('tda.config')
config.load_env_file = lambda: None
config.Config = types.SimpleNamespace(from_env=lambda: types.SimpleNamespace(
    ado_organization='example-org', ado_project='example-project'))
client = types.ModuleType('tda.http_client')
client.ADOClient = lambda cfg: object()
sys.modules.update({'tda': types.ModuleType('tda'), 'tda.config': config, 'tda.http_client': client})
namespace = runpy.run_path(sys.argv[1])
main = namespace['main']
main.__globals__['_fetch_rwis_by_query'] = lambda *args, **kwargs: ['123']
main.__globals__['_get_work_item'] = lambda *args: {'fields': {'System.Title': 'Example release'}}
sys.argv = [sys.argv[1], *sys.argv[2:]]
main()
'''
        cases = (
            ([], ".workbench/release-clinic/reports/audit/RWITDAPresenceReport.html", ""),
            ([], "custom/reports/audit/RWITDAPresenceReport.html", "TDA_OUTPUT_DIR=custom/reports\n"),
            (["--output", "explicit/report.html"], "explicit/report.html", ""),
        )
        for arguments, relative, settings in cases:
            with self.subTest(arguments=arguments, settings=settings):
                (self.root / ".env").write_text(settings, encoding="utf-8")
                result = subprocess.run(
                    [sys.executable, "-S", "-c", probe, str(AUDIT / "rwi_tda_presence_check.py"), *arguments],
                    cwd=self.cwd, env=self.environment, capture_output=True, text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                report = self.root / relative
                self.assertIn("Example release", report.read_text(encoding="utf-8"))
                self.assertFalse((self.cwd / relative).exists())


if __name__ == "__main__":
    unittest.main()
