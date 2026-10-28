import hashlib
import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).parents[1]


class CheckFlashMemoryReconstructionTests(unittest.TestCase):
    def test_summary_matches_catalog_and_origin(self):
        summary = json.loads((ROOT / "analysis/check-flash-memory-summary.json").read_text())
        catalog = json.loads((ROOT / "analysis/global-release-catalog.json").read_text())
        self.assertEqual(summary["release_count"], len(catalog["releases"]))
        self.assertEqual(summary["origin_reference"], catalog["releases"][0]["id"])
        self.assertEqual(catalog["releases"][0]["language"], "Japanese")
        self.assertFalse(summary["raw_rom_bytes_included"])

    def test_every_release_has_hashed_evidence(self):
        summary = json.loads((ROOT / "analysis/check-flash-memory-summary.json").read_text())
        for release in summary["releases"]:
            evidence = json.loads((ROOT / release["evidence"]).read_text())
            function = evidence["function"]
            self.assertEqual([item["name"] for item in function["calls"]],
                             ["IdentifyFlash", "InitFlashTimer"])
            self.assertEqual(function["rom_code_range"]["length"], 38)
            self.assertFalse(function["rom_code_range"]["raw_bytes_published"])
            self.assertFalse(evidence["raw_rom_bytes_included"])

    def test_manifest_hashes_outputs(self):
        manifest = json.loads((ROOT / "manifests/check-flash-memory-reconstruction.json").read_text())
        self.assertFalse(manifest["raw_rom_bytes_included"])
        for output in manifest["outputs"]:
            data = (ROOT / output["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), output["sha256"])

    def test_source_preserves_success_only_timer_initialization(self):
        source = (ROOT / "src/check_flash_memory.c").read_text()
        self.assertIn("IdentifyFlash() == 0", source)
        self.assertIn("gFlashMemoryPresent = 1", source)
        self.assertIn("InitFlashTimer();", source)
        self.assertIn("gFlashMemoryPresent = 0", source)


if __name__ == "__main__":
    unittest.main()

