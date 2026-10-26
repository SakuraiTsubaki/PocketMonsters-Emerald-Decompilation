import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]


class AgbMainReconstructionTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads(
            (ROOT / "analysis/global-release-catalog.json").read_text(encoding="utf-8")
        )
        self.profile = json.loads(
            (ROOT / "analysis/agb-main-profile.json").read_text(encoding="utf-8")
        )
        self.summary = json.loads(
            (ROOT / "analysis/agb-main-summary.json").read_text(encoding="utf-8")
        )

    def maps(self):
        for release in self.summary["releases"]:
            yield release, json.loads(
                (ROOT / release["evidence"]).read_text(encoding="utf-8")
            )

    def variants(self):
        return {item["id"]: item for item in self.profile["variants"]}

    def test_every_catalog_release_has_evidence_in_priority_order(self):
        self.assertEqual(
            [item["id"] for item in self.summary["releases"]],
            [item["id"] for item in self.catalog["releases"]],
        )
        self.assertEqual(self.summary["release_count"], len(self.catalog["releases"]))
        self.assertEqual(self.catalog["releases"][0]["language"], "Japanese")
        self.assertEqual(self.summary["origin_reference"], self.catalog["releases"][0]["id"])

    def test_entry_chain_reaches_nonreturning_agb_main(self):
        for release, address_map in self.maps():
            with self.subTest(release=release["id"]):
                self.assertEqual(
                    address_map["entry_chain"]["thumb_transition_target"],
                    address_map["function"]["address"],
                )
                self.assertTrue(address_map["function"]["nonreturning"])
                self.assertFalse(address_map["control_flow"]["return_observed"])
                edge = address_map["function"]["loop_back_edge"]
                self.assertLess(int(edge["target"], 16), int(edge["source"], 16))

    def test_call_names_and_target_equivalence_are_preserved(self):
        variants = self.variants()
        for release, address_map in self.maps():
            with self.subTest(release=release["id"]):
                variant = variants[address_map["profile_variant"]]
                self.assertIn(release["id"], variant["release_ids"])
                names = variant["call_names"]
                calls = address_map["direct_calls"]
                self.assertEqual([item["name"] for item in calls], names)
                self.assertEqual(
                    address_map["control_flow"]["target_equivalence"],
                    variant["signature"]["target_equivalence"],
                )

    def test_ranges_have_hashes_without_raw_rom_material(self):
        for release, address_map in self.maps():
            with self.subTest(release=release["id"]):
                code = address_map["function"]["rom_code_range"]
                self.assertEqual(
                    code["length"],
                    code["end_offset_exclusive"] - code["start_offset"],
                )
                self.assertEqual(len(code["sha256"]), 64)
                self.assertFalse(code["raw_bytes_published"])
                self.assertFalse(address_map["raw_rom_bytes_included"])
                text = json.dumps(address_map).lower()
                for forbidden in ("halfword\"", "instruction_word", "raw_hex", "bytes_hex"):
                    self.assertNotIn(forbidden, text)

    def test_source_and_manifest_cover_all_outputs(self):
        source = (ROOT / self.profile["source"]).read_text(encoding="utf-8")
        names = {
            name
            for variant in self.profile["variants"]
            for name in variant["call_names"]
        }
        for name in names:
            self.assertIn(name, source)
        manifest = json.loads(
            (ROOT / "manifests/agb-main-reconstruction.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["release_count"], len(self.catalog["releases"]))
        for output in manifest["outputs"]:
            self.assertEqual(
                hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(),
                output["sha256"],
            )


if __name__ == "__main__":
    unittest.main()
