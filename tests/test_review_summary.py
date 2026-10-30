"""Check task assessments retain adverse outcomes, evidence limits, and protected inputs."""
from pathlib import Path
import copy,hashlib,json,tempfile,unittest
from unittest.mock import patch
from ai_sdlc_workbench.models import WorkbenchError
from ai_sdlc_workbench.release_report_render import render_review_summary
from test_release_report_render import Elements

class ReviewSummaryTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name).resolve()
  self.evidence=self.root/'source.txt';self.evidence.write_text('Actual retained evidence\n')
  self.path=self.root/'index.json'
  loc={'artifact_id':'SOURCE'}
  self.payload={'schema_version':1,'id':'review','scope_id':'scope','title':'<script>unsafe</script>', 'inventory_completeness':{'criteria':'UNKNOWN','changes':'UNKNOWN','cases':'SELECTED'},'artifacts':[{'id':'SOURCE','kind':'EXECUTION','path':'source.txt','sha256':hashlib.sha256(self.evidence.read_bytes()).hexdigest()}],'criteria':[],'changes':[],'cases':[{'id':'TC1','definition':loc,'limits':[]}],'assertions':[],'links':[],'executions':[{'id':'E1','case_id':'TC1','source':loc,'original_status':'failed','outcome':'FAILED','characterization':False,'level':'UNKNOWN','mode':'UNKNOWN','assertion_ids':[],'environment_id':None,'limits':[]}],'limits':['Scope remains unknown.'],'assessment':{'source':loc,'recommendation':'NO_GO','decision_certainty':'HIGH','summary':'Replay issued access after logout.','review_state':'pending','issues':[{'id':'SEC1','title':'Credential replay','observed_impact':'Refresh issued new access.','priority':'P1','release_blocking':True,'owner':'unknown','next_action':'Correct revocation.','evidence':[loc],'limits':['Local controller; persistence substituted.']},{'id':'MIN1','title':'Minor observation','observed_impact':'No disruption observed.','priority':'P4','release_blocking':False,'owner':'unknown','next_action':'Retain evidence.','evidence':[loc],'limits':[]}],'limits':['Historical assessment.']}}
 def render(self):
  self.path.write_text(json.dumps(self.payload));return render_review_summary(self.path,self.root,self.root/'summary.html')
 def test_decision_impact_owner_action_visible_and_details_collapsed(self):
  """Given a failed case and recorded hold, when rendered, then decision and consequence remain visible."""
  with patch('socket.socket',side_effect=AssertionError('Offline only')):p=self.render()
  dom=Elements(p.read_text());visible=dom.text(initial=True)
  for value in ['NO_GO','Refresh issued new access.','Owner: unknown','Correct revocation.','HIGH','UNKNOWN','FAILED','1'] :self.assertIn(value,visible)
  self.assertNotIn('No disruption observed.',visible)
  self.assertFalse(any(tag=='script' for tag,_ in dom.tags))
  self.assertTrue(all('open' not in attrs for tag,attrs in dom.tags if tag=='details'))
  self.assertIn('source.txt',p.read_text())
 def test_unknown_assessment_is_not_go(self):
  """Given no assessment, when rendered, then missing judgment remains explicit."""
  self.payload.pop('assessment');text=self.render().read_text();self.assertIn('INSUFFICIENT_EVIDENCE',text);self.assertIn('NOT_VERIFIED',text)
 def test_stale_evidence_warns_before_reuse(self):
  """Given changed evidence, when rendered, then freshness remains stale and requires reassessment."""
  self.evidence.write_text('Changed\n');text=self.render().read_text();self.assertIn('STALE',text);self.assertIn('Evidence needs review',text)
 def test_cannot_replace_index_or_evidence(self):
  """Given protected evidence, when selected as output, then rendering rejects the overwrite."""
  self.render();before=self.path.read_bytes()
  for p in [self.path,self.evidence]:
   with self.assertRaises(WorkbenchError):render_review_summary(self.path,self.root,p)
  self.assertEqual(self.path.read_bytes(),before)
 def test_invalid_references_fail_before_output(self):
  """Given a dangling reference, when rendered, then no report is created."""
  self.payload['cases'][0]['definition']={'artifact_id':'missing'}
  with self.assertRaises(WorkbenchError):self.render()
  self.assertFalse((self.root/'summary.html').exists())
 def test_repeated_render_is_deterministic_and_preserves_input(self):
  """Given retained assessment, when rendered twice, then output and source remain unchanged."""
  p=self.render();one=p.read_bytes();source=self.path.read_bytes();p=self.render();self.assertEqual(one,p.read_bytes());self.assertEqual(source,self.path.read_bytes())

 def test_real_composite_case_ids_are_preserved(self):
  """Given composite Session Refresh IDs, when rendered, then reference validation preserves the original identity."""
  self.payload['cases'][0]['id']='RN-C001/PAIR-001'
  self.payload['executions'][0]['case_id']='RN-C001/PAIR-001'
  self.assertTrue(self.render().is_file())
