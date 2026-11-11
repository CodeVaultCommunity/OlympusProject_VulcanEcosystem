"""Validation of a Vulcan project against its embedded Minerva source."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

from .generator import sha256_file
from .minerva import load_project, safe_relative_path


def _symbols(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {node.name for node in tree.body if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))}


def _class_methods(path: Path, symbol: str) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == symbol:
            return {
                child.name
                for child in node.body
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
            }
    return set()


def validate_project(example_root: Path | str) -> dict[str, Any]:
    root = Path(example_root).resolve()
    errors: list[str] = []
    project = load_project(root / "docs" / "L2_MinervaBlueprints")
    realization_path = root / "docs" / "L3_Vulcan" / "realization.json"
    graph_path = root / "docs" / "L3_Vulcan" / "knowledge-graph.json"
    if not realization_path.is_file():
        return {"status": "failed", "errors": ["missing docs/L3_Vulcan/realization.json"]}
    realization = json.loads(realization_path.read_text(encoding="utf-8"))
    if realization.get("format") != "vulcan-realization/1.0.0":
        errors.append("unsupported realization format")
    if realization.get("model_version") != "Stable-v1.0.0":
        errors.append("unsupported Vulcan model version")
    source = realization.get("source", {})
    expected_source = project.manifest["source"]
    if source.get("atlas_semantic_sha256") != expected_source.get("semantic_sha256"):
        errors.append("Atlas semantic hash differs between Minerva and Vulcan")
    if source.get("semantic_authority") != "distributed_markdown_modules":
        errors.append("Vulcan did not preserve Minerva's distributed semantic authority")

    expected_modules = {
        module.module_id: module
        for module in project.modules
        if module.generation.get("mode") in {"code", "test"}
    }
    mappings = realization.get("modules", [])
    mapped_ids = [str(mapping.get("minerva_module_id")) for mapping in mappings]
    if len(mapped_ids) != len(set(mapped_ids)):
        errors.append("duplicate Minerva module mapping")
    missing = sorted(set(expected_modules) - set(mapped_ids))
    extra = sorted(set(mapped_ids) - set(expected_modules))
    if missing:
        errors.append(f"unrealized Minerva modules: {missing}")
    if extra:
        errors.append(f"unknown realization mappings: {extra}")

    for mapping in mappings:
        module_id = str(mapping.get("minerva_module_id"))
        module = expected_modules.get(module_id)
        if module is None:
            continue
        target = mapping.get("target", {})
        try:
            relative_path = safe_relative_path(str(target.get("path", "")))
        except ValueError as error:
            errors.append(str(error))
            continue
        if target.get("path") != module.generation.get("path") or target.get("symbol") != module.generation.get("symbol"):
            errors.append(f"target drift for {module_id}")
        if mapping.get("minerva_path") != module.relative_path:
            errors.append(f"Minerva path drift for {module_id}")
        if mapping.get("source_refs") != [str(value) for value in module.metadata.get("source_refs", [])]:
            errors.append(f"source refs drift for {module_id}")
        path = root / Path(relative_path)
        if not path.is_file():
            errors.append(f"missing target file for {module_id}: {relative_path}")
            continue
        if sha256_file(path) != mapping.get("sha256"):
            errors.append(f"target hash drift for {module_id}")
        try:
            if str(target.get("symbol")) not in _symbols(path):
                errors.append(f"missing target symbol for {module_id}")
            expected_methods = {
                str(method.get("name"))
                for method in module.design.get("methods", [])
                if isinstance(method, dict) and method.get("name")
            }
            missing_methods = sorted(expected_methods - _class_methods(path, str(target.get("symbol"))))
            if missing_methods:
                errors.append(f"target methods drift for {module_id}: {missing_methods}")
        except SyntaxError as error:
            errors.append(f"invalid Python for {module_id}: {error}")
        if module.kind == "boundary" and module.design.get("boundary_semantics") != "Interaction interface only; never a test case or observation point.":
            errors.append(f"Boundary semantic violation in {module_id}")
        if module.kind == "behavioral_test":
            for scenario in module.design.get("scenarios", []):
                if "observation_points" not in scenario or "boundary" in scenario:
                    errors.append(f"test scenario uses Boundary terminology in {module_id}")

    concrete_modules = [module for module in project.modules if module.kind == "concrete_tool"]
    abstract_ids = {module.module_id for module in project.modules if module.kind == "abstract_tool"}
    for concrete in concrete_modules:
        implementations = set(str(value) for value in concrete.design.get("implements", []))
        if not implementations or not implementations <= abstract_ids:
            errors.append(f"invalid concrete-tool lineage in {concrete.module_id}")

    if not graph_path.is_file():
        errors.append("missing Vulcan knowledge graph")
        graph: dict[str, Any] = {}
    else:
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        if graph.get("format") != "vulcan-knowledge-graph/1.0.0":
            errors.append("unsupported Vulcan knowledge graph format")
        node_ids = {str(node.get("id")) for node in graph.get("nodes", [])}
        for module_id in expected_modules:
            if f"MOD:{module_id}" not in node_ids or f"CODE:{module_id}" not in node_ids:
                errors.append(f"knowledge graph misses module/code pair for {module_id}")
        edge_keys = {
            (str(edge.get("source")), str(edge.get("target")), str(edge.get("relation")))
            for edge in graph.get("edges", [])
        }
        for module_id in expected_modules:
            if (f"MOD:{module_id}", f"CODE:{module_id}", "realized_by") not in edge_keys:
                errors.append(f"knowledge graph misses realization edge for {module_id}")

    return {
        "status": "passed" if not errors else "failed",
        "model_version": "Stable-v1.0.0",
        "project_id": project.manifest["project_id"],
        "counts": {
            "minerva_modules": len(project.modules),
            "code_modules": len(expected_modules),
            "realized_modules": len(mappings),
            "knowledge_nodes": len(graph.get("nodes", [])),
            "knowledge_edges": len(graph.get("edges", [])),
        },
        "errors": errors,
    }

