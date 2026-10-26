import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
COUNT = 6
VARIANT = "rtc-full-reset"
RESET_MASK = "0xFF"
CALL_COUNT = 4


class DoSoftResetCatalogTests(unittest.TestCase):
    def test_release_catalog(self):
        summary = json.loads((ROOT / "analysis/do-soft-reset-catalog-summary.json").read_text())
        catalog = json.loads((ROOT / "analysis/global-release-catalog.json").read_text())
        self.assertEqual((summary["release_count"], len(catalog["releases"])), (COUNT, COUNT))
        self.assertEqual(sum(item["origin_reference"] for item in summary["releases"]), 1)
        self.assertEqual({item["variant"] for item in summary["releases"]}, {VARIANT})
        for item in summary["releases"]:
            mapping = json.loads((ROOT / item["evidence"]["map"]).read_text())
            cfg = json.loads((ROOT / item["evidence"]["cfg"]).read_text())
            self.assertEqual(mapping["target"]["sha256"], item["sha256"])
            self.assertEqual(mapping["behavior"]["soft_reset_mask"], RESET_MASK)
            self.assertEqual(mapping["hardware_writes"]["dma_control_high"], ["0x040000C6", "0x040000D2", "0x040000DE"])
            self.assertEqual((cfg["raw_halfwords_omitted"], len(cfg["calls"]), len(cfg["returns"])), (True, CALL_COUNT, 1))
            self.assertFalse(mapping["raw_rom_bytes_included"])

    def test_manifest(self):
        manifest = json.loads((ROOT / "manifests/do-soft-reset-catalog-reconstruction.json").read_text())
        for output in manifest["outputs"]:
            self.assertEqual(hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(), output["sha256"])


if __name__ == "__main__":
    unittest.main()
