import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
PREFIX = "emerald"
SLUGS = ("reset", "start", "stop", "set-to-max")
NAMES = (
    "PlayTimeCounter_Reset",
    "PlayTimeCounter_Start",
    "PlayTimeCounter_Stop",
    "PlayTimeCounter_SetToMax",
)


class PlayTimeCounterControlsReconstructionTests(unittest.TestCase):
    def setUp(self):
        self.map = json.loads(
            (ROOT / f"analysis/{PREFIX}-jp-play-time-counter-controls-map.json").read_text()
        )
        self.manifest = json.loads(
            (ROOT / "manifests/play-time-counter-controls-reconstruction.json").read_text()
        )
        self.source = (ROOT / "src/play_time_counter.c").read_text()

    def test_cfgs_match_map_without_rom_words(self):
        self.assertEqual([item["name"] for item in self.map["functions"]], list(NAMES))
        for slug, item in zip(SLUGS, self.map["functions"]):
            cfg = json.loads(
                (ROOT / f"analysis/{PREFIX}-jp-play-time-counter-{slug}-cfg.json").read_text()
            )
            self.assertEqual(cfg["start_address"], int(item["address"], 16))
            self.assertEqual(cfg["range_end"], int(item["range_end_exclusive"], 16))
            self.assertEqual(len(cfg["returns"]), 1)
            self.assertTrue(cfg["raw_halfwords_omitted"])
            self.assertTrue(all("halfword" not in instruction for instruction in cfg["instructions"]))
            self.assertFalse(item["rom_code_range"]["raw_bytes_published"])

    def test_only_start_calls_observed_set_to_max(self):
        calls = [item["calls"] for item in self.map["functions"]]
        self.assertEqual([len(value) for value in calls], [0, 1, 0, 0])
        self.assertEqual(calls[1][0]["target"], self.map["functions"][3]["address"])

    def test_source_implements_all_control_states(self):
        for name in NAMES:
            self.assertIn(f"void {name}(void)", self.source)
        self.assertIn("sPlayTimeCounterState = PLAY_TIME_STOPPED;", self.source)
        self.assertIn("sPlayTimeCounterState = PLAY_TIME_RUNNING;", self.source)
        self.assertIn("sPlayTimeCounterState = PLAY_TIME_MAXED_OUT;", self.source)
        self.assertIn("playTimeHours = 999;", self.source)
        self.assertEqual(
            hashlib.sha256((ROOT / "src/play_time_counter.c").read_bytes()).hexdigest(),
            self.map["source_sha256"],
        )

    def test_manifest_hashes_every_output(self):
        self.assertFalse(self.manifest["raw_rom_bytes_included"])
        self.assertEqual(self.manifest["functions"], list(NAMES))
        for output in self.manifest["outputs"]:
            self.assertEqual(
                hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(),
                output["sha256"],
            )


if __name__ == "__main__":
    unittest.main()
