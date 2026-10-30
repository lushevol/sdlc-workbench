"""Verify answered questions cannot silently lose source and consumer bindings."""
from pathlib import Path
import copy,hashlib,tempfile,unittest
from ai_sdlc_workbench.question_reconciliation import reconcile_questions
from ai_sdlc_workbench.models import WorkbenchError
class QuestionReconciliationTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name).resolve()
  self.answer='\nStatus: `ANSWERED_FROM_EVIDENCE`.\nEvidence: [controller](controller.java).\n'
  self.write('questions.md','# Questions\n\n### KQ-1\n'+self.answer)
  self.write('knowledge.md','---\nversion: 1\n---\nOld meaning.\n')
  self.manifest={'schema_version':1,'questions':[{'id':'KQ-1','document':self.ref('questions.md'),'consumers':[self.ref('knowledge.md')|{'version':1}]}]}
 def write(self,name,text):(self.root/name).write_text(text)
 def ref(self,name):return {'path':name,'sha256':hashlib.sha256((self.root/name).read_bytes()).hexdigest()}
 def codes(self):return [r['code'] for r in reconcile_questions(self.manifest,self.root)['findings']]
 def test_resolved_answer_without_consuming_update_is_visible(self):
  """Given a resolved answer and old consumer, when reconciled, then missing propagation remains actionable."""
  self.assertIn('ANSWER_PROPAGATION_MISSING',self.codes())
 def test_matching_hash_reference_version_are_only_reference_completion(self):
  """Given all reference bindings, when reconciled, then business verification remains separate."""
  self.write('knowledge.md','---\nversion: 2\n---\n[Answer](questions.md#kq-1)\n')
  report=reconcile_questions(self.manifest,self.root);answer_hash=report['questions'][0]['answer_sha256']
  self.manifest['questions'][0]['consumers']=[self.ref('knowledge.md')|{'version':2,'applied_answer_sha256':answer_hash}]
  result=reconcile_questions(self.manifest,self.root);self.assertEqual(result['status'],'REFERENCES_COMPLETE');self.assertEqual(result['verification'],'NOT_VERIFIED')
 def test_revised_answer_invalidates_prior_propagation(self):
  """Given changed answer bytes, when reconciled, then stale evidence is reported."""
  self.write('questions.md',(self.root/'questions.md').read_text()+'New rule.\n');self.assertIn('STALE_ANSWER_SOURCE',self.codes())
 def test_duplicate_entry_points_and_headings_remain_visible(self):
  """Given duplicate question entry points, when reconciled, then the conflict is reported."""
  self.manifest['questions'].append(copy.deepcopy(self.manifest['questions'][0]));self.assertIn('DUPLICATE_ENTRY_POINT',self.codes())
  self.write('questions.md',(self.root/'questions.md').read_text()+'\n### KQ-1\nDuplicate.\n');self.assertIn('DUPLICATE_QUESTION_ID',self.codes())
 def test_answer_source_missing_and_unknown_consumer_scope(self):
  """Given an answered question without sources or consumers, when checked, then both limits are explicit."""
  self.write('questions.md','### KQ-1\nStatus: ANSWERED\n');self.manifest['questions'][0]['document']=self.ref('questions.md');self.manifest['questions'][0]['consumers']=[]
  self.assertIn('ANSWER_SOURCE_MISSING',self.codes());self.assertIn('CONSUMER_SCOPE_UNKNOWN',self.codes())
 def test_unsafe_consumer_path_is_rejected(self):
  """Given a consumer outside the workspace, when checked, then its path is rejected."""
  self.manifest['questions'][0]['consumers'][0]['path']='../escape'
  with self.assertRaises(WorkbenchError):self.codes()
 def test_same_anchor_in_unrelated_document_does_not_prove_propagation(self):
  """Given an unrelated answer link, when checked, then the required consumer binding remains missing."""
  self.write('knowledge.md','---\nversion: 2\n---\n[Answer](unrelated.md#kq-1)\n')
  self.manifest['questions'][0]['consumers']=[self.ref('knowledge.md')|{'version':2}]
  row=reconcile_questions(self.manifest,self.root)['questions'][0]
  self.assertFalse(row['consumers'][0]['answer_reference_present'])
 def test_nested_answer_edit_invalidates_consumer_hash(self):
  """Given an answer under a deeper heading, when that answer changes, then its prior propagation hash becomes stale."""
  self.write('questions.md','### KQ-1\n'+self.answer+'\n#### Answer\nOld answer.\n')
  self.write('knowledge.md','---\nversion: 2\n---\n[Answer](questions.md#kq-1)\n')
  entry=self.manifest['questions'][0];entry['document']=self.ref('questions.md')
  answer_hash=reconcile_questions(self.manifest,self.root)['questions'][0]['answer_sha256']
  entry['consumers']=[self.ref('knowledge.md')|{'version':2,'applied_answer_sha256':answer_hash}]
  self.assertEqual(reconcile_questions(self.manifest,self.root)['status'],'REFERENCES_COMPLETE')
  self.write('questions.md',(self.root/'questions.md').read_text().replace('Old answer.','Changed answer.'));entry['document']=self.ref('questions.md')
  self.assertIn('ANSWER_PROPAGATION_MISSING',self.codes())
 def test_nonstring_question_id_is_a_validation_error(self):
  """Given a numeric question ID, when checked, then a structured validation error replaces an interpreter failure."""
  self.manifest['questions'][0]['id']=123
  with self.assertRaises(WorkbenchError):self.codes()
 def test_malformed_consumer_metadata_is_a_validation_error(self):
  """Given malformed consumer metadata, when checked, then reconciliation reports a validation error."""
  self.write('knowledge.md','---\nversion: [\n---\n')
  self.manifest['questions'][0]['consumers']=[self.ref('knowledge.md')|{'version':1}]
  with self.assertRaises(WorkbenchError):self.codes()
