"""Strict reader for the controlled Minerva Markdown interchange format."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any

import yaml


_FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


@dataclass(frozen=True)
class MinervaModule:
    path: Path
    relative_path: str
    metadata: dict[str, Any]
    atlas: dict[str, Any]
    design: dict[str, Any]

    @property
    def module_id(self) -> str:
        return str(self.metadata["id"])

    @property
    def kind(self) -> str:
        return str(self.metadata["kind"])

    @property
    def generation(self) -> dict[str, Any]:
        value = self.metadata.get("generation", {})
        return value if isinstance(value, dict) else {}


@dataclass(frozen=True)
class MinervaProject:
    root: Path
    manifest: dict[str, Any]
    modules: tuple[MinervaModule, ...]


def _controlled_json(text: str, label: str) -> dict[str, Any]:
    matches = re.findall(rf"```{re.escape(label)}\r?\n(.*?)\r?\n```", text, re.DOTALL)
    if len(matches) != 1:
        raise ValueError(f"expected exactly one {label} block, found {len(matches)}")
    value = json.loads(matches[0])
    if not isinstance(value, dict):
        raise ValueError(f"{label} block must contain one JSON object")
    return value


def safe_relative_path(value: str) -> str:
    candidate = PurePosixPath(value)
    if candidate.is_absolute() or ".." in candidate.parts or not candidate.parts:
        raise ValueError(f"unsafe relative path: {value!r}")
    return candidate.as_posix()


def load_module(project_root: Path, relative_path: str) -> MinervaModule:
    relative_path = safe_relative_path(relative_path)
    path = project_root / Path(relative_path)
    text = path.read_text(encoding="utf-8")
    match = _FRONTMATTER.search(text)
    if not match:
        raise ValueError(f"missing YAML frontmatter: {relative_path}")
    metadata = yaml.safe_load(match.group(1))
    if not isinstance(metadata, dict):
        raise ValueError(f"invalid YAML frontmatter: {relative_path}")
    if metadata.get("format") != "minerva-markdown/1.0.0":
        raise ValueError(f"unsupported Minerva module format: {relative_path}")
    if metadata.get("model_version") != "Stable-v1.0.0":
        raise ValueError(f"unsupported Minerva model version: {relative_path}")
    return MinervaModule(
        path=path,
        relative_path=relative_path,
        metadata=metadata,
        atlas=_controlled_json(text, "atlas-source-json"),
        design=_controlled_json(text, "minerva-design-json"),
    )


def load_project(project_root: Path | str) -> MinervaProject:
    root = Path(project_root).resolve()
    manifest_path = root / "minerva.project.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("format") != "minerva-project/1.0.0":
        raise ValueError(f"unsupported Minerva project manifest: {manifest_path}")
    if manifest.get("model_version") != "Stable-v1.0.0":
        raise ValueError("Vulcan Stable-v1.0.0 requires Minerva Stable-v1.0.0")
    if manifest.get("semantic_authority") != "distributed_markdown_modules":
        raise ValueError("the Minerva manifest must be discovery-only")
    paths = manifest.get("modules")
    if not isinstance(paths, list) or not paths:
        raise ValueError("the Minerva project must list distributed Markdown modules")
    modules = tuple(load_module(root, str(path)) for path in paths)
    ids = [module.module_id for module in modules]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate Minerva module id")
    return MinervaProject(root=root, manifest=manifest, modules=modules)

