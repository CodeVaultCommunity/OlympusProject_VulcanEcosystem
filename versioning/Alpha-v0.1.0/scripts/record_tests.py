"""Isolated unittest execution with per-scenario observations; never rewrites a model."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys
import time
import unittest


class RecordingResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = []

    def record(self, test, status, **extra):
        self.records.append({"test": test.id(), "status": status, **extra})

    def addSuccess(self, test):
        super().addSuccess(test)
        self.record(test, "passed", observations=getattr(test, "observations", {}))

    def addFailure(self, test, error):
        super().addFailure(test, error)
        self.record(test, "failed", detail=self._exc_info_to_string(error, test))

    def addError(self, test, error):
        super().addError(test, error)
        self.record(test, "error", detail=self._exc_info_to_string(error, test))

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.record(test, "skipped", reason=reason)

    def addSubTest(self, test, subtest, error):
        super().addSubTest(test, subtest, error)
        self.record(subtest, "passed" if error is None else "failed", parameters=json.loads(json.dumps(dict(subtest.params), default=repr)),
                    detail=None if error is None else self._exc_info_to_string(error, test),
                    observations=getattr(test, "observations", {}))


def coverage(records, expected):
    """Only executed subtests can satisfy an expected scenario or supporting check."""
    observed = {}
    for record in records:
        params = record.get("parameters", {})
        identifiers = list(params.get("scenario_ids", []))
        identifiers += [params[key] for key in ("scenario_id", "check_id") if key in params]
        for identifier in identifiers:
            observed.setdefault(identifier, []).append(record["status"])
    return {identifier: "not_run" if identifier not in observed else
            "passed" if all(status == "passed" for status in observed[identifier]) else "failed"
            for identifier in expected}


def sourceHashes(root):
    paths = [p for p in root.rglob("*") if p.is_file() and p.suffix in {".py", ".yaml", ".json"}
             and not {"work", "__pycache__", "verification"}.intersection(p.relative_to(root).parts)]
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--tests", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--expectations", type=Path)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    sys.path.insert(0, str(root))
    expected = json.loads(args.expectations.read_text(encoding="utf-8")) if args.expectations else {}
    binding = root / "docs/L2_MinervaBlueprints/blueprint.yaml"
    declared_hash = expected.get("model_baseline", {}).get("binding_sha256")
    baseline_matches = not declared_hash or binding.is_file() and hashlib.sha256(binding.read_bytes()).hexdigest() == declared_hash
    hashes = sourceHashes(root)
    start = time.monotonic()
    suite = unittest.TestLoader().discover(str(args.tests.resolve()), pattern="Test_*.py")
    result = unittest.TextTestRunner(verbosity=2, resultclass=RecordingResult).run(suite)
    covered = coverage(result.records, expected.get("scenario_ids", []) + expected.get("supporting_check_ids", []))
    changed = hashes != sourceHashes(root)
    passed = result.wasSuccessful() and result.testsRun > 0 and not changed and baseline_matches and all(v == "passed" for v in covered.values())
    report = {
        "edition": "Alpha-v0.1.0", "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(), "platform": platform.platform(),
        "command": [sys.executable, *sys.argv],
        "status": "passed" if passed else "failed", "tests_run": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
        "duration_seconds": round(time.monotonic() - start, 3), "records": result.records,
        "coverage": covered, "sources": hashes, "sources_changed_during_run": changed,
        "binding_baseline_matches": baseline_matches,
        "model_baseline": expected.get("model_baseline"),
        "limits": ["Observations on the recorded host and selected Python/SQLite realization only.",
                   "Fault doubles verify handling of uncertainty, not physical disk-failure tolerance.",
                   "Skipped checks remain unverified. Passing scenarios do not imply stakeholder approval.",
                   "No production identity provider, distributed deployment, browser interaction or production SLA assessed."],
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
