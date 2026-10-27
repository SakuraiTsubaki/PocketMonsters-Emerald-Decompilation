import hashlib,json,unittest
from pathlib import Path
R=Path(__file__).parents[1];N=['ResetBgs','ResetBgControlStructs','SetTextModeAndHideBgs']
class Tests(unittest.TestCase):
 def test_catalog(self):
  s=json.loads((R/'analysis/bg-reset-summary.json').read_text());c=json.loads((R/'analysis/global-release-catalog.json').read_text());self.assertEqual((s['cluster'],s['release_count'],sum(x['origin_reference']for x in s['releases'])),(N,len(c['releases']),1))
  for x in s['releases']:
   e=json.loads((R/x['evidence']).read_text());self.assertEqual([f['name']for f in e['functions']],N);self.assertEqual([f['control_flow']['direct_call_count']for f in e['functions']],[2,0,2]);self.assertEqual(e['verified_behavior']['background_count'],4);self.assertNotIn('instructions',e)
 def test_source_and_manifest(self):
  src=(R/'src/bg_reset.c').read_text();self.assertIn('uint8_t visible:1',src);m=json.loads((R/'manifests/bg-reset-reconstruction.json').read_text())
  for x in m['outputs']:self.assertEqual(hashlib.sha256((R/x['path']).read_bytes()).hexdigest(),x['sha256'])
if __name__=='__main__':unittest.main()
