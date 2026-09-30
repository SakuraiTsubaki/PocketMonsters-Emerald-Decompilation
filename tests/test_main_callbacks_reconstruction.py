from __future__ import annotations

import json
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MainCallbacksReconstructionTests(unittest.TestCase):
    def setUp(self):
        self.mapping = json.loads((ROOT / "analysis" / "emerald-jp-main-callbacks-map.json").read_text())
        self.cfg = json.loads((ROOT / "analysis" / "emerald-jp-callee-080004c4.json").read_text())
        self.source = (ROOT / "src" / "main_callbacks.c").read_text()

    def test_ranges_and_cfg_targets_agree(self):
        functions = {item["name"]: item for item in self.mapping["functions"]}
        self.assertEqual(functions["UpdateLinkAndCallCallbacks"]["address"], self.cfg["start_address"])
        cfg_targets = {call["target"] for call in self.cfg["calls"]}
        self.assertTrue(set(functions["UpdateLinkAndCallCallbacks"]["direct_callees"]).issubset(cfg_targets))
        self.assertIn(functions["CallCallbacks"]["address"], cfg_targets)
        self.assertIn(functions["SetMainCallback2"]["address"], cfg_targets)

    def test_proven_offsets_are_not_speculatively_named(self):
        setter = self.mapping["functions"][2]
        self.assertEqual([store["offset"] for store in setter["stores"]], [4, 0x438])
        self.assertIn("unknown_008[0x430]", self.source)
        self.assertIn("gMain.state = 0", self.source)

    def test_source_has_three_reconstructed_functions(self):
        for name in ("UpdateLinkAndCallCallbacks", "CallCallbacks", "SetMainCallback2"):
            self.assertIn(name + "(", self.source)
        self.assertFalse(self.mapping["naming_basis"]["raw_rom_bytes_published"])

    def test_manifest_hashes_all_reconstruction_outputs(self):
        manifest = json.loads((ROOT / "manifests" / "main-callbacks-reconstruction.json").read_text())
        for output in manifest["outputs"]:
            digest = hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest()
            self.assertEqual(digest, output["sha256"], output["path"])


if __name__ == "__main__":
    unittest.main()
