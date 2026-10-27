import hashlib,json,unittest
from pathlib import Path
R=Path(__file__).parents[1]
class Tests(unittest.TestCase):
 def test_catalog(self):
  s=json.loads((R/'analysis/clear-dma3-requests-summary.json').read_text());c=json.loads((R/'analysis/global-release-catalog.json').read_text());self.assertEqual((s['function'],s['release_count'],sum(x['origin_reference']for x in s['releases'])),('ClearDma3Requests',len(c['releases']),1))
  for x in s['releases']:
   e=json.loads((R/x['evidence']).read_text());self.assertEqual((e['verified_behavior']['request_count'],e['control_flow']['instruction_halfwords'],e['control_flow']['direct_call_count'],e['control_flow']['return_count']),(128,21,0,1));self.assertNotIn('instructions',e);self.assertFalse(e['raw_rom_bytes_included'])
 def test_source_and_manifest(self):
  src=(R/'src/dma3_manager.c').read_text();self.assertIn('void ClearDma3Requests(void)',src);self.assertIn('request->size = 0',src);m=json.loads((R/'manifests/clear-dma3-requests-reconstruction.json').read_text())
  for x in m['outputs']:self.assertEqual(hashlib.sha256((R/x['path']).read_bytes()).hexdigest(),x['sha256'])
if __name__=='__main__':unittest.main()
