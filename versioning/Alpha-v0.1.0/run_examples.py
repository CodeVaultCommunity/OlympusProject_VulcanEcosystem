#!/usr/bin/env python3
"""Edition-local entry point: paths are resolved from this file, never the cwd."""

import argparse
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
import unittest


EDITION = Path(__file__).resolve().parent
ECOSYSTEM = EDITION / "examples/task-board-ecosystem"


class RecordingResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.records.append({"test": test.id(), "status": "passed"})

    def addFailure(self, test, error):
        super().addFailure(test, error)
        self.records.append({"test": test.id(), "status": "failed"})

    def addError(self, test, error):
        super().addError(test, error)
        self.records.append({"test": test.id(), "status": "error"})

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.records.append({"test": test.id(), "status": "skipped", "reason": reason})

    def addSubTest(self, test, subtest, error):
        super().addSubTest(test, subtest, error)
        if error is not None:
            self.records.append({"test": subtest.id(), "status": "failed_subtest"})


def writeReport(path, report):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def evaluate(report_dir):
    specification = importlib.util.spec_from_file_location("vulcan_structure", EDITION / "scripts/evaluate_structure.py")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    report = module.assess(ECOSYSTEM, ["TaskBoard"], ["LegacyReports"], technical_files=["apps/TaskBoard/main.py"])
    writeReport(report_dir / "structure.json", report)
    print(f"Structure: {report['status']}; {report['scope']['python_files_parsed']} Python files", flush=True)
    return report["status"] != "failed"


def test(report_dir):
    sys.path.insert(0, str(ECOSYSTEM))
    suite = unittest.TestSuite()
    for location in [ECOSYSTEM / "apps/TaskBoard/tests", EDITION / "tests"]:
        suite.addTests(unittest.TestLoader().discover(str(location), pattern="Test_*.py"))
    start = time.monotonic()
    timestamp = datetime.now(timezone.utc).isoformat()
    result = unittest.TextTestRunner(verbosity=2, resultclass=RecordingResult).run(suite)
    report = {
        "model": "Vulcan Ecosystem", "edition": "Alpha-v0.1.0", "executed_at_utc": timestamp,
        "command": [sys.executable, *sys.argv], "python": platform.python_version(), "platform": platform.platform(),
        "status": "passed" if result.wasSuccessful() else "failed", "tests_run": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
        "duration_seconds": round(time.monotonic() - start, 3), "tests": result.records,
        "limits": ["Python standard-library implementation only; recorded host only",
                   "HTTP requests and HTML response checks do not demonstrate browser interaction",
                   "Test counts are unittest methods, not counts of every subcase or assertion",
                   "C/Go, Docker, production identity, load, distributed failure and deployment were not tested",
                   "CI configuration alone is not a hosted CI run"],
    }
    writeReport(report_dir / "execution.json", report)
    return result.wasSuccessful()


def validateMinerva(report_dir):
    validator = EDITION / "vendor/minerva/validator/minerva_validate.py"
    blueprint = ECOSYSTEM / "docs/L2_MinervaBlueprints/blueprint.yaml"
    if not validator.is_file() or not blueprint.is_file():
        writeReport(report_dir / "minerva.json", {"status": "not_run", "reason": "Required edition-local Minerva resources are missing."})
        print("Minerva: required edition-local resources missing", file=sys.stderr)
        return False
    result = subprocess.run([sys.executable, str(validator), str(blueprint), "--root", str(ECOSYSTEM), "--verify-code", "--json"],
                            cwd=EDITION, capture_output=True, text=True)
    try:
        report = json.loads(result.stdout)
    except ValueError:
        report = {"status": "failed", "stdout": result.stdout, "stderr": result.stderr}
    writeReport(report_dir / "minerva.json", report)
    print(f"Minerva: exit {result.returncode}", flush=True)
    if result.returncode:
        print(result.stderr or result.stdout, file=sys.stderr)
    return result.returncode == 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["verify", "test", "evaluate", "list", "start"])
    parser.add_argument("--report-dir", type=Path, default=EDITION / "verification")
    args, remaining = parser.parse_known_args(argv)
    if args.command in {"list", "start"}:
        return subprocess.call([sys.executable, str(ECOSYSTEM / "launch.py"), args.command, *remaining], cwd=ECOSYSTEM)
    if remaining:
        parser.error("unrecognized arguments: " + " ".join(remaining))
    reports = args.report_dir.resolve()
    results = []
    if args.command in {"evaluate", "verify"}:
        results.append(evaluate(reports))
    if args.command in {"test", "verify"}:
        results.append(test(reports))
    if args.command == "verify":
        results.append(validateMinerva(reports))
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
