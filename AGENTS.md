# Agent guide for Vulcan Ecosystem

## Select the edition

Respect an edition requested by the user. This repository currently contains Alpha-v0.1.0; choose its manual and tooling together. Do not substitute another model/profile version silently. Root READMEs are illustrated introductions; versioning/Alpha-v0.1.0/README.md is normative and README.pt-br.md is its translation.

## Locate contracts

Read the selected edition manual, relevant profile guide and verification/REQUIREMENTS.md before implementation changes. Check verification/source-baselines.json for the pinned OAL and Atlas references. Preserve the separate meanings of specification, realization and observed evidence.

For an application ecosystem, docs/ at the root is recommended. Use L1_AtlasSpecifications, L2_MinervaBlueprints, L3_Vulcan and Shared for the adopted materials. The per-file YAML mirror belongs in L2. L3 documents concrete organization, composition, execution and evidence. Libraries and abstract base classes remain optional.

## Maintain the edition

Keep English and Portuguese aligned, preserve IDs, update links and validate examples using edition-local commands. The requirements catalog distinguishes source obligations and design decisions; do not promote code observations or test passes into stakeholder approval. Mark limitations and unsupported profiles explicitly. Preserve historical edition bytes when adding future versions.

## Verify and distribute

Run the edition tests and example checks and inspect changed artwork. From the root, use scripts/check_repository.py and scripts/tests. Update evidence before generating CONTENT-SHA256.json. Stage intended delivery files, generate the inventory last, verify it and commit locally. Follow docs/releasing.md for ZIP creation and extraction checks. The final commit and ZIP digest belong in an external receipt to avoid circular hashes. A ZIP request does not imply permission to push or publish remotely.

## Unpublished Alpha revision

Continue improving Alpha-v0.1.0 in place until the user requests another edition. Use specification/ for adopted rules, profiles/ for optional architecture, integrations/ for explanatory manual derivation only, and examples/minimal, composition and task-board for the canonical Atlas/Minerva family. Do not implement a translator or reintroduce vendor/. Old divergent business behavior is isolated in tests/fixtures/. Full verify requires an explicitly selected external Minerva edition; do not claim complete integration when it is unavailable. Keep new runs separate from historical reports.

## Keep the root focused

Root documentation is limited to README.md, README.pt-br.md, AGENTS.md, CLAUDE.md, CHANGELOG.md, VERSION, CONTENT-SHA256.json and LICENSE. Keep citation, contribution and acknowledgements under docs/; development requirements under scripts/; artwork dependencies under assets/sources/. Store task scratch files outside the repository. Hidden Git/CI configuration and assets/, docs/, scripts/, versioning/ remain at the root.
