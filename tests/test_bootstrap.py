import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.summary = json.loads((ROOT / "analysis/entry-bootstrap-summary.json").read_text())

    def test_transition_reaches_corresponding_agb_main(self):
        for release in self.summary["releases"]:
            bootstrap = json.loads((ROOT / release["evidence"]["bootstrap"]).read_text())
            cfg = json.loads((ROOT / release["evidence"]["thumb_cfg"]).read_text())
            with self.subTest(release=release["id"]):
                self.assertEqual(bootstrap["transition"]["target_state"], "thumb")
                self.assertEqual(
                    bootstrap["transition"]["target_address"],
                    cfg["function"]["address"],
                )
                code = bootstrap["bootstrap"]["rom_code_range"]
                self.assertEqual(code["length"], code["end_offset_exclusive"] - code["start_offset"])
                self.assertFalse(code["raw_bytes_published"])
                text = json.dumps(bootstrap).lower()
                for forbidden in ("instructions", "instruction_word", '"word"', "raw_target"):
                    self.assertNotIn(forbidden, text)

    def test_manifest_hashes_outputs(self):
        manifest = json.loads((ROOT / "manifests/bootstrap.json").read_text())
        self.assertEqual(manifest["release_count"], self.summary["release_count"])
        for output in manifest["outputs"]:
            self.assertEqual(
                hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(),
                output["sha256"],
            )


if __name__ == "__main__":
    unittest.main()
