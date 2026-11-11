# Vulcan Ecosystem · Stable-v1.0.0

Vulcan is the executable L3 realization of a Minerva Stable-v1.0.0 project.
The maintained examples embed their complete distributed Minerva Markdown tree
under `docs/L2_MinervaBlueprints/`; no separate summary blueprint replaces
those modules.

## Ecosystem contract

- Every Minerva module with generation mode `code` or `test` maps to exactly
  one Python file and top-level symbol.
- The generated `realization.json` preserves module identity, Markdown path,
  Atlas source references, target file/symbol, code hash, and realization mode.
- A preserved reference implementation may contain additional support code,
  but it must expose every method declared by `minerva-design-json`.
- Abstract tools become protocols. Concrete-tool designs become code adapters
  over the verified SQLite implementations and expose the designed operations.
- `Boundary` remains reserved for interaction adapters that expose use cases.
  Behavioral scenarios use `observation_points`.
- The Vulcan knowledge graph extends the complete Minerva graph with a
  `realized_by` edge from each executable/testable module to its code symbol.

## Layout

```text
examples/<name>/
  docs/L2_MinervaBlueprints/       complete Minerva source
  docs/L3_Vulcan/realization.json  module-to-code ledger
  docs/L3_Vulcan/knowledge-graph.json
  apps/<App>/                      executable code and tests
  launch.py                        local CLI/HTTP demonstration
schemas/                           stable interchange schemas
vulcan_ecosystem/                  generator and validators
scripts/validate_ecosystem.py      Atlas → Minerva → Vulcan audit
```

## Commands

```powershell
vulcan-generate examples/minimal
vulcan-validate examples/minimal
python run_examples.py
python scripts/validate_ecosystem.py
```

Generation is deterministic for generator-owned files and leaves maintained
reference implementations intact. Validation checks paths, source hashes,
symbols, designed methods, tool lineage, Boundary terminology, graph coverage,
and code hashes.

## Maintained examples

- `examples/minimal`: Request Register, 7 Minerva-to-code mappings.
- `examples/composition`: Booking Desk, 12 mappings.
- `examples/task-board`: Task Board, 12 mappings.

The runtime contract suites cover authorization-before-effects, validation,
SQLite transaction behavior, conflicts, unknown write outcomes, persistence,
composition, and boundary translation.

Distributed under the [MIT license](LICENSE).

