import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
COUNT = 6
MODE = "volatile-poll"
LEGACY_MAP = "analysis/emerald-jp-wait-for-vblank-map.json"
MASK_ADDRESS = "0x080008D8"


class WaitForVBlankCatalogTests(unittest.TestCase):
    def test_release_catalog(self):
        summary = json.loads((ROOT / "analysis/wait-for-vblank-catalog-summary.json").read_text())
        catalog = json.loads((ROOT / "analysis/global-release-catalog.json").read_text())
        self.assertEqual((summary["release_count"], len(catalog["releases"])), (COUNT, COUNT))
        self.assertEqual(summary["intr_check_offset"], 0x1C)
        self.assertEqual(sum(item["origin_reference"] for item in summary["releases"]), 1)
        self.assertEqual({item["wait_mode"] for item in summary["releases"]}, {MODE})
        for item in summary["releases"]:
            mapping = json.loads((ROOT / item["evidence"]["map"]).read_text())
            cfg = json.loads((ROOT / item["evidence"]["cfg"]).read_text())
            self.assertEqual(mapping["target"]["sha256"], item["sha256"])
            self.assertEqual(mapping["state"], {"intrCheck_offset": 0x1C, "cleared_mask": 1})
            self.assertEqual((cfg["raw_halfwords_omitted"], len(cfg["calls"]), len(cfg["returns"])), (True, 0, 1))
            self.assertFalse(mapping["raw_rom_bytes_included"])

    def test_legacy_origin_literal_is_recalculated(self):
        mapping = json.loads((ROOT / LEGACY_MAP).read_text())
        self.assertEqual(mapping["literal_addresses"]["clear_mask"], MASK_ADDRESS)

    def test_manifest(self):
        manifest = json.loads((ROOT / "manifests/wait-for-vblank-catalog-reconstruction.json").read_text())
        for output in manifest["outputs"]:
            self.assertEqual(hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(), output["sha256"])


if __name__ == "__main__":
    unittest.main()
