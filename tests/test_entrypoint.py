import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]


class EntrypointTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((ROOT / "analysis/global-release-catalog.json").read_text())
        self.summary = json.loads((ROOT / "analysis/entry-bootstrap-summary.json").read_text())

    def test_every_catalog_release_has_raw_free_entry_evidence(self):
        self.assertEqual(
            [item["id"] for item in self.summary["releases"]],
            [item["id"] for item in self.catalog["releases"]],
        )
        self.assertEqual(self.catalog["releases"][0]["language"], "Japanese")
        for release in self.summary["releases"]:
            evidence = json.loads((ROOT / release["evidence"]["entrypoint"]).read_text())
            self.assertEqual(evidence["target"]["release"], release["id"])
            self.assertEqual(evidence["entry"]["address"], "0x08000000")
            self.assertEqual(evidence["entry"]["state"], "arm")
            self.assertEqual(evidence["entry"]["operation"], "b")
            self.assertFalse(evidence["entry"]["rom_code_range"]["raw_bytes_published"])
            text = json.dumps(evidence).lower()
            self.assertNotIn("instruction_word", text)
            self.assertNotIn("raw_hex", text)

    def test_source_is_semantic_and_manifest_hashes_outputs(self):
        source = (ROOT / self.summary["source"]).read_text()
        self.assertIn("b ArmBootstrap", source)
        self.assertNotIn(".word", source)
        manifest = json.loads((ROOT / "manifests/entrypoint.json").read_text())
        self.assertEqual(manifest["release_count"], len(self.catalog["releases"]))
        for output in manifest["outputs"]:
            self.assertEqual(
                hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(),
                output["sha256"],
            )


if __name__ == "__main__":
    unittest.main()
