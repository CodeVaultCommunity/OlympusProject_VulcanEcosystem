"""Edition-local checks and launch commands. Integration validation requires an explicit Minerva edition."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import uuid

EDITION = Path(__file__).resolve().parent
EXAMPLES = {"minimal": "RequestRegister", "composition": "BookingDesk", "task-board": "TaskBoard"}


def writeReport(path, report):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def evaluate(name, reports):
    spec = importlib.util.spec_from_file_location("vulcan_structure", EDITION / "scripts/evaluate_structure.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    report = module.assess(EDITION / "examples" / name, [EXAMPLES[name]])
    writeReport(reports / name / "structure.json", report)
    print(f"{name} structure: {report['status']}", flush=True)
    return report["status"] != "failed"


def runTests(root, tests, report, expectations=None):
    command = [sys.executable, str(EDITION / "scripts/record_tests.py"), "--root", str(root),
               "--tests", str(tests), "--report", str(report)]
    if expectations:
        command += ["--expectations", str(expectations)]
    return subprocess.call(command, cwd=root) == 0


def validateMinerva(name, reports, selected):
    target = reports / name / "minerva.json"
    if selected is None:
        writeReport(target, {"status": "inconclusive", "reason": "Select the external Minerva Alpha-v0.1.0 with --minerva-edition; no validator is vendored."})
        return False
    selected = selected.resolve()
    validator = selected / "validator/minerva_validate.py"
    if not validator.is_file() or selected.name != "Alpha-v0.1.0":
        writeReport(target, {"status": "inconclusive", "reason": "Selected edition/validator is missing or does not match Alpha-v0.1.0."})
        return False
    sources = {p.relative_to(selected).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
               for p in sorted((selected / "minerva_blueprints").rglob("*")) if p.is_file() and p.suffix in {".py", ".json"}}
    sources[validator.relative_to(selected).as_posix()] = hashlib.sha256(validator.read_bytes()).hexdigest()
    version = subprocess.run([sys.executable, str(validator), "--version"], capture_output=True, text=True, timeout=30)
    if version.returncode or "Minerva Blueprints Alpha-v0.1.0 | YAML 0.1.0" not in version.stdout:
        writeReport(target, {"status": "inconclusive", "reason": "Selected tool does not declare the required model and profile.", "stdout": version.stdout, "stderr": version.stderr})
        return False
    root = EDITION / "examples" / name
    process = subprocess.run([sys.executable, str(validator), str(root / "docs/L2_MinervaBlueprints/blueprint.yaml"),
                              "--root", str(root), "--verify-code", "--json"], capture_output=True, text=True, encoding="utf-8", timeout=60)
    try:
        result = json.loads(process.stdout)
    except ValueError:
        result = {"status": "operational_error", "stdout": process.stdout, "stderr": process.stderr}
    report = {"status": "passed" if process.returncode == 0 else "inconclusive" if process.returncode == 3 else "failed",
              "external_tool": str(selected), "tool_version": version.stdout.strip(), "tool_sources": sources,
              "exit_code": process.returncode, "result": result,
              "limit": "Structural and consistency validation plus declared source observations; not behavioral proof or translation."}
    writeReport(target, report)
    print(f"{name} Minerva: {report['status']}", flush=True)
    return report["status"] == "passed"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["verify", "test", "evaluate", "list", "start"])
    parser.add_argument("--example", choices=[*EXAMPLES, "all"], default="all")
    parser.add_argument("--report-dir", type=Path)
    parser.add_argument("--minerva-edition", type=Path)
    args, remaining = parser.parse_known_args(argv)
    selected = list(EXAMPLES) if args.example == "all" else [args.example]
    if args.command in {"list", "start"}:
        if args.command == "start" and len(selected) != 1:
            parser.error("start selects one independent ecosystem using --example")
        return max(subprocess.call([sys.executable, str(EDITION / "examples" / name / "launch.py"), args.command, *remaining]) for name in selected)
    if remaining:
        parser.error("unrecognized arguments: " + " ".join(remaining))
    reports = (args.report_dir or EDITION / "verification/runs" / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-") + uuid.uuid4().hex[:8])).resolve()
    if reports.exists() and any(reports.iterdir()):
        parser.error("report directory must be absent or empty")
    outcomes = {}
    for name in selected:
        root = EDITION / "examples" / name
        if args.command in {"evaluate", "verify"}:
            outcomes[name + ":structure"] = evaluate(name, reports)
        if args.command in {"test", "verify"}:
            outcomes[name + ":tests"] = runTests(root, root / f"apps/{EXAMPLES[name]}/tests", reports / name / "execution.json", root / "docs/L3_Vulcan/test-bindings.json")
        if args.command == "verify":
            outcomes[name + ":minerva"] = validateMinerva(name, reports, args.minerva_edition)
    if args.command in {"test", "verify"}:
        outcomes["tooling:tests"] = runTests(EDITION, EDITION / "tests", reports / "tooling.json")
        legacy = EDITION / "tests/fixtures/legacy-ecosystem"
        outcomes["legacy-fixture:tests"] = runTests(legacy, legacy / "apps/TaskBoard/tests", reports / "legacy-fixture.json")
    summary = {"edition": "Alpha-v0.1.0", "command": args.command, "examples": selected,
               "executed_at_utc": datetime.now(timezone.utc).isoformat(), "status": "passed" if all(outcomes.values()) else "incomplete_or_failed", "checks": outcomes}
    writeReport(reports / "summary.json", summary)
    print(f"Report: {reports}; {summary['status']}")
    return 0 if all(outcomes.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
