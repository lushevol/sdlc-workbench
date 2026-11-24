"""Keep portal policy corrections from erasing implementation/test evidence."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PortalKnowledgeBoundaryTests(unittest.TestCase):
    def read(self, relative):
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_session_fixture_is_removed_from_policy_but_retained_as_evidence(self):
        requirement = self.read("knowledge/records/candidates/requirements/REQ-active-session-renewal.md")
        criteria = requirement.split("## Acceptance criteria", 1)[1].split("Owner:", 1)[0]
        for fixture in ("100 milliseconds", "15 seconds", "30 seconds"):
            self.assertNotIn(fixture, criteria)

        mfe = self.read("knowledge/llm-wiki/wiki/entities/mfe-base.md")
        evidence = mfe.split("### Retained implementation evidence", 1)[1].split("## CES migration compatibility", 1)[0]
        self.assertIn("setTimeout(runExtend, 5000)", evidence)
        self.assertIn("every 100 milliseconds for a 15-second observation window", evidence)
        self.assertIn("implementation and test-observation facts", evidence)
        self.assertIn("does not establish current deployment behavior", evidence)

    def test_related_evidence_overstatements_remain_qualified(self):
        ems3 = self.read("knowledge/llm-wiki/wiki/entities/ems3.md")
        self.assertIn("no universal Auth Server call path", ems3)
        self.assertIn("no implementation evidence", ems3)

        jmeter = self.read("knowledge/llm-wiki/wiki/entities/apache-jmeter.md")
        self.assertIn("500 users, a 250-second ramp-up, and five iterations", jmeter)
        self.assertIn("executable plan, result archive, direct assertions", jmeter)

        graphql = self.read("knowledge/llm-wiki/wiki/entities/graphql.md")
        self.assertIn("no retained execution establishes measured performance", graphql)
        self.assertIn("no accepted notification decision, supported code revision, or execution evidence", graphql)


if __name__ == "__main__":
    unittest.main()
