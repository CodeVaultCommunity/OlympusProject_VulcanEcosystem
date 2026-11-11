"""Audit canonical Atlas → Minerva → Vulcan traceability for maintained examples."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


EDITION = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[4]
ATLAS = WORKSPACE / "L1-AtlasSpecifications" / "versioning" / "Stable-v1.1.0" / "examples"
MINERVA = WORKSPACE / "L2-MinervaBlueprints" / "versioning" / "Stable-v1.0.0" / "examples"

sys.path.insert(0, str(EDITION))
from vulcan_ecosystem.validation import validate_project  # noqa: E402


def digest_tree(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(value for value in root.rglob("*") if value.is_file()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        data = path.read_bytes()
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def main() -> int:
    results = {}
    for name in ("minimal", "composition", "task-board"):
        errors = []
        atlas_envelope = json.loads((ATLAS / name / "example.atlas.json").read_text(encoding="utf-8"))
        atlas_source = atlas_envelope["atlas"]
        normalized = json.loads((MINERVA / name / "provenance" / "atlas.normalized.json").read_text(encoding="utf-8"))
        if normalized.get("format") != "atlas-normalized/1.1.0":
            errors.append("Minerva does not pin atlas-normalized/1.1.0")
        if normalized.get("atlas") != atlas_source:
            errors.append("Minerva lossless Atlas payload differs from the canonical Atlas example")
        canonical_minerva = MINERVA / name
        embedded_minerva = EDITION / "examples" / name / "docs" / "L2_MinervaBlueprints"
        if digest_tree(canonical_minerva) != digest_tree(embedded_minerva):
            errors.append("embedded Minerva tree differs from canonical Minerva Stable-v1.0.0")
        vulcan = validate_project(EDITION / "examples" / name)
        errors.extend(vulcan["errors"])
        results[name] = {
            "status": "passed" if not errors else "failed",
            "atlas_document_id": atlas_source.get("document_id"),
            "atlas_revision": str(atlas_source.get("revision")),
            "atlas_semantic_sha256": normalized.get("source", {}).get("semantic_sha256"),
            "minerva_tree_sha256": digest_tree(canonical_minerva),
            "vulcan": vulcan["counts"],
            "errors": errors,
        }
    report = {
        "format": "olympus-ecosystem-validation/1.0.0",
        "atlas_version": "Stable-v1.1.0",
        "minerva_version": "Stable-v1.0.0",
        "vulcan_version": "Stable-v1.0.0",
        "status": "passed" if all(value["status"] == "passed" for value in results.values()) else "failed",
        "examples": results,
    }
    output = EDITION / "verification" / "ecosystem-validation.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

