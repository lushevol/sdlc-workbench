"""tda/result_store.py — Single accumulator replacing all module-level globals.

Instead of appending to bare lists at module scope, all collectors append to
the appropriate field on a ``ResultStore`` instance that is threaded through
every function.

``to_tda_output()`` assembles the final JSON dict that matches the shape
expected by the SKILL.md report generator.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ResultStore:
    # Release-level
    release_features:      list = field(default_factory=list)
    release_pt_features:   list = field(default_factory=list)
    regression_justification: list = field(default_factory=list)
    snow_features:         list = field(default_factory=list)
    snow_enabled:          bool = True
    pit_result:            list = field(default_factory=list)
    pit_content:           list = field(default_factory=list)
    aig_rollback_check:    list = field(default_factory=list)

    # WI-level
    story_features:        list = field(default_factory=list)
    bug_features:          list = field(default_factory=list)
    application_features:  list = field(default_factory=list)

    # Testing
    test_plan_features:    list = field(default_factory=list)
    test_result_features:  list = field(default_factory=list)
    test_case_details:     list = field(default_factory=list)
    testing_types:         list = field(default_factory=list)

    # Acceptance Testing PO-approval email evidence (best-effort, informational only)
    po_approval_evidence:  list = field(default_factory=list)

    # Coverage
    unit_tests:            list = field(default_factory=list)
    sonar_coverage:        list = field(default_factory=list)
    sonar_quality_gates:   list = field(default_factory=list)
    sonar_quality_gate_statuses: list = field(default_factory=list)
    sonar_exclusions:      list = field(default_factory=list)
    sonar_new_code_periods: list = field(default_factory=list)
    sonar_skipped:         bool = False
    sonar_skip_reason:     str = ''

    # Genie
    genie_count:           list = field(default_factory=list)
    genie_failures:        list = field(default_factory=list)
    genie_tag_split:       list = field(default_factory=list)
    genie_story_tag_split: list = field(default_factory=list)
    genie_story_type_breakdown: list = field(default_factory=list)

    # Traceability
    traceability:          list = field(default_factory=list)
    unique_test_cases:     dict = field(default_factory=dict)

    # -----------------------------------------------------------------------
    def ingest_release_data(self, data: dict) -> None:
        """Bulk-import the dict returned by collect_release_data()."""
        self.release_features.extend(data.get('release', []))
        self.release_pt_features.extend(data.get('release_pt', []))
        self.regression_justification.extend(data.get('regression_justification', []))
        self.testing_types.extend(data.get('testing_types', []))
        self.snow_features.extend(data.get('snow', []))
        self.snow_enabled = data.get('snow_enabled', True)
        self.pit_result.extend(data.get('pit_result', []))
        self.pit_content.extend(data.get('pit_content', []))
        self.aig_rollback_check.extend(data.get('aig_rollback_check', []))
        self.unit_tests.extend(data.get('unit_tests', []))
        self.sonar_coverage.extend(data.get('sonar', []))
        self.sonar_quality_gates.extend(data.get('sonar_quality_gates', []))
        self.sonar_quality_gate_statuses.extend(data.get('sonar_quality_gate_statuses', []))
        self.sonar_exclusions.extend(data.get('sonar_exclusions', []))
        self.sonar_new_code_periods.extend(data.get('sonar_new_code_periods', []))
        if data.get('sonar_skipped'):
            self.sonar_skipped = True
            self.sonar_skip_reason = data.get('sonar_skip_reason', '')
        self.genie_count.extend(data.get('genie_count', []))
        self.genie_failures.extend(data.get('genie_failures', []))
        self.genie_tag_split.extend(data.get('genie_tags', []))
        self.genie_story_tag_split.extend(data.get('genie_story_tags', []))
        self.genie_story_type_breakdown.extend(data.get('genie_story_type_breakdown', []))

    def ingest_traceability(self, rows: list, unique_tcs: dict) -> None:
        self.traceability.extend(rows)
        for tc_id, tc_data in unique_tcs.items():
            if tc_id not in self.unique_test_cases:
                self.unique_test_cases[tc_id] = tc_data
            else:
                for wi_id in tc_data.get('Linked WIs', []):
                    if wi_id not in self.unique_test_cases[tc_id]['Linked WIs']:
                        self.unique_test_cases[tc_id]['Linked WIs'].append(wi_id)

    # -----------------------------------------------------------------------
    def to_tda_output(self,
                       release_id: str,
                       release_stream: str,
                       blade_release_builds: dict,
                       pipeline_versions: dict | None = None,
                       collector_version: str | None = None,
                       ado_organization: str | None = None,
                       ado_project: str | None = None) -> dict:
        """Assemble the JSON structure expected by the SKILL.md report generator."""

        # Check 3: Token coverage ratio — unique test cases vs. stories in scope.
        # A very low ratio (e.g. 1 TC shared across 38 stories) indicates nominal
        # test coverage that satisfies the per-story link check but provides no
        # real traceability depth.  Flagged as SPARSE for SKILL awareness.
        story_count    = len(self.story_features)
        unique_tc_count = len(self.unique_test_cases)
        if story_count > 0:
            coverage_ratio = round(unique_tc_count / story_count, 2)
            if unique_tc_count == 0:
                coverage_ratio_check = 'NO_TEST_CASES'
            elif coverage_ratio < 0.25:
                coverage_ratio_check = 'SPARSE'        # fewer than 1 TC per 4 stories
            elif coverage_ratio < 0.75:
                coverage_ratio_check = 'THIN'          # between 1:4 and 3:4
            else:
                coverage_ratio_check = 'OK'
        else:
            coverage_ratio       = None
            coverage_ratio_check = 'NOT_ASSESSED'

        return {
            'release_id':           release_id,
            'release_stream':       release_stream,
            'collector_version':    collector_version or '',
            'ado_organization':     ado_organization or '',
            'ado_project':          ado_project or '',
            'blade_release_builds': blade_release_builds,
            'pipeline_versions':    pipeline_versions or {},

            # Step 3 — Release
            'release_features':     self.release_features,
            'release_pt_features':  self.release_pt_features,
            'regression_justification': self.regression_justification,
            'snow_features':        self.snow_features,
            'snow_enabled':         self.snow_enabled,
            'pit_result':           self.pit_result,
            'pit_content':          self.pit_content,
            'aig_rollback_check':   self.aig_rollback_check,
            'testing_types':        self.testing_types,
            'unit_tests':           self.unit_tests,
            'sonar_coverage':       self.sonar_coverage,
            'sonar_quality_gates':  self.sonar_quality_gates,
            'sonar_quality_gate_statuses': self.sonar_quality_gate_statuses,
            'sonar_exclusions':     self.sonar_exclusions,
            'sonar_new_code_periods': self.sonar_new_code_periods,
            'sonar_skipped':        self.sonar_skipped,
            'sonar_skip_reason':    self.sonar_skip_reason,
            'genie_count':          self.genie_count,
            'genie_failures':       self.genie_failures,
            'genie_tag_split':      self.genie_tag_split,
            'genie_story_tag_split': self.genie_story_tag_split,
            'genie_story_type_breakdown': self.genie_story_type_breakdown,

            # Step 4 — WI-level
            'story_features':       self.story_features,
            'bug_features':         self.bug_features,
            'application_features': self.application_features,
            'test_plan_features':   self.test_plan_features,
            'test_result_features': self.test_result_features,
            'test_case_details':    self.test_case_details,
            'po_approval_evidence': self.po_approval_evidence,

            # Step 5 — Traceability
            'traceability':         self.traceability,
            'unique_test_cases':    list(self.unique_test_cases.values()),

            # Check 3 — token coverage ratio
            'coverage_ratio_check': {
                'story_count':        story_count,
                'unique_tc_count':    unique_tc_count,
                'coverage_ratio':     coverage_ratio,
                'check':              coverage_ratio_check,
            },
        }
