import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
COUNT = 6


class SetMainCallback2CatalogTests(unittest.TestCase):
    def test_release_catalog(self):
        summary = json.loads((ROOT / "analysis/set-main-callback2-catalog-summary.json").read_text())
        catalog = json.loads((ROOT / "analysis/global-release-catalog.json").read_text())
        self.assertEqual((summary["release_count"], len(catalog["releases"])), (COUNT, COUNT))
        self.assertEqual(summary["proven_callback2_offset"], 4)
        self.assertEqual(summary["observed_state_offsets"], [0x438])
        self.assertEqual(sum(item["origin_reference"] for item in summary["releases"]), 1)
        for item in summary["releases"]:
            mapping = json.loads((ROOT / item["evidence"]["map"]).read_text())
            cfg = json.loads((ROOT / item["evidence"]["cfg"]).read_text())
            self.assertEqual(mapping["target"]["sha256"], item["sha256"])
            self.assertEqual(mapping["state"]["callback2_offset"], 4)
            self.assertEqual((mapping["state"]["state_offset"], mapping["state"]["state_value"]), (0x438, 0))
            self.assertEqual((cfg["raw_halfwords_omitted"], len(cfg["calls"]), len(cfg["returns"])), (True, 0, 1))
            self.assertFalse(mapping["raw_rom_bytes_included"])

    def test_manifest(self):
        manifest = json.loads((ROOT / "manifests/set-main-callback2-catalog-reconstruction.json").read_text())
        for output in manifest["outputs"]:
            self.assertEqual(hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(), output["sha256"])


if __name__ == "__main__":
    unittest.main()
