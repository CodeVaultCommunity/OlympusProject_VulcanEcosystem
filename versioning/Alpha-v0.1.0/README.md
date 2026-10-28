# Vulcan Ecosystem — Alpha-v0.1.0

[Português](README.pt-br.md) · [Rules](specification/README.md) · [OAL alignment](specification/OAL-ALIGNMENT.md) · [Verification](verification/README.md)

**Vulcan is a reusable OAL L3 / ADI model for organizing and realizing applications in code.** This English manual is normative; Portuguese is its coordinated translation. This is the same unpublished Alpha-v0.1.0, revised in place. It is not a new release or a production platform.

## Model and responsibilities

Atlas L1 specifies externally meaningful contracts. Minerva L2 specifies the program, ADVS and per-file descriptions. Vulcan L3 realizes those contracts, composes concrete collaborators and records execution evidence. Interaction choices belong to L4, including HTTP/CLI code inside the concrete artifact. [Source baselines](verification/source-baselines.json) pin OAL Stable-v1.0.0, Atlas Stable-v1.0.0 and the selected Minerva Alpha inputs.

An ecosystem MUST have `apps/`, identifiable app directories and a functioning root entry mechanism. Each app declares its language, architecture, modes, public operations and assessment scope. Other architectures may participate without adopting [Vulcan Architecture](profiles/vulcan-architecture/README.md). Libraries, abstract base classes, containers and injection frameworks are optional.

## Organization

| Location in an instantiated ecosystem | Responsibility |
| --- | --- |
| `apps/<App>/` | Concrete application code and tests. |
| `docs/L1_AtlasSpecifications/` | Canonical externally meaningful contracts. |
| `docs/L2_MinervaBlueprints/` | Designed blueprint and per-file observation mirror. |
| `docs/L3_Vulcan/` | Organization, composition, execution, bindings and evidence references. |
| `docs/Shared/` | Shared explanations, provenance and identified L4 interaction choices. |
| `launch.py` or another root entry | Explicit registration/discovery; all default modes or selected apps. |

The documentation names and root `docs/` are recommended. Alternative locations must keep the information recoverable. This repository's editorial layout separates `specification/`, `profiles/`, `integrations/`, `guides/`, `templates/`, `examples/`, `scripts/`, `tests/` and `verification/` within the edition.

## Reference rules

The normative [VUL-001 through VUL-030 rules](specification/README.md) identify obligations and their scope. Profile obligations apply only to apps selecting that profile. Discovery may use an explicit registry; adding a directory does not automatically register an app. See [execution](guides/execution.md) for startup, ownership and failure contracts.

## Quick start

Use Python 3.11 or later. Application code, structural checks and tests use the standard library. From this edition:

```sh
python run_examples.py list
python run_examples.py evaluate
python run_examples.py test
python run_examples.py start --example task-board --all --duration 10
```

For the complete cross-model check, install `requirements.txt` and explicitly select the compatible external Minerva edition:

```sh
python -m pip install -r requirements.txt
python run_examples.py verify --minerva-edition /path/to/L2-MinervaBlueprints/versioning/Alpha-v0.1.0
```

No validator is vendored. Missing or incompatible Minerva yields an inconclusive integration result and a nonzero overall exit. The command validates existing artifacts; it does not translate or generate models/code. Every check invocation creates a unique `verification/runs/` directory; `--report-dir` must identify an empty/new location.

## Canonical examples

| Example | Source and purpose |
| --- | --- |
| [minimal](examples/minimal/README.md) | Request submission: exact code, positive quantity, duplicate refusal and uncertain writes. |
| [composition](examples/composition/README.md) | Booking lookup/create/cancel: same-context composition and conditional versioned writes. |
| [task-board](examples/task-board/README.md) | Caller-supplied task IDs, board isolation, revision conflicts, retention and consistent listing. |

All three preserve the corresponding Atlas source bytes and Minerva logical/scenario IDs. The old divergent TaskBoard and LegacyReports now live in a [technical fixture](tests/fixtures/legacy-ecosystem/README.md), solely for heterogeneous startup and public integration checks. [Negative fixtures](tests/fixtures/structural-counterexamples/README.md) test the bounded assessor. Atlas revision-2/revision-3 evolution variants are not additional runnable Vulcan examples in this Alpha.

## Integration and evolution

[Minerva integration](integrations/minerva/README.md) explains manual derivation, decision points, aliases, source pinning, test mapping and impact review. It supplies documentation only. A local blueprint binding revision adds source observations without changing inherited ADPM or scenario intent. Source changes require explicit semantic review, changed bindings and fresh evidence; a hash update alone does not authorize a semantic change.

## Conformance and verification

Claims MUST name edition, OAL reference, selected profile, target, applicable rules, evidence and limits. Structural inspection, Minerva validation, scenario execution and stakeholder approval have distinct meanings. Missing scenarios are reported as `not_run`; skipped tests are retained. [Assessment](guides/assessment.md), [requirements](verification/REQUIREMENTS.md) and the [current verification receipt](verification/RELEASE.md) delimit results.

`model.json`, `realization.json` and `test-bindings.json` are documentation choices for this repository, not mandatory universal L3 schemas. Tests measure local Python/SQLite behavior and selected channels. They do not establish production identity, distributed guarantees, C/Go support or a production SLA.

## Versioning

Keep `Alpha-v0.1.0` and Python metadata `0.1.0a0`. Future published editions must preserve historical bytes. This revision improves an unpublished candidate in place; see [migration](verification/MIGRATION.md). An edition can run its own L3 checks independently of root scripts; integration still requires the explicitly selected external Minerva validator.

## Release notes

Canonical examples replace the divergent business example; integrations are explanatory; EN/PT manuals are present at root and edition; Windows dependency inspection and scenario evidence are corrected. No translation engine, new edition, remote publication or automatic acceptance is introduced.
