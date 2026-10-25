#!/usr/bin/env python3
"""Copy one committed candidate into the isolated browser fixture without changing the checkout."""
import argparse,hashlib,io,json,subprocess,tarfile
from pathlib import Path
from datetime import datetime,timezone
root=Path.cwd();repo=root/'repos/ui/mfe-base';stage=root/'tasks/portal-background-session-20261019/evidence/minor-fixes-20261025'
p=argparse.ArgumentParser();p.add_argument('--ref',required=True);p.add_argument('--label',required=True);args=p.parse_args()
ref=subprocess.check_output(['git','-C',str(repo),'rev-parse',args.ref],text=True).strip()
data=subprocess.check_output(['git','-C',str(repo),'archive',ref,'src'])
destination=root/'.workbench/session-active-cutoff-fix-20261024/mfe/source'
files={}
with tarfile.open(fileobj=io.BytesIO(data)) as archive:
 for member in archive.getmembers():
  if not member.isfile():continue
  content=archive.extractfile(member).read();target=destination/member.name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(content);files[member.name]=hashlib.sha256(content).hexdigest()
record={'recorded_at':datetime.now(timezone.utc).isoformat(),'candidate_ref':ref,'fixture_source':str(destination.relative_to(root)),'source_archive_sha256':hashlib.sha256(data).hexdigest(),'files':files,'scope':'Committed src bytes only. Existing isolated webpack substitutions remain unchanged. No application checkout edit.'}
out=stage/'setup'/f'source-sync-{args.label}.json';out.write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':'COPIED','ref':ref,'files':len(files),'binding':str(out)}))
