"""Bounded Python structural assessment for Vulcan Architecture Alpha-v0.1.0.

This does not validate Minerva YAML, prove domain behavior, authorize users, or
execute applications. Static import edges cannot discover dynamic imports.
"""

import argparse
import ast
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys


ROLE_PREFIXES = {"usecases": "UseCase_", "tools": "Tool_", "entities": "Entity_", "value_objects": "ValueObject_"}
METHOD = re.compile(r"^[a-z][A-Za-z0-9]*$")
ATTRIBUTE = re.compile(r"^_*[a-z][a-z0-9]*(?:_[a-z0-9]+)*_*$")
STRUCTURE = re.compile(r"^(?:(?:UseCase|Tool|Entity|ValueObject|Boundary|Test)_)?[A-Z][A-Za-z0-9]*$")
HOOKS = {"__init__", "__post_init__", "__eq__", "__hash__", "__repr__", "__str__", "__enter__", "__exit__"}
HTTP_HOOKS = {"do_GET", "do_POST", "do_PUT", "do_DELETE", "do_PATCH", "do_OPTIONS", "do_HEAD", "log_message"}
INFRASTRUCTURE = {"sqlite3", "socket", "subprocess", "http", "urllib", "requests"}
RULES = ["ECO_APPS", "ECO_ENTRY", "ECO_CLASSIFICATION", "VA_AREAS", "VA_SINGLE_STRUCTURE", "VA_FILE_NAME",
         "VA_ROLE_NAME", "VA_METHOD_CASE", "VA_ATTRIBUTE_CASE", "VA_DOMAIN", "VA_DEPENDENCY_DIRECTION",
         "VA_VALUE_OBJECT_CONSUMER", "VA_PURE_DATA", "VA_STATIC_CYCLE", "PYTHON_SYNTAX"]


def assess(ecosystem, profile_apps, legacy_apps=(), entry="launch.py", technical_files=()):
    root = Path(ecosystem).resolve()
    findings, sources, graph, exceptions = [], {}, {}, []
    profile_apps, legacy_apps = list(profile_apps), list(legacy_apps)

    def add(rule, path, message, line=None, severity="error"):
        findings.append({"rule": rule, "path": str(path), "line": line, "severity": severity, "message": message})

    if not (root / "apps").is_dir():
        add("ECO_APPS", "apps", "The ecosystem must contain apps/.")
    entry_path = (root / entry).resolve()
    if not entry_path.is_relative_to(root) or not entry_path.is_file():
        add("ECO_ENTRY", entry, "A local root entry mechanism must exist; this check does not execute it.")
    overlap = set(profile_apps) & set(legacy_apps)
    if overlap:
        add("ECO_CLASSIFICATION", "apps", "Apps cannot be both evaluated and excluded as legacy: " + ", ".join(sorted(overlap)))
    classified = set(profile_apps) | set(legacy_apps)
    if (root / "apps").is_dir():
        for app_dir in sorted((root / "apps").iterdir()):
            if app_dir.is_dir() and not app_dir.name.startswith("_") and app_dir.name not in classified:
                add("ECO_CLASSIFICATION", app_dir.relative_to(root), "App has no selected assessment profile.", severity="warning")
    for app_id in sorted(classified):
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", app_id):
            add("ECO_CLASSIFICATION", "apps", "Invalid app identifier: " + app_id)
        elif not (root / "apps" / app_id).is_dir():
            add("ECO_CLASSIFICATION", "apps/" + app_id, "Declared app directory does not exist.")

    technical = {Path(value).as_posix() for value in technical_files}
    for app_id in profile_apps:
        app_root = root / "apps" / app_id
        if not app_root.is_dir():
            continue
        if not app_root.resolve().is_relative_to(root):
            add("ECO_CLASSIFICATION", f"apps/{app_id}", "Declared app resolves outside the ecosystem; its sources were not assessed.")
            continue
        for area in ROLE_PREFIXES:
            if not (app_root / area).is_dir():
                add("VA_AREAS", f"apps/{app_id}/{area}", "Required core area is missing; it may be empty.")
        files = sorted(app_root.rglob("*.py"))
        if not files:
            add("PYTHON_SYNTAX", f"apps/{app_id}", "No Python sources found for the selected Python profile.")
        for path in files:
            relative = path.relative_to(root).as_posix()
            if not path.resolve().is_relative_to(root):
                add("PYTHON_SYNTAX", relative, "Source resolves outside the assessed ecosystem.")
                continue
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=relative)
            except (SyntaxError, UnicodeError, OSError) as error:
                add("PYTHON_SYNTAX", relative, str(error), getattr(error, "lineno", None))
                continue
            area = path.relative_to(app_root).parts[0]
            sources[relative] = {"tree": tree, "area": area, "app": app_id}
            graph[relative] = set()
            classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            functions = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
            if relative in technical:
                exceptions.append({"path": relative, "reason": "Explicit technical entry point; no application class is required. Semantic allocation requires review."})
                if classes:
                    add("VA_SINGLE_STRUCTURE", relative, "Technical entry exemption cannot conceal a separate class.")
                continue
            if len(classes) != 1:
                add("VA_SINGLE_STRUCTURE", relative, f"Expected one structure; found {len(classes)}.")
            if functions:
                add("VA_SINGLE_STRUCTURE", relative, "Standalone functions outside the main structure require an explicit language adaptation.", functions[0].lineno)
            if len(classes) != 1:
                continue
            structure = classes[0]
            if path.stem != structure.name:
                add("VA_FILE_NAME", relative, f"Filename stem must equal {structure.name}.", structure.lineno)
            if not STRUCTURE.fullmatch(structure.name):
                add("VA_ROLE_NAME", relative, "Structure must use role prefix and PascalCase, or PascalCase for support.", structure.lineno)
            if area in ROLE_PREFIXES and not structure.name.startswith(ROLE_PREFIXES[area]):
                add("VA_ROLE_NAME", relative, f"Area {area} requires {ROLE_PREFIXES[area]} prefix.", structure.lineno)
            if area == "usecases" and len(path.relative_to(app_root).parts) < 3:
                add("VA_DOMAIN", relative, "Place the use case in usecases/<Domain>/.")
            is_http = any(isinstance(base, ast.Name) and base.id == "BaseHTTPRequestHandler" for base in structure.bases)
            for node in structure.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if node.name in HOOKS or (is_http and node.name in HTTP_HOOKS):
                        exceptions.append({"path": relative, "symbol": node.name, "reason": "Python or HTTP framework spelling."})
                    elif not METHOD.fullmatch(node.name):
                        add("VA_METHOD_CASE", relative, f"Method {node.name} must use camelCase.", node.lineno)
                targets = []
                if isinstance(node, ast.AnnAssign):
                    targets = [node.target]
                elif isinstance(node, ast.Assign):
                    targets = node.targets
                for target in targets:
                    if isinstance(target, ast.Name) and not ATTRIBUTE.fullmatch(target.id):
                        add("VA_ATTRIBUTE_CASE", relative, f"Attribute {target.id} must use snake_case.", node.lineno)
            for node in ast.walk(structure):
                if isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Store) and isinstance(node.value, ast.Name) and node.value.id in {"self", "cls"}:
                    if not ATTRIBUTE.fullmatch(node.attr):
                        add("VA_ATTRIBUTE_CASE", relative, f"Attribute {node.attr} must use snake_case.", node.lineno)

    module_to_file = {Path(path).with_suffix("").as_posix().replace("/", "."): path for path in sources}
    for relative, information in sources.items():
        area, app_id = information["area"], information["app"]
        for node in ast.walk(information["tree"]):
            modules = []
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                prefix = node.module or ""
                if node.level:
                    package = relative[:-3].split("/")[:-1]
                    prefix = ".".join(package[:len(package) - node.level + 1] + ([prefix] if prefix else []))
                modules = [prefix] + [prefix + "." + alias.name for alias in node.names]
            for module in modules:
                parts = module.split(".")
                target = module_to_file.get(module)
                if target and target != relative:
                    graph[relative].add(target)
                if module.startswith(f"apps.{app_id}.") and len(parts) > 2:
                    target_area = parts[2]
                    if area == "tools" and target_area == "usecases":
                        add("VA_DEPENDENCY_DIRECTION", relative, "A tool must not import a use case.", node.lineno)
                    if area in {"entities", "value_objects"} and target_area in {"tools", "usecases", "boundaries", "composition"}:
                        add("VA_DEPENDENCY_DIRECTION", relative, "Entity/value object depends on an outer realization role.", node.lineno)
                    if area == "usecases" and target_area in {"boundaries", "composition"}:
                        add("VA_DEPENDENCY_DIRECTION", relative, "Core use case must be independent of its channel/composition.", node.lineno)
                    if target_area == "value_objects" and area not in {"entities", "value_objects", "tests"}:
                        add("VA_VALUE_OBJECT_CONSUMER", relative, "Only entities consume value objects in production.", node.lineno)
                if area in {"entities", "value_objects"} and parts[0] in INFRASTRUCTURE:
                    add("VA_PURE_DATA", relative, f"Data structure imports an infrastructure module: {parts[0]}.", node.lineno)
                if len(parts) >= 3 and parts[0] == "apps" and parts[1] != app_id:
                    add("VA_DEPENDENCY_DIRECTION", relative, "Cross-app Python import needs review as an explicitly public API: " + module, node.lineno, "warning")

    visited, active, stack = set(), set(), []

    def visit(source):
        if source in active:
            cycle = stack[stack.index(source):] + [source]
            add("VA_STATIC_CYCLE", source, "Static component dependency cycle: " + " -> ".join(cycle))
            return
        if source in visited:
            return
        active.add(source)
        stack.append(source)
        for target in sorted(graph[source]):
            visit(target)
        stack.pop()
        active.remove(source)
        visited.add(source)

    for source in sorted(graph):
        visit(source)
    findings = [json.loads(item) for item in dict.fromkeys(json.dumps(item, sort_keys=True) for item in findings)]
    return {
        "model": "Vulcan Ecosystem", "edition": "Alpha-v0.1.0", "profile": "Vulcan Architecture Python",
        "evaluated_at_utc": datetime.now(timezone.utc).isoformat(), "ecosystem": str(root),
        "status": "failed" if any(item["severity"] == "error" for item in findings) else "passed_with_warnings" if findings else "passed",
        "scope": {"profile_apps": profile_apps, "legacy_apps_not_structurally_assessed": legacy_apps,
                  "python_files_parsed": len(sources), "rules": RULES, "entry": entry,
                  "not_assessed": ["Minerva schema or per-file mirror", "semantic preservation", "authorization behavior",
                                   "runtime execution", "dynamic imports", "C/Go", "all foreign library dependencies", "cross-app API public status"]},
        "diagnostics": findings, "adaptations": exceptions,
        "static_dependencies": {source: sorted(targets) for source, targets in sorted(graph.items())},
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ecosystem", type=Path, required=True)
    parser.add_argument("--profile-app", action="append", required=True)
    parser.add_argument("--legacy-app", action="append", default=[])
    parser.add_argument("--entry", default="launch.py")
    parser.add_argument("--technical-file", action="append", default=[])
    parser.add_argument("--json", nargs="?", const="-", metavar="REPORT")
    args = parser.parse_args(argv)
    report = assess(args.ecosystem, args.profile_app, args.legacy_app, args.entry, args.technical_file)
    encoded = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.json == "-":
        print(encoded, end="")
    else:
        if args.json:
            target = Path(args.json)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(encoded, encoding="utf-8")
        print(f"{report['status']}: {report['scope']['python_files_parsed']} Python files; {len(report['diagnostics'])} diagnostics")
        for diagnostic in report["diagnostics"]:
            print(f"{diagnostic['severity']} {diagnostic['rule']} {diagnostic['path']}: {diagnostic['message']}")
    return 1 if report["status"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
