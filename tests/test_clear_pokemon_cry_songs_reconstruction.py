import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).parents[1];COUNT=6
class T(unittest.TestCase):
 def test_catalog(self):
  s=json.loads((ROOT/'analysis/clear-pokemon-cry-songs-summary.json').read_text());c=json.loads((ROOT/'analysis/global-release-catalog.json').read_text());self.assertEqual((s['release_count'],len(c['releases']),s['cleared_byte_count']),(COUNT,COUNT,104));self.assertEqual(sum(x['origin_reference'] for x in s['releases']),1)
  for x in s['releases']:
   m=json.loads((ROOT/x['evidence']['map']).read_text());g=json.loads((ROOT/x['evidence']['cfg']).read_text());self.assertEqual((m['target']['sha256'],m['behavior']['halfword_count'],m['state']['byte_count']),(x['sha256'],52,104));self.assertEqual((g['raw_halfwords_omitted'],len(g['calls']),len(g['returns'])),(True,1,1));self.assertFalse(m['raw_rom_bytes_included'])
 def test_manifest(self):
  m=json.loads((ROOT/'manifests/clear-pokemon-cry-songs-reconstruction.json').read_text());[self.assertEqual(hashlib.sha256((ROOT/o['path']).read_bytes()).hexdigest(),o['sha256']) for o in m['outputs']]
if __name__=='__main__':unittest.main()
