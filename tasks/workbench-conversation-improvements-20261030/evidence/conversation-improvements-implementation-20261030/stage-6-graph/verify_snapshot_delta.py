"""Verify unchanged and current-source comparisons using two real validated bundles."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

from ai_sdlc_workbench.relationships.skill import load_graph_tool

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
BASELINE = ROOT / 'relationships/service-dependencies/generated'
CANDIDATE = ROOT / '.workbench/conversation-graph-source-20261030'


def retain(name, result, checks):
    result['verification'] = {'case_id': name, 'recorded_at': datetime.now(timezone.utc).isoformat(),
                             'assertions': checks, 'assertions_passed': all(checks.values())}
    (HERE / f'{name}.json').write_text(json.dumps(result, indent=2) + '\n')
    assert all(checks.values())
    print(json.dumps({'case': name, 'passed': True, 'counts': result['counts'],
                      'affected_consumers': len(result['affected_consumers']),
                      'requires_reinvestigation': len(result['requires_reinvestigation'])}), flush=True)


def main():
    module = load_graph_tool('snapshot_delta', ROOT)
    result = module.compare_snapshots(BASELINE, BASELINE, ROOT)
    retain('GRAPH-REAL-002-unchanged', result, {
        'same_saved_graph_is_unchanged': result['comparison'] == 'UNCHANGED',
        'no_false_deltas': all(value == 0 for counts in result['counts'].values() for value in counts.values()),
        'current_source_staleness_remains_visible': result['baseline']['current_freshness']['status'] == 'STALE',
        'uncaptured_instruction_identity_stays_unknown': result['baseline']['initial_instruction_freshness']['status'] == 'UNKNOWN',
        'stale_claims_require_reinvestigation': bool(result['requires_reinvestigation']),
        'no_affected_consumers_from_no_delta': not result['affected_consumers']})
    result = module.compare_snapshots(BASELINE, CANDIDATE, ROOT)
    retain('GRAPH-REAL-003-current-source-delta', result, {
        'real_saved_graphs_differ': result['comparison'] == 'CHANGED',
        'candidate_sources_are_current': result['candidate']['current_freshness']['status'] == 'CURRENT',
        'old_graph_preserved': hashlib.sha256((BASELINE / 'graph.json').read_bytes()).hexdigest() == result['baseline']['graph_sha256'],
        'two_source_repositories_changed': len(result['changes']['source_inventory']['changed']) == 2,
        'coverage_scope_changes_are_separate': len(result['changes']['repositories']['changed']) == 8,
        'real_edge_additions_exist': result['counts']['edges']['added'] > 0,
        'direct_static_consumers_exist': bool(result['affected_consumers']),
        'context_omission_is_explicit': result['architecture_context_scope_changed'] and result['claim_removal_interpretation'] == 'CONTEXT_SCOPE_DIFFERENCE',
        'unsupported_links_remain_unavailable': result['contract_case_link_status'] == 'UNAVAILABLE_IN_SNAPSHOT'})
    receipt = {'recorded_at': datetime.now(timezone.utc).isoformat(),
        'command': '.venv/bin/python docs/evidence/conversation-improvements-implementation-20261030/stage-6-graph/verify_snapshot_delta.py',
        'source_sha256': {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in [
            ROOT / '.agents/skills/service-dependencies-graph/tools/snapshot_delta.py',
            ROOT / '.agents/skills/service-dependencies-graph/tests/test_snapshot_delta.py', Path(__file__)]},
        'assertions_passed': True, 'network_used': False, 'business_behavior_executed': False}
    (HERE / 'verification-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')


if __name__ == '__main__':
    main()
