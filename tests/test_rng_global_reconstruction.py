import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
EXPECTED={
'jp':('Japanese','0x0806F050','0x0806F07C','0x03005AE0','0x02024664','0x02024660'),
'en':('English','0x0806F5CC','0x0806F5F8','0x03005D80','0x020249C0','0x020249BC'),
'de':('German','0x0806F5CC','0x0806F5F8','0x03005D80','0x020249C0','0x020249BC'),
'fr':('French','0x0806F5C8','0x0806F5F4','0x03005D80','0x020249C0','0x020249BC'),
'it':('Italian','0x0806F5CC','0x0806F5F8','0x03005D80','0x020249C0','0x020249BC'),
'es':('Spanish','0x0806F5C8','0x0806F5F4','0x03005D80','0x020249C0','0x020249BC')}
class Tests(unittest.TestCase):
 def test_all_established_retail_identities(self):
  catalog=json.loads((ROOT/'analysis/global-release-catalog.json').read_text());by_lang={r['language']:r for r in catalog['releases']};self.assertEqual(set(by_lang),{v[0] for v in EXPECTED.values()})
  for code,(language,random_addr,seed_addr,rng,count,unknown) in EXPECTED.items():
   m=json.loads((ROOT/f'analysis/emerald-{code}-rng-map.json').read_text());rel=by_lang[language];self.assertEqual(m['target']['sha256'],rel['sha256']);self.assertEqual(m['variant'],'emerald');self.assertEqual(m['globals'],{'gRngValue':rng,'sRandCount':count,'sUnknown':unknown});self.assertEqual(m['functions']['Random']['address'],random_addr);self.assertEqual(m['functions']['SeedRng']['address'],seed_addr);self.assertEqual(m['algorithm']['multiplier'],1103515245);self.assertEqual(m['algorithm']['increment'],24691)
   for name,slug,address in (('Random','random',random_addr),('SeedRng','seed-rng',seed_addr)):
    cfg=json.loads((ROOT/f'analysis/emerald-{code}-{slug}-cfg.json').read_text());self.assertEqual(cfg['source_sha256'],rel['sha256']);self.assertTrue(cfg['raw_halfwords_omitted']);self.assertEqual((len(cfg['returns']),cfg['calls']),(1,[]));self.assertEqual(cfg['range_start'],int(address,16));self.assertEqual(cfg['range_end'],int(m['functions'][name]['range_end_exclusive'],16))
 def test_manifest(self):
  m=json.loads((ROOT/'manifests/rng-global-reconstruction.json').read_text());self.assertFalse(m['raw_rom_bytes_included']);[self.assertEqual(hashlib.sha256((ROOT/o['path']).read_bytes()).hexdigest(),o['sha256'])for o in m['outputs']]
if __name__=='__main__':unittest.main()
