import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class DisplaySerialInterruptTests(unittest.TestCase):
    def test_every_catalog_release_has_publication_safe_evidence(self):
        catalog = load("analysis/global-release-catalog.json")
        summary = load("analysis/display-serial-interrupt-summary.json")
        self.assertEqual(summary["release_count"], len(catalog["releases"]))
        self.assertEqual(summary["origin_reference"], catalog["releases"][0]["id"])
        self.assertEqual(catalog["releases"][0]["language"], "Japanese")
        self.assertEqual(
            [item["id"] for item in summary["releases"]],
            [item["id"] for item in catalog["releases"]],
        )
        source_sha256 = hashlib.sha256((ROOT / summary["source"]).read_bytes()).hexdigest()
        for release in summary["releases"]:
            mapping = load(release["evidence"]["map"])
            self.assertEqual(mapping["target"]["release"], release["id"])
            self.assertEqual(mapping["target"]["sha256"], release["sha256"])
            self.assertEqual(mapping["source_sha256"], source_sha256)
            self.assertEqual([item["name"] for item in mapping["functions"]],
                             ["HBlankIntr", "VCountIntr", "SerialIntr"])
            self.assertEqual(mapping["interrupt_flags"],
                             {"HBLANK": "0x0002", "VCOUNT": "0x0004", "SERIAL": "0x0080"})
            self.assertEqual(mapping["literal_addresses"]["INTR_CHECK"], "0x03007FF8")
            self.assertFalse(mapping["raw_rom_bytes_included"])
            for function in mapping["functions"]:
                self.assertFalse(function["rom_code_range"]["raw_bytes_published"])
                self.assertEqual(len(function["rom_code_range"]["sha256"]), 64)
                self.assertTrue(function["control_flow"]["raw_halfwords_omitted"])

    def test_source_preserves_profile_specific_behavior(self):
        summary = load("analysis/display-serial-interrupt-summary.json")
        source = (ROOT / summary["source"]).read_text(encoding="utf-8")
        self.assertIn("gMain.hblankCallback();", source)
        self.assertIn("gMain.serialCallback();", source)
        if summary["profile"] == "rs":
            self.assertIn("gMain.vcountCallback();", source)
            self.assertNotIn("m4aSoundVSync", source)
        elif summary["profile"] == "emerald":
            self.assertIn("gMain.vcountCallback();\n    m4aSoundVSync();", source)
        else:
            self.assertEqual(summary["profile"], "frlg")
            self.assertIn("sVcountAtIntr = (uint8_t)REG_VCOUNT;", source)
            self.assertNotIn("gMain.vcountCallback();", source)

    def test_manifest_hashes_every_declared_output(self):
        manifest = load("manifests/display-serial-interrupt-reconstruction.json")
        self.assertEqual(manifest["release_count"],
                         load("analysis/display-serial-interrupt-summary.json")["release_count"])
        self.assertEqual(manifest["generator"]["tool"], "tools/display_interrupt_catalog.py")
        self.assertFalse(manifest["raw_rom_bytes_included"])
        for output in manifest["outputs"]:
            self.assertEqual(hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(),
                             output["sha256"])


if __name__ == "__main__":
    unittest.main()

