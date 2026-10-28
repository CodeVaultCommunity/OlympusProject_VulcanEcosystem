# Assessment scope

[Português](assessment.pt-br.md)

`evaluate` inspects declared Python source structure, role/naming conventions, selected static import directions and cycles. Paths are normalized to POSIX for graph keys on Windows and POSIX. It does not execute code or prove semantic preservation.

`test` executes canonical scenarios, concrete storage checks, HTTP/CLI lifecycle checks, assessor regressions and the isolated legacy fixture. Successful subtests retain scenario/check IDs; missing expected IDs are `not_run`. Method counts, scenario coverage and supporting checks are separate quantities. Source hashes are captured before execution and checked again afterward. Reports refuse overwriting an earlier run directory.

`verify` adds read-only validation using an explicitly selected compatible external Minerva edition. It records that tool's source hashes and declared version. No fallback, code generation or translation occurs. A missing/incompatible validator or dependency is inconclusive and prevents complete success. The configured GitHub workflow runs local L3 checks only; external L2 integration is separately selected and recorded.

Evidence cannot promote source assumptions into approved requirements. Timing checks measure 30 local CLI invocations through complete captured stdout. Their 2-second target is the source's didactic assumption, not a production SLA. Booking cancellation references the source creation-time procedure; this does not establish cancellation latency. Source input retains that unresolved issue.

Fault doubles show how cases handle acknowledgement loss without retry; they do not demonstrate disk survival under physical power loss. Threaded SQLite checks cover local conditional updates and read consistency. Symlink and POSIX-signal checks may be skipped where unavailable; skips remain visible. Production identity, browser UI, distributed systems, C/Go and hosted CI execution remain outside observed scope.
