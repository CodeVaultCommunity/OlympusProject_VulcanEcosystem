# Assessment, evidence and limits

[Edition verification](../README.md#verification) · [Português](assessment.pt-br.md)

## Three separate questions

Structural assessment asks whether supported source forms follow the chosen organization. Minerva validation asks whether a selected L2 representation and its links are coherent. Runtime tests ask whether implemented scenarios produce the observed outcomes. None of those results substitutes for the others, and their conjunction still has the recorded environment and scenario limits.

The edition's full entry `python run_examples.py verify` runs these gates separately and returns nonzero if one fails or a required gate cannot run. Reports are outputs of actual commands. A static reference to a test symbol is traceability, not a claim that the test ran. A schema being valid is not proof that code preserves a contract.

## Python assessor

```bash
python scripts/evaluate_structure.py --ecosystem examples/task-board-ecosystem --profile-app TaskBoard --legacy-app LegacyReports --technical-file apps/TaskBoard/main.py --json
```

Use repeated `--profile-app` / `--legacy-app` options to declare the scope. `--entry` changes the root entry filename. `--technical-file` explicitly identifies language bootstrapping files for review; the assessor rejects classes hidden inside that exception. `--json REPORT` writes a machine-readable report; `--json` alone writes JSON to standard output. A diagnostic contains rule, path, line where available, severity and message. Exit 1 means a structural error; argument errors use argparse exit 2.

| Rule family | Implemented inspection |
| --- | --- |
| `ECO_APPS`, `ECO_ENTRY` | Presence of apps directory and a local root entry file; existence does not demonstrate execution |
| `ECO_CLASSIFICATION` | Declared profile/legacy paths, conflicting classification and warnings for unclassified apps |
| `VA_AREAS`, `VA_DOMAIN` | Four core areas and use-case placement within a domain subdirectory |
| `VA_SINGLE_STRUCTURE`, `VA_FILE_NAME`, `VA_ROLE_NAME` | Python class count including nested classes, no standalone functions without explicit adaptation, matching filename and role spelling |
| `VA_METHOD_CASE`, `VA_ATTRIBUTE_CASE` | Defined method and class/self-attribute spellings, with known Python and HTTP hook adaptations |
| `VA_DEPENDENCY_DIRECTION` | Recognized static imports that violate core direction, plus review warnings for cross-app imports |
| `VA_VALUE_OBJECT_CONSUMER`, `VA_PURE_DATA` | Direct value-object consumption by an unsupported role and a bounded list of infrastructure imports in data structures |
| `VA_STATIC_CYCLE` | Cycles in recognized local static import edges, including case/tool relationships |
| `PYTHON_SYNTAX` | Python parsing, readable sources and explicit refusal of a selected profile with no Python sources |

The assessor supports the source forms demonstrated by TaskBoard. It does not establish runtime call edges, inspect reflection, discover dynamic imports, prove dependency purity against every possible library, infer a public API from an import, or evaluate type/behavioral equivalence. Known HTTP overrides are recognized for direct `BaseHTTPRequestHandler` inheritance; other frameworks require a declared adaptation and, where needed, an evaluator extension.

It does not treat the existence or absence of `docs/` as conformance by itself and does not inspect YAML. Documentation content, actor-context trust, operational I/O meaning, source-to-code preservation, production identity and resource guarantees outside the tested paths need the appropriate separate review. C and Go are not implemented evaluator languages.

## Negative and positive evidence

The [counterexample fixture](../examples/structural-counterexamples/README.md) intentionally violates ten diagnostic families. Tests confirm these failures, positive assessment of TaskBoard, missing areas/entry, syntax errors, relative-import direction and acceptance of an alternative documentation location. The fixture is not a runnable product or a second example claiming conformance.

Runtime tests verify selected observable guarantees, including refusal before injected tool access, construction/normalization and immutable values, persistence between compositions, a mocked connection failure, HTTP/CLI projection, live loopback integration, full/selected startup, occupied-port preservation and owned-process cleanup. Some failure paths use controlled doubles; live process tests and mocked assertions are identified by their test names and documentation. Passing those paths does not establish all concurrency, crash recovery or fault combinations.

## Release decision and change impact

A release must preserve the selected sources, local execution commands and the requirement coverage evidence. Compare authoritative source contracts before updating observed file hashes. If a title-length requirement changed, review the Atlas criterion, Minerva data/algorithm/ADVS, canonical value object, affected boundary constraints and tests. If only a source file moved, update its physical binding/mirror while retaining the unchanged logical case identity. Neither action is just a blind hash refresh.

The illustrative impact record is in [L3 change impact](../examples/task-board-ecosystem/docs/L3_Vulcan/change-impact.md). It is a reasoned change exercise, not a claim that the hypothetical change has been implemented. Historical and current reports must remain distinguishable.
