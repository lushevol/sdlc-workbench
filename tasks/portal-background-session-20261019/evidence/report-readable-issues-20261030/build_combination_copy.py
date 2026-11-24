#!/usr/bin/env python3
"""Build editorial copy from retained results; do not execute or change outcomes."""
import hashlib
import json
import re
from pathlib import Path

TASK = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = TASK / 'evidence/report-impact-priority-20261029/case-priority-audit.json'
AUDIT = json.loads(SOURCE.read_text())
ROWS = [row for row in AUDIT['rows'] if row['id'].startswith('RN-C')]
FIELDS = ['id', 'title', 'what_happened', 'reason', 'user_impact', 'missing_check',
          'priority_reason', 'next_action', 'limits', 'owner']

TRIGGER_TITLE = {
    'manual': 'Manual renewal',
    'activity': 'Activity renewal',
    'refresh-acquisition': 'Request for a renewal credential',
}
TRIGGER = {
    'manual': 'The test requested manual sign-in renewal',
    'activity': 'The test called the function that renews sign-in after activity',
    'refresh-acquisition': 'The test requested a replacement credential for future sign-in renewal',
}
LIFETIME = {
    60000: '60 seconds left', 25000: '25 seconds left',
    24999: 'just under 25 seconds left', 0: 'expired access',
}
RESPONSE_TITLE = {
    'usable': 'valid reply', 'rejected': 'server rejection',
    'timeout': 'timeout', 'malformed': 'invalid reply',
}
RESPONSE = {
    'usable': 'The test returned a valid renewal reply.',
    'rejected': 'The test returned a server error for the renewal request.',
    'timeout': 'The test made the renewal request time out.',
    'malformed': 'The test returned an unreadable credential in the renewal reply.',
}
OWNERSHIP = {
    'unchanged-A': 'same user', 'logout-A': 'sign out',
    'replace-with-B': 'switch to another user',
}
TRANSPORT = {
    'stomp': 'STOMP messaging', 'sse': 'server-sent events',
    'graphql-websocket': 'GraphQL over WebSocket', 'http': 'HTTP',
    'long-poll': 'long polling', 'file-transfer': 'file transfer',
}
LIFECYCLE = {
    'visible': 'a visible page',
    'hidden-after-start': 'hiding the page after renewal starts',
    'resume-before-delivery': 'resuming the page before the reply',
    'unmount-after-start': 'removing the page components before the reply',
}


def make_copy(row, result):
    inputs = result['inputs']
    count = result['guard_observation']['accepted_renewal_requests']
    ownership = inputs['ownership']
    is_pair = inputs['outline'] == 'RN-C001'
    unreadable = result['final']['unreadable_access']
    lifetime = LIFETIME[int(inputs['access_ms'])]
    title = ' · '.join((TRIGGER_TITLE[inputs['trigger']], lifetime,
                        RESPONSE_TITLE[inputs['response']], OWNERSHIP[ownership]))
    if int(inputs['access_ms']):
        start = f"{TRIGGER[inputs['trigger']]} with {lifetime} before access expired."
    else:
        start = f"{TRIGGER[inputs['trigger']]} after access expired."
    sentences = [start]
    if count:
        if ownership == 'logout-A':
            sentences.append('The test signed out before returning the old renewal reply.')
        elif ownership == 'replace-with-B':
            sentences.append('The test signed in as another user before returning the old renewal reply.')
        sentences.append(RESPONSE[inputs['response']])
    else:
        sentences.append('The app sent no renewal request, so the selected reply was never delivered.')
        if ownership == 'logout-A':
            sentences.append('The test then signed out.')
        elif ownership == 'replace-with-B':
            sentences.append('The test then signed in as another user.')
    subject = result['final']['subject']
    if ownership != 'unchanged-A':
        assert subject == ('B' if ownership == 'replace-with-B' else None)
        if count:
            sentences.append('The old reply changed none of the current sign-in details.')
        else:
            sentences.append('No old renewal reply was available to challenge the new sign-in state.')
        sentences.append('The second user remained signed in.' if subject == 'B' else 'The app remained signed out.')
    elif unreadable:
        assert subject == 'UNREADABLE'
        sentences.append('The app stored a sign-in credential it could not read.')
    else:
        assert subject == 'A'
        sentences.append('The stored sign-in credential still identified the first user.')
    what_happened = ' '.join(sentences)
    reason = ('The test did not connect to a real service that saves business data. '
              'It therefore could not check whether the server permits each save.')
    impact = ('No forced sign-out, interrupted work, or data loss was demonstrated. '
              'Permission checks for real business saves remain unverified.')
    missing = 'Check that only permitted users can save data through a real business service.'
    next_action = 'Select a real business save. Record its server permission checks and saved results for this case.'
    priority_reason = ('Missing test evidence does not establish a user failure. '
                       'This remains P3 follow-up without a separate release hold.')
    limits = 'The test used simulated server replies and time, without a real sign-in provider or business service.'
    if inputs['trigger'] == 'activity':
        limits += ' It called a renewal function directly instead of generating mouse or keyboard activity.'
    if ownership == 'unchanged-A':
        limits += ' The completed assertion only checked for replies from a different session.'
    if unreadable:
        reason = ('The completed assertion checked session ownership. '
                  'It did not check whether the returned sign-in credential was readable. '
                  'The test also lacked a real service that saves business data.')
        impact = ('An unreadable sign-in credential could prevent later authenticated requests. '
                  'No later request, session interruption, or real-provider occurrence was checked.')
        missing += ' Check later authenticated requests after an unreadable renewal reply.'
        next_action = ('Test later authenticated requests after an unreadable reply. '
                       'Check whether the real provider can produce this response. '
                       'Then check a real business save.')
        priority_reason = ('The test observed an unreadable credential, but did not demonstrate an interrupted session or unusable app. '
                           'This remains P3 follow-up.')
    if is_pair:
        missing += ' Confirm each requested save occurs once.'
        missing += f" Run {TRANSPORT[inputs['transport']]} with the planned network and page conditions."
        next_action += ' Record unique save identifiers and server save counts. Repeat the planned connection and page conditions.'
        limits += (f" Planned conditions included {TRANSPORT[inputs['transport']]} and {LIFECYCLE[inputs['lifecycle']]}. "
                   'The test did not run the actual connection or native browser schedule.')
        if inputs.get('refresh') == 'revoked':
            limits += ' The test used a valid credential, so it did not check rejection of credentials cancelled by the server.'
    return dict(zip(FIELDS, [row['id'], title, what_happened, reason, impact, missing,
                             priority_reason, next_action, limits, 'Unknown business-service and test owners.']))


copies = []
unreadable_ids = []
for row in ROWS:
    data = (TASK / row['result']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == row['result_sha256'], row['id']
    result = json.loads(data)
    assert row['status'] == result['execution_status'] == 'PARTIALLY_EXECUTED', row['id']
    assert row['new_priority'] == 'P3' and row['release_blocking'] is False, row['id']
    assert result['bounded_execution']['status'] == 'PASSED', row['id']
    assert all(item['status'] == 'PASSED' for item in result['assertions']), row['id']
    copies.append(make_copy(row, result))
    if result['final']['unreadable_access']:
        unreadable_ids.append(row['id'])

assert len(copies) == 181
assert len({row['id'] for row in copies}) == 181
assert unreadable_ids == ['RN-C002/RISK-106', 'RN-C002/RISK-118']
long_sentences = []
for row in copies:
    assert list(row) == FIELDS
    for field in FIELDS[2:]:
        for sentence in re.split(r'(?<=[.!?])\s+', row[field]):
            count = len(sentence.split())
            if count > 20:
                long_sentences.append({'id': row['id'], 'field': field, 'words': count, 'text': sentence})
assert not long_sentences, long_sentences
output = HERE / 'combination-copy.json'
output.write_text(json.dumps(copies, indent=2, ensure_ascii=False) + '\n')
validation = {
    'scope': 'Editorial rewrite of 181 partial combination cases only. No application execution or disposition changes.',
    'rows': len(copies),
    'source_hashes_verified': len(copies),
    'partial_statuses_preserved': len(copies),
    'P3_nonblocking_dispositions_preserved': len(copies),
    'unreadable_credential_observations': unreadable_ids,
    'sentences_over_20_words': 0,
    'source_audit': str(SOURCE.relative_to(TASK)),
    'source_audit_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'writing_review': {
        'standard': 'ASD-STE100', 'automated_check': 'PASSED',
        'asd_review': 'PENDING', 'reviewer': None, 'reviewed_at': None,
        'limitations': ['Automated checks do not check the complete approved dictionary or grammar rules.'],
    },
}
(HERE / 'combination-copy-validation.json').write_text(json.dumps(validation, indent=2) + '\n')
print(json.dumps(validation, indent=2))
