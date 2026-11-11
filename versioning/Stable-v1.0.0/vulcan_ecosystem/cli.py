"""Command-line interfaces for Vulcan generation and validation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .generator import realize_project
from .validation import validate_project


def generate_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Realize a Minerva project as a Vulcan codebase.")
    parser.add_argument("example_root", type=Path)
    parser.add_argument("--regenerate", action="store_true", help="Replace every target with deterministic generated code.")
    args = parser.parse_args(argv)
    result = realize_project(args.example_root, regenerate=args.regenerate)
    print(json.dumps(result["coverage"], indent=2))
    return 0


def validate_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a Vulcan project against embedded Minerva.")
    parser.add_argument("example_root", type=Path)
    args = parser.parse_args(argv)
    result = validate_project(args.example_root)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "passed" else 1

