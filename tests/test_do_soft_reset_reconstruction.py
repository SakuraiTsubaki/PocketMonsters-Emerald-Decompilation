import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
class Tests(unittest.TestCase):
 def test_cfg_map_and_source(self):
  cfg=json.loads((ROOT/'analysis/emerald-jp-do-soft-reset-cfg.json').read_text());m=json.loads((ROOT/'analysis/emerald-jp-do-soft-reset-map.json').read_text());src=(ROOT/'src/do_soft_reset.c').read_text()
  self.assertEqual(cfg['source_sha256'],m['target']['sha256']);self.assertEqual(cfg['start_address'],int(m['function']['address'],16));self.assertEqual(cfg['range_end'],int(m['function']['range_end_exclusive'],16));self.assertTrue(cfg['return_observed']);self.assertTrue(cfg['raw_halfwords_omitted']);self.assertFalse(m['rom_code_range']['raw_bytes_published'])
  for token in ('REG_IME = 0;','m4aSoundVSyncOff();','ScanlineEffect_Stop();','DmaStop(1);','DmaStop(2);','DmaStop(3);','SoftReset('):self.assertIn(token,src)
 def test_variant_and_calls(self):
  m=json.loads((ROOT/'analysis/emerald-jp-do-soft-reset-map.json').read_text());src=(ROOT/'src/do_soft_reset.c').read_text();self.assertEqual([c['name'] for c in m['calls']],["m4aSoundVSyncOff","ScanlineEffect_Stop","SiiRtcProtect","SoftReset"]);self.assertEqual(m['behavior']['rtc_protected'],True);self.assertEqual(m['behavior']['soft_reset_mask'],'0xFF');self.assertEqual(('SiiRtcProtect();' in src),True)
 def test_manifest(self):
  m=json.loads((ROOT/'manifests/do-soft-reset-reconstruction.json').read_text());self.assertFalse(m['raw_rom_bytes_included'])
  for o in m['outputs']:self.assertEqual(hashlib.sha256((ROOT/o['path']).read_bytes()).hexdigest(),o['sha256'])
if __name__=='__main__':unittest.main()

