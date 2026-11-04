"""Inspect retained API bodies. Emit no request headers or credentials."""
import collections
import hashlib
import json
from pathlib import Path
import subprocess
import yaml

ROOT = Path(__file__).resolve().parents[4]
API = ROOT / 'tasks/ces-entitlement-migration-20261102/api'
OUT = Path(__file__).parent
SDK = ROOT / 'repos/libraries/single-ui-sdk-starter'
REVISION = 'fd9a157e260850b6d9efa10da3223950ea61133a'

def body(path):
    document = yaml.safe_load(path.read_text())
    return json.loads(document['examples'][0]['response']['body']['data'])

catalog_path = API / 'EMS3-user entitlements by application.yml'
catalog = body(catalog_path)
by_role = {row['entitlement_name']: row for row in catalog}
comparisons = []
for environment in ('PROD', 'UAT'):
    for path in sorted((API / environment).glob('*entitlementList*')):
        response = body(path)
        user = next(iter(response))
        groups = collections.defaultdict(list)
        for row in response[user]['entitlements']:
            groups[(row['role']['entity']['name'], row['role']['name'])].append(
                (row['subject']['name'], row['action']['name']))
        for (entity, role), rows in groups.items():
            expected = set(rows)
            target = by_role.get(role)
            observed = {(grant['feature'], grant['action']) for grant in target['role_entitlements']} if target else set()
            comparisons.append(dict(environment=environment, user=user, entity=entity, role=role,
                source=str(path.relative_to(ROOT)), source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                ems2_rows=len(rows), ems2_unique_pairs=len(expected), matched_pairs=len(expected & observed),
                missing_pairs=sorted(expected - observed), extra_pairs_in_same_ces_role=sorted(observed - expected),
                user_assigned_in_ces_catalog=user in target.get('user_ids', []) if target else False))

role_names = []
for environment in ('PROD', 'UAT'):
    path = API / environment / f'[{environment}] EMS2 subjects from entity id (X_RATANONE).yml'
    source = body(path)
    expected = {role['name'] for role in source['roles']}
    role_names.append(dict(environment=environment, source=str(path.relative_to(ROOT)),
        source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        response_kind='roles, despite subjects in filename', expected_count=len(expected),
        matching_name_count=len(expected & by_role.keys()), absent_names=sorted(expected - by_role.keys()),
        limitation='Name presence does not establish equal definitions or complete account assignments.'))

fixture_path='single-ui-sdk-starter/src/test/resources/ces-role-details.json'
fixture_bytes=subprocess.check_output(['git','-C',str(SDK),'show',f'{REVISION}:{fixture_path}'])
fixture=json.loads(fixture_bytes)
fixture_names={role['entitlementName']for role in fixture}
effective_path=API / 'EMS3-user entitlements by app and user (1481696).yml'
effective=body(effective_path)[0]
effective_names=set(effective['entitlements']['entitlement_name'])
prod=[r for r in comparisons if r['environment']=='PROD']
prod_tuples={(r['entity'],r['role'],s,a)for r in prod for s,a in
    {(g['feature'],g['action'])for g in by_role[r['role']]['role_entitlements']}}
result=dict(
    assessed_at='2026-11-04', mode='Offline retained sample inspection; no SDK execution and no live service calls',
    sdk_candidate=REVISION, sdk_baseline='b0aa82005e7f14202f85f5ef583f25e42da9eeb3',
    ces_catalog=dict(path=str(catalog_path.relative_to(ROOT)),sha256=hashlib.sha256(catalog_path.read_bytes()).hexdigest(),count=len(catalog)),
    prod_summary=dict(account_count=len({r['user']for r in prod}),entity_role_account_rows=len(prod),
        ems2_grant_rows=sum(r['ems2_rows']for r in prod),distinct_entity_role_subject_action_tuples=len(prod_tuples),
        matched_grant_rows=sum(r['matched_pairs']for r in prod),missing_grant_rows=sum(len(r['missing_pairs'])for r in prod),
        all_selected_roles_assigned=all(r['user_assigned_in_ces_catalog']for r in prod),
        limitation='Same-name entitlement definitions and catalog account assignments are indirect compatibility evidence. They do not exercise the SDK assigned-role endpoint.'),
    comparisons=comparisons, role_name_presence=role_names,
    candidate_fixture=dict(path=fixture_path,revision=REVISION,sha256=hashlib.sha256(fixture_bytes).hexdigest(),role_count=len(fixture),
        current_effective_source=str(effective_path.relative_to(ROOT)),current_effective_role_count=len(effective_names),
        roles_in_current_effective_sample_absent_from_candidate_fixture=sorted(effective_names-fixture_names),
        limitation='Different source times and endpoint shapes prevent treating the fixture difference as a current assigned-role endpoint defect.'),
    limits=['All comparisons use supplied snapshots, not synchronized live reads.',
        'The supplied API directory contains no assigned-role endpoint capture.',
        'No EMS2 account endpoint capture is supplied; grant rows alone cannot establish baseline complete output map.',
        'PROD EMS2 is compared with CES UAT; environment-specific policy differences remain visible.',
        'Global profile names and VIEW_ENTITLEMENT grants do not establish equal resolved data restrictions.',
        'All accounts and all role grant definitions are not supplied. The three account examples do not define the production population.'])
(OUT/'api-parity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result['prod_summary'],indent=2))

# Subject dictionary presence is separate from role-scoped grant equality.
ces_pairs={(grant['feature'],grant['action'])for row in catalog for grant in row['role_entitlements']}
ces_features={feature for feature,action in ces_pairs}
flow_path=API/'EMS3-user entitlements by application (FlowZero).yml'
flow_catalog=body(flow_path)
flow_pairs={(grant['feature'],grant['action'])for row in flow_catalog for grant in row['role_entitlements']}
subject_dictionaries=[]
grant_unions=[]
for environment in ('PROD','UAT'):
    for path in sorted((API/environment).glob('*subjects*')):
        response=body(path)
        kind='subjects' if 'subjects' in response else 'roles'
        rows=response[kind]
        names={row['name']for row in rows}
        matched=names & (ces_features if kind=='subjects' else by_role.keys())
        subject_dictionaries.append(dict(
            environment=environment,entity=path.stem.split('(')[-1].rstrip(')'),
            source=str(path.relative_to(ROOT)),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            response_kind=kind,declared_count=response['count'],retained_rows=len(rows),
            names=sorted(names),ces_same_name_matches=sorted(matched),absent_from_ratan_ces_catalog=sorted(names-matched),
            absent_from_both_ces_catalog_feature_unions=sorted(names-ces_features-{f for f,a in flow_pairs}) if kind=='subjects' else None,
            action_definitions_supplied=False,
            scope_limit='Presence checks use the configured RATAN application catalog. Matching names do not prove role grants or assignments.'))
    observed=collections.defaultdict(set)
    for path in sorted((API/environment).glob('*entitlementList*')):
        response=body(path)
        for row in next(iter(response.values()))['entitlements']:
            observed[row['subject']['entity']['name']].add((row['subject']['name'],row['action']['name']))
    for entity,pairs in sorted(observed.items()):
        grant_unions.append(dict(environment=environment,entity=entity,
            source_scope='Union of three retained account entitlement-list examples only',
            pair_count=len(pairs),subject_count=len({f for f,a in pairs}),action_count=len({a for f,a in pairs}),
            observed_subjects=sorted({f for f,a in pairs}),observed_actions=sorted({a for f,a in pairs}),
            matched_pair_count=len(pairs & ces_pairs),missing_pairs=sorted(pairs-ces_pairs),
            missing_in_both_ces_catalogs=sorted(pairs-ces_pairs-flow_pairs),
            limitation='Union presence does not prove correct role attribution or complete entity action coverage.'))
result['supplied_function_inventory']=dict(
    ces_catalogs=[dict(application='RATAN_ENTITLEMENT_RULE',path=str(catalog_path.relative_to(ROOT)),
        sha256=hashlib.sha256(catalog_path.read_bytes()).hexdigest(),role_count=len(catalog),
        feature_count=len(ces_features),action_count=len({a for f,a in ces_pairs}),pair_count=len(ces_pairs)),
        dict(application='FLOWZERO',path=str(flow_path.relative_to(ROOT)),
        sha256=hashlib.sha256(flow_path.read_bytes()).hexdigest(),role_count=len(flow_catalog),
        feature_count=len({f for f,a in flow_pairs}),action_count=len({a for f,a in flow_pairs}),pair_count=len(flow_pairs))],
    ems2_dictionaries=subject_dictionaries,observed_account_grant_unions=grant_unions,
    conclusion='All supplied production subject dictionary names (four names across data and system entities) and all 36 observed production subject-action pairs occur in the RATAN CES catalog. A complete X_RATANONE subject dictionary and complete action definitions are not supplied.',
    specific_unresolved_names=[dict(name='srv.fxu.001',environment='UAT',entity='RATAN_FUNC',
        category='Subject dictionary name absent from both supplied CES catalogs',actions='not supplied',
        impact='No granted action or affected account is demonstrated by these samples.',
        owner='unknown',next_action='Classify the subject and inspect its role/action assignments before deciding migration applicability.'),
        dict(name='EMS2_ADMIN',environment='PROD and UAT',entity='X_RATANONE',
        description='This role allows the user to perform IAM  role and entitlement management',
        category='Role name absent from RATAN CES catalog',
        inference='The description indicates platform administration. The migration disposition remains unsourced.',
        owner='unknown',next_action='Record whether CES management roles replace this EMS2 administration role.')])
(OUT/'api-parity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'subject_dictionary_count':len(subject_dictionaries),'observed_grant_union_count':len(grant_unions),'conclusion':result['supplied_function_inventory']['conclusion']},indent=2))
