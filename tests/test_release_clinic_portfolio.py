"""Check portfolio day filters against retained service registry timestamps."""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest


SERVICE = Path(__file__).resolve().parents[1] / "core/release-clinic/plugins/test/dtp-tda-service"
SCRIPT = SERVICE / "scripts/aggregate_portfolio.py"


class ReleaseClinicPortfolioDatesTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="release-clinic-portfolio-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.registry = self.root / "registry.jsonl"
        self.environment = {**os.environ, "AI_SDLC_WORKSPACE": str(self.root)}
        self.environment.pop("AI_SDLC_ENV_FILE", None)
        self.build_record = runpy.run_path(str(SERVICE / "service/registry.py"))["build_success_record"]

    def record(self, release, timestamp):
        completed = datetime.fromisoformat(timestamp)
        return self.build_record(
            f"job-{release}", SimpleNamespace(release_id=release, stream="EXAMPLE"), {},
            completed, completed, completed, f"{release}.json",
        )

    def run_portfolio(self, *arguments):
        return subprocess.run(
            [sys.executable, "-S", str(SCRIPT), "--registry", str(self.registry), *arguments],
            cwd=self.root, env=self.environment, capture_output=True, text=True,
        )

    def test_utc_registry_records_respect_both_inclusive_day_boundaries(self):
        records = [
            self.record("before", "2026-10-16T23:59:59.999999+00:00"),
            self.record("start", "2026-10-17T00:00:00+00:00"),
            self.record("end", "2026-10-18T23:59:59.999999+00:00"),
            self.record("offset-inside", "2026-10-19T00:30:00+01:00"),
            self.record("after", "2026-10-19T00:00:00+00:00"),
        ]
        original = "".join(json.dumps(record) + "\n" for record in records).encode()
        self.registry.write_bytes(original)
        result = self.run_portfolio("--since", "2026-10-17", "--until", "2026-10-18")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["meta"]["total_records_before_filter"], 5)
        self.assertEqual(data["summary"]["total_jobs"], 3)
        self.assertEqual(data["per_stream"]["EXAMPLE"]["releases_covered"], ["end", "offset-inside", "start"])
        self.assertEqual(data["meta"]["filters"]["since"], "2026-10-17")
        self.assertEqual(data["meta"]["filters"]["until"], "2026-10-18")
        self.assertEqual(self.registry.read_bytes(), original)

    def test_invalid_and_reversed_dates_fail_before_reading_registry(self):
        cases = (
            ("--since", "2026-02-30"),
            ("--until", "invalid"),
            ("--since", "2026-1-1"),
            ("--since", "2026-10-19", "--until", "2026-10-18"),
        )
        for arguments in cases:
            with self.subTest(arguments=arguments):
                result = self.run_portfolio(*arguments)
                self.assertEqual(result.returncode, 2)
                self.assertIn("error:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertNotIn("Registry file not found", result.stderr)
                self.assertEqual(result.stdout, "")

    def test_timestamp_parser_normalizes_legacy_and_utc_z_records(self):
        parse = runpy.run_path(str(SCRIPT))["_parse_dt"]
        expected = datetime(2026, 10, 18, tzinfo=timezone.utc)
        self.assertEqual(parse("2026-10-18T00:00:00"), expected)
        self.assertEqual(parse("2026-10-18T00:00:00Z"), expected)


if __name__ == "__main__":
    unittest.main()
