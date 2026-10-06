import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
class Tests(unittest.TestCase):
 def test_behavior(self):
  m=json.loads((ROOT/'analysis/emerald-jp-display-serial-interrupt-map.json').read_text());s=(ROOT/'src/display_serial_interrupts.c').read_text();self.assertEqual([f['address'] for f in m['functions']],['0x08000814','0x08000844','0x08000878']);self.assertFalse(m['rom_code_and_literals']['raw_bytes_published']);self.assertIn('gMain.vcountCallback();m4aSoundVSync()',s);self.assertEqual(m['calls'][2]['target'],'0x0828DF98')
 def test_manifest(self):
  m=json.loads((ROOT/'manifests/display-serial-interrupt-reconstruction.json').read_text());self.assertFalse(m['raw_rom_bytes_included']);[self.assertEqual(hashlib.sha256((ROOT/o['path']).read_bytes()).hexdigest(),o['sha256']) for o in m['outputs']]
if __name__=='__main__':unittest.main()

