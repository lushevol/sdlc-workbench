"""Record inspected mappings for the three executed browser specifications."""
import hashlib
import json
import re
from pathlib import Path
D=Path(__file__).resolve().parent
T=D.parent.parent
R=T.parent.parent
spec=T/'06-test-cases.md'
text=spec.read_text().splitlines()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources=json.loads((D/'source-manifest.json').read_text())['sources']
ui=next(s for s in sources if s['path']=='repos/ui/mfe-base/src/components/Timeout/index.tsx')
requirement=R/'knowledge/candidates/requirements/REQ-active-session-renewal.md'
runner=D/'renewal-loop-e2e.mjs'
manifest={'version':1,'evidence':{},'scenarios':{}}
def ev(key,path,start,end,kind,authority,revision=None):
 p=R/path
 manifest['evidence'][key]={'path':path,'sha256':sha(p),'start_line':start,'end_line':end,'kind':kind,'authority':authority}
 if revision:manifest['evidence'][key]['revision']=revision
ev('E_UI',ui['snapshot'],15,63,'ui','established',ui['revision'])
ev('E_REQ',str(requirement.relative_to(R)),216,235,'behavior','draft','candidate-v5')
ev('E_SETUP',str(runner.relative_to(R)),25,54,'automation','established')
ev('E_CANONICAL',str(spec.relative_to(R)),1,len(text),'behavior','draft')
for cid,start,end in [('RN-X001',55,63),('RN-X002',64,68),('RN-X003',69,74)]:
 key='E_'+cid.replace('-','_')
 ev(key,str(runner.relative_to(R)),start,end,'automation','established')
 review={'state':'UNVERIFIED','reviewer':None,'reviewed_at':None,
   'notes':'Inspected direct runner mapping. Candidate intent review and complete semantic step-binding review remain pending. Existing execution has narrower disclosed fixture claims.'}
 entry={'file':str(spec.relative_to(R)),'sha256':sha(spec),
    'behavior':{'intent':'Verify manual renewal state and current-session ownership within the isolated fixture.',
      'requirement':'E_REQ' if cid!='RN-X003' else 'E_CANONICAL',
      'criterion':str(requirement.relative_to(R))+'#L216-L235' if cid!='RN-X003' else str(spec.relative_to(R))+'#rn-x003'},
    'components':{},'steps':{},'review':review,
    'automation':{'framework':'existing Playwright portal probe','mode':'mapped','bindings':{},'review':review}}
 for name in ['Extend','Logout']:
  entry['components']['C_'+name.upper()]={'type':'button','identity':name,'identity_kind':'visible_label',
     'scope':'dialog named "Your session has been expired"','evidence':['E_UI']}
 entry['components']['C_DIALOG']={'type':'dialog','identity':'Your session has been expired','identity_kind':'accessible_name','scope':'portal','evidence':['E_UI']}
 index=next(i for i,l in enumerate(text) if l.strip()==f'Scenario: {cid}')
 mode='condition'
 for i in range(index+1,len(text)):
  line=text[i].strip()
  if line=='```':break
  match=re.match(r'(Given|When|Then|And) (.+)',line)
  if not match:continue
  token,step=match.groups()
  if token=='Given':mode='condition'
  if token=='When':mode='event'
  if token=='Then':mode='assertion'
  kind='interaction' if mode=='event' and 'button labeled' in step else mode
  mapped={'kind':kind,'evidence':['E_UI',key] if kind=='interaction' else ['E_SETUP'] if kind=='condition' else [key]}
  comps=[]
  for name in ['Extend','Logout']:
   if f'"{name}"' in step:comps.append('C_'+name.upper())
  if 'dialog' in step.lower():comps.append('C_DIALOG')
  if comps:mapped['components']=comps
  if kind=='assertion':mapped['observation']='ui' if 'dialog' in step else 'functional'
  entry['steps'][str(i+1)]=mapped
  symbol='page' if kind=='condition' else 'page.getByTestId' if kind=='interaction' else 'check' if kind=='assertion' else 'open' if 'expiry' in step else 'held' if 'late' in step else 'mode'
  entry['automation']['bindings'][str(i+1)]={'symbol':symbol,'evidence':['E_SETUP'] if kind=='condition' else [key]}
 manifest['scenarios'][cid]=entry
(D/'gherkin-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(len(manifest['scenarios']))
