# Alignment with OAL L3

[Português](OAL-ALIGNMENT.pt-br.md) · [Pinned source](../verification/sources/oal/README.md.txt)

Reference: OAL Stable-v1.0.0, commit `0cc54a19df324ac54857b92b068931cc1b090a10`. Its ADI section defines five obligations for a reusable code organization. Vulcan addresses them as follows.

| OAL ADI obligation | Vulcan realization and review point |
| --- | --- |
| Materialize L2 roles, dependencies, algorithms and failures | Optional internal profile; callable cases, canonical entities, concrete tools; exact Atlas contracts and pinned Minerva intent in each example. |
| Explicit actor-context path and authorization in each case | Composition resolves the demo identity; direct calls accept trusted context; each case denies insufficient context before validation/storage, including composed lookup. |
| Execute ADVS and channel checks with links | Seven logical behavioral tests, 76 scenarios and 12 supporting checks are mapped in `test-bindings.json`; the runner records executed subtests and missing observations. HTTP/CLI checks are separate. |
| Select and supply collaborators; meet concrete guarantees | `AppComposition`, per-operation SQLite transactions, conditional updates, consistent reads, resource closure and failure certainty. |
| Evolution, traceability and evidence | Pinned source bytes, separate binding revision, per-file L2 observations and isolated execution reports with source hashes and environment. |

The source/catalog mapping requires semantic review. Static passes and executed examples are bounded evidence, not certification for arbitrary future projects. Production authentication, distributed guarantees and other languages remain unverified. Naming, four sibling core directories and explicit registry are Vulcan decisions, not requirements imposed by OAL on every L3 model.

L1 owns requested externally meaningful behavior; L2 owns designed program/verification meaning; L3 owns concrete realization; HTTP routes, CLI forms and result projection are L4 choices even when their code is in an L3 artifact. No layer is inferred solely from a directory name.
