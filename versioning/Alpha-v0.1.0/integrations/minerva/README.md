# Minerva → Vulcan: manual realization procedure

[Português](README.pt-br.md) · [Model](../../README.md) · [Canonical examples](../../examples/README.md)

Target Minerva Alpha-v0.1.0 / YAML profile 0.1.0 and Vulcan Alpha-v0.1.0. This guide describes the translation decisions; it does not implement a translator. The three example programs were authored and reviewed as concrete realizations.

1. Select the source edition, document ID/revision, Atlas origin and exact hashes. Preserve the original blueprint as an input snapshot. Record unresolved source questions before writing code.
2. Inventory cases, actor policies, entities, tools, dependencies, ADVS scenarios and shared checks. Keep case and criterion identity; a channel does not create another logical case.
3. Select applications, architecture profiles and language adaptations. Allocate cases to declared domains, canonical validity to entities, infrastructure capabilities to tools, and concrete selection/injection to composition.
4. Record operational names, representations, absence/failure outcomes and technical injections. Preserve validation order, exact text, same-context composition and write certainty. Document any proposed semantic deviation and seek source review; code observations cannot silently replace intent.
5. Author the callable core and selected channels. Choose concrete resources/transactions that satisfy the source guarantees. Declare identity trust, resource owner/lifetime, configuration, readiness and shutdown.
6. Implement each ADVS scenario and shared check. Maintain a mapping to test path and symbol; distinguish authored tests from observed runs. Add channel and runtime tests separately.
7. Describe every selected source file in the L2 mirror. Keep the full extension (`Entity_Task.py.yaml`). Observations include source hashes and lexical symbols; they do not infer stakeholder requirements. Keep L3 composition/evidence in `docs/L3_Vulcan/`.
8. Execute structural inspection, the selected Minerva validator, scenario tests and channel checks. Record missing, failed, skipped and uncertain results. Review source changes and refresh affected observations before creating a new evidence run.

| Minerva element | Concrete location / decision |
| --- | --- |
| Case identity, algorithm, authorization | `apps/<App>/usecases/Main/UseCase_*.py`; one callable method per selected case. `Main` is the concrete domain folder; these source blueprints do not select a named domain. |
| Entity invariants and transitions | `entities/Entity_*.py`; optional encapsulated value objects. |
| Tool capability and failure guarantee | `tools/Tool_Sqlite*Store.py`; transaction/locking implementation in `support/SqliteResource.py`. |
| Abstract dependencies | Constructor injection selected in `composition/AppComposition.py`; Booking cancellation receives the lookup case and forwards the same context. |
| Operational task_identifier | Native parameter/field `task_id`; value preserved exactly. |
| Authorized board | Concrete store instance `board_id`, bound by composition; each TaskBoard case checks matching trusted context. |
| Case-to-test identity and scenario | `docs/L3_Vulcan/test-bindings.json` plus subtest IDs; seven logical tests can have many native methods. |
| Designed ADPM/ADVS | Exact original in `verification/sources/minerva/`; local L2 binding revision `<source>-vulcan-1` adds observations without changing intended behavior. |
| Execution | Immutable `verification/runs/<id>/` with input/source hashes, host and subtest outcomes. No test run rewrites the blueprint. |

The local binding blueprint is `mixed`: its ADPM and scenario intent are inherited design; its per-file mirrors are source observations. Native signatures and lexical steps describe implementation details, while operational typing and semantic contracts remain in ADPM. The pinned source's pending owner-review decision is preserved.

The external Minerva validator is selected by `--minerva-edition`. Its declared edition/profile and source hashes are recorded; absent dependencies or incompatible editions cannot yield a complete pass. Validation is read-only and does not implement this derivation procedure. It checks the declared source catalogue; it does not independently parse/prove every Atlas requirement.
