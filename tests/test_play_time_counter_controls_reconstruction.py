import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class PlayTimeCounterControlsTests(unittest.TestCase):
    def test_every_release_has_four_control_routines(self):
        catalog = load("analysis/global-release-catalog.json")
        summary = load("analysis/play-time-counter-summary.json")
        self.assertEqual(summary["release_count"], len(catalog["releases"]))
        self.assertEqual(summary["origin_reference"], catalog["releases"][0]["id"])
        self.assertEqual(catalog["releases"][0]["language"], "Japanese")
        self.assertEqual([item["id"] for item in summary["releases"]],
                         [item["id"] for item in catalog["releases"]])
        names = ["PlayTimeCounter_Reset", "PlayTimeCounter_Start",
                 "PlayTimeCounter_Stop", "PlayTimeCounter_SetToMax"]
        source_sha = hashlib.sha256((ROOT / summary["source"]).read_bytes()).hexdigest()
        for release in summary["releases"]:
            mapping = load(release["evidence"]["controls"])
            self.assertEqual(mapping["target"]["release"], release["id"])
            self.assertEqual(mapping["target"]["sha256"], release["sha256"])
            self.assertEqual(mapping["source_sha256"], source_sha)
            self.assertEqual([item["name"] for item in mapping["functions"]], names)
            self.assertEqual([len(item["calls"]) for item in mapping["functions"]], [0, 1, 0, 0])
            self.assertEqual(mapping["functions"][1]["calls"][0]["target"],
                             mapping["functions"][3]["address"])
            self.assertFalse(mapping["raw_rom_bytes_included"])
            for function in mapping["functions"]:
                self.assertFalse(function["rom_code_range"]["raw_bytes_published"])
                self.assertTrue(function["control_flow"]["raw_halfwords_omitted"])

    def test_source_preserves_storage_profile(self):
        summary = load("analysis/play-time-counter-summary.json")
        source = (ROOT / summary["source"]).read_text(encoding="utf-8")
        if summary["profile"] == "direct":
            self.assertIn("gSaveBlock2.playTimeHours", source)
            self.assertNotIn("gSaveBlock2Ptr", source)
        else:
            self.assertEqual(summary["profile"], "pointer")
            self.assertIn("gSaveBlock2Ptr->playTimeHours", source)
        self.assertIn("PLAY_TIME_MAXED_OUT", source)

    def test_manifest_hashes_outputs(self):
        manifest = load("manifests/play-time-counter-controls-reconstruction.json")
        self.assertEqual(manifest["release_count"],
                         load("analysis/play-time-counter-summary.json")["release_count"])
        self.assertEqual(manifest["generator"]["tool"], "tools/play_time_controls.py")
        self.assertFalse(manifest["raw_rom_bytes_included"])
        for output in manifest["outputs"]:
            self.assertEqual(hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(),
                             output["sha256"])


if __name__ == "__main__":
    unittest.main()

