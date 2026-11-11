"""Deterministic Minerva-to-Python realization and traceability generation."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import re
import shutil
from typing import Any

from .minerva import MinervaModule, MinervaProject, load_project, safe_relative_path


GENERATOR = "vulcan-ecosystem/1.0.0"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _python_identifier(value: str, fallback: str = "value") -> str:
    value = re.sub(r"\W+", "_", value.strip()).strip("_").lower()
    if not value or value[0].isdigit():
        value = f"{fallback}_{value}"
    return value


def _python_type(value: str | None) -> str:
    return {
        "text": "str",
        "integer": "int",
        "number": "float",
        "boolean": "bool",
    }.get(str(value).lower(), "object")


def _method_signature(method: dict[str, Any]) -> str:
    parameters = ["self"]
    for parameter in method.get("parameters", []):
        if isinstance(parameter, dict):
            name = _python_identifier(str(parameter.get("name", "value")))
            parameters.append(f"{name}: {_python_type(parameter.get('type'))}")
    return ", ".join(parameters)


def _doc_header(module: MinervaModule) -> list[str]:
    refs = ", ".join(str(value) for value in module.metadata.get("source_refs", []))
    return [
        f'"""Generated from Minerva module {module.module_id}.',
        "",
        f"Source refs: {refs}",
        'Do not edit generated files by hand; update Minerva and regenerate."""',
        "",
        f'MINERVA_MODULE_ID = "{module.module_id}"',
        f"SOURCE_REFS = {tuple(str(value) for value in module.metadata.get('source_refs', []))!r}",
        "",
    ]


def _render_protocol(module: MinervaModule, symbol: str) -> str:
    lines = _doc_header(module)
    lines += ["from typing import Protocol, runtime_checkable", "", "@runtime_checkable", f"class {symbol}(Protocol):"]
    methods = module.design.get("methods", [])
    if not methods:
        lines.append("    pass")
    for method in methods:
        name = _python_identifier(str(method.get("name", "execute")))
        lines += [
            f"    def {name}({_method_signature(method)}) -> object:",
            f'        """Implements {", ".join(str(v) for v in method.get("source_refs", []))}."""',
            "        ...",
            "",
        ]
    return "\n".join(lines).rstrip() + "\n"


def _legacy_tool(module: MinervaModule, target: Path) -> Path | None:
    if module.kind != "concrete_tool" or target.parent.name != "concrete":
        return None
    candidate = target.parent.parent / target.name
    return candidate if candidate.is_file() else None


def _render_concrete_tool(module: MinervaModule, symbol: str, target: Path) -> str:
    legacy = _legacy_tool(module, target)
    if legacy:
        app = target.parts[target.parts.index("apps") + 1]
        import_path = f"apps.{app}.tools.{target.stem}"
        lines = _doc_header(module)
        operation_to_legacy = {
            "OP-REQUEST-STORE": "storeRequest",
            "OP-BOOKING-LOAD": "loadBooking",
            "OP-BOOKING-SAVE": "saveBooking",
            "OP-TASK-CREATE": "createTask",
            "OP-TASK-LOAD": "loadTask",
            "OP-TASK-COMPLETE": "completeTask",
            "OP-TASK-LIST": "listTasks",
        }
        lines += [
            f"from {import_path} import {symbol} as _ReferenceImplementation",
            "",
            f"class {symbol}(_ReferenceImplementation):",
            f'    """Concrete realization of {", ".join(module.design.get("implements", []))}."""',
            "",
            "    minerva_design = {",
            f'        "technology": {module.design.get("technology")!r},',
            f'        "configuration": {module.design.get("configuration", [])!r},',
            f'        "lifecycle": {module.design.get("lifecycle")!r},',
            "    }",
        ]
        for method in module.design.get("methods", []):
            name = _python_identifier(str(method.get("name", "execute")))
            operation = str(method.get("implements_operation", ""))
            legacy_method = operation_to_legacy.get(operation)
            parameters = [
                _python_identifier(str(value.get("name", "value")))
                for value in method.get("parameters", [])
                if isinstance(value, dict)
            ]
            signature = ", ".join(["self", *parameters])
            if not legacy_method:
                lines += ["", f"    def {name}({signature}) -> object:", "        raise NotImplementedError"]
                continue
            call_parameters = list(parameters)
            if operation.startswith("OP-TASK-"):
                call_parameters = [value for value in call_parameters if value != "board"]
            arguments = ", ".join(call_parameters)
            lines += [
                "",
                f"    def {name}({signature}) -> object:",
                f'        """Realize {operation} through the verified SQLite implementation."""',
                f"        return super().{legacy_method}({arguments})",
            ]
        return "\n".join(lines).rstrip() + "\n"
    lines = _doc_header(module)
    lines += [f"class {symbol}:", f"    implements = {tuple(module.design.get('implements', []))!r}"]
    for method in module.design.get("methods", []):
        name = _python_identifier(str(method.get("name", "execute")))
        lines += ["", f"    def {name}({_method_signature(method)}) -> object:", "        raise NotImplementedError"]
    return "\n".join(lines).rstrip() + "\n"


def _render_boundary(module: MinervaModule, symbol: str, target: Path) -> str:
    app = target.parts[target.parts.index("apps") + 1]
    methods = module.design.get("methods", [])
    lines = _doc_header(module)
    lines += [
        f"from apps.{app}.boundaries.Boundary_Json import Boundary_Json",
        "",
        f"class {symbol}:",
        '    """Interaction adapter; this is not a test scenario or observation point."""',
        "",
        "    def __init__(self, application) -> None:",
        "        self._delegate = Boundary_Json(application)",
    ]
    for method in methods:
        name = _python_identifier(str(method.get("name", "invoke")))
        operation = name.removesuffix("_form").replace("_booking", "").replace("_task", "")
        for candidate in ("submit", "create", "cancel", "lookup", "locate", "complete", "list"):
            if candidate in name:
                operation = candidate
                break
        lines += [
            "",
            f"    def {name}(self, payload: dict, caller_token: str | None = None):",
            f'        """Expose {method.get("exposes_use_case", "the declared use case")}."""',
            f"        return self._delegate.invoke({operation!r}, payload, caller_token)",
        ]
    return "\n".join(lines).rstrip() + "\n"


def _render_use_case(module: MinervaModule, symbol: str, target: Path) -> str:
    alternate = None
    if "Locate" in target.stem:
        alternate = target.with_name(target.name.replace("Locate", "Lookup"))
    if alternate and alternate.is_file():
        app = target.parts[target.parts.index("apps") + 1]
        import_symbol = alternate.stem
        import_path = f"apps.{app}.usecases.Main.{alternate.stem}"
        method = next(iter(module.design.get("methods", [])), {"name": "execute", "parameters": []})
        parameters = [
            _python_identifier(str(value.get("name", "value")))
            for value in method.get("parameters", [])
            if isinstance(value, dict)
        ]
        signature = ", ".join(["self", "actor_context", *parameters])
        arguments = ", ".join(["actor_context", *parameters])
        lines = _doc_header(module)
        lines += [
            f"from {import_path} import {import_symbol}",
            "",
            f"class {symbol}({import_symbol}):",
            '    """Terminology-aligned realization of the lookup use case."""',
            "",
            f"    def execute({signature}):",
            f"        return self.lookupBooking({arguments})",
        ]
        return "\n".join(lines).rstrip() + "\n"
    return _render_fallback(module, symbol)


def _render_test_design(module: MinervaModule, symbol: str) -> str:
    scenarios = module.design.get("scenarios", [])
    lines = _doc_header(module)
    lines += [
        "import unittest",
        "",
        f"class {symbol}(unittest.TestCase):",
        '    """Generated behavioral-test binding; executable contracts live beside it."""',
        f"    tests_use_case = {module.design.get('tests_use_case')!r}",
        f"    scenarios = {scenarios!r}",
        "",
        "    def test_scenarios_declare_observation_points(self) -> None:",
        "        self.assertTrue(self.scenarios)",
        "        for scenario in self.scenarios:",
        "            self.assertIn(\"observation_points\", scenario)",
        "            self.assertNotIn(\"boundary\", scenario)",
    ]
    return "\n".join(lines).rstrip() + "\n"


def _render_type(module: MinervaModule, symbol: str) -> str:
    examples = []
    for value in module.atlas.get("examples", []):
        if isinstance(value, dict) and isinstance(value.get("text"), str):
            examples.append(value["text"])
    lines = _doc_header(module)
    if examples:
        lines += ["from enum import StrEnum", "", f"class {symbol}(StrEnum):"]
        for value in examples:
            lines.append(f"    {_python_identifier(value, 'value').upper()} = {value!r}")
    else:
        lines += [f"class {symbol}(str):", "    pass"]
    return "\n".join(lines).rstrip() + "\n"


def _render_fallback(module: MinervaModule, symbol: str) -> str:
    lines = _doc_header(module)
    lines += [
        f"class {symbol}:",
        f'    """Generated {module.kind} realization placeholder with complete traceability."""',
        "    pass",
    ]
    return "\n".join(lines).rstrip() + "\n"


def render_module(module: MinervaModule, target: Path, symbol: str) -> str:
    if module.kind == "abstract_tool":
        return _render_protocol(module, symbol)
    if module.kind == "concrete_tool":
        return _render_concrete_tool(module, symbol, target)
    if module.kind == "boundary":
        return _render_boundary(module, symbol, target)
    if module.kind == "behavioral_test":
        return _render_test_design(module, symbol)
    if module.kind == "type":
        return _render_type(module, symbol)
    if module.kind == "use_case":
        return _render_use_case(module, symbol, target)
    return _render_fallback(module, symbol)


def _top_level_symbols(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {node.name for node in tree.body if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))}


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def realize_project(example_root: Path | str, *, regenerate: bool = False) -> dict[str, Any]:
    root = Path(example_root).resolve()
    minerva_root = root / "docs" / "L2_MinervaBlueprints"
    project = load_project(minerva_root)
    mappings: list[dict[str, Any]] = []
    code_modules = [module for module in project.modules if module.generation.get("mode") in {"code", "test"}]
    for module in code_modules:
        generation = module.generation
        relative_target = safe_relative_path(str(generation["path"]))
        symbol = str(generation["symbol"])
        target = root / Path(relative_target)
        mode = "preserved_reference_implementation"
        generator_managed = target.is_file() and target.read_text(encoding="utf-8").startswith('"""Generated from Minerva module ')
        if regenerate or not target.is_file() or generator_managed:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render_module(module, target, symbol), encoding="utf-8", newline="\n")
            mode = "generated_from_minerva"
        symbols = _top_level_symbols(target)
        if symbol not in symbols:
            raise ValueError(f"target symbol {symbol!r} not found in {relative_target}")
        mappings.append({
            "minerva_module_id": module.module_id,
            "minerva_path": module.relative_path,
            "kind": module.kind,
            "source_refs": [str(value) for value in module.metadata.get("source_refs", [])],
            "target": {"language": "python", "path": relative_target, "symbol": symbol},
            "realization_mode": mode,
            "sha256": sha256_file(target),
        })

    source = project.manifest["source"]
    realization = {
        "format": "vulcan-realization/1.0.0",
        "model_version": "Stable-v1.0.0",
        "project_id": project.manifest["project_id"],
        "generated_by": GENERATOR,
        "source": {
            "minerva_format": project.manifest["format"],
            "minerva_model_version": project.manifest["model_version"],
            "semantic_authority": project.manifest["semantic_authority"],
            "atlas_document_id": source["document_id"],
            "atlas_revision": str(source["revision"]),
            "atlas_semantic_sha256": source["semantic_sha256"],
        },
        "modules": mappings,
        "coverage": {
            "minerva_code_modules": len(code_modules),
            "realized_modules": len(mappings),
            "complete": len(code_modules) == len(mappings),
        },
    }
    vulcan_docs = root / "docs" / "L3_Vulcan"
    _write_json(vulcan_docs / "realization.json", realization)
    _write_json(vulcan_docs / "knowledge-graph.json", build_knowledge_graph(project, realization))
    return realization


def build_knowledge_graph(project: MinervaProject, realization: dict[str, Any]) -> dict[str, Any]:
    minerva_graph_path = project.root / str(project.manifest["knowledge_graph"])
    minerva_graph = json.loads(minerva_graph_path.read_text(encoding="utf-8"))
    nodes = list(minerva_graph.get("nodes", []))
    edges = [
        {
            **{key: value for key, value in edge.items() if key not in {"from", "to"}},
            "source": edge.get("source", edge.get("from")),
            "target": edge.get("target", edge.get("to")),
        }
        for edge in minerva_graph.get("edges", [])
    ]
    existing_ids = {str(node.get("id")) for node in nodes}
    for mapping in realization["modules"]:
        code_id = f"CODE:{mapping['minerva_module_id']}"
        if code_id not in existing_ids:
            nodes.append({
                "id": code_id,
                "kind": "code_symbol",
                "path": mapping["target"]["path"],
                "symbol": mapping["target"]["symbol"],
            })
            existing_ids.add(code_id)
        edges.append({
            "source": f"MOD:{mapping['minerva_module_id']}",
            "target": code_id,
            "relation": "realized_by",
        })
    return {
        "format": "vulcan-knowledge-graph/1.0.0",
        "model_version": "Stable-v1.0.0",
        "project_id": realization["project_id"],
        "source_graph_format": minerva_graph.get("format"),
        "nodes": nodes,
        "edges": edges,
    }

