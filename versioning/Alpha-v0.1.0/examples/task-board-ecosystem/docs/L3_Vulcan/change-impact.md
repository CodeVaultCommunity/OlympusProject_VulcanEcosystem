# Change-impact exercise

**Status: illustrative analysis, not an implemented change.** The current code and selected sources retain their current title rule. This record demonstrates VUL-028; it does not silently amend L1/L2.

## Example A — propose a different title limit

| Responsibility | Affected artifact/identity | Required action before claiming a new realization |
| --- | --- | --- |
| L1 obligation | `AC-TASK-001-INVALID` in the selected Atlas instance | Decide the new requirement and revise the authoritative source; preserve the case identity if its meaning remains the same |
| L2 program | `RULE-TASK-TITLE`, `ENT-TASK`, canonical construction and related algorithm description | Review the changed invariant and affected capability assumptions |
| L2 verification | `BT-TASK-001`, `SC-TASK-001-INVALID` and boundary-related expectations | Define positive/negative edge values and observable results before accepting a source update |
| L3 implementation | `ValueObject_TaskTitle.__post_init__` | Implement the revised canonical bound once; tools continue to use canonical construction |
| L4 interaction | Browser input bound in `Boundary_Http.renderPage` and the identified channel contract | Keep the user-facing restriction aligned with the selected domain requirement |
| L3 checks | `Test_TaskCases.testCreateTask`, `testCanonicalValuesAndContext`, `Test_Boundaries.testBrowserPageAndHttpFailureProjection` | Update affected scenarios, rerun actual tests and review compatibility |
| L2 mirror / L3 evidence | Per-file records and verification reports | Update hashes only after semantic reconciliation; record newly executed scope without overwriting historical meaning |

No existing case needs a new ID merely because the source filename or implementation changes. Conversely, keeping an ID does not prove behavioral preservation. An unresolved disagreement remains a pending issue rather than a false conformance claim.

## Example B — move an implementation file without changing behavior

A future relocation of `UseCase_CreateTask.py` retains `UC-TASK-001` and its acceptance criteria. Update imports/composition, the physical binding and corresponding L2 mirror location, plus the L3 organization reference. Run structural evaluation and the affected tests. If the move violates the selected `usecases/<Domain>/` rule, either correct the move or explicitly revise the chosen profile; do not disguise it by changing only a hash.

This exercise has not moved any file and has not changed the title limit. Current execution evidence applies to the unchanged implementation packaged in this edition.
