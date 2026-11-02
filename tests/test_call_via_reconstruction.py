import hashlib,json,pathlib,unittest
ROOT=pathlib.Path(__file__).parents[1]
class T(unittest.TestCase):
 def test_releases(self):
  s=json.loads((ROOT/"analysis/call-via-summary.json").read_text());self.assertEqual(s["release_count"],6);self.assertEqual(s["function_count"],15)
  for r in s["releases"]:
   e=json.loads((ROOT/r["evidence"]).read_text());v=e["verified_layout"];self.assertEqual(v["function_count"],15);self.assertTrue(v["word_aligned"]);self.assertEqual(v["register_ram_reset_to_suite_delta"],40);self.assertGreaterEqual(v["suite_signature_match_count"],1);self.assertTrue(v["selected_by_verified_sdk_layout"]);self.assertEqual(e["functions"]["_call_via_r0"]["branch_exchange_register"],"r0");self.assertEqual(e["functions"]["_call_via_lr"]["branch_exchange_register"],"lr");self.assertFalse(e["raw_rom_bytes_included"])
 def test_manifest(self):
  m=json.loads((ROOT/"manifests/call-via-reconstruction.json").read_text())
  for x in m["outputs"]:self.assertEqual(hashlib.sha256((ROOT/x["path"]).read_bytes()).hexdigest(),x["sha256"])
if __name__=="__main__":unittest.main()
