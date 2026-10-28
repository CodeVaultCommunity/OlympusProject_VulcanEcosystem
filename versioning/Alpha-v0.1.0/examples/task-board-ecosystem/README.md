# TaskBoard ecosystem — executable realization

[Português](README.pt-br.md) · [Edition manual](../../README.md)

This is an instantiated Vulcan Ecosystem with two apps. TaskBoard adopts Vulcan Architecture; LegacyReports preserves a procedural interior. Both can run together, or the launcher can select the required subset. The application code is independent of a Vulcan framework.

## Execute from this directory

```bash
python launch.py list
python launch.py start --all
python launch.py start --apps TaskBoard
python launch.py start --apps LegacyReports --duration 2
```

TaskBoard opens `http://127.0.0.1:8765/`; reports open `http://127.0.0.1:8766/report`. Only loopback is selected by the ecosystem launcher. Default example tokens are `demo-editor` and `demo-reader`; environment configuration and trust assumptions are in [execution](../../guides/execution.md). Ctrl+C stops owned child processes and preserves the database file.

## Direct case surfaces

```bash
python apps/TaskBoard/main.py --token demo-editor create --title "Read the contract"
python apps/TaskBoard/main.py --token demo-reader list
python apps/TaskBoard/main.py --token demo-editor complete TASK_ID
python apps/LegacyReports/reports.py report
```

The report command needs the public TaskBoard HTTP service running; the TaskBoard CLI can operate directly without that server. All direct TaskBoard commands share the selected database path. Relative `--db` paths resolve at this ecosystem root.

## Read the sources in their layers

| Location | Read it for |
| --- | --- |
| [Atlas L1](docs/L1_AtlasSpecifications/README.md) | The explicitly reconstructed, example-specific cases and criteria |
| [Minerva L2 blueprint](docs/L2_MinervaBlueprints/blueprint.yaml) | Program/ADVS contracts, source links and graphs |
| `docs/L2_MinervaBlueprints/apps/` | One YAML per code file, including multiple real units in the legacy source |
| [Vulcan L3](docs/L3_Vulcan/README.md) | Inventory, profiles, concrete wiring, resources, execution and evidence |
| [Shared interaction, L4](docs/Shared/interaction.md) | Buttons/routes/commands mapped to the prepared cases and real legacy handlers |

The selected blueprint is reconstructed from this teaching implementation and its specific Atlas source. It does not pretend that the published Atlas Task Board has identical inputs, identity strategy or update contract.

Run all verification from the edition root with `python run_examples.py verify`, or by absolute path to that script from any directory. Application tests alone can be run here with:

```bash
python -m unittest discover -s apps/TaskBoard/tests -p 'Test_*.py' -v
```

The current application suite has 19 methods; the full edition also tests the structural assessor. See [verification](../../verification/README.md) for authoritative reports and limits. The demonstration does not include deployment, production identity, Docker or browser end-to-end testing.
