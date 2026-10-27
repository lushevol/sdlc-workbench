from pathlib import Path
import subprocess,os,json,datetime,time,sys,hashlib
out=Path(__file__).resolve().parent
name=sys.argv[1]; attempt=sys.argv[2]
prompt=out/f"claude-independent-{name}-prompt.txt"
cmd=["claude","--print","--output-format","json","--tools","","--strict-mcp-config","--mcp-config",'{"mcpServers":{}}',"--disable-slash-commands","--no-session-persistence","--safe-mode"]
env=dict(os.environ,CLAUDE_CODE_MAX_OUTPUT_TOKENS="4096")
record={"command":cmd,"cwd":"/tmp","started_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"tools_disabled":True,"mcp_disabled":True,"source_only":True,"prompt":prompt.name,"prompt_sha256":hashlib.sha256(prompt.read_bytes()).hexdigest(),"status":"RUNNING"}
execution=out/f"claude-independent-{name}-{attempt}-execution.json"
execution.write_text(json.dumps(record,indent=2)+"\n")
start=time.monotonic()
response=out/f"claude-independent-{name}-{attempt}-response.json"
with prompt.open() as inp,response.open("w") as result,(out/f"claude-independent-{name}-{attempt}-stderr.log").open("w") as err:
 r=subprocess.run(cmd,stdin=inp,stdout=result,stderr=err,env=env,cwd=Path("/tmp"))
record.update({"ended_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"duration_seconds":time.monotonic()-start,"exit_code":r.returncode,"status":"FINISHED","response":response.name,"response_sha256":hashlib.sha256(response.read_bytes()).hexdigest()})
try:
 body=json.loads(response.read_text());record.update({"is_error":body.get("is_error"),"models":list(body.get("modelUsage",{})),"duration_ms":body.get("duration_ms"),"success":r.returncode==0 and not body.get("is_error",False)})
except Exception as e:
 record["parse_error"]=str(e)
execution.write_text(json.dumps(record,indent=2)+"\n");print(json.dumps(record))
