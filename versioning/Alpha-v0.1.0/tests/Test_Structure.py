"""Positive, negative and scope checks for the bounded Python assessor."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


EDITION = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("vulcan_assessor", EDITION / "scripts/evaluate_structure.py")
ASSESSOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ASSESSOR)


class Test_Structure(unittest.TestCase):
    def testRunnableExamplePassesWithExplicitScope(self):
        report = ASSESSOR.assess(EDITION / "tests/fixtures/legacy-ecosystem", ["TaskBoard"], ["LegacyReports"],
                                 technical_files=["apps/TaskBoard/main.py"])
        self.assertEqual(report["status"], "passed", report["diagnostics"])
        self.assertEqual(report["scope"]["python_files_parsed"], 14)
        self.assertEqual(report["scope"]["legacy_apps_not_structurally_assessed"], ["LegacyReports"])
        self.assertIn("runtime execution", report["scope"]["not_assessed"])

    def testPublishedCounterexampleProducesAllPromisedDiagnostics(self):
        directory = EDITION / "tests/fixtures/structural-counterexamples"
        expected = json.loads((directory / "expected-diagnostics.json").read_text())
        report = ASSESSOR.assess(directory / expected["fixture"], ["BrokenApp"])
        self.assertEqual(report["status"], expected["expected_status"])
        actual = {finding["rule"] for finding in report["diagnostics"]}
        self.assertTrue(set(expected["required_rules"]).issubset(actual), actual)

    def testMissingRootEntryAndCoreAreasAreDiagnosed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "apps/Empty").mkdir(parents=True)
            report = ASSESSOR.assess(root, ["Empty"])
            rules = {finding["rule"] for finding in report["diagnostics"]}
            self.assertTrue({"ECO_ENTRY", "VA_AREAS", "PYTHON_SYNTAX"}.issubset(rules))

    def testAlternativeDocumentationLocationDoesNotFailStructure(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for area in ["entities", "tools", "usecases", "value_objects"]:
                (root / "apps/Small" / area).mkdir(parents=True)
            (root / "start.py").write_text("# Technical entry existence, not runtime evidence\n")
            (root / "apps/Small/entities/Entity_Item.py").write_text("class Entity_Item:\n    pass\n")
            report = ASSESSOR.assess(root, ["Small"], entry="start.py")
            self.assertEqual(report["status"], "passed", report["diagnostics"])
            self.assertFalse((root / "docs").exists())

    def testSyntaxAndRelativeImportViolationsAreDiagnosed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for area in ["entities", "tools", "usecases", "value_objects"]:
                (root / "apps/Small" / area).mkdir(parents=True)
            (root / "launch.py").write_text("pass\n")
            (root / "apps/Small/tools/Tool_Bad.py").write_text("from ..usecases import UseCase_Foo\nclass Tool_Bad:\n    pass\n")
            (root / "apps/Small/entities/Entity_Invalid.py").write_text("class !!!\n")
            report = ASSESSOR.assess(root, ["Small"])
            rules = {finding["rule"] for finding in report["diagnostics"]}
            self.assertTrue({"VA_DEPENDENCY_DIRECTION", "PYTHON_SYNTAX"}.issubset(rules), rules)

    def testCliReturnsNonzeroAndMachineReadableDiagnostics(self):
        result = subprocess.run([sys.executable, str(EDITION / "scripts/evaluate_structure.py"),
            "--ecosystem", str(EDITION / "tests/fixtures/structural-counterexamples/invalid-ecosystem"),
            "--profile-app", "BrokenApp", "--json"], capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 1)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "failed")
        self.assertTrue(all("path" in entry and "rule" in entry for entry in report["diagnostics"]))

    def testAppSymlinkOutsideRootCannotPassWithoutAssessment(self):
        with tempfile.TemporaryDirectory() as temporary, tempfile.TemporaryDirectory() as outside:
            root = Path(temporary)
            (root / "apps").mkdir()
            (root / "launch.py").write_text("pass\n")
            try:
                (root / "apps/Escaped").symlink_to(Path(outside), target_is_directory=True)
            except (OSError, NotImplementedError) as error:
                self.skipTest(f"Directory symlink creation unavailable: {error}")
            report = ASSESSOR.assess(root, ["Escaped"])
            self.assertEqual(report["status"], "failed")
            self.assertEqual(report["scope"]["python_files_parsed"], 0)
            self.assertTrue(any(item["rule"] == "ECO_CLASSIFICATION" and "outside" in item["message"]
                                for item in report["diagnostics"]))


if __name__ == "__main__":
    unittest.main()
