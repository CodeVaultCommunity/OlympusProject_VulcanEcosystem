# task-board — TaskBoard

[Português](README.pt-br.md) · [Atlas source](docs/L1_AtlasSpecifications/example.atlas.json) · [Minerva](docs/L2_MinervaBlueprints/blueprint.yaml) · [Realization](docs/L3_Vulcan/README.md)

Concrete Python/SQLite realization of the corresponding canonical Atlas Stable-v1.0.0 and Minerva Alpha-v0.1.0 example. Public JSON operations: `create(task_id, title), complete(task_id), list()`. POST the operation name under `/`; use Bearer `demo-editor` for the local demonstration. The caller supplies the domain identifier; input text is preserved.

```sh
python launch.py list
python launch.py start --all --port 8765 --duration 10
python ../../run_examples.py test --example task-board
```

Default mode is loopback HTTP. CLI mode uses `--mode cli --operation NAME --payload JSON`; set `VULCAN_CALLER_TOKEN=demo-editor` in your shell. `--db` selects SQLite storage, `--board` selects TaskBoard scope. See [execution](../../guides/execution.md) for complete commands and lifecycle. Context is resolved by composition, never accepted from a JSON actor object. Direct internal callers are trusted to construct authentic context.

Inherited ADPM/scenarios retain their IDs. Local binding revision and hashes appear in [test bindings](docs/L3_Vulcan/test-bindings.json). Per-file YAML stays in L2; execution outcomes are in the edition's [verification runs](../../verification/README.md). No production authentication or stakeholder acceptance is asserted.
