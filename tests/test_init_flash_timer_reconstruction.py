import hashlib
import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).parents[1]


class InitFlashTimerReconstructionTests(unittest.TestCase):
    def test_release_matrix_and_calls(self):
        summary = json.loads((ROOT / "analysis/init-flash-timer-summary.json").read_text())
        catalog = json.loads((ROOT / "analysis/global-release-catalog.json").read_text())
        self.assertEqual(summary["release_count"], len(catalog["releases"]))
        self.assertEqual(summary["origin_reference"], catalog["releases"][0]["id"])
        self.assertEqual(catalog["releases"][0]["language"], "Japanese")
        for release in summary["releases"]:
            evidence = json.loads((ROOT / release["evidence"]).read_text())
            self.assertEqual(evidence["target"]["sha256"], release["sha256"])
            self.assertEqual(evidence["function"]["calls"][0]["name"], "SetFlashTimerIntr")
            self.assertEqual(evidence["verified_behavior"]["timer_index"], 2)
            self.assertEqual(evidence["verified_behavior"]["interrupt_table_slot"], 7)
            self.assertTrue(evidence["control_flow"]["raw_halfwords_omitted"])
            self.assertFalse(evidence["raw_rom_bytes_included"])

    def test_manifest_hashes_outputs(self):
        manifest = json.loads((ROOT / "manifests/init-flash-timer-reconstruction.json").read_text())
        for output in manifest["outputs"]:
            self.assertEqual(hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(),
                             output["sha256"])
        self.assertFalse(manifest["raw_rom_bytes_included"])


if __name__ == "__main__":
    unittest.main()

