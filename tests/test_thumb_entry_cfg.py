import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]


class ThumbEntryCfgTests(unittest.TestCase):
    def setUp(self):
        self.summary = json.loads((ROOT / "analysis/entry-bootstrap-summary.json").read_text())

    def test_cfg_is_compact_and_matches_agb_main(self):
        for release in self.summary["releases"]:
            cfg = json.loads((ROOT / release["evidence"]["thumb_cfg"]).read_text())
            agb_path = ROOT / cfg["cross_reference"]["agb_main_map"]
            agb = json.loads(agb_path.read_text())
            with self.subTest(release=release["id"]):
                self.assertEqual(cfg["function"]["address"], agb["function"]["address"])
                self.assertEqual(
                    cfg["function"]["range_end_exclusive"],
                    agb["function"]["range_end_exclusive"],
                )
                self.assertEqual(
                    cfg["control_flow"]["direct_call_count"],
                    len(agb["direct_calls"]),
                )
                self.assertEqual(cfg["control_flow"]["return_count"], 0)
                self.assertEqual(
                    cfg["control_flow"]["loop_back_edge"],
                    agb["function"]["loop_back_edge"],
                )
                self.assertEqual(
                    hashlib.sha256(agb_path.read_bytes()).hexdigest(),
                    cfg["cross_reference"]["agb_main_map_sha256"],
                )
                text = json.dumps(cfg).lower()
                for forbidden in ('"instructions"', '"halfword":', "instruction_word", "raw_hex"):
                    self.assertNotIn(forbidden, text)

    def test_manifest_hashes_outputs(self):
        manifest = json.loads((ROOT / "manifests/thumb-entry-cfg.json").read_text())
        self.assertEqual(manifest["release_count"], self.summary["release_count"])
        for output in manifest["outputs"]:
            self.assertEqual(
                hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(),
                output["sha256"],
            )


if __name__ == "__main__":
    unittest.main()
