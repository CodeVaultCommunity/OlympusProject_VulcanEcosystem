# Delivery verification report — Vulcan Ecosystem Alpha-v0.1.0

[Português](RELEASE.pt-br.md) · [Manual](../README.md) · [Requirements](REQUIREMENTS.md) · [Contract review](CONTRACT-REVIEW.md) · [Migration](MIGRATION.md)

**The checks listed below passed in the recorded environment.** This Alpha is supplied for review of the model, formats and examples. It distinguishes document validation, structural assessment, AI-assisted semantic review and observed execution. It does not assert project-owner approval or blanket OAL certification.

## Observed results

| Check | Result and scope |
| --- | --- |
| Realization and assessor | 26 tests passed: 19 application/lifecycle checks and 7 assessor checks; zero failures, errors or skips. |
| Python structure | 14 profile TaskBoard source files assessed with no diagnostic; LegacyReports remains outside the internal architecture profile. |
| Integrated Minerva | 16 documents; 3 cases; 3 behavioral tests; 11 criteria; 28 scenarios; 4 graphs; 15 source bindings checked. |
| Channels and lifecycle | Direct calls, HTTP/CLI, public legacy integration, full/selected startup, readiness identity, partial failure and owned-child cleanup exercised. |
| Distribution tooling | 33 tests passed for inventories, exact content and package checking. |
| Edition isolation | Passed: only the edition directory was copied; commands were invoked from outside it with an external Python environment. |
| Atlas input | Dedicated input validated by the official Atlas Stable-v1.0.0 translator pinned by commit. |
| Artwork and visual integrity | Eight renders and eight SVGs per project; icons preserved byte-for-byte; all images visually reviewed and metadata/hashes checked. |

Counts refer to test methods, not every subcase or assertion. The 33 distribution checks are each repository maintenance suite; they are not additional domain cases.

## Environment and reproduction

- Python: **3.12.14** (CPython).
- Platform: `Linux-6.18.55-x86_64-with-glibc2.39`.
- PyYAML: `6.0.3`; jsonschema: `4.25.1`; pytest: `8.4.2`.
- Commands, timestamps, raw outputs and Python source hashes: [observed/checks.json](observed/checks.json).
- Isolation: [observed/isolation.json](observed/isolation.json).
- Final document check: [observed/final-document-check.json](observed/final-document-check.json).
- Atlas input validator: [observed/atlas-validation.json](observed/atlas-validation.json).
- Artwork: [observed/artwork.json](observed/artwork.json).
- Links and frozen source snapshots: [observed/repository-check.json](observed/repository-check.json).

The edition declares Python 3.11+, but this delivery was observed in the environment above. The configured GitHub Actions Linux/Windows and Python 3.11/3.12 matrix is not reported as already executed.

## Contract preservation

The [review matrix](contract-review.json) links the dedicated Atlas input’s three cases and eleven criteria to ADPM, ADVS and the realization. It records application-generated identity, trimmed title, idempotent completion, insertion ordering, authorization and failure semantics. The source was reconstructed for this demonstration; it is not the different example published by Atlas.

Cross-review corrected qualified Python references accepted under the wrong class, silently excluded app scope, two scenario/test mismatches and the missing list-failure observation. The validator also received a regression for source-record-local graphs. Final document checking added the omitted internal title attribute and recorded the optional completion argument correctly; these last edits did not change the business contract or app code.

## Evidence limits

Automation does not prove every scenario sufficient, arbitrary algorithm equivalence or production identity trust. Simulated connection failures do not establish ambiguous-commit recovery guarantees. HTTP and HTML responses were checked without browser interaction end to end. C/Go adaptations are descriptive; these languages, Docker, load, distributed recovery and remote deployment were not executed.

In Minerva, the model and mirror are documents; the validator never imports or executes the described program. In Vulcan, execution is a separate explicit command, and L2 validation uses the selected vendored Minerva copy. File placement does not erase the L4 responsibility of interaction channels.

## Distribution integrity

The single repository-root `CONTENT-SHA256.json` is generated after final documents and evidence. It records the path, byte size and SHA-256 of every distributed file except the inventory itself. The builder archives only the checked commit and refuses dirty tracked content, stale inventory or temporary artifacts.

The actual ZIP and its extracted tree are audited after packaging. The final commit and ZIP digest belong in the external delivery receipt, avoiding a circular self-reference. Audit the extracted copy before installing dependencies or generating new files:

```bash
python scripts/check_archive.py .
```

This local delivery does not imply remote repository creation, push, tag or GitHub release. The files are organized for review and subsequent publication from the checked content.
