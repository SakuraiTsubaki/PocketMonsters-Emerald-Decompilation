import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
class Tests(unittest.TestCase):
 def setUp(self):
  self.cfg=json.loads((ROOT/'analysis/emerald-jp-thumb-entry-cfg.json').read_text())
  self.map=json.loads((ROOT/'analysis/emerald-jp-agb-main-map.json').read_text())
  self.source=(ROOT/'src/main_loop.c').read_text()
 def test_map_exactly_covers_cfg_calls(self):
  self.assertEqual({(x['address'],x['target']) for x in self.map['direct_calls']},{(x['source'],x['target']) for x in self.cfg['calls']})
  self.assertTrue(all(x['name'] for x in self.map['direct_calls']));self.assertEqual(len(self.cfg['calls']),29)
 def test_loop_and_callback_dispatch(self):
  edge=self.map['function']['loop_back_edge'];self.assertIn({'source':edge['source'],'target':edge['target'],'kind':'branch'},self.cfg['edges'])
  self.assertEqual(self.source.count('UpdateLinkAndCallCallbacks();'),3)
 def test_emerald_build_specific_behavior(self):
  for token in ('RtcInit();','gFlashMemoryPresent!=1','SetMainCallback2(0);','InitRFU();','ClearSpriteCopyRequests();'):
   self.assertIn(token,self.source)
  self.assertNotIn('AGBPrintInit',self.source);self.assertNotIn('gHelpSystemEnabled',self.source)
 def test_manifest_hashes_outputs(self):
  manifest=json.loads((ROOT/'manifests/agb-main-reconstruction.json').read_text())
  for output in manifest['outputs']:
   self.assertEqual(hashlib.sha256((ROOT/output['path']).read_bytes()).hexdigest(),output['sha256'])
if __name__=='__main__':unittest.main()
