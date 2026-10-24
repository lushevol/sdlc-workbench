"""Verify local report configuration without external services."""

import os
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

from ai_sdlc_workbench.release_report import _Collector


class ReleaseReportConfigurationTests(unittest.TestCase):
    def test_empty_process_value_overrides_root_clinic_output_setting(self):
        """
        Scenario: Apply process configuration before root file configuration
          Given the root file selects a custom Clinic output directory
          And the process sets TDA_OUTPUT_DIR to an empty string
          When the collector discovers Clinic links for release 501
          Then it links the default directory report
          And it does not link the custom directory report
          And no Clinic file changes
        """
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".env").write_text('export TDA_OUTPUT_DIR="custom" # local setting\n', encoding="utf-8")
            custom = root / "custom/TDAReport_CUSTOM_501.html"
            default = root / ".workbench/release-clinic/reports/TDAReport_DEFAULT_501.html"
            for path in (custom, default):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"<p>Separate Clinic fixture</p>")
            before = {path: path.read_bytes() for path in (custom, default)}
            collector = SimpleNamespace(workspace=root, release_id=501)
            with patch.dict(os.environ, {"TDA_OUTPUT_DIR": ""}, clear=True):
                links = _Collector.clinic(collector, {"relations": []})
            self.assertEqual(links["status"], "available")
            self.assertEqual([link["name"] for link in links["links"]], [default.name])
            self.assertEqual({path: path.read_bytes() for path in (custom, default)}, before)


if __name__ == "__main__":
    unittest.main()
