import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
class Tests(unittest.TestCase):
 def test_emerald_interrupt_differences(self):
  m=json.loads((ROOT/'analysis/emerald-jp-interrupt-init-map.json').read_text());s=(ROOT/'src/interrupt_init.c').read_text();self.assertEqual(m['version_difference'],{'vblank_enable':'EnableInterrupts call','serial_timer3_restore':True});self.assertIn('EnableInterrupts(INTR_FLAG_VBLANK)',s);self.assertIn('gIntrTable[1]=SerialIntr',s);self.assertIn('gIntrTable[2]=Timer3Intr',s);self.assertNotIn('REG_DISPSTAT',s);self.assertFalse(m['rom_code_and_literals']['raw_bytes_published'])
 def test_dma_and_callbacks(self):
  m=json.loads((ROOT/'analysis/emerald-jp-interrupt-init-map.json').read_text());self.assertEqual(m['dma']['byte_count'],0x800);self.assertEqual(m['literal_addresses']['gIntrTableTemplate'],'0x0829BDBC');self.assertEqual(m['proven_offsets']['serialCallback'],24)
 def test_manifest(self):
  m=json.loads((ROOT/'manifests/interrupt-init-reconstruction.json').read_text());self.assertFalse(m['raw_rom_bytes_included'])
  for o in m['outputs']:self.assertEqual(hashlib.sha256((ROOT/o['path']).read_bytes()).hexdigest(),o['sha256'])
if __name__=='__main__':unittest.main()
