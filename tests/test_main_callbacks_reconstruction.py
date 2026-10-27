import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]


class MainCallbacksReconstructionTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads(
            (ROOT / "analysis/global-release-catalog.json").read_text()
        )
        self.summary = json.loads(
            (ROOT / "analysis/main-callbacks-summary.json").read_text()
        )

    def maps(self):
        for release in self.summary["releases"]:
            yield release, json.loads((ROOT / release["evidence"]).read_text())

    def test_every_release_has_four_function_cluster(self):
        self.assertEqual(
            [item["id"] for item in self.summary["releases"]],
            [item["id"] for item in self.catalog["releases"]],
        )
        self.assertEqual(self.catalog["releases"][0]["language"], "Japanese")
        expected = [
            "UpdateLinkAndCallCallbacks", "InitMainCallbacks",
            "CallCallbacks", "SetMainCallback2",
        ]
        for release, address_map in self.maps():
            with self.subTest(release=release["id"]):
                self.assertEqual(
                    [item["name"] for item in address_map["functions"]], expected
                )

    def test_ranges_cfgs_and_cross_references_are_verified(self):
        for release, address_map in self.maps():
            with self.subTest(release=release["id"]):
                functions = {item["name"]: item for item in address_map["functions"]}
                for function in functions.values():
                    code = function["rom_code_range"]
                    self.assertEqual(
                        code["length"],
                        code["end_offset_exclusive"] - code["start_offset"],
                    )
                    self.assertEqual(function["control_flow"]["return_count"], 1)
                    self.assertFalse(code["raw_bytes_published"])
                set_map_path = ROOT / address_map["cross_references"]["set_main_callback2_map"]
                set_map = json.loads(set_map_path.read_text())
                self.assertEqual(
                    functions["SetMainCallback2"]["address"],
                    set_map["function"]["address"],
                )
                self.assertEqual(
                    hashlib.sha256(set_map_path.read_bytes()).hexdigest(),
                    address_map["cross_references"]["set_main_callback2_map_sha256"],
                )

    def test_named_call_relationships_and_raw_free_maps(self):
        for release, address_map in self.maps():
            with self.subTest(release=release["id"]):
                functions = {item["name"]: item for item in address_map["functions"]}
                self.assertEqual(
                    functions["UpdateLinkAndCallCallbacks"]["calls"][-1]["name"],
                    "CallCallbacks",
                )
                self.assertEqual(
                    functions["InitMainCallbacks"]["calls"][-1]["name"],
                    "SetMainCallback2",
                )
                self.assertEqual(functions["SetMainCallback2"]["calls"], [])
                text = json.dumps(address_map).lower()
                for forbidden in ('"instructions"', '"halfword":', "instruction_word", "raw_hex"):
                    self.assertNotIn(forbidden, text)

    def test_sources_and_manifest_hashes(self):
        for source in self.summary["sources"]:
            self.assertTrue((ROOT / source).is_file())
        manifest = json.loads(
            (ROOT / "manifests/main-callbacks-reconstruction.json").read_text()
        )
        self.assertEqual(manifest["release_count"], len(self.catalog["releases"]))
        for output in manifest["outputs"]:
            self.assertEqual(
                hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(),
                output["sha256"],
            )


if __name__ == "__main__":
    unittest.main()
