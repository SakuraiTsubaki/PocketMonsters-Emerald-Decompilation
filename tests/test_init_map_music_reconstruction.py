import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class InitMapMusicTests(unittest.TestCase):
    def test_every_release_has_verified_init(self):
        catalog = load("analysis/global-release-catalog.json")
        summary = load("analysis/map-music-summary.json")
        self.assertEqual(summary["release_count"], len(catalog["releases"]))
        self.assertEqual(summary["origin_reference"], catalog["releases"][0]["id"])
        self.assertEqual(catalog["releases"][0]["language"], "Japanese")
        source_sha = hashlib.sha256((ROOT / "src/init_map_music.c").read_bytes()).hexdigest()
        for release in summary["releases"]:
            mapping = load(release["evidence"]["init"])
            self.assertEqual(mapping["target"]["release"], release["id"])
            self.assertEqual(mapping["target"]["sha256"], release["sha256"])
            self.assertEqual(mapping["source_sha256"], source_sha)
            self.assertEqual(mapping["function"]["name"], "InitMapMusic")
            self.assertEqual([item["name"] for item in mapping["calls"]], ["ResetMapMusic"])
            self.assertTrue(0x03000000 <= int(mapping["literal_addresses"]["gDisableMusic"], 16)
                            <= 0x03007FFF)
            self.assertFalse(mapping["raw_rom_bytes_included"])
            self.assertFalse(mapping["function"]["rom_code_range"]["raw_bytes_published"])
            self.assertTrue(mapping["function"]["control_flow"]["raw_halfwords_omitted"])

    def test_source_and_manifest(self):
        source = (ROOT / "src/init_map_music.c").read_text(encoding="utf-8")
        self.assertIn("gDisableMusic = FALSE", source)
        self.assertIn("ResetMapMusic();", source)
        manifest = load("manifests/init-map-music-reconstruction.json")
        self.assertEqual(manifest["release_count"],
                         load("analysis/map-music-summary.json")["release_count"])
        self.assertEqual(manifest["generator"]["tool"], "tools/map_music_catalog.py")
        self.assertFalse(manifest["raw_rom_bytes_included"])
        for output in manifest["outputs"]:
            self.assertEqual(hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(),
                             output["sha256"])


if __name__ == "__main__":
    unittest.main()

