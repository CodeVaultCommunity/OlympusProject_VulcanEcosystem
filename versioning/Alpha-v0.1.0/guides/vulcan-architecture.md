# Vulcan Architecture profile

[Edition rules](../README.md#reference-rules) · [Português](vulcan-architecture.pt-br.md)

## Applicability

Vulcan Ecosystem organizes cooperating applications. An application selects Vulcan Architecture explicitly; another may retain a procedural, functional, framework-specific or existing architecture. A claim identifies app, language adaptation, edition, assessed files and limitations. Folder membership never transfers the profile to neighboring apps.

The four core roles are `UseCase_`, `Tool_`, `Entity_` and `ValueObject_`. They are responsibilities of code organization, not required classes from a support library. The running example instantiates ordinary concrete Python classes. Its constructors receive collaborators directly, and `AppComposition` selects the implementations once.

## Units and names

| Role | Example path | Principal structure |
| --- | --- | --- |
| Use case in a declared domain | `usecases/TaskManagement/UseCase_CreateTask.py` | `UseCase_CreateTask` |
| Concrete capability | `tools/Tool_SqliteTaskStore.py` | `Tool_SqliteTaskStore` |
| Domain data and intrinsic behavior | `entities/Entity_Task.py` | `Entity_Task` |
| Encapsulated value | `value_objects/ValueObject_TaskTitle.py` | `ValueObject_TaskTitle` |
| Composition support | `composition/AppComposition.py` | `AppComposition` |
| Channel adapter, identified L4 | `boundaries/Boundary_Http.py` | `Boundary_Http` |

The filename stem equals the principal class/struct name. Methods use camelCase, such as `createTask`; attributes use snake_case, such as `task_store`. Support files also keep one principal structure. A technical process entry may contain language-required or bootstrapping functions, but that exception does not authorize hiding application operations in an unclassified script.

Python examples use namespace packages: no empty `__init__.py` files are needed. `main.py` is an explicit technical entry exception. Python hooks such as `__init__` and `__post_init__`, and the HTTP framework's `do_GET`, `do_POST` and `log_message`, retain their required spellings. These exceptions are listed in structural evidence. LegacyReports is excluded from the internal profile instead of receiving ad hoc exemptions for each procedural function.

Invalid examples include two independent classes in one file, `Entity_Task.py` containing `Tool_Task`, a `create_task` method, a `taskStore` attribute, or a use case placed directly under `usecases/` without a domain. The [published counterexample](../examples/structural-counterexamples/README.md) exercises these and dependency violations.

## Responsibility and dependency

Entities own canonical validity and intrinsic transitions. They do not acquire a database connection, read a request or resolve an identity. Value objects represent immutable values, their equality and invariants; the profile confines their direct production consumption to entities. Tests may inspect a value object directly to verify that promise.

Tools implement capabilities such as persistence or an external request. A tool may receive primitives and construct/hydrate an entity through its canonical constructor. This is different from independently repeating an entity's intrinsic validation. Context-dependent conditions such as an existing storage row, transport failure or transaction scope belong in the capability contract. Authorization of the use case remains in the case.

Use cases preserve their logical case identity, declared domain and selected behavior. Their public operational parameters/results use primitives, entities and typed collections; constructor collaborators are technical dependencies. A prepared use case can be called directly or through multiple channels. It receives trusted actor context and denies insufficient access before calling a domain-effecting collaborator. When cases compose other cases, each case still checks its own permission, and the caller propagates context without silently upgrading it.

Concrete dependencies must be explicit and acyclic. Case-to-case and tool-to-tool collaboration is permitted when the selected logical model calls for it; tools do not depend on use cases. An algorithm loop is not a dependency cycle. The example has no case-to-case or tool-to-tool edge: the three cases share one store, while entities depend only on their value object and language support. The actual static graph is recorded in [structure.json](../verification/structure.json); the abstract graph remains in the L2 blueprint.

## Composition and resources

`AppComposition` constructs a concrete SQLite tool and passes that tool to three concrete use cases. It also resolves the local demonstration tokens into entity context at the trusted edge. Neither the whole composition object nor an ambient service locator is passed as an operational input to a case.

The store's lifetime is an application instance. SQLite connections are opened per operation and closed with `contextlib.closing`; the connection context commits successful writes and rolls back on exceptions. A database file remains owned by the operator, so process cleanup never deletes task data. Startup schema creation is an infrastructure action before request handling; authorization promises concern domain operations, not the absence of all infrastructure initialization.

## Language adaptations: descriptive, not executed

### C

A declared C adaptation associates one principal `struct`/`typedef` with functions whose receiver parameter and naming identify that structure. `Entity_Task.h` and `Entity_Task.c` can be an explicitly declared declaration/implementation pair for the same unit. Every physical code file still receives its own Minerva mirror record, and both records reference the same logical element where appropriate. Functions belonging to another structure require another unit. Linkage, opaque handles, allocation, ownership, error returns and cleanup must be declared; neither a macro nor a header is a new architecture role.

### Go

A Go adaptation associates receiver methods with one principal struct and retains the chosen filename/type correspondence. Unexported methods can use camelCase and internal fields snake_case. Exported methods need an uppercase initial under Go's language rules; a profile must explicitly record this exception, for example `GetId` instead of `getId`, rather than claiming exact camelCase compliance. Package layout, exported surface, constructor usage, zero-value behavior and immutable-value conventions must be specified for a concrete implementation. The presence of a Go struct alone does not establish these guarantees.

No C or Go code is compiled or tested by this edition. The Python assessor returns evidence only for Python forms it supports; it is not a cross-language architecture validator. An implementation in a new language needs its own assessment and execution evidence.
