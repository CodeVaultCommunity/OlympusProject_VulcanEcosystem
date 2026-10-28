# TaskBoard ecosystem realization — L3

[Português](README.pt-br.md) · [Realization record](realization.json) · [Example](../../README.md)

This document records the concrete organization and operation of the selected realization. The canonical program, flows, data contracts, scenarios and per-source-file mirror are in [Minerva L2](../L2_MinervaBlueprints/blueprint.yaml). The selected L1 is [the reconstructed Atlas instance](../L1_AtlasSpecifications/task-board.atlas.json), not the independently published Atlas Task Board example. Interaction projection remains [identified L4](../Shared/interaction.md).

## Inventory and profile

| App | Internal organization | Modes | Assessment scope |
| --- | --- | --- | --- |
| TaskBoard | Vulcan Architecture, Python; support for composition, tests and L4 boundaries | HTTP default; direct CLI | 14 Python sources structurally assessed, three selected cases and supporting runtime checks |
| LegacyReports | Existing procedural/module style; functions and one handler in `reports.py` | HTTP default; report CLI | Public integration and lifecycle; no claim of Vulcan Architecture internal organization |

The application code root is `apps/`. No abstract support library is required. The legacy source remains multi-unit, and its per-file Minerva description represents that actual structure. Source hashes and member-level descriptions are authoritative in L2, not repeated here.

## Concrete composition

`apps/TaskBoard/composition/AppComposition.py` selects `Tool_SqliteTaskStore` for logical capability `TOL-TASK-STORE` and constructs the implementations of `UC-TASK-001`, `UC-TASK-002` and `UC-TASK-003`. Each case receives the store directly. The main entry supplies those prepared cases and the trusted context resolver to its selected boundary.

The UUID generation strategy, SQLite backend and insertion ordering are implementation selections tied to the selected blueprint. The store creates an entity canonically before insertion; that construction is not moved into the create case. The entity delegates title validity to its internal value object. The static implementation graph is available in [the structural report](../../../../verification/structure.json); its logical meaning is in Minerva.

SQLite connections are scoped per store operation and explicitly closed. The file persists across application compositions and remains operator-owned. HTTP servers own sockets; the launcher owns only the direct processes it starts. Domain refusal precedes store access in case execution, while infrastructure composition can prepare the database schema before handling requests.

## Execution and integration

The root `launch.py` discovers both apps and starts either all default modes or the selected subset. Its dependency policy expands LegacyReports to include TaskBoard, rejects cycles and verifies each launch instance through health metadata. It cleans owned children after startup failure, interruption or managed-child exit. It does not control external daemons or erase the database.

LegacyReports uses TaskBoard's public HTTP operation with a read identity; no private TaskBoard import or direct database access is used. The primitive transport representation is defined in [interaction](../Shared/interaction.md). The [execution guide](../../../../guides/execution.md) records commands, working directory, environment defaults, readiness meaning and completion/shutdown behavior for every mode.

## Source selection, traceability and evidence

The realization selects Minerva Blueprints `Alpha-v0.1.0`, YAML profile `0.1.0`, document `MINERVA-TASKBOARD`, revision `1`. That blueprint selects Atlas `Stable-v1.0.0`, document `ATLAS-VULCAN-TASKBOARD`, revision `1`. The frozen reference sources and their hashes are [recorded with the edition](../../../../verification/source-baselines.json).

The three behavioral links are `BT-TASK-001` → `Test_TaskCases.testCreateTask`, `BT-TASK-002` → `testListTasks` and `BT-TASK-003` → `testCompleteTask`. Additional tests support authorization ordering, canonical values, selected failures, channels, integration and lifecycle. Expected criteria/scenarios stay in ADVS; [execution.json](../../../../verification/execution.json) reports what actually ran. [minerva.json](../../../../verification/minerva.json) reports the separate L2/code-binding check.

The scope does not include full browser interaction, C/Go execution, Docker, production identity, distributed transactions or hosted CI. The [change-impact exercise](change-impact.md) demonstrates preserving source responsibility during an update. A successful structural or schema gate does not silently widen any of these claims.
