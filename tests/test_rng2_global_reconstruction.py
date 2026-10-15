import hashlib,json,unittest
from pathlib import Path
R=Path(__file__).parents[1]
E={'jp':('Japanese','0x0806F094','0x0806F0A4','0x03005AE4'),'en':('English','0x0806F610','0x0806F620','0x03005D84'),'de':('German','0x0806F610','0x0806F620','0x03005D84'),'fr':('French','0x0806F60C','0x0806F61C','0x03005D84'),'it':('Italian','0x0806F610','0x0806F620','0x03005D84'),'es':('Spanish','0x0806F60C','0x0806F61C','0x03005D84')}
class T(unittest.TestCase):
 def test_all_six_retail_identities(self):
  cat=json.loads((R/'analysis/global-release-catalog.json').read_text());langs={x['language']:x for x in cat['releases']};self.assertEqual(set(langs),{v[0]for v in E.values()})
  for code,(language,seed,random,state) in E.items():
   rel=langs[language];m=json.loads((R/f'analysis/emerald-{code}-rng2-map.json').read_text());self.assertEqual(m['target'],{'release':rel['id'],'sha256':rel['sha256']});self.assertEqual(m['globals'],{'gRng2Value':state});self.assertEqual(m['algorithm'],{'state_bits':32,'multiplier':1103515245,'increment':24691,'return_bits':'state[31:16]','independent_from_primary':True});self.assertEqual(m['functions']['SeedRng2']['address'],seed);self.assertEqual(m['functions']['Random2']['address'],random)
   for name,slug,address in (('SeedRng2','seed-rng2',seed),('Random2','random2',random)):
    cfg=json.loads((R/f'analysis/emerald-{code}-{slug}-cfg.json').read_text());self.assertEqual(cfg['source_sha256'],rel['sha256']);self.assertTrue(cfg['raw_halfwords_omitted']);self.assertEqual((len(cfg['returns']),cfg['calls']),(1,[]));self.assertEqual(cfg['range_start'],int(address,16));self.assertEqual(cfg['range_end'],int(m['functions'][name]['range_end_exclusive'],16))
 def test_source_contains_independent_stream(self):
  s=(R/'src/random.c').read_text();self.assertIn('uint32_t gRng2Value;',s);self.assertIn('void SeedRng2(uint16_t seed)',s);self.assertIn('uint16_t Random2(void)',s);self.assertIn('gRng2Value = ISO_RANDOMIZE1(gRng2Value);',s)
 def test_manifest(self):
  m=json.loads((R/'manifests/rng2-global-reconstruction.json').read_text());self.assertFalse(m['raw_rom_bytes_included']);[self.assertEqual(hashlib.sha256((R/o['path']).read_bytes()).hexdigest(),o['sha256'])for o in m['outputs']]
if __name__=='__main__':unittest.main()
