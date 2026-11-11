# Stable-v1.0.0 release verification

This local edition establishes the first stable Vulcan realization contract.
No remote publication or stakeholder approval is asserted.

## Delivered contract

- Exact consumption of Minerva Stable-v1.0.0 distributed Markdown modules.
- One traceable Python file/symbol for every Minerva `code` or `test` target.
- Public-method validation against each `minerva-design-json` record.
- Abstract protocols and concrete SQLite tool adapters with explicit lineage.
- Boundary reserved for use-case interaction adapters; scenario instrumentation
  uses `observation_points`.
- A merged knowledge graph containing the Minerva graph plus every
  module-to-code `realized_by` edge.
- Stable schemas for realization ledgers and knowledge graphs.

## Current local verification

| Example | Minerva modules | Code mappings | Runtime tests | Graph nodes | Graph edges |
| --- | ---: | ---: | ---: | ---: | ---: |
| Minimal | 22 | 7 | 10 | 120 | 420 |
| Composition | 26 | 12 | 19 | 237 | 992 |
| Task board | 28 | 12 | 21 | 227 | 969 |

Five Vulcan stable-contract tests pass. All 50 runtime contract tests pass.
The cross-layer audit passes for all three examples and proves:

1. canonical Atlas JSON equals Minerva's lossless `/atlas` payload;
2. embedded Minerva trees equal the canonical Stable-v1.0.0 trees byte for
   byte;
3. all 31 generation targets have valid files, symbols, methods, hashes, and
   graph links.

Machine-readable results are stored in
`verification/ecosystem-validation.json`.

