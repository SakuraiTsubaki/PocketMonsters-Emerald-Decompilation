import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class MapMusicMainTests(unittest.TestCase):
    def test_every_release_has_eight_case_state_machine(self):
        summary = load("analysis/map-music-summary.json")
        expected_calls = ["PlayBGM", "IsBGMStopped", "IsBGMStopped",
                          "IsFanfareTaskInactive", "PlayBGM", "IsBGMStopped",
                          "IsFanfareTaskInactive", "FadeInNewBGM"]
        source_sha = hashlib.sha256((ROOT / "src/map_music_main.c").read_bytes()).hexdigest()
        for release in summary["releases"]:
            mapping = load(release["evidence"]["main"])
            self.assertEqual(mapping["source_sha256"], source_sha)
            self.assertEqual(mapping["function"]["name"], "MapMusicMain")
            self.assertEqual(mapping["behavior"]["state_cases"], list(range(8)))
            self.assertEqual(mapping["behavior"]["shared_idle_target_cases"], [0, 2, 3, 4])
            self.assertEqual(list(mapping["jump_table"]["cases"]), [str(i) for i in range(8)])
            self.assertEqual([item["name"] for item in mapping["calls"]], expected_calls)
            cases = mapping["jump_table"]["cases"]
            self.assertEqual(cases["0"], cases["2"])
            self.assertEqual(cases["0"], cases["3"])
            self.assertEqual(cases["0"], cases["4"])
            self.assertFalse(mapping["raw_rom_bytes_included"])
            self.assertTrue(mapping["function"]["control_flow"]["raw_halfwords_omitted"])

    def test_source_and_manifest(self):
        source = (ROOT / "src/map_music_main.c").read_text(encoding="utf-8")
        self.assertIn("switch (sMapMusicState)", source)
        self.assertIn("case 7:", source)
        self.assertIn("FadeInNewBGM", source)
        manifest = load("manifests/map-music-main-reconstruction.json")
        self.assertEqual(manifest["release_count"],
                         load("analysis/map-music-summary.json")["release_count"])
        self.assertEqual(manifest["generator"]["tool"], "tools/map_music_catalog.py")
        self.assertFalse(manifest["raw_rom_bytes_included"])
        for output in manifest["outputs"]:
            self.assertEqual(hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(),
                             output["sha256"])


if __name__ == "__main__":
    unittest.main()

