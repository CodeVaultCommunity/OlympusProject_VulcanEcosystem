"""Generate, validate, and execute every maintained Stable-v1.0.0 example."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from vulcan_ecosystem.generator import realize_project
from vulcan_ecosystem.validation import validate_project


ROOT = Path(__file__).resolve().parent
EXAMPLES = {
    "minimal": "apps.RequestRegister.tests.Test_Contracts",
    "composition": "apps.BookingDesk.tests.Test_Contracts",
    "task-board": "apps.TaskBoard.tests.Test_Contracts",
}


def main() -> int:
    results = {}
    with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
        environment = dict(os.environ, TEMP=temporary, TMP=temporary)
        for name, suite in EXAMPLES.items():
            root = ROOT / "examples" / name
            realize_project(root)
            validation = validate_project(root)
            execution = subprocess.run(
                [sys.executable, "-m", "unittest", suite],
                cwd=root,
                env=environment,
                capture_output=True,
                text=True,
                timeout=90,
            )
            results[name] = {
                "validation": validation,
                "runtime_status": "passed" if execution.returncode == 0 else "failed",
                "runtime_output": execution.stderr.strip(),
            }
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0 if all(
        value["validation"]["status"] == "passed" and value["runtime_status"] == "passed"
        for value in results.values()
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())

