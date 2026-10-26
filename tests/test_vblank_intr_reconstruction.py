import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class VBlankIntrReconstructionTests(unittest.TestCase):
    def test_every_catalog_release_has_publication_safe_evidence(self):
        catalog = load("analysis/global-release-catalog.json")
        summary = load("analysis/vblank-intr-summary.json")
        self.assertEqual(summary["release_count"], len(catalog["releases"]))
        self.assertEqual(summary["origin_reference"], catalog["releases"][0]["id"])
        self.assertEqual(catalog["releases"][0]["language"], "Japanese")
        self.assertEqual([item["id"] for item in summary["releases"]],
                         [item["id"] for item in catalog["releases"]])
        expected_calls = 6 if summary["profile"] == "rs" else 9
        source_sha256 = hashlib.sha256((ROOT / summary["source"]).read_bytes()).hexdigest()
        for release in summary["releases"]:
            mapping = load(release["evidence"]["map"])
            self.assertEqual(mapping["target"]["release"], release["id"])
            self.assertEqual(mapping["target"]["sha256"], release["sha256"])
            self.assertEqual(mapping["source_sha256"], source_sha256)
            self.assertEqual(mapping["function"]["name"], "VBlankIntr")
            self.assertEqual(len(mapping["calls"]), expected_calls)
            self.assertEqual(mapping["interrupt_flag"], "0x0001")
            self.assertEqual(mapping["literal_addresses"]["INTR_CHECK"], "0x03007FF8")
            dependency = mapping["evidence_dependency"]
            self.assertEqual(hashlib.sha256((ROOT / dependency["path"]).read_bytes()).hexdigest(),
                             dependency["sha256"])
            self.assertFalse(mapping["raw_rom_bytes_included"])
            self.assertFalse(mapping["function"]["rom_code_range"]["raw_bytes_published"])
            self.assertTrue(mapping["function"]["control_flow"]["raw_halfwords_omitted"])

    def test_source_preserves_profile_specific_behavior(self):
        summary = load("analysis/vblank-intr-summary.json")
        source = (ROOT / summary["source"]).read_text(encoding="utf-8")
        if summary["profile"] == "rs":
            self.assertIn("savedIme = REG_IME", source)
            self.assertNotIn("RfuVSync", source)
        elif summary["profile"] == "emerald":
            self.assertIn("gTrainerHillVBlankCounter", source)
            self.assertIn("BATTLE_RNG_SUPPRESS_MASK", source)
        else:
            self.assertEqual(summary["profile"], "frlg")
            self.assertIn("sVcountBeforeSound", source)
            self.assertIn("sVcountAfterSound", source)

    def test_manifest_hashes_every_declared_output(self):
        manifest = load("manifests/vblank-intr-reconstruction.json")
        self.assertEqual(manifest["release_count"],
                         load("analysis/vblank-intr-summary.json")["release_count"])
        self.assertEqual(manifest["generator"]["tool"], "tools/vblank_intr_catalog.py")
        self.assertFalse(manifest["raw_rom_bytes_included"])
        for output in manifest["outputs"]:
            self.assertEqual(hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(),
                             output["sha256"])


if __name__ == "__main__":
    unittest.main()

