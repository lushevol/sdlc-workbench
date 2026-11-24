"""Use only the owned synthetic loopback identity fixture; never retain credentials."""
from pathlib import Path
import json,re,sys,time,urllib.request,urllib.error
ROOT=Path(__file__).resolve().parents[5]
base='http://127.0.0.1:8191/api/auth/v2/sso/'

def call(endpoint,data):
 req=urllib.request.Request(base+endpoint,data=json.dumps(data).encode(),headers={'Content-Type':'application/json'},method='POST')
 try:
  with urllib.request.urlopen(req,timeout=10) as r:return r.status,dict(r.headers),r.read()
 except urllib.error.HTTPError as e:return e.code,dict(e.headers),e.read()

try:
 if sys.argv[1]=='login':
  src=(ROOT/'.workbench/portal-session-real-20261019/local-bff/runner/local/portalsession/LocalSessionApplication.java').read_text()
  user=re.search(r'public static final String USER="([^"]+)"',src).group(1)
  password=re.search(r'public static final String PASSWORD="([^"]+)"',src).group(1)
  status,headers,body=call('login',{'username':user,'password':password})
  access=next((v for k,v in headers.items() if k.lower()=='single-ui-authorization'),None)
  print(json.dumps({'status':status,'access':access,'observed_now_ms':round(time.time()*1000),'error':None if status==200 and access else 'Login did not issue access'}))
 elif sys.argv[1]=='validate':
  access=json.load(sys.stdin)['access'];status,headers,body=call('validate',{'singleUIAuthorization':access});data=json.loads(body)
  info=data.get('userInfo');info=json.loads(info) if isinstance(info,str) else info or {}
  print(json.dumps({'status':status,'result':data.get('result'),'accepted_identity':info.get('sub') or info.get('userId'),'error':None,'endpoint':'POST /api/auth/v2/sso/validate','credentials_retained':False}))
except Exception as error:
 print(json.dumps({'error':type(error).__name__+': '+str(error),'credentials_retained':False}))
