# Execution and resource lifetime

[Edition](../README.md) · [Português](execution.pt-br.md)

## App modes

All paths below are relative to `examples/task-board-ecosystem/`. `launch.py` changes each child's working directory to that root. Direct TaskBoard invocations also resolve a relative `--db` against that root. An absolute database path is used unchanged.

| App / mode | Entrypoint | Lifetime and observable completion | Dependencies |
| --- | --- | --- | --- |
| TaskBoard / HTTP, default | `apps/TaskBoard/main.py --db PATH serve --host 127.0.0.1 --port 8765` | HTTP process until interrupted; `/health` identifies app and instance | Local Python and writable SQLite path |
| TaskBoard / CLI | `apps/TaskBoard/main.py --db PATH --token TOKEN create`, `list` or `complete` | One invocation; result JSON or an explicit error/exit code | Same core and SQLite path; no HTTP server required |
| LegacyReports / HTTP, default | `apps/LegacyReports/reports.py --upstream URL serve --port 8766` | HTTP report service until interrupted | TaskBoard public HTTP contract |
| LegacyReports / CLI | `apps/LegacyReports/reports.py --upstream URL report` | One JSON report or upstream error; exit 0 or 5 | TaskBoard public HTTP contract |

The all-apps selection starts the two default HTTP modes, not both HTTP and CLI. The launcher discovers its app registry with `list`. This example's registry and process commands are ordinary Python configuration; Vulcan does not require that implementation or prescribe a universal manifest.

## Configuration

| Setting | Default | Owner and meaning |
| --- | --- | --- |
| TaskBoard database | `.runtime/tasks.sqlite3` under ecosystem root | Operator-owned local data file, preserved after shutdown |
| `TASKBOARD_EDITOR_TOKEN` | `demo-editor` | Demonstration identity with create/read/complete permissions |
| `TASKBOARD_READER_TOKEN` | `demo-reader` | Demonstration read identity; also used by LegacyReports upstream requests |
| `TASKBOARD_TOKEN` | Unset | Convenience default for a direct TaskBoard CLI invocation; `--token` overrides |
| Launcher `--task-port` | `8765` | Loopback TaskBoard HTTP port, range 1–65535 |
| Launcher `--report-port` | `8766` | Loopback LegacyReports port; must differ when both apps run |
| Launcher `--startup-timeout` | `10` seconds | Positive finite per-app readiness timeout |
| Launcher `--duration` | Unset | Nonnegative finite interval after readiness; omitted means remain running |

Editor and reader tokens must be nonempty and distinct. HTTP obtains the credential from `Authorization: Bearer …`, and the trusted composition resolves it. Clients cannot submit permissions or actor context as request fields. A direct caller that constructs an `Entity_ActorContext` is part of the trusted in-process boundary; this example does not establish trust in arbitrary code inside the process. Context is frozen, validates its field types and denies unresolved/unknown/insufficient identities. Production identity proof, token rotation, TLS and remote deployment are outside this example's evaluated scope.

## Startup, readiness and failure

`planApps` expands required dependencies in a deterministic topological order, reports unknown apps and rejects cycles. Selecting LegacyReports therefore includes TaskBoard. A missing dependency is not silently ignored. Runtime commands create a unique launch instance identifier and pass it to both owned children.

Readiness requires a responding `/health` with the expected app, `ready: true`, the matching instance identifier and a still-live child. A foreign service occupying a port cannot satisfy that check. Here readiness means that initial composition succeeded and the HTTP handler is accepting requests; it does not promise future storage or upstream availability. Each subsequent request still handles its applicable dependency failures.

During startup the launcher observes already-started dependencies; during steady execution it observes its children. Failure to start, timeout or a child exiting leads to nonzero failure and cleanup of the other owned children. The registry does not start descendant process trees, external containers or daemons. Supporting such resources would require an explicit ownership/lifetime adapter rather than killing unrelated processes by port or name.

The launcher sends termination to its owned direct children, waits up to three seconds per child, then kills an owned child that did not exit. A SIGTERM or Ctrl+C to the launcher follows the same owned cleanup path. Termination does not promise rollback of every in-flight operation and never deletes the operator's database. SQLite connections use bounded per-operation lifetime; process handles and temporary test resources are released in test cleanup.

## Failure projections

The domain/behavioral contract is authoritative in [the selected L2 blueprint](../examples/task-board-ecosystem/docs/L2_MinervaBlueprints/blueprint.yaml). Channel projections are documented in [Shared interaction](../examples/task-board-ecosystem/docs/Shared/interaction.md). The CLI uses 0 for success, 3 for forbidden, 2 for domain/input errors, 4 for missing task and 5 for storage failure. Argument parsing/configuration errors also use 2 and may be usage text rather than domain JSON. LegacyReports collapses its upstream failure into its explicitly documented error/exit 5.

The current SQLite realization is synchronous. It has no deferred job identity, cancellation API, optimistic revision contract, cross-database transaction or promise to distinguish every possible uncertain commit. A future requirement for those outcomes must first be reflected in the selected L1/L2 contracts and then implemented and verified.

## Reproduce the lifecycle checks

```bash
python run_examples.py test
python run_examples.py start --all --duration 1 --task-port 8875 --report-port 8876
```

The suite checks full and partial selection, dependency expansion, invalid selections, cycles, instance mismatch, occupied ports, cleanup after partial startup and SIGTERM on POSIX. It also checks the kill fallback with a controlled test double. These evidence scopes are distinct; a controlled fallback assertion is not a test of every real process-tree behavior.
