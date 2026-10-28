# Verification records

[Português](README.pt-br.md) · [Current receipt](RELEASE.md) · [Requirements](REQUIREMENTS.md) · [Contract review](CONTRACT-REVIEW.md)

`source-baselines.json` pins exact OAL/Atlas/Minerva input snapshots. `sources/` contains documentary inputs, not copied validator code. `requirements/` preserves catalog IDs and scoped delivery mapping. `runs/<id>/` contains immutable observed executions; each invocation creates a new directory. `reviews/baseline-78232f2/` preserves reports received before this revision as historical evidence only.

`test-bindings.json` in each example identifies expected scenarios/checks and native tests. The execution report separately records actual subtests, statuses, input/source hashes, platform, timing and skips. Structural and Minerva reports are separate. The overall result cannot pass when an expected scenario is absent or an explicitly required integration check is unavailable.
