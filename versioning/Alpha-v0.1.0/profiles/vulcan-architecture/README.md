# Vulcan Architecture profile

[Português](README.pt-br.md) · [Edition](../../README.md) · [Rules](../../specification/README.md)

This is an optional internal architecture for an app participating in Vulcan Ecosystem. Select the app, edition, language adaptation and assessed files explicitly. Folder membership does not transfer this profile to neighboring legacy apps.

| Area | Responsibility and example |
| --- | --- |
| `usecases/<Domain>/` | Callable case, authorization and algorithm: `UseCase_CreateTask.py`. |
| `tools/` | Concrete capability and infrastructure guarantees: `Tool_SqliteTaskStore.py`. |
| `entities/` | Canonical intrinsic validity and transitions: `Entity_Task.py`. |
| `value_objects/` | Optional immutable values consumed in production by entities: `ValueObject_TaskIdentity.py`. |

All four sibling areas exist; an empty area is permitted. Minimal does not invent a value object. Support areas `composition/`, `boundaries/`, `support/` and `tests/` are explicitly identified. One principal class/structure per profile source file; filename equals structure name. Core role prefixes are followed by PascalCase, methods use camelCase and attributes snake_case. Python dunder hooks and required HTTP overrides retain framework spelling.

Entities/value objects do not depend on infrastructure, cases or tools. Ready entities are not intrinsically revalidated by tools. Hydration of raw storage is canonical construction. Contextual persistence conditions, transactions, isolation and uncertain outcomes belong to tool contracts. A case independently authorizes trusted context before validation/effects. Operational data is primitive/entity/typed collection; injected collaborators are technical dependencies.

Dependencies are explicit and acyclic. Tools do not consume cases. Cases may compose cases while preserving actor context and each callee's authorization. Booking cancellation concretely composes lookup. `AppComposition` selects implementations and injects collaborators; no base class, container or architecture library is mandatory.

Stores live with the app; connections live per operation and close in `finally`. Explicit SQLite transactions and `BEGIN IMMEDIATE` protect selected read/write guarantees. The operator owns persistent data. Channels project inputs/results and obtain context through the trusted path; they do not own domain validation or permission policy.

The [assessor](../../scripts/evaluate_structure.py) checks bounded Python syntax/import structure. Its graph is static and cannot prove dynamic dependencies or domain preservation. [Negative fixtures](../../tests/fixtures/structural-counterexamples/README.md) exercise diagnostics.

## Descriptive language adaptations

C may associate one principal struct/typedef with receiver-style functions and a declared header/implementation pair. Each physical file still has its own L2 mirror. Document ownership, allocation, linkage, errors and cleanup.

Go may associate receiver methods with a principal struct. Exported names require uppercase initials; record this adaptation instead of claiming literal camelCase. Declare package layout, zero values, constructor use and immutability. C and Go are descriptions only; no compiler/runtime or assessor evidence for them is delivered.
