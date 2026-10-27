import hashlib,json,unittest
from pathlib import Path
R=Path(__file__).parents[1];N=['SetDefaultFontsPointer','SetFontsPointer']
class Tests(unittest.TestCase):
 def test_catalog(self):
  s=json.loads((R/'analysis/font-pointer-bootstrap-summary.json').read_text());c=json.loads((R/'analysis/global-release-catalog.json').read_text());self.assertEqual((s['cluster'],s['release_count'],sum(x['origin_reference']for x in s['releases'])),(N,len(c['releases']),1))
  for x in s['releases']:
   e=json.loads((R/x['evidence']).read_text());self.assertEqual([f['name']for f in e['functions']],N);self.assertEqual([f['control_flow']['direct_call_count']for f in e['functions']],[1,0]);self.assertEqual(e['verified_behavior']['default_table'],'sFontInfos');self.assertNotIn('instructions',e)
 def test_source_and_manifest(self):
  src=(R/'src/font_pointer.c').read_text();self.assertIn('gFonts = fonts',src);m=json.loads((R/'manifests/font-pointer-bootstrap-reconstruction.json').read_text())
  for x in m['outputs']:self.assertEqual(hashlib.sha256((R/x['path']).read_bytes()).hexdigest(),x['sha256'])
if __name__=='__main__':unittest.main()
