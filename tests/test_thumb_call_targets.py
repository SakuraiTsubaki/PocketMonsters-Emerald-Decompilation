from __future__ import annotations
import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ThumbCallTargetsTests(unittest.TestCase):
 def test_target_census(self):
  r=json.loads((ROOT/"analysis"/"emerald-jp-thumb-call-targets.json").read_text());self.assertEqual((r["call_sites"],r["unique_targets"],r["repeated_targets"]),(29,27,1));self.assertTrue(all(x["in_rom"] for x in r["targets"]));self.assertEqual([(x["target_address"],x["call_count"]) for x in r["targets"] if x["call_count"]>1],[(0x080004C4,3)])
 def test_manifest_hash(self):
  m=json.loads((ROOT/"manifests"/"thumb-call-targets.json").read_text());o=m["outputs"][0];self.assertEqual(hashlib.sha256((ROOT/o["path"]).read_bytes()).hexdigest(),o["sha256"])
if __name__=="__main__":unittest.main()
