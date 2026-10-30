import hashlib,json,pathlib,unittest
ROOT=pathlib.Path(__file__).parents[1]
class T(unittest.TestCase):
 def test_releases(self):
  s=json.loads((ROOT/"analysis/register-ram-reset-summary.json").read_text());self.assertEqual(s["release_count"],6)
  for r in s["releases"]:
   e=json.loads((ROOT/r["evidence"]).read_text());self.assertEqual(e["verified_behavior"]["software_interrupt"],1);self.assertFalse(e["raw_rom_bytes_included"])
 def test_manifest(self):
  m=json.loads((ROOT/"manifests/register-ram-reset-reconstruction.json").read_text())
  for x in m["outputs"]:self.assertEqual(hashlib.sha256((ROOT/x["path"]).read_bytes()).hexdigest(),x["sha256"])
if __name__=="__main__":unittest.main()
