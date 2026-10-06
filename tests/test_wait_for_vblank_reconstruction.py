import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
class Tests(unittest.TestCase):
 def test_cfg_map_and_source_agree(self):
  cfg=json.loads((ROOT/'analysis/emerald-jp-wait-for-vblank-cfg.json').read_text());m=json.loads((ROOT/'analysis/emerald-jp-wait-for-vblank-map.json').read_text());src=(ROOT/'src/wait_for_vblank.c').read_text()
  self.assertEqual(cfg['source_sha256'],m['target']['sha256']);self.assertEqual(cfg['start_address'],int(m['function']['address'],16));self.assertEqual(cfg['range_end'],int(m['function']['range_end_exclusive'],16));self.assertTrue(cfg['return_observed']);self.assertTrue(cfg['raw_halfwords_omitted']);self.assertFalse(m['rom_code_range']['raw_bytes_published'])
  self.assertIn('gMain.intrCheck &= (uint16_t)~INTR_FLAG_VBLANK;',src);self.assertEqual(m['proven_offsets']['intrCheck'],0x1C)
 def test_wait_strategy(self):
  m=json.loads((ROOT/'analysis/emerald-jp-wait-for-vblank-map.json').read_text());src=(ROOT/'src/wait_for_vblank.c').read_text()
  self.assertEqual(m['calls'],[]);self.assertIn('while (!(gMain.intrCheck & INTR_FLAG_VBLANK))',src)
 def test_manifest(self):
  m=json.loads((ROOT/'manifests/wait-for-vblank-reconstruction.json').read_text());self.assertFalse(m['raw_rom_bytes_included'])
  for o in m['outputs']:self.assertEqual(hashlib.sha256((ROOT/o['path']).read_bytes()).hexdigest(),o['sha256'])
if __name__=='__main__':unittest.main()

