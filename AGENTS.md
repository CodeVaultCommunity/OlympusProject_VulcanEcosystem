# Agent guide for Vulcan Ecosystem

## Select the edition

Respect an explicitly requested edition. Otherwise select the highest numeric
Stable edition under `versioning/`. Stable-v1.0.0 is the current edition;
Alpha-v0.1.0 is historical.

## Consume Minerva, do not reinterpret it

Stable-v1.0.0 consumes a complete Minerva Stable-v1.0.0 project whose semantic
authority is `distributed_markdown_modules`. The embedded
`docs/L2_MinervaBlueprints/` tree must match its canonical source. Do not
substitute a central YAML blueprint or silently omit Atlas-preserved content.

Every Minerva module with generation mode `code` or `test` must have exactly
one realization entry and a valid target file, top-level symbol, declared
public methods, source references, hash, and knowledge-graph edge. Preserve
abstract-to-concrete tool lineage. Generator-owned files may be regenerated;
maintained reference implementations must not be overwritten accidentally.

`Boundary` is reserved for interaction adapters that expose use cases. Tests
and instrumentation use `observation_points`. Code observations and passing
tests are evidence, not stakeholder acceptance.

## Maintain and verify

From Stable-v1.0.0 run:

```powershell
python -m unittest discover -s tests -v
python run_examples.py
python scripts/validate_ecosystem.py
```

The cross-layer audit must prove lossless Atlas payloads, byte-identical
canonical Minerva trees, complete generation-target realization, tool lineage,
and graph coverage. Keep English and Portuguese aligned and preserve historical
edition bytes. Do not publish, tag, push, or create a remote release without
explicit authorization.
