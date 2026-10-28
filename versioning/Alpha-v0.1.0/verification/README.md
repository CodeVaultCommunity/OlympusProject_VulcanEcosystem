# Verification evidence

[Português](README.pt-br.md) · [Edition](../README.md#verification)

Run `python run_examples.py verify` from this edition, or invoke the same file by absolute path. It writes actual reports and returns a nonzero status if structure, tests or the required Minerva gate fail. To keep a new run separate, use `--report-dir PATH`.

| Report | Scope |
| --- | --- |
| [structure.json](structure.json) | Bounded Python AST assessment of 14 TaskBoard sources; LegacyReports is explicitly excluded from that internal profile |
| [execution.json](execution.json) | Runtime/application and assessor unittest methods; exact environment, command, duration, outcomes and limits |
| [minerva.json](minerva.json) | Independent L2 representation and code-binding validation through the declared vendored Minerva version |
| [Source baselines](source-baselines.json) | Selected source revisions, immutable locations and content hashes |
| [Requirement coverage](REQUIREMENTS.md) | Traceable delivery/verification status for the catalog |

The application suite contains 19 methods and the assessor suite 7. Core methods retain the three ADVS identities; supporting tests cover channels, integration, structural negatives and lifecycle. Successful suite execution is not a claim that every possible scenario or acceptance assertion has been independently proved. Some tests use mocks for specific failure paths; actual HTTP/subprocess checks are also included and their scope is described in the guides.

The current reports are evidence of this edition, not transplanted results from the earlier Alpha. No C/Go, Docker, remote deployment, production identity, load test, browser interaction or hosted CI run is implied. POSIX signal assertions are explicitly skipped on other operating systems; any skipped count must remain visible.

Do not commit runtime databases, credentials, bytecode caches or temporary test directories. An observed-source hash can detect a changed file but cannot decide whether a changed behavior is correct; reconcile with L1/L2 before updating it.
