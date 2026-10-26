import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]


class EnableVCountIntrReconstructionTests(unittest.TestCase):
    def test_all_catalog_releases(self):
        catalog = json.loads((ROOT / "analysis/global-release-catalog.json").read_text(encoding="utf-8"))
        summary = json.loads((ROOT / "analysis/enable-vcount-intr-at-line150-summary.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["release_count"], len(catalog["releases"]))
        self.assertEqual(summary["origin_reference"], catalog["releases"][0]["id"])
        for release in catalog["releases"]:
            release_id = release["id"]
            mapping = json.loads((ROOT / f"analysis/{release_id}-enable-vcount-intr-at-line150-map.json").read_text(encoding="utf-8"))
            cfg = json.loads((ROOT / f"analysis/{release_id}-enable-vcount-intr-at-line150-cfg.json").read_text(encoding="utf-8"))
            self.assertEqual(mapping["target"]["sha256"], release["sha256"])
            self.assertEqual([call["name"] for call in mapping["calls"]], ["GetGpuReg", "SetGpuReg", "EnableInterrupts"])
            self.assertEqual(mapping["function"]["rom_code_range"]["length"], 40)
            self.assertEqual(mapping["behavior"]["vcount_compare_line"], 150)
            self.assertTrue(cfg["raw_halfwords_omitted"])
            self.assertFalse(mapping["raw_rom_bytes_included"])

    def test_source_and_manifest(self):
        source = (ROOT / "src/enable_vcount_intr_at_line150.c").read_text(encoding="utf-8")
        self.assertIn("VCOUNT_COMPARE_LINE = 150", source)
        manifest = json.loads((ROOT / "manifests/enable-vcount-intr-at-line150-reconstruction.json").read_text(encoding="utf-8"))
        self.assertFalse(manifest["raw_rom_bytes_included"])
        for output in manifest["outputs"]:
            self.assertEqual(hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(), output["sha256"])


if __name__ == "__main__":
    unittest.main()

