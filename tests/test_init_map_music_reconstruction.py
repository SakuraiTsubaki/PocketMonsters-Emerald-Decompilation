import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class InitMapMusicReconstructionTests(unittest.TestCase):
    def setUp(self):
        self.cfg = json.loads((ROOT / "analysis/emerald-jp-init-map-music-cfg.json").read_text())
        self.map = json.loads((ROOT / "analysis/emerald-jp-init-map-music-map.json").read_text())
        self.manifest = json.loads((ROOT / "manifests/init-map-music-reconstruction.json").read_text())
        self.source = (ROOT / "src/init_map_music.c").read_text()

    def test_cfg_map_and_source(self):
        self.assertEqual(self.cfg["source_sha256"], self.map["target"]["sha256"])
        self.assertEqual(self.cfg["start_address"], int(self.map["function"]["address"], 16))
        self.assertEqual(self.cfg["range_end"], int(self.map["function"]["range_end_exclusive"], 16))
        self.assertTrue(self.cfg["return_observed"])
        self.assertTrue(self.cfg["raw_halfwords_omitted"])
        self.assertFalse(self.map["rom_code_range"]["raw_bytes_published"])
        self.assertEqual(self.map["rom_code_range"]["length"], 16)
        self.assertEqual(hashlib.sha256((ROOT / "src/init_map_music.c").read_bytes()).hexdigest(), self.map["source_sha256"])

    def test_behavior_and_single_call(self):
        self.assertEqual([call["name"] for call in self.map["calls"]], ["ResetMapMusic"])
        self.assertEqual(self.cfg["calls"][0]["target"], int(self.map["calls"][0]["target"], 16))
        self.assertIn("gDisableMusic = FALSE;", self.source)
        self.assertIn("ResetMapMusic();", self.source)
        self.assertTrue(self.map["behavior"]["cross_title_code_range_identical"])

    def test_manifest_hashes_outputs(self):
        self.assertFalse(self.manifest["raw_rom_bytes_included"])
        for output in self.manifest["outputs"]:
            self.assertEqual(hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(), output["sha256"])


if __name__ == "__main__":
    unittest.main()

