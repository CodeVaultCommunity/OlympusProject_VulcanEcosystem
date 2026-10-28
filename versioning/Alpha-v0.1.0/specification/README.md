# Adopted Vulcan rules — Alpha-v0.1.0

[Português](README.pt-br.md) · [Edition manual](../README.md) · [OAL alignment](OAL-ALIGNMENT.md)

MUST denotes an obligation within the named scope, SHOULD a recommendation, MAY an option. These are Vulcan's adopted rules. File prefixes, folder names, naming conventions and launcher policies are model/profile decisions; they are not universal OAL requirements. The separate [requirements catalog](../verification/requirements/catalog.json) preserves the original discussion and IDs. [Delivery coverage](../verification/REQUIREMENTS.md) records scope and evidence, not stakeholder acceptance.

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
| VUL-022 | The root mechanism MUST identify apps through a declared registry or discovery policy, start all declared default modes or a selected subset and report failures. |
| VUL-023 | Every mode MUST identify execution mechanism, working directory, configuration, parameters, prerequisites, readiness or completion, and termination. No universal Docker or programming language is required. |
| VUL-024 | Startup MUST declare whether required dependencies are expanded or rejected when missing; readiness order MUST be respected and dependency cycles rejected. |
| VUL-025 | Startup MUST verify the readiness of the intended instance, detect managed service failure and stop only resources it owns or has explicitly been assigned to manage. |
| VUL-026 | The realization MUST define how ADVS behavioral tests and supporting checks are implemented and run, retaining their case and criterion links. |
| VUL-027 | Evidence MUST identify version, actual environment, command, results and limits, distinguishing passed, failed, skipped, configured and unexecuted checks. |
| VUL-028 | The realization MUST reference selected L2 versions and record relevant code/test impact when contracts, permissions, data or dependencies change. |
| VUL-029 | L3 documentation MUST explain app organization, profiles, composition, resources, execution, concrete integration and evidence, referencing canonical contracts and per-file descriptions in L2. |
| VUL-030 | Structural assessment MUST publish the rules and language forms it supports, counterexamples and diagnostics. It MUST distinguish inspection from semantic review and execution and from Minerva validation. |

Discovery may use an explicit registry. The canonical single-app ecosystems use `REGISTRY` in their root launcher; adding a folder does not register an application. The multi-app technical fixture declares dependencies and expands prerequisites. Libraries, base classes and value objects are optional; a required profile area may be empty.
