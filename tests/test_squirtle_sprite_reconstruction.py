import hashlib,json,pathlib,struct,unittest
ROOT=pathlib.Path(__file__).parents[1]
class T(unittest.TestCase):
 def test_assets(self):
  s=json.loads((ROOT/"analysis/squirtle-sprite-set-summary.json").read_text());self.assertEqual(s["release_count"],6);self.assertEqual(s["species"],{"id":7,"name":"squirtle"})
  for r in s["releases"]:
   e=json.loads((ROOT/r["evidence"]).read_text());self.assertEqual(e["target"]["sha256"],r["sha256"]);self.assertFalse(e["raw_rom_bytes_included"])
   for key in("front","back"):
    data=(ROOT/r[key]).read_bytes();self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"));self.assertEqual(struct.unpack(">II",data[16:24]),(128,128))
   self.assertTrue((ROOT/r["palette"]).read_bytes().startswith(b"JASC-PAL\n0100\n16\n"))
 def test_manifest(self):
  m=json.loads((ROOT/"manifests/squirtle-sprite-reconstruction.json").read_text())
  for x in m["outputs"]:self.assertEqual(hashlib.sha256((ROOT/x["path"]).read_bytes()).hexdigest(),x["sha256"])
if __name__=="__main__":unittest.main()

