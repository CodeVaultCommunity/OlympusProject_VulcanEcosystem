# Verification receipt — Alpha-v0.1.0

[Português](RELEASE.pt-br.md) · [JSON](current.json) · [Summary / resumo](runs/20261028-windows-final/summary.json)

Same unpublished Alpha revised in place. The current run passed on Windows with Python 3.12.14. No remote publication, hosted CI execution or stakeholder approval is asserted.

| Scope / escopo | Result / resultado |
| --- | --- |
| [minimal](runs/20261028-windows-final/minimal/execution.json) | 10 methods; 12 scenarios; 2 supporting checks; all passed |
| [composition](runs/20261028-windows-final/composition/execution.json) | 19 methods; 33 scenarios; 3 supporting checks; all passed |
| [task-board](runs/20261028-windows-final/task-board/execution.json) | 21 methods; 31 scenarios; 7 supporting checks; all passed |
| [L3 tooling / ferramentas](runs/20261028-windows-final/tooling.json) | 13 methods, 1 skipped (directory symlink privilege unavailable) |
| [Legacy technical fixture / fixture legada](runs/20261028-windows-final/legacy-fixture.json) | 19 methods, 1 skipped (POSIX SIGTERM assertion) |
| [Repository tools / ferramentas da raiz](runs/20261028-windows-final/repository-tests.json) | 33 tests passed |
| [Source preservation / preservação das fontes](runs/20261028-windows-final/source-preservation.json) | 3 exact canonical Atlas inputs; inherited Minerva ADPM/scenarios unchanged; observed source hashes match current bytes. |

The edition executed 82 unittest methods: 80 passed and 2 skipped. Scenario/check coverage is a separate count: all 76 scenarios and 12 supports passed. Each of the three examples also passed structural assessment and the explicitly selected external Minerva validator with zero diagnostics. Tool source hashes/version are preserved in its report.

[minimal Minerva](runs/20261028-windows-final/minimal/minerva.json) · [composition Minerva](runs/20261028-windows-final/composition/minerva.json) · [task-board Minerva](runs/20261028-windows-final/task-board/minerva.json)

The local Minerva inputs were read from the unpublished working tree based on commit `5e4da7d`; hashes identify the selected content, not the old commit bytes. The preservation check confirmed equality with that working tree at the recorded time. The original input snapshots and final binding revisions remain separate.

Limits: local SQLite and demo identity; fault doubles do not establish physical disaster durability. Timing records cover 30 CLI requests per relevant source procedure, not a production SLA. Booking cancellation reuses the source creation-time check; cancellation latency remains an open source question. No browser UI, C/Go, Docker, distributed deployment or hosted CI was executed. The two skipped checks are not considered verified. Artwork was unchanged in this revision. Historical reports are retained under `reviews/` and earlier runs, without being reused as current evidence.

Root inventory is generated after this receipt and checked separately; the final commit ID belongs in an external receipt to avoid circular hashes.

## Root organization follow-up

The root was reduced to the agreed entry/governance files, LICENSE and technical Git/CI configuration. Auxiliary documents and dependency files were relocated; task scratch files were preserved outside the repository. All 33 repository-tool tests and the complete edition verification passed again. See the [organization receipt](runs/20261028-root-organization/organization.json) and [edition results](runs/20261028-root-organization/summary.json).
