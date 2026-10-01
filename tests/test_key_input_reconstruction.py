import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
class Tests(unittest.TestCase):
 def test_emerald_specific_map_and_source(self):
  m=json.loads((ROOT/'analysis/emerald-jp-key-input-map.json').read_text());s=(ROOT/'src/key_input.c').read_text();self.assertEqual([f['address'] for f in m['functions']],[0x080005BC,0x080005E4]);self.assertEqual(m['version_difference']['save_options_access'],'pointer_indirect');self.assertIn('gSaveBlock2Ptr->optionsButtonMode',s);self.assertNotIn('gSaveBlock2.optionsButtonMode',s);self.assertFalse(m['rom_code_range']['raw_bytes_published'])
 def test_behavioral_reconstruction(self):
  s=(ROOT/'src/key_input.c').read_text()
  for token in ('gMain.keyRepeatCounter--','gMain.newAndRepeatedKeys = keyInput','gMain.newKeys |= A_BUTTON','gMain.watchedKeysPressed = 1'):self.assertIn(token,s)
 def test_manifest(self):
  m=json.loads((ROOT/'manifests/key-input-reconstruction.json').read_text());self.assertFalse(m['raw_rom_bytes_included'])
  for o in m['outputs']:self.assertEqual(hashlib.sha256((ROOT/o['path']).read_bytes()).hexdigest(),o['sha256'])
if __name__=='__main__':unittest.main()
