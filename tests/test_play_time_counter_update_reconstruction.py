import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
PREFIX = "emerald"


class PlayTimeCounterUpdateReconstructionTests(unittest.TestCase):
    def setUp(self):
        self.cfg = json.loads((ROOT / f"analysis/{PREFIX}-jp-play-time-counter-update-cfg.json").read_text())
        self.map = json.loads((ROOT / f"analysis/{PREFIX}-jp-play-time-counter-update-map.json").read_text())
        self.manifest = json.loads((ROOT / "manifests/play-time-counter-update-reconstruction.json").read_text())
        self.source = (ROOT / "src/play_time_counter.c").read_text()

    def test_cfg_map_and_single_call(self):
        self.assertEqual(self.cfg["source_sha256"], self.map["target"]["sha256"])
        self.assertEqual(self.cfg["start_address"], int(self.map["function"]["address"], 16))
        self.assertEqual(self.cfg["range_end"], int(self.map["function"]["range_end_exclusive"], 16))
        self.assertEqual(len(self.cfg["edges"]), 10)
        self.assertEqual(len(self.cfg["returns"]), 1)
        self.assertTrue(self.cfg["raw_halfwords_omitted"])
        self.assertEqual(
            [(item["source"], item["target"]) for item in self.cfg["calls"]],
            [(int(item["address"], 16), int(item["target"], 16)) for item in self.map["calls"]],
        )
        self.assertEqual(self.map["calls"][0]["name"], "PlayTimeCounter_SetToMax")

    def test_behavior_offsets_and_source(self):
        self.assertEqual(self.map["save_field_offsets"], {
            "playTimeHours": 0x0E, "playTimeMinutes": 0x10,
            "playTimeSeconds": 0x11, "playTimeVBlanks": 0x12,
        })
        self.assertEqual(
            [self.map["behavior"][name] for name in (
                "vblanks_per_second", "seconds_per_minute", "minutes_per_hour", "maximum_hours"
            )],
            [60, 60, 60, 999],
        )
        self.assertFalse(self.map["rom_code_range"]["raw_bytes_published"])
        self.assertIn("gSaveBlock2Ptr->playTimeVBlanks", self.source)
        self.assertIn("PlayTimeCounter_SetToMax();", self.source)
        self.assertEqual(hashlib.sha256((ROOT / "src/play_time_counter.c").read_bytes()).hexdigest(), self.map["source_sha256"])

    def test_manifest_hashes_outputs(self):
        self.assertFalse(self.manifest["raw_rom_bytes_included"])
        for output in self.manifest["outputs"]:
            self.assertEqual(hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(), output["sha256"])


if __name__ == "__main__":
    unittest.main()

