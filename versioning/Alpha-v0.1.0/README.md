# Vulcan Ecosystem — Alpha-v0.1.0

**A reusable OAL L3 model for organizing and realizing an ecosystem in code.** Vulcan belongs to the Olympus Project, alongside Atlas Specifications (L1) and Minerva Blueprints (L2). Vulcan Architecture is an optional internal organization profile for an application participating in the ecosystem.

[Português](README.pt-br.md) · [Quick start](#quick-start) · [Reference rules](#reference-rules) · [Verification](#verification) · [Conformance](#conformance) · [Release notes](#release-notes)

This English edition is normative. The Portuguese manual is its coordinated translation. **Alpha** means that the model, tooling and representation may change incompatibly in later editions. The runnable example is a bounded demonstration, not a production platform or a certification of all OAL obligations.

## Model and responsibility

OAL Stable-v1.0.0 is the selected reference. Atlas supplies externally meaningful contracts; Minerva specifies the abstract domain program and its behavioral verification; Vulcan realizes the selected program, tests, concrete composition and runtime organization. Interaction decisions remain L4 even when their code physically resides in an application's `boundaries/` directory.

| Artifact or decision | Authoritative responsibility in this edition |
| --- | --- |
| Cases, stakeholder criteria, permissions and externally required outcomes | Atlas L1 instance |
| Domain contracts, logical components, algorithms, states, dependency meaning and ADVS scenarios | Minerva L2 blueprint |
| Per-source-file mirror, symbols, descriptive flows and realization bindings | Minerva L2 mirror; observed facts are identified as observations |
| App inventory, architecture profile, implementation choices, concrete dependency wiring, execution and observed evidence | Vulcan L3 documentation |
| HTTP routes, CLI parsing, browser controls and channel projections | Identified L4 material in the example |
| Glossary, provenance and material shared across layers | `Shared/`, with links to canonical definitions |

Folders do not change the layer of a responsibility. A semantic contract is not duplicated as a competing L3 definition. The model does not require a universal YAML for an ecosystem, a container, an abstract class, a `VulcanUseCase` base class, an interface hierarchy or an injection framework.

The normative sources are frozen in [source baselines](verification/source-baselines.json), [OAL English](verification/sources/oal/README.md.txt) and [Atlas English](verification/sources/atlas/README.md.txt). The executable demo uses its own Atlas instance, `ATLAS-VULCAN-TASKBOARD`, revision `1`; it does **not** claim to implement the separately published Atlas Task Board example unchanged.

## Quick start

Python 3.11 or later is the declared source requirement. The recorded run identifies the exact interpreter and host actually tested. Application execution and structural assessment use the standard library; complete verification additionally uses the declared, vendored Minerva validator and its pinned Python dependencies.

Run from this edition directory:

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run_examples.py verify
.venv/bin/python run_examples.py list
.venv/bin/python run_examples.py start --all
```

On Windows use `.venv\Scripts\python.exe` instead of `.venv/bin/python`. That spelling is an installation adaptation, not evidence of a Windows test. The HTTP services bind to `127.0.0.1`: TaskBoard at `http://127.0.0.1:8765/`, LegacyReports at `http://127.0.0.1:8766/report`. Ctrl+C stops the children started by the launcher. Ports and database path can be changed explicitly.

A short run and a selection are also real executions:

```bash
python run_examples.py start --all --duration 2 --task-port 8875 --report-port 8876
python run_examples.py start --apps TaskBoard
python run_examples.py start --apps LegacyReports
```

Selecting LegacyReports includes TaskBoard, its declared prerequisite. Default modes are HTTP services; `--all` does not run maintenance commands or every available mode. Entrypoints resolve resources from their own location and can be invoked by absolute path from another working directory.

The same cases can be invoked from a terminal:

```bash
python examples/task-board-ecosystem/apps/TaskBoard/main.py --token demo-editor create --title "Review the blueprint"
python examples/task-board-ecosystem/apps/TaskBoard/main.py --token demo-reader list
python examples/task-board-ecosystem/apps/TaskBoard/main.py --token demo-editor complete TASK_ID
python examples/task-board-ecosystem/apps/LegacyReports/reports.py report
```

Replace `TASK_ID` with the identifier returned by creation. The demonstration tokens are local example identities. The trust boundary and environment settings are documented in [execution](guides/execution.md); they are not a production authentication design.

## Organization

Every instantiated ecosystem MUST provide `apps/`, one identifiable directory per app, and an implemented root entry mechanism. `docs/` is recommended, with the following homes for adopted models:

| Path in an instantiated ecosystem | Purpose |
| --- | --- |
| `apps/<App>/` | Application code, in any supported language and internal architecture |
| `docs/L1_AtlasSpecifications/` | Atlas instances and links to externally meaningful contracts |
| `docs/L2_MinervaBlueprints/` | Blueprints and the per-source-file mirror |
| `docs/L3_Vulcan/` | Organization, concrete composition, execution, integration and evidence references |
| `docs/Shared/` | Suggested name for shared support material |
| A root entry such as `launch.py` | Discover and start all default apps or a chosen subset |

The information is required where specified; these documentation directory names are recommended. A different location does not itself invalidate conformance when references remain recoverable. Unused layers do not require empty placeholder directories. This specification repository has its own editorial organization; the instantiated ecosystem is [the executable example](examples/task-board-ecosystem/README.md).

## Reference rules

In the following rules, **MUST** is an obligation within the named scope, **SHOULD** is a recommendation, and **MAY** is permitted. Requirements for the Vulcan Architecture profile do not silently apply to legacy apps. The IDs link to the requirement catalog shipped with this edition; this table states the adopted rules, while the coverage report records implementation and evaluation status separately.

| ID | Scope and rule |
| --- | --- |
| VUL-001 | The model MUST identify itself as OAL L3 and distinguish ecosystem, architecture profile, L2 sources and L4 interaction. |
| VUL-002 | An ecosystem MUST have `apps/`, per-app directories and a functioning root entry. It SHOULD use the documented layer-oriented documentation layout. |
| VUL-003 | Every app MUST declare identity, language, internal profile, available modes and the scope of any conformance claim. |
| VUL-004 | Other architectures MAY participate without internal refactoring. Their public operations and unavailable or unassessed internals MUST be described faithfully. |
| VUL-005 | Vulcan Architecture apps MUST expose sibling `usecases/`, `tools/`, `entities/` and `value_objects/` areas. An area may be empty; artificial classes are not required. Support areas MUST be identified. |
| VUL-006 | Profile use cases MUST belong to `usecases/<Domain>/`. A domain folder does not itself grant permission. |
| VUL-007 | A profile source file MUST have one principal class or equivalent structure and its associated members. Independent structures require separate files; mandatory language exceptions MUST be identified. |
| VUL-008 | Structure names MUST combine a role prefix and PascalCase for core roles; methods use camelCase, attributes snake_case, and the filename stem equals the structure name. Framework spellings require a documented adaptation. |
| VUL-009 | A language adaptation MUST preserve responsibility and identify deviations required by the language, including C declaration/implementation pairs and Go exported identifiers. Description and executed evidence MUST be distinguished. |
| VUL-010 | Value objects MUST be immutable, infrastructure-independent and invariant-bearing. Direct production consumption is confined to entities; public core data does not expose value objects. |
| VUL-011 | Entities MUST enforce canonical intrinsic validity at construction and permitted change without depending on tools, use cases or infrastructure. Persistent identity is not a universal requirement for all entities. |
| VUL-012 | Tools MUST realize technical capabilities under declared contracts. They MUST NOT assume use-case authorization or duplicate intrinsic validation of an already valid entity. Hydration uses canonical construction; contextual checks remain explicit. |
| VUL-013 | Each case MUST realize its selected logical identity and remain callable independently of HTTP, CLI or another particular channel. |
| VUL-014 | Core operational inputs and outputs MUST be primitives, entities or typed collections of them. Technical collaborators and resources MUST be distinguished from operational data. Meaningful absence, empty results and representations MUST be explicit. |
| VUL-015 | Every case MUST receive actor context through an explicit trusted path and authorize before domain effects. Missing, unresolved, unknown or insufficient context is denied; anonymous access requires explicit admission. |
| VUL-016 | Composition MUST identify selected collaborators and inject what each case needs. No library, abstract base class, container or injection framework is mandatory. |
| VUL-017 | Concrete case-to-case and tool-to-tool dependency graphs MUST be explicit and acyclic and link to L2 meaning. Tools MUST NOT consume use cases. Composed cases preserve context and each case's authorization. |
| VUL-018 | Implementations MUST preserve distinct success, absence, failure and, where specified, partial or uncertain results. Cancellation does not imply rollback unless the selected contract guarantees it. |
| VUL-019 | Composition and tools MUST identify resource owner/lifetime and release resources on applicable success and failure paths. |
| VUL-020 | In profile/OAL-assessed scopes, channels MUST adapt context, data and results to prepared cases, preserving domain ownership. Interaction responsibility MUST be identified as L4. Legacy handlers remain their real operations. |
| VUL-021 | Apps MUST integrate through documented public operations, without private imports or direct access to another app's domain storage. Representation, compatibility and failure behavior MUST be explicit. |
| VUL-022 | The root mechanism MUST discover apps, start all declared default modes or a selected subset and report failures. |
| VUL-023 | Every mode MUST identify execution mechanism, working directory, configuration, parameters, prerequisites, readiness or completion, and termination. No universal Docker or programming language is required. |
| VUL-024 | Startup MUST declare whether required dependencies are expanded or rejected when missing; readiness order MUST be respected and dependency cycles rejected. |
| VUL-025 | Startup MUST verify the readiness of the intended instance, detect managed service failure and stop only resources it owns or has explicitly been assigned to manage. |
| VUL-026 | The realization MUST define how ADVS behavioral tests and supporting checks are implemented and run, retaining their case and criterion links. |
| VUL-027 | Evidence MUST identify version, actual environment, command, results and limits, distinguishing passed, failed, skipped, configured and unexecuted checks. |
| VUL-028 | The realization MUST reference selected L2 versions and record relevant code/test impact when contracts, permissions, data or dependencies change. |
| VUL-029 | L3 documentation MUST explain app organization, profiles, composition, resources, execution, concrete integration and evidence, referencing canonical contracts and per-file descriptions in L2. |
| VUL-030 | Structural assessment MUST publish the rules and language forms it supports, counterexamples and diagnostics. It MUST distinguish inspection from semantic review and execution and from Minerva validation. |

The profile is detailed in [Vulcan Architecture](guides/vulcan-architecture.md). [Legacy and boundaries](guides/legacy-and-boundaries.md) explains interoperability without imposing that profile on LegacyReports.

## Verification

```bash
python run_examples.py evaluate
python run_examples.py test
python run_examples.py verify
```

`evaluate` inspects the declared Python structure. `test` runs the application and assessor suites. `verify` requires both and validates the L2 blueprint/mirror through the bundled Minerva CLI. Reports are written under `verification/`; use `--report-dir PATH` for a new evidence location. A failure is nonzero, and missing vendored L2 resources fail the complete verification rather than silently skipping it.

| Evidence | Meaning |
| --- | --- |
| [structure.json](verification/structure.json) | Actual Python files inspected, rule IDs, adaptations, dependency edges and diagnostics |
| [execution.json](verification/execution.json) | Actual test count, environment, command, durations and per-test status |
| [minerva.json](verification/minerva.json) | Separate L2 validation result, including source bindings when requested |
| [Requirement coverage](verification/REQUIREMENTS.md) | Per-requirement delivery and verification scope; not an inference from file counts |
| [Negative fixtures](examples/structural-counterexamples/README.md) | Deliberate violations and the diagnostics expected from the assessor |

The recorded suite contains 26 unittest methods: 19 application/lifecycle checks and 7 assessor checks. The tests cover the three case identities directly, HTTP/CLI projection, public legacy integration, authorization refusal, canonical title validity, selected storage failure, startup selection, dependency cycles, foreign-instance rejection and owned-process cleanup. Subcases are not counted as separate test methods. Tests actually executed and their current outcomes are authoritative in `execution.json`.

There is no evidence here of C/Go execution, Docker execution, production authentication, browser interaction end to end, load handling, distributed transaction safety or a hosted GitHub CI run. C/Go are documented adaptations. The pages are served and checked as HTTP responses; no browser automation claim follows. See [assessment scope](guides/assessment.md).

## Conformance

A claim MUST identify the model and edition, OAL reference, selected profile, target artifact/app, applicable rules, evidence and limits. Participation in an ecosystem is distinct from adoption of the internal architecture profile. TaskBoard uses the Python Vulcan Architecture profile; LegacyReports is an intentionally different architecture participating through a public HTTP contract.

`model.json` is editorial model metadata, not a mandatory application manifest. The sample [realization record](examples/task-board-ecosystem/docs/L3_Vulcan/realization.json) is one concrete L3 documentation format; it does not introduce a second universal schema alongside Minerva. [The example's L3 README](examples/task-board-ecosystem/docs/L3_Vulcan/README.md) links decisions, composition, tests and execution.

Passing the Python assessor proves only its declared syntactic checks. Passing Minerva validation checks the selected representation and links, not implementation behavior. Passing the test suite proves its observed scenarios in the recorded environment. A model-level or OAL conformance assessment still requires the published scope and semantic review; no blanket certificate is implied.

## Versioning

`Alpha-v0.1.0` is the human-facing edition identifier. The optional Python project metadata uses `0.1.0a0` because Python packaging has its own version grammar. Each edition owns its manual, guides, example, tests, tooling, selected source snapshots and dependency declarations. Copying this directory retains its execution entrypoints; no command depends on repository-root scripts.

Keep prior published editions reproducible. A future change records source and target editions, changed obligations, compatibility and migration. Implementation fixes that change observed behavior require corresponding source/blueprint review and new evidence. Changing an artifact hash is not itself a semantic migration decision.

The [migration map](verification/MIGRATION.md) traces the older combined specification to the separated responsibilities. Its editorial correspondences are distinct from runtime evidence.

## Release notes

This edition separates Vulcan L3 realization from Minerva L2 documentation. The file mirror now lives under `docs/L2_MinervaBlueprints/`, while L3 documents its own concrete organization and operation. `docs/` is recommended; `apps/` and the initializer remain mandatory for instantiated ecosystems.

The runnable example retains its didactic identity generation, canonical entity construction, trimmed title and idempotent completion. It adds explicit source/criterion links, a bounded Python assessor with counterexamples, expanded negative tests and lifecycle checks, and a local verification entrypoint. No abstract architecture library was introduced.

The source is derived from the earlier Vulcan Alpha example and revised for the current responsibility split. Historical reports are not reused as evidence of this edition. The [source baseline record](verification/source-baselines.json) preserves provenance; current reports record current execution.
