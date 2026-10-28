from pathlib import Path
import json,hashlib,datetime
root=Path.cwd(); out=root/'tasks/portal-background-session-20261019/evidence/review-e2e-20261028'
sha=lambda b:hashlib.sha256(b).hexdigest()
def read(p):return json.loads((out/p).read_text())
def pair(prefix,case='result.json'):return [f'{prefix.format(side=side)}/{case}' for side in ['candidate','baseline']]
selected={
 '01':pair('final-focused/review-01-{side}'),
 '02':[f'contracts-02-{variant}-{side}/result.json' for variant in ['opaque','missingiat'] for side in ['candidate','baseline']],
 '03':pair('rerun/review-03-{side}'), '04':pair('rerun/review-04-{side}'),
 '05':pair('focused/review-05-{side}'), '06':pair('review-06-{side}'),
 '07':pair('near-expiry-final/review-07-{side}'), '12':pair('loader-{side}'),
 '17':pair('contracts17-near-deadline-{side}'),
}
checks=[];records=[]
for ident,paths in selected.items():
 for f in paths:
  d=read(f);assert d['status']=='COMPLETED',(f,d['status']);assert d['sourceRevision'] in ['e0030f5cf920b715f5831faf7df86cb9789b6d0f','f025513f696476a9cc8162681410cbd21e029bcb']
  for capture in d.get('screenshots',[]):
   if 'file' not in capture or 'sha256' not in capture:continue
   img=(out/f).parent/capture['file'];assert sha(img.read_bytes())==capture['sha256'],str(img)
  records.append({'finding':f'REVIEW-{ident}','caseId':f'REVIEW-E2E-{ident}','side':d.get('side',d.get('comparisonSide')),'variant':d.get('variant'),'status':d['status'],'result':f,'sha256':sha((out/f).read_bytes()),'sourceRevision':d['sourceRevision'],'runnerSha256':d.get('runnerSha256'),'impact':d.get('impact',d.get('impactDisposition',d.get('disposition'))),'screenshotCount':len(d.get('screenshots',[]))})
c=read(selected['01'][0]);b=read(selected['01'][1]);assert c['replacementTiming']['installedAtCompletion'] and c['replacementTiming']['completedAfterLogoutClickMs']<1000
assert c['protected']=={'called':True,'status':200,'result':True}
assert c['after']['access']['sha256']==c['afterReplacement']['access']['sha256'] and c['after']['dialogVisible'] and c['after']['extendDisabled'] and not c['after']['logoutDisabled']
logoutRequests=[x for x in c['requests'] if x['event']=='request' and x['pathname'].endswith('/logout')]
assert not logoutRequests;assert not b['after']['authenticated']
checks.append({'predicate':'REVIEW01 valid replacement installed before1000ms, BFF accepted, stale dialog persists, Extend disabled, Logout starts zero logout requests, baseline clears replacement','passed':True})
for f in selected['03']+selected['07']+selected['17']:
 d=read(f);assert d['protected']['result'] is True
checks.append({'predicate':'REVIEW03,07,17 final BFF validation succeeds on both exact revisions','passed':True})
c=read(selected['07'][0]);b=read(selected['07'][1]);assert 0<c['remainingAtHomeMs']<25000 and c['acquisitionsAfterRemount']==0 and b['acquisitionsAfterRemount']==1
checks.append({'predicate':'REVIEW07 actual Home remount inside25seconds; candidate retains usable refresh without catch-up, baseline reacquires after reducer clears refresh','passed':True})
for f in selected['12']:
 d=read(f);assert d['observations']['after']['isLoading'] is False and d['observations']['after']['signInInputActionable'] is True
checks.append({'predicate':'REVIEW12 final loader clears and SignIn remains actionable on both revisions','passed':True})
for f in selected['02']:
 d=read(f);assert d['validProtected']['result'] is True
checks.append({'predicate':'REVIEW02 valid controls recover for both token shapes and revisions; candidate uses same prompt','passed':True})
for f in selected['17']:
 d=read(f);assert d['acceptedAccessInstalled'] and not d['returnedAccessExpiredAtDelivery'];assert d['after']['dialogVisible'] is False
checks.append({'predicate':'REVIEW17 accepted access remains usable at late delivery, installs exactly, closes actual dialog, and validates on both revisions','passed':True})
classifications={
 '01':('REPRODUCED_LOCAL_IMPACT','Valid replacement session remains behind stale dialog; production caller unknown.'),
 '02':('UNSUPPORTED_PROVIDER_SHAPE_RECOVERS_WITH_VALID_RESPONSE','Opaque and missingiat are rejected; valid retry succeeds. Local provider emits finite exp and iat.'),
 '03':('BLOCKING_IMPACT_NOT_REPRODUCED','Failed fresh login clears refresh; actual Home reacquires and Extend recovers.'),
 '04':('STATE_DIFFERENCE_OBSERVED_IDENTITY_IMPACT_UNVERIFIED','Direct setter retains old refresh with new access; same local identity; distinct-user variant NOT_RUN.'),
 '05':('BOUNDED_WAIT_OBSERVED','Extend disabled during actual pending acquisition; Logout remains available; released failure settles. Suspended wall-clock duration unknown.'),
 '06':('MALFORMED_FIXTURE_ONLY','Missingexp with invalid signature forces logout. Inspected local provider never emits this shape.'),
 '07':('RECOVERY_BLOCK_NOT_REPRODUCED','Candidate remounts with usable refresh and under25seconds; no catch-up; actual Extend succeeds. Baseline clears refresh and reacquires.'),
 '08':('NOT_RUN_APPLICABLE_ARTIFACT_UNAVAILABLE','Inherited public-path rule; no matching non-loopback server artifact/deployment proof.'),
 '09':('NOT_RUN_CONSUMER_UNAVAILABLE','Development remote declaration; no actual importing journey or deployed composition identified.'),
 '10':('NOT_RUN_ROUTE_UNAVAILABLE','Parser evaluation is retained; no supported body-reading route identified.'),
 '11':('NOT_RUN_EXTERNAL_TEMPLATE_UNAVAILABLE','Exact external pipeline template and artifact unavailable.'),
 '12':('PERSISTENT_LOADER_NOT_REPRODUCED','Actual auth-error route clears loader and leaves SignIn actionable. Other stale completion routes unverified.'),
 '13':('NOT_RUN_UNREACHED_CONFIGLESS_ERROR','Inherited fallback; no source-bound browser path to a configless transport error identified.'),
 '14':('NOT_RUN_AFFECTED_CONSUMER_UNAVAILABLE','Local consumers catch stale cancellations; no concrete consumer failure identified.'),
 '15':('NOT_RUN_AFFECTED_CONSUMER_UNAVAILABLE','Timeout catches relogin rejection; no affected external consumer identified.'),
 '16':('NOT_RUN_AFFECTED_CONSUMER_UNAVAILABLE','Error-object identity differs; no identified consumer depends on that identity.'),
 '17':('VALID_LATE_DELIVERY_RECOVERS','Actual provider acceptance before expiry and usable response delivery afterward recover. Longer response hold separately reaches timeout.'),
 '18':('STATIC_MAINTENANCE_ONLY','Ignore typo has no tracked pnpm lockfile or formatter consumer. Business E2E not applicable.'),
}
result={'recordedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Requested session refresh review entries, not a rerun of original27browser cases or production verification.','status':'COMPLETED_WITH_EVIDENCE_LIMITS','baseline':'f025513f696476a9cc8162681410cbd21e029bcb','candidate':'e0030f5cf920b715f5831faf7df86cb9789b6d0f','reviewEntryCount':18,'entriesWithPairedBrowserObservations':9,'primaryBrowserObservations':len(records),'primaryCompletedObservations':sum(x['status']=='COMPLETED' for x in records),'reproducedLocalImpactEntries':['REVIEW-01'],'confidence':{'controlledLocalStaleDialog':'HIGH','productionReachability':'UNKNOWN'},'checks':checks,'cases':[{'finding':f'REVIEW-{i:02}', 'disposition':classifications[f'{i:02}'][0],'claimAndLimit':classifications[f'{i:02}'][1],'results':selected.get(f'{i:02}',[]),'definition':f'../../06-test-cases.md#review-e2e-{i:02}' if f'{i:02}' in selected else None,'audit':'case-audit.json'} for i in range(1,19)],'primaryResults':records,'retainedAdditionalEvidence':['contracts-summary.json','rerun/browser-summary.json','browser-summary.json','focused/browser-summary.json','final-focused/browser-summary.json','runner-assertion-audit.json'],'initialRunnerIdentityCorrection':{'appliesTo':'browser-summary.json and review-06-{side}/result.json','actualSource':'reviewE2e-attempt1.mjs.snapshot','actualSourceSha256':sha((out/'reviewE2e-attempt1.mjs.snapshot').read_bytes()),'reason':'Initial runner hashed on completion after the source file changed. Its exact executed snapshot is retained separately. Later runners hash before execution.'},'limits':['Local BFF uses identity and entitlement substitutes; toolkit substitute and webpack development configuration differ from deployment.','All primary timing uses real wall-clock. Route holds, malformed token shapes, and public API triggers remain disclosed in individual results.','Zero new approved ACs. Complete behavioral equivalence and production conformance remain unknown.','Distinct-user direct replacement, natural suspended-browser acquisition, and proposed direct expired-access assertion remain NOT_RUN.','Initial harness failures remain retained and do not count as business failures or primary completed observations.','No application fix, business acceptance, publication, or deployment occurred.']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'entries':18,'paired':9,'primaryObservations':len(records),'checksPassed':len(checks)}))
