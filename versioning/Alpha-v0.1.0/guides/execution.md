# Execution contracts

[Português](execution.pt-br.md) · [Edition](../README.md)

The three canonical examples are independent single-app ecosystems. Root `launch.py` contains an explicit `REGISTRY`; `list` reports it, `start --all` selects default modes and `start --apps APP` selects the registered app. Unknown apps are rejected before initialization. The edition runner requires `--example NAME` to start one ecosystem. It does not combine unrelated examples into one app.

HTTP is the default mode, bound to `127.0.0.1`. Readiness is printed only after binding/listening and includes a unique instance ID also returned by `/health`. `--port 0` requests an ephemeral port. Ctrl+C or a positive finite `--duration` ends the service and closes its socket. Startup failure is nonzero; an occupied port is rejected without terminating another service. The sequential demo HTTP server is not a production concurrent service.

CLI performs one operation, prints one JSON result and exits. Success is zero; domain refusal/failure is nonzero. Configuration/usage errors are separate. Default SQLite storage is `work/demo.sqlite3` relative to the ecosystem; `--db PATH` overrides it. `--board` defaults to `board-A` for TaskBoard. `VULCAN_DEMO_TOKEN` configures the demo identity (default `demo-editor`); `VULCAN_CALLER_TOKEN` supplies CLI credentials. HTTP uses `Authorization: Bearer ...`. Do not supply an actor object as credentials.

PowerShell, from the edition directory:

```powershell
$env:VULCAN_CALLER_TOKEN = 'demo-editor'
python examples/task-board/launch.py start --mode cli --operation create --payload '{"task_id":"TASK001","title":"Review Atlas"}'
python examples/task-board/launch.py start --mode cli --operation complete --payload '{"task_id":"TASK001"}'
python examples/task-board/launch.py start --mode cli --operation list
python run_examples.py start --example composition --apps BookingDesk --port 8766 --duration 10
```

In POSIX shells, use `export VULCAN_CALLER_TOKEN=demo-editor` instead. Direct calls construct `AppComposition(db_path)` and invoke its prepared case with trusted `Entity_ActorContext`; the caller must be part of the trusted application. The demo token resolver is not a production identity provider.

The [legacy fixture](../tests/fixtures/legacy-ecosystem/README.md) demonstrates multiple apps, prerequisite expansion, instance-specific readiness, child failure and cleanup of owned processes only. It is technical evidence, not the canonical TaskBoard contract.
