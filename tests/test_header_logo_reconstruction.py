import hashlib,json,pathlib,struct,unittest
ROOT=pathlib.Path(__file__).parents[1]
class T(unittest.TestCase):
 def test_catalog(self):
  s=json.loads((ROOT/"analysis/header-logo-summary.json").read_text());self.assertEqual(s["release_count"],6);self.assertEqual(s["source_sha256"],"08a0153cfd6b0ea54b938f7d209933fa849da0d56f5a34c481060c9ff2fad818")
  png=(ROOT/s["png"]).read_bytes();self.assertTrue(png.startswith(b"\x89PNG\r\n\x1a\n"));self.assertEqual(struct.unpack(">II",png[16:24]),(416,64));self.assertEqual(hashlib.sha256(png).hexdigest(),s["png_sha256"])
  for r in s["releases"]:
   e=json.loads((ROOT/r["evidence"]).read_text());self.assertEqual(e["target"]["sha256"],r["sha256"]);self.assertEqual(e["asset"]["source_offset"],4);self.assertEqual(e["asset"]["source_length"],156);self.assertFalse(e["raw_rom_bytes_included"])
 def test_manifest(self):
  m=json.loads((ROOT/"manifests/header-logo-reconstruction.json").read_text())
  for x in m["outputs"]:self.assertEqual(hashlib.sha256((ROOT/x["path"]).read_bytes()).hexdigest(),x["sha256"])
if __name__=="__main__":unittest.main()
