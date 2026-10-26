import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class PlayTimeCounterUpdateTests(unittest.TestCase):
    def test_every_release_has_verified_update_routine(self):
        catalog = load("analysis/global-release-catalog.json")
        summary = load("analysis/play-time-counter-summary.json")
        self.assertEqual(summary["release_count"], len(catalog["releases"]))
        for release in summary["releases"]:
            mapping = load(release["evidence"]["update"])
            controls = load(release["evidence"]["controls"])
            function = mapping["function"]
            self.assertEqual(mapping["target"]["release"], release["id"])
            self.assertEqual(mapping["target"]["sha256"], release["sha256"])
            self.assertEqual(function["name"], "PlayTimeCounter_Update")
            self.assertEqual(len(function["calls"]), 1)
            self.assertEqual(function["calls"][0]["name"], "PlayTimeCounter_SetToMax")
            self.assertEqual(function["calls"][0]["target"],
                             controls["functions"][3]["address"])
            self.assertEqual(mapping["behavior"], {
                "required_state": 1, "vblanks_per_second": 60,
                "seconds_per_minute": 60, "minutes_per_hour": 60,
                "maximum_hours": 999,
            })
            self.assertFalse(mapping["raw_rom_bytes_included"])
            self.assertFalse(function["rom_code_range"]["raw_bytes_published"])
            self.assertTrue(function["control_flow"]["raw_halfwords_omitted"])

    def test_source_contains_nested_counter_thresholds(self):
        source = (ROOT / "src/play_time_counter.c").read_text(encoding="utf-8")
        self.assertIn("sPlayTimeCounterState != PLAY_TIME_RUNNING", source)
        self.assertIn("playTimeVBlanks", source)
        self.assertIn("< 60", source)
        self.assertIn("> 999", source)

    def test_manifest_hashes_outputs(self):
        manifest = load("manifests/play-time-counter-update-reconstruction.json")
        self.assertEqual(manifest["release_count"],
                         load("analysis/play-time-counter-summary.json")["release_count"])
        self.assertEqual(manifest["generator"]["tool"], "tools/play_time_controls.py")
        self.assertFalse(manifest["raw_rom_bytes_included"])
        for output in manifest["outputs"]:
            self.assertEqual(hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(),
                             output["sha256"])


if __name__ == "__main__":
    unittest.main()

