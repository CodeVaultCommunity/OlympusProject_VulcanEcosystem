# TaskBoard: concrete realization

[Português](README.pt-br.md) · [Inventory](realization.json) · [Test bindings](test-bindings.json) · [Integration procedure](../../../../integrations/minerva/README.md)

`AppComposition` chooses SQLite and injects concrete collaborators. The case applies its authorization first; canonical entities own intrinsic validity. `Boundary_Json` projects results for HTTP and CLI; those interaction choices are L4. Cases are callable without either channel.

The store is an application-scoped capability; connections live for one operation and close in `finally`. Explicit transactions cover reads/writes. Conditional writes use `BEGIN IMMEDIATE`; failed acknowledgements preserve `unknown` and are never automatically retried. Raw record hydration uses the canonical entity constructor. The operator owns the database; shutdown does not delete it.

`Main` is the concrete case domain folder. The selected source does not name a domain. Native `task_id` maps to L2 `task_identifier`; board is bound to the store by composition and checked against caller context. This physical binding preserves board scope without repeating the board parameter in every concrete method.

The designed blueprint snapshot is retained in edition verification sources. Local binding revision adds observations and supporting test references. Planned mappings are separate from observed results. For changes, trace source criterion → case/entity/tool → composition/channel → scenario/support → source mirror → new evidence. Review intended behavior before refreshing hashes.

Limitations: local SQLite demonstration and demo identity; fault doubles cover uncertainty handling, not physical durability under power loss. Scope of each test and measurement appears in the execution report.
