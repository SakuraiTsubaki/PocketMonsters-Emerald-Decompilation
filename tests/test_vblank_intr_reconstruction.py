import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
class Tests(unittest.TestCase):
 def test_emerald_ordered_behavior(self):
  m=json.loads((ROOT/'analysis/emerald-jp-vblank-intr-map.json').read_text());s=(ROOT/'src/vblank_intr.c').read_text();self.assertEqual(m['function']['address'],0x08000738);self.assertEqual(m['constants']['inBattle_offset'],0x439);self.assertFalse(m['rom_code_and_literals']['raw_bytes_published']);s=s[s.index('void VBlankIntr'):]
  tokens=['if(gWirelessCommType!=0)','gMain.vblankCounter1++','gTrainerHillVBlankCounter','gMain.vblankCallback()','gMain.vblankCounter2++','CopyBufferedValuesToGpuRegs()','ProcessDma3Requests()','m4aSoundMain()','TryReceiveLinkBattleData()','BATTLE_RNG_SUPPRESS_MASK','UpdateWirelessStatusIndicatorSprite()','INTR_CHECK|=INTR_FLAG_VBLANK']
  p=[s.index(t) for t in tokens];self.assertEqual(p,sorted(p))
 def test_saturating_counter_and_battle_rng_gate(self):
  s=(ROOT/'src/vblank_intr.c').read_text();self.assertIn('*gTrainerHillVBlankCounter<0xFFFFFFFFu',s);self.assertIn('if(!gMain.inBattle||!(gBattleTypeFlags&BATTLE_RNG_SUPPRESS_MASK))Random()',s)
 def test_manifest(self):
  m=json.loads((ROOT/'manifests/vblank-intr-reconstruction.json').read_text());self.assertFalse(m['raw_rom_bytes_included'])
  for o in m['outputs']:self.assertEqual(hashlib.sha256((ROOT/o['path']).read_bytes()).hexdigest(),o['sha256'])
if __name__=='__main__':unittest.main()
