import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
PREFIX = "emerald"
SLUGS = ['set-trainer-id','get-trainer-id','copy-trainer-id']
NAMES = ['SetTrainerId','GetTrainerId','CopyTrainerId']


class TrainerIdHelpersReconstructionTests(unittest.TestCase):
    def setUp(self):
        self.map = json.loads(
            (ROOT / f"analysis/{PREFIX}-jp-trainer-id-helpers-map.json").read_text()
        )
        self.manifest = json.loads(
            (ROOT / "manifests/trainer-id-helpers-reconstruction.json").read_text()
        )
        self.source = (ROOT / "src/trainer_id.c").read_text()

    def test_cfgs_match_map_and_publish_no_words(self):
        self.assertEqual([item["name"] for item in self.map["functions"]], NAMES)
        for slug, item in zip(SLUGS, self.map["functions"]):
            cfg = json.loads((ROOT / f"analysis/{PREFIX}-jp-{slug}-cfg.json").read_text())
            self.assertEqual(cfg["start_address"], int(item["address"], 16))
            self.assertEqual(cfg["range_end"], int(item["range_end_exclusive"], 16))
            self.assertEqual(len(cfg["returns"]), 1)
            self.assertEqual(cfg["calls"], [])
            self.assertTrue(cfg["raw_halfwords_omitted"])
            self.assertTrue(all("halfword" not in value for value in cfg["instructions"]))
            self.assertFalse(item["rom_code_range"]["raw_bytes_published"])

    def test_source_preserves_four_byte_little_endian_behavior(self):
        for name in NAMES:
            self.assertIn(name, self.source)
        self.assertIn(">> 8", self.source)
        self.assertIn(">> 16", self.source)
        self.assertIn(">> 24", self.source)
        self.assertIn("i < 4", self.source)
        self.assertEqual(self.map["byte_order"], "little-endian")
        self.assertEqual(self.map["trainer_id_length"], 4)
        self.assertEqual(
            hashlib.sha256((ROOT / "src/trainer_id.c").read_bytes()).hexdigest(),
            self.map["source_sha256"],
        )

    def test_manifest_hashes_outputs(self):
        self.assertFalse(self.manifest["raw_rom_bytes_included"])
        for output in self.manifest["outputs"]:
            self.assertEqual(
                hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(),
                output["sha256"],
            )


if __name__ == "__main__":
    unittest.main()
