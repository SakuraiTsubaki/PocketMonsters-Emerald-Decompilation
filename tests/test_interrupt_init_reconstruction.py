import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class InterruptInitReconstructionTests(unittest.TestCase):
    def test_every_catalog_release_has_publication_safe_evidence(self):
        catalog = load("analysis/global-release-catalog.json")
        summary = load("analysis/interrupt-init-summary.json")
        self.assertEqual(summary["release_count"], len(catalog["releases"]))
        self.assertEqual(summary["origin_reference"], catalog["releases"][0]["id"])
        self.assertEqual(catalog["releases"][0]["language"], "Japanese")
        self.assertEqual([item["id"] for item in summary["releases"]],
                         [item["id"] for item in catalog["releases"]])
        source_sha256 = hashlib.sha256((ROOT / summary["source"]).read_bytes()).hexdigest()
        expected = ["InitIntrHandlers", "SetVBlankCallback", "SetHBlankCallback",
                    "SetVCountCallback"]
        if summary["profile"] == "emerald":
            expected.append("RestoreSerialTimer3IntrHandlers")
        expected.append("SetSerialCallback")
        for release in summary["releases"]:
            mapping = load(release["evidence"]["map"])
            self.assertEqual(mapping["target"]["release"], release["id"])
            self.assertEqual(mapping["target"]["sha256"], release["sha256"])
            self.assertEqual(mapping["source_sha256"], source_sha256)
            self.assertEqual([item["name"] for item in mapping["functions"]], expected)
            self.assertEqual(mapping["dma"],
                             {"channel": 3, "byte_count": 2048, "control": "0x84000200"})
            self.assertEqual(mapping["literal_addresses"]["DMA3"], "0x040000D4")
            self.assertEqual(mapping["literal_addresses"]["INTR_VECTOR"], "0x03007FFC")
            self.assertEqual(int(mapping["literal_addresses"]["gIntrTable"], 16) + 0x40,
                             int(mapping["literal_addresses"]["IntrMain_Buffer"], 16))
            self.assertEqual(mapping["serial_timer3_restore"], summary["profile"] == "emerald")
            self.assertFalse(mapping["raw_rom_bytes_included"])
            for function in mapping["functions"]:
                self.assertFalse(function["rom_code_range"]["raw_bytes_published"])
                self.assertEqual(len(function["rom_code_range"]["sha256"]), 64)
                self.assertTrue(function["control_flow"]["raw_halfwords_omitted"])

    def test_source_preserves_profile_specific_vblank_setup(self):
        summary = load("analysis/interrupt-init-summary.json")
        source = (ROOT / summary["source"]).read_text(encoding="utf-8")
        self.assertIn("i < 14", source)
        self.assertIn("sizeof(IntrMain_Buffer) / 4", source)
        if summary["profile"] == "rs":
            self.assertIn("REG_DISPSTAT = DISPSTAT_VBLANK_INTR", source)
            self.assertNotIn("EnableInterrupts", source)
        else:
            self.assertIn("EnableInterrupts(INTR_FLAG_VBLANK)", source)
        if summary["profile"] == "emerald":
            self.assertIn("RestoreSerialTimer3IntrHandlers", source)
        else:
            self.assertNotIn("RestoreSerialTimer3IntrHandlers", source)

    def test_manifest_hashes_every_declared_output(self):
        manifest = load("manifests/interrupt-init-reconstruction.json")
        self.assertEqual(manifest["release_count"],
                         load("analysis/interrupt-init-summary.json")["release_count"])
        self.assertEqual(manifest["generator"]["tool"], "tools/interrupt_init_catalog.py")
        self.assertFalse(manifest["raw_rom_bytes_included"])
        for output in manifest["outputs"]:
            self.assertEqual(hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(),
                             output["sha256"])


if __name__ == "__main__":
    unittest.main()
