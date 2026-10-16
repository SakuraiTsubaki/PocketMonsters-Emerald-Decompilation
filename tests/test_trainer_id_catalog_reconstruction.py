import hashlib,json,unittest
from pathlib import Path
R=Path(__file__).parents[1];COUNT=6;NAMES=['SetTrainerId','GetTrainerId','CopyTrainerId']
class T(unittest.TestCase):
 def test_catalog(self):
  s=json.loads((R/'analysis/trainer-id-catalog-summary.json').read_text());c=json.loads((R/'analysis/global-release-catalog.json').read_text());self.assertEqual((s['release_count'],len(c['releases'])),(COUNT,COUNT));self.assertEqual((s['functions'],sum(x['origin_reference'] for x in s['releases'])),(NAMES,1))
  for x in s['releases']:
   m=json.loads((R/x['evidence']['map']).read_text());self.assertEqual((m['target']['sha256'],m['byte_order'],[f['name'] for f in m['functions']]),(x['sha256'],'little-endian',NAMES))
   for f,p in zip(m['functions'],x['evidence']['cfgs']):
    cfg=json.loads((R/p).read_text());self.assertEqual((cfg['source_sha256'],cfg['raw_halfwords_omitted'],len(cfg['returns']),cfg['calls']),(x['sha256'],True,1,[]));self.assertEqual((cfg['range_start'],cfg['range_end']),(int(f['address'],16),int(f['range_end_exclusive'],16)))
 def test_manifest(self):
  m=json.loads((R/'manifests/trainer-id-catalog-reconstruction.json').read_text());[self.assertEqual(hashlib.sha256((R/o['path']).read_bytes()).hexdigest(),o['sha256'])for o in m['outputs']]
if __name__=='__main__':unittest.main()
