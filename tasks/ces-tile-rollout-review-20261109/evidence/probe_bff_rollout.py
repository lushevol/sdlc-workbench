#!/usr/bin/env python3
"""Controlled BFF service probe; external CES and private error bases are substitutes.

No repository source is changed. The service, mapper, drawer, DTOs, and configuration
compile from their actual source. This excludes Spring wiring and external clients.
"""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
REPO = ROOT / "repos/services/single-ui-bff"
BASE = REPO / "src/main/java/com/scb/sso/singleuibff"
JAVA = Path("/opt/homebrew/opt/openjdk@17/bin")
SOURCE = r'''
import java.util.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.scb.sso.singleuibff.config.*;
import com.scb.sso.singleuibff.dto.config.EntitlementSource;
import com.scb.sso.singleuibff.dto.ems2.v2.*;
import com.scb.sso.singleuibff.dto.request.RequestOfApplicationTile;
import com.scb.sso.singleuibff.service.v2.*;
import com.scb.sso.singleuibff.service.v2.authorization.*;
import com.scb.sso.singleuibff.service.v2.filter.ems3.*;
import com.scb.sso.singleuibff.service.v2.filter.ems3.dto.Ems3DataEntitlementDto;
import com.scb.sso.singleuibff.util.*;
public class RolloutProbe {
 static final ObjectMapper JSON = new ObjectMapper();
 static void check(boolean value) { if(!value) throw new AssertionError(); }
 static Map<String,Object> row(long id,String source,String app) {
  Map<String,Object> r=new HashMap<>();
  r.put("application_tile_id",id);r.put("application_category_id",10L);
  r.put("key_name","app");r.put("module","module");r.put("tile","tile"+id);
  r.put("is_template",false);r.put("entitlement_source",source);
  r.put("ems2_entities","LEGACY");r.put("ems2_subject","feature");
  r.put("entitlement_app_id","id");r.put("entitlement_app_name",app);
  r.put("entitlement_app_feature","feature");return r;
 }
 static Ems3DataEntitlementDto response() {
  var role=new Ems3DataEntitlementDto.RoleEntitlement();role.setFeature("feature");role.setAction("read");
  var e=new Ems3DataEntitlementDto.Entitlements();e.setRoleEntitlements(List.of(role));
  var d=new Ems3DataEntitlementDto();d.setEntitlements(e);return d;
 }
 static Ems2Result legacy() {
  var s=new Subject();s.setName("feature");s.setEntitlementSource(EntitlementSource.EMS2);s.setActions(List.of());
  var e=new Entity();e.setName("LEGACY");e.setSubjects(List.of(s));
  var result=new Ems2Result();result.setEntities(List.of(e));return result;
 }
 static List<Long> visible(List<Map<String,Object>> rows,TileAuthorizationResult result) {
  var util=new AdminModuleUtil(null,JSON,null,null);
  return util.getAuthorizedDrawer(rows,result).stream()
   .flatMap(d->((List<Map<String,Object>>)d.get("tiles")).stream())
   .map(t->Long.parseLong(t.get("id").toString())).sorted().toList();
 }
 public static void main(String[] args) throws Exception {
  String scenario=args[0];
  if(scenario.equals("request")) {
   var omitted=JSON.readValue("{}",RequestOfApplicationTile.class);
   var explicitNull=JSON.readValue("{\"entitlementSource\":null}",RequestOfApplicationTile.class);
   check(omitted.getEntitlementSource()==EntitlementSource.EMS2);
   check(explicitNull.getEntitlementSource()==null);
   System.out.println("RESULT {\"omittedSource\":\"EMS2\",\"explicitNullSource\":null}");return;
  }
  var props=new AuthorizationMigrationProperties();props.setMode(AuthorizationMigrationMode.EMS3_PRIMARY_DUAL_READ);
  var mapper=new AuthorizationResultMapper();var comparison=new AuthorizationComparisonService(mapper);
  var field=AuthorizationComparisonService.class.getDeclaredField("objectMapper");field.setAccessible(true);field.set(comparison,JSON);
  Ems3EntitlementService ces=new Ems3EntitlementService() {
   public Ems3DataEntitlementDto getAuthorization(String user,String id,String app) {
    if(scenario.equals("failure")&&app.equals("APP_B"))throw new IllegalStateException("synthetic CES app B failure");
    var r=response();
    if(scenario.equals("empty")&&app.equals("APP_B"))r.getEntitlements().setRoleEntitlements(List.of());
    return r;
   }
  };
  AuthorizationService old=(user,entities)->legacy();
  var svc=new TileAuthorizationServiceImpl(old,ces,mapper,comparison,props,Runnable::run,new JsonLogUtils(JSON));
  var rows=List.of(row(1,"EMS2",""),row(2,"EMS3","APP_A"),row(3,"EMS3","APP_B"));
  var result=svc.getAuthorization("synthetic-user",rows);
  var tiles=visible(rows,result);
  if(scenario.equals("mixed")) { check(tiles.equals(List.of(1L,2L,3L)));check(result.featureGrantedTileIds().equals(Set.of(2L,3L))); }
  else { check(tiles.equals(List.of(1L)));check(result.featureGrantedTileIds().isEmpty()); }
  System.out.println("RESULT "+JSON.writeValueAsString(Map.of("visibleTileIds",tiles,"grantedCesTileIds",result.featureGrantedTileIds(),"entityNames",result.entitlements().getEntities().stream().map(Entity::getName).toList())));
 }
}
'''
SUBSTITUTES = {
 "com/scb/sso/singleuibff/service/v2/filter/ems3/Ems3EntitlementService.java": "package com.scb.sso.singleuibff.service.v2.filter.ems3; import com.scb.sso.singleuibff.service.v2.filter.ems3.dto.Ems3DataEntitlementDto; public class Ems3EntitlementService { public Ems3DataEntitlementDto getAuthorization(String user,String id,String name){throw new UnsupportedOperationException();}}",
 "com/scb/ratan/commons/RatanError.java": "package com.scb.ratan.commons; public interface RatanError {String getErrorCode();int getStatus();}",
 "com/scb/ratan/commons/exception/RatanServiceException.java": "package com.scb.ratan.commons.exception; import com.scb.ratan.commons.RatanError; public class RatanServiceException extends RuntimeException {private final RatanError error;public RatanServiceException(RatanError e,String m){super(m);error=e;}public RatanError getError(){return error;}}",
}
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 binding=json.loads((HERE/"bff-routing-tests/result.json").read_text())
 sources=[REPO/s["path"] for s in binding["sources"] if s["path"].startswith("src/main/")]
 sources += [BASE/p for p in ["config/AuthorizationMigrationMode.java","config/AuthorizationMigrationProperties.java","service/v2/AuthorizationService.java","service/v2/authorization/TileAuthorizationService.java","service/v2/authorization/TileAuthorizationServiceImpl.java","service/v2/authorization/TileFeatureMatcher.java","service/v2/authorization/Ems3TileReadResult.java","service/v2/authorization/AuthorizationResultMapper.java","service/v2/authorization/AuthorizationComparisonService.java","service/v2/filter/ems3/dto/Ems3DataEntitlementDto.java","service/v2/filter/ems3/exception/Ems3UnRetryableException.java","service/v2/filter/ems3/exception/Ems3Error.java","util/JsonLogUtils.java"]]
 sources=sorted(set(sources)); jars=[Path(j["path"]) for j in binding["dependencies"]]
 result={"head":subprocess.check_output(["git","rev-parse","HEAD"],cwd=REPO,text=True).strip(),"started_at":dt.datetime.now(dt.timezone.utc).isoformat(),"sources":[{"path":str(p.relative_to(REPO)),"sha256":sha(p)} for p in sources],"dependencies_binding":"bff-routing-tests/result.json","dependencies_binding_sha256":sha(HERE/"bff-routing-tests/result.json"),"probe_sha256":sha(Path(__file__)),"cases":[],"limits":["Exact production service, mapper, DTOs, configuration, and drawer utility; cached dependency versions from shared routing binding.","Synthetic EMS2/CES assignments; CES transport and private Ratan error bases are explicit substitutes in this script.","Synchronous direct executor; no Spring injection, controller, retry, HTTP, live assignments, database, browser, or production reachability verification.","These assertions confirm observed behavior, including loss of unrelated CES grants. PASSED does not mean independent rollout passed."]}
 with tempfile.TemporaryDirectory(prefix="bff-rollout-probe-") as temp:
  tmp=Path(temp);classes=tmp/"classes";classes.mkdir();generated=[]
  for rel,content in {**SUBSTITUTES,"RolloutProbe.java":SOURCE}.items():
   p=tmp/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content);generated.append(p)
  cp=os.pathsep.join(map(str,jars))
  p=subprocess.run([str(JAVA/"javac"),"--release","17","-cp",cp,"-processorpath",str(jars[0]),"-d",str(classes),*map(str,sources+generated)],capture_output=True,text=True,timeout=60)
  result["compile_exit_code"]=p.returncode
  if p.returncode:
   result["compile_diagnostics"]=p.stderr; (HERE/"bff-rollout-probe.json").write_text(json.dumps(result,indent=2)+"\n");print(p.stderr);return 1
  for case in ["mixed","failure","empty","request"]:
   started=dt.datetime.now(dt.timezone.utc).isoformat()
   p=subprocess.run([str(JAVA/"java"),"-cp",str(classes)+os.pathsep+cp,"RolloutProbe",case],capture_output=True,text=True,timeout=30)
   line=next((l[7:] for l in p.stdout.splitlines() if l.startswith("RESULT ")),None)
   result["cases"].append({"id":"BFF-ROLLOUT-"+case.upper(),"started_at":started,"finished_at":dt.datetime.now(dt.timezone.utc).isoformat(),"status":"PASSED" if p.returncode==0 else "FAILED","observed":json.loads(line) if line else None,"diagnostics":p.stderr if p.returncode else None})
   (HERE/"bff-rollout-probe.json").write_text(json.dumps(result,indent=2)+"\n")
   print(case,p.returncode,line)
 return int(any(c["status"]!="PASSED" for c in result["cases"]))
if __name__=="__main__":raise SystemExit(main())
