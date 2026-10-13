import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
PREFIX = "emerald"


class MapMusicMainReconstructionTests(unittest.TestCase):
    def setUp(self):
        self.cfg = json.loads((ROOT / f"analysis/{PREFIX}-jp-map-music-main-cfg.json").read_text())
        self.map = json.loads((ROOT / f"analysis/{PREFIX}-jp-map-music-main-map.json").read_text())
        self.manifest = json.loads((ROOT / "manifests/map-music-main-reconstruction.json").read_text())
        self.source = (ROOT / "src/map_music_main.c").read_text()

    def test_cfg_covers_all_switch_cases(self):
        self.assertEqual(self.cfg["source_sha256"], self.map["target"]["sha256"])
        self.assertEqual(self.cfg["start_address"], int(self.map["function"]["address"], 16))
        self.assertEqual(self.cfg["range_end"], int(self.map["function"]["range_end_exclusive"], 16))
        jump = next(item for item in self.cfg["instructions"] if item["kind"] == "jump-table-branch")
        self.assertEqual(jump["table_address"], int(self.map["jump_table"]["address"], 16))
        self.assertEqual(jump["targets"], [int(self.map["jump_table"]["cases"][str(i)], 16) for i in range(8)])
        self.assertEqual(len([edge for edge in self.cfg["edges"] if edge["kind"] == "jump-table"]), 8)
        self.assertTrue(self.cfg["return_observed"])
        self.assertTrue(self.cfg["raw_halfwords_omitted"])

    def test_calls_source_and_publication_boundary(self):
        cfg_calls = sorted((item["source"], item["target"]) for item in self.cfg["calls"])
        map_calls = [(int(item["address"], 16), int(item["target"], 16)) for item in self.map["calls"]]
        self.assertEqual(cfg_calls, map_calls)
        self.assertEqual([item["name"] for item in self.map["calls"]], [
            "PlayBGM", "IsBGMStopped", "IsBGMStopped", "IsFanfareTaskInactive",
            "PlayBGM", "IsBGMStopped", "IsFanfareTaskInactive", "FadeInNewBGM"
        ])
        self.assertEqual(self.map["rom_code_range"]["length"], 232)
        self.assertFalse(self.map["rom_code_range"]["raw_bytes_published"])
        self.assertEqual(hashlib.sha256((ROOT / "src/map_music_main.c").read_bytes()).hexdigest(), self.map["source_sha256"])
        for token in ("switch (sMapMusicState)", "case 7:", "IsFanfareTaskInactive()", "FadeInNewBGM"):
            self.assertIn(token, self.source)

    def test_manifest_hashes_outputs(self):
        self.assertFalse(self.manifest["raw_rom_bytes_included"])
        for output in self.manifest["outputs"]:
            self.assertEqual(hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(), output["sha256"])


if __name__ == "__main__":
    unittest.main()

