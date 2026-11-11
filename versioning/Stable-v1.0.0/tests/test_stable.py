from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from vulcan_ecosystem.generator import realize_project
from vulcan_ecosystem.minerva import load_project
from vulcan_ecosystem.validation import validate_project


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ("minimal", "composition", "task-board")


class StableContractTests(unittest.TestCase):
    def test_all_examples_validate(self):
        for name in EXAMPLES:
            with self.subTest(name=name):
                self.assertEqual(validate_project(ROOT / "examples" / name)["errors"], [])

    def test_every_generation_target_has_exact_mapping(self):
        for name in EXAMPLES:
            root = ROOT / "examples" / name
            project = load_project(root / "docs" / "L2_MinervaBlueprints")
            realization = json.loads((root / "docs" / "L3_Vulcan" / "realization.json").read_text(encoding="utf-8"))
            expected = {
                module.module_id
                for module in project.modules
                if module.generation.get("mode") in {"code", "test"}
            }
            actual = {mapping["minerva_module_id"] for mapping in realization["modules"]}
            self.assertEqual(actual, expected)

    def test_boundary_and_observation_point_terms_are_distinct(self):
        for name in EXAMPLES:
            project = load_project(ROOT / "examples" / name / "docs" / "L2_MinervaBlueprints")
            for module in project.modules:
                if module.kind == "boundary":
                    self.assertEqual(
                        module.design["boundary_semantics"],
                        "Interaction interface only; never a test case or observation point.",
                    )
                if module.kind == "behavioral_test":
                    for scenario in module.design["scenarios"]:
                        self.assertIn("observation_points", scenario)
                        self.assertNotIn("boundary", scenario)

    def test_concrete_tools_have_complete_abstract_lineage(self):
        for name in EXAMPLES:
            project = load_project(ROOT / "examples" / name / "docs" / "L2_MinervaBlueprints")
            abstracts = {module.module_id for module in project.modules if module.kind == "abstract_tool"}
            for module in project.modules:
                if module.kind == "concrete_tool":
                    self.assertEqual(module.design["design_status"], "complete")
                    self.assertTrue(set(module.design["implements"]) <= abstracts)

    def test_generation_is_idempotent_for_managed_files(self):
        root = ROOT / "examples" / "minimal"
        first = realize_project(root)
        second = realize_project(root)
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()

